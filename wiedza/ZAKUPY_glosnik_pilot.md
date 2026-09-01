# LISTA ZAKUPOWA — pilot glosnika ultradzwiekowego na kuny (1 glowica)
Zrodlo: narada n_tanio 29.08.2026 (Henio: zywe API AliExpress, ceny PLN z VAT wg oferty; linki 12/12 = HTTP 200 31.08). Dekret Tomasza 31.08: "Zrob liste co zamowic na aliexpres". ZAKUP KLIKA TOMASZ — Klaudek nie kupuje.
| # | czesc | wariant (UWAGA!) | cena | link |
|---|---|---|---|---|
| 1 | przetworniki 40kHz TCT40-16T | wybrac "10pcs TRANSMITTER (T)" — NIE odbiorniki R | 15,99 zl | https://www.aliexpress.com/item/1005007038725377.html |
| 2 | mostek H DRV8871 | 1 szt (zapas: 2 szt 17,59 zl = 1005010691214345) | 9,29 zl | https://www.aliexpress.com/item/1005006710394258.html |
| 3 | ESP32 DevKit 30-pin | CH340 USB-C — wybrac PLYTKE, nie adapter za 6,69 zl | 15,59 zl | https://www.aliexpress.com/item/1005005692090880.html |
| 4 | zasilacz 24V/60W IP67 | 24V 2,5A (Henio: 230V bez nadzoru → rozwazyc markowy Mean Well z PL) | 62,19 zl | https://www.aliexpress.com/item/1005009313160127.html |
| 5 | obudowa ABS IP65 | 80x110x70 mm (bezpieczniejsza niz 65x95x55 za 28,69) | 35,49 zl | https://www.aliexpress.com/item/1005006370513437.html |
| 6 | przetwornica LM2596 24→5V | cena ze snippetu, nie z API | 6,85 zl | https://www.aliexpress.com/item/1005002059701112.html |
SUMA czesci: 145,40 zl (bez dostaw; Choice: 3,59 zl/oferta lub darmowa od 40 zl).
NIE z Ali: naswietlacz LED 20W 12-24V IP65 — krajowy ~29 zl (Ali 134,99 odrzucony); kabel outdoor, dlawiki, zlacza, bezpiecznik — lokalnie.
Kod: AZ-Delivery/Grzesina (ESP32, wobble/burst) + tor glowicy wg github mcore1976/pest-repellent → przepisac pod ESPHome→HA.

## AKTUALIZACJA 31.08 — decyzja Tomasza: OPCJA 3 (naswietlacz BEZ czujnika + przekaznik sterowany z ESP32)
| 7 | naswietlacz Philips LOIS 20W 2050lm IP65 BEZ czujnika, 220-240V | wariant 5000K (zimny — ostrzejszy w oczy) 29,90 zl w listingu Allegro; strona produktu 3000K (oferta 17231354805) | ~29,90-40,99 zl | https://allegro.pl/produkt/philips-reflektor-zewnetrzny-led-trwaly-ip65-20w-2000lm-czarny-ef22bce0-73b2-431b-851a-ed657f828fbd (3000K) ; 5000K: https://allegro.pl/listing?string=na%C5%9Bwietlacz+led+philips+20w ; alt. leddo.pl 5000K kod 8720169365087 |
| 8 | modul przekaznika 1-kanal, optoizolacja 817c, NATYWNE 3.3V (SRD-03VDC-SL-C) lub 5V low-level trigger, 10A/250VAC | fraza Ali: "1 channel relay module 3.3V optocoupler low level trigger 10A 250V"; konkretny item ID NIEZWERYFIKOWANY (Ali wholesale nie daje ID w wyszukiwarce) — Henio moze dociagnac z API | ~4-6 zl | mechaniczny, NIE SSR (przeciek SSR + zasilacz LED naswietlacza = podswietlony LED) |
Naswietlacz z PIR (Asato 29 zl, oferta 17761089390) — ODRZUCONY (230V + wlasny PIR z rozgrzewka, nie da sie impulsowo sterowac).
SUMA po aktualizacji: ~145,40 (Ali) + ~30-41 (Philips) + ~5 (przekaznik) = ~180-190 zl bez dostaw.
