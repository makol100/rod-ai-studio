#!/usr/bin/env python3
"""porzadek.py — jeden magazyn wiedzy, jeden indeks, zero recznego utrzymania.

Co robi (idempotentnie, mozna puszczac po kazdej zmianie):
1. Regeneruje wiedza/INDEX.md z RZECZYWISTYCH plikow (nazwa, data, rozmiar, pierwsza linia opisu).
   Indeks nie moze sie zestarzec, bo powstaje z dysku a nie z pamieci czlowieka.
2. Synchronizuje kopie dla dyzurnego (data/wiedza_kopia/) — Henik czyta to samo co reszta.
3. Raportuje magazyny wiedzy z rozmiarami i wiekiem — widac, co jest martwe.

Uzycie: python3 tools/porzadek.py [--cicho]
"""
import hashlib
import os
import shutil
import subprocess
import sys
from datetime import datetime

REPO = "/root/rod-ai-studio"
WIEDZA = os.path.join(REPO, "wiedza")
KOPIA = os.path.join(REPO, "data", "wiedza_kopia")
INDEX = os.path.join(WIEDZA, "INDEX.md")

MAGAZYNY = [
    (os.path.join(REPO, "TELEPORT_fabryka.md"), "teleport fabryki — ARCHIWUM, nie czytac w calosci, szukac przez szukaj.py"),
    ("/root/TELEPORT_HA.md", "teleport HA — ARCHIWUM, jw."),
    (os.path.join(REPO, "AGENTS.md"), "regulamin pracy agentow w repo — CZYTAC ZAWSZE"),
    ("/root/.claude/CLAUDE.md", "konfiguracja Claude Code na VPS"),
    ("/home/hermes/PODRECZNIK_DYZURNEGO.md", "podrecznik Henika (dyzurny)"),
]


def opis_pliku(sciezka: str) -> str:
    """Pierwsza sensowna linia pliku jako opis."""
    try:
        with open(sciezka, encoding="utf-8", errors="replace") as f:
            for linia in f:
                t = linia.strip().lstrip("#").strip()
                if len(t) > 15 and not t.startswith(("---", "```", "|")):
                    return t[:110]
    except OSError:
        pass
    return "(brak opisu)"


def buduj_index() -> int:
    pliki = sorted(
        (p for p in os.listdir(WIEDZA) if p.endswith(".md") and p != "INDEX.md"),
        key=lambda p: os.path.getmtime(os.path.join(WIEDZA, p)),
        reverse=True,
    )
    linie = [
        "# INDEKS WIEDZY FABRYKI",
        "",
        f"Wygenerowany automatycznie przez `tools/porzadek.py` — {datetime.now():%d.%m.%Y %H:%M}.",
        "NIE EDYTOWAC RECZNIE: kazde uruchomienie skryptu nadpisuje ten plik stanem dysku.",
        "",
        "Szukanie tresci: `python3 tools/szukaj.py <slowo>` — przeszukuje wszystko ponizej plus teleporty.",
        "",
        f"## Pliki wiedzy ({len(pliki)}), od najswiezszego",
        "",
        "| plik | zmiana | rozmiar | o czym |",
        "|---|---|---|---|",
    ]
    for p in pliki:
        pelna = os.path.join(WIEDZA, p)
        st = os.stat(pelna)
        linie.append(
            f"| `{p}` | {datetime.fromtimestamp(st.st_mtime):%d.%m} | {st.st_size // 1024 or 1}K | {opis_pliku(pelna)} |"
        )
    linie += ["", "## Pozostale magazyny", "", "| plik | rozmiar | zmiana | rola |", "|---|---|---|---|"]
    for sciezka, rola in MAGAZYNY:
        if os.path.isfile(sciezka):
            st = os.stat(sciezka)
            linie.append(f"| `{sciezka}` | {st.st_size // 1024 or 1}K | {datetime.fromtimestamp(st.st_mtime):%d.%m} | {rola} |")
    linie += [
        "",
        "## Zasada",
        "",
        "Jeden fakt ma jedno miejsce. Nowy zapis idzie do `wiedza/`, nie do teleportu.",
        "Teleporty sa ARCHIWUM historycznym — czyta sie je wyszukiwarka, nie w calosci.",
        "",
    ]
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write("\n".join(linie))
    return len(pliki)


def suma(sciezka: str) -> str:
    h = hashlib.sha256()
    with open(sciezka, "rb") as f:
        for kawalek in iter(lambda: f.read(65536), b""):
            h.update(kawalek)
    return h.hexdigest()


def sync_archiwum() -> int:
    """Teleporty (archiwum historyczne) do okna dyzurnego — ma widziec CALA historie."""
    cel = os.path.join(KOPIA, "archiwum")
    os.makedirs(cel, exist_ok=True)
    ile = 0
    for zrodlo in (os.path.join(REPO, "TELEPORT_fabryka.md"), "/root/TELEPORT_HA.md"):
        if not os.path.isfile(zrodlo):
            continue
        b = os.path.join(cel, os.path.basename(zrodlo))
        if not os.path.exists(b) or suma(zrodlo) != suma(b):
            shutil.copy2(zrodlo, b)
            ile += 1
    return ile


def sync_kopia() -> tuple:
    os.makedirs(KOPIA, exist_ok=True)
    zrodlo = {p for p in os.listdir(WIEDZA) if p.endswith(".md")}
    cel = {p for p in os.listdir(KOPIA) if p.endswith(".md")}
    skopiowane = 0
    for p in zrodlo:
        a, b = os.path.join(WIEDZA, p), os.path.join(KOPIA, p)
        if not os.path.exists(b) or suma(a) != suma(b):
            shutil.copy2(a, b)
            skopiowane += 1
    osierocone = cel - zrodlo
    for p in osierocone:
        os.remove(os.path.join(KOPIA, p))
    return skopiowane, len(osierocone)


def main() -> int:
    cicho = "--cicho" in sys.argv
    ile = buduj_index()
    nowe, usuniete = sync_kopia()
    arch = sync_archiwum()
    if not cicho:
        print(f"INDEX.md przebudowany: {ile} plikow wiedzy")
        print(f"kopia dyzurnego: {nowe} zaktualizowanych, {usuniete} osieroconych usunietych")
        print(f"archiwum (teleporty) dla dyzurnego: {arch} zaktualizowanych")
        print("\nMAGAZYNY:")
        for sciezka, rola in MAGAZYNY:
            if os.path.isfile(sciezka):
                st = os.stat(sciezka)
                wiek = (datetime.now() - datetime.fromtimestamp(st.st_mtime)).days
                flaga = "  <-- MARTWY?" if wiek > 7 else ""
                print(f"  {st.st_size:>8}B  {wiek:>2}d temu  {sciezka}{flaga}")
    try:
        subprocess.run(["git", "add", "wiedza/INDEX.md", "data/wiedza_kopia"], cwd=REPO, check=False,
                       capture_output=True, timeout=30)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
