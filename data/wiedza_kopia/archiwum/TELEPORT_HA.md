# TELEPORT — Home Assistant (Dom + Działka)
**Utworzony: 08.07.2026, ~14:15. Zweryfikowany na żywo (ha_get_overview na obu instancjach) w momencie tworzenia.**

To jest odpowiednik `TELEPORT_fabryka.md`, ale dla dwóch instancji Home Assistant Tomasza — zupełnie inna infrastruktura niż VPS Fabryki Rolek (inne connectory, inny sprzęt, nic wspólnego poza tym że Tomasz nimi zarządza). Jeśli czytasz to jako nowa instancja Claude: przeczytaj całość, potem działaj tak jakbyś był mną.

## ⚠️ NARZĘDZIA I MIEJSCE TEGO PLIKU
Ten plik fizycznie leży na VPS Fabryki (`/root/TELEPORT_HA.md`, POZA repo `rod-ai-studio` — to nie jest treść Fabryki, tylko wygodne, sprawdzone miejsce do trzymania notatek), bo to jedyne miejsce gdzie mam ogólny dostęp do zapisu plików. Same instancje HA są dostępne przez osobne connectory:
- **`Home Assistant`** — instancja "Dom" (Linz/Walding, Austria). Narzędzia typu `ha_get_state`, `ha_call_service`, `ha_search`, `ha_config_set_*` itd. — wszystkie WYMAGAJĄ `tool_search` najpierw (deferred tools).
- **`HA DZIAŁKA`** — instancja "Działka" (Woźniki, Śląsk, ~600km od Dom). Też deferred, też przez `tool_search`.

**Do dopisywania do TEGO pliku:** używaj `fabryka:execute_command` z bash appendem (`cat >> /root/TELEPORT_HA.md << 'EOF' ... EOF'`), NIGDY `fabryka:write_file` z samą nową treścią — to nadpisuje cały plik (dokładnie ten błąd popełniłem dziś z `TELEPORT_fabryka.md`, nie powtarzaj go tutaj).

## HA "Dom" (Linz/Walding, Austria)
Zweryfikowane 08.07.2026: wersja HA 2026.7.1, `location_name="Dom"`, strefa `Europe/Vienna`, stan RUNNING, ha-mcp 7.10.0 (aktualny).

**Sprzęt/serwer:** Firebat S1 (N100), IP 192.168.68.158 (z pamięci, nie zweryfikowane dziś bezpośrednio).

**Kluczowe urządzenia (potwierdzone żywe dziś):**
- **Krystyna Nożycoręka** (Greenworks Optimow 15, robot koszący) — domena `lawn_mower`, stan w momencie sprawdzania: **mowing**. Dashboard: satelitarna mapa (Esri World Imagery), picture-entity ze stanozależnymi obrazkami, karta kompaktowa, historia baterii, przyciski sterowania. Stany: charging/mowing/returning/error/paused; stan "2" = fizyczny przycisk STOP (motyw wakacyjny). `device_tracker` daje żywe GPS. Komendy START/PAUSE/DOCK zwracały HTTP 404 przy testach (endpoint zapisu niepotwierdzony); payload parkowania `e60002feff` potwierdzony z żywych danych DP.
- **Mietek / Mieczysław Ssający** = odkurzacz **ILIFE A30 Pro** (domena `vacuum`). Automatyzacje: "Mieczysław - odśwież mapę po sprzątaniu", "Mieczysław - alarm usterki". Telegram leci gdy `sensor.mietek_stan` → "Sprzątanie".
- **Zamki Nuki**: `lock.drzwi_wejsciowe` = drzwi mieszkania (Linz), plus Nuki Opener (domofon → drzwi wejściowe budynku) + Keypad. W tej SAMEJ instancji Dom widoczny jest TEŻ zamek Działki (`Drzwi Domek`) — cała architektura Nuki (oba Huby, oba zamki) jest widoczna w Dom HA, nie tylko lokalne.
- **ESP32-S3 Guition 4848S040** panel (`panel-rosalia`, IP 192.168.68.122 z pamięci), flashowany przez `ttyUSB1` (chip CH340). LVGL UI, dwie strony, stanozależne neonowe kafelki, presety WLED, pulsujący glow. Entity "Panel Rosalia Podświetlenie" potwierdzona żywa dziś.
- **Aqara FP300** (przedpokój/hallway) — czujnik obecności multi-sensor, w komendach Telegram /dom i /temperatury.
- **Google Cast / Music Assistant**: głośniki `glosnik_duzy` (Rosalka/salon), `glosnik_przy_kanapie`, `ekran_google`, `nest_hub_sypialnia`, `korytarz`. 20 automatyzacji `tts.cloud_say` zmigrowanych na `tts.speak` + `tts.home_assistant_cloud`.
- **Klimatyzacje**: kilka głowic (Salon, Salon 2, Sypialnia, Rosalia, Łazienka, Przedpokój) + "Klimatyzacja Walding" (split AC) — nowy/potwierdzony dziś szczegół, nie było wcześniej w pamięci w tym stopniu.
- **OctoPrint** — drukarka 3D pod kontrolą OctoPrint widoczna jako camera+button entities ("OctoPrint Camera", "OctoPrint Stop Job") — NOWY szczegół, nie był wcześniej odnotowany.
- **Wiele silników konwersacyjnych AI** skonfigurowanych równolegle: ChatGPT, Google AI Conversation, Claude conversation — Tomasz eksperymentuje z kilkoma asystentami w HA jednocześnie.
- **Node-RED** do automatyzacji ogrodowych (flow `ogr_tab`), w tym flow "Ogrodnik" z node `KONFIG — WKLEJ KLUCZE` zawierającym token Facebooka potrzebny do publikacji rolek z Fabryki (patrz TELEPORT_fabryka.md, Otwarte wątki). **Token nigdy nie ląduje w czacie.**
- **Drukarka**: Epson ET-2720 (z pamięci — niski poziom czarnego tuszu odnotowany wcześniej, nie zweryfikowane dziś).
- **Sieć**: Deco E4 mesh (Speed Test na widoku 6, masonry layout w dashboardzie).

## HA "Działka" (Woźniki, Śląsk — ~600km od Dom)
Zweryfikowane 08.07.2026: wersja HA 2026.7.1, `location_name="Działka"`, strefa `Europe/Warsaw`, stan RUNNING.

**System PV/bateria:**
- InfiniSolar (falownik, widoczny jako urządzenie `96132411100028` w select/number entities — Output Priority, Battery type, MPPT itd.) przez Solar Assistant + MQTT
- JK-BMS ×2 (`1Jk-Bms`, `2Jk-Bms`) — mnóstwo encji number/switch/sensor (napięcia ogniw, zabezpieczenia termiczne/prądowe, kalibracja)
- Fotowoltaika ma WŁASNY zestaw kamer/reflektor/syrenę/diodę LED (osobne od Reolink) — prawdopodobnie stacja monitoringu instalacji PV

