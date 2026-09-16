#!/usr/bin/env python3
"""Zrzut strony headless Chrome (Playwright) + wysyłka na Telegram do Tomasza.

Dekret 03.09.2026: „Masz całą fabrykę na VPS to wejdź i zrób" — zrzut robimy
z VPS i ślemy Tomaszowi, zamiast kazać mu odświeżać telefon.

Użycie:
  python3 tools/zrzut_strony.py URL [--plik out.png] [--pulpit] [--caly]
                                [--podpis "tekst"] [--bez-wysylki]
Domyślnie widok telefonu (412x915, jak Fold7 zewn.), zrzut widocznej części.
--caly = pełna wysokość strony. Headless ma zawsze pusty cache (lekcja z teczki).
"""
import argparse
import sys
import urllib.request
from pathlib import Path


def zrzut(url: str, plik: Path, pulpit: bool, caly: bool) -> None:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        vp = {"width": 1280, "height": 900} if pulpit else {"width": 412, "height": 915}
        page = browser.new_page(viewport=vp, device_scale_factor=2)
        page.goto(url, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1200)  # pogoda/liczniki dociągają się JS-em
        page.screenshot(path=str(plik), full_page=caly)
        browser.close()


def wyslij_tomaszowi(plik: Path, podpis: str) -> bool:
    token = chat = ""
    with open("/home/hermes/.hermes/.env", encoding="utf-8", errors="replace") as f:
        for linia in f:
            k, _, w = linia.strip().partition("=")
            w = w.strip().strip('"').strip("'")
            if k == "HANS_BOT_TOKEN":
                token = w
            elif k == "HANS_CHAT_ID":
                chat = w
    if not token or not chat:
        print("BRAK tokena/chat_id Hansa", file=sys.stderr)
        return False
    granica = "----zrzut"
    dane = plik.read_bytes()
    cialo = (
        f"--{granica}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat}\r\n"
        f"--{granica}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{podpis}\r\n"
        f"--{granica}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{plik.name}\"\r\n"
        f"Content-Type: image/png\r\n\r\n"
    ).encode() + dane + f"\r\n--{granica}--\r\n".encode()
    def _post(metoda: str, pole: str) -> bool:
        c = cialo.replace(b'name="photo"', f'name="{pole}"'.encode())
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/{metoda}", data=c,
            headers={"Content-Type": f"multipart/form-data; boundary={granica}"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return b'"ok":true' in r.read()
        except urllib.error.HTTPError as e:
            print(f"{metoda}: HTTP {e.code}", file=sys.stderr)
            return False

    # sendPhoto odrzuca obrazy o sumie wymiarow > ~10000 px (pelne zrzuty stron)
    ok = _post("sendPhoto", "photo") or _post("sendDocument", "document")
    print("wysylka:", "OK" if ok else "BLAD")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--plik", default="/tmp/zrzut.png")
    ap.add_argument("--pulpit", action="store_true")
    ap.add_argument("--caly", action="store_true")
    ap.add_argument("--podpis", default="")
    ap.add_argument("--bez-wysylki", action="store_true")
    a = ap.parse_args()
    plik = Path(a.plik)
    zrzut(a.url, plik, a.pulpit, a.caly)
    print(f"zrzut: {plik} ({plik.stat().st_size} B)")
    if not a.bez_wysylki:
        return 0 if wyslij_tomaszowi(plik, a.podpis or a.url) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
