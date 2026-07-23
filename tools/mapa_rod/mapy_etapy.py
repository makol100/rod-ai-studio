# -*- coding: utf-8 -*-
"""
MAPY ETAPOW 1/2/3 — ROD im. Jozefa Lompy.  1920x1080.
Wszystkie na WSPOLNEJ BAZIE (baza_mapy.py) — w filmie widz patrzy caly czas na ten sam
ogrod, zmienia sie tylko instalacja.

ETAP 1: stan wyjsciowy — jedno przylacze przy domu dzialkowca, jeden licznik glowny,
        caly ogrod na trzech wspolnych przewodach, kazda dzialka ma tylko PODLICZNIK.
ETAP 2: odciazenie — drugie przylacze ze slupa przy drodze, dwa liczniki glowne,
        7 dzialek (1,2,3,4 + 16,17,18) wypietych z domu. Pozostale 44 po staremu.
ETAP 3: docelowo — trzy zlacza ZK, 51 licznikow w szafach, osobny kabel do kazdej dzialki.
        ZK 3 = PLAN (kable niewkopane).

UWAGA: ETAP 1 i 3 to rekonstrukcja logiczna zaakceptowana przez Tomasza 12.07.2026 ("Ok.").
ETAP 2 odtworzony 1:1 z jego oryginalu (GEMINI-etap2.jpg).

WYMAGA: pip install pillow
"""
from baza_mapy import (rysuj_baze, stopka, pozycje_dzialek, x_kol, srodek, font,
                       X_DROGA, DROGA_W, X0, X_KON, Y_ALN, Y_ALS, Y_ALP, AL_H,
                       Y_R4, DZ_H, DZ_W, W, H)

CZARNY = "#2C2C2C"      # alejka polnocna
ZLOTY = "#C8922E"       # alejka srodkowa
TURKUS = "#3AAFC9"      # alejka poludniowa
FIOLET = "#8E6BB0"      # prad ze slupa
ZIELEN, ZIELEN_C = "#2E9E7A", "#1F7A5C"
SZARY = "#A9A294"

OUT = "/root/rod-ai-studio/data/rolka-prad/mapy-16x9"

POZ = pozycje_dzialek()
X_ALEJ_START = X_DROGA + DROGA_W


def dom_punkt():
    xa, _ = x_kol(0)
    return xa + 30, Y_R4 + DZ_H / 2


def slup_punkt():
    return X_DROGA + DROGA_W / 2, Y_ALP - 40


def kropka(d, x, y, kolor, r=6):
    d.ellipse([x - r, y - r, x + r, y + r], fill=kolor)


def magistrala(d, y_alej, kolor, dzialki_gora, dzialki_dol, x_start):
    """Wspolny przewod w alejce + podliczniki (kropki) przy kazdej dzialce."""
    y = y_alej + AL_H / 2
    d.line([(x_start, y), (X_KON - 30, y)], fill=kolor, width=7)
    for nr in dzialki_gora + dzialki_dol:
        if nr not in POZ:
            continue
        xa, xb, y0, y1 = POZ[nr]
        xw = (xa + xb) / 2
        gora = y1 <= y_alej + 2
        d.line([(xw, y), (xw, y0 if not gora else y1)], fill=kolor, width=4)
        kropka(d, xw, y, kolor)


# ============================ ETAP 1 ============================
def etap1_kable(d):
    dx, dy = dom_punkt()
    d.line([(dx, dy), (dx, Y_ALN + AL_H / 2)], fill=CZARNY, width=7)
    d.line([(dx, dy), (dx, Y_ALS + AL_H / 2)], fill=ZLOTY, width=7)
    d.line([(dx, dy), (dx, Y_ALP + AL_H / 2)], fill=TURKUS, width=7)
    magistrala(d, Y_ALN, CZARNY, [51, 50, 49, 48, 47, 46, 45, 44, 43],
               [34, 35, 36, 37, 38, 39, 40, 41, 42], dx)
    magistrala(d, Y_ALS, ZLOTY, [33, 32, 31, 30, 29, 28],
               [19, 20, 21, 22, 23, 24, 25, 26, 27], dx)
    magistrala(d, Y_ALP, TURKUS, [18, 17, 16, 15, 14, 13, 12, 11, 10],
               [1, 2, 3, 4, 5, 6, 7, 8, 9], dx)


img, d = rysuj_baze(
    "ZASILANIE — ETAP 1  (stan wyjściowy)",
    "Jedno przyłącze przy domu działkowca · jeden licznik główny · cały ogród na wspólnych przewodach",
    etap1_kable)
dx, dy = dom_punkt()
kropka(d, dx, dy, "#FFF", 11)
kropka(d, dx, dy, CZARNY, 7)
stopka(d,
       "Wszystkie 51 działek wisi na trzech wspólnych przewodach — każda ma tylko PODLICZNIK.",
       "Jedno przyłącze, jeden licznik główny. Prąd dzielony w ogrodzie, rozliczany podlicznikami.",
       [(CZARNY, "alejka północna"), (ZLOTY, "alejka środkowa"), (TURKUS, "alejka południowa")])
img.save(f"{OUT}/ETAP1-16x9.jpg", "JPEG", quality=93)

# ============================ ETAP 2 ============================
NA_SLUPIE = [1, 2, 3, 4, 16, 17, 18]