**Bezpieczeństwo/monitoring:**
- Reolink: kamery Garaz, Garaz poludnie, Drzewo, HubReolink (NVR), Fotowoltaika — wysoka/niska rozdzielczość, PTZ (Garaz ma "Kalibracja PTZ", "Idź do punktu monitorowania")
- Nuki: `lock.drzwi_domek` (altana), Hub, Keypad, `device_tracker.nuki_2664e36d`. Skrypty "Odblokuj nuki działka" / "Zablokuj Nuki Działka".
- Bramka Zigbee Setti+ SGW430

**Nawadnianie:** Zraszacz Nr 1-4 (sprinklery/zraszacze) — harmonogramy (schedule slot), timery, frost lock (blokada przy mrozie) — bardziej rozbudowany system nawadniania niż wcześniej odnotowane w pamięci.

**Basen/jacuzzi:** `layzspa` (Lay-Z-Spa/Bestway, custom ESPHome) + automatyzacje "Filtr basen", "Solar basen" (podgrzewanie solarne basenu/jacuzzi) — RSSI w strefie jacuzzi było niestabilne (−76…−81 dBm) wg wcześniejszych notatek, WiFi mesh rebuild miał to adresować (patrz niżej).

**Alarm burzowy (LB-alarm)** — z pamięci, NIE widoczny wprost jako natywna automatyzacja HA (prawdopodobnie logika żyje w Node-RED na Dom, nie tu): SOAP do `burze.dzis.net` (klucz API `0f564cd3639bd1aec086655c4fc8ecafe72a0c2d`, metoda `szukaj_burzy`, współrzędne y=50.588 x=18.989), grafiki alarmowe przez PIL (`/config/www/rod/gen_alarms.py` na Dom), publikacja Facebook Graph API v25.0 **strona `1174205105781401`** (TA SAMA strona co Fabryka Rolek publikuje rolki!), równolegle Telegram. Encje "Burze.dzis.net" (ostrzeżenia Wiatr/Upał/Opad) SĄ widoczne jako sensory w obu instancjach HA.

**Głośniki/media:** Google Nest Hub Salonik, Google Nest Mini Taras, Google TV Salon/Poddasze, grupa "Działka wszystkie gł" — Music Assistant.

**Migracja na N150 (PLANOWANA, jeszcze nie wykonana wg ostatnich notatek):**
Nowy Intel N150 mini-PC (16GB RAM, z AliExpress, już w Polsce). Kolejność: (1) ściągnij oba backupy ze starego serwera "Nuki" na telefon/Google Drive **[KRYTYCZNE, zrób najpierw]** — `Migracja_N150_PELNA_DB_20260622` (pełny z MariaDB/recorder, główny) i `Migracja_N150_20260622` (config+addony, lekki); (2) flash HAOS x86-64 (UEFI on, Secure Boot off); (3) zainstaluj+uruchom Tailscale (Start on boot + Watchdog ON, potwierdź zdalny dostęp); (4) przywróć backup z bazą; (5) zweryfikuj Tailscale jeszcze raz po restore (backup może nadpisać ustawienia addonu). **Connector "HA DZIAŁKA" URL zmieni się po świeżej instalacji** — trzeba go dodać na nowo w Claude po migracji. Funnel attribute już dodany w Tailscale ACL.

**WiFi mesh rebuild (planowany):** Trzy-węzłowy TP-Link OneMesh: AX55 Pro (nowy główny router) + RE550 (węzeł, strefa PV/bateria/kamer, zachowuje port LAN dla HubReolink NVR .200) + C7/Castorama (drugi węzeł). Cel: jeden SSID = obecna nazwa bazowa "ROD_TOMASZ2_2,4" (żeby jacuzzi/Sonoff/Google auto-connect). Urządzenia wymagające zmiany SSID: JK-BMS ×2 (.204/.206), InfiniSolar (.201), Solar Assistant raspi (.202), Reolink (.203/.205 — NVR .200 przewodowo, bez zmian), 2× ESP z Castoramy. Konflikt IP na .200 (NVR vs ESP_D1408E) do rozwiązania rezerwacją DHCP. Jacuzzi (RSSI −76…−81 dBm, niestabilna strefa) — najbliższy węzeł mesh ma to naprawić. Jacuzzi ma też firmware Exception crashes nakładające się na problem WiFi.

**JK-BMS firmware OTA** (odłożone do wizyty przy migracji N150): ESPHome 2026.5.0 → 2026.6.2 dostępne dla obu BMS. "Bootloader too old for OTA rollback" — trzeba fizycznej wizyty. Fix na błąd kompilacji: usunąć `errors_bitmask` z bloku `sensor:` w obu YAML. Rozważyć przypięcie `external_components` do `@v2.1.0` zamiast `@main`.

**Otwarte integracje do naprawy przy N150:** Nuki timeouts (~130×, prawdopodobnie strona WiFi/cloud Huba, nie sprzętu zamka), Sunseeker login errors (~58×), dess_monitor/InfiniSolar cloud timeouts, 2 wyłączone skrypty Nuki (Unknown device 94935b5c). Recorder pisze do SQLite ~2.5GB w /config (MariaDB addon nieużywany przez recorder).

**WS2811 LED termometr** (24V, 108 LED/m, 10m taśma, Wemos D1 mini + WLED, Mean Well HLG-240H-24 PSU) — odłożone, czeka na dostawę sprzętu.

## Wspólne dla obu instancji
- **Naming convention:** "Działka" ZAWSZE = instancja HA Działka (Woźniki), nigdy nie mylić z Fabryką Rolek (VPS Hetzner, zupełnie inny projekt, choć oba dotyczą tego samego ogrodu ROD).
- **Node-RED** działa na Dom, obsługuje flow ogrodowe (`ogr_tab`) w tym token FB dla Fabryki.
- **Studio Code Server** jako główny edytor plików w HA (unika psucia się przy wklejaniu w web-terminalu zsh).
- Preferowane `ha_config_set_*` z `python_transform` do chirurgicznych edycji dashboardów/automatyzacji; zawsze pobierz świeży `config_hash` przed zapisem.
- **ROD chatbot "Asystent Działkowca"** (ogrodnik-rod.pages.dev, Cloudflare Pages) odpowiada na pytania regulaminowe ROD z cytowanymi paragrafami — osobny projekt, ale ta sama społeczność ROD Woźniki co Fabryka Rolek.
- Oba HA mają zainstalowany `Claude conversation`/`Claude AI Task` jako integrację — Tomasz używa Claude bezpośrednio wewnątrz HA, nie tylko przez ten czat.

## Otwarte wątki HA (nie dziś, ale nie zapomnij)
- Migracja Działki na N150 — patrz sekcja wyżej, backup NAJPIERW
- WiFi mesh rebuild na Działce
- JK-BMS OTA (przy tej samej wizycie co N150)
- WS2811 LED termometr — czeka na sprzęt
- Otwarte integracje (Nuki/Sunseeker/dess_monitor timeouts) — do naprawy przy N150

