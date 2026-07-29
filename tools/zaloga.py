#!/usr/bin/env python3
"""zaloga.py — jedno polecenie, cala czworka pracuje rownolegle.

Powstalo 29.07.2026, bo Tomasz musial trzeci raz tego samego dnia przypominac:
"Dlaczego pracujecie we dwojke? Mieliscie pracowac zawsze wszyscy".
Regula byla zapisana w pamieci, w START.md, w AGENTS.md i w podreczniku — i mimo to Klaudek
zrobil pomiar z samym Heniem. Wniosek: regula w dokumencie nie wystarcza. Wolanie calej zalogi
musi byc LATWIEJSZE niz praca solo. To narzedzie robi z tego jedno polecenie.

Uzycie:
    python3 tools/zaloga.py --zadanie /tmp/zadanie.md
    python3 tools/zaloga.py --zadanie /tmp/z.md --material plik1.md,plik2.txt
    python3 tools/zaloga.py --zadanie /tmp/z.md --kto zenek,genek        # gdy ktos juz odpowiedzial
    python3 tools/zaloga.py --zadanie /tmp/z.md --katalog /tmp/narada7   # gdzie zapisac glosy

Kazdy dostaje TO SAMO zadanie i ten sam material. Nikt nie widzi cudzej odpowiedzi przed napisaniem
wlasnej — glosy powstaja niezaleznie, dokladnie tak jak chcial Tomasz.
Material dokladany jest do zlecenia Genka, bo on jako jedyny nie ma dostepu do dysku.

Wynik: pliki <katalog>/<imie>.txt oraz zbiorcze podsumowanie na wyjsciu.
Awaria jednego wykonawcy NIE jest zgoda — w podsumowaniu stoi wtedy "GLOS NIEODEBRANY".
"""
import argparse
import json
import os
import subprocess
import sys
import threading
import urllib.request

REPO = "/root/rod-ai-studio"
STOPKA = ("\n\nPodpisz sie swoim imieniem. Jesli czegos nie da sie ustalic z materialu — napisz NIE WIEM. "
          "Nie uzgadniaj odpowiedzi z nikim, to ma byc TWOJ glos.")


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


def zenek(zadanie: str, _material: str, wynik: dict) -> None:
    try:
        w = subprocess.run(["codex", "exec", zadanie + STOPKA], cwd=REPO,
                           capture_output=True, text=True, timeout=600)
        out = w.stdout
        wynik["zenek"] = out.split("\ncodex\n")[-1].strip() if "\ncodex\n" in out else out[-3000:]
    except Exception as e:
        wynik["zenek"] = f"GLOS NIEODEBRANY ({e})"


def genek(zadanie: str, material: str, wynik: dict) -> None:
    try:
        klucz = next(l.split("=", 1)[1].strip() for l in open("/root/.gemini/.env")
                     if l.startswith("GEMINI_API_KEY="))
    except Exception as e:
        wynik["genek"] = f"GLOS NIEODEBRANY (brak klucza: {e})"
        return
    tresc = zadanie + STOPKA
    if material:
        tresc += "\n\n=== MATERIAL ZRODLOWY (dolaczony, bo nie masz dostepu do dysku) ===\n" + material
    body = json.dumps({
        "contents": [{"parts": [{"text": tresc}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2000,
                             "thinkingConfig": {"thinkingBudget": 0}},
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={klucz}",
        data=body, headers={"Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=400).read())
        c = r["candidates"][0]
        tekst = "".join(p.get("text", "") for p in c.get("content", {}).get("parts", []))
        wynik["genek"] = tekst.strip() or "GLOS NIEODEBRANY (pusta odpowiedz)"
    except Exception as e:
        wynik["genek"] = f"GLOS NIEODEBRANY ({e})"


def henio(zadanie: str, _material: str, wynik: dict) -> None:
    sciezka = "/tmp/_zaloga_zadanie_henio.txt"
    try:
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write(zadanie + STOPKA)
        os.chmod(sciezka, 0o644)
        w = subprocess.run(
            ["su", "-", "hermes", "-c", f'hermes -z "$(cat {sciezka})"'],
            capture_output=True, text=True, timeout=600)
        wynik["henio"] = (w.stdout or w.stderr).strip() or "GLOS NIEODEBRANY (pusta odpowiedz)"
    except Exception as e:
        wynik["henio"] = f"GLOS NIEODEBRANY ({e})"


WYKONAWCY = {"zenek": zenek, "genek": genek, "henio": henio}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--zadanie", required=True, help="plik z trescia zadania")
    p.add_argument("--material", default="", help="pliki zrodlowe po przecinku (trafiaja do Genka)")
    p.add_argument("--kto", default="zenek,genek,henio")
    p.add_argument("--katalog", default="/tmp/narada")
    a = p.parse_args()

    if not os.path.isfile(a.zadanie):
        print(f"BLAD: brak pliku zadania {a.zadanie}")
        return 2
    with open(a.zadanie, encoding="utf-8", errors="replace") as f:
        zadanie = f.read()
    if not zadanie.strip():
        print("BLAD: zadanie jest puste")
        return 2

    material = czytaj_material(a.material)
    os.makedirs(a.katalog, exist_ok=True)
    kto = [x.strip() for x in a.kto.split(",") if x.strip() in WYKONAWCY]
    if not kto:
        print("BLAD: nikt do wywolania")
        return 2

    print(f"NARADA: {', '.join(kto)} — kazdy dostaje to samo, nikt nie widzi cudzej odpowiedzi.\n")
    wynik: dict = {}
    watki = [threading.Thread(target=WYKONAWCY[k], args=(zadanie, material, wynik)) for k in kto]
    for w in watki:
        w.start()
    for w in watki:
        w.join()

    nieodebrane = 0
    for k in kto:
        tresc = wynik.get(k, "GLOS NIEODEBRANY (brak wyniku)")
        sciezka = os.path.join(a.katalog, f"{k}.txt")
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write(tresc)
        if tresc.startswith("GLOS NIEODEBRANY"):
            nieodebrane += 1
        print("=" * 25, k.upper(), "=" * 25)
        print(tresc, "\n")

    print(f"GLOSY: {len(kto) - nieodebrane}/{len(kto)} odebrane. Zapisane w {a.katalog}/")
    if nieodebrane:
        print("UWAGA: brak glosu NIE jest zgoda. Wniosek bez pelnego skladu jest niepelny.")
    print("Klaudek dokłada swoj wlasny glos osobno — jest w druzynie, nie nad nia.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