def etap2_kable(d):
    dx, dy = dom_punkt()
    d.line([(dx, dy), (dx, Y_ALN + AL_H / 2)], fill=CZARNY, width=7)
    d.line([(dx, dy), (dx, Y_ALS + AL_H / 2)], fill=ZLOTY, width=7)
    magistrala(d, Y_ALN, CZARNY, [51, 50, 49, 48, 47, 46, 45, 44, 43],
               [34, 35, 36, 37, 38, 39, 40, 41, 42], dx)
    magistrala(d, Y_ALS, ZLOTY, [33, 32, 31, 30, 29, 28],
               [19, 20, 21, 22, 23, 24, 25, 26, 27], dx)
    magistrala(d, Y_ALP, TURKUS, [15, 14, 13, 12, 11, 10], [5, 6, 7, 8, 9], dx)
    sx, sy = slup_punkt()
    d.line([(sx, sy), (sx, Y_ALP + AL_H + 60)], fill=FIOLET, width=7)
    y_f = Y_ALP + AL_H + 60
    d.line([(sx, y_f), (X0 + 4 * (DZ_W + 9), y_f)], fill=FIOLET, width=7)
    for nr in NA_SLUPIE:
        xa, xb, y0, y1 = POZ[nr]
        xw = (xa + xb) / 2
        d.line([(xw, y_f), (xw, y0 if y0 > y_f else y1)], fill=FIOLET, width=4)
        kropka(d, xw, y_f, FIOLET)


img, d = rysuj_baze(
    "ZASILANIE — ETAP 2  (odciążenie)",
    "Drugie przyłącze ze słupa przy drodze · dwa liczniki główne · siedem działek zdjętych z domu",
    etap2_kable)
dx, dy = dom_punkt()
kropka(d, dx, dy, "#FFF", 11); kropka(d, dx, dy, CZARNY, 7)
sx, sy = slup_punkt()
d.rounded_rectangle([sx - 22, sy - 30, sx + 22, sy + 14], radius=6, fill="#FFF",
                    outline=FIOLET, width=4)
for nr in NA_SLUPIE:
    xa, xb, y0, y1 = POZ[nr]
    d.rounded_rectangle([xa - 3, y0 - 3, xb + 3, y1 + 3], radius=11, outline=FIOLET, width=5)
stopka(d,
       "Siedem działek najbliżej drogi — 1, 2, 3, 4 oraz 16, 17, 18 — wypięto z domu działkowca.",
       "Mają własne przyłącze ze słupa i drugi licznik główny. Pozostałe 44 działki zostały po staremu.",
       [(CZARNY, "alejka północna"), (ZLOTY, "alejka środkowa"),
        (TURKUS, "alejka południowa"), (FIOLET, "prąd ze słupa")])
img.save(f"{OUT}/ETAP2-16x9.jpg", "JPEG", quality=93)

# ============================ ETAP 3 ============================
ZK1 = list(range(1, 19))
ZK2 = list(range(19, 34))
ZK3 = list(range(34, 52))


def etap3_kable(d):
    for zk_lista, y_alej, plan in ((ZK1, Y_ALP, False), (ZK2, Y_ALS, False), (ZK3, Y_ALN, True)):
        kolor = SZARY if plan else ZIELEN
        y = y_alej + AL_H / 2
        zx = X_ALEJ_START + 24
        for k, nr in enumerate(sorted(zk_lista)):
            if nr not in POZ:
                continue
            xa, xb, y0, y1 = POZ[nr]
            xw = (xa + xb) / 2
            gora = y1 <= y_alej + 2
            y_tor = y + ((k % 9) * 2.2 - 9)
            if plan:
                for s in range(int((xw - zx) / 22)):
                    d.line([(zx + s * 22, y_tor), (zx + s * 22 + 12, y_tor)], fill=kolor, width=2)
            else:
                d.line([(zx, y_tor), (xw, y_tor)], fill=kolor, width=2)
            d.line([(xw, y_tor), (xw, y1 if gora else y0)], fill=kolor, width=2)


img, d = rysuj_baze(
    "ZASILANIE — ETAP 3  (docelowo)",
    "Trzy złącza kablowe · 51 liczników w szafach · osobny kabel i własne przyłącze dla każdej działki",
    etap3_kable)
for nazwa, y_alej, plan in (("ZK1", Y_ALP, False), ("ZK2", Y_ALS, False), ("ZK3", Y_ALN, True)):
    kolor = SZARY if plan else ZIELEN_C
    y = y_alej + AL_H / 2
    zx = X_ALEJ_START + 4
    d.rounded_rectangle([zx - 26, y - 30, zx + 30, y + 30], radius=8, fill="#FFF",
                        outline=kolor, width=5)
    srodek(d, (zx + 2, y), nazwa, font("Bold", 19), kolor)
stopka(d,
       "Każda działka dostaje własny kabel ze złącza i własny licznik — bezpośrednio od Taurona.",
       "ZK 1 (działki 1–18) i ZK 2 (19–33) — kable wkopane. ZK 3 (34–51) — złącze stoi, kable w planie.",
       [(ZIELEN, "kabel wkopany"), (SZARY, "w planie")])
img.save(f"{OUT}/ETAP3-16x9.jpg", "JPEG", quality=93)

print("gotowe: ETAP1, ETAP2, ETAP3")
