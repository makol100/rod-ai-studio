#!/usr/bin/env python3
"""Punkty sfer 360 na mapie ogrodu (D-0313: co 10 m) — numeracja = kolejnosc zdjec na trasie.
Wyjscie: data/spacer_oryginaly/punkty.json (nr, opis, x%, y%) + /tmp/mapa_punkty.jpg.
Skala z wymiarow Tomasza (04.09.2026): dzialka 20 m wzdluz alejki x 25 m w glab."""
import json, sys, math
from pathlib import Path
sys.path.insert(0, '/root/rod-ai-studio/tools/mapa_rod')
from baza_mapy import x_kol, X0, X_KON, X_DROGA, DROGA_W, Y_MAPA, PARK2_H, Y_ALN, Y_ALS, Y_ALP, AL_H, Y_R4, Y_R5, DZ_H, W, H, font
from PIL import Image, ImageDraw

KROK = 10.0
PX_M_X = (x_kol(0)[1] - x_kol(0)[0]) / 20.0          # px na metr wzdluz alejki (dzialka 20 m)
Y_PK2 = Y_MAPA + PARK2_H / 2
Y_PN, Y_SR, Y_PD = Y_ALN + AL_H / 2, Y_ALS + AL_H / 2, Y_ALP + AL_H / 2
_, x2b = x_kol(2); x3a, _ = x_kol(3); X_P = (x2b + x3a) / 2      # przejscia 36|37, 21|22, 16|15
_, x7b = x_kol(7); x8a, _ = x_kol(8); X_E = (x7b + x8a) / 2      # przejscie 43|44
X_BRAMA = X_DROGA + DROGA_W + 33
X_KONIEC = X_KON - 12

def odc(x1, y1, x2, y2, dl_m, opis, obow_start=None, obow_koniec=None):
    """odcinek o realnej dlugosci dl_m; zwraca liste punktow co KROK m (z koncami)."""
    n = int(round(dl_m / KROK))
    pts = []
    for i in range(n + 1):
        t = i / n if n else 0
        m = min(dl_m, i * KROK) if i < n else dl_m
        t = m / dl_m
        o = opis
        if i == 0 and obow_start: o = obow_start
        if i == n and obow_koniec: o = obow_koniec
        pts.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, o, bool((i == 0 and obow_start) or (i == n and obow_koniec))))
    return pts

L_ALEJKA = (X_KONIEC - X_BRAMA) / PX_M_X            # brama -> koniec
L_ZACH = (X_P - X_BRAMA) / PX_M_X                   # brama -> przejscie 36|37 / 21|22
L_WSCH = (X_KONIEC - X_P) / PX_M_X                  # przejscie -> koniec
L_E_WSCH = (X_KONIEC - X_E) / PX_M_X                # 43|44 -> koniec

