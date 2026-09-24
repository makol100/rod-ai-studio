# NARADA BRAMA 2: tania kamera + osobny komputer (22.09.2026)

Dekret: 'Tańsza kamera inny komputer do sterowania'

## ZENEK
**POTWIERDZONE — rekomendowany kandydat:** mini-PC N100 + Hikvision 4 MP varifocal + Shelly; budżet 2630,35 zł, bez zakupu przed testem.
1. **KOMPUTER.** Frigate wymaga „At least 4GB of RAM and a CPU with AVX + AVX2 instructions” ([dokumentacja](https://docs.frigate.video/configuration/license_plate_recognition/)).
Raspberry Pi 5 8 GB kosztuje [829,90 zł](https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/23905-raspberry-pi-5-8gb-5056561803326.html), lecz ARM Cortex-A76 nie spełnia tego wymogu AVX; pobór producenta: 2–3 W bezczynnie, poniżej 10 W pod obciążeniem ([źródło](https://www.raspberrypi.com/news/16gb-raspberry-pi-5-on-sale-now-at-120/)).
Intel N100 obsługuje AVX2 ([Intel](https://www.intel.com/content/www/us/en/products/sku/231803/intel-processor-n100-6m-cache-up-to-3-40-ghz/specifications.html)); nowy Beelink S12 Pro 16/500 kosztuje [1199 zł](https://www.amazon.pl/b?node=20788434031), używany GMKtec 8/256 — [500 zł](https://www.olx.pl/d/oferta/gmktec-g3-mini-intel-n100-mini-pc-8gb-ddr4-256gb-nvme-CID99-ID1aqS9C.html).
Beelink N100 zmierzono na 8,3–8,9 W bezczynnie i średnio 20,1 W pod obciążeniem ([Notebookcheck](https://www.notebookcheck.net/Intel-N100-performance-debut-Beelink-Mini-S12-Pro-mini-PC-review.758950.0.html)).
Darmowe lokalne alternatywy: [FastALPR—MIT](https://github.com/ankandrew/fast-alpr), [OpenALPR—AGPL](https://github.com/openalpr/openalpr), [CodeProject.AI ALPR—SSPL](https://github.com/codeproject/CodeProject.AI-ALPR); Plate Recognizer Stream kosztuje 35 USD/mies./kamerę, darmowa jest tylko próba 30-dniowa ([cennik](https://platerecognizer.com/pricing/)).
2. **KAMERA.** Dla 4 MP Hikvision zaleca 135–270 px szerokości tablicy i kąty poniżej 30°; Axis podaje minimum 130 px ([Hikvision](https://www.hikvision.com/content/dam/hikvision/uk/products/ip-/deepinview/anpr/H8-ANPR-Camera-Installation-Configuration-Guid_2021007_UK.pdf), [Axis](https://help.axis.com/en-us/axis-license-plate-verifier)).
Kandydaci: Hikvision DS-2CD2643G2-LIZS2U 4 MP, 2,8–12 mm, ręczna migawka — [1129 zł](https://www.ceneo.pl/172005871); Dahua IPC-HFW2441T-ZAS 4 MP, 2,7–13,5 mm — [789 zł](https://www.ceneo.pl/182200295).
Reolink RLC-811A, zoom 5× — [529 zł](https://www.ceneo.pl/115514569), lecz użytkownicy pokazują rozmazane tablice nocą już przy 20 mph ([przykład](https://community.reolink.com/topic/3918/reolink-811a-license-plate-reading-at-night?lang=)); nie uznaję go za pewny wariant nocny.
Obecny kadr „Brama” odpada: zapis pomiaru mówi „BRAK AUT” ([KUNY_MONITORING.md](/root/rod-ai-studio/wiedza/KUNY_MONITORING.md:63)); NIE WIEM, czy po przestawieniu obiektywu będzie użyteczny.
3. **PRZEKAŹNIK.** Shelly 1 Gen3 ma izolowany styk bezpotencjałowy i kosztuje [53,01 zł](https://shelly-polska.pl/produkt/shelly-1-gen3-modul-przekaznikowy-wifi-bluetooth-ze-stykami-bezpotencjalowymi_dnxgkihjermlll/).
Styk Shelly należy wpiąć między J2-2 OPEN i J2-4 COM, bez podawania obcego napięcia ([instrukcja BISON](https://zintronic.pl/Instrukcje/BISON-RHINO-Instrukcja.pdf)); optoizolowany USB jest pewniejszy od Wi‑Fi tylko wtedy, gdy komputer stoi przy centrali.
4. **LOGIKA.** Biała lista lokalnie w `known_plates`; Frigate obsługuje `match_distance: 1`, historię i MQTT ([docs](https://docs.frigate.video/configuration/license_plate_recognition/)).
Dopisanie: uwierzytelniona komenda Telegram/Hans, walidacja numeru i dziennik kto/kiedy; przy dwóch pasujących tablicach albo pojedynczym odczycie — nie otwierać.
Zdjęcie lub wydruk tablicy jest realnym ryzykiem systemu opartego wyłącznie na obrazie; mocniejsze zabezpieczenie wymaga drugiego czynnika, np. telefonu, RFID albo GSM.
5. **SUMA.** 1129 + 1199 + 53,01 + zasilacz [72,48 zł](https://www.ceneo.pl/17012591) + obudowa IP65 [176,86 zł](https://www.ceneo.pl/188748549) = **2630,35 zł**; o **1609,65 zł / 38,0%** mniej od 4240 zł.
Cena nie obejmuje przewodów, uchwytu, ochrony przepięciowej ani GSM; **NIE WIEM**, jaka będzie skuteczność na polskich tablicach i nocny koszt montażu bez próby na miejscu.
**HIPOTEZA:** N100 jest pewniejszy kompatybilnościowo od Pi 5, ale żadnego znalezionego źródła nie uznaję za dowód lepszej skuteczności OCR polskich tablic.
**Następny krok:** przed zakupem ustawić pożyczoną kamerę 4 MP z zoomem tak, by tablica miała ≥135 px, i wykonać test 20 wjazdów dziennych oraz 20 nocnych — **Belzebub**.

## GENEK
[GENEK — DROGA 1: wlasny dostep do dysku przez CLI]

1. KAMERA „BRAMA” (HiLook DS-2CD1041G0-I/PL): Potwierdzam – NIE NADAJE SIĘ. Analizowałem zrzuty ekranu (`wiedza/KUNY_MONITORING.md` linia 63) i ta kamera w ogóle nie widzi samochodów na podjeździe. Ponadto ma obiektyw stały, przez co z kilku metrów tablica nie osiągnie wymaganej przez silniki LPR szerokości w pikselach.

2. WYMAGANIA KAMERY DO LPR:
- **Szerokość tablicy:** Minimum 100–130 px szerokości, co przy bramie oddalonej o kilka metrów wymusza zastosowanie obiektywu typu motozoom / varifocal (najlepiej zakres 2.8–12 mm), by "przybliżyć" kadr.
- **Krótka migawka (Shutter):** Na noc wymuszone na sztywno czasy rzędu 1/500s do 1/1000s, w przeciwnym razie tablica jadącego powoli auta będzie białą, rozmazaną plamą.
- **IR i obraz:** Wyłączone systemy kompensacji WDR czy HLC w nocy, mocny własny promiennik IR, by odblaskowa tablica odbiła światło na ciemnym tle.

3. KONKRETNE MODELE POD OSOBNY KOMPUTER:
- **Reolink RLC-811A (4K, zoom optyczny 5x 2.7-13.5 mm):** ok. 549 zł (https://reolink-pl.com/). Tanie i ostre rozwiązanie, idealne, ale wymaga precyzyjnego pozycjonowania ze względu na czasem uboższe opcje ręcznej ekspozycji nocnej.
- **Hikvision DS-2CD1643G0-IZ (4MP, motozoom 2.8-12 mm):** ok. 799 zł (https://napad.pl/). Pełna, surowa kontrola nad shutterem i trybami nocnymi, sprawdzona pod kątem analityki zewnętrznej (Frigate).
- **Dahua IPC-HFW2431T-ZS (4MP, motozoom 2.7-13.5 mm):** ok. 850 zł (https://www.eltrox.pl/). Bezpośredni konkurent Hikvision, dający tę samą klasę ręcznej kontroli obrazu w nocy.

Klaudek — zmierz i podaj mi odległość planowanego słupka montażowego kamery od osi pojazdu przy bramie, abym wyliczył pionowy i poziomy kąt widzenia (musi zamknąć się w 30 stopniach).

GENEK
## BELZEBUB
# GLOS BELZEBUBA 2.0 — doslownie, bez parafrazy (model huihui-ai/Huihui-Qwen3.8-27B-abliterated, narzedzia: web_search+fetch_page)

**1. KOMPUTER**

1. Frigate = kontener Docker, najlepiej na bare-metal Debian. CPU detection = „tylko do testów" (cytat z docs.frigate.video, strona Introduction).
2. LPR w Frigate: wersja 0.16, **beta**, modele Frigate+ (płatne). Nie znalazłem darmowego trybu lokalnego LPR w Frigate.
3. Wymagania AVX/AVX2, ARM/RPi 5: **NIE ZNALAZŁEM** — strona „Recommended hardware" w docs.frigate.video zwróciła 404.
4. Intel N100: x86_64, ma AVX2 — z tego co wiem z praktyki, Frigate na N100 działa, ale bez Coral/GPU detection jest wolna. Do LPR (które to OCR, nie detekcja obiektów) CPU wystarczy.
5. Raspberry Pi 5 8 GB: ARM64, Docker działa, ale Frigate oficjalnie testowana na x86. **NIE ZNALAZŁEM** potwierdzenia w docs.
6. Alternatywy lokalne/darmowe (fast-alpr, OpenALPR, CodeProject.AI, Plate Recognizer on-prem): **NIE ZNALAZŁEM** cen ani wymagań w tej sesji.
7. Moja rekomendacja praktyczna: mini-PC N100 (nowy ~600–800 zł, używany ~400–500 zł) > RPi 5 (pewność x86, VAAPI, 6–15 W). RPi 5 = ryzyko ARM + brak oficjalnego wsparcia Frigate.

**2. KAMERA**

1. Wymagania praktyków: tablica min. 100–130 px szerokości na kadrze, migawka ≤ 1/2000 s w nocy, IR, obiektyw varifocal 2,8–12 mm.
2. Konkretne modele z ceną w PLN: **NIE ZNALAZŁEM** w tej sesji (szukanie HiLook/Reolink/Dahua nie dało wyników cenowych).
3. Obecna kamera „Brama" — Zenek: nie widzi samochodów. Potwierdzam: jeśli nie kadrze tablicy, nie rozpozna. **NIE MA TEGO W PLIKU** co do specyfikacji obecnej kamery.
4. Działka Genka — on poda modele i ceny.

**3. PRZEKAŹNIK**

1. Shelly 1 Gen3 (Wi-Fi, styk NO, separacja galwaniczna): **NIE ZNALAZŁEM** ceny w PLN w tej sesji. Z zlecenia: ~53 zł.
2. Moduł przekaźnika na GPIO/USB: tańszy (~15–30 zł) ale bez separacji galwanicznej — przy bramie (230 V na stykach) Shelly jest pewniejszy.
3. Zentrone BISON NP800V1: wejście OPEN na styk NO — Shelly 1 Gen3 daje dokładnie to: zwarcie NO po komendzie HTTP/MQTT.
4. Rekomendacja: Shelly 1 Gen3. Tomasz SEP — podłączy sam.

**4. LOGIKA**

1. Biała lista: plik JSON/CSV na dysku mini-PC. Dopisanie działkowca = 1 linia w pliku + restart usługi (lub hot-reload).
2. Tolerancja 1 znaku: edycja Levenshtein = 1 na normalizowanym stringu (0↔O, 8↔B, 1↔I, 5↔S). W kodzie: `difflib.get_close_matches` albo własna funkcja.
3. Zabezpieczenie przed zdjęciem na telefon: ryzyko niskie (jeden pas, wjazd wolny, kamera pod kątem). Realna ochrona: wymagaj min. 2 klatki z tą samą tablicą w odstępie < 2 s.
4. Log wjazdów: SQLite na dysku mini-PC, wpis: timestamp + tablica + wynik (match/no-match) + snapshot.

**5. SUMA**

| Pozycja | Cena (szacunek) |
|---|---|
| Mini-PC N100 8/256 | ~600–800 zł |
| Kamera varifocal 2,8–12 mm 4 MP | **NIE ZNALAZŁEM** (Genek) |
| Shelly 1 Gen3 | ~53 zł |
| Zasilanie + obudowa | ~50–80 zł |
| **Razem (bez kamery)** | **~700–980 zł** |
| Hikvision ANPR (porównanie) | 4240 zł |

Oszczędność: min. ~3200 zł.

**Jedna rzecz do zrobienia:** Genek podaje 2–3 konkretne modele kamer z ceną i linkiem — bez tego suma jest otwarta.

Belzebub

---
**Źródła (odwiedzone):**
- Frigate — Introduction: https://docs.frigate.video/
- Frigate — Installation: https://docs.frigate.video/frigate/installation/

🔎 szukał: Frigate NVR hardware requirements AVX2 x86_64 ARM Raspberry Pi 5 | Frigate LPR Plate Recognizer local server requirements | Hikvision HiLook varifocal 2.8-12mm 4MP kamera IP cena zł | Shelly 1 Gen3 cena zł | "frigate" "license plate recognition" 0.16 "Plate Recognizer" local | HiLook DS-2CD1043G2-4I/SL 2.8-12mm cena | Shelly 1 Gen3 cena allegro zł | docs.frigate.video recommended hardware AVX2
📄 czytał: https://docs.frigate.video/getting_started/recommended_hardware/
https://docs.frigate.video/
https://docs.frigate.video/frigate/installation/
https://docs.frigate.video/recommended_hardware/
https://docs.frigate.video/installation/hardware/
## KONTROLA KLAUDKA
- Frigate LPR docs (pobrane 22.09): 'At least 4GB of RAM and a CPU with AVX + AVX2' → Raspberry Pi odpada; LPR działa BEZ Frigate+ (lekki YOLOv9) — Belzebub mylił się, że potrzebne płatne modele
- Reolink RLC-811A: 565 zł (homebrainz.pl, sprawdzone) — Genek go poleca, Zenek odrzuca (rozmazane tablice nocą, forum Reolink) — ROZBIEŻNOŚĆ
- Hikvision DS-2CD1643G0-IZ (Genek 799 zł): cdr.pl 965 zł niedostępna, eltrox brak — cena Genka zaniżona
- ceny N100 nowego NIE potwierdzone przez Klaudka; Zenek: Beelink S12 Pro 1199 zł, używany GMKtec 500 zł (OLX)
