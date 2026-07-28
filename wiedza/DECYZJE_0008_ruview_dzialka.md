# DECYZJA 0008 — RuView (WiFi CSI) IDZIE NA HA DZIAŁKA (28.07.2026)

## SŁOWA TOMASZA (dosłownie)
"Takie coś to na HA działka"
(poprzednio, tego samego dnia: "2. Ogarniam esp32")

## SKUTEK
- Rekomendacja załogi z 28.07 (Zenek + Genek jednogłośnie: pierwszy węzeł w DOMU) — **NIEWAŻNA**. Obowiązuje słowo Tomasza.
- Dokument wiedza/PILOTAZ_RUVIEW.md w części "MIEJSCE: DOM" jest nieaktualny — poprawiony tą decyzją.
- Miejsce pilotażu: **HA DZIAŁKA (Woźniki, ~600 km od domu)**.

## UZASADNIENIE MERYTORYCZNE (Klaudek, po fakcie decyzji)
Decyzja ma sens użytkowy, którego załoga nie doceniła, patrząc tylko na ryzyko serwisowe:
1. WARTOŚĆ JEST TAM, GDZIE TOMASZA NIE MA. W Domu obecność jest znana; na Działce (pusta większość roku, bez kamer) informacja "ktoś jest na terenie / w altanie" ma realną wartość.
2. WARUNEK KALIBRACJI SPEŁNIONY NATURALNIE. Firmware wymaga startu w PUSTYM pomieszczeniu przez pierwsze 60 s — na Działce to stan domyślny, w Domu trzeba by go wymuszać.
3. MNIEJ ZAKŁÓCEŃ RF. Brak mikrofalówki w ciągłym użyciu, mniej sąsiednich AP skaczących mocą niż w zabudowie mieszkalnej.
4. KOREKTA (weryfikacja 28.07): teza "brak kamer" jest BLEDNA — na Dzialce sa kamery (np. camera1 "Garaz poludnie", nagrywanie ON). Argument zawezony: CSI ma sens tam, gdzie kamery nie siegaja lub sa niewskazane (wnetrze altany, pomieszczenia).

## KOSZT DECYZJI (do zaadresowania w planie, NIE kontrargument)
- Instalacja i pierwsza kalibracja MUSZĄ odbyć się podczas pobytu Tomasza na miejscu.
- Zawieszony ESP32 = brak obecności do następnej wizyty → OBOWIĄZKOWO gniazdko sterowane (Zigbee) do zdalnego power-cycle + automatyzacja watchdog.
- Agregator Rust musi działać lokalnie na serwerze Działki (N150), nie na VPS.

## STATUS 28.07 (późny wieczór) — ODPUSZCZONE
SŁOWA TOMASZA (dosłownie): "Narazie odpuszczam punkt 2"
- Pilotaż RuView/WiFi CSI **WSTRZYMANY**. Nic nie kupujemy, nic nie budujemy, nie wracamy do tematu z własnej inicjatywy.
- Dokumentacja (ten plik + PILOTAZ_RUVIEW.md) zostaje jako gotowy materiał na wypadek powrotu — cała robota rozpoznawcza jest zrobiona, przy wznowieniu startujemy od planu, nie od zera.
- Wznowienie WYŁĄCZNIE na wyraźne słowo Tomasza.