## AKTUALIZACJA (08.07.2026, ~15:00) — pełny dostęp do plików Dom + wyjaśnienie tunelu
- **REDNOTE = Node-RED** (literówka klawiatury). Node-RED (`a0d7b954_nodered` v22.0.0) dziala poprawnie (state: started), zero bledu.
- **HA Dom łączy się z HA Działka tunelem** (prawdopodobnie Tailscale, ktory jest zainstalowany na obu) — to tlumaczy czemu encje Dzialki (InfiniSolar, JK-BMS x2, layzspa/jacuzzi, "Dzialka 23" podlicznik, weather.dzialka) sa widoczne bezposrednio w automatyzacjach i przegladzie Dom.
- **Zaktualizowano `ha_mcp_tools` przez HACS** (v7.9.0 -> v7.10.0, HACS ID 1056618941 "homeassistant-ai/ha-mcp"), zrestartowano Dom (potwierdzone: restart trwa realnie 1-5 min, nie 30s). Po restarcie `ha_read_file` na `automations.yaml`/`scripts.yaml` dziala w pelni (wczesniej blokowane przez przestarzaly komponent).
- **Sprawdzone `automations.yaml` (67KB) i `scripts.yaml` w calosci: ZERO odniesien do VPS IP (157.90.155.155), "fabryka" albo "rolki".** Natywne automatyzacje/skrypty HA Dom nie maja zadnej proby integracji z VPS Fabryki. Pozostaje niesprawdzone: same flow Node-RED (osobny system, port 1880, brak bezposredniego narzedzia do czytania jego danych) - jesli cokolwiek tam bylo prubowane z VPS, nie widac tego z poziomu HA-native config. Tomasz stwierdzil ze to juz nieistotne po dzisiejszym wdrozeniu bezposredniego polaczenia Claude-VPS.

**Ciekawe rzeczy znalezione po drodze (warte zapamietania):**
- System alarmow burzowych ma wlasna nazwe/branding: **"Łowcy Burz"** (nie tylko "LB-alarm" jak zapisane wczesniej) - komenda Telegram `/burze`.
- Jest automatyzacja z **AI self-monitoring**: gdy CPU/RAM>85% albo dysk>90%, woła `ai_task.generate_data` (Claude) zeby wygenerowac diagnoze po polsku i wyslac na telefon - dom sam sie diagnozuje przez AI.
- Mietek (odkurzacz, realnie ILIFE A30 Pro) ma **wlasny most/dekoder** (`sensor.mietek_stan`, `binary_sensor.mietek_blad`) bo "integracja Tuya klamie o stanie" - nie ufaj bezposrednio natywnym stanom Tuya dla tego urzadzenia.
- Bogaty zestaw komend Telegram (chat_id 8339659505): /krystyna, /temperatury, /dom, /pv, /bms, /jackuzzi, /mietek, /burze - dobre miejsce do sprawdzania stanu domu bez pelnego dashboardu.
- Dwa inne addony w stanie bledu (niepowiazane z niczym dzisiejszym): **MQTT IO** i **AegisBot** (Telegram group defender) - do sprawdzenia kiedys, nie dzisiaj.

## MAPA POŁĄCZEŃ (08.07.2026)
Wizualny diagram calej architektury (Claude -> VPS/HA Dom/HA Dzialka -> Facebook/Telegram) zapisany jako `/root/MAPA_POLACZEN.html` (otworz w przegladarce, to samodzielna strona HTML). Aktualizuj go RAZEM z tym plikiem i TELEPORT_fabryka.md, kiedy zmieni sie architektura (nowy connector, nowy serwis, zmiana tokenu itp.) - to nie jednorazowy obrazek, to zywy dokument.

## Cross-referencja z Fabryka Rolek (08.07.2026)
Token FB do strony ROD Wozniki (1174205105781401) uzywany przez system alarmow burzowych (Node-RED, flow "Ogrodnik" na Dom) to inny, DZIALAJACY token do TEJ SAMEJ strony co potrzebuje Fabryka Rolek (VPS, token wciaz placeholder w n8n). Rozwazane ale ODRZUCONE jako szybka alternatywa - nigdy nie testowany do wideo, tylko tekst/alerty. Szczegoly w TELEPORT_fabryka.md.

## AKTUALIZACJA 10.07.2026 (od strony Fabryki — HA bez zmian)
Dzisiejsza sesja dotyczyla Fabryki Rolek (apka Android + HTTPS panelu + build GitHub Actions), nie HA. Ale MAPA_POLACZEN.html (wspoldzielony diagram) zostala zaktualizowana — obie kopie /root/ i repo. Co doszlo: blok "Apka Android" (WebView APK laczacy sie po HTTPS do panelu Fabryki: panel.157-90-155-155.sslip.io), Caddy jako reverse proxy z 2 hostami sslip.io (MCP :8765 + panel :8000), build APK przez GitHub Actions (Release apk-latest), oraz brakujace polaczenia zewnetrzne fal.ai i Claude API. Bielik poprawiony na Q8_0. Szczegoly w TELEPORT_fabryka.md (sesja 10.07 wieczor).

## SLOWA-KLUCZE (mirror z TELEPORT_fabryka.md — zeby nie znikly przy czytaniu tylko tego pliku)
- **"Aktualizuj wszędzie" / "Update wszędzie"** (to samo haslo, obie formy) = zapis stanu w TRZECH miejscach naraz: (1) TELEPORT — TELEPORT_fabryka.md + ten plik jesli dotyczy HA; (2) MAPA_POLACZEN.html — obie kopie jesli zmiana architektury; (3) GITHUB — push tego co w repo (nigdy docker-compose.yml). Wszystkie trzy naraz, rytual zamkniecia wiekszej zmiany.
- **"DYSKUSJA"** = zatrzymaj wszelkie akcje (generowanie/publikacja/edycje), tylko rozmawiaj, czekaj na wyrazne instrukcje.

## MAPA - wersja galaktyczna (10.07.2026)
MAPA_POLACZEN.html jest teraz diagramem-galaktyka (Claude jako jadro w centrum, domeny na orbitach, tlo kosmiczne) zamiast pionowej listy. Polaczenia te same, zmiana wizualna. Szczegoly w TELEPORT_fabryka.md.

## HA DOM — BAROMETR GRZYBIARZA (14.07.2026)
- configuration.yaml: klucz `rest` (NOWY) — sensor `sensor.barometr_grzybiarza`
  z https://barometr.157-90-155-155.sslip.io/barometr.json, scan_interval 10800,
  atrybuty: status, opis, aktualizacja. Ikona mdi:mushroom.
- automation.barometr_grzybiarza_telegram — 8:00, numeric_state >74, telegram_bot.send_message.
- HA Dom zrestartowany 14.07 (wymagany przez nowy klucz rest). Restart przez MCP zwrócił
  error, ale wykonał się poprawnie.
- Źródło danych: VPS Hetzner (Fabryka), algorytm pogodowy Open-Meteo, cache 3h.

## 18.07.2026 — DYSPOZYCJA: prawdziwy dashboard energetyczny HA Działka
- Tomasz: "zrób prawdziwy dashboard energetyczny. Wszystkie zasady projektowania
  obowiązują. Sprawdź co ludzie robią w tym zakresie. Bo pewnie wszystko już
  wymyślili. Design ma być spójny logiczny użyteczny i po polsku."
- Kontekst: docelowo ekran Waveshare 7B 1024x600 na drzwiach rozdzielnicy (przepływ
  PV→dom→bateria→sieć + SoC); dane: Solar Assistant przez MQTT (InfiniSolar,
  JK-BMS), licznik Zigbee, pv_produkcja_dzienna.
