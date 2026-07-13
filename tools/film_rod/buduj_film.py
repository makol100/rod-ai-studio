# -*- coding: utf-8 -*-
"""
BUDUJ FILM — ROD im. Józefa Lompy, przebudowa sieci.  1920x1080, YouTube.

Typy scen:
  ("mapa",  plik, tekst)                          -> mapa na pełnym ekranie
  ("foto",  plik, tekst, tytuł, [linie], liczba, podpis_liczby)
  ("klip",  plik, tekst, tytuł, [linie], od_sek)  -> wideo w oknie, BEZ DŹWIĘKU
  (typ,     plik, None,  tytuł, [linie], czas)    -> scena bez lektora (czas w sek.)

Lektor: edge-tts pl-PL-MarekNeural. Długość sceny = długość lektora + 0.7 s.
Klipy: dźwięk oryginalny WYRZUCONY (decyzja Tomasza — "tam to bzdury").
"""
import asyncio, subprocess, os
import edge_tts
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
GLOS = "pl-PL-MarekNeural"
ZNAKOW_NA_SEK = 11.6

TLO, TEKST, TEKST_2 = "#F7F3EA", "#2C2C2C", "#6B675E"
ZIELEN, ZIELEN_C, LINIA = "#2E9E7A", "#1F7A5C", "#C9C3B4"

TMP = "/root/rod-ai-studio/data/rolka-prad/_film_tmp"
os.makedirs(TMP, exist_ok=True)


def font(n, r):
    for s in (f"/usr/share/fonts/truetype/google-fonts/Poppins-{n}.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(s, r)
        except OSError:
            continue
    return ImageFont.load_default()


async def _tts(tekst, plik):
    await edge_tts.Communicate(tekst, GLOS).save(plik)


def lektor(tekst, plik):
    asyncio.run(_tts(tekst, plik))
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", plik], capture_output=True, text=True)
    return float(out.stdout.strip())


def cisza(czas, plik):
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", str(czas), plik, "-y"], check=True)


def panel_tlo(tytul, linie, liczba=None, podpis=None, okno_w=0):
    img = Image.new("RGB", (W, H), TLO)
    d = ImageDraw.Draw(img)
    ox, oy = 90, (H - 900) // 2

    if okno_w:
        cien = Image.new("RGB", (okno_w + 24, 924), TLO)
        ImageDraw.Draw(cien).rounded_rectangle([12, 12, okno_w + 12, 912], radius=14, fill="#DDD7C9")
        img.paste(cien.filter(ImageFilter.GaussianBlur(7)), (ox - 12, oy - 6))

    px = ox + okno_w + 80 if okno_w else 140
    szer = W - px - 90
    y = oy + 40
    d.line([(px, y), (px + 70, y)], fill=ZIELEN, width=6)
    y += 40
    for w in (tytul or "").split("\n"):
        d.text((px, y), w, font=font("Bold", 62), fill=TEKST)
        y += 76
    y += 26
    for w in (linie or []):
        d.text((px, y), w, font=font("Regular", 34), fill=TEKST_2)
        y += 52
    if liczba:
        y += 40
        d.line([(px, y), (px + szer, y)], fill=LINIA, width=2)
        y += 34
        d.text((px, y), liczba, font=font("Bold", 96), fill=ZIELEN_C)
        l, t, r, b = d.textbbox((0, 0), liczba, font=font("Bold", 96))
        d.text((px + (r - l) + 24, y + 44), podpis or "", font=font("Regular", 32), fill=TEKST_2)
    return img


def scena_mapa(plik, czas, out):
    subprocess.run(["ffmpeg", "-v", "error", "-loop", "1", "-i", plik, "-t", str(czas),
                    "-vf", f"scale={W}:{H},fps={FPS},format=yuv420p",
                    "-c:v", "libx264", "-preset", "veryfast", out, "-y"], check=True)


def scena_foto(plik, czas, tytul, linie, liczba, podpis, out):
    src = Image.open(plik)
    ow = int(src.width * 900 / src.height)
    p = f"{TMP}/_t.png"
    panel_tlo(tytul, linie, liczba, podpis, okno_w=ow).save(p)
    oy = (H - 900) // 2
    subprocess.run(["ffmpeg", "-v", "error", "-loop", "1", "-i", p, "-loop", "1", "-i", plik,
                    "-filter_complex",
                    f"[1:v]scale={ow}:900[m];[0:v][m]overlay=90:{oy},fps={FPS},format=yuv420p",
                    "-t", str(czas), "-c:v", "libx264", "-preset", "veryfast", out, "-y"], check=True)


def scena_klip(plik, czas, tytul, linie, od, out):
    out_p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", plik],
                           capture_output=True, text=True).stdout.strip()
    sw, sh = map(int, out_p.split("x"))
    ow = int(sw * 900 / sh)
    p = f"{TMP}/_tk.png"
    panel_tlo(tytul, linie, okno_w=ow).save(p)
    oy = (H - 900) // 2
    subprocess.run(["ffmpeg", "-v", "error", "-loop", "1", "-i", p,
                    "-stream_loop", "-1", "-ss", str(od), "-i", plik,
                    "-filter_complex",
                    f"[1:v]scale={ow}:900,setpts=PTS-STARTPTS[m];"
                    f"[0:v][m]overlay=90:{oy},fps={FPS},format=yuv420p",
                    "-t", str(czas), "-an", "-c:v", "libx264", "-preset", "veryfast",
                    out, "-y"], check=True)


