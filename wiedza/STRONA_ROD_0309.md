# rodwozniki.pl — stan po sesji 03.09.2026 (czytać przy pracy nad stroną ROD)

## CO JEST NA STRONIE (żywe, https://rodwozniki.pl)
- Generator: www_rod/build.py (markdown+JSON → dist → wolumen Caddy /var/lib/docker/volumes/caddy_mcp_data/_data/www_rod). Cache-bust hash na CSS/JS.
- Podstrony: start, ogłoszenia, dla-działkowców, dokumenty, elektryfikacja (galeria 12 zdjęć + film YT), filmy (rolki YT + FB), o-ogrodzie, patron (Józef Lompa), kontakt (formularz + mapa Google), prywatność/RODO, 404.
- Hero: logo ROD z ANALOGOWYM ZEGAREM (same wskazówki, czarne, grube z jasną obwódką dla starszych, wspólny środek — transform-box: view-box, origin 50px 50px; NIE fill-box!) + DATA pod logo (sama data bez godziny, w hero-visual flex column).
- Pasek WYSZUKIWARKI GOOGLE: pełna szerokość pod nagłówkiem (.g-pasek-rzad, width var(--shell)), action google.com/search target _blank. UWAGA: CSP musi mieć form-action 'self' https://www.google.com — inaczej Enter nie działa!
- POGODA: Open-Meteo (Woźniki 50.588,18.989), teraz domyślnie + prognoza 8 dni po kliknięciu; cron tools/pogoda_rod.py co 30 min → /pogoda.json.
- RADAR OPADÓW: mapa Leaflet (cdnjs 1.9.4) + IMGW SCENE/MERGE INCA — PROGNOZA DO 6H w przód (36 klatek co 10 min, model AROME+POLRAD). Proxy apps/api/src/radar_rod.py (/radar/meta, /radar/kafel/{ts}/{z}/{x}/{y}.png — IMGW ma z/y/x!). Oś czasu z tilesources-a.imgw.pl/vector/tms.xml. Atrybucja IMGW-PIB. Plan B jak padnie: LibreWXR api.librewxr.net (tylko 1h nowcast) lub RainViewer (tylko przeszłość). CSP: img-src +tile.openstreetmap.org +*.tile.openstreetmap.org +cdnjs; script/style-src +cdnjs +unsafe-inline.
- LICZNIK odwiedzin: z logów Caddy, cron tools/licznik_rod.py co 5 min → /licznik.json (NIE mój API — zostaje wersja z logów).
- KAMERY: osobno https://kamery.rodwozniki.pl (za hasłem, LibreWXR-relay IMGW... nie — to VTM Hik-Connect, patrz kuny-monitoring). Link w hero (przycisk Kamery).
- SEO: zweryfikowane w Google Search Console (plik google9886392fdebaacb5.html w www_rod/static/root/ → dist), sitemap.xml zgłoszony. Wizytówka Google Maps ROD wskazuje na stronę (Tomasz ustawił witrynę w profilu).
- Bot ogłoszeń @RodOgloszenia_bot (tools/ogloszenia_bot.py, ogloszenia-bot.service): Tomasz + zarząd (dopisywany przez przesłanie KONTAKTU w bocie). Lista /root/skrzynka/ogloszenia_zarzad.json (na 03.09 pusta — tylko Tomasz).

## DEKRETY WIZUALNE TOMASZA (grafika ZOSTAJE — inne strony ROD są wizualnie chujowe)
- Paleta jasna ogrodowa: #2e7d4f zieleń, krem #fffdf6, złoto #e5b744. NIE ciemna/wojskowa.
- Logo oryginalne okrągłe (assets/branding/rod_logo_kolo.png). Rok założenia 1948.
- Usunięte przez Tomasza: barometr grzybiarza, "51 działek" (dymek z hero), mapa ogrodu, zdublowana karta Kamery, zdublowany licznik.
- Zdjęcie na głównej = wachlarz kabli (BUD-2), nie szafki.

## AUTOMAT FB→STRONA (w toku): tools/na_strone.py — dodaje opublikowany film FB na stronę (miniatura+link). content/fb_filmy.json. NIE dokończone podpięcie do build.py/publikuj_prezenter.py.

## ŹRÓDŁO CODZIENNYCH POSTÓW FB (ustalone 03.09 przez FB Graph API): aplikacja "Ogrodnik ROD" publikuje na stronę FB (page 1174205105781401) codziennie: ~6:32 powitanie z datą ("Dzień dobry, Sąsiedzi! 🌿 <dzień, data>") + ~9:02 porada/temat działkowy ("🌱 Wrzesień na działce...", "🔌 Bezpieczeństwo elektryczne...", "🤝 Razem raźniej..."). To TEKSTY, nie filmy. NIE idzie z VPS (ostatni skrypt fabryki 01.09) ani z HA Dom (83 automatyzacje, żadna na FB) ani z Działki (leży). Gdzie fizycznie mieszka "Ogrodnik ROD" — DO USTALENIA (narada /tmp/n_fb630). Token FB: data/.secrets/fb_page_token. DEKRET Tomasza: te codzienne teksty mają też trafiać na rodwozniki.pl automatycznie.

## LEKCJE
- Caddyfile zamontowany single-file: sed -i tworzy nowy inode → kontener widzi starą wersję. Edytować open('w') w miejscu, reload. Blok rodwozniki.pl to linia ~282, CSP linia ~292.
- Git: praca była na gałęzi zenek-warsztat, nie main — pushować i scalać do main! (03.09 zaległo 100 commitów).
- Playwright test + qwen2.5vl:7b (VLM) do weryfikacji wyglądu strony — /tmp/pwenv, chrome w /tmp/n_kamery_live/henio_artifacts.
