#!/usr/bin/env python3
"""Filtr sekretow — FAIL-CLOSED. Warunek Zenka z narady 13.08 (.scratch/okno_telegram/zenek.txt P4.5).

Zasada: NIGDY nie maskujemy czesciowo i NIGDY nie drukujemy podejrzanej wartosci.
Gdy cokolwiek pachnie sekretem — caly rekord jest ODRZUCANY, a komunikat mowi TYLKO
ktora regula sie zapalila i w ktorej linii. Wartosc nie trafia ani do logu, ani do czatu,
ani do meldunku.

Dwa zrodla wiedzy o sekretach:
1. WARTOSCI ZNANE  — realne sekrety z plikow /root/.sekrety i /root/.hilook_cred.
   Plik jest czytany do porownania, ale jego tresc NIGDY nie jest nigdzie wypisywana.
2. WZORCE  — ksztalt przypisania hasla/tokenu, naglowek Authorization, URL z
   poswiadczeniami, dlugi ciag hex/base64.

Uwaga na falszywe alarmy: samo SLOWO "haslo" w zdaniu ("haslo MQTT lezy jawnym tekstem")
NIE jest sekretem. Zapala sie dopiero PRZYPISANIE wartosci (haslo: cosik123).
"""

from __future__ import annotations

import os
import re
from pathlib import Path

PLIKI_SEKRETOW = ("/root/.sekrety", "/root/.hilook_cred")

# Wartosci, ktore wygladaja jak sekret, ale sa zaslepka — nie zapalaja alarmu.
ZASLEPKI = {
    "xxxxxx", "xxxxxxxx", "changeme", "placeholder", "twojehaslo", "podaj",
    "redacted", "ukryte", "sekret", "secret", "password", "haslo", "none", "null",
}

WZORCE = (
    (
        "przypisanie hasla/tokenu (klucz = wartosc)",
        re.compile(
            r"(?i)\b(has[lł]o|password|passwd|pwd|token|api[_-]?key|apikey|secret|"
            r"klucz|credential|bot[_-]?token)\b\s*[:=]\s*[\"']?([^\s\"',;]{6,})"
        ),
        2,
    ),
    (
        "naglowek Authorization",
        re.compile(r"(?i)\bauthorization\s*:\s*(?:bearer|basic|token)?\s*(\S{8,})"),
        1,
    ),
    (
        "URL z poswiadczeniami (schemat://uzytkownik:haslo@host)",
        re.compile(r"[a-zA-Z][a-zA-Z0-9+.-]*://[^/\s:@]+:[^/\s@]{3,}@"),
        0,
    ),
    (
        "dlugi ciag hex (>=32 znaki) — wyglada jak klucz",
        re.compile(r"\b[0-9a-fA-F]{32,}\b"),
        0,
    ),
    (
        "token bota Telegrama (cyfry:ciag)",
        re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b"),
        0,
    ),
    (
        "klucz prywatny",
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        0,
    ),
)


def _wartosci_znane() -> list[str]:
    """Realne sekrety z plikow. Zwraca wartosci do POROWNANIA — nigdzie ich nie drukujemy."""
    wartosci: list[str] = []
    zrodla: list[Path] = []
    for sciezka in PLIKI_SEKRETOW:
        p = Path(sciezka)
        if p.is_dir():
            # 13.08: /root/.sekrety okazalo sie KATALOGIEM — read_text rzucalo IsADirectoryError,
            # ktore ginelo w "except OSError". Filtr milczal, choc mial porownywac.
            zrodla.extend(sorted(x for x in p.iterdir() if x.is_file()))
        else:
            zrodla.append(p)
    for sciezka in zrodla:
        try:
            tekst = Path(sciezka).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for linia in tekst.splitlines():
            linia = linia.strip()
            if not linia or linia.startswith("#"):
                continue
            _, znak, po = linia.partition("=")
            kandydat = (po if znak else linia).strip().strip('"').strip("'")
            if len(kandydat) >= 6 and kandydat.lower() not in ZASLEPKI:
                wartosci.append(kandydat)
    return wartosci


def _jest_zaslepka(wartosc: str) -> bool:
    czysta = wartosc.strip().strip('"').strip("'")
    if czysta.lower() in ZASLEPKI:
        return True
    if czysta.startswith("[") and czysta.endswith("]"):
        return True
    # 13.08: falszywy alarm na naszym wlasnym opisie w teleporcie ("haslo: <wartosc>").
    # Nawias trojkatny to konwencja zaslepki w dokumentacji, nie sekret.
    if czysta.startswith("<") and czysta.endswith(">"):
        return True
    if set(czysta) <= {"*", "x", "X", ".", "-", "_"}:
        return True
    return False


def zbadaj(tekst: str) -> list[str]:
    """Zwraca liste POWODOW odrzucenia. Pusta lista = czysto.

    Powod ma postac 'linia N: <nazwa reguly>'. NIGDY nie zawiera podejrzanej wartosci.
    """
    powody: list[str] = []
    linie = tekst.splitlines()

    znane = _wartosci_znane()
    for nr, linia in enumerate(linie, 1):
        for wartosc in znane:
            if wartosc in linia:
                powody.append(f"linia {nr}: dokladna wartosc z pliku sekretow")
                break

    for nazwa, wzorzec, grupa in WZORCE:
        for dopasowanie in wzorzec.finditer(tekst):
            trafiona = dopasowanie.group(grupa) if grupa else dopasowanie.group(0)
            if grupa and _jest_zaslepka(trafiona):
                continue
            nr = tekst.count("\n", 0, dopasowanie.start()) + 1
            powody.append(f"linia {nr}: {nazwa}")

    # deduplikacja z zachowaniem kolejnosci
    widziane = set()
    wynik = []
    for p in powody:
        if p not in widziane:
            widziane.add(p)
            wynik.append(p)
    return wynik


def czysto(tekst: str) -> bool:
    return not zbadaj(tekst)


if __name__ == "__main__":
    import sys

    dane = sys.stdin.read() if len(sys.argv) < 2 else Path(sys.argv[1]).read_text(
        encoding="utf-8", errors="replace"
    )
    problemy = zbadaj(dane)
    if problemy:
        print("ODRZUCONE — filtr sekretow zapalil sie:")
        for p in problemy:
            print("  " + p)
        raise SystemExit(1)
    print("CZYSTO — filtr sekretow nie znalazl nic podejrzanego.")
