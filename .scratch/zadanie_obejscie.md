# ZADANIE CALEJ DRUZYNY (Zenek + Genek + Henio): OBRAZ kamer Xiaomi DZIS - obejsc blokade

CEL Tomasza: obraz z kamery Xiaomi .112 w HA Dzialki DZIS (nie jutro). Kazdy PODPISANY glos, potem wspolny wniosek. DOCZYTAC ZRODLO / POSZUKAC, absolutnie NIE ZGADYWAC (zgadywanie wpakowalo nas w blokade). Decyduje Tomasz.

## STAN (wszystko gotowe OPROCZ tokenu konta)
- go2rtc addon a889bffc_go2rtc w HA Dzialki (v1.9.14, host_network=true) DOSIEGA kamery (.112 ping OK z hosta HA, izolacji NIE ma). Stream wpiety /config/go2rtc.yaml: `cam_zachod_112: xiaomi://6338598787:de@192.168.0.112?did=1022085077&model=chuangmi.camera.021a04`.
- go2rtc API z VPS: `curl http://100.115.112.5:1984/api/...` (dziala 200). SSH `root@100.115.112.5` klucz /root/.ssh/id_ed25519 -> powloka HA Dzialki.
- MAM w /tmp/go2rtc_token.txt (chmod 600): userId=6338598787, passToken(323zn), ssecurity, serviceToken - z Extractora QR longPolling (klasa QrCodeXiaomiCloudConnector: _pass_token=response_data['passToken'], _ssecurity, _serviceToken=cookies['serviceToken']). region=de.

## DWA NIEZALEZNE PROBLEMY (przeczytane z go2rtc add.html + issues, NIE zgadniete):
A) passToken z QR NIE dziala w go2rtc: `xiaomi: 6338598787: 'V1:<passToken>'` -> KONTO zapisane (/api/xiaomi -> ['6338598787']) ALE load devices (/api/xiaomi?id=6338598787) = **401 Unauthorized** we wszystkich regionach (de/i2/sg/us/ru/cn). issue #2233: `func LoginWithToken(userID, passToken)`. Wiec teoretycznie V1=passToken, a jednak 401.
B) Password login DZIALA (haslo maksys79 przyjete) ale FLOW (z add.html): POST /api/xiaomi `username=EMAIL&password=HASLO&server=de` -> {captcha|verify_email|verify_phone}; verify_email -> kod na email; POST /api/xiaomi `verify=KOD` (SAMO, BEZ login, sesja server-side) -> passToken. POTWIERDZONE: verify=zlyKod -> 70014 'blad kodu' (parametr+sesja OK). ALE Xiaomi ZABLOKOWAL wysylke kodu do jutra: 70022 'Wyslano zbyt wiele kodow, sprobuj jutro' (moja wina - dodawalem login do verify -> resend). Przy triggerze Xiaomi WYMUSZA verify_email (NIE daje captcha ani verify_phone).

## ROZSTRZYGNIJ - jak OBRAZ DZIS mimo blokady (podpisany glos KAZDY, potem wniosek):
1. **DROGA A - passToken/V1** (GENEK+ZENEK doczytajcie ZRODLO): github AlexxIT/go2rtc internal/xiaomi/cloud.go + pkg/xiaomi - jak DOKLADNIE parsuje 'V1:', co LoginWithToken robi z passToken, DLACZEGO QR-owy passToken daje 401 a password-login by dzialal. Czy z passToken+ssecurity+serviceToken (MAM) da sie zbudowac DZIALAJACY token? Moze V1 to nie surowy passToken tylko combo/base64? Czy jest V2/inny format?
2. **DROGA B - sesja Extractora** (obejscie): Extractor (ssecurity+serviceToken) DZIALA - pobral kamery z de. Czy przekazac te SESJE do go2rtc BEZPOSREDNIO (nie przez password login)? go2rtc config przyjmie ssecurity/serviceToken? Cookie injection do go2rtc? (mam SSH do HA Dzialki + go2rtc API).
3. **DROGA C - verify_phone SMS** (obejscie blokady email): Xiaomi zablokowal EMAIL. Da sie WYMUSIC verify_phone (SMS na tel +43, osobny limit)? Jaki parametr/endpoint go2rtc/Xiaomi wymusza SMS zamiast email? (mam android control - ODCZYTAM SMS z telefonu Tomasza).
4. **DROGA D - inny serwer**: blokada per region de? Login to samo konto przez inny serwer (i2/sg/ru/cn) omija blokade wysylki?
5. NAJPEWNIEJSZA droga DZIS + KONKRETNY plan wykonania (komendy).

Zasada 17.07: DOCZYTAC zrodlo go2rtc, nie zgadywac. Sekrety (passToken/ssecurity/serviceToken) NIE do meldunku.
