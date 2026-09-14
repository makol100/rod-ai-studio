# STRONA ROD — FILMY (stan 04.09.2026, dekrety D-0314 / D-0315)

## Dekrety Tomasza (dosłownie)
- D-0314: „Niech filmy otwierają się w oknie na stronie rodwozniki" (po telefonie od osoby, u której linki do rolek FB nie działały).
- D-0315: „Nie przenoś po kliknięciu na jakikolwiek film na YouTube czy Facebooka ma się to otwierać na stronie ROD Woźniki".
- ZAKAZ ściągania filmów z YouTube na VPS: „Po co kombinujesz jakieś ściąganie tych filmów… przecież można zrobić łącze… zapytaj Gienka bo on jest od Google".

## Jak jest zrobione
- www_rod/static/js/film-okno.js (v=20260904b, dołączony w templates/page.html): klik w element z data-wideo → okno z <video> (własny mp4, controls, playsinline, preload=metadata, poster); klik w element z data-yt → okno z iframe https://www.youtube-nocookie.com/embed/ID?autoplay=1&rel=0&modestbranding=1&playsinline=1 (przepis Genka, wzorzec fasady: miniatura i.ytimg.com/vi/ID/hqdefault.jpg, player ładuje się dopiero po kliknięciu); X / tło / Esc zamyka i usuwa player. BEZ style.inset (psuło stare telefony) — top/right/bottom/left.
- Rolki FB i film z ogłoszenia: własne mp4 w www_rod/static/wideo/ID.mp4 (te same pliki, które szły na FB); fb_na_strone.py sam dociąga brakujące z Graph API pole `source` (token strony w data/.secrets/fb_page_token). 22/22 skompletowane 04.09 (7 z lokalnych finałów, 15 z Graph).
- Karty w build.py (wideo_html): href = ścieżka mp4 (fallback bez JS zostaje na naszej domenie), data-wideo, data-mini; ogłoszenie z filmem: _ogl_film_html.
- YouTube (3 długie filmy: xKHxqNi02MQ prąd, 4tfLWG4fxHY Etap 3 — pion 9:16, b2f_srU7lF4 kuny): fasady w content/pages/filmy.md, elektryfikacja.md, dla-dzialkowcow.md, templates/home.html. Linki „Otwórz film na YouTube" usunięte.
- Genek o wtyczce FB video.php: blokuje niezalogowanych ekranem logowania — dlatego rolki grają z własnych mp4, nie z embedu FB.
- CSP (Caddyfile, vhost rodwozniki.pl): media-src 'self'; frame-src youtube-nocookie.com + youtube.com; img-src i.ytimg.com. HTTP/3 wyłączone globalnie (servers { protocols h1 h2 }) — głosy Genka i Henia: QUIC/UDP 443 to najczęstsza przyczyna „u innych nie działa"; zmiana Caddyfile = docker restart caddy-mcp (bind-mount przypina inode), restart zrywa konektor fabryka na ~10 s.
- Bramka po każdej zmianie: /tmp/pup_film2.js (puppeteer w zenika/alpine-chrome) — klik → gra (currentTime>0) / iframe obecny, X zamyka; 5 miejsc: /filmy/ mp4, /filmy/ YT, / film-mini, /elektryfikacja/, /ogloszenia/.
- Deploy ręczny = podmiana katalogu wolumenu KASUJE pogoda.json i licznik.json → po podmianie odpalić tools/pogoda_rod.py i tools/licznik_rod.py.

## Otwarte
- ZAMKNIĘTE 04.09 wieczorem (Tomasz: „4 naprawione") — po wyłączeniu HTTP/3 i poprawce inset filmy działają u innych.
