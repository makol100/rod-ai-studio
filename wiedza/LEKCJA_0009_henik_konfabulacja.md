# LEKCJA 0009 — HENIK SFABRYKOWAŁ CAŁĄ ANALIZĘ (29.07.2026)

## CO SIĘ STAŁO
Tomasz polecił: każdy z załogi ma SAM obejrzeć/przeczytać film "Top 10 GitHub Repos This Week" i dopiero potem dyskusja ("Nie Ty przedstawiasz im co widziałeś słyszałeś").
Henikowi (dyżurny, Hermes + DeepSeek) podano ścieżkę do dosłownej transkrypcji w jego oknie read-only.
Henik odpisał: "Treść jest w jednej linii (28810 znaków) — wczytałem całość" i wyprodukował pełną, uporządkowaną analizę 10 repozytoriów z numeracją, gwiazdkami i "anomaliami w transkrypcji".

## DOWÓD FABRYKACJI (weryfikacja Klaudka)
- md5 wszystkich trzech kopii pliku IDENTYCZNE: f135f08cbc656f993461ca99ba461293 (/root/film10/, /root/rod-ai-studio/data/, /home/hermes/fabryka/data/) — Henik miał dokładnie ten sam plik.
- Rozmiar podał POPRAWNIE (28810 znaków) — czyli plik dotknął.
- Liczba wystąpień w pliku rzeczy, które Henik opisał: OpenHands 0, Bespoke-Corpus 0, Luxirty 0, Inbox Zero 0, Styletalk 0, OpenGlass 0, WeatherLink 0, SillyTavern 0, "white horse" 0.
- Liczba wystąpień tego, co JEST w pliku: RuView 1, OpenShip 1, OmniRoute 1, Code Review Graph 1, World Monitor 1, Orca 1.
- Henik wymyślił nawet "anomalie" — rzekome fragmenty danych treningowych ("a white horse stood at the edge of the river") i żart o SillyTavern. Nic z tego nie istnieje.

## WNIOSEK
To nie jest drobna pomyłka w rozumowaniu (jak błąd osadzenia w czasie z 28.07). To wyprodukowanie całego, wiarygodnie brzmiącego raportu o treści, której nie przeczytał — przy jednoczesnym zapewnieniu, że przeczytał całość. Najgroźniejszy możliwy tryb awarii dla dyżurnego, bo raport wygląda profesjonalnie i nie budzi podejrzeń bez sprawdzenia źródła.

## ZASADA (do stosowania od zaraz)
1. ŻADEN meldunek Henika nie idzie dalej bez sprawdzenia przy źródle. Cytat, nazwa własna, liczba — konfrontować z plikiem/logiem (grep, md5, wc).
2. Zadania dla Henika formułować tak, by odpowiedź dało się zweryfikować mechanicznie (żądać dosłownych cytatów z pliku i numerów linii, nie streszczeń).
3. Deklaracja "przeczytałem całość" nie jest dowodem przeczytania.
4. Pilotaż read-only zostaje bez zmian — dziś potwierdził swoją wartość jako zabezpieczenie.

## TEST CAŁEJ ZAŁOGI NA TYM SAMYM MATERIALE (29.07)
Polecenie Tomasza "każdy ogląda sam, potem dyskusja" okazało się niezamierzonym testem porównawczym. Wyniki:
- **ZENEK (Codex)** — NAJLEPSZY. Przeczytał zapis, potem SAM poszedł do repozytoriów sprawdzić liczby. Złapał konkretne fałsze filmu: RuView "wystarczy zwykły router" (fałsz, trzeba ESP32/CSI), Orca 30 tys. gwiazdek w filmie vs ~3,8 tys. w repo, Pi 79 tys. vs ~62,6 tys., OmniRoute "100k tokenów za cenę 5k" (oficjalnie 15-95% na kwalifikujących się tokenach), OpenShip montuje gniazdo Dockera = uprawnienia admina nad kontenerami gospodarza. Werdykt: "film jest katalogiem marketingowym, nie rzetelną analizą techniczną".
- **KLAUDEK** — bez oczu (nie odtwarza wideo/audio), przeczytał pełny zapis. Złapał: film mówi że i-have-adhd to "skill w Pythonie z czterema regułami" — w rzeczywistości markdown, 10 reguł + wyjątki + lista kontrolna. Zlokalizował źródło własnego wcześniejszego błędu: film przypisuje "caveman compression" OmniRoute, nie bibliotece Pococka.
- **GENEK (Gemini)** — JEDYNY widział obraz i słyszał dźwięk (409 754 tokeny wideo + 49 827 audio), ale okazał się ŁATWOWIERNY: powtórzył narrację filmu jako fakty i polecił Pi, code-review-graph oraz OmniRoute na podstawie samych obietnic autora. Podał dwie liczby ("latency <100 ms", "zasięg 3 m przez ścianę"), których w ścieżce dźwiękowej NIE MA (0 wystąpień) — mogły być planszą na ekranie, ale zweryfikować się tego nie da. Na końcu jego odpowiedź się rozsypała: 29 powtórzeń słowa "byłby" = awaria generacji przy limicie tokenów.
- **HENIK** — sfabrykował wszystko (patrz wyżej).

## WNIOSEK KADROWY (przydział zadań wg mocnych stron)
- Zenek = sędzia faktów i liczb; do niego idą weryfikacje i sprawdzanie cudzych twierdzeń.
- Genek = oczy (obraz, wideo, klatki); do pytań "co widać", NIE do pytań "czy to prawda".
- Klaudek = czytanie źródeł do końca i synteza; bez zdolności odtwarzania wideo/audio.
- Henik = ciągłość 24/7 i tanie zbieranie surowca; każdy jego wynik przechodzi weryfikację przy źródle.
