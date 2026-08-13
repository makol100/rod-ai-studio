# KUNY — MONITORING I PRZESZUKIWANIE NAGRAN (kanon)

Powstal 13.08.2026 na polecenie Tomasza: "Zapisac wszedzie. Sprawdzic czy sie zapisalo!!!!"
Zrodlo faktow: pomiary z 13.08 (ISAPI, ffprobe, ssh na N150) + glosy Zenka i Henia.
Kazda liczba tutaj pochodzi z pomiaru, nie z dokumentacji producenta.

## 1. DEKRETY TOMASZA (jego slowo przebija wszystko ponizej)

- "Sprzet jest moj i chuj do tego komus" — wolno zmieniac ustawienia kamer i NVR.
- "Kamery na zywo maja byc w HA Dzialka, w tej samej co wszystkie okna kamer.
  Strumieniuja jak wejde w to okno to sie maja zaladowac do podgladu na zywo"
- "Jak macie dojscie do nagrywarki wyciagnac zapisy i szukac KUN!"
- "Slady kuny sa na dachu auta zawsze wiec musi lazic po autach" — wiedza z terenu.
- "Nie kablach a autach" — ROI to AUTA, nie kable.
- "Na N150 tam to przemielic i wyslac na vps" — analiza lokalna, na VPS tylko kandydaci.
- "Mialo byc obrobione na n150 potem do Gienka" — Genek NIE dostaje surowego materialu.
- "Kiedys dojdziemy do ostatniej nocy" + "Potem na biezaco" — nadrobic wstecz, potem automat.
- "Nazywa sie N150 i chuj!!!!" — maszyna Dzialki nazywa sie N150.
- "Wszystko robic w grupie !!!!!!" — Klaudek nie decyduje sam.
- W PRZYSZLOSCI (cytat): "czujniki ruchu w nocy na kuny i inne zwierzeta zeby powstal taki
  alert a on zostanie sprawdzony czy to kuna a dalej odpali jakas automatyzacje o ktorej
  pomyslimy (lampy powiadomienia alarm cichy albo glosnik z ultradzwiekami"

## 2. SPRZET — STAN ZMIERZONY 13.08

NVR 192.168.3.110: NVR-4CH-5MP, firmware V4.76.010, dysk ok. 930 GB.
Poswiadczenia URZADZENIA (inne niz konto Hik-Connect z aplikacji) leza w /root/.sekrety
na VPS i w /share/kuny/cred/nvr.env na N150 (600). NIGDY nie drukowac.

Kanaly (ISAPI /System/deviceInfo, wszystkie HTTP 200):
- .111 "Kamera brama"  = kanal 1 / track 101
- .112 "KAMERA 2"      = kanal 2 / track 201
- .113                 = HTTP 401 (inne haslo albo martwe) — ZAKAZ prob logowania
- .114 "Kamera4"       = kanal 4 / track 401
Kanal 3 ("Rog") MARTWY: RTSP 404, rozdzielczosc 0x0, w apce OFFLINE.

Strumienie na zywo: WSZYSTKIE H.265.
- main 101: 1280x720 20 fps | 201: 2560x1440 20 fps | 401: 1280x720 20 fps
- sub 102/202/402: 640x360, 8 fps, vbrUpperCap 128 kb/s
NAGRANIA na NVR sa w H.264 (track description), nominalnie 3072 kb/s.

N150 (serwer HA Dzialka, homeassistant-1, 192.168.0.250 / Tailscale 100.115.112.5):
Intel i3-6006U 2.0 GHz, 4 watki, 8 GB RAM, SSD 512 GB (416 GB wolnego), HAOS 18.2,
HA 2026.8.1, /dev/dri/renderD128 obecne, sprzet fizyczny. Widzi NVR (ISAPI 401 w 9,5 ms).
ffmpeg 8.1.2 + ffprobe DOINSTALOWANE 13.08 przez opcje `packages` dodatku Advanced SSH
(przezylo restart dodatku; czy przezyje aktualizacje HAOS — NIE WIEM).
Dostep z VPS: ssh root@homeassistant-1.tail0109d4.ts.net (klucz "rod-ai-studio").

## 3. CO JUZ USTALONE — I CO SIE OKAZALO NIEPRAWDA

- NVR **IGNORUJE** filtr po ruchu. Pomiar 13.08: dwa identyczne zapytania
  ContentMgmt/search (kanal 1, 2026-08-12 01:00-02:00), jedyna roznica to metadataDescriptor
  -> WYNIK IDENTYCZNY: 2 trafienia, te same przedzialy, typ 'recordType.meta.hikvision.com/timing'.
  Wczesniejsze "129/191/112 zdarzen ruchu, w tym 178 nocnych" to byly SEGMENTY nagrania
  ciaglego, NIE detekcje. Zenek slusznie kazal to zmierzyc.
- go2rtc NIE zrobi klatki JPEG z H.265 (frame.jpeg = 0 bajtow), ale KAMERA zrobi:
  ISAPI /Streaming/channels/<kanal>/picture zwraca JPEG (zmierzone 82-173 KB). To znalazl Henio.
- Karta katalogowa DS-2CD1041G0-I/PL mowi, ze substream jest H.264 — NIEPRAWDA dla tych
  egzemplarzy: zmierzone H.265. Dokumentacja opisuje mozliwosci, nie ustawienie.

## 4. KTORE KAMERY WIDZA AUTA (Genek, oglad klatek dziennych 13.08)

- kanal 1 "Kamera brama": BRAK AUT (brama, plot, droga, drzewa, linie energetyczne) — ODPADA
- kanal 2 "KAMERA 2": dwa auta, dachy widoczne, nad nimi OTWARTA PRZESTRZEN — drugi w kolejce
- kanal 4 "Kamera4": kilka aut, dachy widoczne, NAD NIMI DRZEWA/KRZEWY; tez wiata, taczka,
  napis "Smietnik" — PIERWSZY, bo drzewa nad autami to gotowa droga zejscia kuny na dach

## 5. ROI — OBSZAR SZUKANIA (kanal 4)

Wyznaczony przez Genka z JEDNEJ dziennej klatki, bez recznego klikania Tomasza.
- na klatce ISAPI 704x576: X=418 Y=30 W=286 H=195 (wszystkie zaparkowane auta z dachami
  i pasem ok. 30 px nad dachami)
- przeliczone na nagranie 1280x720: **crop=520:244:760:38**, czyli 13,8% kadru
Reszta kadru NIE jest wyrzucana — sluzy do wykrywania zmian GLOBALNYCH (podczerwien,
swiatlo, deszcz), ktore maja byc odrzucane.
UWAGA: w tym prostokacie na klatce dziennej byla tez osoba przy aucie. Nocne trafienia
z ludzmi tez wejda do kandydatow — odsiew ich nie odrzuci.

## 6. DROGA, KTORA WYBRAL TOMASZ

1. POBRAC noc na dysk N150 (droga Zenka: bezpieczniej, bo przy zerwaniu polaczenia
   nie trzeba czytac NVR od nowa). Skrypt: /share/kuny/pobierz_noc.sh NOC TRACK START KONIEC
   Poswiadczenia z pliku, nie z palca. Czasy w URL sa w formacie ...Z.
2. MIELIC na N150 (ROI z pkt. 5, odrzucanie zmian globalnych, filtr rozmiaru plamy i toru ruchu).
3. Surowa noc KASOWANA po przemieleniu — na dysku nigdy wiecej niz jedna noc.
4. Na VPS ida TYLKO kandydaci (30 s, ok. 11,5 MB kazdy), rsync po Tailscale z --bwlimit.
5. Genek oglada TYLKO kandydatow. Najpierw 10 kalibracyjnych, potem reszta.

## 7. SKALA I TERMIN

- kanal 4: 20 nocy do nadrobienia (archiwum od 23.07; pierwsza PELNA noc to 24/25.07)
- kanal 2: 9 nocy (archiwum od 4.08)
- razem 29 nocy, ok. 96 GB przeplywu — LOKALNIE, nie przez lacze Tomasza
- **RETENCJA NVR 30 DNI: najstarsze noce znikaja ok. 22-23.08.2026**. Po tej dacie
  nadrabianie wstecz nie ma sensu, bo materialu juz nie bedzie.
- POTEM TRYB BIEZACY: kazda kolejna noc mielona automatycznie, bez proszenia.

## 8. POMIAR PIERWSZEGO POBIERANIA (noc 24/25.07, kanal 4, 13.08 ~14:1x-14:2x)

- tempo ok. 908 kb/s (~6,9 MB/min) -> osiem godzin nocy to ok. 3,3 GB, nie 11 GB
- ffmpeg zjada 0,6-0,9% CPU, obciazenie maszyny bez zmian (load ok. 1,0), HA nietkniete
- w logu ostrzezenia o znacznikach czasu (Non-monotonic DTS) — normalne przy kopiowaniu
  z odtwarzania archiwum; jesli czasy sie rozjada, wycinki liczyc od poczatku pliku

## 9. CZEGO NIE WIEMY (wprost, zeby nikt nie zgadywal)

- czy ffmpeg na N150 przezyje aktualizacje HAOS
- jakie jest rzeczywiste pasmo wysylania lacza Dzialki
- czy NVR pozwoli czytac archiwum szybciej niz 1x realtime
- limit rownoczesnych sesji RTSP na NVR i na kamerach
- przyczyna 401 na .113 (inne haslo, blokada czy uszkodzenie)
- ile trafien przejdzie odsiew i ile z nich pokaze kune

## 10. ZAKAZY

- ZERO prob logowania do .113 (HiLook blokuje konto po 5 nieudanych na 30 min;
  13.08 zrobiono juz ok. 15 prob).
- ZERO drukowania hasel w oknie czatu — 13.08 haslo wyciekło TRZY razy
  (z pliku slow, z odpowiedzi go2rtc /api/streams?src=, z logu Telegrama). Wszystkie
  miejsca wyczyszczone, ale haslo nalezy uznac za jawne i zmienic.
- ZERO wysylania surowego materialu do Genka.
- ZERO trwalych zmian na NVR/kamerach bez osobnego slowa Tomasza.

## 11. JAK WEJSC NA ROUTER LINKSYS (procedura, ktorej brakowalo w zapisach)

Tomasz 13.08: "Robiles to przez tailscale". Tak — i to jest cala droga, bez apki i bez hasla:

    curl -s -X POST "http://192.168.3.1/JNAP/" \
      -H "X-JNAP-Action: http://linksys.com/jnap/devicelist/GetDevices" \
      -H "Content-Type: application/json" -d '{}'

- z VPS, przez Tailscale (trase 192.168.3.0/24 oglasza homeassistant-1 = N150, 100.115.112.5)
- API JNAP Linksysa oddaje liste urzadzen BEZ autoryzacji; core/GetDeviceInfo tez
- devicelist/GetDevices3 NIE ISTNIEJE na tym firmware — zwraca _ErrorUnknownAction
- NIE probowac przez aplikacje Linksys na telefonie: to WebView, mapa elementow rozjezdza sie
  z obrazem, tapniecia trafiaja w inne miejsca (13.08 zamiast listy urzadzen odpalil sie
  test predkosci i fast.com)
- przegladarka mobilna tez odpada: panel zwraca "Linksys Smart Wi-Fi nie obsluguje twojej przegladarki"

ROUTER: Linksys WRT1900ACS, firmware 2.0.2.188405 (2018-05-01), sieci ROD_Wozniki_2 i _5GHz.
STAN 13.08: 147 wpisow urzadzen, 25 podlaczonych.

NAZWY KAMER WIDZIANE PRZEZ ROUTER:
- .110 "Recodder" (nagrywarka), MAC 3C:1B:F8:6D:66:D1
- .111 DS-2CD1041G0-I-PL...0924766, MAC 74:3F:C2:AE:3B:BD
- .112 DS-2CD1041G0-I-PL...0924802, MAC 74:3F:C2:AE:3B:E1
- .114 DS-2CD1041G0-I-PL...0925072, MAC 74:3F:C2:AE:3C:F0
- .113 "RODZARZAD", MAC D8:0F:99:4D:0D:FD  <-- INNY producent karty sieciowej niz trzy
  pozostale (74:3F:C2 = Hikvision). Nazwa "RODZARZAD" powtarza sie tez pod .102 i .21,
  wiec to etykieta wpisana recznie w routerze, nie nazwa wlasna kamery.
