#!/usr/bin/env python3
"""szukaj_net.py — wyszukiwarka internetowa dla CALEJ zalogi, takze dla Henia.

Powod (zmierzony 29.07.2026): Henio NIE MA narzedzia web_search ani web_fetch. Jego realna lista
narzedzi w sesji: clarify, delegate_task, execute_code, memory, patch, process, read_file,
search_files, session_search, skill_manage, skill_view, skills_list, terminal, text_to_speech,
todo, vision_analyze, write_file, tool_search, tool_describe, tool_call. Ma tylko terminal z curlem,
a Google odbija curla jako bota (challenge JS). Klaudek wczesniej blednie zameldowal, ze Henio ma
przegladarke — czytal liste WLACZONYCH toolsetow w config.yaml zamiast sprawdzic, co realnie sie laduje.

To narzedzie zdejmuje ten brak: uzywa Gemini z google_search grounding (klucz Henio ma wlasny
w ~/.gemini/.env), wiec dziala z terminala jak zwykle polecenie i ZAWSZE zwraca adresy zrodel.

Uzycie:
    python3 tools/szukaj_net.py "najnowsza wersja Home Assistant Core"
    python3 tools/szukaj_net.py "cena Claude Opus 5 za milion tokenow" --zapis /tmp/wynik.txt

Fail-closed: brak klucza, blad API albo pusta odpowiedz = wyjscie 2 i komunikat. Nigdy zmyslona tresc.
Wynik ZAWSZE konczy sie lista adresow — bez zrodel odpowiedz nie jest dowodem.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

SCIEZKI_KLUCZA = [
    os.path.expanduser("~/.gemini/.env"),
    "/root/.gemini/.env",
]

POLECENIE = (
    "Wyszukaj w internecie i odpowiedz WYLACZNIE na podstawie znalezionych stron.\n"
    "Podaj konkretne liczby, daty i nazwy tak, jak stoja w zrodle.\n"
    "Jesli wyszukiwanie nie daje odpowiedzi — napisz dokladnie NIE WIEM i nic wiecej.\n"
    "Nie zgaduj, nie uzupelniaj z pamieci modelu.\n\nPYTANIE: "
)


def klucz() -> str:
    for s in SCIEZKI_KLUCZA:
        if os.path.isfile(s):
            try:
                for linia in open(s, encoding="utf-8"):
                    if linia.startswith("GEMINI_API_KEY="):
                        return linia.split("=", 1)[1].strip()
            except OSError:
                continue
    print("BLAD: nie znalazlem GEMINI_API_KEY (~/.gemini/.env ani /root/.gemini/.env)")
    sys.exit(2)


def szukaj(pytanie: str) -> tuple:
    body = json.dumps({
        "contents": [{"parts": [{"text": POLECENIE + pytanie}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 1500},
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={klucz()}",
        data=body, headers={"Content-Type": "application/json"})
    try:
        odp = json.loads(urllib.request.urlopen(req, timeout=180).read())
    except urllib.error.HTTPError as e:
        print(f"BLAD API {e.code}: {e.read().decode()[:400]}")
        sys.exit(2)
    except Exception as e:
        print(f"BLAD POLACZENIA: {e}")
        sys.exit(2)

    kandydaci = odp.get("candidates") or []
    if not kandydaci:
        print("BLAD: brak odpowiedzi od wyszukiwarki — NIE zmyslam zastepczej tresci")
        sys.exit(2)
    c = kandydaci[0]
    tekst = "".join(p.get("text", "") for p in c.get("content", {}).get("parts", []))
    if not tekst.strip():
        print("BLAD: pusta odpowiedz — NIE zmyslam zastepczej tresci")
        sys.exit(2)

    g = c.get("groundingMetadata", {}) or {}
    zrodla = []
    for kawalek in g.get("groundingChunks", []):
        w = kawalek.get("web", {})
        if w.get("uri"):
            zrodla.append((w.get("title") or "?", w["uri"]))
    zapytania = g.get("webSearchQueries", [])
    return tekst.strip(), zrodla, zapytania


def szukaj_zapasowo(pytanie: str) -> tuple:
    """DROGA ZAPASOWA — Marginalia (niezalezny indeks) + Wikipedia. BEZ Gemini, bez klucza.

    Powod (30.07.2026, Tomasz: "cala debata jest nierowna, jezeli reszta nie miala dostepu do internetu"):
    wyszukiwarka chodzila WYLACZNIE przez Gemini, wiec awaria Google (status 503) odebrala internet
    Genkowi, Heniowi i Klaudkowi naraz. Jeden dostawca = jeden punkt awarii dla calej zalogi.

    Zmierzone 30.07 z tego VPS: DuckDuckGo (lite i html, GET i POST) — 0 wynikow, blokuje serwer.
    Mojeek — 0 wynikow. Marginalia API — dziala. Wikipedia API — dziala.
    Ta droga NIE streszcza — zwraca surowe trafienia z adresami, zeby czytajacy ocenil sam.
    """
    wyniki, linie = [], []

    adres = "https://api.marginalia.nu/public/search/" + urllib.parse.quote(pytanie)
    try:
        r = json.loads(urllib.request.urlopen(
            urllib.request.Request(adres, headers={"Accept": "application/json"}), timeout=45).read())
        for w in (r.get("results") or [])[:6]:
            tytul = (w.get("title") or "?").strip()[:110]
            uri = w.get("url") or ""
            opis = (w.get("description") or "").strip()[:240]
            if uri:
                wyniki.append((tytul, uri))
                linie.append(f"{len(wyniki)}. {tytul}")
                if opis:
                    linie.append(f"   {opis}")
    except Exception as e:
        linie.append(f"(Marginalia niedostepna: {e})")

    try:
        wadres = ("https://pl.wikipedia.org/w/api.php?action=query&list=search&srlimit=2&format=json&srsearch="
                  + urllib.parse.quote(pytanie))
        rw = json.loads(urllib.request.urlopen(
            urllib.request.Request(wadres, headers={"User-Agent": "rod-ai-studio/1.0"}), timeout=30).read())
        for w in rw.get("query", {}).get("search", [])[:2]:
            tytul = w.get("title", "")
            uri = "https://pl.wikipedia.org/wiki/" + urllib.parse.quote(tytul.replace(" ", "_"))
            opis = re.sub(r"<[^>]+>", "", w.get("snippet", ""))
            wyniki.append((f"Wikipedia: {tytul}", uri))
            linie.append(f"{len(wyniki)}. Wikipedia: {tytul}")
            if opis:
                linie.append(f"   {opis}")
    except Exception:
        pass

    if not wyniki:
        return "", [], "obie drogi zapasowe bez wynikow (Marginalia i Wikipedia)"
    return "\n".join(linie), wyniki, ""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("pytanie", nargs="+")
    p.add_argument("--zapis", default="")
    p.add_argument("--tylko-zapasowo", action="store_true", help="pomin Gemini, idz od razu droga zapasowa (Marginalia + Wikipedia)")
    a = p.parse_args()
    pytanie = " ".join(a.pytanie)

    # DROGA 1: Gemini z google_search (streszcza i podaje zrodla)
    # DROGA 2 (gdy Gemini padnie): DuckDuckGo — surowe wyniki, bez modelu, bez klucza
    if a.tylko_zapasowo:
        tekst, wyniki, blad = szukaj_zapasowo(pytanie)
        if blad:
            print(f"BLAD: {blad}")
            return 2
        zrodla, zapytania = wyniki, [pytanie]
        tekst = "[DROGA ZAPASOWA — Marginalia + Wikipedia, surowe wyniki bez streszczenia]\n\n" + tekst
    else:
        try:
            tekst, zrodla, zapytania = szukaj(pytanie)
        except SystemExit:
            print("[szukaj_net] Gemini niedostepny — przechodze na DuckDuckGo", file=sys.stderr)
            tekst, wyniki, blad = szukaj_zapasowo(pytanie)
            if blad:
                print(f"BLAD: obie drogi padly | {blad}")
                return 2
            zrodla, zapytania = wyniki, [pytanie]
            tekst = "[DROGA ZAPASOWA — Marginalia + Wikipedia, surowe wyniki bez streszczenia]\n\n" + tekst
    linie = [f"PYTANIE: {pytanie}", "", tekst, ""]
    if zapytania:
        linie.append(f"ZAPYTANIA WYSZUKIWARKI: {'; '.join(zapytania)}")
    if zrodla:
        linie.append(f"ZRODLA ({len(zrodla)}):")
        for tytul, uri in zrodla[:8]:
            linie.append(f"  - {tytul}: {uri}")
    else:
        linie.append("ZRODLA: BRAK — traktuj odpowiedz jak niepotwierdzona i sprawdz inaczej.")
    wynik = "\n".join(linie)

    if a.zapis:
        with open(a.zapis, "w", encoding="utf-8") as f:
            f.write(wynik)
        print(f"[szukaj_net] zapisane: {a.zapis}", file=sys.stderr)
    print(wynik)
    return 0


if __name__ == "__main__":
    sys.exit(main())
