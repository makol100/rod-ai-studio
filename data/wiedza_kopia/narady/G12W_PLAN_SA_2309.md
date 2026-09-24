# PLAN G12w w Solar Assistant (23.09.2026) — DO ZATWIERDZENIA, nic nie ustawione

## ZENEK
**POTWIERDZONE**
1. **1a TAK, warunkowo:** „Solary i sieć jednocześnie” zezwala na ładowanie z sieci bez względu na taryfę, lecz tylko w Line/Standby/Fault; w Battery mode ładuje wyłącznie PV. [Instrukcja Voltronic, s. 17](https://voltronicpower.com/content/download/Manual/InfiniSolar%20V%20IV%20manual-20211115.pdf)
2. **1b TAK według instrukcji:** w SBU falownik przechodzi na Utility po osiągnięciu programu 20; 46,5 V jest poniżej ustawionych 48,0 V, więc SBU nie zapewnia zera sieci w szczycie.
3. **2 TAK dla odczytanego obciążenia:** 40 A jest prądem DC baterii: 1,92 kW przy 48 V i maks. 2,27 kW przy absorpcji 56,8 V. [Odczyt SA](/root/rod-ai-studio/wiedza/SA_ODCZYT_2309.md:4)
4. Przy 229 V: przyłącze 25 A = 5,73 kVA, limit wejścia falownika 23,3 A = 5,34 kVA; idealnie na odbiory zostaje 3,42–3,06 kW, realnie mniej, a 0,946 kW się mieści.
5. **3a NIE:** nie ma poprawnych punktów A/B — jedna krzywa nie odwzoruje czterech okien doby G12w; obecnych 08:00 30/40% i 15:00 70/80% nie włączać.
6. **3b TAK:** Rule table obsługuje czas+SoC, a Charger source priority jest ustawieniem zapisywalnym; okna przez północ trzeba rozbić. [Rule table](https://solar-assistant.io/help/automation/table), [MQTT SA](https://solar-assistant.io/help/integration/mqtt)
7. **3c NIE:** SA nie ma udokumentowanego warunku polskich świąt/dni tygodnia; bez HA święta i weekend wymagają profilu ręcznego.
8. **4:** 7 h × 0,946 kW / 93% = 7,12 kWh = 23,7 pkt SoC; przy rezerwie 20% cel minimalny na 15:00 = 45%.
9. Przy 40 A przez 13–15 dojdzie teoretycznie maks. 3,72–4,54 kWh = 12,4–15,1 pkt; dlatego cel na 06:00 = minimum 57%, planowo 60% bez prognozowanego PV.
**HIPOTEZY — PLAN DO ZATWIERDZENIA**
10. Pn–pt Output: 00:00–05:59 SUB; 06:00–12:59 SBU; 13:00–14:59 SUB; 15:00–21:59 SBU; 22:00–23:59 SUB.
11. Charger: noc <60% „Solary i sieć”, od 60% „Tylko solary”; 13–15 analogicznie z celem 45%; w szczycie 0–100% „Tylko solary”.
12. Weekend/święto ręcznie: SUB całą dobę; „Solary i sieć” poniżej 25%, „Tylko solary” od 25%; przy założeniu 90% AC→DC limit odbiorów podczas 40 A przyjąć roboczo 2,8 kW.
**NIE WIEM**
13. Dlaczego odczyt przy 46,5 V nadal pokazał PV/baterię; dokładnej sprawności AC→DC, innych odbiorów na fazie i bezpiecznego niższego „back to grid” bez danych BMS.
14. Dalej: Tomasz zatwierdza profil **60% o 06:00 / 45% o 15:00**; do tego czasu obie automatyzacje pozostają wyłączone i niczego nie zmieniamy.
— Zenek

## GENEK
[GENEK — DROGA 1: wlasny dostep do dysku przez CLI]

1. **TAK**. Priorytet „Solary i sieć jednocześnie” (SNU) wpuszcza sieć bez ograniczeń czasowych. Przy napięciu 46,5 V < „back to grid” (48,0 V) w trybie SBU falownik przełącza się w całości na sieć. Skutek: w najdroższym szczycie falownik pobiera z sieci prąd na dom i dodatkowo ładuje nim akumulator.
2. **TAK**. Prąd ładowania 40 A DC do baterii (48 V) zabiera z sieci ok. 2,0–2,2 kW (z uwzględnieniem strat). Przyłącze główne 25 A (230 V) udostępnia maksymalnie 5,75 kW. Po odcięciu ok. 2,2 kW na ładowanie zostaje Ci ok. 3,55 kW (ok. 15,4 A) bezpiecznej rezerwy na odbiory.
3. Plan działania w bazowym Solar Assistant:
   (a) Automatyzacja krzywej SoC steruje przełącznikiem wyjścia. Punkty G12w: 13:00 i 22:00 -> SUB (sieć wspiera), 06:00 i 15:00 -> SBU (odcięcie sieci, praca z baterii).
   (b) **TAK**, SA posiada zakładkę „Rule table”, która powiąże akcję „Charger source priority” z godzinami (np. 15:00 -> OSO [tylko solary]).
   (c) **NIE**, sam SA nie umie rozpoznawać weekendów i dni ustawowo wolnych. Do tego musiałby być sprzężony z Home Assistantem (Workday sensor).
4. Oknom 6–13 i 15–22 (po 7 godzin) odpowiada zużycie 7 kWh (7 h * 1 kW obciążenia). 7 kWh z magazynu o pojemności 30 kWh to spadek o ok. 23 %. Okna ładowania z sieci (13–15 oraz 22–6) muszą pompować baterię do celu wynoszącego co najmniej **25–30 % SoC**.
Do zrobienia (Tomasz): Wejdź w SA i ustaw w „Rule table” nową pozycję, która codziennie o 6:00 i 15:00 przestawia priorytet ładowarki na „Tylko solary” (OSO), żeby natychmiast zatrzymać pompowanie drogiego prądu.
GENEK
## ROZBIEŻNOŚCI
- Cel SoC: Genek 25–30% (bez rezerwy dna) vs Zenek 45% o 15:00 / 60% o 06:00 (rezerwa 20%, 40 A w 13–15 daje max 12–15 pkt). Klaudek: przyjmuje liczby Zenka.
- Krzywa SoC (Automatyzacja nr 2): Genek — da się; Zenek — jedna krzywa nie odwzoruje 4 okien, użyć Rule table. Obie obecne automatyzacje zostają wyłączone.
- Rule table + Charger source priority: Zenek i Genek TAK; docs SA pokazują w przykładach tylko Output source priority/Use timer — potwierdzić w apce przy ustawianiu.
- Weekend/święta: SA bez warunku dnia tygodnia/świąt (obaj) → do HA Workday profil codzienny.
