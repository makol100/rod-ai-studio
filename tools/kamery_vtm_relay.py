#!/usr/bin/env python3
"""Hik-Connect VTM relay for the ROD camera page.

The script deliberately keeps account credentials and camera media keys out of
the command line and logs.  It has two operations:

* ``fetch-keys`` exchanges a one-time Hik-Connect MFA code for the three media
  decryption keys and stores them in a mode-0600 JSON file.
* ``relay`` receives one VTM MPEG-PS stream, decrypts its HEVC NAL payloads and
  publishes H.264 to the private RTSP URL supplied by go2rtc's ``{output}``.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn
from urllib.parse import parse_qs, unquote, urlsplit

from hikcloudstream.client import HikConnectClient
from hikcloudstream.models import Camera, Credentials, StreamType
from hikcloudstream.stream.session import open_live_stream
from pyezvizapi.__main__ import _BufferedStreamPayloadDecryptor


DEFAULT_SOURCES = Path("/root/go2rtc-hik/cfg/ezviz_zrodla_docelowe.txt")
DEFAULT_KEYS = Path("/root/rod-ai-studio/data/.secrets/hikconnect_media_keys.json")
DEFAULT_MFA = Path("/tmp/n_kamery_live/mfa.txt")


@dataclass(frozen=True)
class Source:
    name: str
    username: str
    password: str
    serial: str
    channel: int


def fail(message: str, code: int = 1) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr, flush=True)
    raise SystemExit(code)


def load_sources(path: Path) -> dict[str, Source]:
    """Parse go2rtc-style ``name:`` + ``- ezviz://...`` source pairs."""

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        fail(f"cannot read source configuration: {exc}")

    sources: dict[str, Source] = {}
    current_name: str | None = None
    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not stripped.startswith("-") and stripped.endswith(":"):
            current_name = stripped[:-1].strip()
            continue
        if not stripped.startswith("- ezviz:"):
            continue
        if not current_name:
            fail("ezviz source without a preceding stream name")

        value = stripped[2:].strip()
        parsed = urlsplit(value)
        if parsed.scheme != "ezviz" or not parsed.username or parsed.password is None:
            fail(f"invalid ezviz source for {current_name}")
        serial = parsed.path.strip("/")
        if not serial:
            fail(f"missing device serial for {current_name}")
        query = parse_qs(parsed.query)
        try:
            channel = int(query.get("channel", ["1"])[0])
        except ValueError:
            fail(f"invalid channel for {current_name}")
        sources[current_name] = Source(
            name=current_name,
            username=unquote(parsed.username),
            password=unquote(parsed.password),
            serial=serial,
            channel=channel,
        )

    if not sources:
        fail("no ezviz sources found")
    credentials = {(item.username, item.password) for item in sources.values()}
    if len(credentials) != 1:
        fail("all configured cameras must use one Hik-Connect account")
    return sources


def login(source: Source) -> HikConnectClient:
    client = HikConnectClient()
    client.login(Credentials(source.username, source.password))
    return client


def query_media_key(client: HikConnectClient, serial: str, mfa_code: str) -> str:
    """Use the full web-client request expected by query/encryptkey."""

    payload = client.request_json(
        "POST",
        "/api/device/query/encryptkey",
        data={
            "checkcode": mfa_code,
            "serial": serial,
            "clientNo": "web_site",
            "clientType": 3,
            "netType": "WIFI",
            "featureCode": client._feature_code,
            "sessionId": client.session_id,
        },
    )
    result_code = str(payload.get("resultCode"))
    key = payload.get("encryptkey")
    if result_code != "0" or not isinstance(key, str) or not key:
        fail(f"media key request failed for {serial}: resultCode={result_code}")
    return key


