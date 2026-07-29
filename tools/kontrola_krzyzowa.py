#!/usr/bin/env python3
"""Kontrola krzyzowa - jeden wykonawca sprawdza twierdzenie drugiego przy SUROWYM materiale.

Uzycie:
    python3 tools/kontrola_krzyzowa.py --twierdzenie "Orca ma 3800 gwiazdek" \
        --material /sciezka/do/dowodu.txt [--kto zenek|genek|obaj]

Zasada: kontroler dostaje SUROWY material i jedno pytanie - czy twierdzenie z niego wynika.
Nie dostaje autora twierdzenia ani kontekstu, ktory moglby go sklonic do uprzejmosci.
Werdykt kontrolera jest HIPOTEZA - liczbe i tak rozstrzyga API, zawartosc pliku rozstrzyga grep.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

PYTANIE = (
    "Jestes kontrolerem faktow. Ponizej SUROWY material i JEDNO twierdzenie.\n"
    "Odpowiedz w trzech linijkach, po polsku, bez uprzejmosci:\n"
    "WERDYKT: POTWIERDZONE / OBALONE / NIE WYNIKA Z MATERIALU\n"
    "DOWOD: doslowny fragment materialu, ktory rozstrzyga (albo: brak takiego fragmentu)\n"
    "UWAGA: jedno zdanie, jesli twierdzenie jest czesciowo prawdziwe albo material nie wystarcza\n"
    "Nie zgadzaj sie z twierdzeniem dlatego, ze brzmi rozsadnie. Liczy sie wylacznie material.\n"
)


def zbierz(twierdzenie: str, material: str) -> str:
    return f"{PYTANIE}\n=== MATERIAL ===\n{material}\n\n=== TWIERDZENIE ===\n{twierdzenie}\n"


def genek(tresc: str) -> str:
    klucz = None
    with open("/root/.gemini/.env") as f:
        for linia in f:
            if linia.startswith("GEMINI_API_KEY="):
                klucz = linia.split("=", 1)[1].strip()
    if not klucz:
        return "GENEK: brak klucza API"
    body = json.dumps({
        "contents": [{"parts": [{"text": tresc}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 600},
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={klucz}",
        data=body, headers={"Content-Type": "application/json"})
    try:
        odp = json.loads(urllib.request.urlopen(req, timeout=120).read())
        return odp["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:  # blad kontrolera nie moze uchodzic za zgode
        return f"GENEK: KONTROLA NIEWYKONANA ({e})"


def zenek(tresc: str) -> str:
    try:
        wynik = subprocess.run(
            ["codex", "exec", tresc], cwd="/root/rod-ai-studio",
            capture_output=True, text=True, timeout=420)
        out = wynik.stdout
        znacznik = "\ncodex\n"
        return out.split(znacznik)[-1].strip() if znacznik in out else out[-1500:]
    except Exception as e:
        return f"ZENEK: KONTROLA NIEWYKONANA ({e})"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--twierdzenie", required=True)
    p.add_argument("--material", required=True, help="sciezka do pliku z surowym dowodem")
    p.add_argument("--kto", default="obaj", choices=["zenek", "genek", "obaj"])
    a = p.parse_args()

    if not os.path.isfile(a.material):
        print(f"BLAD: brak pliku z materialem: {a.material}")
        return 2
    with open(a.material, encoding="utf-8", errors="replace") as f:
        material = f.read()
    if not material.strip():
        print("BLAD: material jest pusty - kontrola bez materialu nie ma sensu")
        return 2

    tresc = zbierz(a.twierdzenie, material)
    print(f"TWIERDZENIE: {a.twierdzenie}")
    print(f"MATERIAL: {a.material} ({len(material)} znakow)\n")
    if a.kto in ("genek", "obaj"):
        print("=== GENEK ===")
        print(genek(tresc), "\n")
    if a.kto in ("zenek", "obaj"):
        print("=== ZENEK ===")
        print(zenek(tresc), "\n")
    print("PRZYPOMNIENIE: werdykt kontrolera to hipoteza. Liczbe rozstrzyga API, zawartosc pliku - grep.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
