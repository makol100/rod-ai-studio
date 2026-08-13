PROBLEM SOSNOWIEC (HA 100.67.61.100, tailscale node "homeassistant"): Zigbee2MQTT addon (slug 45df7312_zigbee2mqtt, v2.13.0) stan ERROR, pada w petli. Koordynator ConBee3 startuje OK, 6 urzadzen joined - to NIE problem radia Zigbee. Z2M nie moze polaczyc z MQTT: log "Connecting to MQTT server at mqtt://192.168.0.107:1883" -> "MQTT failed to connect, exiting (connack timeout)" -> exit.

PRZYCZYNA: siec Sosnowca zmienila sie z 192.168.0.x na 192.168.50.x (HA host teraz 192.168.50.103). Z2M laczy do STAREGO brokera 192.168.0.107 (martwy, nc timeout). Broker Mosquitto (addon core_mosquitto v7.1.0) DZIALA, core-mosquitto:1883 OTWARTY. HA MQTT integration w /config/.storage/core.config_entries ma broker="core-mosquitto" (POPRAWNE).

SEDNO: Z2M v2 bierze 192.168.0.107 z Supervisor MQTT service (bashio::services mqtt), NIE z pliku. Dowod: reczna zmiana /config/zigbee2mqtt/configuration.yaml server->core-mosquitto ZNIKA - Z2M regeneruje plik przy KAZDYM starcie na 192.168.0.107 (testowane stop+edit+start). 192.168.0.107 NIE MA w .storage/core.config_entries (tylko w .storage/auth=logi). /addon_configs/45df7312 PUSTY. /mnt PUSTY w kontenerze.

PROBOWANE BEZ SKUTKU: edycja pliku; ha apps restart core_mosquitto; ha supervisor restart (caly) - Z2M NADAL 192.168.0.107.

DOSTEP: SSH core-ssh (klucz VPS port 22). DZIALA: komenda "ha" (apps install/start/stop/restart/logs/info, supervisor restart) + pliki /config i /config/.storage. NIE DZIALA (token waski): /core/api/states=0 encji; /services/mqtt=403; POST /addons/*/options=403. Advanced SSH addon (a0d7b954_ssh) zainstalowany, protection OFF + nasz klucz (ma docker+token manager) ALE nie na porcie 22 (core_ssh host_network trzyma 22; po stop core_ssh -> 22 refused, Advanced SSH nie re-binduje bez restartu; nohup w kontenerze core_ssh ginie przy stop kontenera = chicken-egg). Klaudek raz stracil tak SSH, Tomasz odzyskal recznie.

PYTANIE ROZSTRZYGALNE (podaj KONKRETNE komendy z sesji core-ssh, gotowe do wklejenia):
(A) Jak zresetowac Supervisor MQTT service host 192.168.0.107 -> core-mosquitto (albo 192.168.50.103), majac TYLKO komende "ha" (apps) + pliki /config, token bez /services i /addons/options?
(B) ALBO jak BEZPIECZNIE (bez utraty jedynego SSH) przelaczyc port 22 z core_ssh na Advanced SSH, skoro proces w tle w core_ssh ginie przy jego stopie a Advanced SSH nie re-binduje 22 bez restartu?
Podaj droge z komendami. Nie znasz pewnej - napisz NIE WIEM, nie zgaduj.
