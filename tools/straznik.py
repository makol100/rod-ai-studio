#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STRAŻNIK — automatyczna kontrola jakości klipów Fabryki Rolek.
6 strażników: techniczny, napisów-widmo (OCR), scenariusza (Whisper),
kotwic FLF, tożsamości (InsightFace), ust (SyncNet), + sędzia VLM.
Uruchamiaj w kontenerze: /app/venv/bin/python /root/rod-ai-studio/tools/straznik.py KLIP.mp4
Opcje: --kwestia "TEKST" --kadr-start X.jpg --kadr-koniec Y.jpg
       --wzorzec NAZWA=karta.jpg --exp-w 1080 --exp-h 1920 --json
Werdykt: PASS / WARN / FAIL per strażnik + zbiorczy. Kod wyjścia 0=PASS, 1=FAIL.
"""
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path

def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def _klatki(plik, n, katalog):
    """Wyciąga n klatek równomiernie; zwraca listę ścieżek."""
    d = _ffprobe(plik).get("czas", 8.0)
    out = []
    for i in range(n):
        t = max(0.05, d * (i + 0.5) / n)
        p = Path(katalog) / f"kl_{i:02d}.jpg"
        _run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(plik),
              "-frames:v", "1", "-q:v", "3", str(p)])
        if p.exists():
            out.append(p)
    return out

def _ffprobe(plik):
    r = _run(["ffprobe", "-v", "error", "-select_streams", "v:0",
              "-show_entries", "stream=width,height,r_frame_rate:format=duration",
              "-of", "json", str(plik)])
    try:
        j = json.loads(r.stdout)
        s = j["streams"][0]
        num, den = s["r_frame_rate"].split("/")
        return {"w": s["width"], "h": s["height"],
                "fps": round(float(num) / float(den), 2),
                "czas": round(float(j["format"]["duration"]), 2)}
    except Exception as e:
        return {"blad": str(e)}

# ---------- 5. STRAŻNIK TECHNICZNY ----------
def straznik_techniczny(plik, exp_w, exp_h):
    info = _ffprobe(plik)
    if "blad" in info:
        return {"status": "FAIL", "detale": info}
    problemy = []
    if exp_w and info["w"] != exp_w: problemy.append(f"szerokość {info['w']}≠{exp_w}")
    if exp_h and info["h"] != exp_h: problemy.append(f"wysokość {info['h']}≠{exp_h}")
    # czarne klatki / zamrożenia
    r = _run(["ffmpeg", "-v", "info", "-i", str(plik), "-vf",
              "blackdetect=d=0.3:pix_th=0.10,freezedetect=n=-60dB:d=1.5",
              "-an", "-f", "null", "-"])
    if "black_start" in r.stderr: problemy.append("czarne klatki (blackdetect)")
    if "freeze_start" in r.stderr: problemy.append("zamrożony obraz (freezedetect)")
    # niechciane cięcia wewnątrz klipu (klip z jednej generacji = 0 cięć)
    r = _run(["ffmpeg", "-v", "info", "-i", str(plik), "-vf",
              "select='gt(scene,0.4)',metadata=print", "-an", "-f", "null", "-"])
    ciecia = len(re.findall(r"lavfi\.scene_score", r.stderr))
    if ciecia > 0: problemy.append(f"wykryto {ciecia} cięć sceny wewnątrz klipu")
    st = "PASS" if not problemy else "FAIL"
    return {"status": st, "detale": {**info, "problemy": problemy}}

# ---------- 3. STRAŻNIK NAPISÓW-WIDMO (OCR) ----------
def straznik_napisow(plik, n=8, tekst_dozwolony=False):
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        return {"status": "POMINIĘTY", "detale": "ETAP 1: brak pytesseract/tesseract"}
    znaleziska = []
    with tempfile.TemporaryDirectory() as td:
        for p in _klatki(plik, n, td):
            try:
                txt = pytesseract.image_to_string(Image.open(p), lang="pol+eng")
            except Exception as e:
                return {"status": "POMINIĘTY", "detale": f"tesseract: {e}"}
            slowa = [w for w in re.findall(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{3,}", txt)]
            if len(slowa) >= 2:
                znaleziska.append({"klatka": p.name, "tekst": " ".join(slowa)[:80]})
    if tekst_dozwolony:
        st = "PASS" if znaleziska else "FAIL"  # kontrola pozytywna (np. plansza)
    else:
        st = "PASS" if not znaleziska else "FAIL"
    return {"status": st, "detale": znaleziska or "brak tekstu na klatkach"}

# ---------- 4. STRAŻNIK SCENARIUSZA (Whisper) ----------
def straznik_scenariusza(plik, kwestia):
    if not kwestia:
        return {"status": "POMINIĘTY", "detale": "nie podano --kwestia"}
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return {"status": "POMINIĘTY", "detale": "brak faster_whisper"}
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(str(plik), language="pl")
    uslyszane = " ".join(s.text.strip() for s in segs).strip()
    norm = lambda t: re.sub(r"[^a-ząćęłńóśźż ]", "", t.lower())
    import difflib
    ratio = difflib.SequenceMatcher(None, norm(kwestia), norm(uslyszane)).ratio()
    st = "PASS" if ratio >= 0.75 else ("WARN" if ratio >= 0.55 else "FAIL")
    return {"status": st, "detale": {"oczekiwane": kwestia,
                                     "usłyszane": uslyszane, "zgodność": round(ratio, 2)}}

# ---------- 7. KOTWICE FLF ----------
def _mad(im_a, im_b):
    import numpy as np
    from PIL import Image
    a = Image.open(im_a).convert("L")
    a = a.resize((64, max(1, int(64 * a.height / a.width))))
    b = Image.open(im_b).convert("L").resize(a.size)
    import numpy
    return float(abs(numpy.asarray(a, float) - numpy.asarray(b, float)).mean())

def kotwice_flf(plik, kadr_start, kadr_koniec):
    if not (kadr_start or kadr_koniec):
        return {"status": "POMINIĘTY", "detale": "nie podano kadrów"}
    det, st = {}, "PASS"
    with tempfile.TemporaryDirectory() as td:
        if kadr_start:
            f0 = Path(td) / "f0.jpg"
            _run(["ffmpeg", "-y", "-v", "error", "-i", str(plik),
                  "-vf", "select='eq(n,0)'", "-frames:v", "1", "-q:v", "2", str(f0)])
            m = _mad(f0, kadr_start); det["MAD_start"] = round(m, 2)
            if m >= 12: st = "FAIL"
        if kadr_koniec:
            f1 = Path(td) / "f1.jpg"
            _run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.15", "-i", str(plik),
                  "-frames:v", "1", "-q:v", "2", "-update", "1", str(f1)])
            m = _mad(f1, kadr_koniec); det["MAD_koniec"] = round(m, 2)
            if m >= 18 and st == "PASS": st = "WARN"
    return {"status": st, "detale": det}

# ---------- 1. STRAŻNIK TOŻSAMOŚCI (InsightFace) ----------
_APP = None
def _twarze(sciezka):
    global _APP
    import cv2
    from insightface.app import FaceAnalysis
    if _APP is None:
        _APP = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        _APP.prepare(ctx_id=-1, det_size=(640, 640))
    img = cv2.imread(str(sciezka))
    return [t for t in _APP.get(img) if t.det_score >= 0.6] if img is not None else []

def straznik_tozsamosci(plik, wzorce, n=10, prog=0.35):
    """wzorce: dict NAZWA->ścieżka karty. Każda twarz z klipu musi pasować
    do któregoś wzorca (cosine ≥ prog); wzorzec obecny gdy ma ≥1 dopasowanie."""
    if not wzorce:
        return {"status": "POMINIĘTY", "detale": "nie podano --wzorzec"}
    try:
        import numpy as np
        emb_w = {}
        for nazwa, sc in wzorce.items():
            tw = _twarze(sc)
            if not tw:
                return {"status": "FAIL", "detale": f"brak twarzy na karcie {nazwa}"}
            emb_w[nazwa] = tw[0].normed_embedding
    except ImportError:
        return {"status": "POMINIĘTY", "detale": "ETAP 2: brak insightface"}
    obcy, male, trafienia = [], [], {k: [] for k in emb_w}
    with tempfile.TemporaryDirectory() as td:
        for p in _klatki(plik, n, td):
            for tw in _twarze(p):
                sims = {k: float(np.dot(tw.normed_embedding, e)) for k, e in emb_w.items()}
                naj = max(sims, key=sims.get)
                if sims[naj] >= prog:
                    trafienia[naj].append(round(sims[naj], 2))
                elif int(tw.bbox[3] - tw.bbox[1]) < 150:
                    male.append({"klatka": p.name, "h_px": int(tw.bbox[3] - tw.bbox[1]),
                                 "sim": round(sims[naj], 2)})
                else:
                    obcy.append({"klatka": p.name, "najbliżej": naj,
                                 "sim": round(sims[naj], 2)})
    det = {k: {"trafienia": len(v),
               "śr_sim": round(sum(v) / len(v), 2) if v else 0.0}
           for k, v in trafienia.items()}
    det["obce_twarze"] = obcy
    det["małe_twarze_WARN"] = male
    st = "FAIL" if obcy else ("WARN" if male else "PASS")
    return {"status": st, "detale": det}

# ---------- 2. STRAŻNIK UST (SyncNet) ----------
def straznik_ust(plik):
    syncdir = Path("/root/rod-ai-studio/tools/syncnet_python")
    if not (syncdir / "run_syncnet.py").exists():
        return {"status": "POMINIĘTY", "detale": "ETAP 3: brak syncnet_python"}
    try:
        import torch  # noqa
    except ImportError:
        return {"status": "POMINIĘTY", "detale": "ETAP 3: brak torch"}
    with tempfile.TemporaryDirectory() as td:
        r1 = _run([sys.executable, str(syncdir / "run_pipeline.py"),
                   "--videofile", str(plik), "--reference", "qc", "--data_dir", td])
        r2 = _run([sys.executable, str(syncdir / "run_syncnet.py"),
                   "--videofile", str(plik), "--reference", "qc", "--data_dir", td])
        wyj = r2.stdout + r2.stderr + r1.stderr
    m_c = re.search(r"Confidence:\s*([\d.]+)", wyj)
    m_o = re.search(r"AV offset:\s*(-?\d+)", wyj)
    if not m_c:
        return {"status": "WARN", "detale": "syncnet nie zwrócił wyniku (brak twarzy?)"}
    conf, off = float(m_c.group(1)), int(m_o.group(1)) if m_o else None
    st = "FAIL" if (conf < 3.0 or abs(off or 0) > 3) else ("WARN" if conf < 5.0 else "PASS")
    return {"status": st, "detale": {"confidence": conf, "av_offset": off,
                                     "próg": "FAIL<3.0, WARN 3-5, PASS≥5; |offset|≤3"}}

# ---------- 6. SĘDZIA VLM (Ollama) ----------
def sedzia_vlm(plik, pytania):
    if not pytania:
        return {"status": "POMINIĘTY", "detale": "nie podano --vlm-pytania"}
    r = _run(["curl", "-s", "http://172.17.0.1:11434/api/tags"])
    if "qwen2.5vl" not in r.stdout and "qwen2.5-vl" not in r.stdout:
        return {"status": "POMINIĘTY", "detale": "ETAP 4: brak modelu VLM w Ollama"}
    import base64
    with tempfile.TemporaryDirectory() as td:
        kl = _klatki(plik, 3, td)
        odp = []
        for p in kl:
            b64 = base64.b64encode(p.read_bytes()).decode()
            payload = json.dumps({"model": "qwen2.5vl:7b", "stream": False,
                                  "prompt": pytania, "images": [b64]})
            rr = _run(["curl", "-s", "http://172.17.0.1:11434/api/generate",
                       "-d", payload])
            try:
                odp.append(json.loads(rr.stdout).get("response", "")[:200])
            except Exception:
                odp.append("(błąd VLM)")
    return {"status": "INFO", "detale": odp}

# ---------- GŁÓWNY ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plik")
    ap.add_argument("--kwestia", default=None)
    ap.add_argument("--kadr-start", default=None)
    ap.add_argument("--kadr-koniec", default=None)
    ap.add_argument("--wzorzec", action="append", default=[],
                    help="NAZWA=/sciezka/karta.jpg (wielokrotnie)")
    ap.add_argument("--vlm-pytania", default=None)
    ap.add_argument("--exp-w", type=int, default=1080)
    ap.add_argument("--exp-h", type=int, default=1920)
    ap.add_argument("--tekst-dozwolony", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    wz = {}
    for w in a.wzorzec:
        nazwa, sc = w.split("=", 1)
        wz[nazwa] = sc
    plik = Path(a.plik)
    R = {
        "techniczny":  straznik_techniczny(plik, a.exp_w, a.exp_h),
        "napisy_OCR":  straznik_napisow(plik, tekst_dozwolony=a.tekst_dozwolony),
        "scenariusz":  straznik_scenariusza(plik, a.kwestia),
        "kotwice_FLF": kotwice_flf(plik, a.kadr_start, a.kadr_koniec),
        "tożsamość":   straznik_tozsamosci(plik, wz),
        "usta_sync":   straznik_ust(plik),
        "sędzia_VLM":  sedzia_vlm(plik, a.vlm_pytania),
    }
    fail = [k for k, v in R.items() if v["status"] == "FAIL"]
    werdykt = "FAIL" if fail else "PASS"
    wynik = {"plik": str(plik), "werdykt": werdykt, "oblane": fail, "strażnicy": R}
    if a.json:
        print(json.dumps(wynik, ensure_ascii=False, indent=1))
    else:
        print(f"=== STRAŻNIK: {plik.name} → {werdykt} ===")
        for k, v in R.items():
            print(f"[{v['status']:9}] {k}: {json.dumps(v['detale'], ensure_ascii=False)[:200]}")
    sys.exit(0 if werdykt == "PASS" else 1)

if __name__ == "__main__":
    main()