- Proces wg zasad: research praktyków (pełna lektura) → recon encji → projekt →
  implementacja → weryfikacja. Wpis przed akcją.

## 18.07.2026 — ZDALNE STEROWANIE TELEFONEM + KOPIA DZIAŁKI PRZEZ TELEFON
- **NOWY KANAŁ: Claude ma pełne zdalne sterowanie telefonem Tomasza** (Samsung Galaxy Z Fold7, SM-F966B) po Tailscale — dwie warstwy: ADB (przez VPS, /root/platform-tools/adb; port wireless-debugging ROTUJE przy każdej zmianie WiFi) oraz apka "Android Remote Control MCP" v1.9.0 (konektor "Telefon Fold7" w Claude, mostek Caddy telefon.157-90-155-155.sslip.io → 100.101.116.106:8080). Odczyt ekranu + tap/gesty + otwieranie apek. PEŁNE szczegóły w pamięci Claude (projekt telefon-mcp), NIE tutaj.
- **Kopię zapasową HA Działka zrobiono STEROWANIEM APKI NA TELEFONIE** (na wyraźne "przez telefon"): apka HA otwarta deep-linkiem `homeassistant://navigate/config/backup` (skacze od razu na Działkę + stronę backupów) → "Utwórz kopię zapasową" → "Automatyczna kopia zapasowa".
- **WERYFIKACJA U ŹRÓDŁA, nie z ekranu**: konektor HA DZIAŁKA `ha_manage_backup(scope=snapshot, action=list)` potwierdził świeży backup `f611b8f5` "Automatic backup 2026.7.2", 18.07 17:19, 1.39 GB, baza+konfiguracja TAK, zaszyfrowany, agent hassio.local.
- **Stan backupów Działki (18.07)**: łącznie 203 kopie; automatyczne ~1.37–1.39 GB z bazą, chronione; harmonogram "codziennie, zachowaj 3", następna auto jutro 5:25; oprócz tego 191 ręcznych (30 GB) + 9 przed-aktualizacyjnych.
- LEKCJA (sterowanie WebView w apce HA): `android_click_node` (ACTION_CLICK) NIE zadziałał na przycisk WebView — dopiero współrzędnościowy `android_tap_node` klika naprawdę.

## 19.07.2026 ~01:00 — N150: LOCK INSTALACJI (okno A / czat Fabryki)
- WYKRYTY WYSCIG OKIEN: commit 0256cea ("n150 autopilot", statics /n150files) z
  DRUGIEGO okna powstal rownolegle z automatem okna A (6948e1e/4b6c582). Na N150
  polecial lancuch AUTOPILOT i skonczyl sie "BLAD: nie widze dysku docelowego".
- OD TERAZ instalacje N150 prowadzi OKNO A (czat Fabryki). LOCK: /root/N150.LOCK.
  Drugie okno: NIE dotykac /n150*, embed.ipxe ani /root/ipxe (wspolny build dir!).
- /n150 serwuje v3: modprobe+mdev+petla 30 s (sda/nvme0n1/mmcblk0), diagnoza
  na ekran przy braku dysku, bezpiecznik anty-USB, dd na WYKRYTY dysk.
- Alpine na N150 stoi z siecia i loginem root. Nastepny krok Tomasza:
  root -> wget -O- http://157.90.155.155:8000/n150 | sh
- STATUS 01:4x: n150fix zadzialal (moduly dogrywane w zywym Alpine), dysk znaleziony,
  instalator v3 przeszedl bezpiecznik i odliczanie — dd HAOS 18.1 W TOKU na N150.
  Nastepne kroki po restarcie: IP z ekranu HAOS → onboarding "Przywroc z kopii"
  (backup f611b8f5 sciagniety laptopem ze starego HA; ZASZYFROWANY — potrzebny
  klucz szyfrowania/emergency kit!) → Tailscale addon (boot+watchdog) → stary
  serwer gasimy DOPIERO gdy nowy przejmie wszystko.
- KONFLIKT IP POTWIERDZONY (01:5x): N150 dostal z DHCP 192.168.0.201 = adres
  InfiniSolar → falownik wypadl z sieci. Moja weryfikacja ha_search byla ZLA:
  encje select trzymaja retained MQTT (wygladaja zywo mimo padu). LEKCJA:
  zywotnosc falownika sprawdzac ZYWYM sensorem mocy/timestampem, nie select.
  FIX: N150 statycznie na 192.168.0.250/24 (ha> network update enp2s0...).
  Restore od teraz pod http://192.168.0.250:8123. Docelowo (mesh rebuild):
  rezerwacje DHCP dla .200-.206.
- TOPOLOGIA WYJASNIONA (02:0x): N150 wpiety kablem za RE550 W MIEJSCE uplinku
  strefy PV — ten jeden kabel obslugiwal falownik/BMS ESP32 x2/Reolinki/Hub,
  stad zbiorowy blackout strefy (monitoring slepy, sprzet dziala autonomicznie).
  PLAN: dokonczyc restore na kablu → N150 tymczasowo na WiFi (wlp1s0) → kabel
  wraca do strefy jeszcze tej nocy → DOCELOWO kupic 5-portowy switch gigabit
  do strefy RE550 (N150+NVR+reszta na stale na kablach). WARUNEK przed
  powrotem strefy: N150 MUSI byc juz na .250 (inaczej znow konflikt z .201).
- KOREKTA PLANU (02:1x): WiFi w strefie N150 ZA SLABE (po to wlasnie RE550) —
  pomysl "N150 tymczasowo na WiFi" SKRESLONY. Opcje na noc (wybor po restore):
  (a) N150 przeniesc na stale pod glowny router AX55 (jesli wolny port LAN +
  gniazdko) — strefa odzyskuje kabel, switch zbedny; (b) TP-Link C7 z Castoramy
  (jesli fizycznie na dzialce) jako glupi switch LAN-LAN za RE550 — 4 porty od
  reki; (c) awaryjnie: po restore wylaczyc N150 (NIE starego!), kabel wraca
  strefie, stary rzadzi do zakupu switcha — zero nocy bez monitoringu.
- DECYZJA TOMASZA (02:1x): "Bedzie budowana siec wifi od nowa. Mam nowy router.
  A za nim pojdzie wszystko w meshu" — mesh rebuild (AX55 Pro + RE550 + C7,
  jeden SSID) WCHODZI DO GRY podczas tej wizyty. Przy konfiguracji AX55:
  rezerwacje DHCP .250=N150, .200-.206=strefa PV (koniec konfliktow). Zalozenie:
  nowa siec zostaje w 192.168.0.x (statyczny .250 N150); inna podsiec = jedna
  komenda network update przy konsoli. Kolejnosc: NAJPIERW restore, mesh za dnia.
