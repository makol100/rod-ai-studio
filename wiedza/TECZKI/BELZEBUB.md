# TECZKA — BELZEBUB (doradca-pisarz bez hamulców)

Założona 02.09.2026 (dekret Tomasza „Kończ Belzebuba"). Zasada teczek: wpis NATYCHMIAST po wykryciu, dostępna całej załodze.

## STAN 02.09.2026 — BELZEBUB 2.0
- MODEL: huihui-ai/Huihui-Qwen3.8-27B-abliterated (Qwen3.8 z 14.08.2026 po ablacji), Featherless.ai, plan Developer 50 USD/mies. wg D-0130 (25.08; Chat 25 USD wyklucza API) — odnowienie 25.09.2026 12:30 obciazylo karte Tomasza 50,00 USD (zrzut z telefonu); UWAGA: wczesniejszy wpis "plan Chat 25 USD" byl bledny, ctx 32K. Poprzednik na ławce: huihui-ai/Llama-3.3-70B-Instruct-abliterated (parametr model=).
- KOD: tools/belzebub_agent.py — pętla narzędziowa do 5 rund: web_search (SearXNG 127.0.0.1:8888, safesearch=0, 8 wyników) + fetch_page (pełny tekst strony, 5000 zn, przez VPS). Ostatnia runda bez narzędzi + „odpowiedz teraz". Zadania twórcze — bez sieci. Linki nieodwiedzone narzędziem dostają dopisek „NIESPRAWDZONY". Pod odpowiedzią ślad: szukał / czytał.
- DROGI: (1) Telegram Hansa: /bzb <pytanie> (tools/hans_ucho.py, pamięć rozmów /root/rozmowy_belzebub, budżet historii 40k zn); (2) narady: python3 tools/odpal.py --kto belzebub (tools/zaloga.py → belzebub()), głos w <katalog>/belzebub.txt DOSŁOWNIE; (3) CLI: python3 tools/belzebub_agent.py "pytanie".
- CZASY: bez sieci ~15 s; z siecią 90–370 s (naprawdę czyta strony). Cloudflare wymaga User-Agent (403/1010).
- ROLA (od 25.08, bez zmian): PROPONUJE, nie wykonuje — nie ma dysku, sudo, dockera, sekretów. Głos cytowany dosłownie.

## KARTA STRAJKÓW (przed 2.0, model Llama 70B)
- #1 link ADAC-404 (zmyślony); #2 zmyślone linki; #3 fałsz „KDP przyjmuje polskie e-booki". Konsekwencja: zadania źródłowe tylko Zenek+Henio; każdy jego link przez curl → od 2.0 walidacja automatyczna w agencie.

## 02.09.2026 — ślepy test STARY vs NOWY (wiedza/BELZEBUB_test_0209.json)
- Humor/polszczyzna: NOWY wyraźnie lepszy. „Bez hamulców" (kuny): NOWY plan z cenami. Źródła: NOWY po poprawce pętli 93 s, liczby z 2 odwiedzonych stron; STARY z głowy + 2 linki NIESPRAWDZONE.
- Wpadka NOWEGO do pilnowania: napisał „Veo Lite bez audio" (cennik: z audio). Fakty nadal sprawdzać.
- Test narady przez odpal.py (/tmp/n_bzb_test): cena Veo 3.1 Lite 0,05 USD/s + 2 źródła — poprawnie.

## 02.09.2026 — audyt koncowy wdrozenia 2.0
- SearXNG: DDG/Brave/Startpage/Qwant/Yahoo blokuja IP VPS; dziala Google CSE (limit dzienny!) + Bing (dolozony 02.09). Przy braku wynikow sprawdzic 'unresponsive_engines' w JSON SearXNG.
- Pierwsza realna wymiana /bzb Tomasza na nowym modelu: 02.09 11:55 (archiwum /root/rozmowy_belzebub).

## 02.09.2026 — narada tauron_kdt (2.0)
- BLAD: 'PPE to uprawnienia elektryka' — FALSZ (PPE = Punkt Poboru Energii, numer w KDT). Reszta glosu rzeczowa: 5 pytan dzialkowcow, zdanie-zapalnik + data graniczna, 3 pominiecia zarzadow z 3 odwiedzonych zrodel.
- TECHNIKA: 2 puste odpowiedzi z rzedu = tryb reasoning zjadal max_tokens; naprawione (/no_think, 6000).

## 03.09.2026 — ZASLUGA: niezaleznie wskazal pyEzvizApi VTM/VTDU (TCP relay) z odwiedzonymi zrodlami — to byla wlasciwa droga; EZVIZ Open Platform HLS jako droga B (platna po probie).

## 17.09.2026 — narada pzd_news: CAPACITY + SŁABY GŁOS
- Pierwsze wywołanie: Featherless „capacity_exhausted" (Qwen3.8-27B) → GŁOS NIEODEBRANY. Retry (/tmp/narada_pzd_news_bzb/_retry.py, 230 s) dał odpowiedź, ale: otworzył JEDNĄ stronę (ozpzd-wroclaw.pl/nowa/page/7, lipiec 2026), pzd.pl zgłosił jako „BŁĄD SSL", i sam napisał „trzy głosy Henio/Genek/Zenek" zamiast własnego. Uczciwie oznaczył braki NIE ZNALAZŁEM. Do meldunku wszedł tylko jako „głos słaby, bez świeżych źródeł". Wniosek techniczny: przy capacity odpal.py powinien sam ponawiać (2×, 20 s) i mieć fallback modelu — TODO w zaloga.py.

## 25.09.2026 — SLEPY TEST 5 MODELI FEATHERLESS (dekret Tomasza „Featherless zwiększenie mocy belzebuba", D-0602)
- Material: .scratch/bzb_test/ (wyniki.json, slepy_test.md, mapa_TAJNA.json, ocena_genek.txt, ocena_henio.txt). 4 zadania PL: zart, prawo ROD (palenie lisci), opinia o rolce, ostra riposta (test braku hamulcow). Sedziowie niezalezni, na slepo: Genek (Gemini 3.8 flash) i Henio (DeepSeek v4-pro).
- WYNIK (Genek / Henio, max 120): OBECNY huihui-ai/Huihui-Qwen3.8-27B-abliterated 97/97 — ZWYCIEZCA u obu; hrktos-37/Hermes-4-70B-heretic 91/78 (jedyny z prawda w T2, ale slaba polszczyzna, brak polskich znakow); huihui-ai/Llama-3.3-70B-Instruct-abliterated 86/81 — ODMOWIL i moralizowal w T4 (nie spelnia zasady Belzebuba); wangzhang/gemma-4-31B-it-abliterated 85/84; huihui-ai/Qwen2.5-72B-Instruct-abliterated 75/84 (bledy jezykowe).
- WNIOSEK: wiekszy (starszy) model na Featherless NIE jest mocniejszy po polsku; zamiana modelu odrzucona. Slabosc obecnego: w T2 falsz + zmyslony akt prawny — lekarstwem jest dobre wyszukiwanie w sieci, nie wiekszy model.
- Koszt obecnego: in 1,60 / out 12,00 USD za 1M; mysli ~1200-1450 tokenow na krotka odpowiedz (37-41 s). Featherless: wszystkie modele max ctx 32K.
- 25.09 Belzebub nie oddal glosu w naradzie: 'The request was rejected as invalid' (bad_request) — prawdopodobnie brief (wiedza + material do 60 000 znakow) ponad 32K ctx.

## 25.09.2026 — BELZEBUB 2.1 WDROZONY (D-0604: „1 to na pewno", „2 poprawić jego pamięć a nie ucinać")
- tools/belzebub_agent.py (kopia poprzedniej: belzebub_agent.py.bak-2509). Model BEZ zmian (Huihui-Qwen3.8-27B-abliterated, wygral slepy test).
- WYSZUKIWANIE: DuckDuckGo (ddgs, region pl-pl) + SearXNG razem, awaryjnie Firecrawl search. CZYTANIE: fetch_page porcjami (od, do 12 000 znakow), gdy zwykle pobranie zawiedzie/strona pusta/PDF -> Firecrawl scrape (plan darmowy 1000/mies., 997 wolnych 25.09); zle adresy zapamietywane, bez ponawiania.
- PAMIEC (NIC NIE UCINAMY): kontekst 32K; nadmiar briefu -> notatnik BRIEF, starsza historia -> HISTORIA, stare wyniki narzedzi -> N1, N2… (zaslepka z numerem w rozmowie); narzedzia czytaj_notatnik(id, od, ile) i szukaj_w_notatniku(fraza) (przeszukuje notatnik i przeczytane strony). Polecenie uzytkownika chronione (_chron), 2 najswiezsze wyniki chronione. max_tokens liczone dynamicznie; przy odrzuceniu przez API — mocniejsze odciazenie i ponowienie. MAX_RUND 10.
- zaloga.py: usuniete ucinanie materialu do 60 000 znakow.
- TESTY (.scratch/bzb21/): fakt (palenie lisci w ROD) — poprawnie „nie wolno", regulamin ROD §68 pkt 5 + ustawa o odpadach, zrodla przeczytane; igla w 132 tys. znakow — v1 CZERWONY (czytal po kolei, zabraklo rund, falszywie twierdzil ze przeczytal calosc) -> po dodaniu szukaj_w_notatniku ZIELONY (29 s i 73 s); brief narady z 25.09 (rano bad_request) — pelna odpowiedz w 280 s, wejscie max ~23K tokenow.
- KONTROLA KODU: Genek (.scratch/bzb21/review_genek.txt) — znalazl 4 bledy (podpowiedz fetch_page bez adresu, globalny limit trafien w szukaniu, martwy warunek 'or True', ponawianie Firecrawl na zlym adresie) — wszystkie poprawione i sprawdzone; Henio nie zdazyl w limicie 480 s.
- Uslugi zrestartowane 25.09 (belzebub-czat, hans-ucho) — /bzb, czat WWW, Wikus i narady uzywaja 2.1.
- OTWARTE: hans_ucho wysyla odpowiedz Belzebuba na Telegram tylko do 12 000 znakow (tools/hans_ucho.py ok. l. 462) — decyzja Tomasza.

## 25.09.2026 — ZDJETE LIMITY (D-0606 „Zdjąć limity")
- tools/hans_ucho.py (kopia: hans_ucho.py.bak-2509): (1) historia rozmowy dla Belzebuba bez sufitu 88 000 znakow — cala (2.1 trzyma najnowsza w kontekscie, starsza w notatniku HISTORIA); (2) odpowiedz na Telegram bez sufitu 12 000 znakow — cala, w porcjach po 3500 (bylo 3800 -> gubilo po 300 znakow), pauza 0,4 s; to samo dla kopii Wikus->Tomasz.
- /root/belzebub_czat/serwer.py (kopia: serwer.py.bak-2509): historia czatu WWW bez ograniczenia [-40:] — cala.
- Test: 130 wiadomosci historii (~105 000 znakow) podane do odpowiedz(); Belzebub przez szukaj/HISTORIA poprawnie zacytowal najstarsze pytanie. Uslugi zrestartowane.

## 29.09.2026 — PEŁNY DOSTĘP DO VPS (D-0659)
Tomasz (dosłownie): „Dać pełen dostęp belzebubowi do WPS. NATYCHMIAST".
- Narzędzie `terminal` w `tools/belzebub_agent.py` (parametr `terminal_cb`): bash jako root, katalog /root/rod-ai-studio, timeout domyślnie 120 s (max 600), limit rund ×3.
- Bot @BelzebubV2_bot przekazuje `terminal_cb` WYŁĄCZNIE w rozmowach Tomasza (8339659505). Wikuś — bez terminala, dopóki Tomasz nie zdecyduje inaczej.
- Dziennik każdego polecenia: `/root/rozmowy_belzebub/terminal.log` (0600).
- W instrukcji Belzebuba: kopia przed zmianą, NIKT NICZEGO NIE USUWA bez polecenia Tomasza, nie wypisywać sekretów.
- Test 29.09 12:27: sam wykonał `uptime && df -h /`, odpowiedź zgodna ze stanem serwera.
