#!/usr/bin/env python3
"""DECYZJE TOMASZA — rejestr z trwałym numerem i polem „zastepuje".

Zbudowane 4.08.2026 na żądanie HENIA, pod kryterium podanym przez Tomasza:
    „Najbardziej cierpię JA, bo ja mam emocje."

PO CO — konkretny koszt, który to ma usunąć:
4.08 Tomasz MUSIAŁ dwa razy powtórzyć to samo rozstrzygnięcie („Klaudek jest zawsze kierownikiem"),
bo w plikach leżały równocześnie trzy sprzeczne zapisy: „Genek kierownik" (2.08),
„Klaudek nie jest nad załogą" (START.md) i nowe rozstrzygnięcie. Henio zapytany o kierownika
odpowiedział zgodnie z zapisem — i wyszedł na zdezorientowanego, choć wina była Klaudka.

Rejestr rozwiązuje to jednym polem: `zastepuje`. Stara decyzja ZOSTAJE (dekret 2.08: nikt niczego
nie usuwa), ale jest jawnie oznaczona jako zastąpiona — więc nikt jej nie odczyta jako obowiązującej.

Użycie:
  python3 tools/decyzje.py --dodaj "Klaudek jest zawsze kierownikiem" --zastepuje D-0006
  python3 tools/decyzje.py --lista              # tylko obowiązujące
  python3 tools/decyzje.py --lista --wszystkie  # z zastąpionymi
  python3 tools/decyzje.py --sprzecznosci       # decyzje o tym samym temacie bez „zastepuje"
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

REPO = "/root/rod-ai-studio"
REJESTR = os.path.join(REPO, ".scratch", "decyzje_tomasza.jsonl")


def wczytaj() -> list:
    if not os.path.isfile(REJESTR):
        return []
    wpisy = []
    with open(REJESTR, encoding="utf-8") as f:
        for linia in f:
            linia = linia.strip()
            if linia:
                try:
                    wpisy.append(json.loads(linia))
                except json.JSONDecodeError:
                    continue
    return wpisy


def dodaj(tresc: str, zastepuje: str, temat: str) -> dict:
    """Dopisuje decyzję. NIGDY nie nadpisuje ani nie usuwa (dekret Tomasza 2.08)."""
    wpisy = wczytaj()
    numer = f"D-{len(wpisy) + 1:04d}"
    wpis = {
        "id": numer,
        "czas_tomasza": datetime.now(ZoneInfo("Europe/Vienna")).strftime("%Y-%m-%d %H:%M:%S %Z"),
        "czas_utc": datetime.now(timezone.utc).isoformat(),
        "tresc": tresc,
        "temat": temat,
        "zastepuje": zastepuje,
        "zastapiona_przez": "",
    }
    os.makedirs(os.path.dirname(REJESTR), exist_ok=True)
    with open(REJESTR, "a", encoding="utf-8") as f:
        f.write(json.dumps(wpis, ensure_ascii=False) + "\n")

    # oznaczenie starej decyzji: zapisujemy NOWY wiersz-adnotację, nie ruszamy poprzedniego
    if zastepuje:
        adnotacja = {
            "id": f"{numer}-ADN",
            "czas_tomasza": wpis["czas_tomasza"],
            "typ": "adnotacja",
            "dotyczy": zastepuje,
            "tresc": f"WYGASŁO — zastąpione przez {numer}",
            "temat": temat,
            "zastepuje": "",
            "zastapiona_przez": numer,
        }
        with open(REJESTR, "a", encoding="utf-8") as f:
            f.write(json.dumps(adnotacja, ensure_ascii=False) + "\n")
    return wpis


def obowiazujace(wpisy: list) -> list:
    """Decyzja jest zastąpiona, jeśli istnieje adnotacja wskazująca na jej numer."""
    wygasle = {w.get("dotyczy") for w in wpisy if w.get("typ") == "adnotacja"}
    return [w for w in wpisy if w.get("typ") != "adnotacja" and w["id"] not in wygasle]


def sprzecznosci(wpisy: list) -> list:
    """Dwie OBOWIĄZUJĄCE decyzje o tym samym temacie = podejrzenie sprzeczności.

    To jest sygnał dla Klaudka: albo jedna z nich powinna mieć „zastepuje", albo temat
    jest źle przypisany. Nie rozstrzyga — zgłasza, bo rozstrzyga wyłącznie Tomasz.
    """
    wg_tematu = {}
    for w in obowiazujace(wpisy):
        wg_tematu.setdefault(w.get("temat", "(bez tematu)"), []).append(w)
    return [(t, lista) for t, lista in wg_tematu.items() if len(lista) > 1 and t != "(bez tematu)"]


def main() -> int:
    p = argparse.ArgumentParser(description="Rejestr decyzji Tomasza")
    p.add_argument("--dodaj", default="", help="dosłowna treść decyzji")
    p.add_argument("--temat", default="", help="czego dotyczy, np. 'kierownik', 'produkcja'")
    p.add_argument("--zastepuje", default="", help="numer decyzji, którą ta zastępuje, np. D-0006")
    p.add_argument("--lista", action="store_true", help="wypisz decyzje")
    p.add_argument("--wszystkie", action="store_true", help="także zastąpione")
    p.add_argument("--sprzecznosci", action="store_true", help="pokaż podejrzenia sprzeczności")
    a = p.parse_args()

    if a.dodaj:
        w = dodaj(a.dodaj, a.zastepuje, a.temat)
        print(f"[decyzje] {w['id']} zapisana ({w['czas_tomasza']})"
              + (f", zastępuje {a.zastepuje}" if a.zastepuje else ""))
        return 0

    wpisy = wczytaj()
    if a.sprzecznosci:
        s = sprzecznosci(wpisy)
        if not s:
            print("[decyzje] brak podejrzeń sprzeczności")
        for temat, lista in s:
            print(f"  PODEJRZENIE — temat '{temat}': {len(lista)} obowiązujących decyzji")
            for w in lista:
                print(f"     {w['id']} ({w['czas_tomasza']}): {w['tresc'][:90]}")
        return 0

    do_pokazania = wpisy if a.wszystkie else obowiazujace(wpisy)
    if not do_pokazania:
        print("[decyzje] rejestr pusty")
    for w in do_pokazania:
        znacznik = "  " if w.get("typ") != "adnotacja" else "~ "
        print(f"{znacznik}{w['id']} [{w.get('temat', '-')}] {w['czas_tomasza']}: {w['tresc'][:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