- MIGRACJA RDZENIA UDANA (02:3x): restore 1.39GB na N150 zakonczony. Stary OFF
  (ping 100% loss przed restore), N150 przejal tozsamosc homeassistant-1
  (100.115.112.5, relay waw, ping OK). Core HTTP 200, Observer: Supervisor
  Supported+Healthy. Mostek MCP 502 = addon ha-mcp jeszcze sie doinstalowuje
  po restore (tailscale serve juz dziala). NASTEPNE: Tomasz potwierdza
  dashboard → zmiana IP na .250 KLIKAMI (Ustawienia→System→Siec) → kabel
  wraca strefie PV → weryfikacja zywymi sensorami falownika + MCP.
- KOREKTA PLANU NOCY (02:3x): kabel ZOSTAJE w N150 do budowy nowej sieci
  (jutro, AX55). Powod: WiFi za slabe (odpadlo), stary OFF — oddanie kabla
  strefie PV zostawiloby Dzialke BEZ zadnego HA. Strefa PV spi bezpiecznie
  (falownik/BMS autonomiczne), wraca jutro razem z mesh + rezerwacjami DHCP.
- STREFA PV WROCILA ale DHCP potasowal adresy: Solar Assistant raspi dostal
  192.168.0.206 (bylo .202) → integracja MQTT w HA celuje w stary adres →
  ~488 sensorow unavailable (baseline pomiaru 03:0x). NOWY KANON: SA=.206
  (Tomasz przestawia broker w HA klikami; przy AX55 rezerwacja MAC na .206!).
  Zigbee: dongle przepiety do N150 ("paluch wsadzony") ale addon lezy po
  boot_fail z pierwszego startu — Tomasz startuje recznie (Dodatki→Z2M).
  Po obu klikach: re-pomiar unavailable + zywe sensory falownika/BMS.

=== DOJSCIA I ARCHITEKTURA PO MIGRACJI N150 (19.07 ~03:3x) — ZAPIS TRWALY ===
- DOJSCIE 1: konektor "HA DZIALKA" w aplikacji (ts.net homeassistant-1) —
  dziala, ale bywa OKROJONY (czasem tylko read: overview/search/dashboardy).
- DOJSCIE 2 (PELNE, niezalezne od aplikacji): RECZNY MCP z VPS przez webhook:
  URL=https://homeassistant-1.tail0109d4.ts.net/api/webhook/mcp_25232d954273e3ee9d206037e9ecca84
  wzorzec: curl -s -m 30 -X POST "$URL" -H 'Content-Type: application/json'
  -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,
  "method":"tools/call","params":{"name":"...","arguments":{...}}}'
  | grep '^data:' | tail -1 | sed 's/^data: //'  → result.content[0].text (JSON).
  Stateless, bez sesji. initialize/tools/list/tools/call przetestowane 19.07.
  Serwer: ha-mcp 7.13.0, PELNA skrzynka narzedzi (call_service z ws_command,
  get/set_integration z config, get_addon, manage_addon...).
