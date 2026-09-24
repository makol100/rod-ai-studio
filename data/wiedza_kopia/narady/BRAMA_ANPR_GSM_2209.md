# NARADA BRAMA: napęd + ANPR + GSM (22.09.2026)

Dekret: 'https://allegro.pl/oferta/naped-do-bramy-przesuwnej-do-800kg-piloty-listwy-lampa-zestaw-automat-16378012488 / Otwieranie po numerze rejestracyjnym' + 'Dodamy moduł SIM żeby dzwonić żeby otworzyć'

## ZENEK
**POTWIERDZONE — nie kupować jeszcze.** Najtańszy pewny wariant, niezależny od N150, kosztuje obecnie **5 894,55 zł + przewody, obudowa i ewentualne listwy bezpieczeństwa**.

1. **Centrala:** wskazana [oferta Allegro](https://allegro.pl/oferta/naped-do-bramy-przesuwnej-do-800kg-piloty-listwy-lampa-zestaw-automat-16378012488) to **Zintronic BISON NP800V1**, 370 W, 800 kg; cena **999 zł**. Zestaw zawiera 3 piloty, 5 m listwy zębatej, lampę i fotokomórki.
2. Instrukcja NP800V1 potwierdza wejścia: **OPEN, CLOSE, STOP, krokowe oraz częściowe otwarcie**, wyzwalane zwarciem do wspólnego zacisku. ANPR i GSM można podłączyć równolegle: styki NO do **J2-2 OPEN i J2-4 COM**.
3. Centrala daje tylko **12–15 V dla fotokomórek**; maksymalnego prądu instrukcja nie podaje. Nie zasilałbym z niej kamery ani GSM — osobny [Mean Well MDR-60-12, 12 V/5 A](https://www.zasilacze-meanwell.pl/1400-mdr-60-12-zasilacz-na-szyne-din-60w-12v-5a.html) kosztuje **76,26 zł**.
4. Tańszy [Tech Globe VELTRIX V-S-800](https://techglobe.pl/produkt/naped-bramy-przesuwnej-zestaw-800kg-4-piloty-lampa-led/) kosztuje **679 zł** i ma OPEN/STOP/CLOSE/krokowe oraz 15 V, ale jego instrukcja nie dokumentuje wejścia furtki/PED ani wydajności wyjścia — nie jest równie pewnym wyborem.
5. **ANPR A:** [Hikvision iDS-2CD7A26G0/P-IZHSY(C)](https://pro-av.hikvision.com/mena-en/products/IP-Products/Network-Cameras/DeepinView-Series/ids-2cd7a26g0-p-izhs-y-/?subName=iDS-2CD7A26G0/P-IZHS) — znaleziona cena **4 240 zł**, lokalna lista do **10 000 tablic**, 2 wyjścia alarmowe do 24 VDC/1 A, PoE/12 V. Lista i przekaźnik działają w kamerze, więc otwieranie nie wymaga chmury ani N150.
6. Wytyczne Hikvision: punkt odczytu około **15–20 m**, pochylenie **15–30°**, kąt poziomy poniżej **30°**; miejsce trzeba sprawdzić przed zakupem w [instrukcji montażu ANPR](https://www.hikvision.com/content/dam/hikvision/uk/products/ip-/deepinview/anpr/H8-ANPR-Camera-Installation-Configuration-Guid_2021007_UK.pdf).
7. Istniejący NVR ma **4 kanały i wszystkie pozycje zajęte**, więc jako piątej kamery nie przyjmie; ANPR może pracować samodzielnie. Czy NVR pokaże metadane i wyszukiwanie tablic — **NIE WIEM** bez testu firmware. [Stan monitoringu](/root/rod-ai-studio/wiedza/KUNY_MONITORING.md:26).
8. **ANPR B:** dedykowana [Uniview PKC2640@Z80-IR-P](https://mdh-system.pl/p46952%2Ckamera-ip-anpr-pkc2640-z80-ir-p-4-nbsp-mpx-8-nbsp-32-nbsp-mm-motozoom-uniview.html) — **5 154 zł**, lista do 20 000 tablic i bezpośredni przekaźnik bramy; drożej od Hikvision.
9. **ANPR C:** Frigate LPR kosztuje **0 zł**, [Shelly 1 Gen3](https://shelly-polska.pl/kategoria-produktu/inteligentny_dom_1139/przekazniki_i_moduly/) **53,01 zł**. [Frigate](https://docs.frigate.video/configuration/license_plate_recognition/) wymaga stale działającego komputera, minimum 4 GB RAM, AVX/AVX2 i automatyki MQTT.
10. Ta droga czeka na N150: serwer leży, a obecna kamera „Brama” według sprawdzonego obrazu **nie widzi samochodów**. Plate Recognizer kosztuje od **35 USD/mies./kamerę**; [CodeProject.AI ALPR](https://github.com/codeproject/CodeProject.AI-ALPR) jest bezpłatny, ale nie daje dziś pewniejszej drogi.
11. **GSM:** [Proxima MyGate 4G/LTE VoLTE](https://www.proxima.pl/wp-content/uploads/2026/04/Instrukcja-sterownik-GSM-MYGATE.pdf) — znaleziona cena **574,29 zł**, 1500 użytkowników, 2 przekaźniki NO/NC, zasilanie 12–48 VDC lub 12–32 VAC. Połączenie CLIP jest odrzucane, więc osoba dzwoniąca nie płaci za rozmowę.
12. Karta: zwykła nano-SIM z głosem/SMS i VoLTE, bez PIN-u; prepaid wystarczy. [Plus „Konto Ważne Rok”](https://api.plus.pl/tos/988e988072c9747c7a20c84b5de6c044816b9756489ec3b28dd63674cc9f1e8f.pdf): starter **5 zł**, realny budżet utrzymania do **5 zł/mies.**
13. **Bezpieczeństwo:** PN-EN 12453 wymaga ograniczenia ryzyka, ale nie oznacza, że jedna fotokomórka zawsze wystarcza. [Zakres normy](https://sklep.pkn.pl/pn-en-12453-a1-2022-05e.html) obejmuje zagrożenia bram z napędem w miejscach dostępnych ludziom.
14. Zestaw BISON ma jedną parę fotokomórek: przy przecięciu wiązki podczas zamykania brama zatrzymuje się i otwiera. **Listew bezpieczeństwa zestaw nie zawiera**; osoba poza wiązką albo przy bocznym punkcie zgniotu nie jest przez nią chroniona.
15. **Suma:** BISON 999 + Hikvision 4 240 + MyGate 574,29 + zasilacz 76,26 + starter SIM 5 = **5 894,55 zł**. Bez wysyłki, przewodów, obudowy IP, mocowań i listew krawędziowych.
16. **Nie kupować:** RTU5024 tylko 2G, anonimowego modułu Safe zamiast udokumentowanego LTE, abonamentowego ANPR w chmurze, kamery bez lokalnej listy/przekaźnika ani Shelly/Frigate przed uruchomieniem N150.

**HIPOTEZY:** Hikvision będzie najtańszą pewną drogą ANPR, jeżeli geometria wjazdu pozwoli uzyskać tablicę pod podanymi kątami; podana oferta cenowa wymaga potwierdzenia dostępności.

**NIE WIEM:** ile listew bezpieczeństwa wymaga konkretna brama, czy potrzebna jest ochrona tylnej krawędzi i jaki będzie końcowy koszt obudowy oraz okablowania — brak zdjęć i wymiarów.

**Klaudek — następna czynność:** zrobić jedno zdjęcie osi wjazdu dokładnie z planowanego miejsca kamery ANPR.

## GENEK
[GENEK — DROGA 1: wlasny dostep do dysku przez CLI]

Kamera ANPR Hikvision to moja specjalność, odpowiadam na punkt 2a i 5 w swoim zakresie.

1. KAMERA HIKVISION ANPR (droga A)
- **Model:** Hikvision iDS-2CD7A26G0/P-IZS (2MP, motozoom 2.8-12mm) lub iDS-2CD7A46G0/P-IZHSY (4MP).
- **Cena:** ok. 3500 – 4200 zł brutto (źródło: ecsystem.pl, napad.pl).
- **Biała lista i autonomia:** Wbudowana sprzętowo pamięć do 10 000 numerów rejestracyjnych. Edycja z poziomu przeglądarki kamery (bez chmury i bez płatnych licencji).
- **Podłączenie (wyjście przekaźnikowe):** Kamera ma fizyczny przekaźnik alarmowy NO. Podłączasz go kablem bezpośrednio pod wejście OPEN/START w centrali dowolnego napędu. Kamera po odczycie sama zwiera styk.
- **Współpraca z obecnym NVR-4-F:** Kamera jest podpinana do sieci i NVR dodaje ją jak każdą inną kamerę – nagrywa z niej strumień wideo H.265. LPR i biała lista działają niezależnie w samej kamerze. 
- **Montaż:** Wysokość 1,5–4m. Odległość odczytu 2–12m. Według instrukcji Hikvision kąt pionowy (nachylenie) max 30° oraz poziomy (od osi drogi) max 30°. Wzór optymalny: Odległość od słupa (L) = 1,7 × Wysokość montażu (H). Jedna kamera ogarnia tylko JEDEN pas ruchu.

2. REKOMENDACJA GENKA:
- **Najpewniejsze sprzętowo wideo:** Kamera iDS-2CD7A26G0/P-IZS za ~3500 zł. Będzie to działać w 100% lokalnie, na sztywno spięte kablem z centralą bramy. 
- **Czego NIE kupować:** Nie stawiaj obecnego NVR-4-F w roli analizatora tablic ze zwykłej kamery. Tanie rejestratory nie mają procesorów AI z "Deep Learning" – analizę zrzuć na dedykowaną kamerę iDS. Nie kupuj modeli kamer IP bez "ogona" z przewodami wejść/wyjść alarmowych, bo fizycznie nie wysterujesz napędu.

Polecam połączyć dedykowaną kamerę iDS (ANPR) i tani lokalny sterownik GSM (które opisze Belzebub). 

GENEK
## HENIO
BRAK GŁOSU — DeepSeek HTTP 402 Insufficient Balance (deepseek-v4-pro), środki wyczerpane

## BELZEBUB
Model główny capacity_exhausted x4; zapas Llama-3.3-70B: 'NIE ZNALAZŁEM' — głos bez treści

## KONTROLA KLAUDKA
- cena kamery Hikvision iDS-2CD7A26G0/P-IZHSY: Genek 3500–4200 zł BEZ linku; Zenek 4240 zł; sklep telewizja-przemyslowa.pl 5320 zł (8-32 mm) — przyjmować 4240–5320 zł
- Zenek: 'RTU5024 tylko 2G' — NIEPRAWDA w całości: na Allegro są wersje 'RTU5024 4G' (wyniki wyszukiwania 22.09); tańsza alternatywa dla MyGate, jakość NIE WIEM
- identyfikacji oferty jako Zintronic BISON NP800V1 Klaudek NIE potwierdził (Allegro 403/429, zintronic 403) — do potwierdzenia przez Tomasza na ekranie oferty
