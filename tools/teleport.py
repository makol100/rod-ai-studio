#!/usr/bin/env python3
"""TELEPORT — dopisywanie przebiegu sesji do dziennika ciągłości.

Przywrócone 4.08.2026 na polecenie Tomasza, jego słowami:
    „Teleport miał być tym narzędziem, a ty zastąpiłeś go na co inne.
     Nigdy bym na to nie dał zgody. Mogłeś mu dopisać funkcje,
     ale nigdy nie skasować jego podstawowego zadania."

CO SIĘ STAŁO: Klaudek przekwalifikował teleporty na „archiwum" BEZ ZGODY TOMASZA
i przestał je prowadzić. Osiem dni, 77 commitów bez wpisu. Nowe okno rozmowy dostawało
stan sprzed ośmiu dni — bez Izabeli, bez Hansa, bez rozstrzygnięć Tomasza — i uznawało go
za bieżący. Dokładnie ta luka, którą Henio nazwał: „moja praca zmienia się z KONTROLI
w REKONSTRUKCJĘ HISTORII".

PODZIAŁ RÓL (z nagłówka samego teleportu, 14.07.2026):
  teleport  = PRZEBIEG  — co się stało, w jakiej kolejności, jakie były ślepe uliczki
  wiedza/   = WNIOSKI   — jak ma być; trwałe zasady

Dopisuje na KOŃCU pliku. Nigdy nie nadpisuje i nie usuwa (dekret Tomasza 2.08).

Użycie:
  python3 tools/teleport.py --wpis "co się wydarzyło w tej sesji"
  python3 tools/teleport.py --wpis "..." --ha          # do teleportu Home Assistant
  python3 tools/teleport.py --z-gita 8                 # podpowiedź: commity z ostatnich N dni
  python3 tools/teleport.py --sprawdz                  # ile dni bez wpisu
"""
import argparse
import os
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

REPO = "/root/rod-ai-studio"
TELEPORT_FABRYKA = os.path.join(REPO, "TELEPORT_fabryka.md")
TELEPORT_HA = "/root/TELEPORT_HA.md"


def czas_tomasza() -> str:
    return datetime.now(ZoneInfo("Europe/Vienna")).strftime("%d.%m.%Y %H:%M %Z")


def dni_bez_wpisu(sciezka: str) -> float:
    if not os.path.isfile(sciezka):
        return -1.0
    return (datetime.now() - datetime.fromtimestamp(os.path.getmtime(sciezka))).total_seconds() / 86400


def commity(dni: int) -> list:
    """Commity z ostatnich N dni — materiał do wpisu, nie sam wpis."""
    try:
        w = subprocess.run(
            ["git", "log", f"--since={dni} days ago", "--pretty=format:%ad %s",
             "--date=format:%d.%m %H:%M"],
            cwd=REPO, capture_output=True, text=True, timeout=30)
        return [l for l in w.stdout.splitlines() if l.strip()]
    except (subprocess.SubprocessError, OSError):
        return []


def dopisz(tresc: str, sciezka: str) -> None:
    """Dopisek na końcu dziennika. Zawsze z datą, zawsze na końcu."""
    naglowek = f"\n\n{'=' * 78}\n## SESJA {czas_tomasza()}\n{'=' * 78}\n\n"
    with open(sciezka, "a", encoding="utf-8") as f:
        f.write(naglowek + tresc.rstrip() + "\n")
    print(f"[teleport] dopisane do {sciezka} ({len(tresc)} znakow, {czas_tomasza()})")


def main() -> int:
    p = argparse.ArgumentParser(description="Dziennik ciągłości między oknami rozmowy")
    p.add_argument("--wpis", default="", help="treść wpisu: co się wydarzyło")
    p.add_argument("--plik", default="", help="wczytaj treść wpisu z pliku")
    p.add_argument("--ha", action="store_true", help="dopisz do teleportu Home Assistant")
    p.add_argument("--z-gita", type=int, default=0, help="wypisz commity z ostatnich N dni")
    p.add_argument("--sprawdz", action="store_true", help="ile dni bez wpisu")
    a = p.parse_args()

    if a.sprawdz:
        for nazwa, sc in (("fabryka", TELEPORT_FABRYKA), ("Home Assistant", TELEPORT_HA)):
            d = dni_bez_wpisu(sc)
            if d < 0:
                print(f"  {nazwa:16} PLIKU NIE MA: {sc}")
            else:
                ostrzezenie = "  <<< ZALEGŁOŚĆ" if d > 1 else ""
                print(f"  {nazwa:16} bez wpisu: {d:.1f} dnia{ostrzezenie}")
        return 0

    if a.z_gita:
        lista = commity(a.z_gita)
        print(f"  commitow z ostatnich {a.z_gita} dni: {len(lista)}")
        for l in lista[:40]:
            print(f"    {l[:110]}")
        return 0

    tresc = a.wpis
    if a.plik:
        try:
            with open(a.plik, encoding="utf-8", errors="replace") as f:
                tresc = f.read()
        except OSError as e:
            print(f"[teleport] nie moge wczytac {a.plik}: {e}")
            return 1
    if not tresc.strip():
        print("[teleport] pusty wpis — nic nie dopisano")
        return 1

    dopisz(tresc, TELEPORT_HA if a.ha else TELEPORT_FABRYKA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
