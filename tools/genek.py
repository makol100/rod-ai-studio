#!/usr/bin/env python3
"""genek.py — Genek Z DOSTEPEM DO DYSKU. Koniec doklejania mu materialu recznie.

Powod (29.07.2026, Tomasz: "Czemu Genek nie ma dysku do chuja!!!"):
Genek to zdalne API Google — nie ma na VPS procesu, ktory sam otworzylby plik. ALE na serwerze stoi
Gemini CLI 0.52.0, ktore ma wlasne narzedzia plikowe i CZYTA DYSK. Kiedy CLI zaczelo sie wywalac na
limitach (503, quota), Klaudek przerzucil Genka na gole wywolania API z recznie doklejanym materialem
— i nikt nigdy nie wrocil. To byla nasza proteza, nie ograniczenie Genka.

To narzedzie przywraca mu dysk:
  DROGA 1 (domyslna): Gemini CLI w katalogu repo — Genek SAM czyta pliki, greppuje, sprawdza.
  DROGA 2 (awaryjna): gole API z doklejonym materialem — gdy CLI padnie. Oznaczona w wyniku jako
                      TRYB AWARYJNY, zeby nikt nie wzial odpowiedzi bez dostepu do zrodel za pelnowartosciowa.

Uzycie:
    python3 tools/genek.py "Przeczytaj wiedza/CENA_BLEDOW.md i sprawdz czy suma w tabeli sie zgadza"
    python3 tools/genek.py --plik /tmp/zadanie.md
    python3 tools/genek.py "..." --material wiedza/X.md   # material tylko dla drogi awaryjnej
    python3 tools/genek.py "..." --tylko-api              # wymus droga 2

Fail-closed: obie drogi padly = wyjscie 2 i komunikat. Nigdy zmyslona tresc, nigdy cicha degradacja.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

REPO = "/root/rod-ai-studio"
MODEL_API = "gemini-2.5-flash"


def klucz() -> str:
    for s in (os.path.expanduser("~/.gemini/.env"), "/root/.gemini/.env"):
        if os.path.isfile(s):
            for linia in open(s, encoding="utf-8"):
                if linia.startswith("GEMINI_API_KEY="):
                    return linia.split("=", 1)[1].strip()
    return ""


def droga_cli(zadanie: str, limit_s: int) -> tuple:
    """Genek z wlasnymi rekami: czyta pliki, greppuje, sprawdza — sam."""
    srodowisko = dict(os.environ, GEMINI_CLI_TRUST_WORKSPACE="true")
    try:
        w = subprocess.run(["gemini", "-p", zadanie], cwd=REPO, env=srodowisko,
                           capture_output=True, text=True, timeout=limit_s)
    except subprocess.TimeoutExpired:
        return "", f"CLI: przekroczony czas {limit_s}s"
    except FileNotFoundError:
        return "", "CLI: brak polecenia gemini"
    tekst = "\n".join(l for l in w.stdout.split("\n")
                      if "256-color" not in l and "Warning:" not in l).strip()
    if w.returncode != 0 or not tekst:
        blad = (w.stderr or "").strip()[:300] or f"kod wyjscia {w.returncode}"
        return "", f"CLI: {blad}"
    return tekst, ""


def droga_api(zadanie: str, material: str) -> tuple:
    k = klucz()
    if not k:
        return "", "API: brak GEMINI_API_KEY"
    tresc = zadanie
    if material:
        tresc += "\n\n=== MATERIAL (doklejony, bo dzialasz bez dostepu do dysku) ===\n" + material
    body = json.dumps({
        "contents": [{"parts": [{"text": tresc}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2500,
                             "thinkingConfig": {"thinkingBudget": 0}},
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_API}:generateContent?key={k}",
        data=body, headers={"Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=300).read())
    except Exception as e:
        return "", f"API: {e}"
    kand = r.get("candidates") or []
    if not kand:
        return "", "API: brak odpowiedzi"
    tekst = "".join(p.get("text", "") for p in kand[0].get("content", {}).get("parts", []))
    return (tekst.strip(), "") if tekst.strip() else ("", "API: pusta odpowiedz")


def czytaj_material(lista: str) -> str:
    if not lista:
        return ""
    kawalki = []
    for s in [x.strip() for x in lista.split(",") if x.strip()]:
        p = s if os.path.isabs(s) else os.path.join(REPO, s)
        if os.path.isfile(p):
            with open(p, encoding="utf-8", errors="replace") as f:
                kawalki.append(f"--- {s} ---\n{f.read()[:25000]}")
        else:
            kawalki.append(f"--- {s} --- PLIK NIE ISTNIEJE")
    return "\n\n".join(kawalki)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("zadanie", nargs="*", default=[])
    p.add_argument("--plik", default="", help="plik z trescia zadania")
    p.add_argument("--material", default="", help="pliki dla drogi awaryjnej")
    p.add_argument("--tylko-api", action="store_true")
    p.add_argument("--limit", type=int, default=280, help="sekundy na droge CLI")
    p.add_argument("--zapis", default="")
    a = p.parse_args()

    if a.plik:
        if not os.path.isfile(a.plik):
            print(f"BLAD: brak pliku zadania {a.plik}")
            return 2
        zadanie = open(a.plik, encoding="utf-8", errors="replace").read()
    else:
        zadanie = " ".join(a.zadanie)
    if not zadanie.strip():
        print("BLAD: puste zadanie")
        return 2

    zadanie += ("\n\nPracujesz w katalogu /root/rod-ai-studio — MASZ DOSTEP DO PLIKOW, czytaj je sam. "
                "Kazde twierdzenie ze sladem: plik i linia. Czego nie da sie ustalic — NIE WIEM. Podpisz sie: GENEK.")

    powody = []
    if not a.tylko_api:
        tekst, blad = droga_cli(zadanie, a.limit)
        if tekst:
            wynik = f"[GENEK — DROGA 1: wlasny dostep do dysku przez CLI]\n\n{tekst}"
            if a.zapis:
                open(a.zapis, "w", encoding="utf-8").write(wynik)
            print(wynik)
            return 0
        powody.append(blad)

    tekst, blad = droga_api(zadanie, czytaj_material(a.material))
    if tekst:
        wynik = ("[GENEK — TRYB AWARYJNY: bez dostepu do dysku, tylko doklejony material"
                 + (f"; droga 1 padla: {powody[0]}" if powody else "") + "]\n\n" + tekst)
        if a.zapis:
            open(a.zapis, "w", encoding="utf-8").write(wynik)
        print(wynik)
        return 0
    powody.append(blad)
    print("BLAD: obie drogi padly — " + " | ".join(powody))
    print("NIE zmyslam zastepczej tresci.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
