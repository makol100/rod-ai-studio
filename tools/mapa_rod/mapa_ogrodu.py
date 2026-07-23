# -*- coding: utf-8 -*-
"""
MAPA OGRODU (przegladowa) — ROD im. Jozefa Lompy.  1920x1080.
Ta sama baza co mapy etapow — w filmie widz caly czas patrzy na ten sam ogrod.
Bez kabli: sam uklad (51 dzialek, 3 alejki, 4 bramy, 2 parkingi, dom dzialkowca).
"""
from baza_mapy import rysuj_baze, font, W, H, Y_KON, LINIA, TEKST, TEKST_2

OUT = "/root/rod-ai-studio/data/rolka-prad/mapy-16x9"

img, d = rysuj_baze(
    "ROD im. Józefa Lompy  —  MAPA OGRODU",
    "Woźniki, Młyńska 40c  ·  51 działek + dom działkowca (0)  ·  3 alejki  ·  4 bramy  ·  2 parkingi",
    None)

# --- legenda: liczby + numeracja ---
F_LICZ, F_LEG = font("Bold", 34), font("Regular", 22)
y = Y_KON + 22
d.line([(44, y), (W - 44, y)], fill=LINIA, width=2)
y += 20

x = 44
for lb, op in [("51", "działek"), ("3", "alejki"), ("4", "bramy"),
               ("2", "parkingi"), ("1", "dom działkowca (0)")]:
    d.text((x, y), lb, font=F_LICZ, fill=TEKST)
    l, t, r, b = d.textbbox((0, 0), lb, font=F_LICZ)
    d.text((x + (r - l) + 10, y + 12), op, font=F_LEG, fill=TEKST_2)
    l2, t2, r2, b2 = d.textbbox((0, 0), op, font=F_LEG)
    x += (r - l) + (r2 - l2) + 46

d.text((W - 640, y + 2), "Numeracja biegnie wężem po rzędach:", font=F_LEG, fill=TEKST_2)
d.text((W - 640, y + 28), "1→9  ·  10→18  ·  19→27  ·  28→33  ·  34→42  ·  43→51",
       font=F_LEG, fill=TEKST_2)

img.save(f"{OUT}/MAPA-OGRODU-16x9.jpg", "JPEG", quality=93)
print("gotowe: MAPA OGRODU")
