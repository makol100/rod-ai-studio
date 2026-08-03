#!/usr/bin/env python3
"""DZWONEK — powiadomienie na Telegram, że coś się skończyło albo wywaliło.

Decyzja Tomasza 01.08.2026:
  „Hans jak powstanie — osobny bot."   -> Hans dostanie WŁASNEGO bota, dopiero gdy powstanie
  „Dzwonki pod Fabryka Rolek."          -> zwykłe powiadomienia idą na ISTNIEJĄCEGO bota
                                            (@HermesDyzurny_Bot), podpisane FABRYKA ROLEK

Powód powstania: Tomasz zapytał „Mam Cię wywołać czy sam się odezwiesz?" — Klaudek nie może
zaczepić go z własnej inicjatywy. Bez dzwonka każdy raport wymaga, żeby Tomasz zapytał pierwszy,
a jego zasada mówi odwrotnie: ma wiedzieć PIERWSZY.

NIE RUSZA bramki Henia (hermes-gateway) — używa wyłącznie tokenu i ID z jego konfiguracji.
Dzięki temu jego dyżur 24/7 nie jest zagrożony.

Użycie:
  python3 tools/dzwonek.py "treść wiadomości"
  python3 tools/dzwonek.py "treść" --tytul "POLOWANIE SKONCZONE"
"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

KONFIGI = (
    "/home/hermes/.hermes/.env",
    "/home/hermes/.hermes/hermes-agent/.env",
)


def wczytaj() -> tuple:
    """Zwraca (token, id_czatu) z konfiguracji bramki Henia. Nic nie zapisuje."""
    token = czat = ""
    for sciezka in KONFIGI:
        try:
            with open(sciezka, encoding="utf-8", errors="replace") as f:
                for linia in f:
                    klucz, _, wartosc = linia.strip().partition("=")
                    wartosc = wartosc.strip().strip('"').strip("'")
                    if klucz == "TELEGRAM_BOT_TOKEN" and wartosc and not token:
                        token = wartosc
                    elif klucz == "TELEGRAM_HOME_CHANNEL" and wartosc and not czat:
                        czat = wartosc
        except OSError:
            continue
    return token, czat


def wyslij(tresc: str, tytul: str = "") -> tuple:
    token, czat = wczytaj()
    if not token or not czat:
        return False, "brak tokenu albo ID czatu w konfiguracji bramki"

    naglowek = f"🔔 FABRYKA ROLEK — {tytul}\n\n" if tytul else "🔔 FABRYKA ROLEK\n\n"
    dane = urllib.parse.urlencode({
        "chat_id": czat,
        "text": (naglowek + tresc)[:4000],
        "disable_web_page_preview": "true",
    }).encode()
    adres = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        with urllib.request.urlopen(urllib.request.Request(adres, data=dane), timeout=25) as o:
            odp = json.load(o)
        return bool(odp.get("ok")), f"message_id={odp.get('result', {}).get('message_id')}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read()[:200].decode(errors='replace')}"
    except Exception as e:  # noqa: BLE001 — dzwonek nie moze wywalic zadania, ktore obwieszcza
        return False, f"{type(e).__name__}: {str(e)[:150]}"


def main() -> int:
    p = argparse.ArgumentParser(description="Dzwonek na Telegram (Fabryka Rolek)")
    p.add_argument("tresc", help="co napisać Tomaszowi")
    p.add_argument("--tytul", default="", help="krótki nagłówek, np. POLOWANIE SKONCZONE")
    a = p.parse_args()
    ok, slad = wyslij(a.tresc, a.tytul)
    print(("[dzwonek] wyslane: " if ok else "[dzwonek] NIE WYSLANE: ") + slad)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
