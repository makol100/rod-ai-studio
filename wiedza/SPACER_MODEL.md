# MODEL WDROŻENIA SPACERU 360 (zapisany na polecenie Tomasza 04.09.2026)
Wzorzec sprawdzony na żywo (proba: parking+plac zabaw, Herzogenburg) — powielać 1:1 przy spacerze w ogrodzie.

## Zdjęcia
1. Apka: 360 Photo Cam (com.dospace.photo360) na Foldzie — pełna sfera 8192×4096, szwy czyste.
2. Pobranie: android_share_file_via_web(location_id+path) → curl na VPS (przy zerwaniu LTE ponawiać CAŁOŚĆ; brak wznowień Range).
3. Oryginały → data/spacer_oryginaly/ ; wersja web 4096×2048 JPEG q85 → www_rod/static/spacer/{nazwa}.jpg (~2 MB/scena).

## Strona (Pannellum 2.5.6, self-hosted)
- Pliki: static/spacer/pannellum.js, pannellum.css, {tour}.js (konfiguracja scen), {tour}.html.
- CSP strony wymusza: ZERO inline <script> (kod wyłącznie w plikach .js); img-src musi mieć blob: (JUŻ dopisane w Caddyfile:292 — nie ruszać).
- Caddyfile: bind-mount read-only przypina inode — po każdej edycji na hoście `docker restart caddy-mcp` (reload NIE wystarcza).
- Strzałki przejść: hotspot type:'scene', cssClass:'strzalka' — 120 px, tło rgba(183,225,195,.92) pastelowa zieleń, biała obwódka 3 px, glif ➤ #1b5e20 (zaakceptowane przez Tomasza 04.09).
- Sceny: type equirectangular, autoLoad, sceneFadeDuration 900, autoRotate -3 (stop po dotknięciu), hfov 100.

## Dowód działania (bramka obowiązkowa PRZED wysłaniem linku Tomaszowi)
docker zenika/alpine-chrome:with-puppeteer (NODE_PATH=/usr/src/app/node_modules) → realne czekanie ≥12 s → zrzut → oczy Genka + zero błędów konsoli. Wzorzec skryptu: /tmp/pup_test.js.

## Plan na ogród (do decyzji Tomasza po burzy mózgów 04.09)
- Punkty i gęstość: patrz DECYZJE po naradzie.
- Integracja z mapą ogrodu (/mapa/, statyczny JPG w lightboxie): klikalne punkty na mapie → /spacer/#scena=X (Pannellum czyta hash → firstScene). Bez inline JS.

## NARADA 04.09.2026 (głosy: /tmp/narada_spacer2/, skopiowane do wiedza/narady/spacer2/)
P1 GĘSTOŚĆ — rozbieżność: Zenek 10 m, Henio 10 m (5 m przy bramach/skrzyżowaniach, 12 m gdy alejki >400 m), Genek 15 m. Punkty obowiązkowe (zgodni): 4 bramy, 2 parkingi, Dom Działkowca, każde skrzyżowanie, końce alejek. Szacunek: ~38-51 sfer, sesja 2-4 h (przy długich alejkach dzielić na 2). PRZED SESJĄ: zmierzyć realną łączną długość 3 alejek (Henio) — od tego zależy liczba sfer.
P2 MAPA→SPACER — JEDNOGŁOŚNE 3/3: kontener position:relative z <img> mapy + absolutnie pozycjonowane <a> w PROCENTACH (skaluje się na telefonie) → href="/spacer/#scena=X"; tour.js (plik, nie inline — CSP) czyta window.location.hash i ustawia scenę, a po scenechange aktualizuje hash. ODRZUCONE <map><area> (piksele, nie skaluje na mobile). Punkt na mapie: kropka ~32 px w stylu strzałek (pastelowa zieleń + biała obwódka), niewidzialne pole dotyku ≥44×44 px, ~10 punktów wejścia (bramy, środki alejek, parkingi, Dom). Mini-mapa WEWNĄTRZ spaceru z kropką "jesteś tu" (event scenechange): wszyscy na TAK, Henio jako faza 2 po MVP.
DECYZJA TOMASZA (otwarta): 10 m czy 15 m między sferami.
