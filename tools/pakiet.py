#!/usr/bin/env python3
"""PAKIET DOWODOWY — zbiera w jednym miejscu to, co Klaudek MUSI sprawdzić,
zanim cokolwiek zamelduje Tomaszowi.

Wdrożone 2 sierpnia 2026 na polecenie Tomasza („Wdrażanie"), wg rozpisu załogi:
Genek (kierownik), Zenek, Henio — wszyscy trzej niezależnie wskazali TĘ SAMĄ zasadę:
    „Nic nie idzie do Tomasza bez potwierdzenia wywołaniem narzędzia W TEJ SAMEJ TURZE."

Powód powstania (5 wpadek z 2.08):
  1. nie sprawdził godziny ani razu — pisał daty z pamięci, mylił dzień
  2. patrzył na numer błędu (429), nie na treść („prepayment credits are depleted")
  3. nie sprawdził salda Genka ani razu
  4. odpalił zlecenie i przez 2 godziny nie sprawdził, czy ruszyło (katalog wyszedł pusty)
  5. wpisał do kanonu model, który zwraca 404 — nie sprawdziwszy, czy istnieje

UCZCIWE OGRANICZENIE: ten skrypt NICZEGO NIE BLOKUJE. Meldunek Klaudka idzie oknem rozmowy,
nie przez dysk — żaden program tego nie zatrzyma. To jest ZBIERACZ DOWODÓW, nie bramka.
Pozorna kontrola byłaby gorsza niż jej brak.

Użycie:
  python3 tools/pakiet.py                    — pełny pakiet
  python3 tools/pakiet.py --zadanie /tmp/x   — dodatkowo sprawdza, czy zlecenie dało wynik
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

REPO = "/root/rod-ai-studio"


def czas_tomasza() -> str:
    """Czas TOMASZA, nie serwera. Nigdy z pamięci — to wpadka nr 1 z 2.08."""
    t = datetime.now(ZoneInfo("Europe/Vienna"))
    dni = ("poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela")
    return f"{dni[t.weekday()]}, {t.strftime('%d.%m.%Y, %H:%M')}"


def saldo_fal() -> str:
    try:
        klucz = subprocess.run(["docker", "exec", "fabryka-api", "printenv", "FAL_KEY"],
                               capture_output=True, text=True, timeout=20).stdout.strip()
        if not klucz:
            return "NIE WIEM (brak klucza)"
        r = urllib.request.Request("https://rest.alpha.fal.ai/billing/user_balance",
                                   headers={"Authorization": f"Key {klucz}"})
        with urllib.request.urlopen(r, timeout=20) as o:
            return f"{float(o.read().decode()):.2f} USD"
    except Exception as e:  # noqa: BLE001
        return f"NIE WIEM ({type(e).__name__})"


def stan_genka() -> str:
    """Sprawdza KOD i TREŚĆ — wpadka nr 2 z 2.08: patrzył na numer, nie na komunikat."""
    try:
        klucz = ""
        with open("/root/.gemini/.env", encoding="utf-8") as f:
            for l in f:
                if l.startswith("GEMINI_API_KEY"):
                    klucz = l.split("=", 1)[1].strip()
        if not klucz:
            return "NIE WIEM (brak klucza)"
        adres = ("https://generativelanguage.googleapis.com/v1beta/models/"
                 f"gemini-3.1-pro-preview:generateContent?key={klucz}")
        dane = json.dumps({"contents": [{"parts": [{"text": "OK"}]}]}).encode()
        r = urllib.request.Request(adres, data=dane, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(r, timeout=25) as o:
                o.read(1)
            return "200 — działa"
        except urllib.error.HTTPError as e:
            tresc = json.loads(e.read().decode()).get("error", {}).get("message", "")[:160]
            return f"{e.code} — {tresc}"
    except Exception as e:  # noqa: BLE001
        return f"NIE WIEM ({type(e).__name__})"


def czy_zlecenie_dalo_wynik(katalog: str) -> str:
    """Wpadka nr 4 z 2.08: odpalił i nie sprawdził przez 2 godziny. Katalog był pusty."""
    if not os.path.isdir(katalog):
        return f"KATALOG NIE ISTNIEJE: {katalog}"
    pliki = [f for f in os.listdir(katalog) if f.endswith(".txt")]
    if not pliki:
        return f"PUSTY — zlecenie NIE dało wyniku ({katalog})"
    opis = []
    for f in sorted(pliki):
        p = os.path.join(katalog, f)
        opis.append(f"{f} ({os.path.getsize(p)} B)")
    return "; ".join(opis)


def main() -> int:
    p = argparse.ArgumentParser(description="Pakiet dowodowy przed meldunkiem do Tomasza")
    p.add_argument("--zadanie", default="", help="katalog zlecenia do sprawdzenia")
    a = p.parse_args()

    print("=" * 62)
    print("PAKIET DOWODOWY — sprawdzone TERAZ, nie z pamięci")
    print("=" * 62)
    print(f"  CZAS TOMASZA:     {czas_tomasza()}")
    print(f"  SALDO fal.ai:     {saldo_fal()}")
    print(f"  GENEK:            {stan_genka()}")
    if a.zadanie:
        print(f"  ZLECENIE:         {czy_zlecenie_dalo_wynik(a.zadanie)}")
    print("-" * 62)
    print("  Czego tu NIE MA — sprawdź osobno, zanim o tym napiszesz:")
    print("   • czy plik/model, o którym piszesz, ISTNIEJE (nie 404)")
    print("   • czy plik, który miałeś zrobić, zmienił rozmiar i czas")
    print("   • czy ktoś z załogi sprawdził Twój pomiar (nikt nie sprawdza sam siebie)")
    print("  Brak elementu = zdanie NIE IDZIE do Tomasza albo idzie jako NIE WIEM.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
