# TECZKA — BELZEBUB (doradca-pisarz bez hamulców)

Założona 02.09.2026 (dekret Tomasza „Kończ Belzebuba"). Zasada teczek: wpis NATYCHMIAST po wykryciu, dostępna całej załodze.

## STAN 02.09.2026 — BELZEBUB 2.0
- MODEL: huihui-ai/Huihui-Qwen3.8-27B-abliterated (Qwen3.8 z 14.08.2026 po ablacji), Featherless.ai, plan Chat 25 USD/mies. (4 jednostki współbieżności; ten model = 2 jednostki → 2 pytania naraz), ctx 32K. Poprzednik na ławce: huihui-ai/Llama-3.3-70B-Instruct-abliterated (parametr model=).
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
