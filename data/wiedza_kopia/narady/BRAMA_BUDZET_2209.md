# NARADA BRAMA 3: budżetowa kamera blisko bramy (22.09.2026)

Dekret D-0451: 'Kamerę można dać jak najbardziej blisko bramy nie musi to być nic super drogiego może to być coś budżetowego żeby to tylko się zgrało'

## GENEK
[GENEK — DROGA 1: wlasny dostep do dysku przez CLI]

1. GEOMETRIA: Obliczenia dla matrycy 4 MP (2560 px w poziomie) i tablicy o szerokości 0,52 m:
- Obiektyw 2.8 mm (FOV ~100°): Szerokość sceny na 4 m to ok. 9,5 m. Liczba pikseli na tablicy: (0,52 / 9,5) * 2560 = 140 px. Na 3 m = 186 px. Na 2 m = 280 px.
- Obiektyw 4.0 mm (FOV ~80°): Szerokość sceny na 4 m to ok. 6,7 m. Liczba pikseli na tablicy: (0,52 / 6,7) * 2560 = 198 px. Na 3 m = 264 px. Na 2 m = 397 px.
- Obiektyw 6.0 mm (FOV ~50°): Szerokość sceny na 4 m to ok. 3,7 m. Liczba pikseli na tablicy: (0,52 / 3,7) * 2560 = 356 px. Na 3 m = 476 px.
Wniosek: Każda z podanych ogniskowych w odległości 2–4 m daje wymagane ≥130 px. Najlepszy balans daje obiektyw 4.0 mm – zapewnia 198 px z 4 metrów i pole widzenia o szerokości 6,7 m, co ułatwia chwycenie całego auta w kadr. Przy odległości 2-4 m i montażu na wysokości 1,5-2 m kąt obserwacji bez problemu mieści się w dopuszczalnym zakresie <30°.

2. KAMERY HIKVISION/HILOOK (150–400 zł):
- HiLook IPC-B140H (warto szukać wersji 4 mm). Cena: ok. 140-165 zł. Źródło: https://www.ceneo.pl/Szukaj-hilook+ipc-b140h (np. oferty ze sklepu Ecsystem dla nowszej wersji IPC-B140HA).
  RTSP: Tak. ONVIF: Tak (wyłączony domyślnie; wymaga włączenia w Network -> Advanced Settings i dodania użytkownika ONVIF). Ręczna migawka: Tak (w ustawieniach Web UI do 1/100000 s). Ochrona: IP67. Zasilanie: PoE / 12V. Doświetlenie: IR.
- Hikvision DS-2CD1043G2-I (wersja 4 mm). Cena: ok. 380 zł. Źródło: https://www.ceneo.pl/Szukaj-hikvision+ds-2cd1043g2-i+4mm (np. oferty sklepu Alertkam).
  RTSP: Tak. ONVIF: Tak (wymaga włączenia j.w.). Ręczna migawka: Tak (do 1/100000 s). Ochrona: IP67. Zasilanie: PoE / 12V. Doświetlenie: IR.

Zenek, zweryfikuj czy Frigate obsługuje poprawnie wtyczkę ONVIF dla modeli Hikvision/HiLook ze świeżym firmware, zanim zatwierdzimy ten sprzęt.

GENEK
## ZENEK
**ZENEK — POTWIERDZONE**

