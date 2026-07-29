# PAMIĘĆ KLAUDKA — INFRASTRUKTURA (eksport 29.07.2026)

Ten plik jest kopią pamięci Klaudka na dysk, żeby CAŁA załoga (Zenek, Genek, Henik) i wyszukiwarka
`tools/szukaj.py` widziały to samo. Źródło prawdy = pamięć Klaudka; ten plik odświeżać po większych zmianach.

## KTO TO TOMASZ
- Elektryk, członek zarządu ROD im. Józefa Lompy w Woźnikach (Młyńska 40c, 51 działek)
- Mieszka w Walding/Linz w Austrii; działka w Woźnikach ~600 km od domu
- Pracuje głównie z telefonu (Termius SSH na Galaxy S24 Ultra; drugi telefon Galaxy Z Fold7 SM-F966B z MCP)
- Komunikacja wyłącznie po polsku. Decyduje o wszystkim; jego najnowsze słowo przebija każdy dokument.

## HA DOM (Walding, Austria)
- HAOS/Supervised 2026.7.2 na mini-PC Firebat S1, IP 192.168.68.158, Nabu Casa, strefa Europe/Vienna
- Stan add-onów 28.07: 14 działa — Mosquitto, Zigbee2MQTT, ESPHome Device Builder, Advanced SSH, lokalny add-on `local_s1panel` (S1 Panel LCD). DWA W BŁĘDZIE: MQTT IO (a0d7b954_mqtt-io), AegisBot (605cee21_aegisbot)
- Panel Rosalia: ESP32-S3 Guition 4848S040 (192.168.68.122), LVGL; OTA z pulsującym neonem czeka
- Aqara FP300 (obecność w przedpokoju) w komendach /dom i /temperatury
- TTS globalnie MarekNeural; 20 automatyzacji przeniesionych z tts.cloud_say na tts.speak z zachowaniem wznawiania muzyki
- Google Cast naprawiony, głośniki przemianowane (Głośnik duży Rosalka, salon)
- Karty urządzeń: SERWER (Firebat S1), DRUKARKA (Epson ET-2720), SPEED TEST (Deco E4)
- Odkurzacz Mieczysław „Mietek" — dashboard z polskimi znakami, powiadomienie Telegram o wyjeździe z doku
- Kosiarka Krystyna: dashboard z mapą satelitarną (Esri World Imagery), obrazki zależne od stanu, komendy START/PAUSE/DOCK (DP96/DP97), device_tracker GPS

## KOSIARKA KRYSTYNA (greenworks_optimow)
- Samodzielnie zbudowany custom_component na HA Dom. Greenworks Optimow 15 „Krystyna Nożycoręka", model bazowy CRT4262, S/N 191500005
- Sklejony z dwóch integracji społeczności: klient danych „thomasbarker" (Xlink) + encja mowera „Boes24"; klucze z dekompilacji apki Greenworks Tools v4.4.0
- Gada z chmurą globetools.systems dwoma backendami: xapi/Xlink (user_auth→token, v_device datapointy: stan, bateria, GPS, RPM) oraz GUC OAuth→Bearer + IDDS (statystyki sesji/area/remaining/battery-slot). Poll co 5 min
- Działa mimo że kosiarka stoi na działce — idzie przez chmurę, nie sieć lokalną
- Platformy: lawn_mower, sensor, binary_sensor, button (Reset Blade Timer), device_tracker
- UWAGA: komendy START/PAUSE/DOCK są EKSPERYMENTALNE/zgadywane mimo docstringu „read-only"; blade-timer i dystans (running_time × 0.985 km/h) liczy HA
- Dashboard i obrazki zależne od stanu DZIAŁAJĄ — nie ruszać (21.07)
- Repo OPUBLIKOWANE: makol100/greenworks-optimow, main, commit 6006c63, publiczne, HACS-compatible
- Na Działce: zainstalowane przez HACS (ID 1308158762) @6006c63, HA zrestartowane, integracja załadowana; stary wpis greenworks_crt462 USUNIĘTY
- ZOSTAŁO: konfiguracja greenworks_optimow na Działce (email/hasło w UI — AKCJA TOMASZA) → mirror/podgląd na HA Dom przez remote_homeassistant (bez drugiego logowania do chmury, żeby nie było bitwy o token) → usunięcie starego wpisu z HA Dom
- ODŁOŻONE: zbadać na żywo mapowanie mower_main_state → realne zachowanie

