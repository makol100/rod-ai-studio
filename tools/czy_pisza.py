#!/usr/bin/env python3
"""czy_pisza.py — JEDYNY dozwolony sposob sprawdzenia, czy zaloga jeszcze pracuje.

POWOD POWSTANIA (18.08.2026, dekret Tomasza: "Popraw to zeby wiecej to nie mialo
miejsca ze bedziesz robil mnie w chuja ze on dalej pisze"):

Klaudek DWA RAZY jednego dnia meldowal "Zenek jeszcze pisze", gdy Zenek dawno
skonczyl. Drugi raz Tomasz czekal 11,5 GODZINY na meldunek, ktory lezal gotowy.

PRZYCZYNA — pulapka `pgrep`/`ps | grep`:
    ps -eo cmd | grep "g284"        <- lapie WLASNA komende bash, ktora zawiera "g284"
    pgrep -f "zaloga.py"            <- to samo, gdy wolane z powloki z ta nazwa w linii
Klaudek widzial "jest proces" i meldowal "pisza". To byl jego wlasny grep.

ZASADA: nie pytamy "czy jest proces o takiej nazwie". Pytamy o TRZY rzeczy naraz:
    1. czy istnieje ZYWY proces zalogi (z wykluczeniem samego siebie i grepa),
    2. KIEDY ostatnio zmienil sie plik wyniku (to jedyny dowod, ze cos sie dzieje),
    3. czy koncowka pliku wyglada na URWANA czy DOMKNIETA.
Gdy plik nie rosnie od minut, a proces "jest" — to NIE znaczy "pisze". To znaczy
"sprawdz jeszcze raz, bo najpewniej skonczyl".

Uzycie:
    python3 tools/czy_pisza.py .scratch/g284
    python3 tools/czy_pisza.py .scratch/g284 --prog 180
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def zywe_procesy_zalogi() -> list[tuple[str, str, str]]:
    """Zwraca [(pid, czas_dzialania, skrocona_komenda)] — TYLKO prawdziwe procesy zalogi.

    Wyklucza: samego siebie, procesy-rodzicow tej powloki i wszystko, co zawiera
    'czy_pisza' albo 'grep' (to wlasnie te falszywki, na ktore Klaudek sie nabral)."""
    moj = str(os.getpid())
    rodzic = str(os.getppid())
    try:
        w = subprocess.run(["ps", "-eo", "pid=,etime=,args="],
                           capture_output=True, text=True, timeout=30)
    except Exception:
        return []
    wynik = []
    for linia in w.stdout.splitlines():
        czesci = linia.strip().split(None, 2)
        if len(czesci) < 3:
            continue
        pid, czas, cmd = czesci
        if pid in (moj, rodzic):
            continue
        if "czy_pisza" in cmd or cmd.startswith("grep") or " grep " in cmd:
            continue
        if "zaloga.py" not in cmd:
            continue
        wynik.append((pid, czas, cmd[:90]))
    return wynik


def stan_katalogu(katalog: Path, prog_sekund: int) -> int:
    if not katalog.is_dir():
        print(f"BLAD: katalog {katalog} nie istnieje")
        return 2

    procesy = zywe_procesy_zalogi()
    pliki = sorted(katalog.glob("*.txt"))
    teraz = time.time()

    print(f"KATALOG: {katalog}")
    print(f"CZAS TERAZ: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    if procesy:
        print(f"PROCESY ZALOGI: {len(procesy)} zywych")
        for pid, czas, cmd in procesy:
            print(f"   pid {pid}  dziala od {czas}  {cmd}")
    else:
        print("PROCESY ZALOGI: BRAK — nikt nie pracuje")
    print()

    if not pliki:
        print("PLIKI WYNIKOW: brak")
    else:
        print("PLIKI WYNIKOW:")
        for p in pliki:
            wiek = teraz - p.stat().st_mtime
            rozmiar = p.stat().st_size
            czas_zmiany = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.stat().st_mtime))
            if wiek < 60:
                opis_wieku = f"{int(wiek)} s temu"
            elif wiek < 3600:
                opis_wieku = f"{int(wiek // 60)} min temu"
            else:
                opis_wieku = f"{wiek / 3600:.1f} GODZIN temu"
            print(f"   {p.name:<16} {rozmiar:>8} B   zmieniony {czas_zmiany}  ({opis_wieku})")
            if rozmiar == 0:
                print(f"      -> PUSTY. To nie jest 'w toku' — to brak wyniku.")

    print()
    # WERDYKT — jednoznaczny, bez miejsca na 'chyba pisze'
    najswiezszy = max((p.stat().st_mtime for p in pliki), default=0)
    od_zmiany = teraz - najswiezszy if najswiezszy else None

    if not procesy and pliki:
        print("WERDYKT: SKONCZYLI. Zaden proces nie zyje, wyniki sa na dysku.")
        print("         -> PRZECZYTAJ pliki i zamelduj Tomaszowi. Nie mow 'jeszcze pisza'.")
        return 0
    if not procesy and not pliki:
        print("WERDYKT: NIC NIE CHODZI I NIC NIE MA. Zadanie padlo albo nie wystartowalo.")
        print("         -> sprawdz log uruchomienia (/tmp/zaloga_*.log) i URUCHOM PONOWNIE.")
        return 3
    if procesy and od_zmiany is not None and od_zmiany > prog_sekund:
        print(f"WERDYKT: PODEJRZANE. Proces zyje, ale plik nie rosnie od "
              f"{od_zmiany / 60:.0f} min (prog: {prog_sekund // 60} min).")
        print("         -> NIE meldowac 'pisza'. Sprawdz koncowke pliku: czy urwana czy domknieta.")
        return 1
    print("WERDYKT: PRACUJA NAPRAWDE (proces zyje, plik rosnie).")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Czy zaloga jeszcze pisze — uczciwa odpowiedz.")
    p.add_argument("katalog", help="katalog wynikow, np. .scratch/g284")
    p.add_argument("--prog", type=int, default=300,
                   help="po ilu sekundach bez zmiany pliku uznac za podejrzane (domyslnie 300)")
    a = p.parse_args()
    k = Path(a.katalog)
    if not k.is_absolute():
        k = REPO / k
    return stan_katalogu(k, a.prog)


if __name__ == "__main__":
    sys.exit(main())
