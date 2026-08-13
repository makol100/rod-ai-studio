#!/usr/bin/env python3
"""Pakiet wznowienia — ratunek kontekstu po zablokowaniu okna czatu.

Decyzja Tomasza 13.08.2026: "stawiamy ratunek kontekstu na Telegramie".
Projekt: narada Zenka i Henia z 13.08 (.scratch/okno_telegram/{zenek,henio}.txt).

CO ROBI: sklada z plikow na dysku jeden plik .txt, ktory nowe okno czatu dostaje
zamiast utraconego kontekstu. Zero wywolan modelu, zero kosztu, zero puli Claude Max.

TWARDE ZASADY (obie z narady):
1. LIMIT 14039 znakow (D-0047). Generator SAM mierzy i SAM skraca ogon teleportu.
   Stary reczny zestaw mial 14250 znakow, czyli juz przekraczal limit o 211.
2. FAIL-CLOSED NA SEKRETY. most.jsonl i SLOWA_TOMASZA.md NIE WCHODZA do pakietu
   (tam moga lezec hasla i loginy — punkt P4.3 Henia; ROZBIEZNOSC: Zenek chcial most
   w pakiecie, Klaudek poszedl za wersja ostrozniejsza, bo blokady okien to dzis
   glowny problem). Gotowy pakiet jest jeszcze raz skanowany filtrem sekretow
   i przy jakimkolwiek trafieniu NIE POWSTAJE.

UZYCIE:
  python3 tools/pakiet_wznowienia.py            # zbuduj i zapisz na dysk
  python3 tools/pakiet_wznowienia.py --wyslij   # zbuduj, zapisz i wyslij na Telegram
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import filtr_sekretow  # noqa: E402

REPO = Path(os.environ.get("HANS_REPO", "/root/rod-ai-studio"))
STREFA = ZoneInfo("Europe/Warsaw")  # D-0053: czas Tomasza wszedzie
LIMIT = 14039  # D-0047
WYJSCIE = REPO / ".scratch" / "pakiet" / "WZNOWIENIE.txt"

BUDZET_BRIEF = 1800
BUDZET_DECYZJE = 1900
BUDZET_STAN = 1400

KONFIGI_HANS = (
    "/home/hermes/.hermes/.env",
    "/home/hermes/.hermes/hermes-agent/.env",
)


def _uruchom(polecenie: list[str], limit: int) -> str:
    try:
        wynik = subprocess.run(
            polecenie, cwd=REPO, capture_output=True, text=True, timeout=90
        )
        tekst = (wynik.stdout or "").strip()
        if not tekst:
            return f"(brak danych; kod wyjscia {wynik.returncode})"
    except (OSError, subprocess.SubprocessError) as blad:
        return f"(nie udalo sie pobrac: {type(blad).__name__})"
    if len(tekst) > limit:
        tekst = tekst[-limit:]
        tekst = tekst[tekst.find("\n") + 1 :]
        tekst = "(...poczatek uciety przez limit...)\n" + tekst
    return tekst


def _brief() -> str:
    sciezka = REPO / "wiedza" / "BRIEF_DLA_KLAUDKA.md"
    try:
        tekst = sciezka.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return "(brak wiedza/BRIEF_DLA_KLAUDKA.md)"
    if len(tekst) > BUDZET_BRIEF:
        tekst = tekst[:BUDZET_BRIEF] + "\n(...ucieto...)"
    return tekst


def _bloki_teleportu() -> list[str]:
    """Teleport pociety na sesje. Zwraca bloki od najstarszego do najnowszego."""
    sciezka = REPO / "TELEPORT_fabryka.md"
    try:
        tekst = sciezka.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    znacznik = "## SESJA "
    pozycje = []
    start = tekst.find(znacznik)
    while start != -1:
        pozycje.append(start)
        start = tekst.find(znacznik, start + 1)
    if not pozycje:
        return [tekst]
    bloki = []
    for i, poz in enumerate(pozycje):
        koniec = pozycje[i + 1] if i + 1 < len(pozycje) else len(tekst)
        blok = tekst[poz:koniec].strip().strip("=").strip()
        if blok:
            bloki.append(blok)
    return bloki


def zbuduj() -> tuple[str, dict]:
    teraz = datetime.now(STREFA)
    brief = _brief()
    decyzje = _uruchom(["python3", "tools/decyzje.py", "--lista"], BUDZET_DECYZJE)
    stan = _uruchom(["python3", "tools/pamiec_stan.py", "pokaz"], BUDZET_STAN)
    sprawdz = _uruchom(["python3", "tools/teleport.py", "--sprawdz"], 300)

    naglowek = (
        f"PAKIET WZNOWIENIA — {teraz:%d.%m.%Y %H:%M} (czas Tomasza, Europe/Warsaw)\n"
        "Zbudowany przez tools/pakiet_wznowienia.py z plikow na dysku VPS.\n"
        "Poprzednie okno czatu zostalo zablokowane. To jest jego kontekst.\n\n"
        "PIERWSZA CZYNNOSC NOWEGO OKNA: nie zaczynaj od zera i nie zgaduj —\n"
        "przeczytaj ten pakiet, potem odpal protokol startu na VPS przez konektor\n"
        "'fabryka' i dopiero potem melduj Tomaszowi, na czym stanelismy.\n\n"
        "CZEGO NIE ROBIC: nie prosic o haslo ani login w oknie czatu; nie drukowac\n"
        "zawartosci /root/.sekrety ani /root/.hilook_cred; nie probowac logowania do\n"
        "HiLook (D-0072). W tym pakiecie NIE MA sekretow — zostal przeskanowany.\n"
    )

    sekcje = [
        ("1. BRIEF OPERACYJNY", brief),
        ("2. ZALEGLOSC DZIENNIKOW", sprawdz),
        ("3. OBOWIAZUJACE DECYZJE TOMASZA", decyzje),
        ("4. STAN: ZROBIONE / W TOKU / BLOKERY", stan),
    ]

    baza = naglowek
    for tytul, tresc in sekcje:
        baza += f"\n{'=' * 70}\n{tytul}\n{'=' * 70}\n{tresc}\n"

    naglowek_teleportu = f"\n{'=' * 70}\n5. PRZEBIEG — OSTATNIE SESJE Z TELEPORTU\n{'=' * 70}\n"
    stopka = f"\n{'=' * 70}\nKONIEC PAKIETU. Pelne zrodla leza na VPS w {REPO}.\n"

    bloki = _bloki_teleportu()
    wybrane: list[str] = []
    for blok in reversed(bloki):
        kandydat = list(reversed([blok] + list(reversed(wybrane))))
        proba = baza + naglowek_teleportu + "\n\n".join(kandydat) + stopka
        if len(proba) > LIMIT:
            break
        wybrane = kandydat

    if not wybrane and bloki:
        # nawet jedna sesja sie nie miesci — bierzemy jej ogon
        zapas = LIMIT - len(baza + naglowek_teleportu + stopka)
        if zapas > 200:
            wybrane = ["(...poczatek sesji uciety...)\n" + bloki[-1][-zapas + 60 :]]

    pakiet = baza + naglowek_teleportu + "\n\n".join(wybrane) + stopka
    pakiet = pakiet.replace("ZNAKI_PLACEHOLDER", "")
    pakiet += f"ZNAKI: {len(pakiet)}/{LIMIT}\n"

    metryka = {
        "znaki": len(pakiet),
        "limit": LIMIT,
        "sesji_teleportu": len(wybrane),
        "sesji_dostepnych": len(bloki),
        "czas": teraz.isoformat(),
    }
    return pakiet, metryka


def _token_hansa() -> tuple[str, str]:
    token = czat = ""
    for sciezka in KONFIGI_HANS:
        try:
            with open(sciezka, encoding="utf-8", errors="replace") as f:
                for linia in f:
                    klucz, _, wartosc = linia.strip().partition("=")
                    wartosc = wartosc.strip().strip('"').strip("'")
                    if klucz == "HANS_BOT_TOKEN" and wartosc and not token:
                        token = wartosc
                    elif klucz == "HANS_CHAT_ID" and wartosc and not czat:
                        czat = wartosc
        except OSError:
            continue
    return token, czat


def wyslij(sciezka: Path, podpis: str) -> tuple[bool, str]:
    """Wysyla pakiet jako PLIK (sendDocument) — nie jako wiadomosc."""
    import requests

    token, czat = _token_hansa()
    if not token or not czat:
        return False, "brak tokenu lub chat_id bota Hansa"
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    try:
        with sciezka.open("rb") as plik:
            odp = requests.post(
                url,
                data={"chat_id": czat, "caption": podpis[:1000]},
                files={"document": ("WZNOWIENIE.txt", plik, "text/plain")},
                timeout=60,
            )
        dane = odp.json()
    except Exception as blad:  # noqa: BLE001
        return False, f"{type(blad).__name__}: {blad}"
    if not dane.get("ok"):
        return False, f"Telegram odmowil: {str(dane)[:200]}"
    return True, "wyslane"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wyslij", action="store_true", help="wyslij pakiet na Telegram")
    parser.add_argument("--cicho", action="store_true", help="nie drukuj pakietu")
    args = parser.parse_args()

    pakiet, metryka = zbuduj()

    problemy = filtr_sekretow.zbadaj(pakiet)
    if problemy:
        print("PAKIET NIE POWSTAL — filtr sekretow zapalil sie (fail-closed):", file=sys.stderr)
        for p in problemy[:20]:
            print("  " + p, file=sys.stderr)
        return 2

    if metryka["znaki"] > LIMIT:
        print(f"PAKIET NIE POWSTAL — {metryka['znaki']} > {LIMIT}", file=sys.stderr)
        return 3

    WYJSCIE.parent.mkdir(parents=True, exist_ok=True)
    tymczasowy = WYJSCIE.with_suffix(".tmp")
    tymczasowy.write_text(pakiet, encoding="utf-8")
    tymczasowy.replace(WYJSCIE)

    podpis = (
        f"PAKIET WZNOWIENIA {metryka['czas'][:16].replace('T', ' ')}\n"
        f"{metryka['znaki']}/{LIMIT} znakow, {metryka['sesji_teleportu']} "
        f"z {metryka['sesji_dostepnych']} sesji teleportu.\n"
        "Wklej ten plik do nowego okna czatu."
    )

    if args.wyslij:
        ok, powod = wyslij(WYJSCIE, podpis)
        metryka["wyslany"] = ok
        metryka["powod_wysylki"] = powod
        if not ok:
            print(f"WYSYLKA NIEUDANA: {powod}", file=sys.stderr)

    print(json.dumps(metryka, ensure_ascii=False))
    if not args.cicho and not args.wyslij:
        print(f"Zapisany: {WYJSCIE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
