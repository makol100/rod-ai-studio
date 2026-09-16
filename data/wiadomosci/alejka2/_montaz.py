#!/usr/bin/env python3
"""Montaż wydania „Alejka Północna — ciąg dalszy" (D-0355, wariant DUET).
Części -> normalizacja 1080x1920/30fps/yuv420p/48k stereo -> concat filter_complex
-> intro C (tools/dolacz_intro.py, bramka klatek). 0 USD."""
import subprocess, sys
from pathlib import Path

B = Path("/root/rod-ai-studio/data/wiadomosci/alejka2")
P, OM, IZ, PL = B / "parts", B / "omni", B / "izabela", B / "plansze"
P.mkdir(exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NORM = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,format=yuv420p"
AUD = "aresample=48000,aformat=channel_layouts=stereo"


def run(args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True, capture_output=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout.strip())


def etykieta(txt):
    return (f"drawtext=fontfile={FONT}:text='{txt}':fontsize=34:fontcolor=white@0.92:box=1:boxcolor=0x1f5a37@0.75:"
            f"boxborderw=14:x=(w-text_w)/2:y=h-150")


def mowca(src, out, tag):
    """klip prezentera (Omni/Kling) z etykietą AI"""
    run(["-i", str(src), "-vf", f"{NORM},{etykieta(tag)}", "-af", AUD, "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-r", "30", "-c:a", "aac", "-ar", "48000", "-b:a", "192k", str(out)])


def plansza(png, out, sek, audio=None):
    """plansza: cisza (anullsrc) albo głos Izabeli; lekki zoom 1.0->1.03"""
    n = int(sek * 30)
    zoom = f"scale=1080:1920,zoompan=z='1+0.03*on/{n}':d={n}:s=1080x1920:fps=30,format=yuv420p"
    if audio:
        run(["-loop", "1", "-i", str(png), "-i", str(audio), "-vf", zoom, "-af", f"{AUD},apad", "-t", f"{sek:.3f}",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-ar", "48000", "-b:a", "192k", str(out)])
    else:
        run(["-loop", "1", "-i", str(png), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-vf", zoom, "-t", f"{sek:.3f}",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-ar", "48000", "-b:a", "192k", str(out)])


def outro(out, sek=4.5):
    txt = "Prezenter Tomasz i Izabela to awatary AI — za zgodą Tomasza"
    run(["-loop", "1", "-i", str(PL / "plansza_09.png"), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
         "-vf", f"scale=1080:1920,format=yuv420p,drawtext=fontfile={FONT}:text='{txt}':fontsize=30:fontcolor=0x59635b:"
                f"x=(w-text_w)/2:y=h-230", "-t", f"{sek}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
         "-c:a", "aac", "-ar", "48000", "-b:a", "192k", str(out)])


def k4_bez_do_mnie(out):
    """D-0356: audio K4 bez 'do mnie' (ciecie 2,83-4,10 s na pauzie wg word-timestamps); wideo: twarz do ciecia, dalej plansza 4 z glosem."""
    T1, T2, KON = 85 / 30, 4.10, 10.0
    K4 = OM / "omni_K4.mp4"
    run(["-i", str(K4), "-filter_complex", f"[0:a]atrim=0:{T1},asetpts=PTS-STARTPTS[a1];[0:a]atrim={T2}:{KON},asetpts=PTS-STARTPTS[a2];[a1][a2]concat=n=2:v=0:a=1,{AUD}[a]",
         "-map", "[a]", "-c:a", "aac", "-ar", "48000", "-b:a", "192k", str(P / "07a.m4a")])
    n2 = int(round((dur(P / "07a.m4a") - T1) * 30))
    run(["-i", str(K4), "-t", f"{T1:.4f}", "-vf", f"{NORM},{etykieta('PREZENTER AI')}", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(P / "07v1.mp4")])
    run(["-loop", "1", "-i", str(PL / "plansza_04.png"), "-vf", f"scale=1080:1920,zoompan=z='1+0.03*on/{n2}':d={n2}:s=1080x1920:fps=30,format=yuv420p",
         "-t", f"{n2 / 30:.4f}", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(P / "07v2.mp4")])
    run(["-i", str(P / "07v1.mp4"), "-i", str(P / "07v2.mp4"), "-i", str(P / "07a.m4a"), "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
         "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-shortest", str(out)])


def main():
    d = lambda n: dur(IZ / f"izabela_{n}.mp3") + 0.6
    seq = []
    mowca(OM / "omni_K1.mp4", P / "01.mp4", "PREZENTER AI"); seq.append("01")
    plansza(PL / "plansza_01.png", P / "02.mp4", 3.0); seq.append("02")
    mowca(OM / "omni_K2.mp4", P / "03.mp4", "PREZENTER AI"); seq.append("03")
    plansza(PL / "plansza_02.png", P / "04.mp4", 3.0); seq.append("04")
    mowca(IZ / "izabela_I1.mp4", P / "05.mp4", "PREZENTERKA AI"); seq.append("05")
    plansza(PL / "plansza_03.png", P / "06.mp4", d("I3"), IZ / "izabela_I3.mp3"); seq.append("06")
    k4_bez_do_mnie(P / "07.mp4"); seq.append("07")   # D-0356: bez "do mnie", plansza 4 maskuje ciecie
    plansza(PL / "plansza_05.png", P / "09.mp4", d("I5"), IZ / "izabela_I5.mp3"); seq.append("09")
    plansza(PL / "plansza_06.png", P / "10.mp4", d("I6"), IZ / "izabela_I6.mp3"); seq.append("10")
    mowca(IZ / "izabela_I7.mp4", P / "11.mp4", "PREZENTERKA AI"); seq.append("11")
    plansza(PL / "plansza_07.png", P / "12.mp4", 2.5); seq.append("12")
    plansza(PL / "plansza_08.png", P / "13.mp4", 2.5); seq.append("13")
    outro(P / "14.mp4"); seq.append("14")
    plansza(PL / "plansza_10.png", P / "15.mp4", 4.0); seq.append("15")   # D-0357: karta "przygotowal Tomasz Maksys"
    ins, fc = [], ""
    for i, s in enumerate(seq):
        ins += ["-i", str(P / f"{s}.mp4")]
        fc += f"[{i}:v]{NORM}[v{i}];[{i}:a]{AUD}[a{i}];"
    fc += "".join(f"[v{i}][a{i}]" for i in range(len(seq))) + f"concat=n={len(seq)}:v=1:a=1[v][a]"
    bez = B / "alejka2_bez_intro_v3.mp4"
    run([*ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
         "-c:a", "aac", "-ar", "48000", "-b:a", "192k", "-movflags", "+faststart", str(bez)])
    print("bez intro:", round(dur(bez), 2), "s")
    r = subprocess.run(["python3", "/root/rod-ai-studio/tools/dolacz_intro.py", str(bez), "--wyjscie", str(B / "ALEJKA2_v3.mp4")],
                       capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
