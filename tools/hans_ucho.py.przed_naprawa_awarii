#!/usr/bin/env python3
"""Ucho Hansa: dopisuje wiadomosci Tomasza z Telegrama do jego slow."""

from __future__ import annotations

import os
import sys
import time
import json
import argparse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import requests

KONFIGI_HANS = (
    "/home/hermes/.hermes/.env",
    "/home/hermes/.hermes/hermes-agent/.env",
)
STREFA_TOMASZA = ZoneInfo("Europe/Vienna")


def _wczytaj_token_hansa() -> tuple[str, str]:
    """Zwraca (token, chat_id) dla bota Hansa z plikow .env. Wzor: tools/hans.py."""
    token = czat = ""
    for sciezka in KONFIGI_HANS:
        try:
            with open(sciezka, encoding="utf-8", errors="replace") as f:
                for linia in f:
                    klucz, _, wartosc = linia.strip().partition("=")
                    wartosc = wartosc.strip().strip('"').strip("'")
                    if klucz == "HANS_BOT_TOKEN" and wartosc and not token:
                        token = wartosc
                    elif klucz == "HANS_CHAT_ID" and wartosc and not czat:
                        czat = wartosc
        except OSError:
            continue
    return token, czat


def _pobierz_slowa_path() -> Path:
    return Path(os.environ.get("HANS_SLOWA_PATH", "wiedza/SLOWA_TOMASZA.md"))


def _pobierz_offset_path() -> Path:
    return Path(os.environ.get("HANS_OFFSET_PATH", ".scratch/hans/ucho_offset.json"))


def _wczytaj_offset(sciezka: Path) -> int:
    try:
        if not sciezka.exists():
            return -1
        dane = json.loads(sciezka.read_text(encoding="utf-8"))
        return int(dane.get("offset", -1))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return -1


def _zapisz_offset(offset: int, sciezka: Path) -> None:
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    tymczasowy = sciezka.with_suffix(sciezka.suffix + ".tmp")
    tymczasowy.write_text(
        json.dumps({"offset": offset}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    tymczasowy.replace(sciezka)


def _dopisz_doslownie(tekst: str, epoch: int | float, sciezka: Path) -> None:
    chwila = datetime.fromtimestamp(epoch, STREFA_TOMASZA)
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    with sciezka.open("a", encoding="utf-8") as plik:
        plik.write(f"\n## {chwila:%d.%m.%Y %H:%M:%S} (Europe/Vienna) — Telegram\n\n")
        plik.write(tekst)
        plik.write("\n")


def uruchom_ucho(token: str | None = None, chat_id: str | None = None) -> bool:
    """Główna funkcja odpytująca Telegram i zapisująca słowa Tomasza."""
    # 1. Uzgodnienie danych uwierzytelniających
    env_token, env_chat_id = _wczytaj_token_hansa()
    token = token or os.environ.get("HANS_BOT_TOKEN") or env_token
    chat_id = chat_id or os.environ.get("HANS_CHAT_ID") or env_chat_id

    if not token or not chat_id:
        print("Hans ucho: brak tokenu lub chat_id.", file=sys.stderr)
        return False

    slowa_path = _pobierz_slowa_path()
    offset_path = _pobierz_offset_path()

    offset = _wczytaj_offset(offset_path)

    # 2. Odpytanie Telegram getUpdates przy użyciu requests
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {"offset": offset + 1, "timeout": 20}
    try:
        res = requests.get(url, params=params, timeout=25)
        res.raise_for_status()
        dane = res.json()
    except Exception as e:
        print(f"Hans ucho: Błąd połączenia lub odpowiedzi z Telegrama: {e}", file=sys.stderr)
        return True

    if not dane.get("ok") or not isinstance(dane.get("result"), list):
        print(f"Hans ucho: Telegram getUpdates zwrócił błąd lub wadliwy format: {dane}", file=sys.stderr)
        return True

    wyniki = dane["result"]
    dopisane = 0
    ostatni_offset = offset

    for aktualizacja in sorted(wyniki, key=lambda x: int(x.get("update_id", -1))):
        up_id = int(aktualizacja.get("update_id", -1))
        if up_id <= offset:
            continue

        wiadomosc = aktualizacja.get("message")
        if not isinstance(wiadomosc, dict):
            wiadomosc = aktualizacja.get("edited_message")

        if isinstance(wiadomosc, dict):
            czat = wiadomosc.get("chat", {})
            nadawca = wiadomosc.get("from", {})
            id_czatu = str(czat.get("id"))
            id_nadawcy = str(nadawca.get("id"))

            tekst = wiadomosc.get("text")
            if tekst is None:
                tekst = wiadomosc.get("caption")

            # Przechwytujemy wiadomości, jeśli chat_id lub from_id pasuje do Tomasza
            if (id_czatu == str(chat_id) or id_nadawcy == str(chat_id)) and isinstance(tekst, str):
                _dopisz_doslownie(tekst, wiadomosc.get("date", time.time()), slowa_path)
                dopisane += 1

        ostatni_offset = up_id
        _zapisz_offset(ostatni_offset, offset_path)

    if dopisane > 0 or wyniki:
        print(f"Hans ucho: odebrano {len(wyniki)} wpisów, dopisano {dopisane} nowych słów Tomasza.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    tryb = parser.add_mutually_exclusive_group(required=True)
    tryb.add_argument("--raz", action="store_true", help="jedno odpytanie Telegrama")
    tryb.add_argument("--petla", type=float, metavar="N", help="odpytuj co N sekund")
    args = parser.parse_args()

    if args.petla is not None and args.petla <= 0:
        parser.error("N dla --petla musi być większe od zera")

    if args.raz:
        uruchom_ucho()
        return 0

    try:
        while True:
            uruchom_ucho()
            time.sleep(args.petla)
    except KeyboardInterrupt:
        print("Hans ucho: zatrzymane.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
