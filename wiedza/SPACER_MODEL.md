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

## D-0311 (04.09, zastępuje wcześniejsze podejście nawigacji) — WZORZEC OSTATECZNY PROBY
- Na starcie ekran "Ładowanie spaceru…" z paskiem % liczonym PO BAJTACH (HEAD Content-Length wszystkich sfer → fetch streamem, licznik odebranych): CAŁY spacer wczytuje się z góry do blobów, chodzenie potem BEZ żadnych pobrań (dowód: licznik żądań .jpg po załadowaniu = 0).
- Sceny dostają blob-URL-e; wymaga w CSP rodwozniki: img-src blob: ORAZ connect-src blob: (oba już w Caddyfile:292; Pannellum czyta panoramę XHR-em, więc sam img-src NIE wystarcza — bez connect-src blob: pada "FileReader parameter 1 is not of type Blob"). Po edycji Caddyfile: docker restart caddy-mcp.
- ignoreGPanoXMP: true w default (nie parsujemy XMP z blobów).

- UWAGA SKALA: pełny ogród ~40 sfer × ~2 MB = ~80 MB ładowane z góry (wola Tomasza D-0311). Przy budowie /spacer/ rozważyć web 3072×1536 q80 (~1,2 MB/sfera → ~50 MB) — decyzja przy sesji.

## STRZAŁKA — WZÓR ZATWIERDZONY (Tomasz 04.09.2026, "Brawo brawo")
120 px, środek CAŁKOWICIE przezroczysty, obwódka 3 px biała rgba(255,255,255,.75),
grot \27A4 BIAŁY rgba(255,255,255,.92), cień 0 2px 10px rgba(0,0,0,.30).
NIE zmieniać rozmiaru ani kolorów bez polecenia Tomasza.

## PRZEJŚCIA I TRASA SESJI (Tomasz 04.09.2026, D-0313: sfery co 10 m)
Przejścia poprzeczne (pion na mapie):
- 36|37: Alejka Północna -> Alejka Środkowa (koło wschodniego rogu Domu Działkowca)
- 21|22 -> 16|15: Alejka Środkowa -> Alejka Południowa (jedna linia)
- 43|44: Alejka Północna -> Parking nr 2 (trójkąt na górze mapy)
TRASA (kolejność zdjęć = kolejność sąsiedztwa): 1 Brama1+Parking2 wschód -> 2 przejście 43|44 w dół ->
3 Północna na zachód do Bramy2 -> (powrót do 36|37) -> 4 przejście w dół -> 5 Środkowa zachód: Dom Działkowca,
Parking1, Brama3 -> (powrót) -> 6 Środkowa wschód do końca -> (powrót do 21|22) -> 7 przejście w dół ->
8 Południowa zachód do Bramy4 -> (powrót) -> 9 Południowa wschód do końca. Zdjęcia co 10 m (~13 kroków),
obowiązkowo: bramy, skrzyżowania, końce alejek, oba końce + środek każdego przejścia.
Rysunek trasy przekazany Tomaszowi (trasa-spaceru.jpg, lokalnie u Klaudka).

## WYMIARY (Tomasz 04.09.2026, „mniej więcej")
Każda działka 20 m × 25 m; 25 m liczone od strony alejki (w głąb), 20 m wzdłuż alejki. Przejścia biegną wzdłuż boku 25 m — jedna kondygnacja działek w przejściu = 25 m.
Wyliczenia (co 10 m): alejka 9 działek × 20 m ≈ 180 m → 19 sfer; trzy alejki 57; Parking 2 wzdłuż ≈ 180 m → ~19 (można rzadziej, płasko); przejścia 36|37 i 21|22→16|15 po 2 kondygnacje ≈ 50 m → 6 sfer każde, 43|44 ≈ 25 m → 3; Parking 1 + Dom Działkowca 3–4. RAZEM ≈ 90 sfer, sesja 2–3 h. (Do potwierdzenia przez Tomasza — „mniej więcej".)

## KONWENCJA NAZW SFER (Tomasz 04.09.2026: „nazwanie tych zdjęć z tymi numerami żeby było łatwiej to poskładać")
Punkty z tools/spacer_punkty.py (92, co 10 m, numer = kolejność trasy; data/spacer_oryginaly/punkty.json z x_proc/y_proc).
Sfera = numer punktu: oryginał data/spacer_oryginaly/pNN.jpg, web www_rod/static/spacer/pNN.jpg, scena Pannellum "pNN".
Tomasz robi zdjęcia w kolejności numerów bez pomijania; apka zapisuje z czasem → kolejność czasowa = numer; powtórka punktu = ostatnie zdjęcie z tego miejsca zastępuje poprzednie. Jeśli podpisuje numerem przy wysyłce — tym lepiej, ale nie musi.
Graf sąsiadów: kolejne numery w obrębie odcinka sąsiadują; na skrzyżowaniach (18/22/42/47/73 i bramy) dokładam połączenia poprzeczne wg trasy.

## ODBIÓR SFER Z TELEFONU (Tomasz 04.09.2026: „Najlepiej jak wejdziesz na telefon po wszystkie zdjęcia z pliku")
Stan zmierzony: apka MCP widzi tylko korzenie builtin:downloads/pictures/movies/music, podfoldery (np. Pictures/My360s) niewidoczne; sfery testowe przyszły przez Telegram. Dwie drogi na poniedziałek:
1) ADB po WiFi ogrodu (mesh Działki) przez Tailscale: telefon na WiFi + debugowanie bezprzewodowe + Tailscale → port odczytać z ekranu (MCP: android_get_screen_state w Ustawienia → Opcje programisty → Debugowanie bezprzewodowe) → adb connect 100.101.116.106:PORT → adb pull tylko nowych plików z folderu apki 360 Photo Cam (folder i nazewnictwo do ustalenia przy pierwszym wejściu).
2) Zapas: w apce MCP dodać własną lokalizację (SAF) wskazującą folder sfer — wtedy list_files/share_file_via_web widzą pliki jako korzeń.
DO ZROBIENIA dziś wieczorem, gdy Tomasz będzie na działce (WiFi): przetestować drogę 1, zapisać folder + wzorzec nazw, przygotować tools/spacer_odbior.py (pull + nazwanie pNN wg kolejności czasu).
