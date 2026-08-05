#!/usr/bin/env python3
"""Generuje dokładnie dziewięcioliniowy brief startowy dla Klaudka."""

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path("/root/rod-ai-studio")
REJESTR = REPO / ".scratch/decyzje_tomasza.jsonl"
START = REPO / "wiedza/START.md"
TECZKA = REPO / "wiedza/TECZKI/KLAUDEK.md"
CLAUDE = Path("/root/.claude/CLAUDE.md")
CEL = REPO / "wiedza/BRIEF_DLA_KLAUDKA.md"


def jedna_linia(tekst):
    return re.sub(r"\s+", " ", tekst).strip()


def wczytaj_decyzje():
    # Wymagany pomiar interfejsem rejestru przy każdym odświeżeniu.
    subprocess.run(["python3", str(REPO / "tools/decyzje.py"), "--lista", "--wszystkie"],
                   cwd=REPO, check=True, capture_output=True, text=True)
    with REJESTR.open(encoding="utf-8") as plik:
        return [json.loads(w) for w in plik if w.strip()]


def obowiazujace(wpisy):
    wygasle = {w.get("dotyczy") for w in wpisy if w.get("typ") == "adnotacja"}
    return [w for w in wpisy if w.get("typ") != "adnotacja" and w["id"] not in wygasle]


def temat(wpisy, nazwa):
    znalezione = [w for w in obowiazujace(wpisy) if w.get("temat") == nazwa]
    if not znalezione:
        raise RuntimeError(f"brak obowiązującej decyzji: {nazwa}")
    return znalezione[-1]


def skrot(wpis, limit=105):
    tekst = jedna_linia(wpis["tresc"])
    return tekst if len(tekst) <= limit else tekst[:limit - 1].rstrip() + "…"


def komenda_henia():
    trafienie = re.search(r"Wywołanie:\s*`([^`]+)`", START.read_text(encoding="utf-8"))
    if not trafienie:
        raise RuntimeError("brak komendy Henia w START.md")
    return jedna_linia(trafienie.group(1))


def zaleglosc_teleportow():
    wynik = subprocess.run(["python3", str(REPO / "tools/teleport.py"), "--sprawdz"],
                           cwd=REPO, check=True, capture_output=True, text=True).stdout
    pomiary = re.findall(r"^\s*(fabryka|Home Assistant)\s+bez wpisu:\s+([0-9.]+) dnia", wynik, re.M)
    if len(pomiary) != 2:
        raise RuntimeError("niepełny pomiar teleportów")
    return ", ".join(f"{nazwa} {dni} dnia" for nazwa, dni in pomiary)


def pilne_reczne():
    """Sprawy wymagajace RECZNEJ roboty Tomasza — Klaudek ma o nich PRZYPOMINAC, nie robic sam.

    4.08: Tomasz odlozyl wymiane kluczy API ("dzis wieczorem albo jutro rano, teraz nie mam czasu").
    ODLOZYL, a nie odwolal — i to jest roznica, ktora Klaudek gubi. Bez tego przypomnienia
    sprawa zniknelaby tak samo jak teleport: nie przez decyzje, tylko przez ciszę.

    Brief ma TWARDO 9 linii (metoda Gawande — dluzsza lista uczy, zeby jej nie czytac),
    wiec sprawa pilna WYPIERA linie o naganie. Nagana jest historia, to jest do zrobienia.
    """
    sciezka = REPO / ".scratch" / "pilne_reczne.txt"
    try:
        for l in sciezka.read_text(encoding="utf-8").splitlines():
            if l.strip() and not l.startswith("#"):
                return jedna_linia(l.strip())
    except OSError:
        pass
    return ""


def ostatnia_nagana():
    nagany = list(re.finditer(r"^## (NAGANA[^\n]+)$", TECZKA.read_text(encoding="utf-8"), re.M))
    if not nagany:
        raise RuntimeError("brak nagany w teczce Klaudka")
    return jedna_linia(nagany[-1].group(1))


