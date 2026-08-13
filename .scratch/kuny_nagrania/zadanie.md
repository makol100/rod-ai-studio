# ZADANIE DLA ZALOGI: nagrania z nagrywarki — szukanie KUN

Dekret Tomasza 13.08: "Jak macie dojscie do nagrywarki wyciagnac zapisy i szukac KUN!"
oraz "Noce to po godzinach najlepiej albo jest kurwa jakis inny sposob?"
oraz nagana dla Klaudka: "Jak nie potrafisz to zapytaj pracownikow. Po to oni sa
a ty kurwa ich bez przerwy omijasz!!!!!!!"

Zlecenie KONTROLNE. Nic nie wykonujecie. Rozstrzyga Tomasz.

## CO JUZ ZMIERZONE (13.08, odczyt ISAPI z NVR 192.168.3.110, nic nie zmieniane)

SCIEZKI NAGRAN (/ISAPI/ContentMgmt/record/tracks):
- track 101: H.264-BP 1280x720 20 fps 3072 kbps, retencja P30DT0H
- track 201: H.264-BP 2560x1440 20 fps 3072 kbps, retencja P0DT0H
- track 301: rozdzielczosc 0x0 (martwy kanal "Rog")
- track 401: H.264-BP 1280x720 20 fps 3072 kbps, retencja P30DT0H
- Enable=false na wszystkich czterech, a nagrania ISTNIEJA; 28 blokow harmonogramu
  ma ActionRecordingMode=CMR (zapis ciagly).
- NAGRANIA SA W H.264, choc podglad na zywo leci H.265.

GLEBOKOSC ARCHIWUM (szukanie 120 dni wstecz, pierwsze trafienie):
- kanal 1: od 2026-07-23 23:25
- kanal 4: od 2026-07-23 22:53
- kanal 2: od 2026-08-04 12:13
Czyli ~3 tygodnie na kanalach 1 i 4, ~9 dni na kanale 2.

SZUKANIE PO ZDARZENIACH RUCHU — DZIALA:
- metadataDescriptor "//recordType.meta.std-cgi.com/motion" -> NO MATCHES
- metadataDescriptor "//metadata.ps.hikvision.com/motionDetection" -> DZIALA

POMIAR ZDARZEN RUCHU, ostatnie 7 dni (przez ContentMgmt/search, maxResults 100, stronicowane):
- kanal 1 "Kamera brama": 129 zdarzen, w tym 55 miedzy 21:00 a 05:00
- kanal 2 "KAMERA 2": 191 zdarzen, 65 nocnych
- kanal 4 "Kamera4": 112 zdarzen, 58 nocnych
- rozklad godzinowy jest PLASKI: 5-9 zdarzen w KAZDEJ godzinie doby, takze w poludnie.

Pozostale fakty: NVR-4CH-5MP fw V4.76.010; kanal 3 martwy; kamery DS-2CD1041G0-I/PL;
HA Dzialka na Intel N150; VPS siega .110 przez Tailscale; Genek (Gemini) to jedyny
w zalodze, kto WIDZI obraz i wideo (tools/oczy_uszy.py, Files API do 2 GB).

## PYTANIA ROZSTRZYGALNE

P1. PLASKI ROZKLAD. 5-9 "zdarzen ruchu" w kazdej godzinie doby, rowno, takze w poludnie
    i o 3 w nocy. Co to naprawde jest: prawdziwe detekcje ruchu, czy NVR zwraca
    SEGMENTY nagrania ciaglego, a nie zdarzenia? Jak to ROZSTRZYGNAC pomiarem
    (np. porownac liczbe wynikow tego samego zapytania bez metadataDescriptor,
    albo sprawdzic dlugosc kazdego trafienia)? Podajcie konkretne zapytanie.

P2. JAK SCIAGNAC FRAGMENT. Konkretnie: ktore wywolanie ISAPI pobiera plik wideo
    z podanego przedzialu czasu (ContentMgmt/download z playbackURI? RTSP playback
    z naglowkiem Range?). Podajcie DZIALAJACA postac zapytania dla tego NVR
    (fw V4.76.010) i format, jaki wyjdzie. Czy da sie pobrac tylko wycinek 30 s
    wokol zdarzenia, czy tylko cale bloki.

P3. ILE TEGO JEST. Przy 3072 kbps i zapisie ciaglym — ile miejsca zajmuje doba na kanal,
    ile wazy 30-sekundowy wycinek, i ile realnie da sie sciagnac przez Tailscale
    bez zapchania lacza dzialki. Liczby, nie "duzo".

P4. JAK SZUKAC KUNY. Kuna jest nocna, mala, szybka, chodzi po dachach i kablach.
    Zaproponujcie SPOSOB odsiania materialu do obejrzenia — tak, zeby Genek dostal
    do obejrzenia dziesiatki wycinkow, a nie setki godzin. Uwzglednijcie, ze Genek
    liczy sie z kosztem (dekret "oszczedzac Genka") i ze film 58 s to juz ~15 tys.
    tokenow wideo (nasza wlasna lekcja z oczy_uszy.py).

P5. RYZYKA (maks 5, kazde z zapobieganiem) i KOSZT W ZLOTOWKACH — osobno koszt
    pobierania, osobno koszt ogladania przez Genka.

P6. KOLEJNOSC KROKOW, [O] odwracalny / [N] nieodwracalny. Pierwszy krok ma byc
    najtanszy i czysto odczytowy.

## ZASADY
- Kazde twierdzenie ze sladem. Bez sladu = NIE WIEM.
- NIE kopiowac poswiadczen ani URL-i z haslem (dzis haslo dwa razy wyciekło do okna czatu).
- Rozbieznosci zostaja widoczne, nie uzgadniajcie ich miedzy soba.
- Podpis.

## KOREKTA TOMASZA 13.08 12:3x — WAZNIEJSZA NIZ POWYZSZE
"Nie kablach a autach". ROI przy odsiewie: ZAPARKOWANE AUTA (numer jeden - kuna wchodzi
pod maske i przegryza przewody w samochodzie), dalej dachy i ogrodzenia. NIE kable.
Skutek: pierwszenstwo maja kamery i kadry obejmujace miejsca parkowania.
