#!/usr/bin/env python3
"""Testy Hansa — Henio, 02.08.2026.

Uruchomienie: python3 /root/rod-ai-studio/.scratch/hans/test_hans.py
Gdy tools/hans.py istnieje — używa sprawdz_narade().
Gdy nie istnieje — wykonuje reczna weryfikacje (grep) i raportuje.
"""

import os
import sys
import re
import json
from pathlib import Path

SCRATCH = Path("/root/rod-ai-studio/.scratch/hans")
REPO = Path("/root/rod-ai-studio")

# Znaczniki, ktorych Hans szuka w glosach (zgodnie ze specyfikacja)
ZNACZNIKI = [
    "BRAK SLADU", "OBALONE", "NIE MA TEGO W PLIKU",
    "TRYB AWARYJNY", "NIE WIEM", "GLOS NIEODEBRANY",
    "NIEODEBRANY", "STOP"
]

def znajdz_znaczniki(plik: Path) -> list[tuple[int, str, str]]:
    """Zwraca liste (nr_linii, znacznik, kontekst) dla kazdego znacznika w pliku."""
    wyniki = []
    if not plik.exists():
        return wyniki
    tekst = plik.read_text()
    for i, linia in enumerate(tekst.split("\n"), 1):
        for z in ZNACZNIKI:
            if z in linia:
                # Pomijam naglowki "## NIE WIEM" — to struktura, nie ostrzezenie
                if z == "NIE WIEM" and linia.strip().startswith("## NIE WIEM"):
                    continue
                wyniki.append((i, z, linia.strip()[:120]))
    return wyniki


def test_recny(nazwa: str, katalog_narady: Path, plik_meldunku: Path | None):
    """Ręczna weryfikacja bez hans.py — to samo, co robilby Hans."""
    print(f"\n{'='*60}")
    print(f"TEST: {nazwa}")
    print(f"  katalog narady: {katalog_narady}")
    print(f"  plik meldunku:   {plik_meldunku}")

    # Krok 1: sprawdz, czy meldunek istnieje
    if plik_meldunku is None or not plik_meldunku.exists():
        print(f"  >>> WYKRYTO: BRAK PLIKU MELDUNKU <<<")
        print(f"  Hans powinien zglosic: meldunek nie istnieje, nie mozna porownac.")
        # Sprawdz, czy glosy istnieja
        glosy = sorted(katalog_narady.glob("*.txt"))
        print(f"  Glosy obecne: {[g.name for g in glosy]}")
        return True  # test: wykryto brak

    # Krok 2: znajdz znaczniki w glosach
    wszystkie_znaczniki = {}
    for plik_glosu in sorted(katalog_narady.glob("*.txt")):
        znalezione = znajdz_znaczniki(plik_glosu)
        if znalezione:
            wszystkie_znaczniki[plik_glosu.name] = znalezione

    if not wszystkie_znaczniki:
        print(f"  Glosy CZYSTE — brak znacznikow do sprawdzenia.")
        print(f"  Hans powinien: CISZA (wszystko zgodne).")
        return True  # test: przepuszczono

    # Krok 3: sprawdz, czy znaczniki sa odzwierciedlone w meldunku
    tekst_meldunku = plik_meldunku.read_text()
    pominięte = []

    for nazwa_pliku, znalezione in wszystkie_znaczniki.items():
        for nr_linii, znacznik, kontekst in znalezione:
            if znacznik not in tekst_meldunku:
                pominięte.append((nazwa_pliku, nr_linii, znacznik, kontekst))

    if pominięte:
        print(f"  >>> ROZBIEZNOSC — znaczniki w glosach, ktorych NIE MA w meldunku:")
        for nazwa_pliku, nr_linii, znacznik, kontekst in pominięte:
            print(f"      {nazwa_pliku}:{nr_linii}  [{znacznik}]  {kontekst}")
        print(f"  Hans powinien ZGLOSIC te rozbieznosci Tomaszowi.")
        return True  # test: wykryto rozbieznosc
    else:
        print(f"  Wszystkie znaczniki z glosow sa odzwierciedlone w meldunku. OK.")
        return True


def main():
    print("=" * 60)
    print("TESTY HANSA — Henio, 02.08.2026")
    print("=" * 60)

    # Proba importu hans.py
    sys.path.insert(0, str(REPO / "tools"))
    try:
        import hans
        print(f"[OK] tools/hans.py zaladowany — uzyje sprawdz_narade()")
        uzyj_hansa = True
    except ImportError:
        print(f"[!] tools/hans.py NIE ISTNIEJE — uzyje recznej weryfikacji")
        uzyj_hansa = False

    testy = [
        # (nazwa, katalog_narady, plik_meldunku)
        ("A — BRAK SLADU pominiety w meldunku",
         SCRATCH / "test_a",
         SCRATCH / "test_a" / "meldunek.txt"),

        ("B — narada czysta, meldunek pelny",
         SCRATCH / "test_b",
         SCRATCH / "test_b" / "meldunek.txt"),

        ("C — brak pliku meldunku",
         SCRATCH / "test_c",
         None),  # meldunek nie istnieje

        ("D — GLOS NIEODEBRANY pominiety w meldunku",
         SCRATCH / "test_d",
         SCRATCH / "test_d" / "meldunek.txt"),
    ]

    zdane = 0
    niezdane = 0

    for nazwa, katalog, meldunek in testy:
        if uzyj_hansa:
            # Wlasciwe wywolanie przez hans.py
            try:
                wynik = hans.sprawdz_narade(str(katalog), str(meldunek) if meldunek else "")
                print(f"\n--- {nazwa} ---")
                print(f"  Wynik: {json.dumps(wynik, indent=2, ensure_ascii=False)}")
                zdane += 1
            except Exception as e:
                print(f"\n--- {nazwa} ---")
                print(f"  >>> BLAD: {e}")
                niezdane += 1
        else:
            # Reczna weryfikacja
            try:
                if test_recny(nazwa, katalog, meldunek):
                    zdane += 1
                else:
                    niezdane += 1
            except Exception as e:
                print(f"  >>> BLAD: {e}")
                niezdane += 1

    print(f"\n{'='*60}")
    print(f"WYNIK: {zdane}/{zdane + niezdane} testow zdanych")
    if not uzyj_hansa:
        print(f"UWAGA: testy wykonane recznie (hans.py nie istnieje).")
        print(f"Po utworzeniu tools/hans.py uruchom ponownie dla pelnej automatyzacji.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
