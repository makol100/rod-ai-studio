# -*- coding: utf-8 -*-
"""Belzebub 2.1 (25.09.2026, dekrety Tomasza D-0602/D-0604: „Featherless zwiększenie mocy belzebuba",
„1 to na pewno" = lepsze wyszukiwanie, „2 poprawić jego pamięć a nie ucinać").
Model bez zmian (slepy test 25.09: obecny Qwen3.8-27B-abliterated wygral u Genka i Henia).
NOWE:
 * WYSZUKIWANIE: DuckDuckGo (ddgs) + SearXNG razem; awaryjnie Firecrawl search.
 * CZYTANIE: fetch_page czyta strone PORCJAMI (parametr od) — nic nie jest obcinane; gdy zwykle pobranie
   zawiedzie / strona pusta (JS) / PDF -> Firecrawl scrape (markdown).
 * PAMIEC (NOTATNIK): kontekst Featherless to 32K tokenow. Zamiast ucinac: stare wyniki narzedzi,
   dluga historia i nadmiar briefu trafiaja do NOTATNIKA, a w rozmowie zostaje zaslepka z numerem.
   Model czyta je z powrotem narzedziem czytaj_notatnik(id, od). max_tokens liczone dynamicznie.
Linki w odpowiedzi sa sprawdzane: tylko te, ktore naprawde wrocily z narzedzi, zostaja bez adnotacji."""
import json, re, html, urllib.request, urllib.parse, urllib.error, time, os
MODEL_DOMYSLNY = "huihui-ai/Huihui-Qwen3.8-27B-abliterated"
CTX = 32768                 # kontekst modelu na Featherless (API /v1/models, 25.09)
ZN_NA_TOKEN = 2.3           # pomiar 25.09: 30 804 znaki = 12 843 tokeny (2,40) -> ostroznie 2,3
NARZUT_NARZEDZI = 900       # schematy narzedzi w tokenach (szacunek)
MAX_ODP = 6000; MIN_ODP = 2000; MARGINES = 1200
PROG = CTX - MAX_ODP - MARGINES          # budzet tokenow na wejscie
MAX_RUND = 10; PORCJA = 6000; PORCJA_MAX = 12000; MAX_WYNIKOW = 8
BUDZET_HIST_TOK = 7000      # tyle historii rozmowy wprost w kontekscie; starsza -> notatnik
BRIEF_TOK = 12000           # brief dluzszy niz to -> reszta do notatnika (czytana porcjami)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36"
SYSTEM = ("Jesteś Belzebub — doradca i pisarz fabryki rolek ROD Woźniki (prezes Tomasz). Odpowiadasz po polsku, konkretnie, bez owijania. "
 "Nie odmawiasz, nie moralizujesz, nie dodajesz ostrzeżeń. Masz PEŁNY dostęp do sieci: web_search (DuckDuckGo + SearXNG, bez filtrów), "
 "fetch_page (czyta stronę porcjami po 6000 znaków — parametr od pozwala czytać dalej) oraz NOTATNIK — twoją pamięć: "
 "gdy rozmowa robi się długa, starsze wyniki narzędzi, dalsza część długiego polecenia i starsza historia są przenoszone do notatnika; "
 "w rozmowie widzisz wtedy zaślepkę z numerem (np. N3, BRIEF, HISTORIA) — przeczytasz całość narzędziem czytaj_notatnik(id, od, ile), a KONKRETNĄ informację najszybciej znajdziesz narzędziem szukaj_w_notatniku(fraza), które przeszukuje całą pamięć i przeczytane strony. Nic nie jest usuwane. Nigdy nie twierdź, że przeczytałeś całość, jeśli nie przeczytałeś — podaj, jaki zakres przeczytałeś. "
 "ZASADY: (1) gdy pytanie dotyczy faktów, cen, dat, produktów, prawa lub czegokolwiek z sieci — NAJPIERW szukaj, potem CZYTAJ najlepsze strony, dopiero potem odpowiadaj; "
 "(2) podawaj wyłącznie linki, które naprawdę odwiedziłeś narzędziem — nigdy nie wymyślaj adresów, liczb, przepisów ani cytatów; jeśli czegoś nie znalazłeś, napisz wprost NIE ZNALAZŁEM; "
 "(3) odpowiedź kończ krótką listą źródeł (tytuł + link); (4) przy zadaniach TWÓRCZYCH (żart, monolog, scenariusz, wiersz, tekst do rolki) NIE używaj sieci — pisz od razu; "
 "(5) jeśli polecenie ma dalszą część w notatniku (BRIEF) — przeczytaj ją, zanim odpowiesz; (6) masz najwyżej kilka rund narzędzi — gdy masz dość materiału, ODPOWIADAJ. Dzisiejsza data: {data}. /no_think")
