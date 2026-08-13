# ZADANIE (Zenek + Henio): OBRAZ kamer Xiaomi w HA Dzialki — bariera izolacji

CEL: obraz z kamer Xiaomi (chuangmi.camera.*) w HA Dzialki. Kazdy PODPISANY glos, potem wspolny wniosek. Rozbieznosc zostaje. Decyduje Tomasz.

## FAKTY (sprawdzone 8.08)
- Kamery WYCIAGNIETE (Extractor przez telefon Tomasza): .112 did=1022085077 model=chuangmi.camera.021a04; .114 did=371002387 model=chuangmi.camera.029a02; .127 did=323183877 model=chuangmi.camera.ipc019; .121 did=448715358 model=chuangmi.camera.025b02. userId=6338598787, region=de. did+device-token w /tmp/qr3.txt na VPS.
- go2rtc postawiony na VPS (docker alexxit/go2rtc latest, dziala HTTP 200) ALE VPS NIE DOSIEGA kamer: .112 GLUCHA na ping I portach 554/6668/8554/54321/5000. Router Dzialki .0.1 z VPS PING OK, ale kamera .112 nie. (go2rtc VPS juz usuniety - i tak bezuzyteczny.)
- HA Dzialki NIE ma tych kamer zintegrowanych (tylko update entities Xiaomi Home/MiIO/Miot Auto).
- HA Dzialki SSH ZAMKNIETY (port 22 refused). Dostep: MCP connector "HA DZIALKA" (ha_call_service, ha_get_addon, ha_manage_addon, ha_eval_template, ha_config_*) + panel :8123 (HTTP 200 przez Tailscale). Wczesniej addon Tailscale zmienialem przez ha_manage_addon.
- Router Dzialki: D-0066 NIE RUSZAC bez zgody Tomasza. Odczyt dziala: tplinkrouterc6u haslo <USUNIETE> (Client List OK).

## RESEARCH (go2rtc README + issues, potwierdzone, czytac cale):
- go2rtc xiaomi:// "Connection to the camera is LOCAL ONLY" (README, powtorzone 3x). Klucze szyfrowania z chmury (internet), ale STREAM P2P bezposrednio do kamery IP w LAN. => go2rtc MUSI byc w LAN Dzialki i DOSIEGAC kamery lokalnie. VPS bezuzyteczny - POTWIERDZONE.
- go2rtc 1.9.14 ma BUG: CS2 cameras i/o timeout (issue #2294, #2048); v1.9.13 dziala. UZYC 1.9.13, nie latest.
- CS2 vendor supported, TUTK nie. chuangmi zwykle mess+cs2 (dzialaja), niektore legacy EOF.
- KLUCZOWA POSZLAKA: router .0.1 dosiegalny a kamera .112 NIE = prawdopodobnie CLIENT/AP ISOLATION na WiFi routera (izoluje klientow miedzy soba) ALBO firewall kamery. Jesli client isolation - NAWET go2rtc w HA Dzialki (inny klient WiFi) NIE dosiegnie kamer.

## ROZSTRZYGNIJ (podpisany glos, potem wniosek)
1. Jak ZDIAGNOZOWAC czy kamery sa dosiegalne z LAN Dzialki, MAJAC tylko MCP HA (bez SSH/roota)? Konkretne pomysly: (a) ha_eval_template - czy da sie nim odpalic cokolwiek sieciowego? (b) zainstalowac go2rtc jako ADDON w HA Dzialki (host mode) i jego LOG powie czy dosiega kamere; (c) odczytac w panelu routera (tplinkrouterc6u) czy "AP Isolation"/"Access Control" wlaczone; (d) HA integracja Xiaomi Miot - dodac kamere po IP i zobaczyc czy HA ja widzi (HA jest w LAN Dzialki).
2. GDZIE go2rtc: addon w HA Dzialki (host mode, 1.9.13) - jak zainstalowac przez MCP/panel :8123? Czy jest oficjalny addon (AlexxIT/hassio-addons)?
3. Jesli to CLIENT ISOLATION na routerze: czy wylaczyc (D-0066 = decyzja Tomasza)? Czy jest droga BEZ ruszania routera?
4. Config go2rtc dla 021a04/029a02: CS2? transport udp/tcp? subtype? Jak podac konto (V1 token - go2rtc WebUI login, moze przez telefon jak Extractor).
5. PLAN krok po kroku, najnizszy koszt, z jasnym "co wymaga Tomasza / co wymaga routera".

Zasada 17.07: uczyc sie z issues, czytac do konca, nie zgadywac.
