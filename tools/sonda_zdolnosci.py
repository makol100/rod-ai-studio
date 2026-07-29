#!/usr/bin/env python3
"""sonda_zdolnosci.py — codzienna sonda REALNYCH mozliwosci zalogi.

Powstala 29.07.2026, bo dwa razy tego samego dnia Klaudek zameldowal Tomaszowi stan, ktorego nie zmierzyl:
"Henio ma przegladarke" (czytal liste wlaczonych toolsetow zamiast sprawdzic sesje) i "Genek nie ma dysku"
(powtarzal wlasne obejscie sprzed tygodnia jako fakt o Genku).

Zasada: NIE PYTA nikogo o samoocene. Sprawdza mechanicznie, czy droga dziala, i porownuje ze stanem
zapisanym w wiedza/srodowiska/_stan_zdolnosci.json. Kazda ROZNICA to alarm — bo znaczy, ze ktos po cichu
stracil albo zyskal zdolnosc, a karty srodowisk klamia.

Uzycie:
    python3 tools/sonda_zdolnosci.py           # sonda + porownanie, alarm na roznicy
    python3 tools/sonda_zdolnosci.py --zapisz  # przyjmij obecny stan jako wzorzec

Wyjscie 0 = bez zmian. Wyjscie 1 = ROZNICA (na cronie: to trafia na Telegram).
Fail-closed: kazdy blad sondy = zdolnosc raportowana jako NIE, nigdy jako "pewnie dziala".
"""
import argparse
import json
import os
import subprocess
import sys

REPO = "/root/rod-ai-studio"
STAN = os.path.join(REPO, "wiedza/srodowiska/_stan_zdolnosci.json")


def polecenie(cmd: str, limit: int = 60, jako: str = "") -> tuple:
    """Uruchamia polecenie, zwraca (czy_ok, pierwsze_linie_wyjscia)."""
    pelne = ["su", "-", jako, "-c", cmd] if jako else ["bash", "-lc", cmd]
    try:
        w = subprocess.run(pelne, capture_output=True, text=True, timeout=limit)
        return w.returncode == 0, (w.stdout or w.stderr).strip()[:160]
    except Exception as e:
        return False, f"blad sondy: {e}"


def sonda() -> dict:
    wynik = {}

    # ZENEK — czy CLI istnieje i odpala sie w katalogu repo
    ok, opis = polecenie("command -v codex >/dev/null && echo JEST")
    wynik["zenek.cli"] = {"dziala": ok and "JEST" in opis, "slad": opis}

    # GENEK — czy CLI czyta dysk i czy potrafi ZAPISAC (to bylo cicho stracone)
    ok, opis = polecenie(
        f"cd {REPO} && GEMINI_CLI_TRUST_WORKSPACE=true timeout 120 gemini --yolo -p "
        "'Utworz plik .scratch/_sonda.txt z trescia OK, potem odczytaj go i napisz TYLKO jego zawartosc.' "
        "2>&1 | tail -3", limit=150)
    plik = os.path.join(REPO, ".scratch/_sonda.txt")
    zapisal = os.path.isfile(plik)
    wynik["genek.dysk_zapis"] = {"dziala": zapisal, "slad": opis if not zapisal else "plik powstal"}
    if zapisal:
        os.remove(plik)

    # GENEK — klucz do API (droga awaryjna)
    wynik["genek.klucz"] = {"dziala": os.path.isfile("/root/.gemini/.env"), "slad": "/root/.gemini/.env"}

    # HENIO — gateway zyje i ma zadania cykliczne
    ok, opis = polecenie("export XDG_RUNTIME_DIR=/run/user/1000; hermes cron status 2>&1 | head -3",
                         jako="hermes")
    wynik["henio.gateway"] = {"dziala": "running" in opis.lower(), "slad": opis[:100]}

    # HENIO — zapis w repo bez sudo (ACL)
    ok, opis = polecenie(f"touch {REPO}/.scratch/_sonda_henio && rm {REPO}/.scratch/_sonda_henio && echo OK",
                         jako="hermes")
    wynik["henio.zapis_repo"] = {"dziala": ok and "OK" in opis, "slad": opis[:100]}

    # HENIO — oczy przez polecenie (jego silnik nie przyjmuje obrazow)
    wynik["henio.oczy"] = {"dziala": os.path.isfile(os.path.join(REPO, "tools/oczy_uszy.py"))
                           and os.path.isfile("/home/hermes/.gemini/.env"),
                           "slad": "tools/oczy_uszy.py + wlasny klucz"}

    # HENIO — wyszukiwarka przez polecenie (nie ma web_search w sesji)
    wynik["henio.internet"] = {"dziala": os.path.isfile(os.path.join(REPO, "tools/szukaj_net.py")),
                               "slad": "tools/szukaj_net.py"}

    # WSPOLNE — bramka i jej petla testowa
    ok, opis = polecenie(f"cd {REPO} && python3 tools/test_bramki.py 2>&1 | tail -1", limit=180)
    wynik["bramka.petla"] = {"dziala": ok and "0 czerwonych" in opis, "slad": opis[:100]}
    return wynik


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--zapisz", action="store_true", help="przyjmij obecny stan jako wzorzec")
    a = p.parse_args()

    teraz = sonda()
    if a.zapisz or not os.path.isfile(STAN):
        with open(STAN, "w", encoding="utf-8") as f:
            json.dump({k: v["dziala"] for k, v in teraz.items()}, f, indent=1, ensure_ascii=False)
        print("WZORZEC ZAPISANY:")
        for k, v in teraz.items():
            print(f"  {'TAK' if v['dziala'] else 'NIE'}  {k}")
        return 0

    with open(STAN, encoding="utf-8") as f:
        wzorzec = json.load(f)

    roznice = []
    for k, v in teraz.items():
        oczekiwane = wzorzec.get(k)
        if oczekiwane is None:
            roznice.append(f"NOWA ZDOLNOSC {k}: {'TAK' if v['dziala'] else 'NIE'}")
        elif oczekiwane != v["dziala"]:
            kierunek = "STRACONE" if oczekiwane else "ODZYSKANE"
            roznice.append(f"{kierunek}: {k} (bylo {'TAK' if oczekiwane else 'NIE'}, "
                           f"jest {'TAK' if v['dziala'] else 'NIE'}) | {v['slad']}")
    for k in wzorzec:
        if k not in teraz:
            roznice.append(f"ZNIKNELA SONDA: {k}")

    if not roznice:
        return 0
    print("SONDA ZDOLNOSCI — ZMIANA STANU ZALOGI")
    for r in roznice:
        print(f"  !!! {r}")
    print("\nKarty w wiedza/srodowiska/ moga byc juz nieaktualne. Sprawdzic i poprawic.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
