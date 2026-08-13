#!/usr/bin/env python3
"""szukaj_www.py — NIEZALEZNA wyszukiwarka internetowa (SearXNG na VPS).
NIE przez Gemini, NIE przez Klaudka - wlasna metawyszukiwarka (Google/Bing/DDG naraz).
Uzycie: python3 tools/szukaj_www.py "zapytanie"
Kazdy czlonek zalogi szuka SAM: wlasne zapytania, wlasne surowe wyniki."""
import sys, json, urllib.parse, urllib.request
if len(sys.argv)<2:
    print('Uzycie: szukaj_www.py "zapytanie"'); sys.exit(1)
q=" ".join(sys.argv[1:])
url="http://127.0.0.1:8888/search?"+urllib.parse.urlencode({"q":q,"format":"json"})
try:
    req=urllib.request.Request(url, headers={"User-Agent":"rod-zaloga/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d=json.load(r)
    res=d.get("results",[])
    if not res:
        print(f"BRAK WYNIKOW dla: {q}"); sys.exit(0)
    print(f"[SearXNG] {len(res)} wynikow dla: {q}\n")
    for x in res[:8]:
        print(f"- {x.get('title','')[:80]}")
        print(f"  {x.get('url','')}")
        c=x.get('content','')
        if c: print(f"  {c[:180]}")
        print()
except Exception as e:
    print(f"BLAD SearXNG: {e}"); sys.exit(2)
