#!/usr/bin/env python3
"""ODPAL ZLECENIE DLA ZALOGI I NATYCHMIAST PUSC POLACZENIE.

Powod (ustalone 5.08.2026 pomiarem dziennika caddy-mcp):
most Anthropic <-> VPS zrywa polaczenia komunikatem „aborting with incomplete response"
przy czasie 0,003 s — 21 takich zerwan w ciagu doby, rozrzuconych po calym dniu.
Zrywa STRONA ANTHROPICA (adres 160.79.106.x), nie serwer: mcp-fabryka ma zero restartow,
zero bledow wlasnych, 27 dni pracy.

Naprawic tego z naszej strony NIE DA SIE. Ale da sie zmniejszyc skutki:
Klaudek do tej pory odpalal zlecenie i TRZYMAL polaczenie przez `sleep 20-25`, czekajac az ruszy.
Kazda taka sekunda to okazja do zerwania — a zerwanie w trakcie oznacza, ze Klaudek NIE WIE,
czy zlecenie wystartowalo.

To narzedzie odpala i wraca NATYCHMIAST (ponizej sekundy). Stan sprawdza sie osobnym,
krotkim wywolaniem: --stan
"""
import argparse
import json
import os
import subprocess
import time
from pathlib import Path

KATALOG = Path("/root/rod-ai-studio")
ZNACZNIK = Path("/tmp/zaloga_biezace.json")


def odpal(zadanie, kto, katalog, wykonanie=False):
    Path(katalog).mkdir(parents=True, exist_ok=True)
    polecenie = [
        "python3", str(KATALOG / "tools/zaloga.py"),
        "--zadanie", zadanie,
        "--kto", kto,
        "--katalog", katalog,
        "--mimo-braku",
    ]
    if wykonanie:
        polecenie.append("--wykonanie")

    log = f"{katalog}/_przebieg.log"
    with open(log, "w") as f:
        p = subprocess.Popen(
            ["timeout", "1500"] + polecenie,
            cwd=str(KATALOG), stdout=f, stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    ZNACZNIK.write_text(json.dumps({
        "pid": p.pid,
        "katalog": katalog,
        "kto": kto,
        "zadanie": zadanie,
        "start": time.time(),
    }), encoding="utf-8")
    print(f"odpalone pid={p.pid} katalog={katalog} kto={kto}")


def stan():
    if not ZNACZNIK.exists():
        print("brak biezacego zlecenia")
        return
    z = json.loads(ZNACZNIK.read_text(encoding="utf-8"))
    minelo = int(time.time() - z["start"])
    kat = Path(z["katalog"])
    oczekiwani = [k.strip() for k in z["kto"].split(",") if k.strip()]

    gotowi, brak = [], []
    for k in oczekiwani:
        p = kat / f"{k}.txt"
        if p.exists() and p.stat().st_size > 0:
            tresc = p.read_text(encoding="utf-8", errors="replace")[:120]
            gotowi.append(f"{k}({'NIEODEBRANY' if 'NIEODEBRANY' in tresc else str(p.stat().st_size) + 'B'})")
        else:
            brak.append(k)

    zyje = subprocess.run(["pgrep", "-f", "zaloga.py"], capture_output=True).returncode == 0
    print(f"minelo {minelo // 60}m{minelo % 60}s | proces: {'pracuje' if zyje else 'zakonczony'}")
    print(f"gotowe: {', '.join(gotowi) if gotowi else 'brak'}")
    if brak:
        print(f"czekam na: {', '.join(brak)}")


if __name__ == "__main__":
    a = argparse.ArgumentParser(description="Odpal zlecenie zalogi bez trzymania polaczenia")
    a.add_argument("--zadanie")
    a.add_argument("--kto", default="zenek,henio")
    a.add_argument("--katalog")
    a.add_argument("--wykonanie", action="store_true")
    a.add_argument("--stan", action="store_true")
    args = a.parse_args()

    if args.stan:
        stan()
    elif args.zadanie and args.katalog:
        odpal(args.zadanie, args.kto, args.katalog, args.wykonanie)
    else:
        a.error("podaj --zadanie i --katalog albo --stan")
