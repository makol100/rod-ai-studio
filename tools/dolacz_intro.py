#!/usr/bin/env python3
"""Dokleja kanoniczne intro „Wiadomości z ogrodu" przed wydanie (D-0350:
„Dodawać do wszystkich wiadomości zawsze"). 0 USD.

Użycie: python3 tools/dolacz_intro.py WYDANIE.mp4 [--wyjscie PLIK.mp4]

Sklejka przez filter_complex concat z pełną normalizacją (scale+fps+pix_fmt,
audio 48 kHz stereo) — NIE concat-demuxerem (lekcja 08.09: różne pix_fmt
urywały obraz w połowie). Po sklejce: liczenie klatek vs suma oczekiwana
i zrzut klatki z końca — bramka fail-closed.
"""
import argparse
import subprocess
import sys
from pathlib import Path

INTRO = Path("/root/rod-ai-studio/assets/intro_wiadomosci/INTRO_WIADOMOSCI_C_v1.mp4")
FPS = 30


def _probe(plik: Path, entries: str, strumien: str = "v") -> str:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", strumien,
                        "-show_entries", entries, "-of", "csv=p=0", str(plik)],
                       capture_output=True, text=True, check=True)
    return r.stdout.strip()


def _klatki(plik: Path) -> int:
    return int(subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(plik)],
        capture_output=True, text=True, check=True).stdout.strip())


def dolacz(wydanie: Path, wyjscie: Path) -> None:
    if not INTRO.exists():
        sys.exit(f"BLAD: brak kanonu intro {INTRO}")
    w, h = _probe(wydanie, "stream=width,height").split(",")[:2]
    if (w, h) != ("1080", "1920"):
        sys.exit(f"BLAD: wydanie {w}x{h}, oczekiwane 1080x1920 (pion)")
    ma_audio = bool(_probe(wydanie, "stream=codec_type", "a"))
    if not ma_audio:
        sys.exit("BLAD: wydanie bez sciezki audio — dokleic audio przed intro")

    norm = ("scale=1080:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,"
            f"fps={FPS},format=yuv420p")
    fc = (f"[0:v]{norm}[v0];[1:v]{norm}[v1];"
          "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];"
          "[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];"
          "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", str(INTRO), "-i", str(wydanie),
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    "-c:a", "aac", "-ar", "48000", "-b:a", "192k",
                    "-movflags", "+faststart", str(wyjscie)],
                   check=True, capture_output=True)

    # bramka: klatki wyjscia ~= intro + wydanie (tolerancja 3 klatki na fps/concat)
    k_intro, k_wyd, k_out = _klatki(INTRO), _klatki(wydanie), _klatki(wyjscie)
    if abs(k_out - (k_intro + k_wyd)) > 3:
        sys.exit(f"BLAD BRAMKI: klatki {k_out} != {k_intro}+{k_wyd}")
    kadr = wyjscie.with_suffix(".koniec.png")
    dl = float(_probe(wyjscie, "format=duration", "v").split(",")[-1] or 0) \
        if False else k_out / FPS
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{dl - 0.2:.2f}",
                    "-i", str(wyjscie), "-frames:v", "1", str(kadr)],
                   check=True, capture_output=True)
    print(f"OK: {wyjscie} | klatki {k_out} = intro {k_intro} + wydanie {k_wyd}"
          f" | kadr z konca: {kadr}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("wydanie")
    ap.add_argument("--wyjscie", default="")
    a = ap.parse_args()
    wydanie = Path(a.wydanie)
    wyjscie = Path(a.wyjscie) if a.wyjscie else wydanie.with_name(
        wydanie.stem + "_z_intro.mp4")
    dolacz(wydanie, wyjscie)
