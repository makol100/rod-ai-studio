# -*- coding: utf-8 -*-
"""
ROLKA ZAPOWIADAJĄCA — 1080x1920, ~40 s.
PUBLICZNIE (strona ROD + Shorts) -> tylko materiał BEZ TWARZY.
Zadanie rolki: nie tłumaczyć, tylko zatrzymać kciuk i odesłać do filmu.
"""
import asyncio, subprocess, os
import edge_tts
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
GLOS = "pl-PL-MarekNeural"
TLO, TEKST, TEKST_2 = "#F7F3EA", "#2C2C2C", "#6B675E"
ZIELEN, ZIELEN_C = "#2E9E7A", "#1F7A5C"

D = "/root/rod-ai-studio/data/rolka-prad"
BT = f"{D}/bez_twarzy"
TMP = f"{D}/_rolka_tmp"
MUZYKA = "/root/rod-ai-studio/assets/music/precious-memories(chosic.com)-1.mp3"
os.makedirs(TMP, exist_ok=True)


def font(n, r):
    for s in (f"/usr/share/fonts/truetype/google-fonts/Poppins-{n}.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(s, r)
        except OSError:
            continue
    return ImageFont.load_default()


def lektor(t, p):
    asyncio.run(edge_tts.Communicate(t, GLOS).save(p))
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
    return float(d)


def napis(txt, duzy, plik):
    """Przezroczysta nakładka z napisem na dole — tak się robi rolki."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    linie = txt.split("\n")
    f = font("Bold", 68 if duzy else 52)
    wys = len(linie) * (86 if duzy else 68)
    y0 = H - 430 - wys

    # ciemna poducha pod tekstem — żeby był czytelny na każdym tle
    d.rectangle([0, y0 - 40, W, y0 + wys + 40], fill=(20, 20, 20, 165))
    y = y0
    for w in linie:
        l, t, r, b = d.textbbox((0, 0), w, font=f)
        d.text(((W - (r - l)) / 2 - l, y), w, font=f, fill="#FFFFFF")
        y += 86 if duzy else 68
    img.save(plik)


def scena(zrodlo, czas, txt_ekran, od, out, duzy=False):
    n = f"{TMP}/n.png"
    napis(txt_ekran, duzy, n)
    wideo = zrodlo.endswith(".mp4")
    src = ["-stream_loop", "-1", "-ss", str(od), "-i", zrodlo] if wideo else ["-loop", "1", "-i", zrodlo]
    subprocess.run(["ffmpeg", "-v", "error", *src, "-i", n,
                    "-filter_complex",
                    f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                    f"setpts=PTS-STARTPTS[v];[v][1:v]overlay=0:0,fps={FPS},format=yuv420p",
                    "-t", str(czas), "-an", "-c:v", "libx264", "-preset", "veryfast",
                    out, "-y"], check=True)
    return czas


def plansza(out, czas=6.0):
    img = Image.new("RGB", (W, H), TLO)
    d = ImageDraw.Draw(img)

    def srodek(y, txt, f, k):
        l, t, r, b = d.textbbox((0, 0), txt, font=f)
        d.text(((W - (r - l)) / 2 - l, y), txt, font=f, fill=k)

    d.line([(W / 2 - 60, 660), (W / 2 + 60, 660)], fill=ZIELEN, width=7)
    srodek(750, "Teraz", font("Bold", 104), TEKST)
    srodek(872, "Twoja kolej", font("Bold", 104), TEKST)

    # film jest NIEPUBLICZNY — na kanale go nie ma. Kierujemy do linku.
    d.rounded_rectangle([120, 1090, W - 120, 1290], radius=20,
                        fill="#FFFFFF", outline=ZIELEN, width=5)
    srodek(1130, "CAŁY FILM", font("Bold", 46), ZIELEN_C)
    srodek(1200, "link w opisie", font("Regular", 44), TEKST_2)

    srodek(1420, "ROD im. Józefa Lompy", font("Regular", 38), TEKST_2)

    p = f"{TMP}/pl.png"
    img.save(p)
    subprocess.run(["ffmpeg", "-v", "error", "-loop", "1", "-i", p, "-t", str(czas),
                    "-vf", f"fps={FPS},format=yuv420p,fade=t=in:st=0:d=0.5",
                    "-c:v", "libx264", "-preset", "veryfast", out, "-y"], check=True)
    return czas


# ============ SCENY ROLKI (Z TWARZAMI — decyzja Tomasza 13.07) ============
F = f"{D}/filmy"
B = f"{D}/budowa"

SCENY = [
    (f"{F}/VID-20260712-WA0008.mp4",
     "Pod naszymi alejkami jest skała. Nie ziemia — skała.",
     "Pod alejką\njest SKAŁA", 15, True),

    (f"{B}/1000098548.jpg",
     "A w rowie leży osiemnaście kabli. Jeden idzie prosto do Twojej działki.",
     "18 kabli\nJeden — Twój", 0, True),

    (f"{B}/1000098520.jpg",
     "Robili to nasi ludzie. Po pracy, po nocach. Za darmo.",
     "Nasi ludzie\nZa darmo", 0, True),

    (f"{D}/KABEL-NA-PLOCIE.jpg",
     "Ten kabel wisi na Twojej siatce. Ogród doprowadził go pod płot.",
     "Kabel wisi\nna Twojej siatce", 0, False),

    (f"{D}/02-ZK-front.jpg",
     "Licznik czeka w szafie — z numerem Twojej działki.",
     "Licznik czeka\nz Twoim numerem", 0, False),
]

if __name__ == "__main__":
    for f in os.listdir(TMP):
        if f.startswith(("v", "s")) and f.endswith((".mp4", ".mp3")):
            os.remove(os.path.join(TMP, f))

    czesci, audio = [], []
    for i, (zr, tekst, ekran, od, duzy) in enumerate(SCENY):
        v = f"{TMP}/v{i}.mp4"
        a = f"{TMP}/s{i}.mp3"
        czas = lektor(tekst, a)
        subprocess.run(["ffmpeg", "-v", "error", "-i", a, "-af", "apad=pad_dur=0.6",
                        "-t", str(czas + 0.6), f"{TMP}/s{i}p.mp3", "-y"], check=True)
        scena(zr, czas + 0.6, ekran, od, v, duzy)
        czesci.append(v)
        audio.append(f"{TMP}/s{i}p.mp3")
        print(f"  [{i}] {czas+0.6:4.1f}s  {os.path.basename(zr)}", flush=True)

    # plansza końcowa
    pv = f"{TMP}/vpl.mp4"
    pc = plansza(pv, 7.5)
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", str(pc), f"{TMP}/spl.mp3", "-y"], check=True)
    czesci.append(pv)
    audio.append(f"{TMP}/spl.mp3")
    print(f"  [plansza] {pc:4.1f}s", flush=True)

    with open(f"{TMP}/lv.txt", "w") as f:
        for c in czesci:
            f.write(f"file '{c}'\n")
    with open(f"{TMP}/la.txt", "w") as f:
        for a in audio:
            f.write(f"file '{a}'\n")

    subprocess.run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{TMP}/lv.txt",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(FPS),
                    f"{TMP}/v.mp4", "-y"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{TMP}/la.txt",
                    "-c:a", "libmp3lame", f"{TMP}/a.mp3", "-y"], check=True)

    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", f"{TMP}/v.mp4"],
                               capture_output=True, text=True).stdout.strip())
    subprocess.run(["ffmpeg", "-v", "error", "-i", f"{TMP}/v.mp4", "-i", f"{TMP}/a.mp3",
                    "-stream_loop", "-1", "-i", MUZYKA,
                    "-filter_complex",
                    f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,asplit=2[lek][key];"
                    f"[2:a]volume=0.4,afade=t=out:st={dur-3:.1f}:d=3[m];"
                    f"[m][key]sidechaincompress=threshold=0.03:ratio=12:attack=20:release=350[md];"
                    f"[lek][md]amix=inputs=2:duration=longest:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", f"{D}/ROLKA-ZAPOWIEDZ.mp4", "-y"], check=True)
    print(f"\ngotowe: {D}/ROLKA-ZAPOWIEDZ.mp4  ({dur:.0f} s)")
