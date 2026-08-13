# ZADANIE KONTROLNE: wpiecie kamer HiLook do HA Dzialka przez go2rtc

Tomasz 13.08: "go2rtc podobno gotowy. Przedyskutuj to z druzyna."
To jest zlecenie KONTROLNE — kazdy odpowiada na pytania rozstrzygalne, podpisuje sie,
i wprost pisze NIE WIEM tam, gdzie nie ma sladu. Rozstrzyga Tomasz.

## FAKTY ZMIERZONE DZIS (13.08, wszystkie ze sladem, nie z pamieci)

Kamery HiLook / nagrywarka, siec dzialkowa 192.168.3.0/24, dosiegalne z VPS przez Tailscale.
Poswiadczenia URZADZENIA przyszly od Tomasza przez Telegram i dzialaja (wczesniej mielismy
tylko konto Hik-Connect z aplikacji -> wszedzie 401).

ISAPI /System/deviceInfo (curl --digest):
- 192.168.3.110  HTTP 200  "Network Video Recorder"  NVR-4CH-5MP  fw V4.76.010
- 192.168.3.111  HTTP 200  "Kamera brama"   DS-2CD1041G0-I/PL  fw V5.7.0
- 192.168.3.112  HTTP 200  "KAMERA 2"       DS-2CD1041G0-I/PL  fw V5.7.0
- 192.168.3.114  HTTP 200  "Kamera4"        DS-2CD1041G0-I/PL  fw V5.7.0
- 192.168.3.113  HTTP 401  (inne haslo albo martwe urzadzenie — NIEUSTALONE)

Porty na .110: 80 open, 554 open, 8000 open; 443/8200/8443/9000 zamkniete.

RTSP z NAGRYWARKI .110, /Streaming/Channels/<kanal> (ffprobe, transport TCP):
- kanal 101: DZIALA — hevc 1280x720, 20 fps
- kanal 201: DZIALA — hevc 2560x1440, 20 fps
- kanal 301: 404 Not Found  (to jest kanal "Rog", w aplikacji HiLook widoczny jako OFFLINE)
- kanal 401: DZIALA — hevc 1280x720, 20 fps
Czyli WSZYSTKIE dzialajace strumienie sa w H.265 (HEVC).

Stan HA Dzialka (zmierzony przez konektor):
- Home Assistant 2026.8.1, strefa Europe/Warsaw, stan RUNNING
- Dodatek go2rtc a889bffc_go2rtc, wersja 1.9.14, state=started, boot=auto, watchdog=FALSE,
  auto_update=FALSE, ingress port 1984, host_network=true, opis dodatku: "Transcoding for
  Intel (VAAPI) and Raspberry (V4L2)". options={} (pusty obiekt), schema=[].
- go2rtc /api/streams zwraca 4 JUZ SKONFIGUROWANE strumienie, wszystkie kamery Xiaomi
  z sieci domowej 192.168.0.x (cam_domek_114, cam_furtka_121, cam_taras_127, cam_zachod_112),
  producenci typu xiaomi://... — czyli dodatek pracuje i ma dzialajaca konfiguracje.
  UWAGA: te wpisy zawieraja poswiadczenia w URL — nie kopiowac ich do meldunku ani do czatu.
- Sprzet: HA Dzialka chodzi na mini-PC Intel N150.
- Dodatki obecne m.in.: Mosquitto, MariaDB, Tailscale, Zigbee2MQTT, ESPHome, Whisper, Piper,
  Music Assistant, Studio Code Server, Samba, Advanced SSH.
- Frigate NIE jest zainstalowany.

Kontekst zdalny: Tomasz jest 600 km od dzialki, laczy sie przez Tailscale, ogląda z telefonu.

## PYTANIA ROZSTRZYGALNE

P1. Home Assistant 2026.8.1 ma WBUDOWANY go2rtc w rdzeniu, a na dzialce chodzi dodatkowo
    ODDZIELNY dodatek go2rtc 1.9.14 z wlasnymi 4 strumieniami Xiaomi.
    Gdzie wpiac strumienie HiLook: do dodatku czy do wbudowanego go2rtc?
    Czy dwa go2rtc naraz to konflikt (porty 1984/8555, WebRTC), czy wspolistnieja?
    Odpowiedz z odwolaniem do dokumentacji/zrodel, nie z przeczucia.

P2. Strumienie sa w H.265. Czy podglad w Lovelace na telefonie Tomasza (Android, Chrome)
    zadziala BEZ transkodowania przez WebRTC, czy trzeba transkodowac do H.264?
    Jesli trzeba — czy VAAPI na Intel N150 to udzwignie dla 3 strumieni (w tym jeden 2560x1440)
    i jaki bedzie koszt CPU? Czy jest tansza droga: przestawic kamery na H.264 przez ISAPI
    (kamery to DS-2CD1041G0-I/PL, 4 Mpx) albo uzyc SUBSTRUMIENIA (kanal 102/202/402), ktory
    w Hikvision/HiLook czesto jest H.264 — tego jeszcze NIE ZMIERZYLISMY.

P3. Brac strumienie z NAGRYWARKI (.110 kanaly 101/201/401) czy BEZPOSREDNIO z kamer
    (.111/.112/.114)? Co jest pewniejsze przy 600 km i po co placic podwojnym przejsciem
    przez NVR? Jakie sa wady kazdej drogi (limit sesji RTSP na kamerze, nagrywanie na NVR,
    restart NVR)?

P4. Co zrobic z .113 (HTTP 401) i kanalem 301 (404). Czy da sie to rozstrzygnac ZDALNIE
    bez wizyty na dzialce i bez zgadywania hasel (uwaga: HiLook blokuje konto po kilku
    nieudanych probach — dzis zrobilismy juz 15 prob).

P5. RYZYKA I KOSZT. Co moze pojsc zle przy wpieciu (obciazenie N150, pasmo Tailscale,
    watchdog dodatku wylaczony, brak auto_update, nagrywanie na NVR). Czy cokolwiek z tego
    kosztuje pieniadze. Maksymalnie 5 punktow, kazdy z zapobieganiem.

P6. JEDNA REKOMENDACJA: konkretna sciezka wdrozenia w krokach, od najtanszej i najmniej
    ryzykownej. Napisz wprost, ktory krok jest odwracalny, a ktory nie.

## ZASADY ODPOWIEDZI
- Kazde twierdzenie ze sladem (plik, wynik polecenia, dokumentacja z adresem). Bez sladu = NIE WIEM.
- Nie kopiowac poswiadczen ani URL-i z haslami.
- Rozbieznosc miedzy wami zostaje widoczna — nie uzgadniajcie jej miedzy soba.
- Podpis na koncu.
