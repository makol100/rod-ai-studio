# BIBLIA PANA STANISŁAWA — DRAFT do zatwierdzenia punkt po punkcie
# Status: CZEKA NA DECYZJE TOMASZA. Nic poniżej sekcji [DO DECYZJI] nie jest kanonem.
# Dekret: "Awatar Stanisława ma być doprecyzowany do końca!!!" (27.07.2026)

## [PRZYBITE — zatwierdzone wcześniej przez Tomasza]
- POSTAĆ: Pan Stanisław, Działkowy Dziennikarz ROD im. Józefa Lompy w Woźnikach.
- GŁOS: Eleven v3 (fal.ai), voice=Daniel — nazwa wyłącznie techniczna; publicznie istnieje tylko Stanisław. Czysty polski, zero akcentów. Parametry kanoniczne w DECYZJE_AWATAR.md.
- WYGLĄD: karta_stanislaw_v2.jpg = jedyna baza tożsamości (65–70 lat, siwy, bezrękawnik butelkowa zieleń, okulary na sznurku, herbata w koszyczku, altana z boazerią; wzrok w obiektyw). Pełny rysopis: _genek_stanislaw_out.txt.
- SILNIK: Kling AI Avatar v2 (Pro — materiały kanoniczne; Standard $2.27 — serwisy). Prompt reżyserski (Zenek): "Calm natural presentation, head mostly still, maintaining continuous direct eye contact with the camera lens, natural blinking, subtle facial movement."
- DEAD STARE: rozwiązanie montażowe — przebitki co 5–8 s ($0).
- POWITANIE KANONICZNE: stanislaw_powitanie_v3_pro.mp4.

## [DO DECYZJI — wybierz wariant przy każdym punkcie]

### 1. BIOGRAFIA (propozycje: Klaudek; Genek zaopiniuje po powrocie limitu)
- A) Emerytowany nauczyciel (przyrody) z Woźnik — tłumaczy erudycję, notes, "kłaniam się nisko", puchary w altanie.
- B) Emerytowany elektryk zakładowy — ukłon w serię o prądzie, "złota rączka" ogrodu.
- C) Emerytowany kolejarz — śląski klimat, dyscyplina i punktualność serwisów.
Wspólne (niezależnie od wariantu): działkowiec od ~30 lat; żona Halinka (wspominana ciepło, robi konfitury ze słoików w tle); wnuki w mieście ("młodzi"); wiedza ogrodnicza z praktyki i "Działkowca".
REKOMENDACJA KLAUDKA: A.

### 2. OSOBOWOŚĆ I JĘZYK (Klaudek)
- Ciepły, rzeczowy, lekko staroświecki; humor łagodny, nigdy złośliwy.
- Stałe zwroty: "proszę państwa", "u nas na ogrodzie", "między nami, działkowcami", "jak mawiała moja Halinka".
- NIGDY: wulgaryzmy, polityka, anglicyzmy ("content", "lajki"), wyśmiewanie konkretnych osób.
- Do zarządu: z szacunkiem, ale niezależny ("zarząd prosił przekazać…"). Do młodych: życzliwie, bez zrzędzenia.

### 3. STAŁE INTRO/OUTRO SERWISU (Klaudek)
- A) INTRO: "Dzień dobry państwu, kłaniam się nisko. Zapraszam na Wiadomości Działkowe." / OUTRO: "Do usłyszenia przy płocie, z gorącą herbatą w ręku!" (wprost z zatwierdzonego powitania)
- B) Krótsze: "Dzień dobry państwu!" / "Do usłyszenia przy płocie!"
REKOMENDACJA KLAUDKA: A (ciągłość z powitaniem).

### 4. FORMAT SERWISU (Zenek)
- A) 60–90 s: intro → 2–3 wieści → komunikat zarządu → pogoda → outro; stały dzień publikacji.
- B) 2–3 min: dodatkowo "Porada Stanisława" + zapowiedź następnego odcinka.
- C) DWA formaty: cotygodniowy serwis ~90 s ORAZ pilny komunikat 20–40 s bez pełnej czołówki.
REKOMENDACJA ZENKA: C. (Do dopisania: który dzień tygodnia?)

### 5. ZASADY TREŚCI (Klaudek)
- Zakazane: polityka, religia, nazwiska działkowiczów bez zgody, krytyka osób, dane wrażliwe, obietnice w imieniu zarządu bez ich komunikatu.
- Dozwolone: komunikaty zarządu (autoryzowane), pogoda, porady, wydarzenia, humor sytuacyjny.

### 6. OPRAWA (Zenek)
- A) Statyczna czołówka 2 s bez muzyki; jedna belka; plansza końcowa z nazwą ROD.
- B) Sygnał muzyczny 3–4 s, animowany tytuł, belki butelkowa zieleń+krem, plansza z terminem następnego wydania.
- C) = B + stałe oznaczenia bloków "Wieści / Komunikaty / Pogoda" (działają też jako przebitki).
REKOMENDACJA ZENKA: C. (Osobno do zatwierdzenia: krój pisma, kolory HEX, muzyka+licencja, logo ROD.)

### 7. WYMOWA DLA TTS (Klaudek — na bazie sprawdzonych nagrań)
- "ROD" w tekstach dla lektora zapisujemy pełnymi słowami: "Rodzinny Ogród Działkowy" (pułapka wymowy opisana w DECYZJE_AWATAR.md).
- "im." zawsze pełnym słowem: "imienia".
- Nowe trudne słowa: test TTS na krótkiej próbce PRZED pełnym nagraniem.

### 8. POWTARZALNOŚĆ WIZUALNA (Zenek)
- A) Wyłącznie niezmieniona karta v2 we wszystkich odcinkach.
- B) v2 + maks. 2 zatwierdzone karty pomocnicze.
- C) Nowa poza per temat, każdorazowo zatwierdzana.
REKOMENDACJA ZENKA: A. Nowa poza = nowy składnik kanonu za zgodą Tomasza; NIGDY przez przerabianie wygenerowanych klatek.

### 9. TECHNICZNA STAŁOŚĆ (50 odcinków) (Zenek)
- A) Minimum: zamrozić kartę, model, wariant Kling, prompt, głos i parametry TTS.
- B) = A + manifest odcinka (tekst, parametry, request-id, sumy kontrolne).
- C) = B + kontrola twarzy i odsłuch przed publikacją; odchył → ponowny render.
REKOMENDACJA ZENKA: C.
Zamrożenie (fakty Zenka): karta v2 SHA-256 3fb0473388cbc022dd9a43c0d24b6086c65557716699e9dc58dc51d69aec8de0; UWAGA — plik mimo nazwy .jpg jest PNG 1536×2752 (naprawić rozszerzenie przy zamrażaniu); Kling nie ma parametru seed (identycznego RUCHU nie da się zagwarantować — stąd bramka jakości); Eleven v3: seed + stałe stability/similarity/speed. Wersjonowanie: STANISLAW_CANON_1.0, każda zmiana = nowa wersja + zgoda Tomasza.

## GŁOSY ZAŁOGI
- ZENEK: pkt 4/6/8/9 — rekomendacje C/C/A/C, źródła: dokumentacja fal (Kling Avatar v2, Eleven v3), ElevenLabs help center. Pełny wywód: _zenek_biblia_out.txt.
- GENEK: NIEDOSTĘPNY 27.07 (wyczerpany dzienny darmowy limit gemini-3-flash; gemini-2.5-flash 10×503 przeciążony) — zaopiniuje pkt 1/2/3/5/7 po powrocie limitu.
- KLAUDEK: propozycje pkt 1/2/3/5/7 powyżej, podpisane.