def stan_produkcji(d):
    """Czy ostatnia decyzja o produkcji NAKLADA stop, czy go ZDEJMUJE."""
    t = (d.get("tresc") or d.get("decyzja") or "").upper()
    t = t.replace("Ę", "E").replace("Ó", "O").replace("Ż", "Z").replace("Ź", "Z")
    zdjete = ("ZDJETY", "ZDJETE", "ZDJETA", "WZNOWION", "RUSZAMY", "ODWOLANY", "ODWOLANE")
    if any(k in t for k in zdjete):
        return "WOLNA — stop zdjety"
    return "STOP OBOWIAZUJE"


def main():
    wpisy = wczytaj_decyzje()
    aktywne = obowiazujace(wpisy)
    if not aktywne:
        raise RuntimeError("brak obowiązujących decyzji")
    ostatnia = aktywne[-1]
    stop = temat(wpisy, "produkcja")
    hans = temat(wpisy, "hans")
    genek = temat(wpisy, "genek")
    kierownik = temat(wpisy, "kierownik")
    teraz = datetime.now(ZoneInfo("Europe/Warsaw"))
    dni_claude = (datetime.now().timestamp() - CLAUDE.stat().st_mtime) / 86400
    _pilne = pilne_reczne()
    linie = [
        # BLAD ZNALEZIONY 5.08 przez Tomasza ("Aktualizacja przed odprawa zrobiona?"):
        # narzedzie pisalo ZAWSZE "OBOWIĄZUJE", nie sprawdzajac, czy decyzja stop NAKLADA
        # czy ZDEJMUJE. Po D-0039 ("STOP PRODUKCJI ZDJETY") brief nadal straszyl stopem —
        # nowy Klaudek stanalby z produkcja, ktora Tomasz wznowil.
        f"1. PRODUKCJA: {stan_produkcji(stop)} ({stop['id']}) | wygenerowano {teraz:%Y-%m-%d %H:%M:%S %Z}",
        f"2. OSTATNIA DECYZJA: {ostatnia['id']} | {ostatnia['czas_tomasza'][:10]} | {skrot(ostatnia)}",
        f"3. PRAWA RĘKA: HENIO | {komenda_henia()}",
        f"4. HANS: Henia, nie Klaudka ({hans['id']})",
        f"5. TELEPORTY: {zaleglosc_teleportow()}",
        f"6. /root/.claude/CLAUDE.md: {dni_claude:.1f} dnia bez zmian",
        (f"7. !! DO ZROBIENIA PRZEZ TOMASZA: {_pilne}" if _pilne
         else f"7. OSTATNIA NAGANA KLAUDKA: {ostatnia_nagana()}"),
        f"8. GENEK: oszczędzany — tylko oczy/uszy/grafika ({genek['id']}: {skrot(genek)})",
        f"9. KIEROWNIK: Klaudek, rozstrzygnięte 4.08 ({kierownik['id']})",
    ]
    if len(linie) != 9 or any("\n" in linia for linia in linie):
        raise RuntimeError("brief nie ma dokładnie dziewięciu pojedynczych linii")
    tmp = CEL.with_suffix(".md.tmp")
    tmp.write_text("\n".join(linie) + "\n", encoding="utf-8")
    os.replace(tmp, CEL)
    print(f"[brief] zapisano {CEL}: 9 linii")


if __name__ == "__main__":
    # 4.08: bez tego kazde uruchomienie — TAKZE `--help` — wykonywalo zapis.
    # Zenek NADPISAL brief, probujac tylko zobaczyc pomoc (zglosil to sam w audycie).
    import argparse as _ap
    _p = _ap.ArgumentParser(description="Generator briefu dla Klaudka (utrzymuje HENIO)")
    _p.add_argument("--pokaz", action="store_true",
                    help="tylko wypisz wynik, NIE zapisuj niczego na dysk")
    _ARGS = _p.parse_args()
    main()