trasa = [
    odc(X_BRAMA, Y_PK2, X_KONIEC, Y_PK2, L_ALEJKA, "Parking 2", "BRAMA 1", "koniec Parkingu 2"),
    # powrot do 43|44 bez zdjec
    odc(X_E, Y_PK2, X_E, Y_PN, 25, "przejście 43|44", "skrzyż. Parking 2 × przejście", "skrzyż. Północna × 43|44"),
    odc(X_E, Y_PN, X_KONIEC, Y_PN, L_E_WSCH, "Północna wschód", None, "koniec Północnej"),
    # powrot
    odc(X_E, Y_PN, X_BRAMA, Y_PN, (X_E - X_BRAMA) / PX_M_X, "Północna", None, "BRAMA 2"),
    # powrot do 36|37
    odc(X_P, Y_PN, X_P, Y_SR, 50, "przejście 36|37", "skrzyż. Północna × 36|37", "skrzyż. Środkowa × 36|37"),
    odc(X_P, Y_SR, X_BRAMA, Y_SR, L_ZACH, "Środkowa zachód", None, "BRAMA 3"),
    odc(X_P, Y_SR, X_KONIEC, Y_SR, L_WSCH, "Środkowa wschód", None, "koniec Środkowej"),
    odc(X_P, Y_SR, X_P, Y_PD, 50, "przejście 21|22→16|15", None, "skrzyż. Południowa × 16|15"),
    odc(X_P, Y_PD, X_BRAMA, Y_PD, L_ZACH, "Południowa zachód", None, "BRAMA 4"),
    odc(X_P, Y_PD, X_KONIEC, Y_PD, L_WSCH, "Południowa wschód", None, "koniec Południowej"),
]
# Parking 1 + Dom Dzialkowca (po odcinku Srodkowa zachod) — wstawione jako osobne punkty obowiazkowe
_dxa, _ = x_kol(1); _k2a, _k2b = x_kol(2); _dxb = _k2a + (_k2b - _k2a) / 2
_pxa, _ = x_kol(0)
extra_po_srodkowej_zach = [((_dxa + _dxb) / 2, Y_R4 + DZ_H - 16, "przed Domem Działkowca", True),
                           ((_pxa + _dxa) / 2, Y_R4 + DZ_H / 2, "Parking 1", True)]
trasa[5] = trasa[5] + extra_po_srodkowej_zach

punkty = []
def blisko(x, y):
    return any(math.hypot(x - p['x'], y - p['y']) < 30 for p in punkty)
for seg in trasa:
    for x, y, o, ob in seg:
        if blisko(x, y):
            # punkt juz jest (skrzyzowanie) — tylko uzupelnij opis obowiazkowy
            for p in punkty:
                if math.hypot(x - p['x'], y - p['y']) < 30 and ob: p['opis'] = o; p['obow'] = True
            continue
        punkty.append({'nr': len(punkty) + 1, 'x': round(x, 1), 'y': round(y, 1), 'opis': o, 'obow': ob})

out = Path('/root/rod-ai-studio/data/spacer_oryginaly/punkty.json'); out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps([{**p, 'x_proc': round(p['x'] / W * 100, 2), 'y_proc': round(p['y'] / H * 100, 2)} for p in punkty], ensure_ascii=False, indent=1))

im = Image.open('/root/rod-ai-studio/data/rolka-prad/mapy-16x9/MAPA-OGRODU-16x9.jpg').convert('RGB')
d = ImageDraw.Draw(im, 'RGBA')
f = font("Bold", 15); fl = font("Bold", 24)
for p in punkty:
    r = 14
    kol = (235, 120, 30, 255) if p['obow'] else (25, 90, 210, 255)
    d.ellipse([p['x'] - r, p['y'] - r, p['x'] + r, p['y'] + r], fill=(255, 255, 255, 245), outline=kol, width=3)
    t = str(p['nr']); bb = d.textbbox((0, 0), t, font=f)
    d.text((p['x'] - (bb[2] - bb[0]) / 2 - bb[0], p['y'] - (bb[3] - bb[1]) / 2 - bb[1]), t, fill=kol, font=f)
d.rectangle([120, 955, 1100, 1050], fill=(255, 255, 255, 240), outline=(25, 90, 210), width=3)
d.ellipse([140, 968, 168, 996], fill='white', outline=(25, 90, 210), width=3)
d.text((180, 970), f"punkt zdjęcia 360° co {int(KROK)} m — numer = kolejność ({len(punkty)} punktów)", fill=(15, 60, 160), font=fl)
d.ellipse([140, 1008, 168, 1036], fill='white', outline=(235, 120, 30), width=3)
d.text((180, 1010), "punkt obowiązkowy: bramy, skrzyżowania, końce alejek, Dom, parkingi", fill=(160, 70, 10), font=fl)
im.save('/tmp/mapa_punkty.jpg', quality=92)
print(f"punktow: {len(punkty)}")
for p in punkty:
    if p['obow']: print(f"  {p['nr']:3d} {p['opis']}")