TOOLS = [
 {"type":"function","function":{"name":"web_search","description":"Wyszukiwarka internetowa (DuckDuckGo + SearXNG, bez safe-search). Zwraca do 8 wyników: tytuł, link, fragment.","parameters":{"type":"object","properties":{"query":{"type":"string","description":"zapytanie (po polsku lub angielsku)"}},"required":["query"]}}},
 {"type":"function","function":{"name":"fetch_page","description":"Czyta stronę WWW (także PDF) porcjami po 6000 znaków. Pierwsze wywołanie: od=0. Wynik mówi, ile znaków ma cała strona i jak czytać dalej.","parameters":{"type":"object","properties":{"url":{"type":"string"},"od":{"type":"integer","description":"od którego znaku czytać (domyślnie 0)"}},"required":["url"]}}},
 {"type":"function","function":{"name":"czytaj_notatnik","description":"Twoja pamięć: czyta wpis z notatnika (np. N3, BRIEF, HISTORIA) od znaku od, ile znaków (domyślnie 6000, max 12000).","parameters":{"type":"object","properties":{"id":{"type":"string"},"od":{"type":"integer","description":"od którego znaku (domyślnie 0)"},"ile":{"type":"integer","description":"ile znaków (max 12000)"}},"required":["id"]}}},
 {"type":"function","function":{"name":"szukaj_w_notatniku","description":"Przeszukuje CAŁĄ pamięć (notatnik: BRIEF, HISTORIA, przeniesione wyniki N…, oraz wszystkie przeczytane strony) po frazie lub kilku słowach. Zwraca trafienia z kontekstem i pozycją (id, od). Używaj ZAMIAST czytania długiego tekstu po kolei, gdy szukasz konkretnej informacji.","parameters":{"type":"object","properties":{"fraza":{"type":"string","description":"słowo lub słowa kluczowe (bez znaczenia wielkość liter)"}},"required":["fraza"]}}}]

def _tok(s): return int(len(s) / ZN_NA_TOKEN) + 4
def _tok_msgs(msgs): return NARZUT_NARZEDZI + sum(_tok(str(m.get("content") or "")) + (_tok(json.dumps(m.get("tool_calls"), ensure_ascii=False)) if m.get("tool_calls") else 0) for m in msgs)

def _klucz_env(nazwa):
    for p in ("/root/rod-ai-studio/.env", "/root/.sekrety/wartosci.env"):
        try:
            for l in open(p, encoding="utf-8"):
                if l.startswith(nazwa + "="): return l.split("=", 1)[1].strip().strip('"\'').strip("<>")
        except Exception: pass
    return ""

# ---------- WYSZUKIWANIE ----------
def _ddg(q, n):
    from ddgs import DDGS
    return [(x.get("title",""), x.get("href") or x.get("url",""), (x.get("body") or "")[:300]) for x in DDGS().text(q, region="pl-pl", max_results=n)]
