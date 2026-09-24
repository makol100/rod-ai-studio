
## 20.09.2026 ~23:59 — APELACJA ZŁOŻONA W CENTRUM POMOCY (przez telefon, Klaudek na zlecenie Tomasza "Wejdź")
- Droga: apka AliExpress → Konto → Centrum pomocy → zamówienie Mini PC → Problemy ze zwrotami → "Zamówienie otrzymane, mam problemy z przedmiotami" → formularz (e-mail + opis 1042 zn.)
- Treść: pełna apelacja (kopia w /tmp/apelacja.txt na VPS) — sprawa 2053808791215177, spór "Personal reasons" z instrukcji sprzedawcy, pisemne uznanie wady 24.08, żądanie: wznowienie + wymiana z trackingiem albo zwrot 159,71 EUR
- Weryfikacja: pole == plik co do znaku (1042/1042, accessibility tree); wysłanie potwierdził GENEK ze screenshota: "Otrzymaliśmy Twoje dane! Przekazaliśmy sprawę dalej... aktualizacje wyślemy e-mailem"
- Wcześniej tego wieczoru: czat FUCHU odczytany — na ultimatum 48h (mija 21.09) odpowiedzieli wykrętnie ("personel posprzedażowy nie otrzymał zamówienia") + prośba o ocenę; mail na AEbuyerservice = ślepa skrzynka (auto-reply)
- LEKCJA TECHNICZNA: formularz WebView AliExpress gubi znaki przy type_append (literówki "aftet", "idenical"); NIEZAWODNA metoda = set_clipboard → tap w pole → tap w CHIP SCHOWKA na pasku Gboard (natywna wklejka całości); clear_text działa z opóźnieniem (raportować 2x po 3 s); tap w "prześlij" celować w ŚRODEK przycisku

## 21.09.2026 ~11:25 — DRUGIE ZGŁOSZENIE WYSŁANE, TYM RAZEM Z DOWODAMI (na "Składaj" Tomasza)
- Formularz Centrum pomocy przy zamówieniu Mini PC: opis 897 zn. (Re: Case 2053808824560175, kopia /tmp/apelacja2.txt) + DWA załączniki: KOLAZ_A_raport.jpg (pełny raport diagnostyczny z czatu 23-24.08: dysk akceptuje zapisy ale ich nie utrwala, 9 prób naprawy) i KOLAZ_B_zobowiazanie.jpg (zobowiązanie sprzedawcy 24.08 07:46 + jego instrukcja "Powód osobisty" 09:00)
- Checkpointy zaliczone: opis 897/897 identyczny (accessibility tree), 2 kolaże dodane po jednym na przejście przez Photo Picker, prześlij w środek (542,2308)
- Wysłanie potwierdził GENEK ze screenshota: "Otrzymaliśmy Twoje dane! Przekazaliśmy sprawę dalej... aktualizacje wyślemy e-mailem"
- Pierwsze podejście tego dnia (formularz zniknął przed kliknięciem prześlij) — status niewyjaśniony, Tomasz kazał składać ponownie; ewentualny duplikat zgłoszenia jest akceptowalny

## 22.09.2026 ~07:05 — TRZECIE ZGŁOSZENIE: ZDJĘCIE AWARII + 2 KOLAŻE (na "Ok" Tomasza)
- 22.09 03:25 mail AliExpress (nowa sprawa 2053808827134128): znowu szablonowa odmowa "evidence does not sufficiently demonstrate a quality-related issue", żądają video/picture/quality inspection
- Znalezione w galerii Folda (skan DCIM/Camera po nazwach 202608xx, 12 trafień): JEDYNE zdjęcie awarii = 20260815_223830.jpg — ekran N150 w rescue mode ("You are in rescue mode... Press Enter for maintenance"), 15.08 22:38, noc padnięcia SSD; ściągnięte na VPS do data/n150_reklamacja/foto/ (razem z 11 innymi z tego okresu — nieprzydatne, zweryfikował Genek opisując każde)
- Zgłoszenie: formularz Centrum pomocy, opis 1024 zn. (kopia /tmp/apelacja3.txt) + 3 załączniki: AWARIA_SSD_rescue_mode_15sie.jpg (wgrane do builtin:pictures, na wierzch pickera) + KOLAZ_A_raport.jpg + KOLAZ_B_zobowiazanie.jpg
- Checkpointy: opis 1024/1024 identyczny, 3 załączniki po jednym na przejście pickera (kafel "22 wrz" potem 2x "21 wrz 11:09"), prześlij w środek (542,2308)
- Wysłanie potwierdził GENEK ze screena: "Otrzymaliśmy Twoje dane! Przekazaliśmy sprawę dalej... aktualizacje wyślemy e-mailem"
- Nasłuch mailowy (trigger trig_0175A24TsqgQnmTwdZ5dKKS9, co 4 h) dalej aktywny; ultimatum FUCHU minęło 21.09 bez trackingu; plan B (decyzja Tomasza): chargeback 159,71 EUR

