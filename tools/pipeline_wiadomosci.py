#!/usr/bin/env python3
"""Jedna bezkosztowa komenda: tekst + gotowy awatar/audio + czolowka -> final + kontrola ust.

Nie uruchamia historycznych platnych submitow. Nowe TTS/awatar wymagaja osobnej
zgody i dostarczenia plikow; testy korzystaja z istniejacych czesci w data/.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], capture=False):
    print("+", " ".join(map(str, cmd)), flush=True)
    return subprocess.run(cmd, cwd=ROOT, check=True, capture_output=capture, text=capture)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("tekst", type=Path)
    p.add_argument("--awatar-video", type=Path, required=True)
    p.add_argument("--tts-audio", type=Path, help="opcjonalnie podmien dzwiek awatara")
    p.add_argument("--czolowka", type=Path, default=ROOT / "assets/izabela/CZOLOWKA_CANON.mp4")
    p.add_argument("--eksport", type=Path, required=True)
    p.add_argument("--planowane-ciecia", type=int, default=0,
                   help="ciecia wewnatrz gotowego awatara, oczekiwane przez scenariusz")
    p.add_argument("--test-offline", action="store_true",
                   help="pozwol odnotowac POMINIETA kontrole ust, tylko dla danych istniejacych")
    p.add_argument("--zaplac", action="store_true", help="zarezerwowane; nie uruchamia platnosci bez adaptera")
    args = p.parse_args()
    for item in (args.tekst, args.awatar_video, args.czolowka):
        if not item.is_file():
            p.error(f"brak pliku: {item}")
    text = args.tekst.read_text(encoding="utf-8").strip()
    if not text:
        p.error("tekst jest pusty")
    if args.zaplac:
        raise SystemExit("BRAK ADAPTERA PLATNEGO: nie wyslano TTS ani awatara; potrzebna zgoda Tomasza na test")
    args.eksport.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="wiadomosci_", dir="/tmp") as td:
        body = Path(td) / "body.mp4"
        if args.tts_audio:
            if not args.tts_audio.is_file():
                p.error(f"brak audio: {args.tts_audio}")
            run(["ffmpeg", "-y", "-v", "error", "-i", str(args.awatar_video), "-i", str(args.tts_audio),
                 "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-shortest", str(body)])
        else:
            body = args.awatar_video
        guard = run([sys.executable, str(ROOT / "tools/straznik.py"), str(body), "--kwestia", text,
                     "--exp-w", "1080", "--exp-h", "1920", "--final", str(args.planowane_ciecia),
                     "--freeze-ok", "--json"], capture=True)
        print(guard.stdout)
        result = json.loads(guard.stdout)
        lips = result["strażnicy"]["usta_sync"]["status"]
        if lips == "POMINIĘTY" and not args.test_offline:
            raise SystemExit("STOP: kontrola ust POMINIETA; eksport produkcyjny zabroniony")
        if lips == "FAIL":
            raise SystemExit("STOP: kontrola ust FAIL")
        normalized = []
        for number, source in enumerate((args.czolowka, body)):
            target = Path(td) / f"norm_{number}.mp4"
            run(["ffmpeg", "-y", "-v", "error", "-i", str(source),
                 "-vf", "scale=1080:1920,setsar=1,fps=30", "-af", "aresample=48000",
                 "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-c:a", "aac",
                 "-ar", "48000", "-ac", "2", "-avoid_negative_ts", "make_zero", str(target)])
            normalized.append(target)
        concat = Path(td) / "concat.txt"
        concat.write_text("".join(f"file '{item}'\n" for item in normalized), encoding="utf-8")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
             "-c", "copy", "-movflags", "+faststart", str(args.eksport)])
    probe = run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration",
                 "-of", "json", str(args.eksport)], capture=True)
    print(json.dumps({"status": "TEST_OFFLINE" if args.test_offline else "OK", "kontrola_ust": lips,
                     "eksport": str(args.eksport), "ffprobe": json.loads(probe.stdout)},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
