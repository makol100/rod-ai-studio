#!/usr/bin/env python3
"""zrobione.py — BRAMKA UKONCZENIA. Nic nie jest "zrobione" bez dowodu.

Powstala 29.07.2026 z dwoch wnioskow zalogi, ktore Klaudek przyjal i zwlekal z wdrozeniem:
  ZENEK: "Kluczowe jest odebranie mozliwosci przejscia do stanu DONE, gdy wymagany artefakt nie istnieje."
  GENEK: "Najwyzsza dzwignie ma audyt meldunku — odbiera Klaudkowi status jedynej i ostatecznej wyroczni."

Zasada: zanim cokolwiek zostanie oglosone jako dzialajace — musi przejsc trzy sprawdzenia MECHANICZNE:
  1. DOWOD ISTNIEJE — kazdy wskazany plik dowodowy jest na dysku i nie jest pusty
  2. TEST JEST ZIELONY — jesli podano test, musi przejsc TERAZ (nie "przechodzil wczoraj")
  3. ZALOGA POTWIERDZA — twierdzenie idzie do kontroli; ktokolwiek stwierdzi BRAK SLADU = ODRZUCONE

Uzycie:
    python3 tools/zrobione.py --co "bramka dowodowa naprawiona" \
        --dowod tools/bramka_henia.py,testy/bramka/przypadki.json \
        --test tools/test_bramki.py
    python3 tools/zrobione.py --co "..." --dowod ... --bez-zalogi   # tylko sprawdzenia maszynowe

Wyjscie 0 = PRZEPUSZCZONE (wolno oglosic Tomaszowi i zapisac do wiedzy).
Wyjscie 2 = ODRZUCONE (nie wolno napisac, ze dziala).
Przy przepuszczeniu zostawia stempel .scratch/_zrobione_ok — hook pre-commit go sprawdza.
"""
import argparse
import os
import subprocess
import sys
import time

REPO = "/root/rod-ai-studio"
STEMPEL = os.path.join(REPO, ".scratch", "_zrobione_ok")


def sprawdz_dowody(lista: str) -> tuple:
    braki, ok = [], []
    for s in [x.strip() for x in lista.split(",") if x.strip()]:
        p = s if os.path.isabs(s) else os.path.join(REPO, s)
        if not os.path.exists(p):
            braki.append(f"{s} — NIE ISTNIEJE")
        elif os.path.isfile(p) and os.path.getsize(p) == 0:
            braki.append(f"{s} — PUSTY")
        else:
            rozmiar = os.path.getsize(p) if os.path.isfile(p) else 0
            ok.append(f"{s} ({rozmiar} B)")
    return ok, braki


def uruchom_test(sciezka: str) -> tuple:
    p = sciezka if os.path.isabs(sciezka) else os.path.join(REPO, sciezka)
    if not os.path.isfile(p):
        return False, f"test {sciezka} NIE ISTNIEJE"
    try:
        w = subprocess.run([sys.executable, p], cwd=REPO, capture_output=True, text=True, timeout=600)
    except Exception as e:
        return False, f"test nie dokonczyl: {e}"
    ostatnia = (w.stdout.strip().split("\n") or [""])[-1]
    return w.returncode == 0, ostatnia


