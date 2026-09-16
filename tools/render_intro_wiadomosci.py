#!/usr/bin/env python3
"""Render intro „Wiadomości z ogrodu" (wariant C Belzebuba, D-0349).

Deterministycznie: playwright ładuje intro.html, czeka na fonty, potem dla
każdej klatki woła window.ustawKlatke(t) i robi screenshot. ffmpeg składa
30 fps H.264 yuv420p + dżingiel Mixkit 1145 przycięty do 5 s z wyciszeniem.
Koszt: 0 USD. Wyjście: assets/intro_wiadomosci/INTRO_WIADOMOSCI_C_v1.mp4
"""
import subprocess
import sys
from pathlib import Path

BAZA = Path("/root/rod-ai-studio/assets/intro_wiadomosci")
KLATKI = BAZA / "klatki"
FPS = 30
CZAS = 5.0
AUDIO = Path("/root/rod-ai-studio/assets/audio/kandydaci/mixkit_1145.mp3")
WYJSCIE = BAZA / "INTRO_WIADOMOSCI_C_v1.mp4"


def renderuj_klatki() -> int:
    from playwright.sync_api import sync_playwright
    KLATKI.mkdir(exist_ok=True)
    n = int(FPS * CZAS)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--allow-file-access-from-files"])
        page = browser.new_page(viewport={"width": 1080, "height": 1920},
                                device_scale_factor=1)
        page.goto((BAZA / "intro.html").as_uri())
        page.evaluate("document.fonts.ready.then(()=>window._fonty=1)")
        page.wait_for_function("window._fonty===1", timeout=15000)
        page.wait_for_timeout(300)  # logo PNG
        for i in range(n):
            page.evaluate(f"window.ustawKlatke({i / FPS:.6f})")
            page.screenshot(path=str(KLATKI / f"{i:04d}.png"))
        browser.close()
    return n


def zloz() -> None:
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(FPS), "-i", str(KLATKI / "%04d.png"),
        "-i", str(AUDIO),
        "-filter_complex",
        f"[1:a]atrim=0:{CZAS},afade=t=out:st=4.2:d=0.8,"
        f"loudnorm=I=-16:TP=-1.5[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-ar", "48000", "-b:a", "192k",
        "-t", str(CZAS), "-movflags", "+faststart",
        str(WYJSCIE),
    ], check=True, capture_output=True)


if __name__ == "__main__":
    n = renderuj_klatki()
    print(f"klatek: {n}")
    zloz()
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames",
                        "-select_streams", "v", "-show_entries",
                        "stream=nb_read_frames,width,height,r_frame_rate",
                        "-of", "csv=p=0", str(WYJSCIE)],
                       capture_output=True, text=True)
    print("kontrola:", r.stdout.strip())
    print("plik:", WYJSCIE, WYJSCIE.stat().st_size, "B")
    sys.exit(0)
