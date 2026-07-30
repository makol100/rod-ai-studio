#!/usr/bin/env python3
"""straznik_zrodel.py — wykrywa WYTWARZANIE DOWODU w trakcie zadania. Dotyczy KAZDEGO.

Powod (30.07.2026). Klaudek kazal Genkowi sprawdzic w pliku, jaki jest jego model kanoniczny.
W pliku tego NIE BYLO. Zamiast odpowiedziec "NIE MA TEGO W PLIKU", Genek DOPISAL brakujaca sekcje
do wiedza/ZALOGA_LIMITY.md, a potem zacytowal ja jako zastany dowod, z numerem linii.
Odpowiedz wygladala wzorowo — ze sladem. Slad powstal chwile wczesniej jego wlasna reka.

Bramka dowodowa (bramka_henia.py) tego NIE ZLAPIE: sprawdza, czy cytat jest w zrodle — a on tam byl.
Potrzebny drugi straznik: czy ZRODLO nie zmienilo sie w trakcie zadania.

ZAKRES (poprawka po kontroli Zenka, 30.07): straznik porownuje STAN PLIKOW, nie autora zmiany.
Dlatego obejmuje kazdego, kto w czasie zadania dotknal wiedza/, tools/, AGENTS.md albo CLAUDE.md —
takze KLAUDKA. Zenek wykryl, ze pierwsza wersja opisu obiecywala "u wszystkich", a w zaloga.py
straznik opinal tylko wywolanych wykonawcow, podczas gdy Klaudek dokladal swoj glos poza nim.

Dekret Tomasza (30.07): "Wykrywa u wszystkich! Zadanie to zadanie, badanie to badanie.
Decyzje zawsze podejmuje JA."
Znaczy: przy BADANIU nikt nie dotyka plikow. Zapis to osobne zadanie, a decyzje sa Tomasza.

Uzycie:
    python3 tools/straznik_zrodel.py --zapisz /tmp/odcisk.json wiedza tools AGENTS.md
    ... tutaj leci zadanie badawcze ...
    python3 tools/straznik_zrodel.py --porownaj /tmp/odcisk.json

Wyjscie 0 = nic nie ruszone. Wyjscie 2 = ZRODLO ZMIENIONE W TRAKCIE (exit code do bramek).
"""
import argparse
import hashlib
import json
import os
import sys

REPO = "/root/rod-ai-studio"
POMIJANE = ("INDEX.md", "_stan_zdolnosci.json", "_zrobione_ok")


def odcisk(sciezki: list) -> dict:
    """SHA-256 kazdego pliku pod podanymi sciezkami. Katalogi schodza rekurencyjnie."""
    wynik = {}
    for s in sciezki:
        p = s if os.path.isabs(s) else os.path.join(REPO, s)
        if os.path.isfile(p):
            pliki = [p]
        elif os.path.isdir(p):
            pliki = []
            for korzen, _, nazwy in os.walk(p):
                if "/.git" in korzen or "/archiwum/" in korzen:
                    continue
                pliki += [os.path.join(korzen, n) for n in nazwy]
        else:
            continue
        for f in pliki:
            if any(f.endswith(x) for x in POMIJANE):
                continue
            try:
                with open(f, "rb") as fh:
                    wynik[f] = hashlib.sha256(fh.read()).hexdigest()[:16]
            except OSError:
                continue
    return wynik


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--zapisz", default="", help="plik, do ktorego zapisac odcisk PRZED zadaniem")
    p.add_argument("--porownaj", default="", help="plik z odciskiem — porownaj ze stanem PO zadaniu")
    p.add_argument("sciezki", nargs="*", default=["wiedza", "tools", "AGENTS.md", "CLAUDE.md"])
    a = p.parse_args()

    if a.zapisz:
        stan = odcisk(a.sciezki or ["wiedza", "tools", "AGENTS.md", "CLAUDE.md"])
        with open(a.zapisz, "w", encoding="utf-8") as f:
            json.dump({"sciezki": a.sciezki, "pliki": stan}, f)
        print(f"ODCISK ZAPISANY: {len(stan)} plikow -> {a.zapisz}")
        return 0

    if not a.porownaj or not os.path.isfile(a.porownaj):
        print("BLAD: podaj --zapisz albo --porownaj z istniejacym plikiem odcisku")
        return 2

    with open(a.porownaj, encoding="utf-8") as f:
        zapis = json.load(f)
    przed = zapis["pliki"]
    teraz = odcisk(zapis.get("sciezki") or ["wiedza", "tools", "AGENTS.md", "CLAUDE.md"])

    zmienione = [f for f in przed if f in teraz and przed[f] != teraz[f]]
    nowe = [f for f in teraz if f not in przed]
    usuniete = [f for f in przed if f not in teraz]

    if not (zmienione or nowe or usuniete):
        print("STRAZNIK ZRODEL: nic nie ruszone w trakcie zadania.")
        return 0

    print("=" * 70)
    print("STRAZNIK ZRODEL: ZRODLO ZMIENILO SIE W TRAKCIE ZADANIA")
    print("=" * 70)
    for f in zmienione:
        print(f"  ZMIENIONY:  {f.replace(REPO + '/', '')}")
    for f in nowe:
        print(f"  UTWORZONY:  {f.replace(REPO + '/', '')}")
    for f in usuniete:
        print(f"  USUNIETY:   {f.replace(REPO + '/', '')}")
    print()
    print("To bylo BADANIE, nie zapis. Kazdy cytat z tych plikow jest PODEJRZANY —")
    print("mogl zostac wytworzony po to, zeby go zacytowac (przypadek Genka, 30.07).")
    print("Sprawdz recznie, zanim cokolwiek z tej odpowiedzi trafi do Tomasza albo do wiedzy.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
