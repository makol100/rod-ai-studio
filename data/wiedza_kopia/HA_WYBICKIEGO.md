# HA WYBICKIEGO — MIESZKANIE W SOSNOWCU (uruchomione 5.08.2026)

**Trzecia lokalizacja** obok Dom (Walding, Austria) i Dzialka (Wozniki).
Tomasz 5.08: *„Masz miec pelen dostep jak do domu albo dzialki."*

## ADRESY

| do czego | adres |
|---|---|
| lacznik MCP Klaudka | `https://sosnowiec.157-90-155-155.sslip.io/private_1S_c5tNNIZ_qWO_4Ks777A` |
| aplikacja HA — w mieszkaniu | `http://192.168.0.107:8123` |
| aplikacja HA — z zewnatrz (Tailscale) | `http://homeassistant.tail0109d4.ts.net:8123` |
| z VPS (Tailscale) | `http://100.67.61.100:8123` · MCP: `:9583` |

Tailscale: nazwa `homeassistant`, adres `100.67.61.100`. HA 2026.7.4, strefa Europe/Warsaw.
Klucz dostepu: `/root/.ha_sosnowiec_token` (prawa 600).

## CZYM SIE ROZNI OD DZIALKI — WAZNE

**Dzialka** idzie przez webhook: `dzialka.157-90-155-155.sslip.io/api/webhook/mcp_<hash>`
— potrzebuje dodatku *Nabu Casa Webhook Proxy*, ktory ten webhook tworzy.

**Wybickiego POMIJA posrednika webhooka.** Brama uderza WPROST w serwer MCP na porcie 9583,
pod tajna sciezka, ktora dodatek generuje sam:
```
sosnowiec.157-90-155-155.sslip.io {
	@mcp path /private_1S_c5tNNIZ_qWO_4Ks777A*
	handle @mcp {
		reverse_proxy 100.67.61.100:9583 { ...zdjete naglowki X-Forwarded-*... }
	}
	handle { respond "Nie ma tu nic." 404 }
}
```
**Jedno ogniwo mniej, ktore moze sie zepsuc.** Sprawdzone: korzen adresu zwraca 404,
odpowiada wylacznie tajna sciezka.

## SPRZET (zmierzone przez SSH 5.08)

**Raspberry Pi 4 (64-bit)**, `raspberrypi4-64`, aarch64. HA OS, jadro `6.18.34-haos-raspi`.
**RAM 7817 MB** (wolne 6606). **Dysk 28,5 GB** (wolne 19,1 GB).
Dla porownania: Dzialka i Dom chodza na mocniejszym sprzecie — przy ciezkich zadaniach
(rozpoznawanie, modele) pamietac o tym ograniczeniu.

## SSH — WLACZONY 5.08, DOSTEP PELNY

Tomasz: *„Instaluj terminal i SSH na Wybickiego."*
```
ssh root@100.67.61.100        # klucz /root/.ssh/id_ed25519 na VPS
```

**JAK TO ZROBIONO — bo zwykla droga nie dziala:**
Klucz dlugoterminowy HA **nie siega Supervisora** (401), wiec dodatku nie da sie zainstalowac
przez REST. **Obejscie: serwer MCP Wybickiego SAM ma token Supervisora.**
Narzedzie `tools/mcp_wybickiego.py` wola jego `ha_manage_addon` bez posrednictwa lacznika
w aplikacji — czyli Klaudek zainstalowal dodatek rekami dodatku, ktory tam juz stal.

**DWIE RZECZY, BEZ KTORYCH SSH NIE DZIALA — obie latwo przeoczyc:**
1. **`authorized_keys`** — bez wgranego klucza publicznego dodatek nie wpuszcza nikogo.
2. **`network: {"22/tcp": 22}`** — **PORT MUSI BYC WYSTAWIONY**. Domyslnie jest `null`,
   czyli terminal dziala TYLKO przez strone HA, nie przez siec.
   **Na Dzialce jest wlasnie `null` — dlatego SSH tam z zewnatrz NIE DZIALA**, wbrew temu,
   co Klaudek wczesniej zalozyl. Gdyby bylo potrzebne, trzeba zrobic to samo.

## CZEGO NIE DA SIE ZROBIC KLUCZEM — ZMIERZONE 5.08

Klucz dlugoterminowy HA daje pelen dostep do encji, urzadzen, automatyzacji i historii,
**ALE NIE DO SUPERVISORA**: `/api/hassio/supervisor/info` -> **HTTP 401**.
Instalacja dodatkow wymaga rak Tomasza albo SSH.

