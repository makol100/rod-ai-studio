# Solar Assistant — odczyt z apki na telefonie Tomasza (23.09.2026 11:26–11:32), TYLKO ODCZYT, nic nie zmieniano (D-0487, D-0494)
Adres: https://makol100.eu.solar-assistant.io (WebAPK org.chromium.webapk.ae31dbd744219ab9c_v2)

## Pulpit 11:26
Tryb falownika: solary/akumulator. Obciążenie 946–967 W, PV 1,20–1,22 kW, sieć 13–41 W, akumulator +233–326 W (ładowanie), 46,5 V, SoC 22 % (+0,7 %/h). Sieć 229 V, cena w SA 44,1 gr/kWh. Prognoza SA „PV dzisiaj 1.9 kWh" (Pochmurno).

## Falownik — Specyfikacja (/inverter/settings)
Sterownik InfiniSolar V, połączenie Direct cable, SN 96132411100028, FW 05613, numer modelu 7, typ urządzenia Off-grid, beztransformatorowy, max 9 jednostek równoległych, napięcie znamionowe akumulatora 48,0 V, oczekiwane napięcie AC we 240 V, maks. prąd wejściowy AC 23,3 A, maks. moc wyjściowa AC 5,60 kW / 5,60 kVA.

## Akumulator
Typ User; Priorytet źródła ładowania: Solary i sieć jednocześnie; Wyłączenie przy 44,0 V; Napięcie akumulatora oddawane do sieci (back to grid) 48,0 V; Wróć do napięcia akumulatora 50,0 V; Float 56,0 V; Absorpcja 56,8 V; Maks. prąd ładowania 120 A; Maks. prąd ładowania z sieci 40 A.

## Wejście/wyjście
Tryb wyjściowy: pojedyncze urządzenie; Zakres napięcia wejściowego AC: Urządzenie; 50,0 Hz; 240 V; Priorytet źródła wyjściowego: Solary/Akumulator/Sieć (SBU); Bypass przy przeciążeniu: Włączone; Ponowny start po przeciążeniu: Wyłączone.
## Różne: sygnał dźwiękowy wył., podświetlenie wł.
## Fotowoltaika: Solar power priority: Load/Battery/Utility

## Zarządzanie energią (/power)
Priorytet źródła wyjściowego: Solary/Akumulator/Sieć.
Automatyzacja nr 1 — Battery protection: gdy SoC ≤ 25 % → Shutdown inverter output przez ustawienie „Shutdown battery voltage"; po odzyskaniu SoC przywróć 42,0 V. Przycisk „Enable" widoczny → WYŁĄCZONA (odczyt ze zrzutu).
Automatyzacja nr 2 — Stan naładowania akumulatora (krzywa SoC wg pory dnia → Output source priority): Point A 08:00: ≤30 % SUB, ≥40 % SBU; Point B 15:00: ≤70 % SUB, ≥80 % SBU. Przycisk „Enable" → WYŁĄCZONA.
Dziennik automatyzacji: brak wpisów widocznych.

