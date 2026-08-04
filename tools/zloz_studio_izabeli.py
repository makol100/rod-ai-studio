#!/usr/bin/env python3
"""Skladanie studia Izabeli: puste tlo + wycieta postac + logo ROD + belki z napisami.

Uklad wzorowany na TV_STUDIO.png z 1.08 (przyjetym przez Tomasza), ale tlo jest teraz
OSOBNYM plikiem bez postaci, wiec postac da sie wymieniac bez generowania calosci od nowa.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

KATALOG = Path("/root/rod-ai-studio")
TLO = KATALOG / "assets/izabela/TLO_STUDIO_PUSTE_CANON.png"
POSTAC = KATALOG / "assets/izabela/IZABELA_ODKLEJONA_v2.png"
LOGO = KATALOG / "assets/branding/rod_profilowe.png"

SZER, WYS = 1080, 1920
CZCIONKI = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def czcionka(rozmiar, gruba=True):
    for s in (CZCIONKI if gruba else CZCIONKI[::-1]):
        if Path(s).exists():
            return ImageFont.truetype(s, rozmiar)
    return ImageFont.load_default()


def zloz(wyjscie, imie="IZABELA", podpis="wirtualny awatar zarządu",
         etykieta="PREZENTERKA AI"):
    tlo = Image.open(TLO).convert("RGB").resize((SZER, WYS), Image.LANCZOS)

    # --- postac: skalowana tak, zeby siegala dolnej belki ---
    p = Image.open(POSTAC).convert("RGBA")
    obrys = p.getbbox()
    p = p.crop(obrys)
    # WAZNE: dol postaci musi wejsc GLEBOKO POD dolna belke, inaczej widac ucieta krawedz
    # i postac "wisi w powietrzu" (wpadka 4.08 16:19 — konczyla sie 9 px nad belka).
    doc_belki = int(WYS * 0.775)          # dol postaci — schowany pod belka
    gora = int(WYS * 0.15)               # gdzie zaczyna sie glowa
    docelowa_wys = doc_belki - gora
    skala = docelowa_wys / p.height
    p = p.resize((max(1, int(p.width * skala)), docelowa_wys), Image.LANCZOS)

    # postac przesunieta z osi w prawo — miejsce na material z lewej
    x = int(SZER * 0.56) - p.width // 2
    tlo.paste(p, (x, gora), p)

    d = ImageDraw.Draw(tlo, "RGBA")

    # --- BLAT PREZENTERSKI (rysowany PO postaci, wiec zaslania jej ucieta krawedz) ---
    # Dodany 4.08 na polecenie Tomasza: "Stol jej dorobic".
    # Blat zaczyna sie TUZ PONIZEJ dolu postaci, zeby DLONIE LEZALY NA PLYCIE.
    # Wpadka 4.08 16:23: blat byl wyzej i zaslonil jej rece.
    blat_y = doc_belki                       # DOKLADNIE na dole postaci — ani piksela wyzej
    # cien pod blatem — zeby nie byl plaska plama
    d.rectangle([0, blat_y, SZER, WYS], fill=(8, 20, 36, 255))
    # plyta blatu: pionowy gradient od jasniejszego u gory do ciemnego u dolu
    for i in range(int(WYS * 0.06)):
        t = i / max(1, int(WYS * 0.06))
        kolor = (int(26 - 14 * t), int(52 - 30 * t), int(88 - 52 * t), 255)
        d.line([(0, blat_y + i), (SZER, blat_y + i)], fill=kolor)
    # swietlna krawedz blatu — tak wyglada podswietlany pulpit w studiu
    d.rectangle([0, blat_y, SZER, blat_y + 6], fill=(120, 168, 224, 235))
    d.rectangle([0, blat_y + 6, SZER, blat_y + 10], fill=(60, 96, 148, 180))
    # delikatne odbicie na plycie tuz pod krawedzia
    d.rectangle([0, blat_y + 11, SZER, blat_y + 32], fill=(40, 72, 120, 90))

    # --- gorna etykieta ---
    f_et = czcionka(34)
    tw = d.textbbox((0, 0), etykieta, font=f_et)
    d.rectangle([40, 92, 40 + (tw[2] - tw[0]) + 44, 92 + (tw[3] - tw[1]) + 30], fill=(90, 105, 125, 200))
    d.text((62, 104), etykieta, font=f_et, fill=(255, 255, 255, 255))

    # --- logo ROD w kole, prawy gorny rog ---
    if LOGO.exists():
        rozmiar = 118
        lg = Image.open(LOGO).convert("RGBA").resize((rozmiar, rozmiar), Image.LANCZOS)
        maska = Image.new("L", (rozmiar * 4, rozmiar * 4), 0)
        ImageDraw.Draw(maska).ellipse([0, 0, rozmiar * 4, rozmiar * 4], fill=255)
        lg.putalpha(maska.resize((rozmiar, rozmiar), Image.LANCZOS))
        tlo.paste(lg, (SZER - rozmiar - 42, 86), lg)

    # --- dolna belka z imieniem ---
    by = int(WYS * 0.865)
    d.rectangle([0, by, SZER, by + 132], fill=(10, 27, 46, 232))
    d.rectangle([0, by, 14, by + 132], fill=(196, 158, 74, 255))
    d.text((46, by + 20), imie, font=czcionka(62), fill=(255, 255, 255, 255))
    d.text((48, by + 92), podpis, font=czcionka(30, gruba=False), fill=(176, 198, 222, 255))

    Path(wyjscie).parent.mkdir(parents=True, exist_ok=True)
    tlo.save(wyjscie, optimize=True)
    print(wyjscie)


if __name__ == "__main__":
    a = argparse.ArgumentParser(description="Zlozenie studia Izabeli")
    a.add_argument("--output", default="/root/rod-ai-studio/data/upload/podglad/STUDIO_IZABELA_v3.png")
    a.add_argument("--imie", default="IZABELA")
    a.add_argument("--podpis", default="wirtualny awatar zarządu")
    args = a.parse_args()
    zloz(args.output, args.imie, args.podpis)