**Sosnowiec NIE MA dodatku Terminal & SSH** (port 22 odrzuca polaczenie, Tailscale SSH nieaktywny).
Dzialka GO MA. **Gdyby wlaczyc go na Wybickiego, Klaudek instalowalby dodatki sam.**

## RZECZY DO ZROBIENIA PRZEZ TOMASZA (stan 5.08)

1. **Tailscale: 2 trasy czekaja na zatwierdzenie** oraz wezel wyjsciowy.
   Bez zatwierdzenia tras **urzadzenia w sieci mieszkania sa nieosiagalne** — sam HA dziala.
   Wezel wyjsciowy prawdopodobnie NIEPOTRZEBNY (sluzy do przepuszczania calego ruchu
   internetowego przez tamten dom).
2. **Podmienic lacznik `Ha_Działka2` na `HA Sosnowiec`** — Ha_Działka2 prowadzi do TEJ SAMEJ
   instalacji co `HA DZIAŁKA` (zmierzone: obie zwracaja location_name „Działka", wersja 2026.7.4).
   Zdublowany lacznik zjada miejsce w oknie i nic nie wnosi.

## NAZWA — POPRAWIONA 5.08 11:20

Instalacja nazywala sie w srodku **„Dom"** — tak samo jak Walding. Zmienione na **„Wybickiego"**
poleceniem `config/core/update` przez WebSocket (zwykle REST API nie ma tej sciezki: 404).

## PRZEGLAD 5.08.2026 — CO ZNALEZIONO

**AKTUALIZACJE: ZERO.** HA core 2026.7.4, HA OS 18.2, supervisor 2026.07.5 — wszystko najnowsze.
Konfiguracja: `valid`, zero bledow.

### NAPRAWIONE

**1. ZABEZPIECZENIE GAZOWE NIE DZIALALO OD 8 DNI — najwazniejsze znalezisko.**
Automatyzacja „Wykrycie gazu zamkniecie zaworu gazu" byla WLACZONA i wygladala na sprawna,
ale jej wyzwalacz wskazywal `device_id: 258f191a...` — urzadzenie **niedostepne od 28.07 11:59**.
Zawor **nigdy by sie nie zamknal**. W mieszkaniu byl przy tym DRUGI, dzialajacy czujnik gazu
(`binary_sensor.gas_sensor_2_gaz`), ktorego ta automatyzacja nie widziala.
**Przepisana:** wyzwalacz `state` na OBA czujniki, akcja przez `entity_id` zamiast `device_id`.
Awaria jednego czujnika nie unieruchamia juz zabezpieczenia.

**2. DRUGA, BLEDNA INTEGRACJA TUYA** (`01KBQXSQG8BMH3EGP67VFH2B44`, stan `setup_error`)
— usunieta na polecenie Tomasza. Zostala jedna, `loaded`.

### PRZYCZYNA 107 MARTWYCH ENCJI — USTALONA

**Bramka Zigbee Setti SGW430 padla 28.07 o 11:59:18** i wrocila dopiero 5.08 o 13:11,
gdy Tomasz przelogowal Tuya. Wszystkie jej urzadzenia zamilkly W TEJ SAMEJ SEKUNDZIE —
dlatego to nie byly baterie. Po jej powrocie: **107 -> 45 niedostepnych.**

**BLAD KLAUDKA przy tej diagnozie:** zobaczyl `zha: not_loaded` i **ogłosil, ze Zigbee nie dziala**.
Nieprawda — Zigbee chodzi przez **Zigbee2MQTT** (6 urzadzen + mostek), ZHA to nieuzywana
pozostalosc. Tomasz poprawil: *„Zigbee dziala idioto."*
Klaudek widzial Zigbee2MQTT na liscie dodatkow i nie polaczyl faktow.

### ZOSTAJE DO ZROBIENIA

- **Czujnik gazu w kuchni i czujnik zalania w lazience nadal niedostepne** — nie zameldowaly sie
  jeszcze bramce po jej powrocie. Obudzic: czujnik zalania — zewrzec styki mokrym palcem;
  czujnik gazu — wyjac i wlozyc baterie.
- **Tuya: Tomasz nie moze zeskanowac kodu QR** tym samym telefonem, ktory go wyswietla.
  Obejscie: otworzyc HA na komputerze/tablecie i zeskanowac telefonem.
- **1209 wpisow o zbyt niskim napieciu** w dmesg (Raspberry Pi 4). Zasilacz jest ORYGINALNY —
  Tomasz: „mozliwe spadki napiecia" w sieci mieszkania. **Do obserwacji, nie przyczyna
  dzisiejszych awarii.**
- **Nabu Casa wygasa 9.08.2026** (zdalny dostep i tak wylaczony — jedzie przez Tailscale).
