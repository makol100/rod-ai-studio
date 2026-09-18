# Dodatki na rodwozniki.pl z 18.09.2026 (D-0430) — pkt 2, 4, 6, 12, 13 narady www/FB

Dekret: 16:14 „2, 6, 12, 13 nie kasuj mi tej pogody z główne!" + 16:16 „4." ze składem zarządu. Reguła nadrzędna D-0418: nic nie usuwać, tylko dodawać. Koszt 0 zł.

## Co i gdzie
- pkt 2 „Dziś w ROD": `dzis_w_rod_html()` w build.py, placeholder `{{dzis_w_rod}}` w home.html tuż pod podziękowaniami, nad hero. Trzy kafle: Pogoda teraz (app.js dopisuje z TEGO SAMEGO pogoda.json: ikona, temp, opis + min/max/opady dnia), najnowsze Wiadomości z ogrodu (wideo.json, kategoria wiadomosci, otwiera film w oknie), Stan robót (wpis „trwa"). Data po polsku (pierwsza litera wielka, miesiąc małą). Sekcja pogody `#pogoda` niżej NIETKNIĘTA — test pilnuje.
- pkt 4 `/zarzad/`: content/pages/zarzad.md (lista `.zarzad-lista`), menu po „O ogrodzie", stopka „Zarząd ogrodu". Skład dosłownie od Tomasza; godzin dyżuru NIE podał → nie ma; kontakt e-mail + formularz + 991.
- pkt 6 „Stan robót": content/stan_robot.json (status zrobione/trwa/nastepne, data, tytuł, opis, link, ŹRÓDŁO każdego wpisu), `stan_robot_html()`, sekcja `#stan-robot` na głównej przed Elektryfikacją. Aktualizacja = dopisać wpis + build + deploy. Kolejność: trwa → następne → zrobione.
- pkt 12: styles.css blok `@media (max-width: 640px)`: body 18 px, linki menu min-height 44 px, text-link/footer-links 44 px, .button 50 px. Fraunces bez zmian.
- pkt 13: dla-dzialkowcow.md — „[DO POTWIERDZENIA]" zastąpione prawdą („ustalisz z zarządem: e-mail/formularz"); filmy.md — „kliknięcie otwiera nagranie w oknie na tej stronie" (D-0314); page.html — szukajka to Google z `as_sitesearch=rodwozniki.pl`, placeholder „Szukaj na tej stronie…" (dłuższy ucinał się na telefonie — oko Genka); app.js — licznik: „Odwiedziny: dziś X · od 3.09: Y odwiedzin (Z odsłon). Liczymy odwiedziny dzienne po adresie sieci, bez robotów i bez ciasteczek" (licznik_rod.py liczy unikalne IP NA DZIEŃ i sumuje — „gości" było mylące).

## Kontrola
- Test żywy: www_rod/tests/test_dodatki_1809.py (pasek nad hero, pogoda została, ≥3 wpisy stanu robót z 3 etykietami, 5 nazwisk na /zarzad/, link w menu, brak [DO POTWIERDZENIA], nowy opis /filmy/, as_sitesearch, etykieta licznika, 18 px/44 px w bloku mobile, Fraunces, 8 sekcji głównej nadal obecnych) — ZIELONY 18.09.
- Oko Genka (arkusz 3 zrzutów mobile): teksty czytelne, etykiety Zrobione/Trwa/Następne czytelne; uwagi wdrożone: placeholder szukajki skrócony, .stan-meta 1 rem.
- Znany, starszy fail testów build: test_no_remote_scripts_or_styles (leaflet z CDN dla radaru) — nie z tej zmiany.
- Pułapka: port 8765 na VPS to serwer MCP fabryki (claude-vps-mcp) — do podglądu dist używać innego portu (8791). Playwright na lokalnym http.server: `wait_until="load"`, nie networkidle (radar/leaflet nie kończą sieci).

## Zostało z listy dodatków (czekają na „rób"): 3 Opłaty (treść od Tomasza), 5 brakujące treści (walne, wolne działki, śmieci, woda, dyżury — treść od Tomasza), 7 Kronika od 1948, 8 Jedno pytanie z alejki, 9 Działka i człowiek, 10 Plon idzie dalej, 11 Co to za roślinka?
