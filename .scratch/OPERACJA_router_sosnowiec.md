# OPERACJA W TOKU: ZMIANA NUMERACJI ROUTERA SOSNOWCA (start 6.08.2026 ~09:0x CEST)

CEL: rozwiazac kolizje 192.168.0.0/24 miedzy Dzialka a Sosnowcem — zmienic numeracje routera SOSNOWCA na 192.168.50.0/24, zeby obie lokacje dzialaly naraz przez Tailscale.
DECYZJA TOMASZA 6.08: "zrob to sam", "Rob" — pelna zgoda na wykonanie. Tomasz bedzie FIZYCZNIE na miejscu (Sosnowiec) ~09:1x-09:2x (fizyczny rollback).

## BEZPIECZENSTWO POTWIERDZONE (pomiar 6.08)
- HA Sosnowca na DHCP: interfejs end0 (ethernet, primary), method=auto, brama 192.168.0.1. => po zmianie numeracji sam dostanie nowy IP + brame, utrzyma internet i Tailscale. GLOWNE RYZYKO (odciecie) ZNIESIONE.
- Tomasz na miejscu = fizyczny rollback gdyby cos padlo.

## ROUTER SOSNOWCA — ZIDENTYFIKOWANY (nie pomylic jak 5.08!)
- **Archer MR600 "Wybickiego 11"**, MAC **B0-A7-B9-04-BE-28** — w TP-Link Tether jako "Urzadzenie Cloud". Nazwa = adres Sosnowca. TEN zmieniamy.
- BLIZNIAK DZIALKI: Archer MR600 (bez nazwy), MAC D8-47-32-5C-10-7A — to najpewniej Dzialka. ZAKAZ TYKANIA (D-0066/67). To on i Sosnowiec (oba fabrycznie 192.168.0.1) daja kolizje.
- Dom (Walding): Archer AX55 Pro mesh + extendery RE190/RE315/RE550, siec 192.168.68.0/24 (bez konfliktu).

## WEZLY TAILSCALE
- Sosnowiec HA: 100.67.61.100 (SSH z VPS dziala, klucz /root/.ssh/id_ed25519, user root@ -> kontener core-ssh; curl 192.168.0.1 z niego siega router Sosnowca)
- Dzialka HA: 100.115.112.5 (MA trase 192.168.0.0/24 teraz, primary)
- Dom HA: 100.87.37.19 (192.168.68.0/24)
- Telefon Fold7: 100.101.116.106 (online w TS; ale bramka ADB/MCP padala gdy Tomasz w ruchu)

## PLAN KROKOW (dokonczyc gdy telefon stabilny / Tomasz na miejscu)
1. Tether -> wybrac "Archer MR600 Wybickiego 11" (NIE bezimienny MR600 Dzialki) -> zalogowac jesli trzeba -> Ustawienia sieci LAN -> IP routera 192.168.0.1 -> zmienic na 192.168.50.1 -> zapisac (router reboot). PRZED ZAPISEM potwierdzic ze to Sosnowiec (obecny LAN 192.168.0.1 + podlaczone HA Sosnowca).
2. Poczekac ~1-2 min, zweryfikowac: HA Sosnowca (100.67.61.100) dalej online w Tailscale + dostal nowy IP w 192.168.50.x (ssh -> ha network info).
3. Na HA Sosnowca ustawic advertise-routes=192.168.50.0/24 (tailscale up --advertise-routes na jego node) + ZATWIERDZIC w panelu admin Tailscale (login.tailscale.com, konto tomasz.maxisch@gmail.com — przez telefon).
4. Wlaczyc/zatwierdzic druga trase: Dzialka zostaje 192.168.0.0/24, Sosnowiec 192.168.50.0/24 — ZERO kolizji, obie naraz.
5. Zweryfikowac z VPS: obie trasy w tailscale status, oba HA osiagalne.

