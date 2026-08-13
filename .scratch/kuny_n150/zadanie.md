# ZADANIE DLA ZALOGI: mielenie nagran POD KUNY na N150 (zaktualizowany stan)

Uwaga: poprzednie zadanie .scratch/kuny_nagrania/ dostaliscie ZANIM Tomasz wydal dekret
o mieleniu na miejscu. Wasze odpowiedzi liczyly pobieranie NA VPS. Ten brief to poprawia.

## DEKRETY TOMASZA (13.08, doslownie)
- "Na N150 tam to przemielic i wyslac na vps" — analiza LOKALNIE, na VPS ida tylko kandydaci.
- "Nazywa sie N150 i chuj!!!!" — maszyna Dzialki nazywa sie N150. Koniec tematu nazwy.
- "Slady kuny sa na dachu auta zawsze wiec musi lazic po autach" — wiedza z terenu.
- "Nie kablach a autach" — ROI to AUTA (numer jeden), dachy, ogrodzenia. NIE kable.
- "Wszystko robic w grupie !!!!!!" — Klaudek nie decyduje sam.

## CO SIE ZMIENILO OD WASZYCH ODPOWIEDZI (wszystko zmierzone dzis)

1. ROZSTRZYGNIETY KROK 1 ZENKA (Tomasz zgodzil sie, wykonany): dwa identyczne zapytania
   ContentMgmt/search na kanal 1, godzina 2026-08-12 01:00-02:00, jedyna roznica to
   obecnosc metadataDescriptor. WYNIK IDENTYCZNY W OBU: status OK, po 2 trafienia,
   te same przedzialy 00:47:01->01:44:48 i 01:44:48->02:51:18, dlugosci 3467 s i 3990 s,
   typ w kazdym wyniku 'recordType.meta.hikvision.com/timing'.
   WNIOSEK: NVR IGNORUJE filtr po ruchu i zwraca SEGMENTY NAGRANIA CIAGLEGO.
   Moje wczesniejsze "178 zdarzen nocnych" to byly kawalki nagrania ciaglego, NIE detekcje.
   Zenek mial racje kazac to zmierzyc.

2. PARAMETRY N150 (pierwszy pomiar w historii tej maszyny, ssh, cpuinfo/DMI):
   Intel Core i3-6006U 2.00GHz, 4 watki, 8 GB RAM, SSD 512 GB (416 GB WOLNEGO),
   plyta INTEL SKYBAY, HAOS 18.2, HA 2026.8.1, sprzet fizyczny (brak flagi hypervisor),
   /dev/dri/renderD128 obecne. UWAGA: Henio liczyl wczesniej wydajnosc "dla N100/N150" —
   to byl zly procesor. Liczcie jak dwurdzeniowego Skylake'a z 2015 roku.
   Ta sama maszyna obsluguje MariaDB, Zigbee2MQTT, ESPHome, Music Assistant, go2rtc (7 strumieni).

3. FFMPEG ZAINSTALOWANY NA N150 (zrobil Klaudek na polecenie Tomasza "Rob"):
   przez opcje `packages` dodatku Advanced SSH + restart dodatku. ZMIERZONE po restarcie:
   ffmpeg 8.1.2 i ffprobe obecne; dekodery hevc i h264 obecne, w tym h264_qsv;
   hwaccels: vdpau vaapi qsv drm vulkan; python3 w wersji 3.14.5.
   TEGO KROKU NIE WIDZIELISCIE. Jesli uwazacie, ze byl zly albo niepotrzebny — piszcie wprost.

4. KTORE KAMERY WIDZA AUTA (Genek obejrzal po klatce z kazdego kanalu, ISAPI /picture):
   - kanal 1 "Kamera brama": BRAK AUT (brama, plot, droga, drzewa, linie energetyczne)
   - kanal 2 "KAMERA 2": DWA AUTA, dachy widoczne, nad nimi OTWARTA PRZESTRZEN
   - kanal 4 "Kamera4": AUTA (kilka), dachy widoczne, NAD NIMI DRZEWA/KRZEWY; tez wiata,
     taczka, napis "Smietnik"
   Priorytet ustalony: kanal 4 pierwszy (drzewa nad autami = droga zejscia kuny na dach),
   kanal 2 drugi, kanal 1 odpada, kanal 3 martwy.

5. ARCHIWUM: kanal 1 i 4 od 23.07, kanal 2 od 4.08. Zapis ciagly, H.264 (nagrania),
   3072 kbps -> doba na kanal ok. 33 GB. Playback po czasie: rtsp://.../Streaming/tracks/<track>/?starttime=&endtime=

## PYTANIA ROZSTRZYGALNE

P1. PLAN MIELENIA NA N150. Napiszcie KONKRETNY przebieg dla JEDNEJ nocy z kanalu 4:
    czym czytac (ffmpeg z RTSP playback po czasie?), jak wykrywac ruch (filtr ffmpeg
    'select gt(scene,...)' czy wlasny python na roznicy klatek?), jak zapisywac kandydatow.
    Podajcie GOTOWE polecenie, nie opis.

P2. ILE TO POTRWA na tej maszynie i ile zabierze CPU. 8 godzin nocy, jeden kanal, 720p H.264.
    Czy uzywac QSV/VAAPI do dekodowania, zeby nie zjesc CPU potrzebnego HA?
    Czy da sie to ograniczyc (nice/cpulimit/-threads), zeby HA nie ucierpial? Liczby.

P3. ODSIEW POD KUNE. Kuna: mala, szybka, NOCNA, wchodzi NA DACH AUTA (wiedza Tomasza).
    Jak ustawic detekcje, zeby odrzucic: deszcz, przelaczenie na podczerwien, zmiane swiatla,
    owada/pajeczyne przy obiektywie, kolysanie galezi — a zlapac maly obiekt na/nad dachem auta.
    Czy warto ograniczyc obszar analizy do prostokata wokol aut (ROI) i jak go wyznaczyc
    bez recznego klikania.

P4. CO WYSYLAC NA VPS. Format, dlugosc, ile sztuk na noc. Ile to megabajtow.
    Jak przeslac z N150 na VPS (scp po Tailscale? katalog /share + rsync?).

P5. RYZYKA (maks 5, kazde z zapobieganiem) + koszt w zlotowkach.
    Uwzglednijcie: N150 obsluguje cala Dzialke; dysk 416 GB wolnego; lacze dzialki;
    to, ze ffmpeg zostal doinstalowany do dodatku SSH (przezyje restart dodatku, ale
    czy przezyje aktualizacje HAOS? — jesli nie wiecie, napiszcie NIE WIEM).

P6. KOLEJNOSC KROKOW, [O] odwracalny / [N] nieodwracalny. Pierwszy krok najtanszy.

## ZASADY
- Kazde twierdzenie ze sladem. Bez sladu = NIE WIEM.
- NIE kopiowac poswiadczen ani URL-i z haslem.
- Rozbieznosci zostaja widoczne.
- Podpis.
