#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BRAMKA OKA — stała, fail-closed bramka wizualna Fabryki Rolek.
Powstała 28.07.2026 po wpadce WD_0001 v2 (Genek dał 10/10 nie widząc pliku:
read >20MB padł, ocena poszła z promptu; kafle 75-160px nie wykrywały orientacji).

ZASADY (dekret Tomasza "Naprawiać", 28.07.2026):
 1. FAIL ODCZYTU ŹRÓDŁA = FAIL BRAMKI. Żadnej oceny bez potwierdzonego obrazu.
 2. Ocena na PEŁNEJ rozdzielczości, per klatka/slot — nigdy mozaika kafelków.
 3. Prompt BEZ opisu treści materiału — model nie dostaje paliwa do konfabulacji;
    pole "opis" w odpowiedzi = dowód seansu (weryfikowalny przez człowieka/załogę).

Użycie:
  python3 bramka_oka.py WIDEO.mp4 --czasy 12.5,18.5,24 [--out raport.json] [--model gemini-2.5-flash]
Exit: 0 = wszystkie OK; 2 = co najmniej jeden FAIL; 3 = błąd krytyczny.
"""
import argparse, base64, json, os, subprocess, sys, tempfile, time, urllib.request, urllib.error

MIN_JPEG_BYTES = 10_000          # klatka mniejsza = ekstrakcja podejrzana -> FAIL
MAX_B64_BYTES  = 19_000_000      # limit inline_data API (20MB) z zapasem -> FAIL, nie cisza
API_TMPL = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}"

PROMPT = (
 "Jesteś bramką jakości wideo. Oceń WYŁĄCZNIE załączony obraz (klatka pionowego wideo 9:16). "
 "Nie znasz kontekstu materiału i nie wolno Ci niczego zakładać poza tym, co widać. "
 "Odpowiedz TYLKO poprawnym JSON o polach: "
 '{"opis": "co widać, jedno zdanie", '
 '"orientacja_tresci": "pion|lezaca|obrocona_90|obrocona_180|mieszana", '
 '"artefakty": ["lista problemów lub pusta"], '
 '"verdict": "OK|FAIL", "powod": "jedno zdanie"}. '
 "FAIL gdy: treść leżąca/obrócona (ludzie, maszyny, budynki lub horyzont na boku albo do góry nogami) "
 "lub poważny artefakt renderu (bezsensowne rozmycie części kadru, glitch, urwany/pusty kadr, podwójny obraz). "
 "Rozmyte pasy u góry i dołu wypełniające pion przy OSTRYM, poprawnie zorientowanym środku (blur-fill) "
 "to dopuszczalny zabieg montażowy — NIE artefakt. Czołówka z napisami na wideo to norma."
)

def log(msg): print(msg, flush=True)

def wytnij_klatke(video, t, tmpdir):
    """Ekstrakcja klatki w pełnej rozdzielczości. Zwraca ścieżkę JPEG albo (None, powód)."""
    out = os.path.join(tmpdir, f"klatka_t{t}.jpg")
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", video,
           "-frames:v", "1", "-q:v", "2", out]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        return None, f"ffmpeg exit {r.returncode}: {r.stderr.strip()[:200]}"
    if not os.path.isfile(out):
        return None, "ffmpeg nie utworzyl pliku klatki"
    sz = os.path.getsize(out)
    if sz < MIN_JPEG_BYTES:
        return None, f"klatka podejrzanie mala ({sz} B < {MIN_JPEG_BYTES})"
    return out, None

def ocen_klatke(jpeg_path, model, key):
    """Wysyła JEDNĄ klatkę do oceny. Fail-closed na każdym kroku."""
    try:
        with open(jpeg_path, "rb") as f:
            raw = f.read()
    except OSError as e:
        return {"verdict": "FAIL", "powod": f"BLAD ODCZYTU KLATKI: {e}", "_faza": "read"}
    if len(raw) < MIN_JPEG_BYTES:
        return {"verdict": "FAIL", "powod": f"klatka za mala ({len(raw)} B)", "_faza": "read"}
    b64 = base64.b64encode(raw).decode("ascii")
    if len(b64) > MAX_B64_BYTES:
        return {"verdict": "FAIL", "powod": f"obraz za duzy dla inline API ({len(b64)} B b64)", "_faza": "size"}
    body = json.dumps({
        "contents": [{"parts": [
            {"inline_data": {"mime_type": "image/jpeg", "data": b64}},
            {"text": PROMPT},
        ]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 2048,
                             "responseMimeType": "application/json",
                             "thinkingConfig": {"thinkingBudget": 0}},
    }).encode("utf-8")
    req = urllib.request.Request(API_TMPL.format(m=model, k=key), data=body,
                                 headers={"Content-Type": "application/json"})
    last_err = None
    for proba in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
            last_err = e
            if proba == 1:
                time.sleep(4); continue
            return {"verdict": "FAIL", "powod": f"BLAD API po 2 probach: {e}", "_faza": "api"}
    try:
        txt = data["candidates"][0]["content"]["parts"][0]["text"]
        wynik = json.loads(txt)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as e:
        return {"verdict": "FAIL", "powod": f"NIEPOPRAWNA ODPOWIEDZ MODELU: {e}; raw={str(data)[:300]}",
                "_faza": "format"}
    if wynik.get("verdict") not in ("OK", "FAIL"):
        return {"verdict": "FAIL", "powod": f"verdict poza norma: {wynik.get('verdict')!r}", "_faza": "format"}
    wynik["_faza"] = "ok"
    wynik["_jpeg_bytes"] = len(raw)
    return wynik

def main():
    ap = argparse.ArgumentParser(description="Fail-closed bramka wizualna (pelna rozdzielczosc, per klatka)")
    ap.add_argument("video")
    ap.add_argument("--czasy", required=True, help="sekundy po przecinku, np. 12.5,18.5,24")
    ap.add_argument("--model", default="gemini-2.5-flash")
    ap.add_argument("--out", default=None, help="sciezka raportu JSON (domyslnie <video>_bramka_oka.json)")
    a = ap.parse_args()

    if not os.path.isfile(a.video):
        log(f"KRYTYCZNY: brak pliku wideo {a.video}"); sys.exit(3)
    key = None
    env = "/root/.gemini/.env"
    if os.path.isfile(env):
        for line in open(env):
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    key = key or os.environ.get("GEMINI_API_KEY")
    if not key:
        log("KRYTYCZNY: brak GEMINI_API_KEY (/root/.gemini/.env)"); sys.exit(3)

    czasy = [float(x) for x in a.czasy.split(",") if x.strip()]
    out_path = a.out or (os.path.splitext(a.video)[0] + "_bramka_oka.json")
    raport = {"video": a.video, "model": a.model, "kiedy": time.strftime("%Y-%m-%d %H:%M:%S"),
              "zasada": "fail-closed; pelna rozdzielczosc; prompt bez opisu tresci", "klatki": []}
    fail = 0
    with tempfile.TemporaryDirectory(prefix="bramka_oka_") as tmp:
        for t in czasy:
            jpeg, err = None, None
            try:
                jpeg, err = wytnij_klatke(a.video, t, tmp)
            except Exception as e:
                err = f"wyjatek ekstrakcji: {e}"
            if err:
                w = {"t": t, "verdict": "FAIL", "powod": f"EKSTRAKCJA: {err}", "_faza": "extract"}
            else:
                w = ocen_klatke(jpeg, a.model, key); w["t"] = t
            if w.get("verdict") != "OK":
                fail += 1
            raport["klatki"].append(w)
            log(f"t={t:>6}  {w.get('verdict'):4}  orient={w.get('orientacja_tresci','-'):12}  {w.get('powod','')[:100]}")
            if w.get("opis"):
                log(f"         opis: {w['opis'][:140]}")
    raport["podsumowanie"] = {"klatek": len(czasy), "fail": fail,
                              "werdykt": "OK" if fail == 0 else "FAIL"}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(raport, f, ensure_ascii=False, indent=1)
    log(f"WERDYKT BRAMKI: {raport['podsumowanie']['werdykt']}  ({fail}/{len(czasy)} FAIL)  raport: {out_path}")
    sys.exit(0 if fail == 0 else 2)

if __name__ == "__main__":
    main()
