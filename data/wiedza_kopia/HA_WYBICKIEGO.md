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
