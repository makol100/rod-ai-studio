#!/usr/bin/env python3
"""FOTOPULAPKA ROD — nocny nasluch kamer Dzialki.
Pobiera klatki z HA, wykrywa RUCH po naszej stronie (nie ufamy detekcji kamer),
zapisuje sekwencje zdarzenia. Zero zmian w konfiguracji HA — tylko odczyt.
Uzycie: fotopulapka.py [--kamery a,b] [--co 15] [--minuty 60] [--prog 0.9]
"""
import argparse, os, time, urllib.request, datetime, io
import numpy as np
from PIL import Image

BAZA = os.environ.get("HA_DZIALKA_URL", "http://100.115.112.5:8123")
TOK = os.environ.get("HA_DZIALKA_TOKEN") or open(os.environ.get("HA_TOKEN_FILE", "/root/.ha_dzialka_token")).read().strip()
KAT = "/root/rod-ai-studio/data/fotopulapka"

def klatka(kamera):
    req = urllib.request.Request(f"{BAZA}/api/camera_proxy/camera.{kamera}",
                                 headers={"Authorization": f"Bearer {TOK}"})
    return urllib.request.urlopen(req, timeout=25).read()

def szary(dane):
    im = Image.open(io.BytesIO(dane)).convert("L").resize((320, 180))
    a = np.asarray(im, dtype=np.float32)
    return a - a.mean()          # odporne na zmiane jasnosci (IR wl/wyl)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kamery", default="security_camera,kamera_taras")
    p.add_argument("--co", type=int, default=15)
    p.add_argument("--minuty", type=int, default=60)
    p.add_argument("--prog", type=float, default=0.9, help="procent zmienionych pikseli")
    a = p.parse_args()
    kamery = [k.strip() for k in a.kamery.split(",")]
    poprzednie, koniec, zdarzen = {}, time.time() + a.minuty * 60, 0
    os.makedirs(f"{KAT}/klatki", exist_ok=True)
    while time.time() < koniec:
        for k in kamery:
            try:
                d = klatka(k); n = szary(d)
            except Exception as e:
                print(f"[{k}] blad: {e}", flush=True); continue
            if k in poprzednie:
                zmiana = float((np.abs(n - poprzednie[k]) > 26).mean() * 100)
                if zmiana >= a.prog:
                    zdarzen += 1
                    t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    sc = f"{KAT}/klatki/{k}_{t}_{zmiana:.1f}pc.jpg"
                    open(sc, "wb").write(d)
                    print(f"RUCH {k} {t} zmiana={zmiana:.1f}% -> {sc}", flush=True)
            poprzednie[k] = n
        time.sleep(a.co)
    print(f"KONIEC. zdarzen={zdarzen}", flush=True)

if __name__ == "__main__":
    main()
