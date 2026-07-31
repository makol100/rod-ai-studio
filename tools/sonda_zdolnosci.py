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
import time

_MODEL_GENKA = None
REPO = "/root/rod-ai-studio"
STAN = os.path.join(REPO, "wiedza/srodowiska/_stan_zdolnosci.json")


PRZEJSCIOWE = (
    "reason: undefined", "[object Object]", "critical error occurred","503", "429", "overloaded", "rate limit", "quota", "unavailable",
               "timed out", "przekroczony czas", "temporarily")


def model_genka() -> str:
    """Zwraca pierwszy model z kolejki Genka, ktory FAKTYCZNIE odpowiada.
    Dekret Tomasza 30.07: "Genek ma zostac na najwyzszym WOLNYM dla nas modelu zawsze"."""
    global _MODEL_GENKA
    if _MODEL_GENKA is not None:
        return _MODEL_GENKA
    for m in ("gemini-3.1-pro-preview", "gemini-3.6-flash"):  # 3.5-flash usuniety: brak w wiedzy (Zenek)
        _, o = polecenie(
            f"timeout 80 env GEMINI_CLI_TRUST_WORKSPACE=true gemini --yolo -m {m} "
            f"-p 'Napisz OK' 2>&1 | grep -oE 'OK|503|429' | head -1", limit=110)
        if "OK" in o:
            _MODEL_GENKA = m
            return m
    _MODEL_GENKA = ""
    return ""


