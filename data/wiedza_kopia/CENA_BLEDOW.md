# CENA NASZYCH BŁĘDÓW — pomiar (29.07.2026)

Teza Tomasza: „Rolki kosztują tak różnie u nas, bo Wy wszyscy popełnialiście błędy".
Sprawdzone: **teza się potwierdza i da się ją wyrazić liczbą.**

Metoda: Henio przeszukał `wiedza/` i `wiedza/archiwum/` i wyciągnął udokumentowane przypadki
z cytatem i nazwą pliku. Klaudek przepuścił jego raport przez `tools/bramka_henia.py` i przeliczył sumę.

## UDOKUMENTOWANE STRATY Z WINY ZAŁOGI

| odcinek | strata | przyczyna |
|---|---|---|
| #10009 | 5.76 | kolizja okien — dwa okna zrobiły równolegle kanarka i batch |
| #10009 | 5.12 | import `_batch.py` wykonał submit 8 klipów BEZ zgody Tomasza (kod na poziomie modułu) |
| #10009 | 0.30 | k05 i k06 odrzucone — braki w promptach (pusta doniczka, złe wiaderko) |
| #10010 | 0.60 | 4 nieudane próby k04 — research praktyków zrobiony DOPIERO po awanturze |
| Awatar | 4.64 | duplikat Avatar PRO — brak sprawdzenia `tmux ls` + mtimes przed płatnym submitem |
| Awatar | 4.64 | Avatar PRO odrzucony — prompt karty bez wymogu kontaktu wzrokowego |
| Awatar | 0.20 | LatentSync zamiast modelu avatarowego — wybór po cenie zamiast po zamówieniu |
| #10010 | 0.30 | k02 v2 i v3 odrzucone — model uciekał od chwytu, poprawiany prompt zamiast metody „change only" (znalazł GENEK) |
| #10010 | 0.30 | k04_b i k06_b odrzucone — **VLM OSTRZEGAŁ i ostrzeżenie zignorowano**, koszt 3.49 → 3.79 (znalazł ZENEK) |
| **RAZEM** | **21.86** | |

AKTUALIZACJA po naradzie całej czwórki (29.07): pierwsza wersja tego zapisu miała 7 pozycji i sumę 21.26.
Zenek i Genek — każdy niezależnie — znaleźli po jednej BRAKUJĄCEJ pozycji po 0.30 USD (różne zdarzenia,
oba potwierdzone cytatem w DECYZJE_10010.md). Suma po korekcie: **21.86 USD**.
To jest dowód, po co jest cała czwórka: Henio + Klaudek dali 21.26, dopiero pełny skład domknął rachunek.

Dla skali: odcinek #10009 kosztował realnie ~13.17 USD, z czego **~10.88 to podatek od naszych błędów**.
Bez nich mieściłby się w limicie 12 USD z zapasem.

## WNIOSEK, KTÓRY Z TEGO WYNIKA
Rozrzut kosztów między odcinkami (5.12 → 8.38 → 13.17) NIE bierze się z różnej trudności materiału.
Bierze się z powtórek: kolizji równoległych okien, submitów bez zgody, generacji bez wcześniejszego
researchu i niepełnych specyfikacji. Najtańsza dźwignia kosztowa fabryki to nie tańszy model —
to nie powtarzanie własnych pomyłek.

## CO ZŁAPAŁA KONTROLA PRZY OKAZJI TEGO POMIARU
1. Bramka dowodowa zablokowała raport Henia: cytat skrócony wielokropkiem nie zgadzał się ze źródłem
   co do znaku (treść była prawdziwa — sprawdzone osobno greppem).
2. **Henio zsumował błędnie**: pozycje dają 21.26, on zadeklarował 18.76, wcześniej 19.06.
   Wyciągnął fakty bezbłędnie, arytmetykę pomylił. Ten sam wzorzec co zawsze: mocny w wydobyciu, słaby w rachunku.
3. Bramka tego NIE łapała — sprawdzała cytaty, nazwy i obecność liczb, nie działania na nich.
   Dopisana kontrola arytmetyki tabel. Pierwsza wersja liczyła wszystkie kwoty w dokumencie (także
   te wewnątrz cytatów) i dawała bzdurę 124.75 — zawężona do wierszy tabeli i przetestowana trzy razy:
   łapie błąd Henia, przepuszcza poprawną odpowiedź, nie robi fałszywego alarmu na poprawnej tabeli.

## NAJDROŻSZA LEKCJA Z TEGO RACHUNKU
Przy k04_b/k06_b bramka wizyjna **OSTRZEGAŁA** („nogi nie zwisają w dół") i ostrzeżenie zostało
zignorowane, bo pytania do niej były naprowadzające zamiast otwartych. Strażnik zadziałał — zawiódł
człowiek przy nim. To najdroższy wzorzec w całym zestawieniu: nie brak kontroli, tylko jej lekceważenie.