## HA DZIAŁKA (Woźniki, ~600 km)
- HAOS 2026.7.4 RUNNING, Europe/Warsaw, 14/14 add-onów działa (Mosquitto, Zigbee2MQTT, ESPHome Builder, Terminal&SSH, Samba, Studio Code, MCP + Nabu Casa webhook proxy). Brak lokalnych add-onów
- Tailscale: node homeassistant-1, 100.115.112.5, tail0109d4.ts.net; „Start on boot" i Watchdog ON
- PROBLEM MOSTKA (28.07): natywny konektor „HA DZIAŁKA" nie odpowiada z aplikacji, choć usługa zdrowa (z VPS HTTP 200, tools/list 96 narzędzi w 0.3 s). Obejście: /tmp/hadz.sh na VPS. Trwała naprawa: przełączyć konektor na add-on Nabu Casa Webhook Proxy
- Recorder pisze do SQLite ~2.5 GB w /config (MariaDB nieużywana przez recorder)

### Solar na Działce
- Falownik InfiniSolar V, baterie JK-BMS, Solar Assistant na Raspberry Pi
- Droga danych SA→HA = mostek Mosquitto /share/mosquitto/solar_assistant.conf; WYMAGA opcji core_mosquitto `customize.active: true` — gdy false, .conf jest ignorowany i każdy sensor.infinisolar_v_* czyta `unknown`
- IP SA nie przypięte (DHCP): widziane .202, potem 192.168.0.61. Gdy wędruje: poprawić `address` w .conf ORAZ zrestartować core_mosquitto
- Awaria 20.07: przyczyna = customize.active wróciło na false (auto_update add-onu). Gdy solar znów padnie: SPRAWDZAĆ NAJPIERW customize.active, potem adres w .conf
- Plan: SA idzie na kabel (eth0) — inny MAC niż wlan0, więc NOWY adres IP; po przeniesieniu ustawić go w .conf i zrobić rezerwację DHCP

