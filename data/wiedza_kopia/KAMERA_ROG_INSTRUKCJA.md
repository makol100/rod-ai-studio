# KAMERA ROG (.113) — INSTRUKCJA WLACZENIA DO CALEGO SYSTEMU

Stan na 14.08.2026. Ta kamera NIGDY nie dzialala: NVR ma przy niej puste pola
model/serial/firmware, czyli ani razu sie z nia nie polaczyl. Powod: NVR loguje sie
jako "admin" i dostaje errorUserNameOrPasswd. Oba znane haslа Tomasza (komplet A 14 znakow,
komplet B 10 znakow) daja na .113 HTTP 401 — kamera ma TRZECIE haslo, ktorego nikt nie zna.
Dodatkowo .113 to INNY MODEL niz pozostale trzy: realm "IP Camera(FQ921)" kontra
"IP Camera(FG092)", MAC D8:0F:99 kontra 74:3F:C2 (Hikvision).

DLACZEGO TO PILNE: uszkodzony Opel Insignia stal wlasnie w polu widzenia tej kamery.
Rog parkingu jest slepy — nagran z miejsca, gdzie kuna niszczy auta, po prostu NIE MA.

==============================================================
CZESC 1 — CO ROBI TOMASZ NA MIEJSCU (bez tego reszta niemozliwa)
==============================================================

KROK 1. Znajdz kamere i przycisk RESET.
  - Kamera stoi w rogu parkingu, adres w sieci: 192.168.3.113
  - Przycisk RESET jest zwykle pod obrotowa oslona przy podstawie albo pod gumowa
    zaslepka na kablu. W modelach kopulkowych — po zdjeciu klosza.
  - Potrzebne: srubokret (czasem imbus do klosza), spinacz/cienki trzpien do przycisku.

KROK 2. Reset do ustawien fabrycznych.
  - Kamera MUSI byc pod napieciem (dioda swieci).
  - Przytrzymac RESET okolo 10-20 sekund, az kamera zamruga/zrestartuje sie.
  - Puscic. Kamera wstaje z ustawieniami fabrycznymi w 1-2 minuty.
  - UWAGA: po resecie kamera bierze adres fabryczny (zwykle 192.168.1.64 albo z DHCP),
    a NIE 192.168.3.113. To normalne, poprawiamy w kroku 3.

KROK 3. Aktywacja i ustawienie hasla.
  - Kamery HiLook/Hikvision po resecie sa NIEAKTYWNE — trzeba nadac im haslo przy
    pierwszym logowaniu. Bez tego nic nie dziala.
  - Dwie drogi:
    (a) telefon w sieci ROD -> przegladarka -> adres kamery -> kreator prosi o haslo;
    (b) laptop z programem SADP (Hikvision) -> widzi kamere nawet z obcym adresem.
  - HASLO USTAWIC TO SAMO CO NA POZOSTALYCH KAMERACH (komplet A, ten 14-znakowy,
    Klaudek ma go w skrytce). Dzieki temu NVR i wszystkie narzedzia beda dzialac bez zmian.
  - Login: admin

KROK 4. Ustawienie adresu na 192.168.3.113.
  - W panelu kamery: Konfiguracja -> Siec -> TCP/IP
  - Adres IP: 192.168.3.113
  - Maska: 255.255.255.0
  - Brama: 192.168.3.1  (Linksys WRT1900ACS, wspolna siec ROD)
  - DNS: 192.168.3.1
  - Zapisz, kamera sie zrestartuje pod nowym adresem.

KROK 5. Napisz Tomaszowi "gotowe" — reszte robi Klaudek zdalnie.

==============================================================
CZESC 2 — CO ROBI KLAUDEK ZDALNIE (po zgloszeniu "gotowe")
==============================================================

KROK 6. Sprawdzenie, czy kamera odpowiada.
  curl --digest -u <login>:<haslo> http://192.168.3.113/ISAPI/System/deviceInfo
  Oczekiwane: HTTP 200, model, numer seryjny, wersja firmware.

KROK 7. Wpiecie do NVR jako kanal 3.
  NVR .110 ma juz wpis dla kanalu 3 z adresem .113 i uzytkownikiem admin — brakuje
  tylko poprawnego hasla. Zmiana przez ISAPI:
  PUT http://192.168.3.110/ISAPI/ContentMgmt/InputProxy/channels/3
  z haslem w polu <password>. Potem sprawdzenie:
  GET /ISAPI/ContentMgmt/InputProxy/channels/status
  Oczekiwane: kanal 3 online=true, stan "connect" zamiast errorUserNameOrPasswd.
  Od tej chwili NVR ZACZYNA NAGRYWAC ten kanal — zapis ciagly, retencja 30 dni.

KROK 8. Strumien na zywo do go2rtc.
  Dodatek a889bffc_go2rtc na N150, API na porcie 1984. Dodac dwa strumienie:
    rod_rog      = rtsp://.../Streaming/Channels/301   (glowny)
    rod_rog_sub  = rtsp://.../Streaming/Channels/302   (podstrumien, do kafelka)
  Tak samo jak rod_brama / rod_kamera2 / rod_kamera4 zrobione 13.08.

KROK 9. Encja w Home Assistant.
  W /config/configuration.yaml, w sekcji camera:, dopisac wzorem pozostalych:
    - platform: ffmpeg
      name: ROD Rog
      input: -rtsp_transport tcp -i rtsp://100.115.112.5:8554/rod_rog_sub
  Kopia zapasowa pliku PRZED zmiana. Potem sprawdzenie konfiguracji i restart HA
  (encje kamer z YAML powstaja tylko po restarcie).
  Efekt: encja camera.rod_rog.

KROK 10. Kafelek w widoku "Kamery".
  Dashboard lovelace, widok path=kamery, karta custom:advanced-camera-card
  z encja camera.rod_rog — dolozona na koncu, nic istniejacego nie ruszane.

KROK 11. Wlaczenie do szukania kun.
  - Genek oglada jedna klatke dzienna z nowej kamery i wyznacza ROI na autach
    (tak jak dla kanalu 4: crop=520:244:760:38).
  - Skrypt /share/kuny/pobierz_okno.sh dostaje track 301 zamiast 401.
  - Detekcja /share/kuny/detekcja2.py z nowym ROI.
  - Od tej nocy rog parkingu przestaje byc slepy.

==============================================================
CZEGO NIE ROBIC
==============================================================
- NIE probowac zgadywac hasla przez logowanie: HiLook blokuje konto po 5 nieudanych
  probach na 30 minut. 13.08 zrobiono juz okolo 15 prob.
- NIE liczyc na wsparcie HiLook zamiast resetu: ich procedura odzyskiwania hasla wymaga
  programu SADP w TEJ SAMEJ sieci lokalnej (multicast nie przechodzi przez Tailscale),
  czyli i tak ktos musi byc na miejscu. Reset przyciskiem zalatwia to od reki i za darmo.
- NIE zmieniac adresow pozostalych kamer ani ustawien NVR "przy okazji".

==============================================================
CO TO DA
==============================================================
- rog parkingu przestaje byc slepy — pojawiaja sie nagrania z miejsca, gdzie stoja
  auta niszczone przez kune
- czwarty kanal NVR zaczyna nagrywac (dzis nagrywaja trzy z czterech)
- podglad na zywo w HA i w telefonie
- material do detekcji nocnej z wlasciwego miejsca
