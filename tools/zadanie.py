#!/usr/bin/env python3
"""URUCHOM DOWOLNE DLUGIE ZADANIE I ZAMELDUJ TOMASZOWI WYNIK.

Powstalo 5.08.2026 na wniosek HENIA (narada „czego fabryce brakuje").
Henio wskazal bolaczke nr 6 jako najwazniejsza i uzasadnil:
  „Tomasz jest jedynym decydentem. Pracuje z telefonu, w biegu, poza domem.
   Kazde »juz?«, »co jest?« to jego czas i uwaga wyjete z kontekstu."
Zmierzyl tez, ze `odpal.py` dzwoni WYLACZNIE po naradach — kazde inne dlugie zadanie
(generowanie, montaz, wyciecie tla, kopia, instalacja) konczy sie w ciszy.
Nazwal to tym samym bledem, ktory Klaudek juz popelnil: funkcje przywrocono w JEDNYM miejscu.

CZYM SIE ROZNI OD odpal.py:
  odpal.py  — tylko narady zalogi (zaloga.py)
  zadanie.py — DOWOLNE polecenie powloki

DWIE RZECZY, KTORYCH PILNUJE:
1. NIE TRZYMA POLACZENIA MCP. Wraca natychmiast (most zrywa 21 razy na dobe — 5.08).
2. DZWONI ZAWSZE. Sukces i porazka tak samo. Cisza po dlugim zadaniu jest bledem.

Uzycie:
  python3 tools/zadanie.py --nazwa "Wyciecie Izabeli" --polecenie "python3 tools/wytnij_izabele.py ..."
  python3 tools/zadanie.py --stan
  python3 tools/zadanie.py --stan --nazwa "Wyciecie Izabeli"
"""
import argparse
import json
import subprocess
import time
from pathlib import Path

REPO = Path("/root/rod-ai-studio")
KATALOG = Path("/tmp/zadania")
DZWONEK = REPO / "tools/dzwonek.py"


def _slug(nazwa):
    return "".join(c if c.isalnum() else "_" for c in nazwa.lower())[:40]


def odpal(nazwa, polecenie, limit_sekund=1800):
    KATALOG.mkdir(parents=True, exist_ok=True)
    s = _slug(nazwa)
    log = KATALOG / f"{s}.log"
    stan = KATALOG / f"{s}.json"

    # Powloka: uruchom -> zapisz kod wyjscia -> ZAWSZE zadzwon.
    # Dzwonek jest WEWNATRZ powloki, nie doklejany przez wolajacego — zeby nie dalo sie
    # go zgubic przy nastepnym przepisywaniu narzedzia (lekcja z 5.08).
    # BLAD ZNALEZIONY PRZY TESCIE 5.08: polecenie ze srednikiem (np. "sleep 3; exit 7")
    # ROZRYWALO cala konstrukcje — druga czesc wykonywala sie POZA nasza powloka,
    # wiec kod wyjscia nie byl zapisany i DZWONEK NIE DZWONIL.
    # Naprawa: polecenie idzie do osobnego pliku i jest uruchamiane jako calosc.
    skrypt = KATALOG / f"{s}.sh"
    skrypt.write_text(f"#!/bin/bash\ncd {REPO}\n{polecenie}\n", encoding="utf-8")
    skrypt.chmod(0o755)

    powloka = (
        f"cd {REPO} && "
        f"timeout {limit_sekund} bash {skrypt} >> {log} 2>&1; "
        f"K=$?; "
        f"python3 -c \"import json,time;json.dump({{'nazwa':'''{nazwa}''','kod':$K,"
        f"'koniec':time.time()}},open('{stan}','w'))\"; "
        f"if [ $K -eq 0 ]; then W='GOTOWE'; else W=\"BLAD (kod $K)\"; fi; "
        f"python3 {DZWONEK} \"$W: {nazwa}. Log: {log}\" --tytul \"{nazwa[:40]}\" >> {log} 2>&1"
    )

    p = subprocess.Popen(["bash", "-lc", powloka], cwd=str(REPO),
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
    stan.write_text(json.dumps({"nazwa": nazwa, "pid": p.pid, "start": time.time(),
                                "polecenie": polecenie, "kod": None}), encoding="utf-8")
    print(f"odpalone pid={p.pid} | {nazwa} | log: {log}")


def pokaz_stan(nazwa=None):
    KATALOG.mkdir(parents=True, exist_ok=True)
    pliki = sorted(KATALOG.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    if nazwa:
        pliki = [p for p in pliki if p.stem == _slug(nazwa)]
    if not pliki:
        print("brak zadan")
        return
    for p in pliki[:6]:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        kod = d.get("kod")
        if kod is None:
            minelo = int(time.time() - d.get("start", time.time()))
            zyje = subprocess.run(["kill", "-0", str(d.get("pid", 0))],
                                  capture_output=True).returncode == 0
            print(f"  [{'pracuje' if zyje else 'PRZERWANE'}] {d['nazwa']} — {minelo // 60}m{minelo % 60}s")
        else:
            print(f"  [{'gotowe' if kod == 0 else f'BLAD {kod}'}] {d['nazwa']}")


if __name__ == "__main__":
    a = argparse.ArgumentParser(description="Uruchom dlugie zadanie z meldunkiem dla Tomasza")
    a.add_argument("--nazwa")
    a.add_argument("--polecenie")
    a.add_argument("--limit", type=int, default=1800)
    a.add_argument("--stan", action="store_true")
    args = a.parse_args()

    if args.stan:
        pokaz_stan(args.nazwa)
    elif args.nazwa and args.polecenie:
        odpal(args.nazwa, args.polecenie, args.limit)
    else:
        a.error("podaj --nazwa i --polecenie albo --stan")
