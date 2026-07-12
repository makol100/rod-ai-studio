# -*- coding: utf-8 -*-
"""
MAPY ZK 1/2/3 — ROD im. Jozefa Lompy.  FORMAT 1920x1080 (film).
Alejka lezy tak jak w terenie: ZK od zachodu (przy bramie), dzialki ciagna sie na wschod.
Zatwierdzone przez Tomasza 12.07.2026 ("gra", "bardzo idealnie").

FAKTY (potwierdzone):
  ZK 1 — alejka poludniowa, dzialki 1-18, 18 licznikow. Kable WKOPANE.
  ZK 2 — alejka srodkowa, dzialki 19-33, 15 licznikow. Kable WKOPANE.
         Rzad polnocny zaczyna sie od DOMU DZIALKOWCA i PARKINGU NR 1, potem 33..28.
  ZK 3 — alejka polnocna, dzialki 34-51, 18 licznikow. Zlacze stoi, kable NIEWKOPANE = PLAN.

Rzad = lista pozycji: int -> dzialka (dostaje kabel), (etykieta, szer) -> blok bez kabla.

WYMAGA: pip install pillow
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080

TLO, DZIALKA, DZIALKA_OB = "#F7F3EA", "#E5E1D8", "#CFC9BA"
ALEJKA, TEKST, TEKST_2 = "#DEDACE", "#2C2C2C", "#6B675E"
ZIELEN, ZIELEN_C, LINIA = "#2E9E7A", "#1F7A5C", "#C9C3B4"
PLAN_K, BLOK, BLOK_OB = "#A9A294", "#D8CFC0", "#BFB4A2"


def font(n, r):
    for s in (f"/usr/share/fonts/truetype/google-fonts/Poppins-{n}.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(s, r)
        except OSError:
            continue
    return ImageFont.load_default()


F_TYTUL, F_PODTYT = font("Bold", 58), font("Regular", 32)
F_NUMER, F_ZK = font("Bold", 64), font("Bold", 38)
F_MALY, F_BLOK = font("Regular", 25), font("Medium", 24)
F_STOPKA, F_STOPKA2 = font("Bold", 32), font("Regular", 27)


def srodek(d, xy, txt, f, k):
    x, y = xy
    l, t, r, b = d.textbbox((0, 0), txt, font=f)
    d.text((x - (r - l) / 2 - l, y - (b - t) / 2 - t), txt, font=f, fill=k)


def rysuj(nazwa, alejka_nazwa, gorny, dolny, plik, podtytul=None, stopka=None, plan=False):
    kab = PLAN_K if plan else ZIELEN
    zkc = PLAN_K if plan else ZIELEN_C
    img = Image.new("RGB", (W, H), TLO)
    d = ImageDraw.Draw(img)

    liczniki = sum(1 for r in (gorny, dolny) for p in r if isinstance(p, int))

    d.text((70, 48), f"{nazwa}  —  {alejka_nazwa}", font=F_TYTUL, fill=TEKST)
    d.text((70, 124), podtytul or "Z jednego złącza idzie osobny kabel do każdej działki.",
           font=F_PODTYT, fill=TEKST_2)
    if plan:
        d.rounded_rectangle([W - 320, 50, W - 70, 114], radius=10, fill="#FFF",
                            outline=PLAN_K, width=4)
        srodek(d, (W - 195, 82), "PLAN", font("Bold", 34), TEKST_2)
    d.line([(70, 186), (W - 70, 186)], fill=LINIA, width=2)

    def dlugosc(rzad):
        return sum(p[1] if isinstance(p, tuple) else 1 for p in rzad)

    N = max(dlugosc(gorny), dlugosc(dolny))
    X_ZK, ZK_W = 70, 180
    X0 = X_ZK + ZK_W + 60
    ODST = 14
    DZ_W = (W - 70 - X0 - (N - 1) * ODST) / N
    DZ_H, AL_H, Y_G = 205, 240, 235
    Y_A = Y_G + DZ_H
    Y_D = Y_A + AL_H

    d.rectangle([X_ZK + ZK_W // 2, Y_A, W - 70, Y_A + AL_H], fill=ALEJKA)

    ZK_X, ZK_Y = X_ZK + ZK_W // 2, Y_A + AL_H // 2
    krok = (AL_H / 2 - 22) / max(N - 1, 1)

    def pozycje(rzad):
        out, i = [], 0
        for p in rzad:
            szer = p[1] if isinstance(p, tuple) else 1
            xa = X0 + i * (DZ_W + ODST)
            xb = xa + szer * DZ_W + (szer - 1) * ODST
            out.append((p, xa, xb, i))
            i += szer
        return out

    # KABLE — dzialka blizej ZK dostaje tor blizej swojej krawedzi alejki (BRAK KRZYZOWAN)
    for rzad, gora in ((gorny, True), (dolny, False)):
        for p, xa, xb, i in pozycje(rzad):
            if not isinstance(p, int):
                continue
            y_tor = (Y_A + 12 + i * krok) if gora else (Y_A + AL_H - 12 - i * krok)
            y_cel = Y_A if gora else Y_A + AL_H
            xw = (xa + xb) / 2
            if plan:
                for s in range(int(abs(xw - ZK_X) / 24)):
                    sx = ZK_X + s * 24
                    d.line([(sx, y_tor), (sx + 13, y_tor)], fill=kab, width=3)
            else:
                d.line([(ZK_X, ZK_Y), (ZK_X, y_tor)], fill=kab, width=3)
                d.line([(ZK_X, y_tor), (xw, y_tor)], fill=kab, width=3)
            d.line([(xw, y_tor), (xw, y_cel)], fill=kab, width=3)
            d.ellipse([xw - 5, y_cel - 5, xw + 5, y_cel + 5], fill=zkc)

    # DZIALKI I BLOKI
    for rzad, y0 in ((gorny, Y_G), (dolny, Y_D)):
        for p, xa, xb, i in pozycje(rzad):
            if p is None:
                continue
            if isinstance(p, int):
                d.rounded_rectangle([xa, y0, xb, y0 + DZ_H], radius=12,
                                    fill=DZIALKA, outline=DZIALKA_OB, width=3)
                srodek(d, ((xa + xb) / 2, y0 + DZ_H / 2), str(p), F_NUMER, TEKST)
            else:
                d.rounded_rectangle([xa, y0, xb, y0 + DZ_H], radius=12,
                                    fill=BLOK, outline=BLOK_OB, width=3)
                for j, w in enumerate(p[0].split("\n")):
                    srodek(d, ((xa + xb) / 2, y0 + DZ_H / 2 - 14 + j * 32), w, F_BLOK, TEKST_2)

    # ZK — szafa po zachodniej stronie
    zk_h = 190
    zy = ZK_Y - zk_h // 2
    d.rounded_rectangle([X_ZK, zy, X_ZK + ZK_W, zy + zk_h], radius=14,
                        fill="#FFF", outline=zkc, width=6)
    for r_ in range(5):
        for c_ in range(4):
            lx, ly = X_ZK + 20 + c_ * 38, zy + 26 + r_ * 30
            d.rectangle([lx, ly, lx + 26, ly + 16], fill=kab, outline=zkc)
    srodek(d, (X_ZK + ZK_W // 2, zy + zk_h + 32), nazwa, F_ZK, zkc)
    srodek(d, (X_ZK + ZK_W // 2, zy + zk_h + 66), f"{liczniki} liczników", F_MALY, TEKST_2)
    srodek(d, (X_ZK + ZK_W // 2, zy - 34), "od strony drogi", F_MALY, TEKST_2)

    # STOPKA
    y_s = H - 132
    d.line([(70, y_s - 28), (W - 70, y_s - 28)], fill=LINIA, width=2)
    g, dr = stopka or (f"Wszystkie {liczniki} liczników stoi W ZŁĄCZU — po jednym na działkę.",
                       "Do działki idzie sam kabel. Koniec z podlicznikami.")
    d.text((70, y_s), g, font=F_STOPKA, fill=TEKST)
    d.text((70, y_s + 46), dr, font=F_STOPKA2, fill=TEKST_2)
    lx = W - 640
    d.rectangle([lx, y_s + 6, lx + 26, y_s + 26], fill="#FFF", outline=zkc, width=3)
    d.text((lx + 40, y_s), "licznik — stoi w ZK", font=F_MALY, fill=TEKST_2)
    d.line([(lx, y_s + 58), (lx + 46, y_s + 58)], fill=kab, width=5)
    d.text((lx + 60, y_s + 46), "osobny kabel do działki", font=F_MALY, fill=TEKST_2)

    img.save(plik, "JPEG", quality=93)
    return plik


if __name__ == "__main__":
    OUT = "/root/rod-ai-studio/data/rolka-prad/mapy-16x9"

    rysuj("ZK 1", "alejka południowa",
          gorny=[18, 17, 16, 15, 14, 13, 12, 11, 10],
          dolny=[1, 2, 3, 4, 5, 6, 7, 8, 9],
          plik=f"{OUT}/ZK1-16x9.jpg")

    rysuj("ZK 2", "alejka środkowa",
          gorny=[("DOM\nDZIAŁKOWCA", 2), ("PARKING\nNR 1", 1), 33, 32, 31, 30, 29, 28],
          dolny=[19, 20, 21, 22, 23, 24, 25, 26, 27],
          plik=f"{OUT}/ZK2-16x9.jpg")

    rysuj("ZK 3", "alejka północna",
          gorny=[51, 50, 49, 48, 47, 46, 45, 44, 43],
          dolny=[34, 35, 36, 37, 38, 39, 40, 41, 42],
          plik=f"{OUT}/ZK3-16x9.jpg",
          podtytul="Złącze stoi. Kable jeszcze niewkopane — to następny etap.",
          stopka=("Złącze gotowe, 18 liczników czeka na podłączenie.",
                  "Kable do działek zostaną wkopane w kolejnym etapie."),
          plan=True)
    print("gotowe: ZK1, ZK2, ZK3")
