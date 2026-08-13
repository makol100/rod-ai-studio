# ZADANIE (Zenek + Henio): go2rtc V1 token - 401 Unauthorized

CEL: obraz kamer Xiaomi w HA Dzialki. go2rtc STOI, dosiega kamery, ale auth do chmury Xiaomi = 401. Kazdy PODPISANY glos, potem wspolny wniosek. Rozbieznosc zostaje. Decyduje Tomasz.

## FAKTY (sprawdzone 8.08)
- go2rtc 1.9.14 addon w HA Dzialki (host_network=true). Config /config/go2rtc.yaml (zapisuje przez SSH root@100.115.112.5 kluczem VPS).
- Stream wpiety: `cam_zachod_112: xiaomi://6338598787:de@192.168.0.112?did=1022085077&model=chuangmi.camera.021a04`. /api/streams pokazuje producer OK.
- Sekcja konta: `xiaomi: 6338598787: "V1:<passToken>"` (passToken 323 znaki).
- go2rtc DOSIEGA kamere: .112 ping OK z hosta HA (izolacji NIE ma, potwierdzone SSH).
- TEST: curl /api/frame.jpeg?src=cam_zachod_112 -> HTTP 200, 0 bajtow. LOG go2rtc: `error="streams: 401 Unauthorized"` (mjpeg.go:82). Czyli auth do chmury Xiaomi ZLA (klucze szyfrowania sie nie pobieraja).
- MAM z Extractora (QR longPolling login, /tmp/go2rtc_token.txt chmod 600, /tmp/qr6.txt): userId=6338598787, passToken (323zn), ssecurity, serviceToken. Extractor QrCodeXiaomiCloudConnector pola: self._pass_token=response_data["passToken"], self._ssecurity, self._serviceToken=cookies["serviceToken"], self.userId.

## RESEARCH (issues go2rtc + fora):
- issue #2233: "go2rtc uses passToken. func LoginWithToken(userID, passToken string)". Sugeruje V1 = passToken. ALE u nas 401 z passToken.
- privatehomelab (Extractor 2FA fix): sesja go2rtc/micloud = 4 wartosci: **sSecurity, userid, servicetoken, cUserId** (NIE passToken!). SPRZECZNE z #2233.
- issue #2129/#2237: 401 przy "load devices" na 1.9.14 (need_verify=true, empty 401 body) - moze zmiana Xiaomi API / problem konta.
- go2rtc V1 token DOKLADNY FORMAT nieustalony: passToken sam? ssecurity+serviceToken? base64 kombinacja? cUserId potrzebny?

## ROZSTRZYGNIJ (podpisany glos, potem wniosek)
1. Jaki DOKLADNY format go2rtc "V1:" token? (Henio: poszukaj w sieci go2rtc internal/xiaomi cloud.go / api.go - JAK parsuje "V1:" i co LoginWithToken bierze; nie zgaduj, znajdz kod/opis.)
2. Jak ZBUDOWAC V1 z tego co mam (userId/passToken/ssecurity/serviceToken)? Kandydaci: "V1:passToken" (mam, 401); "V1:base64(json)"; "V1:ssecurity:serviceToken"; moze passToken to nie to pole.
3. Czy 401 to na pewno token konta, czy CO INNEGO (kamera CS2 auth osobno? trzeba najpierw "load devices"? passToken 323zn za dlugi/zly?).
4. Najpewniej: zbudowac V1 recznie z sesji (mam ssecurity/serviceToken/passToken) vs go2rtc WebUI login (WYMAGA hasla Mi Home - Tomasz NIE PAMIETA, wiec odpada). Wiec reczny V1 to jedyna droga - jak dokladnie.
5. PLAN: konkretny string "V1:..." do wpisania w go2rtc.yaml + jak zweryfikowac (log 401 znika / klatka niepusta).

Zasada 17.07: czytac ZRODLO, nie zgadywac. Uczyc sie z issues. passToken/ssecurity/serviceToken NIE wpisywac do meldunku (wrazliwe jak haslo).
