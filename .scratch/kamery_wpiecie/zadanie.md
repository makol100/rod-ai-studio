# ZADANIE DLA ZALOGI: kamery HiLook na zywo w HA Dzialka — jak to wpiac

Dekret Tomasza 13.08 (doslownie):
- "Sprzet jest moj i chuj do tego komus."  -> wolno zmieniac ustawienia kamer i nagrywarki
- "Kamery na zywo maja byc w HA Dzialka, w tej samej co wszystkie okna kamer.
   Strumieniuja jak wejde w to okno to sie maja zaladowac do podgladu na zywo"
- "Jak macie dojscie do nagrywarki wyciagnac zapisy i szukac KUN!"
- "W przyszlosci czujniki ruchu w nocy na kuny i inne zwierzeta zeby powstal taki alert
   a on zostanie sprawdzony czy to kuna a dalej odpali jakas automatyzacje o ktorej pomyslimy
   (lampy powiadomienia alarm cichy albo glosnik z ultradzwiekami"
- "Wszystko robic w grupie !!!!!!"  -> Klaudek ruszyl solo, dostal nagane, wraca do zalogi.

To jest zlecenie KONTROLNE + PROJEKTOWE. Nic nie wykonujecie na sprzecie. Rozstrzyga Tomasz.

## STAN ZMIERZONY (13.08, wszystko ze sladem z tej doby)

Nagrywarka i kamery, siec 192.168.3.0/24, dosiegalne z VPS przez Tailscale.
Poswiadczenia URZADZENIA dzialaja (ISAPI 200 na .110/.111/.112/.114; .113 = 401).

Strumienie z NVR .110 (ffprobe, TCP):
- 101 hevc 1280x720 20 fps | 201 hevc 2560x1440 20 fps | 401 hevc 1280x720 20 fps
- 301 = 404 (kanal "Rog", w apce OFFLINE)
- SUBSTRUMIENIE 102 / 202 / 402: hevc 640x360 8 fps  (302 = 404)
Czyli KARTA KATALOGOWA KLAMALA — substream tez jest H.265, nie H.264.

ISAPI /Streaming/channels/102 odczytane z KAMER (kopie w /root/skrzynka/isapi_backup/):
- 192.168.3.111, .112, .114 — wszystkie identycznie: videoCodecType=H.265,
  640x360, maxFrameRate=800 (8 fps), vbrUpperCap=128 kb/s

go2rtc: dodatek a889bffc_go2rtc 1.9.14, host_network, API 1984 dosiegalne Z VPS
(http://homeassistant-1.tail0109d4.ts.net:1984). Mial 4 strumienie Xiaomi.
KLAUDEK SOLO dodal przez PUT /api/streams trzy wpisy: rod_brama(101), rod_kamera2(201),
rod_kamera4(401) — HTTP 200, widoczne na liscie. To jest do WASZEJ oceny, czy zostaja.

PROBLEM ZMIERZONY: go2rtc /api/frame.jpeg?src=rod_brama zwraca HTTP 200 ale ZERO BAJTOW
dla wszystkich trzech. Klatka JPEG z H.265 nie powstaje bez transkodowania.
Encja camera w HA pokazuje miniature (still image) — bez klatki karta bedzie pusta.

Telefon Tomasza: Samsung Z Fold7, Chrome 151.0.7922.108 (prog HEVC/WebRTC to 136) — zmierzone.

Widok docelowy w HA Dzialka: dashboard "lovelace", views[6], path=kamery, tytul "Kamery",
ikona mdi:cctv, 8 kart typu custom:advanced-camera-card, kazda z jedna kamera
(camera.drzewo_wysoka_rozdzielczosc, camera.fotowoltaika_wysoka_rozdzielczosc,
camera.camera1_niska_rozdzielczosc, camera.garaz_wysoka_rozdzielczosc, camera.security_camera,
camera.kamera_zachod, camera.kamera_domek, camera.kamera_taras).
Nowe kamery maja trafic DO TEGO SAMEGO WIDOKU.

## PYTANIA ROZSTRZYGALNE

P1. MINIATURA. Karta advanced-camera-card i encja camera potrzebuja obrazu.
    Przy H.265 klatka JPEG nie powstaje (zmierzone: 0 bajtow).
    Ktore z tych rozwiazan jest najtansze i najpewniejsze — i dlaczego:
    (a) przestawic substream kamer na H.264 przez ISAPI (sprzet Tomasza, wolno),
    (b) zostawic H.265 i dodac w go2rtc drugi strumien z transkodowaniem ffmpeg do H.264/MJPEG,
    (c) cos innego, co przeoczylismy.
    Podajcie KONKRETNE pola ISAPI do zmiany albo KONKRETNY wpis go2rtc.

P2. USTAWIENIA SUBSTRUMIENIA. Dzis 640x360, 8 fps, 128 kb/s — to malo na podglad.
    Jakie wartosci ustawic, zeby grid dziewieciu kamer (6 dzialajacych obecnie + 3 HiLook; fotowoltaika i garaz sa martwe po zmianie routera - kamery WiFi bez nowych danych sieci, do naprawy na miejscu) nie zabil lacza dzialki
    ani N150, a obraz byl uzyteczny? Podajcie liczby (rozdzielczosc, fps, bitrate)
    i uzasadnienie, nie "srednie".

P3. JAK WPIAC W HA. Encje camera: platforma generic/ffmpeg/go2rtc? Tomasz chce, zeby
    "strumieniowaly jak wejde w to okno" — czyli podglad NA ZYWO po wejsciu w widok,
    nie klikanie w kazda karte. Jak to sie ustawia w advanced-camera-card (live preload /
    lazy load) i czy 11 kamer na zywo naraz to rozsadne. Jesli nie — co proponujecie.

P4. NAGRANIA I KUNY. Tomasz chce wyciagnac z nagrywarki zapisy i szukac kun.
    Jak zdalnie pobrac nagrania z tego NVR (ISAPI ContentMgmt/search + download,
    RTSP playback, cos innego)? Ile tego moze byc, jak dlugo siega archiwum,
    i jak odsiac material do przejrzenia (godziny nocne, kanaly).
    NIE projektujcie jeszcze rozpoznawania kuny — tylko DROGA DO MATERIALU.

P5. RYZYKA (maks 5, kazde z zapobieganiem) + koszt w zlotowkach.
    Uwzglednijcie: zmiana kodeka a nagrywanie NVR, pasmo Tailscale, obciazenie N150,
    watchdog dodatku go2rtc = FALSE, blokada konta HiLook po nieudanych logowaniach.

P6. KOLEJNOSC KROKOW do wykonania, z oznaczeniem [O] odwracalny / [N] nieodwracalny.

## ZASADY
- Kazde twierdzenie ze sladem. Bez sladu = NIE WIEM.
- NIE kopiowac poswiadczen ani URL-i z haslem (dzis haslo dwa razy wyciekło do okna czatu
  Tomasza — raz z pliku, raz z odpowiedzi go2rtc /api/streams?src=).
- Rozbieznosci miedzy wami zostaja widoczne.
- Podpis.
