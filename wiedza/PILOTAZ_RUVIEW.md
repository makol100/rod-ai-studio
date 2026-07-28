# PILOTAŻ RuView (WiFi CSI) — decyzja i plan (28.07.2026)
DECYZJA TOMASZA: "2. Ogarniam esp32" — sprzęt bierze na siebie, temat #2 z analizy 10 repo wchodzi do realizacji jako pilotaż.

## WERDYKT ZAŁOGI (jednogłośny)
- Zenek: pilotaż TAK, ale wyłącznie odizolowany eksperyment; 82.3% dokładności + problemy kalibracji wykluczają produkcję.
- Genek: TAK z dużą ostrożnością; technologia nowa, wymaga weryfikacji w realnym środowisku.
- MIEJSCE: **DOM (Walding)** — jednogłośnie. Nigdy Działka jako pierwsza (600 km, awaria = martwy sprzęt do następnej wizyty).
- UŻYCIE: sygnał pomocniczy do automatyki niekrytycznej, obserwacja trendów, fuzja/porównanie z mmWave. NIE: alarmy, ochrona, wykrywanie upadków w realnym użyciu, cokolwiek zdrowotnego.
- VITALS (HR/BR z WiFi): zabawka badawcza. Brak walidacji, wrażliwość na zakłócenia. Zero decyzji zdrowotnych.
- WARUNEK STOPU (Zenek): po prawidłowej kalibracji i 7 dniach porównania z czujnikiem referencyjnym — jeśli RuView myli obecność w >10% obserwowanych okresów, kończymy i zostajemy przy mmWave.

## FAKTY TECHNICZNE (zweryfikowane web_search 28.07)
- Sprzęt: ESP32-S3-DevKitC-1 (potwierdzony w tutorialu autora, ADR-018), ESP32-S3 SuperMini (binaria 4MB), ESP32-C6 (binaria c6-adr110). KLASYCZNY ESP32 NIE — potrzebne CONFIG_ESP_WIFI_CSI_ENABLED i binaria tylko dla S3/C6.
- Gotowe binaria = flash esptool, bez kompilacji (opcjonalnie build w Dockerze espressif/idf:v5.4).
- Łańcuch: ESP32-S3 (promiscuous, ~20 Hz CSI) --UDP:5005--> sensing-server Rust (obraz ruvnet/wifi-densepose:0.7.0, --net=host) --MQTT--> HA auto-discovery = 21 encji/węzeł + 3 blueprinty. Tryb --privacy-mode wycina HR/BR/pozę z wire.
- Samokrytyka README: uczciwa dokładność v2 = 82.3% (wcześniejsze "100% obecności" WYCOFANE — mierzone na nagraniu jednoklasowym).
- Zastrzeżenia firmware (Tier 2): pierwsze 60 s = autokalibracja (start musi być w PUSTYM pomieszczeniu, inaczej power-cycle); mikrofalówka/wentylator przy antenie/skoki mocy sąsiednich AP = fałszywa obecność do rekalibracji; poprawka autokalibracji dopiero w drodze (#491).

## STAN INFRASTRUKTURY DOM (zweryfikowane przez MCP 28.07)
- HA Dom: HAOS/Supervised, wersja 2026.7.2, Firebat S1, strefa Europe/Vienna.
- Mosquitto broker: ZAINSTALOWANY I DZIAŁA (core_mosquitto 7.1.0) — wymóg RuView spełniony.
- Zigbee2MQTT działa (MQTT w realnym użyciu).
- ESPHome Device Builder działa (2026.7.2) — gotowa droga do czujnika referencyjnego mmWave.
- LOKALNE ADD-ONY DZIAŁAJĄ: istnieje `local_s1panel` (S1 Panel LCD) — precedens; agregator Rust można opakować jako lokalny add-on (Dockerfile FROM ruvnet/wifi-densepose:0.7.0, host network), zamiast walczyć z dockerem na HAOS.
- Advanced SSH & Web Terminal zainstalowany.
- UWAGA (do zgłoszenia Tomaszowi): dwa add-ony w stanie ERROR — `a0d7b954_mqtt-io` (MQTT IO) i `605cee21_aegisbot` (AegisBot).

## PLAN (do zatwierdzenia)
1. Sprzęt (Tomasz): 1× ESP32-S3-DevKitC-1 (8MB) LUB ESP32-S3 SuperMini + ZALECANE 1× mmWave LD2410C (~5 EUR) jako czujnik referencyjny/sędzia w teście 7-dniowym.
2. Klaudek przygotowuje: lokalny add-on z agregatorem + konfig ESPHome dla LD2410C + dashboard porównawczy.
3. Flash binariów, prowizjonowanie NVS (WiFi, IP agregatora), start w pustym pomieszczeniu.
4. 7 dni zbierania danych; sędzia = LD2410C + obserwacja Tomasza.
5. Werdykt wg warunku stopu.
