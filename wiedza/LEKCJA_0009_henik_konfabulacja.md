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
