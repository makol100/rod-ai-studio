#!/usr/bin/env python3
"""szukaj_web.py — NIEZALEZNE wyszukiwanie w internecie. Backendy: searxng, ddg, firecrawl.
Kazdy agent moze uzyc INNEGO backendu = rozne zrodla = prawdziwa niezaleznosc (nie przez Klaudka, nie Gemini).
Uzycie: python3 tools/szukaj_web.py "zapytanie" [ile] [--backend=searxng|ddg|firecrawl]"""
import sys, json, os, urllib.parse, urllib.request

def _key(name):
    v = os.environ.get(name)
    if v: return v
    try:
        for line in open(os.path.join(os.path.dirname(__file__), "..", ".env")):
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip()
    except Exception: pass
    return None

def searxng(q, n):
    u = os.environ.get("SEARXNG_URL", "http://localhost:8888")
    url = u.rstrip("/") + "/search?" + urllib.parse.urlencode({"q": q, "format": "json"})
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    return [(it.get("title",""), it.get("url",""), (it.get("content") or "")[:280]) for it in data.get("results",[])[:n]]

def ddg(q, n):
    from ddgs import DDGS
    r = list(DDGS().text(q, max_results=n))
    return [(x.get("title",""), x.get("href") or x.get("url",""), (x.get("body") or "")[:280]) for x in r]

def firecrawl(q, n):
    key = _key("FIRECRAWL_API_KEY")
    if not key: raise RuntimeError("brak FIRECRAWL_API_KEY (dodaj do .env)")
    req = urllib.request.Request("https://api.firecrawl.dev/v2/search",
        data=json.dumps({"query": q, "limit": n}).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=45) as r:
        d = json.load(r)
    web = (d.get("data") or {}).get("web", [])
    return [(it.get("title",""), it.get("url",""), (it.get("description") or "")[:280]) for it in web[:n]]

BACKENDS = {"searxng": searxng, "ddg": ddg, "firecrawl": firecrawl}
args = [a for a in sys.argv[1:] if not a.startswith("--")]
backend = "searxng"
for a in sys.argv[1:]:
    if a.startswith("--backend="): backend = a.split("=",1)[1]
if not args:
    print('Uzycie: szukaj_web.py "zapytanie" [ile] [--backend=searxng|ddg|firecrawl]'); sys.exit(1)
q = args[0]; n = int(args[1]) if len(args) > 1 else 6
fn = BACKENDS.get(backend)
if not fn:
    print(f"Nieznany backend: {backend}. Dostepne: {', '.join(BACKENDS)}"); sys.exit(1)
try:
    res = fn(q, n)
except Exception as e:
    print(f"[szukaj_web/{backend}] BLAD: {str(e)[:160]}"); sys.exit(2)
if not res:
    print(f"[szukaj_web/{backend}] brak wynikow: {q}"); sys.exit(0)
print(f"[szukaj_web/{backend}] {len(res)} wynikow dla: {q}\n")
for i,(t,u,c) in enumerate(res,1):
    print(f"{i}. {t}\n   {u}\n   {c}\n")