## 23.09 12:08–12:10 — próba zmiany (polecenie Tomasza D-0498/0499 „max z sieci 20A", „Ładuj z sieci")
- SA /inverter/settings → Akumulator → edytuj → „Maksymalny prąd ładowania z sieci" 40 A → wybrano 20 A (opcje: 2,10,20,…,120 A).
- Po zapisie strona pokazała: „Maksymalny prąd ładowania z sieci 40 A Rejected" → falownik ODRZUCIŁ 20 A; wartość nadal 40 A.
- Priorytet wyjścia nadal SBU, priorytet ładowania „Solary i sieć jednocześnie" — bez zmian.
- 12:10 na telefonie aktywna apka SmartESS (Eybond, SN 96132411100028) — Tomasz działa sam; Klaudek przestał sterować ekranem.
## 23.09 12:14–12:17 — test ładowania (D-0501)
- 12:15 w SA wyjście przełączone SBU → SUB; potwierdzone: „Falownik Tryb solary/sieć".
- 12:15 odbiory 949 W, PV 1,41 kW, sieć 69 W, bateria +488 W, 48,8 V, 23 %.
- 12:17 odbiory 899 W, PV 5,98 kW (24 A), sieć — (brak poboru), bateria +4,63 kW 50,9 V 91 A — ładuje słońce; limit łączny ładowania 120 A.
- Max prąd ładowania z sieci = 20 A (ustawił Tomasz, potwierdzone w SA 12:13).
## 23.09 12:21 — 50 A (D-0504)
- Na stronie SA: „Maksymalny prąd ładowania z sieci 20 A Rejected" → zapis 50 A odrzucony przez falownik, zostaje 20 A. Priorytet wyjścia: Solary/Sieć/Akumulator (SUB). Ładowanie: Solary i sieć jednocześnie.
- Wniosek roboczy: zmiana priorytetu wyjścia przez SA przechodzi (SBU→SUB 12:15 OK), zmiana prądu ładowania z sieci przez SA jest odrzucana (2×), przez SmartESS przeszła (20 A, Tomasz 12:12).
## 23.09 12:23 — po ustawieniu 50 A (Tomasz przez SmartESS, D-0505)
- SA potwierdza: Maks. prąd ładowania z sieci 50 A; wyjście Solary/Sieć/Akumulator (SUB), tryb „solary/sieć"; ładowanie „Solary i sieć jednocześnie".
- ALE: odbiory 937 W, PV 1,12 kW, sieć 70 W, bateria +198 W, 49,5 V, 24 % → SIEĆ NIE ŁADUJE baterii mimo SUB + SNU + 50 A.
## Trop: okno czasowe ładowania z sieci (Klaudek, 12:27)
Instrukcja MPP Solar Hybrid V2 3K/5K (rebrand InfiniSolar V), https://mppsolar.com/manual/HYBRID%20V,V2,V3P/Hybrid%20V2-3K,%205K%20manual-20200317.pdf , s. 16:
- Program 30 „Start charging time for AC charger" 00:00–23:00, co 1 h, domyślnie 00:00
- Program 31 „Stop charging time for AC charger" 00:00–23:00, co 1 h, domyślnie 00:00
- Program 32/33 „Scheduled time for AC output on/off"
s. 12: program 10 charger source — działa tylko w Line/Standby/Fault; w Battery/Power saving mode ładuje tylko PV.
UWAGA: ta instrukcja podaje maks. ładowanie 5 kW 10–80 A, a falownik Tomasza pokazuje 120 A — inny wariant/generacja; mapowanie programów do potwierdzenia.
## 23.09 12:33 — zrzut SmartESS od Tomasza („Kontrola urządzenia")
- Solar Supply Priority: Battery-Load-Utility / Load-Battery-Utility (wybrane: Load-Battery-Utility)
- Reset PV energy storage; Country Customized Regulations
- Start Time For Enable AC Charger Working / Ending Time For Enable AC Charger Working — okno ładowania z sieci (potwierdza trop z instrukcji Hybrid V, program 30/31)
- Start time / Ending time for enable AC supply the load — okno zasilania odbiorów z sieci (program 32/33)
- Set Date Time
Pola czasów puste w chwili zrzutu — Tomasz: „Pobiera dane".
## 23.09 12:41 — zrzut SmartESS od Tomasza (po wpisaniu)
- Start Time For Enable AC Charger Working 12:00; Ending 15:00 (wpisane, stan wysłania nieznany)
- Start time for enable AC supply the load 00:00; Ending 00:00 (szare, ikona pobierania)
- Country Customized Regulations: Germany
- Set Date Time: 2026-09-23 12:51:14 przy zegarze telefonu 12:41 → jeśli to odczyt z falownika, zegar falownika spieszy się ~10 min (okna czasowe liczą się wg zegara falownika)
## 23.09 12:43 — „nie ładuje z sieci" (odczyt SA) + przyczyna
- 12:43: tryb solary/sieć, odbiory 956 W, PV 1,28 kW, sieć 29–86 W, bateria +297 W 49,5 V 6 A, SoC 24 %.
- PRZYCZYNA (Zenek + Genek, potwierdzone w instrukcji InfiniSolar V IV 2021-11-15, s. 18): program 21 „Battery stop charging voltage when grid is available" — opcje „Battery fully charged" albo 48–58 V co 1 V, domyślnie 54 V. U Tomasza ustawione 50,0 V (w SA: „Wróć do napięcia akumulatora 50.0 V") → sieć przestaje ładować przy 50 V. O 12:17 bateria miała 50,9 V (słońce) → ładowanie z sieci stanęło; 49,5 V leży między progiem 48 V (program 20, „Napięcie akumulatora oddawane do sieci") a 50 V.
- Program 20 „Battery stop discharging voltage when grid is available" = 48,0 V.
- Zenek (isv_okna): AC Charger 00:00→00:00 = brak ograniczenia czasowego (instrukcja InfiniSolar 10KW s. 25); okno przez północ NIE WIEM; „AC supply the load" = timer wyjścia — poza oknem odbiory mogą zostać WYŁĄCZONE.
