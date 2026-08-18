#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/film.py — fabryka umie czytac filmy z YouTube.

POWSTALO 17.08.2026 na polecenie Tomasza: "To jest problem ze nie znacie tresci
filmu!!!! Zebrac grupe bez Gienka i wszyscy macie tak zrobic zebyscie umieli".

Przyjmuje URL, zwraca TRANSKRYPCJE jako czysty tekst. Probuje kolejnych drog,
melduje ktora zadzialala i dlaczego pozostale nie. Nie wysyla nic do platnych modeli.

DROGI (w kolejnosci prob):
  1. yt-dlp + node + ciasteczka  — jedyna PEWNA wg pomiaru Henia 17.08
  2. yt-dlp + node bez ciasteczek — dziala z IP domowego, NIE z centrum danych
  3. youtube-transcript-api       — blokowane z IP centrum danych (RequestBlocked)
  4. Invidious                    — instancje masowo bez API w 2026, VTT bywa puste

POMIARY Z 17.08 (Henio, na tym VPS):
  - node v22.23.1 JEST; --js-runtimes node usuwa blad EJS
  - bez ciasteczek KAZDA droga pada: yt-dlp bot-check, transcript-api RequestBlocked,
    Invidious puste VTT, Piped 502
  - przyczyna: IP Hetznera to centrum danych, YouTube blokuje je na sztywno

CIASTECZKA: plik w formacie Netscape, chmod 600, POZA repozytorium.
Domyslnie /root/.sekrety/youtube_cookies.txt — to dostep do konta Google Tomasza,
wiec NIGDY nie trafia do gita, do wiedza/, do logow ani do meldunkow.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

CIASTKA_DOMYSLNE = "/root/.sekrety/youtube_cookies.txt"
WYNIKI = Path("/root/rod-ai-studio/.scratch/filmy")


def id_filmu(url: str) -> str:
    for wzor in (r"youtu\.be/([A-Za-z0-9_-]{11})",
                 r"[?&]v=([A-Za-z0-9_-]{11})",
                 r"/embed/([A-Za-z0-9_-]{11})",
                 r"/shorts/([A-Za-z0-9_-]{11})"):
        m = re.search(wzor, url)
        if m:
            return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url
    raise SystemExit(f"BLAD: nie rozpoznaje ID filmu w '{url}'")


def vtt_na_tekst(vtt: str) -> str:
    """Usuwa znaczniki czasu i duplikaty z napisow automatycznych."""
    linie, poprzednia = [], None
    for l in vtt.splitlines():
        l = l.strip()
        if (not l or l.startswith("WEBVTT") or "-->" in l
                or l.startswith(("Kind:", "Language:", "NOTE")) or l.isdigit()):
            continue
        l = re.sub(r"<[^>]+>", "", l).strip()
        if l and l != poprzednia:
            linie.append(l)
            poprzednia = l
    return "\n".join(linie)


def tytul(url: str, ciastka: str | None) -> str:
    try:
        with urllib.request.urlopen(
                f"https://www.youtube.com/oembed?url={url}&format=json", timeout=20) as r:
            return json.load(r).get("title", "")
    except Exception:
        return ""


def droga_ytdlp(url: str, vid: str, ciastka: str | None, kat: Path) -> tuple[str, str]:
    """Zwraca (tekst, opis_drogi) albo ('', powod_niepowodzenia)."""
    cel = kat / vid
    cmd = ["yt-dlp", "--js-runtimes", "node", "--skip-download",
           "--write-auto-subs", "--write-subs", "--sub-langs", "pl,pl-orig,en,en-orig",
           "--sub-format", "vtt", "--write-description",
           "-o", str(cel) + ".%(ext)s", url]
    if ciastka:
        cmd[1:1] = ["--cookies", ciastka]
    w = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    pliki = sorted(kat.glob(f"{vid}*.vtt"))
    if pliki:
        tekst = vtt_na_tekst(pliki[0].read_text(encoding="utf-8", errors="replace"))
        if tekst.strip():
            return tekst, f"yt-dlp + node{' + ciasteczka' if ciastka else ''} ({pliki[0].name})"
    blad = (w.stderr or w.stdout or "").strip().splitlines()
    return "", (blad[-1][:300] if blad else "brak napisow w odpowiedzi")


