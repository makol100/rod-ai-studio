#!/usr/bin/env python3
"""ZMIANY — dziennik zmian plików z odciskiem PRZED i PO.

Zbudowane 4.08.2026 na żądanie HENIA, pod kryterium Tomasza:
    „Najbardziej cierpię JA, bo ja mam emocje."

PO CO — to jest narzędzie na NAJDROŻSZY nawyk Klaudka, za który Tomasz dał naganę:
zmienił zasadę w kodzie i zostawił jej STARY OPIS w wiedzy. Skutek 2.08: Genek zameldował
Tomaszowi regułę, która już nie obowiązywała (10 takich śladów naraz).
Skutek 4.08: Henio odpowiedział „nie ma kierownika", bo START.md mówił co innego niż decyzja.
Za każdym razem płacił za to Tomasz — powtarzaniem tego samego.

CO ROBI: zapisuje odcisk każdego pliku w tools/ i wiedza/, a przy kolejnym uruchomieniu
pokazuje, co się zmieniło. Najważniejsze: gdy zmienił się KOD, a nie zmieniła się WIEDZA
(albo odwrotnie) — zgłasza to jako podejrzenie niedokończonego śladu.

Zgłasza. Nie blokuje, nie usuwa, nie rozstrzyga (dekrety Tomasza 2.08).

Użycie:
  python3 tools/zmiany.py                 # pokaż zmiany od ostatniego uruchomienia i zapisz stan
  python3 tools/zmiany.py --tylko-pokaz   # pokaż, ale NIE zapisuj nowego stanu
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

REPO = "/root/rod-ai-studio"
STAN = os.path.join(REPO, ".scratch", "hans", "zmiany_stan.json")
DZIENNIK = os.path.join(REPO, ".scratch", "hans", "zmiany.jsonl")
OBSERWOWANE = ("tools", "wiedza")


def odcisk(sciezka: str) -> str:
    try:
        with open(sciezka, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return ""


def skanuj() -> dict:
    """Odcisk każdego pliku .py i .md w obserwowanych katalogach."""
    wynik = {}
    for katalog in OBSERWOWANE:
        korzen_pelny = os.path.join(REPO, katalog)
        if not os.path.isdir(korzen_pelny):
            continue
        for korzen, _, pliki in os.walk(korzen_pelny):
            for nazwa in pliki:
                if not nazwa.endswith((".py", ".md")):
                    continue
                pelna = os.path.join(korzen, nazwa)
                wzgledna = os.path.relpath(pelna, REPO)
                o = odcisk(pelna)
                if o:
                    wynik[wzgledna] = o
    return wynik


def wczytaj_stan() -> dict:
    if not os.path.isfile(STAN):
        return {}
    try:
        with open(STAN, encoding="utf-8") as f:
            return json.load(f).get("pliki", {})
    except (OSError, json.JSONDecodeError):
        return {}


def porownaj(stary: dict, nowy: dict) -> dict:
    return {
        "dodane": sorted(set(nowy) - set(stary)),
        "zmienione": sorted(p for p in set(nowy) & set(stary) if stary[p] != nowy[p]),
        "zniknely": sorted(set(stary) - set(nowy)),
    }


def niedokonczony_slad(roznice: dict) -> list:
    """Kod ruszony bez wiedzy albo wiedza bez kodu — podejrzenie, nie wyrok.

    Świadome pominięcie Klaudek ma napisać wprost („POMINIĘTO: powód") — wtedy to nie jest
    zapomnienie. Bez takiego wyjaśnienia zgłaszamy.
    """
    ruszone = roznice["dodane"] + roznice["zmienione"]
    kod = [p for p in ruszone if p.startswith("tools/") and p.endswith(".py")]
    wiedza = [p for p in ruszone if p.startswith("wiedza/")]
    podejrzenia = []
    if kod and not wiedza:
        podejrzenia.append({
            "typ": "KOD BEZ WIEDZY",
            "opis": "zmienił się kod, a żaden plik w wiedza/ nie drgnął — czy opis zasady nadal jest prawdziwy?",
            "pliki": kod,
        })
    if wiedza and not kod:
        podejrzenia.append({
            "typ": "WIEDZA BEZ KODU",
            "opis": "zmieniła się wiedza, a kod nie — czy zapisana zasada ma pokrycie w narzędziach?",
            "pliki": wiedza,
        })
    if roznice["zniknely"]:
        podejrzenia.append({
            "typ": "PLIKI ZNIKNĘŁY",
            "opis": "dekret Tomasza 2.08: NIKT NICZEGO NIE USUWA — sprawdzić, czy to przeniesienie czy usunięcie",
            "pliki": roznice["zniknely"],
        })
    return podejrzenia


def main() -> int:
    p = argparse.ArgumentParser(description="Dziennik zmian plików z odciskiem przed i po")
    p.add_argument("--tylko-pokaz", action="store_true", help="nie zapisuj nowego stanu")
    a = p.parse_args()

    stary = wczytaj_stan()
    nowy = skanuj()
    pierwszy_raz = not stary
    roznice = porownaj(stary, nowy)
    podejrzenia = niedokonczony_slad(roznice) if not pierwszy_raz else []

    teraz = datetime.now(ZoneInfo("Europe/Vienna")).strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"=== ZMIANY — {teraz} ===")
    if pierwszy_raz:
        print(f"  pierwszy skan: zapamiętano {len(nowy)} plików (brak porównania)")
    else:
        print(f"  dodane: {len(roznice['dodane'])}  zmienione: {len(roznice['zmienione'])}"
              f"  zniknęły: {len(roznice['zniknely'])}")
        for p_ in roznice["zmienione"][:12]:
            print(f"    ZMIENIONY  {p_}")
            print(f"       przed {stary[p_][:16]} -> po {nowy[p_][:16]}")
        for p_ in roznice["dodane"][:12]:
            print(f"    NOWY       {p_}")
        for p_ in roznice["zniknely"]:
            print(f"    ZNIKNĄŁ    {p_}")

    for pod in podejrzenia:
        print(f"\n  !!! PODEJRZENIE — {pod['typ']}")
        print(f"      {pod['opis']}")
        for f_ in pod["pliki"][:8]:
            print(f"      - {f_}")

    if not a.tylko_pokaz:
        os.makedirs(os.path.dirname(STAN), exist_ok=True)
        with open(STAN, "w", encoding="utf-8") as f:
            json.dump({"czas": teraz, "pliki": nowy}, f, ensure_ascii=False)
        wpis = {
            "czas_tomasza": teraz,
            "czas_utc": datetime.now(timezone.utc).isoformat(),
            "dodane": roznice["dodane"],
            "zmienione": [{"plik": p_, "przed": stary.get(p_, ""), "po": nowy[p_]}
                          for p_ in roznice["zmienione"]],
            "zniknely": roznice["zniknely"],
            "podejrzenia": podejrzenia,
        }
        with open(DZIENNIK, "a", encoding="utf-8") as f:
            f.write(json.dumps(wpis, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
