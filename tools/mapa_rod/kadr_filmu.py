# -*- coding: utf-8 -*-
"""
KADR FILMU 16:9 — pionowy material (zdjecie/wideo) w oknie + panel z trescia.

PROBLEM: caly material z budowy jest PIONOWY (telefon):
  zdjecia 1500x2000, filmy z WhatsAppa 478x850.
ROZWIAZANIE: nie przycinamy do poziomu (strata 2/3 kadru, uciete glowy).
Pokazujemy pionowy material W OKNIE o wysokosci ~900 px, a obok leci panel z tekstem.

  zdjecie 1500x2000 -> okno 675x900  = skala 0.45x  (ZMNIEJSZENIE, ostre)
  film    478x850   -> okno 506x900  = skala 1.06x  (praktycznie natywne)

Zatwierdzone przez Tomasza 12.07.2026.
UWAGA (do poprawy): panel bywa ZA PUSTY. Kazdy kadr musi dostac albo liczbe,
albo kawalek mapy, albo 3-4 wiersze tekstu. Sam tytul + 2 linijki to za malo.

WYMAGA: pip install pillow
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
TLO, TEKST, TEKST_2 = "#F7F3EA", "#2C2C2C", "#6B675E"
ZIELEN, ZIELEN_C, LINIA = "#2E9E7A", "#1F7A5C", "#C9C3B4"


def font(n, r):
    for s in (f"/usr/share/fonts/truetype/google-fonts/Poppins-{n}.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(s, r)
        except OSError:
            continue
    return ImageFont.load_default()


def kadr(zrodlo, tytul, linie, liczba=None, podpis_liczby=None, plik="out.jpg"):
    img = Image.new("RGB", (W, H), TLO)
    d = ImageDraw.Draw(img)

    # ---- OKNO Z MATERIALEM (lewa strona) ----
    src = Image.open(zrodlo).convert("RGB")
    OKNO_H = 900
    skala = OKNO_H / src.height
    ow, oh = int(src.width * skala), OKNO_H
    src = src.resize((ow, oh), Image.LANCZOS)
    ox, oy = 90, (H - oh) // 2

    cien = Image.new("RGB", (ow + 24, oh + 24), TLO)
    dc = ImageDraw.Draw(cien)
    dc.rounded_rectangle([12, 12, ow + 12, oh + 12], radius=14, fill="#DDD7C9")
    img.paste(cien.filter(ImageFilter.GaussianBlur(7)), (ox - 12, oy - 6))

    maska = Image.new("L", (ow, oh), 0)
    ImageDraw.Draw(maska).rounded_rectangle([0, 0, ow, oh], radius=14, fill=255)
    img.paste(src, (ox, oy), maska)

    # ---- PANEL (prawa strona) ----
    px = ox + ow + 80
    szer = W - px - 90

    y = oy + 40
    d.line([(px, y), (px + 70, y)], fill=ZIELEN, width=6)
    y += 40

    for w in tytul.split("\n"):
        d.text((px, y), w, font=font("Bold", 62), fill=TEKST)
        y += 76
    y += 26

    for w in linie:
        d.text((px, y), w, font=font("Regular", 34), fill=TEKST_2)
        y += 52

    if liczba:
        y += 40
        d.line([(px, y), (px + szer, y)], fill=LINIA, width=2)
        y += 34
        d.text((px, y), liczba, font=font("Bold", 96), fill=ZIELEN_C)
        l, t, r, b = d.textbbox((0, 0), liczba, font=font("Bold", 96))
        d.text((px + (r - l) + 24, y + 44), podpis_liczby or "",
               font=font("Regular", 32), fill=TEKST_2)

    img.save(plik, "JPEG", quality=93)
    print("zapisano:", plik, "| okno:", f"{ow}x{oh}", "| skala:", round(skala, 2))
    return plik


if __name__ == "__main__":
    # przyklad — zdjecie kabli w rowie (kluczowy kadr filmu: mapa mowi schemat, zdjecie mowi prawde)
    kadr("/root/rod-ai-studio/data/rolka-prad/budowa/kable-w-rowie.jpg",
         "Osiemnaście kabli\nw jednym rowie",
         ["Każdy kabel idzie do innej działki.", "Nikt nie wisi na wspólnym przewodzie."],
         liczba="18", podpis_liczby="osobnych kabli\nw alejce południowej",
         plik="/root/rod-ai-studio/data/rolka-prad/mapy-16x9/KADR-kable.jpg")
