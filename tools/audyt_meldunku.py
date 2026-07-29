#!/usr/bin/env python3
"""audyt_meldunku.py — zaloga sprawdza KLAUDKA, zanim jego meldunek trafi do Tomasza.

Odwrocenie ukladu: dotad Klaudek oceniał zaloge. Tu zaloga ocenia jego.

Uzycie:
    python3 tools/audyt_meldunku.py --meldunek /tmp/moj_meldunek.txt
    python3 tools/audyt_meldunku.py --meldunek /tmp/m.txt --pliki wiedza/NAUKI.md,AGENTS.md

Co robi:
1. HENIK (24/7, grosze) — dostaje meldunek i sprawdza KAZDA liczbe oraz nazwe wlasna
   przy zrodlach na dysku. Zwraca liste: twierdzenie -> POTWIERDZONE / OBALONE / BRAK SLADU.
2. ZENEK (rozumowanie) — szuka wnioskow, ktore nie wynikaja z przeslanek.
3. GENEK (drugie oko) — dostaje meldunek RAZEM Z MATERIALEM (bo nie ma dostepu do dysku;
   to jego jedyne ograniczenie i tu jest zniesione).

Werdykt kontrolera to hipoteza; liczbe i tak rozstrzyga narzedzie. Ale meldunek, ktoremu
ktokolwiek postawil OBALONE albo BRAK SLADU, nie idzie do Tomasza bez poprawki.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

REPO = "/root/rod-ai-studio"

ZADANIE = """Jestes kontrolerem. Ponizej MELDUNEK, ktory Klaudek chce wyslac Tomaszowi (wlascicielowi).
Twoje zadanie: znalezc w nim twierdzenia, ktore NIE MAJA POKRYCIA.

Dla kazdej liczby, nazwy wlasnej, sciezki pliku i twierdzenia o stanie ("dziala", "zainstalowane",
"zweryfikowane") wypisz linijke:
  <twierdzenie> -> POTWIERDZONE (skad) | OBALONE (czym) | BRAK SLADU (= usunac z meldunku)

Na koncu jedno slowo: PRZEPUSCIC albo POPRAWIC.

Nie chwal. Nie streszczaj meldunku. Nie zgadzaj sie dlatego, ze brzmi rozsadnie.
Klaudek jest twoim przelozonym w hierarchii pracy, ale NIE w kwestii faktow — tu jesteś rowny.
Jesli nie mozesz czegos sprawdzic, napisz BRAK SLADU zamiast zgadywac.
"""


def henik(meldunek: str) -> str:
    polecenie = (
        ZADANIE
        + "\nMasz dostep do wiedzy fabryki w /home/hermes/fabryka/data/wiedza_kopia/ "
        "(podstawa + archiwum/ + teleporty) oraz do danych w /home/hermes/fabryka/data/. "
        "Sprawdzaj grepem, podawaj plik i numer linii.\n\n=== MELDUNEK ===\n"
        + meldunek
    )
    sciezka = "/tmp/_audyt_henik_zadanie.txt"
    with open(sciezka, "w", encoding="utf-8") as f:
        f.write(polecenie)
    try:
        subprocess.run(
            ["su", "-", "hermes", "-c",
             f'hermes -z "$(cat {sciezka})" > /tmp/_audyt_henik_out.txt 2>&1'],
            timeout=300, capture_output=True)
        with open("/tmp/_audyt_henik_out.txt", encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    except Exception as e:
        return f"HENIK: KONTROLA NIEWYKONANA ({e})"


def zenek(meldunek: str) -> str:
    polecenie = ZADANIE + "\nMasz caly dysk i python3 tools/szukaj.py.\n\n=== MELDUNEK ===\n" + meldunek
    try:
        w = subprocess.run(["codex", "exec", polecenie], cwd=REPO,
                           capture_output=True, text=True, timeout=420)
        out = w.stdout
        return out.split("\ncodex\n")[-1].strip() if "\ncodex\n" in out else out[-2000:]
    except Exception as e:
        return f"ZENEK: KONTROLA NIEWYKONANA ({e})"


def genek(meldunek: str, material: str) -> str:
    try:
        klucz = next(l.split("=", 1)[1].strip() for l in open("/root/.gemini/.env")
                     if l.startswith("GEMINI_API_KEY="))
    except Exception as e:
        return f"GENEK: KONTROLA NIEWYKONANA (brak klucza: {e})"
    tresc = ZADANIE + "\n=== MATERIAL ZRODLOWY ===\n" + material + "\n\n=== MELDUNEK ===\n" + meldunek
    body = json.dumps({
        "contents": [{"parts": [{"text": tresc}]}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 1200,
                             "thinkingConfig": {"thinkingBudget": 0}},
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={klucz}",
        data=body, headers={"Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=180).read())
        return r["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"GENEK: KONTROLA NIEWYKONANA ({e})"


def zbierz_material(lista: str) -> str:
    """Znosi slepote Genka: dokleja tresc wskazanych plikow do zlecenia."""
    if not lista:
        return "(nie wskazano plikow zrodlowych)"
    kawalki = []
    for sciezka in [s.strip() for s in lista.split(",") if s.strip()]:
        pelna = sciezka if os.path.isabs(sciezka) else os.path.join(REPO, sciezka)
        if os.path.isfile(pelna):
            with open(pelna, encoding="utf-8", errors="replace") as f:
                kawalki.append(f"--- {sciezka} ---\n{f.read()[:20000]}")
        else:
            kawalki.append(f"--- {sciezka} --- PLIK NIE ISTNIEJE")
    return "\n\n".join(kawalki)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--meldunek", required=True)
    p.add_argument("--pliki", default="", help="pliki zrodlowe, po przecinku — trafiaja do Genka")
    p.add_argument("--kto", default="wszyscy", choices=["henik", "zenek", "genek", "wszyscy"])
    a = p.parse_args()

    if not os.path.isfile(a.meldunek):
        print(f"BLAD: brak pliku z meldunkiem: {a.meldunek}")
        return 2
    with open(a.meldunek, encoding="utf-8", errors="replace") as f:
        meldunek = f.read()
    if not meldunek.strip():
        print("BLAD: meldunek pusty")
        return 2

    print(f"AUDYT MELDUNKU ({len(meldunek)} znakow) — zaloga sprawdza Klaudka\n")
    if a.kto in ("henik", "wszyscy"):
        print("=" * 20, "HENIK", "=" * 20)
        print(henik(meldunek), "\n")
    if a.kto in ("genek", "wszyscy"):
        print("=" * 20, "GENEK", "=" * 20)
        print(genek(meldunek, zbierz_material(a.pliki)), "\n")
    if a.kto in ("zenek", "wszyscy"):
        print("=" * 20, "ZENEK", "=" * 20)
        print(zenek(meldunek), "\n")
    print("ZASADA: meldunek z choc jednym OBALONE albo BRAK SLADU nie idzie do Tomasza bez poprawki.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