## STATUS TERAZ
Wszystko przygotowane, bezpieczenstwo potwierdzone. CZEKAM az Tomasz dojedzie (~15 min) i telefon zlapie WiFi Sosnowca — wtedy krok 1 przez Tether. Lacze telefonu padalo w ruchu, wiec NIE forsowac zmiany routera przez niestabilne lacze (ryzyko zapisu w polowie).
NOWA NUMERACJA: 192.168.50.0/24 (nie koliduje z Dzialka .0 ani Dom .68).

## WYNIK 6.08 ~11:0x — WYKONANE I POTWIERDZONE
- MR600 LAN zmieniony 192.168.0.1 -> 192.168.50.1 (zapisane w panelu przez Tomasza na miejscu). Panel 192.168.50.1 -> HTTP 200.
- HA Sosnowca: brama end0 = 192.168.50.1, DHCP, internet OK, Tailscale 100.67.61.100 online.
- KOLIZJA ROZWIAZANA: Dzialka 192.168.0.0/24, Sosnowiec 192.168.50.0/24 (rozne podsieci).
- ZOSTALO (opcjonalne domkniecie planu): Sosnowiec (100.67.61.100) NIE oglasza jeszcze trasy 192.168.50.0/24 do Tailscale (trasy=[]). Chcac LAN Sosnowca zdalnie jak Dzialka -> advertise-routes=192.168.50.0/24 na HA Sosnowca + zatwierdzenie w panelu admin. Obie trasy moga byc naraz bez kolizji.
- Adres HA Sosnowca w LAN: z 192.168.0.107 na 192.168.50.x (DHCP) — zaktualizowac gdzie zapisany (HA_WYBICKIEGO.md, connectory).
- LEKCJA: core-ssh na Sosnowcu okrojony (bez python3/openssl) vs Advanced SSH na Dom. Port ADB Fold7 ROTUJE przy zmianie WiFi (dok. infrastruktury) — po przelaczeniach nie jest 5555.

## ETAP B WYKONANY 6.08 ~14:56 — TRASA SOSNOWCA W TAILSCALE (ZAMKNIETE)
- advertise_routes=192.168.50.0/24 ustawione na add-onie Tailscale HA Sosnowca przez: python3 tools/mcp_wybickiego.py --narzedzie ha_manage_addon --argumenty '{"slug":"a0d7b954_tailscale","options":{"advertise_routes":["192.168.50.0/24"]}}' (UWAGA: param w opakowaniu "options", NIE top-level; set_options-mode ODRZUCA; potem action=restart osobno, call urywa sie bo Tailscale schodzi — restart i tak dochodzi).
- Trasa ZATWIERDZONA w panelu admin Tailscale przez telefon Fold7 (apka Android Remote Control MCP port 8080, connector "Telefon Fold7" — NIE ADB): login.tailscale.com/admin/machines -> homeassistant (100.67.61.100) -> menu ... -> Edit route settings -> zaznacz 192.168.50.0/24 -> Save.
- POTWIERDZONE z VPS: Sosnowiec allowed=192.168.50.0/24, Dzialka allowed=192.168.0.0/24 (obie naraz, ZERO kolizji). Router 192.168.50.1 z VPS: PING OK + panel HTTP 200.
- CEL OSIAGNIETY: urzadzenia LAN Sosnowca dostepne zdalnie przez Tailscale z kazdego wezla.
- LEKCJE: (1) sterowanie Fold7 = apka MCP port 8080, NIE ADB (port ADB ROTUJE przy zmianie WiFi = slepa uliczka; bylo w telefon-mcp.md, trzeba bylo zajrzec od razu). (2) WebView (panel Tailscale w Chrome) = tap_node wspolrzednosciowy dziala, click_node nie. (3) HA Sosnowca dostal nowy LAN IP (192.168.0.107 -> 192.168.50.x) — connectory przez Tailscale (100.67.61.100) dzialaja niezaleznie od LAN IP.
