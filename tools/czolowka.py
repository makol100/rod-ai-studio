#!/usr/bin/env python3
"""CZOLOWKA WIADOMOSCI DZIALKOWYCH — 6 sekund, robiona kodem (koszt zero).

Decyzja Tomasza 4.08.2026: „6" (z propozycji 5/6/7 sekund).
Przebieg wg rozpiski Henia, przeskalowanej z 7 s na 6 s.
Zastrzezenie Zenka: czolowka rozgrywa sie NA kanonicznym studiu, nie na osobnej planszy —
zeby wygladala na otwarcie serwisu, a nie doklejke z przodu.

Wynik: mp4 1080x1920, 30 fps, 180 klatek.
"""
import argparse
import math
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

KATALOG = Path("/root/rod-ai-studio")
TLO_PUSTE = KATALOG / "assets/izabela/TLO_STUDIO_PUSTE_CANON.png"
STUDIO_Z_IZA = KATALOG / "assets/izabela/STUDIO_IZABELI_CANON_v3.png"
LOGO = KATALOG / "assets/branding/rod_profilowe.png"

SZER, WYS, FPS, SEKUND = 1080, 1920, 30, 6
KLATEK = FPS * SEKUND                      # 180

TYTUL = "WIADOMOŚCI DZIAŁKOWE"
PODTYTUL = "ROD im. Józefa Lompy w Woźnikach"
ZLOTY = (196, 158, 74)

CZCIONKI = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def czcionka(rozmiar, gruba=True):
    for s in (CZCIONKI if gruba else CZCIONKI[::-1]):
        if Path(s).exists():
            return ImageFont.truetype(s, rozmiar)
    return ImageFont.load_default()


def plynnie(t):
    """Wygladzenie 0..1 — bez szarpania na starcie i na koncu."""
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def klatka(nr, tlo_img, studio_img, logo_img):
    """Buduje jedna klatke czolowki. nr: 0..179"""
    s = nr / FPS                            # sekunda

    # ---------- 0,0-0,9 s: SWIATLA STUDIA (wyjscie z czerni) ----------
    if s < 0.9:
        a = plynnie(s / 0.9)
        kadr = Image.new("RGB", (SZER, WYS), (0, 0, 0))
        jasne = ImageEnhance.Brightness(tlo_img).enhance(a)
        kadr = Image.blend(kadr, jasne, a)
        return kadr

    kadr = tlo_img.copy()
    d = ImageDraw.Draw(kadr, "RGBA")

    # ---------- 0,9-1,9 s: ZNAK FIRMOWY (logo + etykieta) ----------
    if s >= 0.9:
        a = plynnie(min(1.0, (s - 0.9) / 1.0))
        rozm = int(118 * (0.85 + 0.15 * a))
        lg = logo_img.resize((rozm, rozm), Image.LANCZOS).copy()
        lg.putalpha(lg.getchannel("A").point(lambda p: int(p * a)))
        kadr.paste(lg, (SZER - rozm - 42, 86), lg)

        et = "PREZENTERKA AI"
        f_et = czcionka(34)
        tw = d.textbbox((0, 0), et, font=f_et)
        d.rectangle([40, 92, 40 + (tw[2] - tw[0]) + 44, 92 + (tw[3] - tw[1]) + 30],
                    fill=(90, 105, 125, int(200 * a)))
        d.text((62, 104), et, font=f_et, fill=(255, 255, 255, int(255 * a)))

    # ---------- 1,9-3,4 s: TYTUL (zlota belka rozsuwa sie, tekst wchodzi) ----------
    if s >= 1.9:
        a = plynnie(min(1.0, (s - 1.9) / 1.5))
        by = int(WYS * 0.44)
        szer_belki = int(SZER * 0.86 * a)
        x0 = (SZER - szer_belki) // 2
        # cienka zlota linia rozsuwajaca sie od srodka
        d.rectangle([x0, by - 6, x0 + szer_belki, by], fill=ZLOTY + (240,))

        if a > 0.35:
            at = plynnie((a - 0.35) / 0.65)
            f_t = czcionka(70)
            tw = d.textbbox((0, 0), TYTUL, font=f_t)
            tx = (SZER - (tw[2] - tw[0])) // 2
            d.text((tx, by + 28), TYTUL, font=f_t, fill=(255, 255, 255, int(255 * at)))

            f_p = czcionka(30, gruba=False)
            pw = d.textbbox((0, 0), PODTYTUL, font=f_p)
            px = (SZER - (pw[2] - pw[0])) // 2
            d.text((px, by + 118), PODTYTUL, font=f_p,
                   fill=(176, 198, 222, int(235 * at)))
            # dolna linia domykajaca tytul
            d.rectangle([x0, by + 170, x0 + szer_belki, by + 174], fill=ZLOTY + (int(200 * at),))

    # ---------- 4,4-6,0 s: PRZEJSCIE DO IZABELI ----------
    if s >= 4.4:
        a = plynnie((s - 4.4) / 1.6)
        kadr = Image.blend(kadr.convert("RGB"), studio_img, a)

    return kadr.convert("RGB")


def zbuduj(wyjscie):
    tlo_img = Image.open(TLO_PUSTE).convert("RGB").resize((SZER, WYS), Image.LANCZOS)
    studio_img = Image.open(STUDIO_Z_IZA).convert("RGB").resize((SZER, WYS), Image.LANCZOS)
    logo_img = Image.open(LOGO).convert("RGBA")
    # logo w okragłej masce
    m = Image.new("L", (logo_img.width * 4, logo_img.height * 4), 0)
    ImageDraw.Draw(m).ellipse([0, 0, m.width, m.height], fill=255)
    logo_img.putalpha(m.resize(logo_img.size, Image.LANCZOS))

    with tempfile.TemporaryDirectory() as tmp:
        for nr in range(KLATEK):
            klatka(nr, tlo_img, studio_img, logo_img).save(f"{tmp}/k{nr:04d}.png")
        Path(wyjscie).parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-framerate", str(FPS), "-i", f"{tmp}/k%04d.png",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
            str(wyjscie),
        ], check=True)
    print(wyjscie)


if __name__ == "__main__":
    a = argparse.ArgumentParser(description="Czolowka Wiadomosci Dzialkowych (6 s, kodem)")
    a.add_argument("--output", default="/root/rod-ai-studio/data/wiadomosci/0000-premiera/CZOLOWKA.mp4")
    args = a.parse_args()
    zbuduj(args.output)
