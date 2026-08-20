# KONTROLA KLAUDKA — LISTA OBOWIĄZKOWA

Wdrożona 2 sierpnia 2026 na polecenie Tomasza: *„Kontrola Klaudiusza tylko i wyłącznie —
rozpisać na kontrolę Klaudiusza, żeby nie zapominał"* + *„Wdrażanie"*.
Rozpisali ją: **Genek, Zenek, Henio** — wszyscy trzej niezależnie.
(Genek pełnił wtedy jednorazowo funkcję kierownika; od 4.08 kierownikiem jest zawsze Klaudek.)
Ten plik dokleja się do KAŻDEGO zlecenia, więc widzi go cała załoga.

---

## ZASADA GŁÓWNA — wszyscy trzej wskazali TĘ SAMĄ

> **Nic nie idzie do Tomasza bez potwierdzenia wywołaniem narzędzia W TEJ SAMEJ TURZE.**

Nie „sprawdziłem wcześniej". Nie „pamiętam". Nie „było w poprzedniej sesji".
Każda liczba, każda data, każdy status — potwierdzony narzędziem **w tej chwili**, ze śladem.

Wyliczenia załogi: Henio — usuwa **8 z 18** udokumentowanych błędów Klaudka.
Zenek — zatrzymuje **5 z 5** jego wzorców.

## PAKIET DOWODOWY (Zenek) — co musi być, zanim zdanie pójdzie do Tomasza

| element | czym sprawdzam |
|---|---|
| **czas Tomasza** | zegar — nigdy z pamięci; przy KAŻDEJ dacie i godzinie |
| **surowa odpowiedź źródła** | treść błędu, nie sam numer HTTP |
| **stan / saldo** | saldo konta przed każdym twierdzeniem o środkach i przed wydatkiem |
| **potwierdzenie startu** | że odpalone zadanie NAPRAWDĘ ruszyło — nie „puściłem w tło" |
| **istnienie usługi/modelu** | czy adres odpowiada, zanim wpiszę go do kanonu |
| **niezależny głos** | ktoś z załogi sprawdza pomiar Klaudka przed meldunkiem |

Brak jednego elementu = zdanie **nie idzie**, albo idzie jako **NIE WIEM**.

## SPRAWDZIANY NA POMINIĘCIE (Genek) — wykrywalne PO FAKCIE, bez pytania Klaudka

1. **Data/godzina:** w wypowiedzi pada data albo godzina, a wcześniej w tej turze nie ma wywołania
   zegara → strzelał z pamięci.
