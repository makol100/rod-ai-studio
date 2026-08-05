# MARTWE URZADZENIA — MATERIAL ROBOCZY DLA TOMASZA
Sporzadzone 05.08.2026 15:21.

> Tomasz 5.08: *„Zostawić tak jak jest. Muszę ogarnąć sam te wszystkie urządzenia pod Tuya.
> Co nie działa albo nie ma tego w ogóle, to usunąć z Tuya."*

**NICZEGO NIE USUNIETO.** To jest lista do przejrzenia, nie wykonana robota.

## JAK CZYTAC

Encja „niedostepna" = Home Assistant ma ja w rejestrze, ale urzadzenie sie nie odzywa.
Przyczyny bywaja trzy: **urzadzenie nie istnieje** (usuniete, sprzedane, wyrzucone),
**urzadzenie padlo** (bateria, zasieg, zasilanie), albo **duplikat** po drugiej integracji.

**UWAGA — dzisiejsza lekcja:** automatyzacja moze wisiec na martwej encji i WYGLADAC na sprawna.
Tak bylo z zaworem gazu: automatyzacja wlaczona, czujnik martwy od 8 dni, zawor nigdy by sie
nie zamknal. **Przed usunieciem czegokolwiek sprawdzic, czy nie jest uzywane.**

## WYBICKIEGO (Sosnowiec) — 43 niedostepnych encji

- `binary_sensor.czujnik_zalania_lazienka_wilgoc`
- `camera.kamera_wybickiego`
- `cover.drzwi_garazowe_drzwi`
- `media_player.65qned86a6a_beufljp3264`
- `media_player.dzialka_wszystkie_gl`
- `media_player.googlehome0292`
- `media_player.googlehome7663`
- `media_player.grupa_glowna`
- `media_player.grupa_glowna_2`
- `media_player.grupa_glowna_3`
- `media_player.home_speakers`
- `media_player.lg_webos_tv_nano82t6b`
- `media_player.lg_webos_tv_qned86a6a`
- `media_player.nest_hub_sypialnia`
- `media_player.nest_mini`
- `media_player.poddasze`
- `media_player.pokoj_do_rozrywki`
- `media_player.rosalia`
- `select.kamera_wybickiego_anti_flicker`
- `select.kamera_wybickiego_motion_detection_sensitivity`
- `select.kamera_wybickiego_night_vision`
- `select.kamera_wybickiego_record_mode`
- `select.wc_power_on_behavior`
- `sensor.czujnik_zalania_lazienka_bateria`
- `sensor.orange_funbox_3_external_ip`
- `sensor.sm_s928b_car_battery`
- `sensor.sm_s928b_car_charging_status`
- `sensor.sm_s928b_car_ev_connector_type`
- `sensor.sm_s928b_car_fuel`
- `sensor.sm_s928b_car_fuel_type`
- `sensor.sm_s928b_car_name`
- `sensor.sm_s928b_car_odometer`
- `sensor.zigbee_temperature_humidity_sensor_bateria`
- `sensor.zigbee_temperature_humidity_sensor_temperatura`
- `sensor.zigbee_temperature_humidity_sensor_wilgotnosc`
- `switch.kamera_dom_polnoc_socket`
- `switch.kamera_wybickiego_flip`
- `switch.kamera_wybickiego_motion_alarm`
- `switch.kamera_wybickiego_motion_tracking`
- `switch.kamera_wybickiego_privacy_mode`
- `switch.kamera_wybickiego_time_watermark`
- `switch.kamera_wybickiego_video_recording`
- `switch.wc_switch_1`

## WALDING (Dom) — DUPLIKATY TUYA

Walding ma **DWA wpisy Tuya**, oba zaladowane (`01K9JFY85X14BVT8DBR7VG3P04`
i `01KBAFTAMTJ1GH6B1D1CEE4Y2A`). Kazdy ciagnie te same urzadzenia z tego samego konta,
wiec kazde urzadzenie jest **dwa razy** — stad encje z koncowka `_2`.

Przyklad (czujniki zalania — fizycznie sa DWA, encji CZTERY):
- `binary_sensor.czujnik_zalania` — **dziala**
- `binary_sensor.czujnik_zalania_2` — martwy (duplikat)
- `binary_sensor.czujnik_zalania_lazienka` — martwy
- `binary_sensor.czujnik_zalania_lazienka_2` — martwy (duplikat)

**Czujnik zalania w lazience jest niedostepny w OBU instalacjach naraz** — czyli to nie usterka
Home Assistant, tylko **samo urzadzenie milczy**. Bateria albo zasieg.

## DLACZEGO URZADZENIA Z WALDINGU WIDAC NA WYBICKIEGO

**Jedno konto Tuya.** Integracja zaciaga WSZYSTKO, co na nim wisi, niezaleznie od tego,
w ktorym mieszkaniu urzadzenie stoi. Zeby to rozdzielic, trzeba rozdzielic konta
albo domy w aplikacji Tuya. **Tomasz 5.08: zostawiamy jak jest.**

## GDYBY KIEDYS SPRZATAC — KOLEJNOSC

1. **Najpierw w aplikacji Tuya** usunac urzadzenia, ktorych fizycznie nie ma.
2. Potem w HA przeladowac integracje — martwe encje znikna same.
3. **Dopiero na koncu** recznie usuwac to, co zostalo (`ha_remove_entity`).
4. Duplikaty `_2` w Waldingu znikna po usunieciu jednego z dwoch wpisow Tuya —
   **ale najpierw sprawdzic, czy zadna automatyzacja na nich nie wisi.**
