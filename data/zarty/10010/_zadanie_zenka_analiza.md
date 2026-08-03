# NARADA TRÓJKI — analiza FAIL strażników (re-roll 10010)

Rola: Zenek, pracownik. Protokół trójki (decyzja Tomasza): Twoja analiza zderza się z diagnozą szefa (Klaudka) i pomiarami strażników — masz się ZGODZIĆ albo UZASADNIĆ SPRZECIW dowodami. Nie zapisujesz nic na dysk; wynik na stdout, po polsku.

## Materiał (czytaj w całości)
1. data/zarty/10010/raporty/straznik_reroll.txt — werdykty kanarka dla 4 klipów re-rollu
2. wiedza/DECYZJE_10010.md — ogon (ostatnie ~15 wpisów): pełna historia dnia z pomiarami

## Twarde dane z pomiarów (z DECYZJE, do zderzenia)
- Referencja bohater_noc.jpg jest ZDRYFOWANA: 0.59-0.63 vs reszta biblioteki (baza↔karta mają 0.92)
- Kadr k04 mierzy 0.46 vs biblioteka; w kanarku2 klip był WIERNY kadrowi (0.39-0.87 vs kadr), a vs biblioteka 0.25-0.40
- Kadr k06 mierzy 0.33 vs biblioteka — zaakceptowany OKIEM Tomasza (mimika osłupienia zaniża pomiar)
- Zmierzona zasada dnia: Veo "zjada" ~0.25 podobieństwa w ruchu
- k01/k05 (kadry 0.55-0.58) przeszły kanarka PASS przy TEJ SAMEJ referencji
- Dziś: k02 PASS, k05 PASS, k04 FAIL (kl_01 sim 0.09 "obca twarz"), k06 FAIL (kl_00 0.27, kl_02 0.26)

## Hipotezy szefa (zweryfikuj, nie przytakuj)
H1: kl_01 w k04 (sim 0.09) to klatka z twarzą pod kątem/w cieniu/z otwartymi ustami — nie obca osoba
H2: k06 0.26-0.27 przy kadrze 0.33 minus ruch = TA SAMA osoba, pomiar zgodny z oczekiwaniem
H3: przyczyna źródłowa = dryf aktywu bohater_noc.jpg, nie zepsucie klipów
H4: rozstrzygnięcie = pomiar klatek klipu vs ZAAKCEPTOWANY KADR (nie vs biblioteka)

## Zadania
1. DIAGNOZA: co naprawdę mówią te FAIL-e? Zgoda/sprzeciw wobec H1-H4, z uzasadnieniem.
2. WERYFIKACJA $0: napisz KOMPLETNY skrypt Pythona (do uruchomienia przez szefa w kontenerze, /app/venv/bin/python, insightface buffalo_l dostępny), który dla klipów k04 i k06 (_reroll.mp4): wyciąga klatki co 1 s (ffmpeg), mierzy cosine podobieństwo twarzy każdej klatki (a) vs kadry/kXX.jpg (zaakceptowany kadr) i (b) vs assets/zarty/karty/bohater_noc.jpg, wypisuje tabelę i werdykt: WIERNY KADROWI / OBCA TWARZ. Ścieżki bezwzględne, zero zapisu poza /tmp.
3. PROPOZYCJE NAPRAWY: minimum 2 warianty z kosztami w $ (stawki: klip Veo lite $0.64, edycja kadru $0.15), przy budżecie $11.09/12.

## Format wyniku
Sekcje: DIAGNOZA / WERDYKT WOBEC HIPOTEZ (H1-H4: zgoda/sprzeciw + 1 zdanie) / SKRYPT (blok ```python```) / PROPOZYCJE (z $).