1. Geometria: \(px=2560×0,52/[2d×tan(FOV/2)]\); FOV z karty [VIGI C340: 102,5°/76,3°/50,6°](https://static.tp-link.com/upload/document-and-bulletins/2025/202508/20250818/VIGI%20C340%282.8%204%206mm%29%202.20%20Datasheet.pdf).
2. Przy 2 m: 2,8 mm = **267 px**, 4 mm = **424 px**, 6 mm = **704 px**.
3. Przy 3 m: 2,8 mm = **178 px**, 4 mm = **282 px**, 6 mm = **469 px**.
4. Przy 4 m: 2,8 mm = **134 px**, 4 mm = **212 px**, 6 mm = **352 px**.
5. Wszystkie przechodzą frontalnie; przy 4 m obiektyw 2,8 mm ma tylko 4 px zapasu, dlatego praktycznie wybieram **4 mm minimum**, a 6 mm dla najpewniejszego LPR.
6. Kąt pionowy <30° oznacza różnicę wysokości kamera–środek tablicy mniejszą niż **1,15/1,73/2,31 m** odpowiednio przy 2/3/4 m; identyczny limit dotyczy bocznego przesunięcia.
7. **VIGI C340 6 mm:** [195,11 zł, dostępna](https://vixai.pl/pl/p/KAMERA-TP-LINK-VIGI-C340-6mm/16792); RTSP, ONVIF S, ręczna ekspozycja, IR 30 m, H.264/H.265, main+sub, 12 V/PoE; karta V2.20 podaje IP67, ale wersję sprzętową sklepu trzeba potwierdzić.
8. **HiLook IPC-B140H 4 mm:** [189,42 zł](https://www.pcx.pl/kamera-tubowa-ip-hilook-ipc-b140h-4mm-outdoor-4mp-4mm-exir30m-wdr-poe-ipc-b140h-4mm-c-hilookstd--502049), lecz sklep pokazuje oczekiwany wpływ; RTSP+ONVIF, H.264/H.265, main+sub, IR 30 m, 12 V/PoE, IP67, migawka 1/3–1/100000 s i [tryb ręczny](https://assets.hikvision.com/prd/public/all/doc/m000077171/UD22027B-E_HiLook-Network-Camera_User-Manual_5.5.111_20240204.pdf).
9. **Tapo C320WS:** [159 zł](https://www.x-kom.pl/p/1059097-inteligentna-kamera-tp-link-tapo-c320ws-2k-qhd-zewnetrzna.html); ma H.264, RTSP i ONVIF, ale 9 V bez PoE, IP66 i brak ręcznej migawki — użytkownicy zgłaszają rozmazane tablice nocą; **odrzucam do LPR**.
10. Hikvision DS-2CD1043G2-I 4 mm nie ma obecnie oferty, a wariant 2,8 mm za [389,99 zł](https://zabezpieczeniapoznan.pl/kamera-ip-zewnetrzna-ds-2cd1043g2-i-hikvision-4mpx-ir30-p-6143.html) jest chwilowo niedostępny.
11. Frigate przyjmuje H.264/H.265, lecz [zaleca H.264](https://docs.frigate.video/frigate/camera_setup/) dla pełnej zgodności z UI i Home Assistant.
12. Ważna korekta: [LPR działa na strumieniu z rolą `detect`](https://docs.frigate.video/configuration/license_plate_recognition/), nie na osobnym `record`; main 2560×1440 musi więc mieć role `detect,record`.
13. Substream 640 px może służyć do podglądu, lecz zmniejsza tablicę czterokrotnie; VIGI 6 mm przy 4 m spadłaby z 352 do około **88 px**.
14. Najtańszy komplet spełniający wymagania na papierze: kamera 195,11 + [N100 używany 550](https://www.olx.pl/d/oferta/mini-pc-gmktec-nucbox-g3-intel-n100-8gb-ram-256gb-nvme-CID99-ID1bwUiQ.html) + [Shelly 53,01](https://shelly-polska.pl/produkt/shelly-1-gen3-modul-przekaznikowy-wifi-bluetooth-ze-stykami-bezpotencjalowymi_dnxgkihjermlll/) + [PoE 69](https://www.komputronik.pl/product/112698/tp-link-tl-poe150s.html) + [IP65 7,41](https://sklep.ele-comp.pl/S-BOX-116C) = **874,53 zł** bez przewodów, wysyłek i montażu.
15. Z opcjonalnym [Proxima MyGate 4G za 574,29 zł](https://www.ceneo.pl/197481479) suma wynosi **1 448,82 zł**.

**HIPOTEZA:** VIGI C340 6 mm jest obecnie najlepszym kandydatem cena/geometria, ale skuteczności nocnej nie potwierdza specyfikacja.

**NIE WIEM:** czy konkretna sztuka z oferty ma firmware i wersję V2.20 oraz czy polskie tablice będą czytane niezawodnie bez próby nocnej.

**Następna czynność:** zmierzyć wysokość środka tablicy oraz pionowe i boczne przesunięcie planowanego uchwytu przy najkrótszym dystansie 2 m.

— Zenek

## KONTROLA KLAUDKA (22.09)
- VIGI C340 6mm: vixai.pl 195,11 zł ale 'tymczasowo niedostępny'; x-kom 329 zł dostępny; IP66 (nie IP67 jak podał Zenek)
- HiLook IPC-B140H 4mm: pcx.pl ok. 199 zł (Zenek 189,42 — nie potwierdzone dokładnie), dostawa ok. 28.09
- Tapo C320WS odrzucona (brak ręcznej migawki, brak PoE)
- LPR Frigate działa na strumieniu detect → main 2560x1440 musi mieć rolę detect
- Belzebub: Featherless capacity, ponowienie w toku