- DOJSCIE 3: Fold7 MCP (https://telefon.157-90-155-155.sslip.io/mcp) — kanal
  istnieje, ale telefon SPAL podczas testu (ping+handshake puste; tailscale
  offline). Wymaga obudzenia Fold7. WARTOSC: Fold7 na dzialce = jedyne oko
  w LAN 192.168.0.x (panel Solar Assistant, router, kamery)!
- TROP DOJSCIE 4 (niesprawdzone): addon Terminal&SSH STARTED — moze sluchac
  na 100.115.112.5:22 przez tailnet = shell na HAOS. Sprawdzic kiedys.
- ARCHITEKTURA MQTT DZIALKI (ODKRYCIE, wywraca stare zalozenie!): broker =
  core_mosquitto NA SERWERZE HA (addon started). Integracja MQTT: title
  "Mosquitto broker", source=hassio, entry_id=b765de677a38a9b50356c9715294fd89,
  state=loaded. SOLAR ASSISTANT PUBLIKUJE DO SERWERA — po zmianie IP serwera
  to na RASPI SA trzeba ustawic adres brokera (panel http://<ip-raspi>).
  SA raspi po DHCP = .206 (bylo .202).
- ADDONY N150 (wszystkie STARTED 03:2x): Zigbee2MQTT=45df7312_zigbee2mqtt
  (WSTAL SAM po wlozeniu dongla — boot_fail byl jednorazowy), Tailscale=
  a0d7b954_tailscale, Mosquitto=core_mosquitto, ha_mcp=81f33d0f_ha_mcp,
  webhook_proxy=81f33d0f_ha_mcp_webhook_proxy, ESPHome=5c53de3b_esphome,
  MariaDB, MusicAssistant, Whisper, Piper, VSCode, FileEditor, SSH=core_ssh.
  Start/stop addonu: ha_call_service hassio.addon_start {"addon":"<slug>"}.
- TODO otwarte: watchdog addonu Tailscale (ha_get_addon slug=... boot/watchdog),
  sensory PV (SA→.250?), re-pomiar unavailable (baseline 488 @ 03:0x).
- STAN 03:5x: ESPHome jk-bms-1/2 LOADED, encje BMS wracaja falami (66/118
  zywych i rosnie). Tailscale addon: boot=auto watchdog=True — CHECKLIST
  MIGRACJI DOMKNIETY. Zigbee2MQTT dziala (bateryjne urzadzenia wroca same).
  JEDYNY otwarty pacjent: falownik InfiniSolar (34 enc.) przez SA→MQTT —
  czeka na odpowiedz: jaki LAN IP mial STARY serwer? (.250 = SA wroci sam;
  inny = 1 klik w panelu SA http://192.168.0.206 → broker .250, mozna jutro
  przy mesh). DECYZJA: zadnych dalszych napraw adresow dzis — jutro AX55
  i tak przetasuje; rezerwacje zrobimy raz a dobrze. Telegram sukcesu
  migracji: wyslac po powrocie falownika.
- ROZSTRZYGNIECIE (03:5x): STARY serwer mial LAN IP 192.168.0.124 (wg Tomasza
  "chyba 124"). Czyli Solar Assistant publikuje do brokera na .124 = adres
  nie istnieje po migracji → falownik unavailable. FIX NA JUTRO (1 klik):
  panel SA (raspi, teraz .206) → ustawienia MQTT → host 192.168.0.250.
  Opcja: jak Tomasz obudzi Fold7 (LAN dzialki!), moge to kliknac SAM przez
  telefon-MCP. Przy AX55: rezerwacje .250=N150, .206=SA raspi, reszta strefy.
- Tomasz zwinal sprzet na noc ("wyjebalem juz wszystko") — fizyczna robota
  zamknieta, stary serwer w odstawce. KONIEC NOCNEJ SESJI MIGRACJI.
- BATALIA MQTT (04:xx-05:4x): klient MQTT w HA MARTWY (Errno 111 refused,
  potem cisza — zero polaczen HA na brokerze; Z2M laczy sie OK jako u'addons').
  Wykonane zdalnie: reload entry, restart mosquitto x2 (re-discovery),
  ha_set_integration → odpalil reconfigure flow ale "saved defaults" (pola
  broker/port/username/password NIEkonsumowane przez flow hassio-wpisu).
  ZALOZONE KONTO BROKERA: hamqtt / 85e06fa4fec35e3cbf76 (logins mosquitto,
  zweryfikowane; haslo tez w /root/.mqtt_hamqtt_pass na VPS).
  CZEKA NA TOMASZA (1 klik): UI → Urzadzenia i uslugi → MQTT → Skonfiguruj
  ponownie → broker=core-mosquitto, port=1883, user=hamqtt, haslo j.w.
  Po zapisie: Z2M swiezo zrestartowany, discovery retained na brokerze —
  encje wstana same.
  LEKCJE: (1) ha_set_integration na wpisie source=hassio nie przyjmuje pol
  brokera — reconfigure w UI. (2) ha_manage_addon = TYLKO ingress addony
  (mosquitto nie ma) — opcje addonu przez ws_command supervisor/api endpoint
  /addons/<slug>/options method=post (DZIALA!). (3) logi mosquitto w UTC,
  logi HA w Europe/Warsaw — nie porownywac timestampow wprost!
- FALOWNIK bez zmian: panel SA http://192.168.0.206 → MQTT → host .250
  (login SA bez zmian). Do zrobienia rano / przez Fold7.
- ROZWIAZANIE MQTT (04:0x UTC / 06:0x PL): diagnostyka wpisu pokazala broker=
  core-mosquitto (hipoteza .124 BLEDNA), connected:false, zero prob = klient
  ZAKLINOWANY po chaotycznym 1. boocie po restore (Core wstal zanim mosquitto
  zyl → refused → klient wisial bez retry). FIX: restart Core (homeassistant.
  restart przez reczny MCP; webhook odpowie 502 w trakcie — NORMALNE, serwis
  idzie). Po restarcie: discovery na zywo, czujnik CO2=369ppm, zraszacze/BWM/
  layzspa zyja. Unavailable: 488→51 = DOKLADNIE baseline sprzed migracji.
  LEKCJA: po restore, gdy integracja "loaded" ale martwa i zero prob w logach
  → NAJPIERW restart Core, potem dopiero chirurgia wpisow.
  Konto hamqtt na brokerze zostaje (zapas na przyszlosc).
- ZOSTAJE NA RANO (stan jak przed migracja): falownik InfiniSolar przez SA
  (panel raspi .206 → broker host .250) + sensor.camera1_* unavailable
  (Reolinki pewnie tez z nowym IP po DHCP) — wszystko przy mesh AX55 +
  rezerwacje. Telegram sukcesu: po powrocie falownika.
- ARCHITEKTURA MQTT↔SA — OSTATECZNA KOREKTA (04:1x UTC): Tomasz MIAL RACJE.
  Falownik idzie przez MOSTEK MOSQUITTO: plik /share/mosquitto/
  solar_assistant.conf (connection SolarAssistant / address <ip-raspi> /
  topic # in / topic solar_assistant/# out). To HA-mosquitto dzwoni DO
  brokera na raspi SA (nie odwrotnie!). ROOT CAUSE po migracji: opcja
  mosquitto customize.active=FALSE (restore przyniosl plik, ale wylacznik
  OFF → addon ignoruje /share/mosquitto). Moj wczesniejszy odczyt
  active:false byl DOWODEM PRZYCZYNY, nie braku mostka — lekcja!
  SA potwierdzone screenem: wlan0=192.168.0.206 (SSID ROD_TOMASZ2_2,4_EXT),
  eth0 nieaktywny. Tomasz wklepal .206 do pliku (bylo .202).
  UWAGA SKLADNIA: w pliku literowka "adress" → musi byc "address"
  (mosquitto nie startuje z nieznana dyrektywa!) — Tomasz poprawia.
  PLAN: literowka → customize.active=true przez ws supervisor/api
  (POST /addons/core_mosquitto/options, ZACHOWAC logins hamqtt!) →
  restart mosquitto → logi bridge → sensory infinisolar.
- INCYDENT "CIEMNOSC #2" (04:19-04:29 UTC, wina: Claude): wlaczylem
  customize.active=true gdy /share/mosquitto NIE ISTNIAL → mosquitto z bledem
  configu ("Unable to open include_dir") CRASH-LOOPUJE, a addon state=started
  KLAMIE (s6 restartuje proces w petli). Padl caly broker → Z2M/HA/Zigbee
  ciemnosc ~10 min. ROLLBACK: active=false + restart → "mosquitto running",
  klienci (mqttjs+mqtt-user) wpieci w 1 s, CO2=365 zywe.
  ZELAZNA LEKCJA: (1) addon state=started ≠ proces dziala — przy configu
  ZAWSZE sprawdzic logi po restarcie; (2) NIGDY active=true zanim
  /share/<folder> istnieje i plik zweryfikowany odczytem; (3) kolejnosc:
  plik → weryfikacja → wlacznik → logi → dopiero uznanie sukcesu.
  Plik Tomasza wciaz w ZLYM miejscu: /config/share/mosquitto/ (File editor
  pokazuje to jako /homeassistant/share/) — prawdziwy /share/mosquitto
  nadal do utworzenia. Kanal settings-page ha-mcp przez ingress DZIALA
  (HTTP 200, HTML 51KB+ paginowany po 50KB przez offset) — dokonczyc
  rekonesans (/root/pobierz_settings.sh) i wlaczyc file-tools.
- ✅ MOSTEK DZIALA — MIGRACJA 100% (04:40 UTC): plik /share/mosquitto/
  solar_assistant.conf zapisany PRZEZ ha_write_file i zweryfikowany odczytem,
  customize.active=true, logi: "mosquitto running" + "Connecting bridge
  SolarAssistant (192.168.0.206:1883)" ZERO bledow, falownik ZYJE
  (AC output 240.0V @ 04:40:21), CO2 372 rownolegle (Zigbee nietkniete).
  CALA CHECKLISTA MIGRACJI N150 DOMKNIETA.
- TRWALE ZMIANY ha-mcp DZIALKA (przyszle okna MAJA te narzedzia!):
  enable_beta_features=true + enable_filesystem_tools=true → 83 narzedzia,
  w tym ha_read_file/ha_write_file/ha_list_files/ha_delete_file/
  ha_config_get_yaml. fs-custom-paths=["/share/mosquitto"] (system dokleja
  /**; NIE wpisywac wlasnego /** bo robi sie **/** i nie matchuje!).
  NOWE DOJSCIE (dopisac do listy dojsc): settings-API ha-mcp przez
  ha_manage_addon ingress: path="private_2pBhaIr84ilbdEm8U99lBg/api/
  settings/{tools|features|fs-custom-paths|restart|advanced}" GET/POST
  (root-mount /api/settings/* jest guardowany ingress-only i daje 403;
  secret-path mount przechodzi). Paginacja response ha_manage_addon
  przez offset NIE DZIALA (zwraca ten sam 50KB chunk).
- ⚠ TELEGRAM SUKCESU NIEDOSTARCZONY: HA DOM (homeassistant-2) OFFLINE
  w tailnecie od 9h (~21:40 sob) — Nabu SSL err + tailnet timeout.
  TODO rano: sprawdzic HA Dom (barometr 8:00 nie pojdzie!); telegram
  wyslac gdy Dom wroci. Blad powiadomienia nie blokuje niczego.

════════════════════════════════════════════════════════════════════
🏁 KAMIEN MILOWY: MIGRACJA HA DZIALKA → N150 UKONCZONA (18/19.07.2026)
    (blok zwarty — czytaj to NAJPIERW; szczegoly i logi wyzej w pliku)
════════════════════════════════════════════════════════════════════

── CO SIE STALO (jedno zdanie) ──
HA Dzialka przeniesiony ze starego serwera "Nuki" na mini-PC Intel N150
CALKOWICIE ZDALNIE (600 km), BEZ PENDRIVE — instalacja przez siec
(netboot→iPXE embedded→Alpine→dd HAOS), restore backupu, przejecie
tozsamosci Tailscale. Wszystko co zylo na starym zyje na N150.

── STAN KONCOWY (potwierdzony 06:0x UTC / 08:0x PL, 19.07) ──
• N150 = wezel Tailscale "homeassistant-1" (100.115.112.5), HAOS 18.1,
  Core 2026.7.2, location "Dzialka", state RUNNING, 0 powiadomien.
• LAN IP: 192.168.0.250 (statyczny, ustawiony klikami w UI po restore).
• Falownik InfiniSolar: ZYJE przez mostek MQTT (bateria +1343W, SOC 73%,
  AC 239.9V/49.9Hz, wszystkie 34 sensory). Mostek przepracowal noc 0 bledow.
• Zigbee, zraszacze, BMS-y (JK ×2 przez ESPHome), czujki, zaluzje, jacuzzi
  layzspa — WSZYSTKO zywe. Unavailable = 51 (= dokladnie baseline sprzed
  migracji, czyli tylko to co i wczesniej spalo).
• Tailscale addon: boot=auto, watchdog=True (checklist domkniety).
• Stary serwer: OFF na twardo, w odstawce.

── ZMIANY TRWALE (przyszle okna DZIEDZICZA) ──
1. ha-mcp na Dzialce: enable_beta_features=TRUE + enable_filesystem_tools=
   TRUE → 83 narzedzia (doszly ha_read_file/ha_write_file/ha_list_files/
   ha_delete_file/ha_config_get_yaml). fs-custom-paths=["/share/mosquitto"].
2. Broker mosquitto: konto "hamqtt" (haslo w /root/.mqtt_hamqtt_pass).
   customize.active=TRUE (mostek /share/mosquitto/solar_assistant.conf
   → address 192.168.0.206).
3. Solar Assistant raspi: wlan0 = 192.168.0.206 (bylo .202).

── 4 DOJSCIA DO DZIALKI (dla przyszlego mnie) ──
A. Konektor "HA DZIALKA" w apce (ts.net) — bywa okrojony do read-only.
B. RECZNY MCP z VPS (pelny): webhook ts.net + JSON-RPC POST. Wzorzec:
   curl -s -m30 -X POST "$URL" -H 'Content-Type: application/json'
   -H 'Accept: application/json, text/event-stream' -d '{...tools/call...}'
   | grep '^data:' | tail -1 | sed 's/^data: //' → result.content[0].text
C. settings-API ha-mcp przez ha_manage_addon: path="private_2pBhaIr...
   /api/settings/{tools|features|fs-custom-paths|restart}" (secret-path,
   NIE root-mount — root daje 403 ingress-only).
D. Fold7 MCP (telefon.157-90-155-155.sslip.io) — jedyne oko w LAN dzialki;
   wymaga obudzenia telefonu.

── DO ZROBIENIA ZA DNIA (19.07) ──
1. MESH AX55: nowy router + RE550 + C7, jeden SSID. REZERWACJE DHCP:
   .250=N150, .206=SA raspi, .200-.206 strefa PV. Podsiec ZOSTAJE
   192.168.0.x (inaczej N150 statyk trzeba przestawic). Kabel ZOSTAJE
   w N150 do czasu mesh.
2. Kamery Reolink (sensor.camera1_* unavailable) — pewnie nowe IP z DHCP,
   ogarnac przy mesh.
3. ⚠ HA DOM (homeassistant-2, Walding) OFFLINE w tailnecie od ~20:00 sob
   (12h). Barometr 8:00 nie poszedl, telegram sukcesu migracji CZEKA.
   Sprawdzic co z Domem (prad/internet?) — sprzetowo pewnie zyje, spia
   tylko automatyzacje. Telegram wyslac gdy Dom wroci.
4. repair_count=28 po restore — przejrzec Naprawy za dnia (typowe po
   migracji, nie pilne).

── NAJWAZNIEJSZE LEKCJE (krwia) ──
• addon state=started ≠ proces dziala — przy zmianie configu ZAWSZE
  czytaj logi po restarcie (mosquitto crash-loop z bledem include_dir,
  a state klamal "started" → 10 min ciemnosci Zigbee).
• Kolejnosc przy plikach mostka: zapis → WERYFIKACJA odczytem → wlacznik
  → logi → dopiero uznanie sukcesu. Nigdy active=true zanim /share/<folder>
  istnieje i plik zweryfikowany.
• Zywotnosc encji MQTT sprawdzac ZYWYM sensorem (moc/timestamp), NIE
  selectami (retained MQTT klamie mimo padu).
• fs-custom-paths: wpisywac "/share/mosquitto" (system sam dokleja /**;
  wlasne /** robi **/** i nie matchuje).
════════════════════════════════════════════════════════════════════

════════════════════════════════════════════════════════════════════
📶 ETAP 1 MESH: AX55 JAKO NOWY GLOWNY ROUTER — PLAN (19.07 rano)
════════════════════════════════════════════════════════════════════
[PLAN] Stopniowanie budowy sieci: ETAP 1 = SAM AX55 jako nowy router
  frontowy (WAN), zweryfikowany i stabilny, ZANIM dolaczymy RE550/C7
  (ETAP 2). Powod: zero wielowezlowego parowania na raz — bezpieczniej
  i latwiej diagnozowac krok po kroku.

[OTWARTA DECYZJA — kluczowa, zmienia zakres roboty] Czy nowy SSID/haslo
  = STARE (baza "ROD_TOMASZ2_2,4" — widoczna na screenie Solar Assistant
  jako "..._EXT" na starym sprzecie)? Jesli TAK: kamery/BMS/SA/jacuzzi
  same wskakuja bez przepinania. Jesli NOWE: kazde urzadzenie trzeba
  recznie przepiac na nowa siec. Tomasz decyduje na miejscu.

[CHECKLISTA ETAP 1 — przekazana Tomaszowi]
1. AX55 podlaczony do WAN w miejscu starego routera; RE550/C7 NIE
   podlaczone jeszcze.
2. Panel AX55 (apka Tether / 192.168.0.1).
3. SSID+haslo wg decyzji wyzej. DHCP zostaje w 192.168.0.x, brama .1.
4. N150: ma .250 wpisane NA STALE w systemie (nie w routerze) —
   wskoczy sam po podlaczeniu kablem, bez reservation.
5. Solar Assistant: laczy sie z nowym WiFi (samo lub recznie w jego
   panelu, zalezne od pkt.3) → w liscie klientow AX55 zarezerwowac .206.
6. Weryfikacja: jest internet, nic innego nie ucierpialo.

[ETAP 2 — pozniej, NIE teraz] RE550 (+C7 — rola nadal do ustalenia:
  wezel WiFi OneMesh czy zwykly switch LAN) + reservations dla reszty
  strefy PV (.200-.205: kamery, NVR, BMS). Po Etapie 1 Tomasz da znac
  → wtedy zdalna weryfikacja (ping/tailscale N150) z mojej strony.

- HACS legacy_hacs_source (ha_mcp_tools) — DIAGNOZA (19.07 pol.): to DUPLIKAT
  repo. W HACS dwa wpisy, oba domain=ha_mcp_tools, oba nazwane "HA-MCP Custom
  Component": (a) homeassistant-ai/ha-mcp-integration id=1289599380 v1.2.1 =
  POPRAWNE, zostaje; (b) homeassistant-ai/ha-mcp id=1056618941 v7.14.0 =
  LEGACY (glowne repo serwera), TO usunac. FIX = usunac (b).
  ⚠ OGRANICZENIE: ha_manage_hacs ma tylko akcje download/add_repository —
  BRAK remove/uninstall. Usuniecie repo = TYLKO przez HACS UI (rece Tomasza).
  Pulapka: identyczne nazwy, rozroznic po wersji (usunac 7.x, zostawic 1.x).
  Po usunieciu: ha_restart + weryfikacja repair_count. Sprawa KOSMETYCZNA
  (updates dzialaja), nie pilna. Status: odlozone (Tomasz na resztkach limitu,
  mid-mesh).
- JACUZZI (Lay-Z-Spa ESP32) po zmianie sieci: reconnect OK, connection=on,
  IP 192.168.0.115, publikuje przez MQTT do brokera. ALE RSSI = -77 dBm
  (slabo!) → lokalny panel ESP po IP "strasznie muli". Przyczyna = slaby
  sygnal w strefie, nie soft. FIX = mesh RE550 (ta sama martwa strefa co PV).
  Interwal raportowania (notification_time) = 0/unknown po restore → ESP
  publikuje tylko przy zmianie (stad zamrozone timestampy gdy idle);
  do ew. ustawienia pozniej. sensor.layzspa_error=2, reboot_reason=Exception
  — drobne, na pozniej. PRZY AX55: DODAC rezerwacje DHCP dla MAC ESP jacuzzi
  (obecnie .115) — dopisac do listy .200-.206 strefy PV.
- JACUZZI — WLASCIWA DIAGNOZA (13:06 PL, wczesniej BLEDNIE uznalem ze dziala!):
  Tomasz mial racje: "nie reaguje i pokazuje bzdury". ESP NIE jest podlaczony
  do nowego brokera .250. Dowody: binary_sensor.layzspa_connection zamrozony
  (retained "on" z 12:54, nie odswieza sie), sensor.layzspa_pump_time wygasl
  do unavailable, connect_count stoi 792 (ESP nie reconnectuje do .250),
  BRAK addona spa (ESP publikuje do brokera bezposrednio). W logach mosquitto
  ZERO prob polaczenia z .115 → ESP celuje w STARY adres brokera / nie na .250.
  => HA pokazuje stare retained wartosci (bzdury), komendy z HA ida na .250
  ktorego ESP nie slucha (zero reakcji). To NIE auth (brak prob logowania) —
  czysto ZLY ADRES BROKERA w ESP.
  FIX: na stronie ESP (.115) → ustawienia MQTT → broker=192.168.0.250 port 1883,
  login/haslo zostawic. BLOKER: strona ESP muli przez sygnal -77 → NAJPIERW
  mesh (RE550 blisko jacuzzi), POTEM zapis brokera na ESP. Do potwierdzenia:
  jaki adres brokera ESP ma teraz wpisany.
  LEKCJA: dashboard pokazujacy wartosci ≠ urzadzenie dziala; przy MQTT
  sprawdzac last_reported (nie tylko last_updated) + proby polaczenia klienta
  w logach brokera, nie ufac retained "on".
- JACUZZI — POTWIERDZONE ZRODLO (13:1x PL): strona ESP 192.168.0.115/mqtt.html
  (lay-z-spa module, visualapproach firmware) pokazala MQTT host addr =
  192.168.0.124 = STARY SERWER (padly). To 100% przyczyna "nie reaguje +
  bzdury". Pozostale pola: port 1883, Username=esp_jacuzzi (konto MQTT =
  user HA, przetrwal restore), Client ID=layzspa, Base Topic=layzspa,
  Telemetry Interval=20s. FIX = zmienic host addr na 192.168.0.250 + SAVE
  (reszte zostawic). Uwaga: pole hasla moze sie wyczyscic przy zapisie →
  jak nie polaczy, wpisac ponownie haslo esp_jacuzzi. Po zapisie weryfikacja:
  mosquitto log "New client connected ... as layzspa" z .115 + encje
  layzspa_* przestaja byc unavailable/zamrozone, last_reported plynie co 20s.
  PRZY MESH: sygnal -77 slaby ale MQTT lekkie — powinno trzymac; RE550
  poprawi. Rezerwacja DHCP dla ESP jacuzzi (.115) do listy.
- JACUZZI FIX — KROK WYKONANY (13:2x PL): admin_change_password na userze HA
  NIE PRZESZEDL (webhook ha-mcp = "Unauthorized" na config/auth_provider/*).
  OBEJSCIE: dodano esp_jacuzzi jako LOGIN BROKERA (mosquitto addon logins:
  ['hamqtt','esp_jacuzzi']) z haslem qg76srfdmjda (w /root/.esp_jacuzzi_pass).
  Broker sprawdza wlasne loginy (OR z userami HA) → ESP zaloguje sie lokalnie
  mimo ze user HA 'Jacuzzi'/esp_jacuzzi (id a3d46dade8fc4869b4799c336eaade3c)
  ma inne, nieznane haslo. USTAWIENIA DO WPISANIA W ESP (.115/mqtt.html):
  host=192.168.0.250, port=1883, username=esp_jacuzzi, password=qg76srfdmjda,
  Client ID=layzspa, Base Topic=layzspa → SAVE. Czekam na potwierdzenie +
  weryfikacja: mosquitto log "New client ... layzspa" z .115, encje ozywaja.
  NB: admin_change_password niedostepne z tego kanalu = lekcja (userow HA nie
  zmienimy zdalnie; konta MQTT robic jako logins brokera).
- ✅ JACUZZI NAPRAWIONE — POTWIERDZONE (13:22 PL): log brokera "New client
  connected from 192.168.0.115 as layzspa (u'esp_jacuzzi')". connect_count
  zresetowany 792→1 (swieze polaczenie z nowym brokerem). pump_time plynie
  na zywo (0.73→0.74, last_reported co ~20s). Sterowanie z HA znow dziala.
  ROZWIAZANIE: ESP host .124→.250 + konto brokera esp_jacuzzi/qg76srfdmjda
  (login mosquitto, bo admin_change_password usera HA byl Unauthorized).
  Konto HA 'Jacuzzi' (esp_jacuzzi) ma nadal swoje stare, nieznane haslo —
  nieuzywane, ESP loguje sie loginem brokera. Rezerwacja DHCP dla .115 przy
  AX55 do listy strefy PV.
