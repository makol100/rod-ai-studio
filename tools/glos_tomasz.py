#!/usr/bin/env python3
"""GŁOS PREZENTERA TOMASZA — kanon od 17.09.2026 (D-0410, Tomasz: „Kandydat 3 poprawiony od teraz jako głos Tomasz").
Klon VoxCPM2 (llama.cpp-omni, GGUF, CPU, 0 zł). Przepis V2: ref_W1_1.wav + jej tekst, seed 7, timesteps 30, cfg 2.0.
Użycie: python3 tools/glos_tomasz.py --tekst "..." --out plik.wav   |   --plik kwestie.txt (linie: NAZWA<TAB>tekst) --katalog DIR
Wyjście: 24 kHz mono PCM. Bramka (whisper + ucho Gemini: akcent) jest OSOBNO — tools/bramka_glosu.py.
"""
import argparse, subprocess, time, os, sys, pathlib
BIN = "/root/modele/voxcpm2/llama.cpp-omni/build/bin/voxcpm2-cli"
M1 = "/root/modele/voxcpm2/models/VoxCPM2-BaseLM-Q8_0.gguf"
M2 = "/root/modele/voxcpm2/models/VoxCPM2-Acoustic-F16.gguf"
REF = "/root/rod-ai-studio/data/glos_tomasz/ref_W1_1.wav"
REF_TEKST = "Dzień dobry, tu Tomasz. Podpisaliście własną umowę z Tauronem? Dziś pokażę, jak mieć ją w telefonie — aplikacja Mój Tauron."
SEED, TS, CFG = 7, 30, 2.0

def syntezuj(tekst, out, seed=SEED, ts=TS, cfg=CFG):
    out = pathlib.Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_suffix(".48k.wav")
    t0 = time.time()
    r = subprocess.run([BIN, "--cpu", "--seed", str(seed), "--timesteps", str(ts), "--cfg", str(cfg),
                        "--prompt-wav", REF, "--prompt-text", REF_TEKST, "-r", REF, "-t", tekst, "-o", str(raw), M1, M2],
                       env={**os.environ, "OMP_NUM_THREADS": "12", "LD_LIBRARY_PATH": os.path.dirname(BIN) + ":" + os.environ.get("LD_LIBRARY_PATH", "")}, capture_output=True, text=True)
    if r.returncode != 0 or not raw.exists():
        raise RuntimeError(f"voxcpm2-cli padl ({r.returncode}): {r.stderr[-800:]}")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(out)], check=True)
    raw.unlink()
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip() or 0)
    return dur, time.time() - t0

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--tekst"); ap.add_argument("--out"); ap.add_argument("--plik"); ap.add_argument("--katalog")
    ap.add_argument("--seed", type=int, default=SEED); ap.add_argument("--timesteps", type=int, default=TS); ap.add_argument("--cfg", type=float, default=CFG)
    a = ap.parse_args()
    if a.tekst:
        d, t = syntezuj(a.tekst, a.out or "glos.wav", a.seed, a.timesteps, a.cfg); print(f"{a.out}: {d:.1f} s audio, {t:.0f} s liczenia")
    elif a.plik:
        for l in open(a.plik, encoding="utf-8"):
            if "\t" not in l: continue
            n, tekst = l.rstrip("\n").split("\t", 1)
            out = pathlib.Path(a.katalog or ".") / f"{n}.wav"
            if out.exists(): print(n, "istnieje — pomijam"); continue
            d, t = syntezuj(tekst, out, a.seed, a.timesteps, a.cfg); print(f"{n}: {d:.1f} s audio, {t:.0f} s liczenia", flush=True)
        print("GLOS_DONE")