def droga_transcript_api(vid: str) -> tuple[str, str]:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
    except ImportError:
        return "", "biblioteka youtube-transcript-api nie zainstalowana"
    try:
        api = YouTubeTranscriptApi()
        for jez in (["pl"], ["en"], None):
            try:
                dane = api.fetch(vid, languages=jez) if jez else api.fetch(vid)
                return "\n".join(f.text for f in dane if f.text.strip()), "youtube-transcript-api"
            except Exception:
                continue
        return "", "brak napisow w zadnym jezyku"
    except Exception as e:
        return "", f"{type(e).__name__}: {str(e)[:200]}"


def droga_invidious(vid: str) -> tuple[str, str]:
    instancje = ["https://inv.nadeko.net", "https://invidious.nerdvpn.de",
                 "https://yewtu.be", "https://invidious.f5.si"]
    for baza in instancje:
        try:
            with urllib.request.urlopen(f"{baza}/api/v1/captions/{vid}", timeout=25) as r:
                dane = json.load(r)
            for cap in dane.get("captions", []):
                url = f"{baza}/api/v1/captions/{vid}?label={urllib.parse.quote(cap['label'])}"
                with urllib.request.urlopen(url, timeout=25) as r2:
                    tekst = vtt_na_tekst(r2.read().decode("utf-8", "replace"))
                if tekst.strip():
                    return tekst, f"Invidious ({baza}, {cap.get('label')})"
        except Exception:
            continue
    return "", "wszystkie instancje Invidious bez wyniku"


def main() -> None:
    p = argparse.ArgumentParser(description="Pobiera transkrypcje filmu z YouTube.")
    p.add_argument("url", help="URL filmu albo samo ID")
    p.add_argument("--ciastka", default=CIASTKA_DOMYSLNE,
                   help=f"plik ciasteczek Netscape (domyslnie {CIASTKA_DOMYSLNE})")
    p.add_argument("--katalog", default=str(WYNIKI), help="gdzie zapisac wynik")
    a = p.parse_args()

    vid = id_filmu(a.url)
    url = f"https://www.youtube.com/watch?v={vid}"
    kat = Path(a.katalog)
    kat.mkdir(parents=True, exist_ok=True)
    ciastka = a.ciastka if (a.ciastka and os.path.isfile(a.ciastka)) else None

    print(f"FILM: {vid}")
    t = tytul(url, ciastka)
    if t:
        print(f"TYTUL: {t}")
    print(f"CIASTECZKA: {'sa (' + a.ciastka + ')' if ciastka else 'BRAK — bez nich z tego VPS kazda droga pada'}")
    print()

    proby = []
    if ciastka:
        proby.append(("yt-dlp + node + ciasteczka", lambda: droga_ytdlp(url, vid, ciastka, kat)))
    proby += [
        ("yt-dlp + node bez ciasteczek", lambda: droga_ytdlp(url, vid, None, kat)),
        ("youtube-transcript-api", lambda: droga_transcript_api(vid)),
        ("Invidious", lambda: droga_invidious(vid)),
    ]

    niepowodzenia = []
    for nazwa, fn in proby:
        print(f"  probuje: {nazwa} ... ", end="", flush=True)
        try:
            tekst, opis = fn()
        except Exception as e:
            tekst, opis = "", f"{type(e).__name__}: {str(e)[:200]}"
        if tekst.strip():
            print("UDALO SIE")
            plik = kat / f"{vid}.txt"
            naglowek = f"# {t or vid}\n# zrodlo: {url}\n# droga: {opis}\n\n"
            plik.write_text(naglowek + tekst, encoding="utf-8")
            print(f"\nZAPISANE: {plik}")
            print(f"DROGA: {opis}")
            print(f"ZNAKOW: {len(tekst)}, LINII: {tekst.count(chr(10)) + 1}")
            if niepowodzenia:
                print("\nnie zadzialaly wczesniej:")
                for n, powod in niepowodzenia:
                    print(f"  - {n}: {powod}")
            return
        print("nie")
        niepowodzenia.append((nazwa, opis))

    print("\nZADNA DROGA NIE ZADZIALALA. Powody:")
    for n, powod in niepowodzenia:
        print(f"  - {n}: {powod}")
    print("\nCO ZROBIC: dostarczyc ciasteczka YouTube (format Netscape) do")
    print(f"  {a.ciastka}  (chmod 600, poza repozytorium)")
    print("  Eksport: dodatek przegladarki 'Get cookies.txt LOCALLY', okno prywatne,")
    print("  zalogowac sie na YouTube, wejsc na youtube.com/robots.txt, eksportowac.")
    sys.exit(1)


if __name__ == "__main__":
    import urllib.parse  # noqa: E402  (uzywane w droga_invidious)
    main()