def buduj(sceny, wynik, muzyka=None):
    czesci, audio = [], []
    for i, s in enumerate(sceny):
        typ, plik, tekst = s[0], s[1], s[2]
        tytul = s[3] if len(s) > 3 else None
        linie = s[4] if len(s) > 4 else None
        extra = s[5] if len(s) > 5 else None

        a = f"{TMP}/a{i:02d}.mp3"
        if tekst:
            czas = lektor(tekst, a) + 0.7
        else:
            czas = float(extra or 5.0)
            cisza(czas, a)
        audio.append(a)

        v = f"{TMP}/v{i:02d}.mp4"
        if typ == "mapa":
            scena_mapa(plik, czas, v)
        elif typ == "foto":
            scena_foto(plik, czas, tytul, linie,
                       extra if isinstance(extra, str) else None,
                       s[6] if len(s) > 6 else None, v)
        elif typ == "klip":
            scena_klip(plik, czas, tytul, linie,
                       extra if isinstance(extra, (int, float)) and tekst else 0, v)
        czesci.append(v)
        print(f"  [{i:02d}] {typ:<5} {czas:5.1f}s  {os.path.basename(plik or '-')}", flush=True)

    with open(f"{TMP}/lv.txt", "w") as f:
        for c in czesci:
            f.write(f"file '{c}'\n")
    with open(f"{TMP}/la.txt", "w") as f:
        for a in audio:
            f.write(f"file '{a}'\n")

    subprocess.run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{TMP}/lv.txt",
                    "-c", "copy", f"{TMP}/v.mp4", "-y"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{TMP}/la.txt",
                    "-c", "copy", f"{TMP}/a.mp3", "-y"], check=True)

    if muzyka and os.path.exists(muzyka):
        subprocess.run(["ffmpeg", "-v", "error", "-i", f"{TMP}/v.mp4", "-i", f"{TMP}/a.mp3",
                        "-stream_loop", "-1", "-i", muzyka,
                        "-filter_complex",
                        "[1:a]volume=1.0[lek];[2:a]volume=0.12[muz];"
                        "[lek][muz]amix=inputs=2:duration=first:dropout_transition=0[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", wynik, "-y"], check=True)
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-i", f"{TMP}/v.mp4", "-i", f"{TMP}/a.mp3",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                        wynik, "-y"], check=True)
    print("\ngotowe:", wynik, flush=True)
