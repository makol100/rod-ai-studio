# -*- coding: utf-8 -*-
"""
BAZA MAPY OGRODU — ROD im. Jozefa Lompy, Wozniki.
Wspolny podklad dla mapy ogrodu i map etapow. Format 1920x1080 (film YouTube).
Styl jasny (wzorzec GEMINI) — zatwierdzony przez Tomasza 12.07.2026.

WYMAGA: pip install pillow  (na VPS jeszcze NIE ma!)
Fonty: Poppins (google-fonts) z fallbackiem na DejaVu.

Uklad wg zatwierdzonej mapy fundamentowej:
  51 dzialek + dom dzialkowca (0), 3 alejki, 4 bramy, 2 parkingi.
  Numeracja wezem po rzedach: 1-9, 10-18, 19-27, 28-33, 34-42, 43-51.
  Kolumna wschodnia (9,10,27,28,42,43) — WIEKSZE dzialki.
  Granica polnocna UKOSNA; nad rzedem 43-51 lezy parking nr 2.
  Rzad srodkowy od zachodu: DOM DZIALKOWCA (2 kolumny) + PARKING NR 1 (1 kolumna), potem 33..28.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080

TLO, DZIALKA, DZIALKA_OB = "#F7F3EA", "#E5E1D8", "#CFC9BA"
ALEJKA, TEKST, TEKST_2 = "#DEDACE", "#2C2C2C", "#6B675E"
LINIA, DROGA, DROGA_L = "#C9C3B4", "#BDB7AA", "#F7F3EA"
DOM, DOM_OB = "#C2705F", "#A2533F"
BRAMA, BLOK, BLOK_OB = "#D9A441", "#D6CCBC", "#BDB1A0"


def font(n, r):
    for s in (f"/usr/share/fonts/truetype/google-fonts/Poppins-{n}.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(s, r)
        except OSError:
            continue
    return ImageFont.load_default()


F_TYT, F_POD = font("Bold", 44), font("Regular", 26)
F_NUM, F_ALEJ = font("Bold", 40), font("Medium", 22)
F_BLOK, F_MALY = font("Medium", 20), font("Regular", 21)
F_LEG, F_LICZ = font("Regular", 22), font("Bold", 34)

# --- geometria (stala dla wszystkich map) ---
X_DROGA, DROGA_W = 44, 62
X0 = X_DROGA + DROGA_W + 34
X_KON = W - 44
DZ_ODST, DUZA_EXTRA = 9, 42
DZ_W = (X_KON - X0 - 8 * DZ_ODST - DUZA_EXTRA) / 9
DZ_W_DUZA = DZ_W + DUZA_EXTRA
Y_MAPA, PARK2_H, DZ_H, AL_H = 132, 62, 104, 42

_y = Y_MAPA + PARK2_H
Y_R6 = _y; _y += DZ_H
Y_ALN = _y; _y += AL_H
Y_R5 = _y; _y += DZ_H
Y_R4 = _y; _y += DZ_H
Y_ALS = _y; _y += AL_H
Y_R3 = _y; _y += DZ_H
Y_R2 = _y; _y += DZ_H
Y_ALP = _y; _y += AL_H
Y_R1 = _y; _y += DZ_H
Y_KON = _y

RZEDY = [
    (Y_R6, [51, 50, 49, 48, 47, 46, 45, 44, 43]),
    (Y_R5, [34, 35, 36, 37, 38, 39, 40, 41, 42]),
    (Y_R4, ["DOM", "DOM", "PARK", 33, 32, 31, 30, 29, 28]),
    (Y_R3, [19, 20, 21, 22, 23, 24, 25, 26, 27]),
    (Y_R2, [18, 17, 16, 15, 14, 13, 12, 11, 10]),
    (Y_R1, [1, 2, 3, 4, 5, 6, 7, 8, 9]),
]


def x_kol(i):
    xa = X0 + i * (DZ_W + DZ_ODST)
    return xa, xa + (DZ_W_DUZA if i == 8 else DZ_W)


def pozycje_dzialek():
    """{numer_dzialki: (xa, xb, y0, y1)} — do podpinania kabli."""
    out = {}
    for y0, rzad in RZEDY:
        i = 0
        while i < len(rzad):
            p = rzad[i]
            if p == "DOM":
                i += 2
                continue
            xa, xb = x_kol(i)
            if p != "PARK":
                out[p] = (xa, xb, y0, y0 + DZ_H)
            i += 1
    return out


def srodek(d, xy, txt, f, k):
    x, y = xy
    l, t, r, b = d.textbbox((0, 0), txt, font=f)
    d.text((x - (r - l) / 2 - l, y - (b - t) / 2 - t), txt, font=f, fill=k)


def rysuj_baze(tytul, podtytul, przed_dzialkami=None):
    """przed_dzialkami: funkcja(d) — rysuje kable POD dzialkami."""
    img = Image.new("RGB", (W, H), TLO)
    d = ImageDraw.Draw(img)

    d.text((44, 26), tytul, font=F_TYT, fill=TEKST)
    d.text((46, 82), podtytul, font=F_POD, fill=TEKST_2)

    # droga (zachod)
    d.rectangle([X_DROGA, Y_MAPA, X_DROGA + DROGA_W, Y_KON], fill=DROGA)
    for yy in range(Y_MAPA + 14, Y_KON - 10, 34):
        d.line([(X_DROGA + DROGA_W / 2, yy), (X_DROGA + DROGA_W / 2, yy + 18)], fill=DROGA_L, width=3)
    srodek(d, (X_DROGA + DROGA_W / 2, Y_KON + 26), "DROGA", F_MALY, TEKST_2)

    # parking nr 2 (ukosna granica polnocna)
    d.polygon([(X0, Y_MAPA + PARK2_H), (X_KON, Y_MAPA + PARK2_H),
               (X_KON, Y_MAPA - 2), (X0, Y_MAPA + 40)], fill=BLOK, outline=BLOK_OB)
    d.text((X_KON - 250, Y_MAPA + 16), "PARKING NR 2", font=F_BLOK, fill=TEKST_2)

    # alejki
    for yy, nazwa in ((Y_ALN, "ALEJKA PÓŁNOCNA"), (Y_ALS, "ALEJKA ŚRODKOWA"),
                      (Y_ALP, "ALEJKA POŁUDNIOWA")):
        d.rectangle([X_DROGA + DROGA_W, yy, X_KON, yy + AL_H], fill=ALEJKA)
        l, t, r, b = d.textbbox((0, 0), nazwa, font=F_ALEJ)
        d.text((X_KON - (r - l) - 18, yy + (AL_H - (b - t)) / 2 - t), nazwa, font=F_ALEJ, fill=TEKST_2)

    # KABLE — rysowane POD dzialkami
    if przed_dzialkami:
        przed_dzialkami(d)

    # dzialki + bloki
    for y0, rzad in RZEDY:
        i = 0
        while i < len(rzad):
            p = rzad[i]
            if p == "DOM":
                xa, _ = x_kol(i)
                _, xb = x_kol(i + 1)
                d.rounded_rectangle([xa, y0, xb, y0 + DZ_H], radius=9, fill=DOM, outline=DOM_OB, width=3)
                d.ellipse([xa + 14, y0 + 14, xa + 52, y0 + 52], outline="#FFF", width=3)
                srodek(d, (xa + 33, y0 + 33), "0", font("Bold", 26), "#FFF")
                srodek(d, ((xa + xb) / 2 + 20, y0 + DZ_H / 2 + 8), "DOM DZIAŁKOWCA", F_BLOK, "#FFF")
                i += 2
                continue
            xa, xb = x_kol(i)
            if p == "PARK":
                d.rounded_rectangle([xa, y0, xb, y0 + DZ_H], radius=9, fill=BLOK, outline=BLOK_OB, width=3)
                srodek(d, ((xa + xb) / 2, y0 + DZ_H / 2 - 12), "PARKING", F_BLOK, TEKST_2)
                srodek(d, ((xa + xb) / 2, y0 + DZ_H / 2 + 14), "NR 1", F_BLOK, TEKST_2)
            else:
                d.rounded_rectangle([xa, y0, xb, y0 + DZ_H], radius=9, fill=DZIALKA,
                                    outline=DZIALKA_OB, width=3)
                srodek(d, ((xa + xb) / 2, y0 + DZ_H / 2), str(p), F_NUM, TEKST)
            i += 1

    # bramy (na wschodniej krawedzi drogi)
    for yy, nr in ((Y_MAPA + PARK2_H / 2, "1"), (Y_ALN + AL_H / 2, "2"),
                   (Y_ALS + AL_H / 2, "3"), (Y_ALP + AL_H / 2, "4")):
        d.rectangle([X_DROGA + DROGA_W, yy - 17, X_DROGA + DROGA_W + 10, yy + 17], fill=BRAMA)
        d.ellipse([X_DROGA + DROGA_W + 18, yy - 15, X_DROGA + DROGA_W + 48, yy + 15],
                  fill=TLO, outline=BRAMA, width=3)
        srodek(d, (X_DROGA + DROGA_W + 33, yy), nr, font("Bold", 20), TEKST_2)

    return img, d


def stopka(d, glowna, druga, legenda):
    """legenda: [(kolor, opis), ...]"""
    y = Y_KON + 22
    d.line([(44, y), (W - 44, y)], fill=LINIA, width=2)
    y += 18
    d.text((44, y), glowna, font=font("Bold", 28), fill=TEKST)
    d.text((44, y + 38), druga, font=F_LEG, fill=TEKST_2)
    x = W - 44
    for kolor, opis in reversed(legenda):
        l, t, r, b = d.textbbox((0, 0), opis, font=F_LEG)
        x -= (r - l)
        d.text((x, y + 14), opis, font=F_LEG, fill=TEKST_2)
        x -= 58
        d.line([(x + 6, y + 26), (x + 46, y + 26)], fill=kolor, width=6)
        x -= 26