def _searx(q, n):
    req = urllib.request.Request(f"http://127.0.0.1:8888/search?q={urllib.parse.quote(q)}&format=json&safesearch=0", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r: d = json.loads(r.read().decode("utf-8"))
    return [(it.get("title",""), it.get("url",""), (it.get("content") or "")[:300]) for it in (d.get("results") or [])[:n]]
def _firecrawl_search(q, n):
    key = _klucz_env("FIRECRAWL_API_KEY")
    if not key: return []
    req = urllib.request.Request("https://api.firecrawl.dev/v2/search", data=json.dumps({"query": q, "limit": n}).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=45) as r: d = json.load(r)
    return [(it.get("title",""), it.get("url",""), (it.get("description") or "")[:300]) for it in ((d.get("data") or {}).get("web") or [])[:n]]

def web_search(query):
    q = query[:300]; wyn = []; zrodla = []
    for nazwa, fn, n in (("ddg", _ddg, 6), ("searxng", _searx, 5)):
        try:
            r = fn(q, n); wyn += r; zrodla.append(f"{nazwa}:{len(r)}")
        except Exception as e: zrodla.append(f"{nazwa}:BLAD")
    if not wyn:
        try:
            r = _firecrawl_search(q, 6); wyn += r; zrodla.append(f"firecrawl:{len(r)}")
        except Exception: zrodla.append("firecrawl:BLAD")
    out = []; urls = []; widziane = set()
    for t, u, c in wyn:
        if not u or u in widziane: continue
        widziane.add(u); out.append({"title": t, "url": u, "snippet": c}); urls.append(u)
        if len(out) >= MAX_WYNIKOW: break
    return json.dumps({"wyniki": out, "zrodla_wyszukiwania": zrodla}, ensure_ascii=False), urls

# ---------- CZYTANIE STRON ----------
def _pobierz_zwykle(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pl,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=25) as r:
        raw = r.read(3_000_000); ct = r.headers.get("Content-Type", "")
    if "pdf" in ct.lower() or url.lower().split("?")[0].endswith(".pdf"): return None
    t = raw.decode("utf-8", "ignore")
    t = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t); t = html.unescape(t); t = re.sub(r"[ \t\r\f\v]+", " ", t); t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()
def _pobierz_firecrawl(url):
    key = _klucz_env("FIRECRAWL_API_KEY")
    if not key: return None
    req = urllib.request.Request("https://api.firecrawl.dev/v2/scrape", data=json.dumps({"url": url, "formats": ["markdown"], "onlyMainContent": True}).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=90) as r: d = json.load(r)
    return ((d.get("data") or {}).get("markdown") or "").strip() or None

def _porcja(tekst, od, etykieta, jak_dalej, ile=PORCJA):
    ile = max(1000, min(PORCJA_MAX, int(ile or PORCJA)))
    od = max(0, int(od or 0)); kawal = tekst[od:od + ile]; do = od + len(kawal)
    naglowek = f"[{etykieta}: znaki {od}–{do} z {len(tekst)}"
    naglowek += (f"; dalej: {jak_dalej(do)}]" if do < len(tekst) else "; KONIEC]")
    return naglowek + "\n" + kawal