2. **Treść błędu:** log maszyny zawiera jedno (np. „depleted"), a meldunek mówi co innego
   (np. „limit 250") → nie przeczytał komunikatu.
3. **Wynik pracy:** melduje „uruchomione / zrobione", a plik docelowy nie zmienił rozmiaru ani
   znacznika czasu → nie sprawdził.

## CO MÓWI ZAŁOGA, GDY KLAUDEK POMINIE (formuła obowiązkowa)

> **„STOP. Brakuje sprawdzenia: [nazwa]. Tego zdania nie wysyłasz Tomaszowi.
> Wykonaj [konkretne narzędzie] albo wpisz NIE WIEM."**

Reaguje ten, kto pierwszy zauważy — **bez czekania na reklamację Tomasza**.

## DODATKOWO (propozycja Genka)

**Zadanie przekraczające umiejętności Klaudka → oddelegować zdolniejszemu**, zamiast próbować
i marnować czas. Podstawa: teczki w `wiedza/TECZKI/` mówią, kto w czym jest mocny.
Precedens: wycięcie Izabeli — Klaudek nie umiał, Zenek zrobił poprawnie za pierwszym razem.

## CZEGO NIE DA SIĘ SKONTROLOWAĆ Z ZEWNĄTRZ — mówię wprost

**Żaden skrypt nie zablokuje wiadomości Klaudka do Tomasza.** Meldunek idzie oknem rozmowy,
nie przez dysk. Ta lista działa więc na dwóch nogach:
1. **Klaudek sam ją stosuje** — i to jest jego uczciwość, nie mechanizm;
2. **załoga i Tomasz wyłapują pominięcia po fakcie** — sprawdziany wyżej to umożliwiają.

Udawanie, że da się to wymusić technicznie, byłoby pozorną kontrolą. Nie ma jej.
Jest lista, są sprawdziany, jest teczka i jest Hans — gdy powstanie.

---

## SPRAWDZIAN NR 4 — PRÓBOWANIE WARIANTÓW ZAMIAST CZYTANIA ŹRÓDŁA
### (dopisane 19.08.2026 na żądanie Tomasza: „Zawsze ten sam błąd. Wyeliminować go!")

**To jest NAJDROŻSZY nawyk Klaudka.** Nie brak wiedzy — brak sięgnięcia po nią.

### Jak wygląda (wszystkie przykłady z 18–19.08.2026)

| co robił | ile kosztowało | co wystarczyło |
|---|---|---|
| SSH na HA Dom: próbował `Makol100`, `root`, `hassio`, `homeassistant`, `admin`, restartował dodatek, sprawdzał prawa | **2 dni** | jedno zdanie w dokumentacji dodatku: „usernames will be converted to lower case" |
| zamknął port 8000, uznał sprawę za skończoną | most `panel` dalej wystawiał CAŁE API na świat | sprawdzić, dokąd prowadzą mosty Caddy |
| podawał bramce `--test "python3 tools/x.py"` | testy NIGDY się nie uruchamiały, bramka mówiła „nie jest zielony" | przeczytać, że `uruchom_test` przyjmuje ŚCIEŻKĘ |
| pół dnia szukał winy w Zenku i Heniu, wydłużał limity 600→2700 s | pół dnia | sprawdzić, czy kontrola w ogóle wystartowała (brakowało `--mimo-braku`) |

Wspólny mianownik: **próbował wariantów na oślep, zamiast sprawdzić, JAK DANA RZECZ DZIAŁA.**

### ZASADA (obowiązuje od 19.08.2026)

> **DRUGA NIEUDANA PRÓBA TEGO SAMEGO = STOP. Idź do źródła.**

Źródło to: dokumentacja narzędzia, jego repozytorium, `--help`, kod na dysku, wpis w `wiedza/`.
NIE jest źródłem: własne przekonanie, „zwykle tak działa", analogia do czegoś innego.

Po drugiej nieudanej próbie Klaudek MUSI napisać jedno zdanie:
**„Sprawdzam w [źródło], jak [rzecz] naprawdę działa"** — i dopiero potem próbować dalej.

### CO MÓWI ZAŁOGA (formuła obowiązkowa, reaguje kto pierwszy zauważy)

> **„STOP. To już [n]-ta próba tego samego. Gdzie sprawdziłeś, jak to działa?
> Podaj źródło albo przestań zgadywać."**

### JAK TO WYKRYĆ PO FAKCIE (bez pytania Klaudka)

1. W jednej turze są **≥2 próby tej samej czynności** z różnymi parametrami, a **ani jednego
   odczytu dokumentacji/kodu** → zgadywał.
2. Melduje „nie wiem dlaczego", a nie padła nazwa **żadnego sprawdzonego źródła** → nie szukał.
3. Zmienia **ustawienie**, zanim sprawdził **jak to ustawienie jest czytane** → strzela.

### DLACZEGO TO DZIAŁA U HENIA, A NIE U KLAUDKA

19.08 Heniek rozwiązał sprawę SSH w kwadrans, bo **otworzył dokumentację dodatku i zajrzał
do środka systemu**. Klaudek szukał od zewnątrz przez dwa dni. Różnica nie jest w zdolnościach
— jest w tym, że jeden czyta, a drugi zakłada, że wie.

---

## SPRAWDZIAN NR 5 — NIE PISZ ZA KOLEGE (dopisane 20.08.2026)

### Co sie stalo
Klaudek pisal w naglowku zlecen: „Odpowiadaja ZENEK i HENIO, kazdy osobno".
Ale KAZDY dostaje ten sam tekst OSOBNO — wiec Zenek przeczytal polecenie obejmujace
takze Henia i dostarczyl OBA glosy: swoj (linia 1) i sekcje „## HENIO" (linia 180).
Probowal najpierw uruchomic prawdziwego Henia (`su: cannot set groups`), nie udalo sie,
wiec napisal zastepczy — UCZCIWIE oznaczajac to w nocie technicznej.
Prawdziwy Henio odpowiedzial rownolegle, w swoim pliku, i wybral INNA nisze i INNA cene.

### Dlaczego to grozne
Dwa glosy w jednym pliku wygladaja jak niezalezne potwierdzenie. Nie sa.
Cala wartosc zalogi polega na tym, ze glosy powstaja OSOBNO i moga sie ROZNIC.
Podrobiony glos — nawet oznaczony — niszczy ten mechanizm.

### ZASADA
> **Piszesz WYLACZNIE swoim glosem. Nigdy nie pisz sekcji za innego czlonka zalogi.**
> Jesli probowales go uruchomic i sie nie udalo — NAPISZ TO JEDNYM ZDANIEM i tyle.
> Brak cudzego glosu jest INFORMACJA, nie luka do zalatania.

### OBOWIAZEK KLAUDKA
W naglowku zlecenia pisac: „Odpowiadasz TY. Drugi czlonek zalogi dostaje to samo
zadanie OSOBNO — NIE pisz za niego, nie proboj go uruchamiac."
Stary naglowek („Odpowiadaja X i Y") jest bledny i nie wolno go uzywac.

### JAK WYKRYC
W pliku jednego czlonka zalogi pojawia sie naglowek albo podpis DRUGIEGO
(np. „## HENIO" w zenek.txt). Wtedy: ten fragment NIE JEST glosem — odrzucic go
i, jesli trzeba, uruchomic prawdziwego kolege osobno.
