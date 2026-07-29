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
import sys
import urllib.error
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


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("pytanie", nargs="+")
    p.add_argument("--zapis", default="")
    a = p.parse_args()
    pytanie = " ".join(a.pytanie)

    tekst, zrodla, zapytania = szukaj(pytanie)
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