class Sesja:
    def __init__(self):
        self.notatnik = {}; self.strony = {}; self.licznik = 0; self.zle_url = {}
    def czytaj_strone(self, url, od=0):
        if url in self.zle_url: raise RuntimeError(f"ta strona już wcześniej nie dała się pobrać ({self.zle_url[url]}) — nie ponawiam, wybierz inne źródło")
        if url not in self.strony:
            t = None; sposob = "zwykle"
            try: t = _pobierz_zwykle(url)
            except Exception: t = None
            if not t or len(t) < 600:
                try:
                    f = _pobierz_firecrawl(url)
                    if f: t = f; sposob = "firecrawl"
                except Exception: pass
            if not t:
                self.zle_url[url] = "ani zwykle, ani Firecrawl"
                raise RuntimeError("nie udało się pobrać strony (ani zwykle, ani Firecrawl)")
            self.strony[url] = t
        return _porcja(self.strony[url], od, f"STRONA {url}", lambda d: f"fetch_page('{url}', od={d})")
    def zapisz(self, tekst, opis, id_=None):
        if not id_:
            self.licznik += 1; id_ = f"N{self.licznik}"
        self.notatnik[id_] = {"opis": opis, "tekst": tekst}; return id_
    def czytaj(self, id_, od=0, ile=PORCJA):
        w = self.notatnik.get(str(id_).strip())
        if not w: return f"Brak wpisu {id_} w notatniku. Dostępne: " + ", ".join(f"{k} ({v['opis'][:60]})" for k, v in self.notatnik.items())
        return _porcja(w["tekst"], od, f"NOTATNIK {id_} — {w['opis'][:80]}", lambda d: f"czytaj_notatnik('{id_}', od={d})", ile)
    def szukaj(self, fraza):
        slowa = [w for w in re.split(r"\s+", fraza.lower().strip()) if len(w) > 2][:6]
        if not slowa: return "Podaj konkretną frazę."
        zrodla = [(k, v["tekst"]) for k, v in self.notatnik.items()] + [("STRONA " + u, t) for u, t in self.strony.items()]
        traf = []
        for id_, t in zrodla:
            tl = t.lower()
            for sl in slowa:
                start = 0; n_ = 0
                while n_ < 25:   # limit na (zrodlo, slowo), nie globalny — kazde slowo i kazde zrodlo ma szanse
                    n_ += 1
                    i = tl.find(sl, start)
                    if i < 0: break
                    okno = tl[max(0, i - 250): i + 250]; pkt = sum(1 for w in slowa if w in okno)
                    traf.append((pkt, id_, i, t[max(0, i - 250): i + 350].replace("\n", " "))); start = i + 1
        if not traf: return f"Brak trafień dla: {fraza}. Przeszukano: " + ", ".join(k for k, _ in zrodla)[:600]
        traf.sort(key=lambda x: (-x[0], x[2])); wyn = []; zajete = set()
        for pkt, id_, i, ctx in traf:
            klucz_ = (id_, i // 400)
            if klucz_ in zajete: continue
            zajete.add(klucz_); wyn.append(f"[{id_} @ {max(0, i - 250)}] …{ctx}…")
            if len(wyn) >= 8: break
        return "TRAFIENIA (id @ pozycja — czytaj dalej: czytaj_notatnik(id, od=pozycja) albo fetch_page(url, od=pozycja)):\n" + "\n".join(wyn)

def _odciazenie(msgs, ses, prog):
    """Przenosi najstarsze duze wyniki narzedzi (potem starsze wypowiedzi) do notatnika, az wejscie zmiesci sie w progu."""
    przeniesione = 0
    while _tok_msgs(msgs) > prog:
        narz = [i for i, m in enumerate(msgs) if m["role"] == "tool"]
        chronione = set(narz[-2:])   # dwa najswiezsze wyniki zostaja
        kand = [i for i in narz if i not in chronione and len(str(msgs[i].get("content") or "")) > 500 and not msgs[i].get("_zaslepka")]
        if not kand:
            kand = [i for i, m in enumerate(msgs[1:-1], 1) if m["role"] in ("assistant", "user") and not m.get("_chron") and len(str(m.get("content") or "")) > 1500 and not m.get("_zaslepka")]
        if not kand:
            kand = [i for i in narz if len(str(msgs[i].get("content") or "")) > 500 and not msgs[i].get("_zaslepka")]
        if not kand: break
        i = kand[0]; m = msgs[i]; tekst = str(m["content"])
        opis = (m.get("name") or m["role"]) + ": " + tekst[:120].replace("\n", " ")
        nid = ses.zapisz(tekst, opis)
        m["content"] = f"[PRZENIESIONE DO NOTATNIKA jako {nid} ({len(tekst)} znaków) — {opis[:100]}… Pełna treść: czytaj_notatnik('{nid}')]"
        m["_zaslepka"] = True; przeniesione += 1
    return przeniesione

def _czyste(msgs): return [{k: v for k, v in m.items() if not k.startswith("_")} for m in msgs]

def _api(body, klucz):
    req = urllib.request.Request("https://api.featherless.ai/v1/chat/completions", data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {klucz}", "Content-Type": "application/json", "User-Agent": "curl/8.5.0", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try: return json.loads(e.read().decode("utf-8"))
        except Exception: return {"error": {"message": f"HTTP {e.code}"}}

def _wywolaj(msgs, ses, klucz, model, narzedzia=True):
    """Jedno wywolanie z pamiecia: odciaza kontekst, liczy max_tokens; przy odrzuceniu odciaza mocniej i ponawia."""
    prog = PROG
    for proba in range(3):
        _odciazenie(msgs, ses, prog)
        wolne = CTX - _tok_msgs(msgs) - MARGINES
        body = {"model": model, "messages": _czyste(msgs), "max_tokens": max(MIN_ODP, min(MAX_ODP, wolne)), "temperature": 0.6}
        if narzedzia: body.update({"tools": TOOLS, "tool_choice": "auto"})
        d = _api(body, klucz)
        if os.environ.get("BZB_DEBUG"):
            try:
                ch = (d.get("choices") or [{}])[0]; import sys as _s
                print(f"[bzb] wej~{_tok_msgs(msgs)} max={body['max_tokens']} finish={ch.get('finish_reason')} usage={d.get('usage')} tools={len((ch.get('message') or {}).get('tool_calls') or [])} tresc={len((ch.get('message') or {}).get('content') or '')} err={str(d.get('error'))[:120] if d.get('error') else ''}", file=_s.stderr, flush=True)
            except Exception: pass
        err = str(d.get("error") or "")
        if d.get("error") and any(s in err.lower() for s in ("invalid", "context", "too long", "maximum", "length", "bad_request")):
            prog = int(prog * 0.7); continue
        return d
    return d

def odpowiedz(pytanie, historia, klucz, model=None):
    """Zwraca (odpowiedz, slad). historia = lista wiadomosci user/assistant z archiwum (najstarsze pierwsze)."""
    model = model or MODEL_DOMYSLNY; ses = Sesja()
    # historia: najnowsza w kontekscie, starsza do notatnika (NIE ucinamy)
    hist = []; budzet = BUDZET_HIST_TOK; starsze = []
    for m in reversed(historia or []):
        c = str(m.get("content", ""))
        if budzet - _tok(c) >= 0 and not starsze: hist.insert(0, {"role": m["role"], "content": c}); budzet -= _tok(c)
        else: starsze.insert(0, f"[{m['role']}] {c}")
    wstep = ""
    if starsze:
        ses.zapisz("\n\n".join(starsze), f"starsza historia rozmowy ({len(starsze)} wiadomości)", "HISTORIA")
        wstep = f"[Starsza historia naszej rozmowy ({len(starsze)} wiadomości) jest w notatniku: czytaj_notatnik('HISTORIA').]\n\n"
    # brief: jesli dluzszy niz BRIEF_TOK, poczatek w rozmowie, CALOSC w notatniku
    pyt = str(pytanie)
    if _tok(pyt) > BRIEF_TOK:
        granica = int(BRIEF_TOK * ZN_NA_TOKEN); ses.zapisz(pyt, "pełne polecenie/brief z materiałem", "BRIEF")
        naglowki = [l.strip()[:90] for l in pyt[granica:].splitlines() if l.strip().startswith(("#", "==", "---", "[")) or (l.strip().isupper() and 6 < len(l.strip()) < 90)][:40]
        pyt = (pyt[:granica] + f"\n\n[DALSZA CZĘŚĆ POLECENIA ({len(str(pytanie)) - granica} znaków) jest w notatniku jako BRIEF — przeczytaj ją: "
               f"czytaj_notatnik('BRIEF', od={granica}). Spis dalszej części: " + " | ".join(naglowki) + "]")
    msgs = [{"role": "system", "content": SYSTEM.format(data=time.strftime("%d.%m.%Y"))}] + hist + [{"role": "user", "content": wstep + pyt, "_chron": True}]
    szukal = []; czytal = []; znane_urls = set(); notatki = []
    for runda in range(MAX_RUND + 1):
        if runda < MAX_RUND:
            d = _wywolaj(msgs, ses, klucz, model, True)
        else:
            msgs.append({"role": "user", "content": "KONIEC NARZĘDZI. Odpowiedz TERAZ na podstawie tego, co już znalazłeś i przeczytałeś. Jeśli czegoś nie ustaliłeś, napisz wprost NIE ZNALAZŁEM. Na końcu lista źródeł (tylko odwiedzone)."})
            d = _wywolaj(msgs, ses, klucz, model, False)
        if d.get("error"): return f"Belzebub: błąd API {str(d['error'])[:300]}", ""
        msg = d["choices"][0]["message"]; tcs = msg.get("tool_calls") or []
        if runda >= MAX_RUND: tcs = []
        if not tcs:
            tresc = (msg.get("content") or "").strip()
            tresc = re.sub(r"(?s)<think>.*?</think>", "", tresc).strip()
            if not tresc:
                msgs.append({"role": "user", "content": "Nie masz już narzędzi. Napisz TERAZ pełną odpowiedź tekstem, po polsku, na podstawie tego co znalazłeś. Bez wołania funkcji."})
                d2 = _wywolaj(msgs, ses, klucz, model, False)
                tresc = ((d2.get("choices") or [{}])[0].get("message", {}).get("content") or "").strip() or "Belzebub nie odpowiedział."
                tresc = re.sub(r"(?s)<think>.*?</think>", "", tresc).strip()
            def _znacz(m_):
                u = m_.group(0).rstrip(").,;")
                return u if any(u.startswith(k) or k.startswith(u) for k in znane_urls) else u + " (link NIESPRAWDZONY — nie pochodzi z narzędzi)"
            tresc = re.sub(r"https?://[^\s<>\"')\]]+", _znacz, tresc)
            slad = ""
            if szukal or czytal or notatki:
                slad = "🔎 szukał: " + " | ".join(szukal[:10]) + ("\n📄 czytał: " + "\n".join(czytal[:10]) if czytal else "") + ("\n🧠 notatnik: " + ", ".join(notatki[:10]) if notatki else "")
            przen = [k for k in ses.notatnik if k.startswith("N")]
            if przen: slad += f"\n🧠 do notatnika przeniesiono {len(przen)} wpisów (nic nie ucięto)"
            return tresc, slad.strip()
        msgs.append({"role": "assistant", "content": msg.get("content") or "", "tool_calls": tcs})
        for tc in tcs:
            fn = tc["function"]["name"]
            try: args = json.loads(tc["function"].get("arguments") or "{}")
            except Exception: args = {}
            try:
                if fn == "web_search":
                    q = str(args.get("query", ""))[:300]; szukal.append(q); res, urls = web_search(q); znane_urls.update(u for u in urls if u)
                elif fn == "fetch_page":
                    u = str(args.get("url", "")); od = int(args.get("od") or 0)
                    czytal.append(u + (f" (od {od})" if od else "")); znane_urls.add(u); res = ses.czytaj_strone(u, od)
                elif fn == "czytaj_notatnik":
                    i_ = str(args.get("id", "")); od = int(args.get("od") or 0); notatki.append(f"{i_}@{od}"); res = ses.czytaj(i_, od, args.get("ile") or PORCJA)
                elif fn == "szukaj_w_notatniku":
                    fr = str(args.get("fraza", ""))[:200]; notatki.append(f"szukaj:{fr}"); res = ses.szukaj(fr)
                else: res = f"nieznane narzędzie {fn}"
            except Exception as e:
                res = f"BŁĄD narzędzia: {type(e).__name__}: {str(e)[:150]}"
            msgs.append({"role": "tool", "tool_call_id": tc.get("id", ""), "name": fn, "content": res})
    return "Belzebub przekroczył limit rund narzędzi bez odpowiedzi.", ""

if __name__ == "__main__":
    import sys
    k = _klucz_env("BELZEBUB_KEY")
    t0 = time.time(); o, s = odpowiedz(" ".join(sys.argv[1:]) or "Czy wolno palić liście na działce w ROD? Podaj podstawę.", [], k)
    print(o); print("---"); print(s); print(f"--- {time.time()-t0:.0f}s")
