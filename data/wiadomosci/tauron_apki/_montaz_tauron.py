#!/usr/bin/env python3
"""Montaż wydań Tauron (D-0364/D-0366/D-0368): Prezenter Tomasz na białym tle + logo w rogu;
każdy krok = twarz ~3,5 s, potem jego głos nad planszą ze zrzutem. Intro C przez dolacz_intro. 0 USD.
Użycie: python3 _montaz_tauron.py W1|W2"""
import subprocess, sys
from pathlib import Path

B = Path("/root/rod-ai-studio/data/wiadomosci/tauron_apki")
OM, PL = B / "omni", B / "plansze"
LOGO = "/root/rod-ai-studio/assets/branding/rod_logo_kolo.png"
OUTRO_PNG = "/root/rod-ai-studio/data/wiadomosci/alejka2/plansze/plansza_10.png"  # PRZYGOTOWAL TOMASZ MAKSYS
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NORM = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,format=yuv420p"
AUD = "aresample=48000,aformat=channel_layouts=stereo"
TWARZ = 3.5  # s twarzy przed przejsciem na plansze

# (klip Omni, plansza po TWARZ s lub None = cala twarz)
SEKW = {
 "W1": [("W1_1", None), ("W1_2", "W1_01"), ("W1_3", "W1_02"), ("W1_4", "W1_03"), ("W1_5", "W1_04"), ("W1_6", "W1_05"), ("W1_7", "W1_06"), ("W1_8", "W1_07")],
 "W2": [("W2_1", None), ("W2_2", None), ("W2_3", "W2_01"), ("W2_4", "W2_02"), ("W2_5", "W2_03"), ("W2_6", "W2_04"), ("W2_7", "W2_05"), ("W2_8", "W2_06"), ("W2_9", "W2_08")],
}
KONCOWE = {"W1": ["W1_08"], "W2": ["W2_07", "W2_09"]}


def run(a): subprocess.run(["ffmpeg", "-y", "-v", "error", *a], check=True, capture_output=True)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True, check=True).stdout.strip())
def etyk(): return f"drawtext=fontfile={FONT}:text='PREZENTER AI':fontsize=34:fontcolor=white@0.95:box=1:boxcolor=0x1f5a37@0.8:boxborderw=14:x=(w-text_w)/2:y=h-150"
def logo_rog(): return "scale=150:150[lg];[v][lg]overlay=W-w-40:40"


def twarz(src, out, t=None):
    """klip Tomasza (biale tlo) + logo w rogu + etykieta; t=None -> caly klip"""
    a = ["-i", str(src), "-i", LOGO]
    if t: a += ["-t", f"{t:.4f}"]
    run([*a, "-filter_complex", f"[0:v]{NORM},{etyk()}[v];[1:v]{logo_rog()}[out]", "-map", "[out]", "-map", "0:a", "-af", AUD,
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-ar", "48000", "-b:a", "192k", str(out)])


def krok(klip, plansza, out):
    """twarz TWARZ s -> plansza z reszta glosu"""
    src = OM / f"omni_{klip}.mp4"; dl = dur(src); t1 = round(TWARZ * 30) / 30
    if plansza is None: twarz(src, out); return
    twarz(src, out.with_suffix(".a.mp4"), t1)
    n2 = int(round((dl - t1) * 30))
    run(["-loop", "1", "-i", str(PL / f"{plansza}.png"), "-vf", f"scale=1080:1920,zoompan=z='1+0.02*on/{n2}':d={n2}:s=1080x1920:fps=30,format=yuv420p", "-t", f"{n2/30:.4f}", "-an",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(out.with_suffix(".b.mp4"))])
    run(["-i", str(src), "-ss", f"{t1:.4f}", "-i", str(src), "-i", str(out.with_suffix(".a.mp4")), "-i", str(out.with_suffix(".b.mp4")),
         "-filter_complex", f"[2:v][3:v]concat=n=2:v=1:a=0[v];[0:a]{AUD}[a]", "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-shortest", str(out)])


def cicha(png, out, sek, etykieta_ai=False):
    vf = f"scale=1080:1920,format=yuv420p"
    if etykieta_ai:
        vf += f",drawtext=fontfile={FONT}:text='Prezenter Tomasz to awatar AI — za zgodą Tomasza':fontsize=30:fontcolor=0x59635b:x=(w-text_w)/2:y=h-230"
    run(["-loop", "1", "-i", str(png), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-vf", vf, "-t", f"{sek}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-ar", "48000", "-b:a", "192k", str(out)])


def main(w):
    P = B / f"parts_{w}"; P.mkdir(exist_ok=True); seq = []
    for i, (klip, plansza) in enumerate(SEKW[w], 1):
        if not (OM / f"omni_{klip}.mp4").exists(): print("BRAK KLIPU", klip, "— pomijam"); continue
        out = P / f"{i:02d}.mp4"; krok(klip, plansza, out); seq.append(out)
    for j, pl in enumerate(KONCOWE[w]):
        out = P / f"k{j}.mp4"; cicha(PL / f"{pl}.png", out, 3.0, etykieta_ai=(j == len(KONCOWE[w]) - 1)); seq.append(out)
    out = P / "outro.mp4"; cicha(OUTRO_PNG, out, 4.0); seq.append(out)
    ins, fc = [], ""
    for i, s in enumerate(seq):
        ins += ["-i", str(s)]; fc += f"[{i}:v]{NORM}[v{i}];[{i}:a]{AUD}[a{i}];"
    fc += "".join(f"[v{i}][a{i}]" for i in range(len(seq))) + f"concat=n={len(seq)}:v=1:a=1[v][a]"
    bez = B / f"{w}_bez_intro.mp4"
    run([*ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-ar", "48000", "-b:a", "192k", "-movflags", "+faststart", str(bez)])
    nazwa = {"W1": "MOJ_TAURON", "W2": "ELICZNIK"}[w]
    r = subprocess.run(["python3", "/root/rod-ai-studio/tools/dolacz_intro.py", str(bez), "--wyjscie", str(B / f"WIADOMOSCI_{nazwa}_v1.mp4")], capture_output=True, text=True)
    print(w, "bez intro:", round(dur(bez), 1), "s |", r.stdout.strip() or r.stderr.strip())


if __name__ == "__main__":
    main(sys.argv[1])
