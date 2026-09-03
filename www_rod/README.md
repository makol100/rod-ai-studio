# ROD Woźniki — statyczna strona v1

Stan: szkielet lokalny. Nieopublikowany.

## Architektura

- `content/announcements.json` — ogłoszenia; docelowy punkt zapisu Hansa.
- `content/pages/*.md` — proste podstrony Markdown z trzema polami front matter.
- `templates/` — wspólny układ i strona główna.
- `static/` — CSS i JS bez frameworków oraz zewnętrznych fontów.
- `build.py` — generator bez zależności, tworzy `dist/`, sitemapę, robots i 404.
- `Caddyfile` — kandydat dla domeny głównej, `www` i proxy Barometru.

Generator nie usuwa starych plików z `dist/`, zgodnie z zakazem usuwania w repo. Nadpisuje wyłącznie pliki, które sam buduje.

## Budowa i testy

```bash
python3 www_rod/build.py --check
python3 www_rod/build.py
python3 -m unittest discover -s www_rod/tests -v
node --check www_rod/static/app.js
```

Walidacja Caddy bez publikacji:

```bash
docker run --rm -v /root/rod-ai-studio/www_rod/Caddyfile:/etc/caddy/Caddyfile:ro caddy:2.11.4 caddy validate --config /etc/caddy/Caddyfile
```

## Hans — kontrakt proponowany

1. `/ogloszenie Tytuł | Treść | data-do` tworzy wersję roboczą wpisu JSON.
2. Hans waliduje długość, datę i brak danych osobowych.
3. Tomasz odpowiada `PUBLIKUJ <kod>`.
4. Hans dopisuje wpis atomowo, uruchamia build i testy.
5. Dopiero komplet zielonych testów podmienia katalog serwowany przez Caddy.

Komenda Hansa nie jest jeszcze wdrożona. Składnia i dwuetapowa akceptacja wymagają decyzji Tomasza.

## Wdrożenie po decyzji

1. Tomasz ustawia rekordy A domeny głównej i `www` na `157.90.155.155`.
2. Uzupełnić dane kontaktowe, administratora RODO, opłaty/dokumenty i pozycję pinezki.
3. Zbudować i przejść testy oraz Lighthouse mobile.
4. Dodać mount `www_rod/dist:/srv/www_rod:ro` do kontenera Caddy i scalić blok hosta po kopii konfiguracji.
5. `caddy validate`, kontrola 200/308/404, certyfikatów, Barometru, linków i widoku telefonu; dopiero potem publikacja.

Cel Lighthouse po uruchomieniu domeny: Performance ≥95, Accessibility ≥95, Best Practices ≥95, SEO ≥95. W tym środowisku nie ma Chromium, więc wynik Lighthouse pozostaje **NIE WIEM** do testu na działającym URL.
