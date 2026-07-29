#!/usr/bin/env python3
"""szukaj.py — natychmiastowe odnalezienie wszystkiego, co fabryka wie o danym slowie.

Uzycie:
    python3 tools/szukaj.py podest
    python3 tools/szukaj.py "bramka oka" krystyna
    python3 tools/szukaj.py --pelne krystyna     # wypisuje cale trafione pliki

Przeszukuje: wiedza/, docs/, AGENTS.md, README, podrecznik dyzurnego, konfiguracje skilli.
Ignoruje wielkosc liter i polskie znaki (kosiarka == KOSIARKA == kosiarką).
Zwraca: plik, numer linii, trafiona linia — czyli SLAD, nie streszczenie.
"""
import argparse
import os
import sys
import unicodedata

KATALOGI = [
    "/root/rod-ai-studio/wiedza",
    "/root/rod-ai-studio/docs",
    "/root/.claude/skills",
]
PLIKI = [
    "/root/rod-ai-studio/AGENTS.md",
    "/root/rod-ai-studio/TELEPORT_fabryka.md",
    "/root/TELEPORT_HA.md",
    "/root/.claude/CLAUDE.md",
    "/root/rod-ai-studio/README.md",
    "/home/hermes/PODRECZNIK_DYZURNEGO.md",
]
ROZSZERZENIA = (".md", ".txt", ".json", ".yaml", ".yml")
MAX_LINIA = 200


def bez_ogonkow(s: str) -> str:
    s = s.replace("ł", "l").replace("Ł", "L")
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()


def zbierz_pliki() -> list:
    out = []
    for k in KATALOGI:
        for root, _, nazwy in os.walk(k):
            for n in nazwy:
                if n.endswith(ROZSZERZENIA):
                    out.append(os.path.join(root, n))
    out += [p for p in PLIKI if os.path.isfile(p)]
    return sorted(set(out))


def szukaj(slowa: list, pelne: bool) -> int:
    igly = [bez_ogonkow(s) for s in slowa]
    pliki = zbierz_pliki()
    trafienia = {}
    for sciezka in pliki:
        try:
            with open(sciezka, encoding="utf-8", errors="replace") as f:
                linie = f.readlines()
        except OSError:
            continue
        for nr, linia in enumerate(linie, 1):
            plaska = bez_ogonkow(linia)
            if any(i in plaska for i in igly):
                trafienia.setdefault(sciezka, []).append((nr, linia.strip()))

    if not trafienia:
        print(f"BRAK TRAFIEN dla: {', '.join(slowa)}")
        print(f"Przeszukano {len(pliki)} plikow. To znaczy: fabryka NIE MA o tym zapisu.")
        return 1

    laczne = sum(len(v) for v in trafienia.values())
    print(f"SZUKANE: {', '.join(slowa)}")
    print(f"TRAFIENIA: {laczne} w {len(trafienia)} plikach (przeszukano {len(pliki)})\n")
    for sciezka, wiersze in sorted(trafienia.items(), key=lambda x: -len(x[1])):
        print(f"### {sciezka}  ({len(wiersze)} trafien)")
        if pelne:
            with open(sciezka, encoding="utf-8", errors="replace") as f:
                print(f.read())
            continue
        for nr, tekst in wiersze[:6]:
            print(f"   {nr:>5}: {tekst[:MAX_LINIA]}")
        if len(wiersze) > 6:
            print(f"   ... jeszcze {len(wiersze) - 6} trafien w tym pliku")
        print()
    if not pelne:
        print("Pelna tresc najbogatszego pliku: dodaj --pelne")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("slowa", nargs="+")
    p.add_argument("--pelne", action="store_true")
    a = p.parse_args()
    return szukaj(a.slowa, a.pelne)


if __name__ == "__main__":
    sys.exit(main())