def command_fetch_keys(args: argparse.Namespace) -> None:
    sources = load_sources(args.sources)
    try:
        mfa_code = args.mfa_file.read_text(encoding="utf-8").strip()
    except OSError as exc:
        fail(f"cannot read MFA file: {exc}")
    if not (4 <= len(mfa_code) <= 12) or not mfa_code.isalnum():
        fail("MFA file must contain one 4-12 character alphanumeric code")

    first = next(iter(sources.values()))
    client = login(first)
    keys: dict[str, str] = {}
    try:
        for item in sources.values():
            if item.serial not in keys:
                keys[item.serial] = query_media_key(client, item.serial, mfa_code)
    finally:
        client.close()

    args.keys.parent.mkdir(parents=True, exist_ok=True)
    previous_umask = os.umask(0o177)
    try:
        args.keys.write_text(json.dumps(keys, sort_keys=True) + "\n", encoding="utf-8")
    finally:
        os.umask(previous_umask)
    os.chmod(args.keys, 0o600)
    print(f"OK: stored {len(keys)} media keys in mode 0600", flush=True)


def load_key(path: Path, serial: str) -> str:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read media key file: {exc}")
    key = payload.get(serial) if isinstance(payload, dict) else None
    if not isinstance(key, str) or not key:
        fail(f"media key is missing for {serial}")
    return key


def ffmpeg_command(output: str) -> list[str]:
    if not output.startswith("rtsp://127.0.0.1:"):
        fail("go2rtc output must be a private localhost RTSP URL")
    return [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-fflags",
        "+genpts+nobuffer",
        "-flags",
        "low_delay",
        "-probesize",
        "2000000",
        "-analyzeduration",
        "3000000",
        "-f",
        "mpeg",
        "-i",
        "pipe:0",
        "-map",
        "0:v:0",
        "-an",
        "-vf",
        "scale=640:360:flags=fast_bilinear",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-tune",
        "zerolatency",
        "-profile:v",
        "baseline",
        "-g",
        "16",
        "-keyint_min",
        "16",
        "-sc_threshold",
        "0",
        "-b:v",
        "700k",
        "-maxrate",
        "800k",
        "-bufsize",
        "400k",
        "-rtsp_transport",
        "tcp",
        "-f",
        "rtsp",
        output,
    ]


def command_relay(args: argparse.Namespace) -> None:
    sources = load_sources(args.sources)
    try:
        source = sources[args.name]
    except KeyError:
        fail(f"unknown stream name: {args.name}")
    media_key = load_key(args.keys, source.serial)
    client = login(source)
    camera = Camera(1, source.name, source.serial, source.channel, source.name)
    process: subprocess.Popen[bytes] | None = None

    def stop(_signum: int, _frame: object) -> None:
        if process and process.poll() is None:
            process.terminate()

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    try:
        with open_live_stream(
            client,
            camera,
            stream_type=StreamType.SUB,
            timeout=15.0,
        ) as session:
            stream_info = session.start()
            if stream_info.result not in (0, None):
                fail(f"VTM negotiation failed: result={stream_info.result}")
            process = subprocess.Popen(ffmpeg_command(args.output), stdin=subprocess.PIPE)
            if process.stdin is None:
                fail("ffmpeg stdin is unavailable")
            decrypt = _BufferedStreamPayloadDecryptor(media_key, codec="hevc")
            print(
                f"OK: VTM relay started for {source.name}; publishing private RTSP",
                file=sys.stderr,
                flush=True,
            )
            try:
                for body in session.iter_rtp_packets():
                    clear = decrypt(body)
                    if clear:
                        process.stdin.write(clear)
                        process.stdin.flush()
                    if process.poll() is not None:
                        fail(f"ffmpeg exited: code={process.returncode}")
            except (BrokenPipeError, ConnectionResetError):
                fail("stream pipeline connection closed")
            tail = decrypt.flush()
            if tail and process.poll() is None:
                process.stdin.write(tail)
            process.stdin.close()
            code = process.wait(timeout=10)
            if code != 0:
                fail(f"ffmpeg exited: code={code}")
    finally:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        client.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--keys", type=Path, default=DEFAULT_KEYS)
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch = subparsers.add_parser("fetch-keys")
    fetch.add_argument("--mfa-file", type=Path, default=DEFAULT_MFA)
    fetch.set_defaults(handler=command_fetch_keys)

    relay = subparsers.add_parser("relay")
    relay.add_argument("--name", required=True)
    relay.add_argument("output")
    relay.set_defaults(handler=command_relay)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