## 22.09.2026 ~07:50 — CZAT Z AGENTEM: DODATKOWE INFO DODANE DO SPRAWY, ESKALACJA 48H
- Rano: 13 oryginalnych zdjec awarii od Tomasza w czacie Claude (rescue mode, "BLAD: nie widze dysku docelowego", WBM 0xc000007b, PXE no boot device, BIOS z SSD 512GB); KOLAZ_C_awaria_boot.jpg zbudowany w kontenerze, wyslany Tomaszowi do czatu (transfer na VPS zablokowany przez proxy - bez znaczenia)
- Czat obslugi (Uslugi online): Eva potwierdzila "sprawa rozpatrywana przez dzial wyzszy"; opcja "Chce podac dodatkowe informacje" -> wyslano pelny opis dowodow TEKSTEM (czat2/czat3/czat4.txt w /tmp na VPS) + potwierdzenie e-maila (radio "Potwierdzilem" + przeslij)
- ZYWA AGENTKA pytala "dodac sam opis czy tez zdjecia/film?" -> odpowiedziano: opis ORAZ zdjecia, zdjecia juz w formularzach 21.09 11:25 i 22.09 7:05
- FINAL: agentka "Dodalam dodatkowe informacje do sprawy. Starsi agenci odpowiedza e-mailem w ciagu 48 godzin"
- LEKCJA: obrazy do czatu WebView AliExpress NIE wchodza zdalnymi tapami (picker wraca, obraz nie dociera) - dowody obrazowe TYLKO formularzem; tekst chip-methodem dziala zawsze
- Nasluch mailowy aktywny (co 4h); nastepny ruch po odpowiedzi "starszych agentow"; plan B niezmiennie: chargeback 159,71 EUR (decyzja Tomasza)

