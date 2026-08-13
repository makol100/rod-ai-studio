# Kontrola: Sosnowiec MQTT/Z2M

Stan podany przez Tomasza: Z2M 2.13.0 nadpisuje `configuration.yaml` adresem MQTT
`192.168.0.107`; źródłem ma być Supervisor MQTT service. Dostęp tylko przez core-ssh:
CLI `ha`, pliki `/config`; wąski token blokuje `/services` i `/addons/options`. Advanced
SSH jest zainstalowany, protection off, ma docker/token manager, ale port 22 zajmuje core_ssh.

Pytanie rozstrzygalne: podaj wyłącznie pewną, udokumentowaną i bezpieczną sekwencję komend
wykonywalną z core-ssh, która (A) poprawi Supervisor MQTT service na core-mosquitto / aktualny
adres albo (B) przełączy port 22 na Advanced SSH bez ryzyka utraty jedynego dostępu. Zweryfikuj
składnię aktualnego Home Assistant CLI/Supervisor. Jeśli brak pewnej drogi, odpowiedz NIE WIEM.
Nie wykonuj żadnych zmian na HA.
