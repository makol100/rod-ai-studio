#!/usr/bin/env python3
"""Edycja ISTNIEJACEGO obrazu przez gemini-3.1-flash-image (image+text -> image). ~0.067 USD/obraz.
Uzycie: gemini_edytuj.py --wejscie k5.jpg --prompt "..." --wyjscie out.png --zaplac
Bez --zaplac tylko drukuje request (0 USD)."""
import argparse, base64, json, os, sys, urllib.request, mimetypes
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
API = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-3.1-flash-image"
def klucz():
    k = os.environ.get("GEMINI_API_KEY")
    if not k:
        for p in (ROOT / ".env", Path("/root/.sekrety/wartosci.env")):
            if p.exists():
                for l in p.read_text().splitlines():
                    if l.startswith("GEMINI_API_KEY="): k = l.split("=", 1)[1].strip().strip('"\''); break
            if k: break
    if not k: sys.exit("brak GEMINI_API_KEY")
    return k
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--wejscie", required=True); ap.add_argument("--prompt", required=True)
    ap.add_argument("--wyjscie", required=True); ap.add_argument("--zaplac", action="store_true"); a = ap.parse_args()
    img = Path(a.wejscie).read_bytes(); mt = mimetypes.guess_type(a.wejscie)[0] or "image/jpeg"
    payload = {"contents": [{"parts": [{"inlineData": {"mimeType": mt, "data": base64.b64encode(img).decode()}}, {"text": a.prompt}]}],
               "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
    if not a.zaplac:
        print("SUCHY BIEG (0 USD). model:", MODEL, "| wejscie:", a.wejscie, len(img), "B | prompt:", a.prompt[:120]); return
    req = urllib.request.Request(f"{API}/models/{MODEL}:generateContent?key={klucz()}", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try: r = json.load(urllib.request.urlopen(req, timeout=180))
    except urllib.error.HTTPError as e: sys.exit("HTTP " + str(e.code) + ": " + e.read().decode()[:400])
    parts = (r.get("candidates") or [{}])[0].get("content", {}).get("parts", [])
    dane = next((p["inlineData"]["data"] for p in parts if p.get("inlineData")), None)
    txt = " ".join(p.get("text", "") for p in parts if p.get("text"))
    if not dane: sys.exit("brak obrazu w odpowiedzi; tekst: " + txt[:300])
    Path(a.wyjscie).write_bytes(base64.b64decode(dane)); print("ZAPISANO", a.wyjscie, Path(a.wyjscie).stat().st_size, "B | koszt ~0.067 USD |", txt[:150])
if __name__ == "__main__": main()