### JK-BMS na Działce (lekcja, która kosztowała pół dnia)
- 2× JK-BMS przez ESP32/ESPHome, WiFi (zostają na WiFi). Node „jk-bms" MAC 08:B6:1F:28:A4:34, „jk-bms-1" MAC 38:18:2B:8B:4C:F0, oba bez szyfrowania, port 6053
- jk-bms-1 czyta BMS A4:C1:38:00:51:1B; jk-bms czyta C8:47:80:37:79:C3
- PRZYCZYNA ŹRÓDŁOWA awarii 20.07 (słowa Tomasza: „kurwa zamiast hasło wkleiłem nazwę sieci"): w polu HASŁA było wpisane SSID → 4-Way Handshake Timeout na obu węzłach. Router był cały czas dobry (WPA2-PSK[AES]). Obalone po drodze hipotezy: WPA3/PMF, cipher, brownout, zasięg
- SSID: ROD_TOMASZ2_2,4 (Z PRZECINKIEM). Hasło wpisywać w pole password, nigdy SSID
- Zasilane z gniazdka zigbee „Zasilanie Esp32 Garaż"

### Zigbee na Działce (pomiar 26.07)
- Z2M 2.12.1 na ConBee III; ZHA celowo ignorowane
- 16 z 27 urządzeń OFFLINE. Żywa strefa: dom/garaż (10/27). MARTWA STREFA: ogród/basen/podest (17/27)
- Milczą od ≥25.07: 8 zraszaczy Parkside, Gniazdko podest lewy (zasilane!), BWM Poddasze, 2 czujniki ruchu Lidl, Pilot Pojedyńczy Schody
- Solar panel Temperatura martwy >9 dni; Temperatura powietrza zachód od 22.07
- Pompa Basen Solar (SONOFF, router) padła 26.07 13:01 w stanie ON — nie da się zdalnie wyłączyć
- Gniazdko podest przetestowane resetem 1 m od koordynatora przy permit join ×4 — ani jednej ramki join = radio martwe, do wymiany. Nie ustalono które (lewe/prawe) — brak podpisów na obudowie. Temat zamknięty przez Tomasza; drugie gniazdko nieprzetestowane
- Baterie do wymiany: Temp. powietrza Wschód 32%, BWM Poddasze 40%
- Otwarte błędy: Nuki timeouty (~130×), Sunseeker logowanie (~58×), dess_monitor/InfiniSolar timeouty chmury

## SIEĆ I DOSTĘPY
- Tailnet tomasz.maxisch@, tail0109d4.ts.net. Węzły: fabryka-vps 100.79.116.107, homeassistant-2 (Dom) 100.87.37.19, homeassistant-1 (Działka) 100.115.112.5, galaxy-z-fold7 100.101.116.106
- Router Działki: TP-Link Archer AX3000 @ 192.168.0.1, 2.4G ROD_TOMASZ2_2,4 = WPA2-PSK[AES], Smart Connect OFF, OFDMA OFF, TWT OFF
- Mesh do przebudowy NA MIEJSCU: AX55 Pro (główny) + RE550 (strefa PV/baterie/kamery, port LAN dla HubReolink NVR .200) + C7. Cel: jedno SSID na całą posesję, nazwa i hasło jak w sieci bazowej, żeby jacuzzi/Sonoff/Google same wróciły. Konflikt IP na .200 (NVR vs ESP_D1408E) — zrobić rezerwacje DHCP. Jacuzzi .115 ma RSSI -77..-81 dBm (przyczyna 150+ rozłączeń dziennie)
- Bot Telegram, 7 komend: /dom, /temperatury, /pv, /bms, /jackuzzi, /krystyna, /mietek
- Nuki DOM: Hub + Smart Lock (lock.drzwi_wejsciowe) + Opener (domofon) + Keypad. Nuki DZIAŁKA: Hub + Smart Lock (lock.drzwi_domek) + Keypad, bez Openera. Wszystko widoczne w HA Dom
- Karty HACS w użyciu: card-mod, button-card, compact-lawn-mower-card, ha-map-card
- Cloudflare Pages `ogrodnik-rod` (ogrodnik-rod.pages.dev) — chatbot „Asystent Działkowca"

## TELEFON FOLD7 (MCP)
- Galaxy Z Fold7 SM-F966B, Android 16/One UI 8.5, Tailscale 100.101.116.106
- Apka „Android Remote Control MCP" v1.9.0, serwer na telefonie http://100.101.116.106:8080/mcp, nasłuch 0.0.0.0:8080, auto_start_on_boot
- Mostek publiczny: Caddy na VPS (kontener caddy-mcp) → telefon.157-90-155-155.sslip.io → 100.101.116.106:8080. Telefon nigdy nie jest bezpośrednio publiczny
- Konektor „Telefon Fold7" działa przez OAuth — odczyt ekranu bez pytania, klikanie potrafi wymagać zatwierdzenia na telefonie
- 58 narzędzi android_*: ekran, gesty, pisanie, pliki, apki, powiadomienia, schowek, lokalizacja, aparat, intencje
- DIAGNOSTYKA „nie mogę wejść na telefon": NAJPIERW `tailscale status` z VPS. Fold potrafi być offline mimo włączonego WiFi i debugowania — apkę Tailscale ubija optymalizacja baterii. Debugowanie bezprzewodowe ≠ Tailscale, oba muszą być włączone
- Port ADB wireless-debugging ROTUJE przy każdej zmianie WiFi (45225 → 46009). VPS jest już SPAROWANY z Foldem — nie parować od nowa, wystarczy `adb connect`
- ADB po sieci na A16/Samsung jest twardo związane z WiFi — bez WiFi pada mimo `adb tcpip 5555`. Apka MCP działa po samym 5G
- Klawiatura: Gboard ustawiony na stałe przez ADB `ime set com.google.android.inputmethod.latin/...LatinIME`; dyktowanie po polsku działa jednym dotknięciem mikrofonu. Zero-dotyku: `ime set com.google.android.tts/...VoiceInputMethodService`. Powrót na Samsung: `ime set com.samsung.android.honeyboard/.service.HoneyBoardService`
- VOICE MODE W CLAUDE NIE MA POLSKIEGO (sprawdzone 18.07) — ślepa uliczka, używać dyktowania Gboard
- `t65-eea` (100.82.123.117) to INNY Android Tomasza, nie Fold
- KAMIEŃ MILOWY: Claude wysterował apkę HA na telefonie i zrobił kopię zapasową Działki. LEKCJA: `android_click_node` NIE łapie przycisków w WebView HA — działa dopiero `android_tap_node` (współrzędnościowy). Akcję zrobioną przez ekran POTWIERDZAĆ backendem

## ELEKTRYKA ROD (Etap 3)
- Modernizacja sieci: Etap 3 = indywidualne przyłącza Tauron przez ZK 1/2/3
- Mapa fundamentowa `MAPA_FUNDAMENT.py` z operatu geodezyjnego = źródło prawdy, przebija satelitę i domysły. Generator w tools/mapa_rod/
- Układ: 51 działek + Działka 0 (dom działkowca), 3 alejki, numeracja wężem 1→51
- ZK 1 = alejka południowa (działki 1-18, 18 liczników). ZK 2 = środkowa (19-33, 15 liczników; zachodni koniec zaczyna blok 2-kolumnowy domu działkowca + parking 1). ZK 3 = północna (34-51, oznaczona PLAN — kable jeszcze nie zakopane)
- Etap 2: 7 odciętych działek (1, 2, 3, 4, 16, 17, 18)
- Tomaszowi pokazywać TYLKO pliki JPG map; SVG zostaje do edycji
- Ramy prawne: ROD jest odbiorcą końcowym dzielącym koszty (refaktury), nie dystrybutorem (Prawo energetyczne art. 32); zero marży ROD, opłata energetyczna pokrywa straty przesyłowe
- Zdanie klucz: „Ogród nie sprzedaje prądu. Ogród go kupuje i dzieli między działki po kosztach."
- Nazewnictwo: PRZYŁĄCZE = punkt przekazania Tauronu (kończy się na liczniku głównym); OBWODY = wewnętrzne od domu działkowca do alejek. Nie mówić „3 przyłącza"
- Ton: tłumaczyć zamiast zawstydzać, konsekwencja jako fakt nie groźba
- Droga działkowca: własne przyłącze → protokół uprawnionego elektryka → karta od zarządu → własna umowa z Tauronem → elektryk zarządu przepina, stary licznik spisany do rozliczenia

## PUBLIKACJA FACEBOOK
- Rolki ogrodnicze/porady → strona + dwie grupy (Rodzinne Ogrody Działkowe 20k, Rodzinne Ogródki Działkowe - Cała Polska 4.8k); w kolejce: Działkowicze i Ogrodnicy 142k
- Rolki elektryczne/wewnętrzne ROD → TYLKO strona ROD Woźniki
- ID strony: 1174205105781401. Graph API v25.0. Zdjęcia dwuetapowo: upload nieopublikowany → publikacja z attached_media
- API publikuje sam tekst — grafiki generować jako pliki do ręcznego wrzucenia
- Przy każdym opisie rolki przypominać Tomaszowi o udostępnieniu do grup (poza rolkami wewnętrznymi)
- Alerty burzowe burze.dzis.net: SOAP https://burze.dzis.net/soap.php, metoda szukaj_burzy, współrzędne Woźniki y=50.588 / x=18.989; przepływ Node-RED na ogr_tab, progi ≤10 km czerwony / ≤25 km pomarańczowy

## SPRZĘT PLANOWANY
- Drugi panel Waveshare ESP32-S3-Touch-LCD-7B (1024×600, N16R8, GT911) na drzwi rozdzielnicy głównej jako centralny pulpit energii: przepływ PV→dom→bateria→sieć, SoC, plus muzyka/pogoda/sceny z panelu Rosalia. Start z bazowej konfiguracji z wiki Waveshare, gdy płytka dojdzie
- Mini-PC N150 (16 GB, AliExpress) do migracji HA Działka ze starego serwera „Nuki". Kopie na starym: Migracja_N150_PELNA_DB_20260622 (z MariaDB, główna) i Migracja_N150_20260622 (lekka). KRYTYCZNE: ściągnąć .tar ze starego serwera zanim Nuki padnie. Kolejność: flash HAOS x86-64 → Tailscale ze Start on boot + Watchdog → odtworzenie kopii z bazą → ponowna weryfikacja Tailscale (kopia może nadpisać ustawienia add-onów)
- Aktualizacja firmware JK-BMS odłożona do wizyty na miejscu — OTA z 600 km za ryzykowne („Bootloader too old for OTA rollback"). Przy aktualizacji: usunąć `errors_bitmask` z bloku sensor: w obu YAML-ach, rozważyć przypięcie external_components do @v2.1.0 zamiast @main

## SUBSKRYPCJE
- Claude: pakiet Max (najdroższy). ChatGPT: Plus