## 22.09.2026 ~10:35 — SPÓR CHARGEBACK W REVOLUT ZŁOŻONY
- Transakcja: AliExpress −159,71 €, 10 cze 12:22, Mastercard ··6260 (konto Osobiste EUR)
- Droga: transakcja → Uzyskaj pomoc → "Mam problem z towarem lub usługą" → Otwórz spór
- UWAGA: pierwsze podejście (rano) przepadło — Revolut po ponownym otwarciu apki przeładował się na ekran główny i szkic zniknął; flow przeszedłem drugi raz w całości
- Odpowiedzi: kategoria "Produkty fizyczne"; dostarczone=Tak; zwrot=Nie (uzasadnienie: sprzedawca kazał zatrzymać wadliwy dysk, brak adresu zwrotu, obiecana wymiana nigdy nie wysłana, spór AliExpress odrzucony przez "Personal reasons"); powód="Produkt był niezgodny z opisem"; dowód zgody usługodawcy na rekompensatę=Tak
- Teksty: ID zamówienia 3074044373716208; opis produktu (Mini PC, Win11, SSD 512GB, FUCHU); opis sporu EN (849 zn., /tmp/opis_spor.txt na VPS) — awaria 15/16.08, 0xc000007b, 9 prób naprawy, pisemne uznanie wady 24.08 (nowy dysk + 30 USD), nic nie wysłane
- Załączniki: potwierdzenie kontaktu = kolaż zobowiązania sprzedawcy (11:09 #2); dowód zakupu = 2 pliki (kafel 10:59 #1 + drugi dołączony przy powtórce Gotowe); dowody = 4 pliki (oba kolaże 21.09 11:09, kolaż Tomasza 22.09 08:32, rescue mode 22.09 06:59)
- Finalny "Prześlij" kliknięty na wyraźne polecenie Tomasza ("Prześli"/"Wyślij"/"zrób to wreszcie")
- STATUS po wysyłce (ekran transakcji): "Zgłoszenie w toku" → "Przesłano zgłoszenie – Chwilę temu" → "Otrzymaliśmy Twoją prośbę o spór. Rozpatrzymy ją w ciągu najbliższych 3 dni." → krok "Wynik" oczekuje; jest opcja "Anuluj"; rozpatrywanie do 90 dni
- Równolegle: nasłuch Gmail (trigger co 4h) na odpowiedź "starszych agentów" AliExpress (48h do ~24.09 rano)

## 22.09.2026 11:35 — REVOLUT: SPRZEDAWCA NIE ODPOWIEDZIAŁ, SPRAWA W PRZEGLĄDZIE
- Zrzut Tomasza 11:47: oś sporu „Przesłano zgłoszenie – Dzisiaj 10:33" → „Trwa spór z usługodawcą – Dzisiaj 11:35: Próbowaliśmy skontaktować się ze sprzedawcą, aby poprosić go o zwrot pieniędzy. Ponieważ nie udzielił odpowiedzi, teraz przejrzymy Twoją sprawę i postaramy się dostarczyć aktualizację w ciągu 3 dni." → krok „Wynik" oczekuje
- Wniosek: Revolut działa szybko (kontakt ze sprzedawcą w ~1 h), milczenie FUCHU = argument za nami; czekać na aktualizację do ~25.09

## 22.09.2026 13:47 — E-MAIL Z APELACJĄ WYSŁANY W WĄTKU SPRAWY #2053808831838409
- Po nieudanych próbach 4. zgłoszenia formularzem (ekran blokował się, Genek mylił kafle galerii, Tomasz: "Złe zdjęcie zaznaczyłeś") Tomasz zarządził zmianę drogi: "Naszykuj mi e-mail do nich zdjęcie dam sam"
- Draft przygotowany w Gmailu jako ODPOWIEDŹ w wątku dzisiejszego maila AliExpress (Following Up... 3074044373716208, 09:24); Tomasz dodał zdjęcie i wysłał sam
- WERYFIKACJA przez Gmail API (get_thread): mail w SENT 13:47, pełna treść apelacji (Case IDs 2053808831838409/2053808827134128/2053808824560175, 4 objawy wady, 9 prób naprawy, zobowiązanie sprzedawcy 24.08, ustawka "Personal reasons", żądanie zwrotu 159,71 EUR), załącznik: 1 × 24755.jpg (~230 KB; treści obrazu nie zweryfikowano — telefon zablokowany), brak auto-reply w wątku na chwilę weryfikacji
- LEKCJA: kafel galerii "22 wrz 08:32" ≠ KOLAZ_C (to zdjęcie przedmiotu/głośnika) — Tomasz nigdy nie zapisał kolażu C do galerii; w Revolut jako 1. dowód poszło to zdjęcie (bez szkody — pozostałe 3 dowody prawidłowe); kafle wybierać po TREŚCI (weryfikacja Genkiem), nie po dacie
- Nasłuch mailowy co 4 h aktywny; czekamy: odpowiedź "starszych agentów" (~24.09), rozpatrzenie Revolut (do ~25.09)

## 22.09.2026 14:06 — KOREKTA: 24755.jpg TO KOLAŻ AWARII (potwierdzone zdjęciem od Tomasza)
- Tomasz pokazał w czacie zawartość 24755.jpg: kolaż 2x2 ORYGINALNYCH ekranów awarii — (1) rescue mode systemd, (2) "N150 AUTOPILOT: BLAD: nie widze dysku docelowego" + Alpine 3.22, (3) Windows Boot Manager 0xc000007b "required file is missing or contains errors", (4) PXE-E61 Media test failure / "Reboot and Select proper Boot device"
- WNIOSKI: (a) mail z 13:47 do sprawy #2053808831838409 zawiera WŁAŚCIWY dowód, zgrany 1:1 z 4 punktami treści; (b) pierwszy dowód w sporze Revolut (24755(2).jpg z kafla 08:32) to TEN SAM kolaż — był dobry; wcześniejszy alarm "głośnik" = pomyłka Genka na małej miniaturze
- LEKCJA GENKA: rozpoznawanie treści MINIATUR (kafle galerii, miniatury formularza) jest zawodne — ciemne zrzuty ekranów myli z przedmiotami; werdykty o obrazach wydawać z pełnowymiarowego pliku, nie z miniatury; przy sprzeczności dwóch odczytów Genka NIE działać na ich podstawie

## 22.09.2026 ~14:48 — WYGRANA: REVOLUT WYPŁACIŁ WARUNKOWY ZWROT 159,71 EUR
- Zrzuty Tomasza 14:48 ("Wygraliśmy!!!!"): transakcja "Provisional refund for Aliexpress.com claim +159,71 €" na koncie Osobiste EUR; oś sporu: Przesłano zgłoszenie 10:33 → Przygotowujemy do przesłania usługodawcy 10:33 → WYPŁACONO WARUNKOWY ZWROT (chwilę temu) → Zgłoszenie przekazane usługodawcy
- Warunkowość: sprzedawca może zakwestionować chargeback — proces do 50 dni (Mastercard); przy milczącym FUCHU i pisemnym uznaniu wady z 24.08 ryzyko cofnięcia minimalne; do ~połowy listopada zwrot formalnie tymczasowy
- Od złożenia sporu (10:33) do wypłaty (~14:45): ~4 godziny
- Otwarte wątki: odpowiedź "starszych agentów" AliExpress (~24.09, mail z kolażem wysłany 13:47 w sprawie #2053808831838409), nasłuch co 4h aktywny; SSD do N150 — WSTRZYMANIE (dekret Tomasza 14:09), po wygranej może wrócić

## 22.09.2026 15:41 — DECYZJA TOMASZA: „Naprawa"
- Po przeglądzie 5 rynków (Amazon.de, AliExpress, willhaben, Allegro, OLX) Tomasz wybrał NAPRAWĘ obecnego N150: zakup Intenso Top M.2 2280 SATA 256GB (~25 €), wymiana dysku, reinstalacja HAOS, restore z pendrive'a ratunkowego (komplet + mariadb.tar)
- Odrzucone: nowy mini PC (N150 16GB w EU 240–380 € przez drożyznę RAM/NAND), Dell poleasing 757 zł, Firebat T8 Plus 1040 zł; Firebat S1 (jak HA Dom) niedostępny na żadnym rynku
- Wygrana z Revolut (159,71 €) zostaje w kieszeni

## 22.09.2026 15:48 — DYSK ZAMÓWIONY (zrzut potwierdzenia od Tomasza)
- Amazon.de: "Die Bestellung wurde aufgegeben" — Intenso Top M.2 SSD SATA III 256GB (M.2 2280, 520 MB/s, 38,51 €), wysyłka do Tomasz Maksys, Reiterstrasse 22/16, GWARANTOWANA DOSTAWA 23.09.2026 (Prime)
- NASTĘPNY KROK: przy najbliższym wyjeździe na działkę — wymiana dysku w N150 (slot M.2, w miejsce starego), instalacja HAOS x86-64 z Ubuntu Live USB, restore z pendrive'a ratunkowego SanDisk (komplet: apps, homeassistant, ssl, storage.tar, mariadb.tar), Tailscale Start on boot + Watchdog, weryfikacja trasy 192.168.3.0/24 (NVR); STAREGO dysku nie wyrzucać (awaryjne źródło danych)
- BILANS DNIA: chargeback Revolut wypłacony +159,71 € (warunkowo, do ~50 dni), dysk −38,51 € → Tomasz na plusie 121,20 €, a Działka rusza po ~5 tygodniach przestoju
- 22.09 15:48 Tomasz: "W weekend bede" — wymiana dysku i odbudowa N150 zaplanowana na weekend 27-28.09 na działce