def pytaj_zaloge(twierdzenie: str, dowody: str) -> tuple:
    """Kontrola przez zaloge — Klaudek nie zatwierdza sam siebie."""
    zadanie = f"""KONTROLA UKONCZENIA. Klaudek twierdzi, ze cos jest ZROBIONE i chce to oglosic Tomaszowi.

TWIERDZENIE: {twierdzenie}

PLIKI DOWODOWE (sa na dysku, otworz je SAM): {dowody}

PYTANIE ROZSTRZYGALNE — odpowiedz jednym slowem w pierwszej linii:
  POTWIERDZAM  — otworzyles dowody i one faktycznie popieraja twierdzenie
  BRAK SLADU   — dowody nie popieraja twierdzenia albo nie da sie ich otworzyc
Potem JEDNO zdanie uzasadnienia z cytatem albo nazwa pliku i linia.
Nie oceniaj, czy pomysl jest dobry. Oceniaj TYLKO, czy dowod pokrywa twierdzenie."""
    sciezka = "/tmp/_zrobione_kontrola.md"
    with open(sciezka, "w", encoding="utf-8") as f:
        f.write(zadanie)
    try:
        w = subprocess.run(
            [sys.executable, os.path.join(REPO, "tools", "zaloga.py"),
             "--zadanie", sciezka, "--katalog", "/tmp/zrobione_kontrola"],
            cwd=REPO, capture_output=True, text=True, timeout=900)
    except Exception as e:
        return False, [f"kontrola nie dokonczyla: {e}"]
    glosy, sprzeciw = [], False
    for imie in ("zenek", "genek", "henio"):
        p = f"/tmp/zrobione_kontrola/{imie}.txt"
        if not os.path.isfile(p):
            glosy.append(f"{imie}: GLOS NIEODEBRANY")
            continue
        tresc = open(p, encoding="utf-8", errors="replace").read()
        gorne = tresc.upper()
        # Kto odpowiadal BEZ dostepu do dysku, nie mogl otworzyc dowodow — jego "potwierdzam" nic nie znaczy.
        # Znalezione testem 29.07: Genek potwierdzil w TRYBIE AWARYJNYM i bramka to zaliczyla.
        if "TRYB AWARYJNY" in gorne:
            glosy.append(f"{imie}: GLOS NIEODEBRANY (tryb awaryjny — nie mial dostepu do dowodow)")
            continue
        if "BRAK SLADU" in gorne or "BRAK ŚLADU" in gorne:
            glosy.append(f"{imie}: BRAK SLADU")
            sprzeciw = True
        elif "POTWIERDZAM" in gorne:
            glosy.append(f"{imie}: POTWIERDZAM")
        else:
            glosy.append(f"{imie}: odpowiedz niejednoznaczna")
            sprzeciw = True
    if "NIEODEBRANY" in " ".join(glosy) and not sprzeciw:
        glosy.append("(brak glosu NIE jest zgoda)")
    return (not sprzeciw), glosy


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--co", required=True, help="co dokladnie twierdzisz, ze jest zrobione")
    p.add_argument("--dowod", required=True, help="pliki dowodowe po przecinku")
    p.add_argument("--test", default="", help="test, ktory MUSI byc zielony teraz")
    p.add_argument("--bez-zalogi", action="store_true", help="tylko sprawdzenia maszynowe")
    a = p.parse_args()

    print(f"BRAMKA UKONCZENIA: {a.co}\n")
    upadki = []

    ok, braki = sprawdz_dowody(a.dowod)
    print("1. DOWODY:")
    for x in ok:
        print(f"   JEST   {x}")
    for x in braki:
        print(f"   !!!    {x}")
    if braki:
        upadki.append(f"{len(braki)} dowodow nie istnieje albo jest pustych")
    if not ok:
        upadki.append("zero dowodow")

    print("\n2. TEST:")
    if a.test:
        zielony, opis = uruchom_test(a.test)
        print(f"   {'ZIELONY' if zielony else 'CZERWONY'}  {a.test} -> {opis}")
        if not zielony:
            upadki.append("test nie jest zielony")
    else:
        print("   (nie podano testu — dla poprawki kodu to SAMO W SOBIE jest brakiem dowodu)")

    print("\n3. KONTROLA ZALOGI:")
    if a.bez_zalogi:
        print("   pominieta na wyrazne zadanie")
    else:
        zgoda, glosy = pytaj_zaloge(a.co, a.dowod)
        for g in glosy:
            print(f"   {g}")
        if not zgoda:
            upadki.append("zaloga nie potwierdzila")

    print()
    if upadki:
        print("WERDYKT: ODRZUCONE — " + "; ".join(upadki))
        print("NIE WOLNO napisac Tomaszowi, ze to dziala. Napraw i uruchom ponownie.")
        return 2
    os.makedirs(os.path.dirname(STEMPEL), exist_ok=True)
    with open(STEMPEL, "w", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {a.co} | dowody: {a.dowod}\n")
    print("WERDYKT: PRZEPUSZCZONE — dowody sa, test zielony, zaloga potwierdza.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