def czy_przejsciowy(opis: str) -> bool:
    # 30.07: Gemini CLI potrafi zwrocic "reason: undefined" / "[object Object]" i zaraz potem
    # dzialac normalnie. To czkawka dostawcy, nie utrata zdolnosci — nie moze blokowac zalogi.
    """Awaria u dostawcy to NIE utrata zdolnosci. Bez tego rozroznienia czkawka Google
    blokowala cala prace przez bramke rownych szans (znalezione testem 29.07)."""
    n = opis.lower()
    return any(t in n for t in PRZEJSCIOWE)


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

    # ZENEK — czy ma siec w piaskownicy (29.07: DNS byl odciety, milczaco).
    # Sonda pisze ZNACZNIK DO PLIKU zamiast szukac liczby w gadatliwym wyjsciu codeksa —
    # pierwsza wersja dawala falszywy alarm i przez bramke rownych szans blokowala CALA prace.
    znacznik = os.path.join(REPO, ".scratch", "_sonda_zenek_siec.txt")
    if os.path.isfile(znacznik):
        os.remove(znacznik)
    polecenie(
        f"cd {REPO} && timeout 120 codex exec \"Uruchom dokladnie to polecenie i nic wiecej: "
        f"python3 -c \\\"import urllib.request,pathlib;"
        f"k=urllib.request.urlopen('https://api.github.com',timeout=10).status;"
        f"pathlib.Path('.scratch/_sonda_zenek_siec.txt').write_text(str(k))\\\"\" >/dev/null 2>&1",
        limit=160)
    tresc = ""
    if os.path.isfile(znacznik):
        tresc = open(znacznik, encoding="utf-8", errors="replace").read().strip()
    wynik["zenek.siec"] = {"dziala": tresc == "200",
                           "slad": f"znacznik: {tresc or 'BRAK PLIKU'}"}

    # GENEK — czy CLI czyta dysk i czy potrafi ZAPISAC (to bylo cicho stracone).
    # Trzy podejscia: 503/429 od Google to czkawka, nie utrata zdolnosci.
    _stary = os.path.join(REPO, ".scratch/_sonda.txt")
    if os.path.exists(_stary):       # Zenek: pozostalosc po przerwanym przebiegu dawala FALSZYWE TAK
        os.remove(_stary)
    for _ in range(3):
        ok, opis = polecenie(
        f"cd {REPO} && GEMINI_CLI_TRUST_WORKSPACE=true timeout 120 gemini --yolo -m {model_genka() or 'gemini-3.6-flash'} -p "
            "'Utworz plik .scratch/_sonda.txt z trescia OK, potem odczytaj go i napisz TYLKO jego zawartosc.' "
            "2>&1 | tail -3", limit=150)
        if os.path.isfile(os.path.join(REPO, ".scratch/_sonda.txt")):
            break
        if not czy_przejsciowy(opis):
            break
        time.sleep(6)
    plik = os.path.join(REPO, ".scratch/_sonda.txt")
    zapisal = os.path.isfile(plik)
    wynik["genek.dysk_zapis"] = {"dziala": zapisal,
                                 "slad": ("plik powstal" if zapisal else
                                          ("CHWILOWA AWARIA U DOSTAWCY: " + opis[:80]
                                           if czy_przejsciowy(opis) else opis[:120]))}
    if zapisal:
        os.remove(plik)

    # GENEK — czy KTORYKOLWIEK model z kolejki odpowiada (dekret Tomasza 30.07: "najwyzszy WOLNY").
    # Sztywne pytanie o 3.1-pro blokowalo cala zaloge, gdy wyczerpal sie jego dobowy limit 250 zapytan,
    # mimo ze 3.6-flash byl wolny i czytal dysk.
    m_dostepny = model_genka()
    # Zenek: wzorzec zapisywal tylko "dziala", wiec zejscie pro->flash NIE bylo zmiana stanu.
    # Teraz nazwa modelu jest czescia stanu — zejscie zobaczysz w porannym meldunku.
    # Dekret Tomasza: "najwyzszy WOLNY dla nas model". Praca na flashu, gdy pro ma wyczerpany limit
    # dobowy, JEST zgodna z dekretem — wiec nie blokuje. Ale MUSI byc widoczna, stad druga linia.
    wynik["genek.model"] = {"dziala": bool(m_dostepny),
                            "slad": f"pracuje na: {m_dostepny or 'ZADEN model z kolejki nie odpowiada'}"}
    if m_dostepny and m_dostepny != "gemini-3.1-pro-preview":
        print(f"  (i) GENEK NIE JEST NA MODELU DOCELOWYM: pracuje na {m_dostepny}, "
              f"bo gemini-3.1-pro-preview nie odpowiada (dobowy limit Tier 1 = 250 zapytan)")

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

    # TELEFON — apka Android Remote Control bywa ubijana przez Androida (29.07: martwa, gdy byla potrzebna)
    ok, opis = polecenie(
        "curl -s -o /dev/null -w '%{http_code}' -m 10 http://100.101.116.106:8080/ || true", limit=25)
    wynik["telefon.apka"] = {"dziala": opis.strip() not in ("000", "", "502"),
                             "slad": f"http://100.101.116.106:8080 -> {opis.strip() or 'brak odpowiedzi'}"}

    # WSPOLNA DROGA ZAPASOWA DO SIECI — zeby awaria jednego dostawcy nie odcinala calej zalogi
    ok, opis = polecenie(
        f"cd {REPO} && timeout 120 python3 tools/szukaj_net.py --tylko-zapasowo 'test' 2>&1 | head -4", limit=160)
    wynik["siec.zapasowa"] = {"dziala": "ZAPASOWA" in opis and "BLAD" not in opis, "slad": opis[:90]}

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

    roznice, nowosci = [], []
    for k, v in teraz.items():
        oczekiwane = wzorzec.get(k)
        if oczekiwane is None:
            # 30.07: NOWA zdolnosc to ULEPSZENIE, nie awaria — nie moze blokowac pracy zalogi.
            # (Zablokowala narade o modelu Genka, bo dopisalem druga droge do sieci.)
            nowosci.append(f"NOWA ZDOLNOSC {k}: {'TAK' if v['dziala'] else 'NIE'} — dopisz wzorzec: --zapisz")
        elif oczekiwane != v["dziala"]:
            kierunek = "STRACONE" if oczekiwane else "ODZYSKANE"
            wpis = (f"{kierunek}: {k} (bylo {'TAK' if oczekiwane else 'NIE'}, "
                    f"jest {'TAK' if v['dziala'] else 'NIE'}) | {v['slad']}")
            # ODZYSKANIE tez nie jest awaria — informujemy, nie blokujemy
            (roznice if kierunek == "STRACONE" else nowosci).append(wpis)
    for k in wzorzec:
        if k not in teraz:
            roznice.append(f"ZNIKNELA SONDA: {k}")

    for n in nowosci:
        print(f"  (i) {n}")
    if not roznice:
        return 0
    print("SONDA ZDOLNOSCI — ZMIANA STANU ZALOGI")
    for r in roznice:
        print(f"  !!! {r}")
    print("\nKarty w wiedza/srodowiska/ moga byc juz nieaktualne. Sprawdzic i poprawic.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
