#!/usr/bin/env python3
"""MELDUNEK — zapis tego, co Klaudek wysyła Tomaszowi, ZANIM to wyśle.

Zbudowane 4.08.2026 na żądanie HENIA (dekret Tomasza: „Heniek ma do tego prawo
i pętla się zamyka").

PO CO: Hans porównuje głosy załogi z meldunkiem Klaudka — ale meldunek idzie oknem rozmowy,
nie przez dysk, więc Hans go nie widzi. Bez tego pliku cała kontrola jest ślepa na jedną stronę.
Henio ujął koszt tak: „kiedy Klaudek pomija decyzję, głos albo własny błąd, moja praca zmienia się
z KONTROLI w REKONSTRUKCJĘ HISTORII".

UCZCIWE OGRANICZENIE: nic nie zmusza Klaudka, żeby to wywołał. Jeśli nie wywoła — Hans zgłosi BRAK
MELDUNKU, co samo w sobie jest naruszeniem i idzie do jego teczki. To jest kontrola po fakcie,
nie blokada. Udawanie, że da się to wymusić technicznie, byłoby pozorną kontrolą.

Użycie:
  python3 tools/meldunek.py --zadanie /tmp/hansh "treść meldunku..."
  python3 tools/meldunek.py --zadanie /tmp/hansh --plik /tmp/tekst.txt
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

REPO = "/root/rod-ai-studio"
DZIENNIK = os.path.join(REPO, ".scratch", "hans", "meldunki.jsonl")


def zapisz(tresc: str, katalog_zadania: str) -> dict:
    """Zapisuje meldunek w katalogu zadania i dopisuje do dziennika. Nigdy nie nadpisuje."""
    teraz_utc = datetime.now(timezone.utc)
    teraz_tomasz = datetime.now(ZoneInfo("Europe/Vienna"))

    sciezki = []
    if katalog_zadania:
        os.makedirs(katalog_zadania, exist_ok=True)
        cel = os.path.join(katalog_zadania, "meldunek.txt")
        # dekret 2.08: nikt niczego nie usuwa — kolejny meldunek dostaje numer, nie nadpisuje
        n = 1
        while os.path.exists(cel):
            n += 1
            cel = os.path.join(katalog_zadania, f"meldunek_{n}.txt")
        with open(cel, "w", encoding="utf-8") as f:
            f.write(tresc)
        sciezki.append(cel)

    os.makedirs(os.path.dirname(DZIENNIK), exist_ok=True)
    wpis = {
        "czas_utc": teraz_utc.isoformat(),
        "czas_tomasza": teraz_tomasz.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "zadanie": katalog_zadania or "(bez zadania)",
        "znakow": len(tresc),
        "plik": sciezki[0] if sciezki else "",
        "tresc": tresc,
    }
    with open(DZIENNIK, "a", encoding="utf-8") as f:
        f.write(json.dumps(wpis, ensure_ascii=False) + "\n")
    return wpis


def main() -> int:
    p = argparse.ArgumentParser(description="Zapis meldunku Klaudka do Tomasza")
    p.add_argument("tresc", nargs="?", default="", help="treść meldunku")
    p.add_argument("--plik", default="", help="wczytaj treść z pliku zamiast argumentu")
    p.add_argument("--zadanie", default="", help="katalog zadania, np. /tmp/hansh")
    a = p.parse_args()

    tresc = a.tresc
    if a.plik:
        try:
            with open(a.plik, encoding="utf-8", errors="replace") as f:
                tresc = f.read()
        except OSError as e:
            print(f"[meldunek] nie moge wczytac {a.plik}: {e}")
            return 1
    if not tresc.strip():
        print("[meldunek] pusta tresc — nic nie zapisano")
        return 1

    w = zapisz(tresc, a.zadanie)
    print(f"[meldunek] zapisany: {w['plik'] or DZIENNIK} ({w['znakow']} znakow, {w['czas_tomasza']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
