# ZADANIE (Zenek + Henio): plan — OBRAZ z kamer Chuangmi/Xiaomi w HA Dzialki

CEL Tomasza (7.08): docelowo widziec OBRAZ z 2 urzadzen Chuangmi (Xiaomi) w HA Dzialki. Kazdy podpisany glos, potem wspolny wniosek. Rozbieznosc zostaje. Decyduje Tomasz.

## FAKTY (z routera Dzialki + HA — sprawdzone dzis)
- 2 urzadzenia "chuangmi" na routerze Dzialki: .112 (MAC 78-8B-2A-1A-FA-F2), .114 (78-8B-2A-CD-64-7C). MAC prefix 78-8B-2A = Chuangmi Technology (Xiaomi).
- Trzecia, JAWNA kamera: chuangmi_camera_ipc019 (.127) — inny MAC (64-90-C1-...).
- .112/.114 NIE oddaja portow lokalnie z VPS (nmap 554/80/443/54321 puste, curl HTTP 000) — Xiaomi gada przez chmure Mi.
- HA Dzialki MA integracje Xiaomi (Xiaomi Home + Xiaomi MiIO + Xiaomi Miot Auto) — update entities widoczne (update.xiaomi_home_update, xiaomi_miio_raw_update, xiaomi_miot_auto_update).
- Model .112/.114 NIEUSTALONY (nazwa gola "chuangmi" bez "camera"/"ipc" — moga to byc kamery Mi starsze ALBO pilot IR chuangmi.remote). NAJPIERW potwierdzic ze to kamery.
- Router Dzialki: dostep tylko ODCZYT (D-0066 nie zmieniac routera).

## RESEARCH PRAKTYKOW (issues HA al-one/hass-xiaomi-miot + fora, 2023-2025):
1. **go2rtc + xiaomi:// (NAJNOWSZE XI.2025, rekomendowane w spolecznosci)**: go2rtc wbudowany w HA (platforma camera) obsluguje strumien `xiaomi://`. Logujesz konto Mi Home w go2rtc WebUI (wybor regionu rejestracji), znajdujesz `did` (device id) + model, dodajesz wpis xiaomi:// -> strumien do HA/Frigate. BEZ stalej chmury, BEZ flashowania firmware, ZACHOWUJE Mi Home. Companion: PiotrMachowski Xiaomi-cloud-tokens-extractor (pobiera did+lokalne IP+model z konta Mi).
2. **hass-xiaomi-miot (al-one)**: daje KONTROLE kamery, ale STRUMIEN czesto NIE dziala — brak "start-p2p-stream", "stream_address blank", blad remote -706010002 "Service does not exist" (issues #2547, #1321, #2727, #17). Kontrola TAK, obraz czesto NIE. PULAPKA — nie liczyc na to jako glowna droge.
3. **RTSP natywny**: niektore Xiaomi maja RTSP po wlaczeniu "Local Network Access" w Mi Home (firmware >=1.5.0), potem Generic IP Camera/FFmpeg w HA. ALE wlaczenie RTSP servera CZESTO WYLACZA apke Mi Home. Nie wszystkie modele. 2.4GHz only.
4. **Micam** (XI.2025): dedykowany RTSP bridge non-official dla Xiaomi kamer — pushuje strumien lokalnie do RTSP.
5. **Custom firmware (Xiaomi-Dafang-Hacks)**: flashowanie, RTSP na 8554, ale TRACI Mi Home. Inwazyjne, ostatecznosc.

WNIOSKI z researchu: (a) MODEL ma znaczenie — miot-spec (home.miot-spec.com/spec/chuangmi.camera.XXX) pokazuje czy kamera ma p2p-stream; (b) potrzebny did/token z konta Mi (Xiaomi Cloud Tokens Extractor); (c) najpewniejsza nowoczesna: go2rtc xiaomi://; (d) NAJPIERW potwierdzic ze .112/.114 to w ogole kamery.

## ROZSTRZYGNIJ (podpisany glos, potem wspolny wniosek)
1. Rekomendowana DROGA dla naszych kamer Chuangmi do HA Dzialki (obraz): go2rtc xiaomi:// czy inna? Uzasadnij vs pulapka miot.
2. KOLEJNOSC krokow: od czego zaczac? (potwierdzic ze .112/.114 to kamery + ustalic model + did+token przez Xiaomi Cloud Tokens Extractor z konta Mi Tomasza)
3. Czego potrzeba OD TOMASZA (login+region konta Mi Home? uruchomienie Extractora?).
4. RYZYKA/pulapki (miot blank stream; RTSP wylacza Mi Home) — jak omijac.
5. Najnizszy koszt + najpewniejsze (27.07). Jesli .112/.114 to NIE kamery (pilot IR) — co wtedy.

Zasada 17.07: uczyc sie z cudzych bledow (te issues), czytac do konca. Sprawdzac u zrodla, nie zgadywac.
