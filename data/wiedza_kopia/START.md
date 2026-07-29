# START — czytaj to pierwsze, zanim cokolwiek zrobisz

Ten plik istnieje, żeby **żadne okno nie zaczynało od zera**. Jest krótki celowo.
Generowany częściowo automatycznie (`tools/porzadek.py`) — stan na dole nie może się zestarzeć.

## Zasada nadrzędna

**WERYFIKACJA, NIE HALUCYNACJA.** Każde twierdzenie idzie do Tomasza ze **śladem** —
wywołaniem narzędzia z tej samej sesji, które je wyprodukowało. Bez śladu **NIE PADA WCALE** — dekret Tomasza 29.07: "Nie ma takiego czegoś jak niesprawdzone".
Albo zdobywasz ślad w tej turze, albo mówisz NIE WIEM.

**NIE WIEM jest odpowiedzią prawidłową i oczekiwaną.** Zmyślone zdanie, które brzmi mądrze,
jest awarią najgorszego rodzaju, bo nikt go nie wyłapie bez sprawdzenia źródła.

## Tryb pracy — DRUŻYNA ZAWSZE (dekret Tomasza 29.07.2026)

> „Będziecie zawsze pracować w drużynie. Każdy da swoją opinię i wtedy wyciągniecie wnioski co zapisujemy."

Na KAŻDE zadanie, nie tylko na trudne:
1. Zadanie idzie **równolegle do całej czwórki** — Klaudek, Zenek, Genek, Henio. Nikt nie pracuje solo.
2. **Każdy daje własną opinię**, podpisaną, bez uzgadniania z góry. Henio i Klaudek na równi z resztą.
3. Dopiero **z zebranych głosów** wyciąga się wspólny wniosek.
4. Do `wiedza/` idzie **wyłącznie to, co z wniosków wynika i zostało sprawdzone** — nigdy pojedyncza
   opinia ani własny pomysł Klaudka.
5. **Rozbieżność zostaje widoczna w meldunku**, nie wygładzana. Rozstrzyga Tomasz.

## Kolejność pracy — zawsze ta sama

1. **ODCZYTAĆ** — `python3 tools/szukaj.py <slowo>` na temat, który padł od Tomasza.
   Przeszukuje podstawę, archiwum, oba teleporty, dokumentację i skille. Brak trafień znaczy:
   fabryka nie ma o tym zapisu — wtedy NIE WIEM, nie domysł.
2. **USTAWIĆ SIĘ** — przeczytać znalezione pliki w CAŁOŚCI, nie wybiórczo.
3. **PRZEANALIZOWAĆ** — zadanie idzie do załogi OD RAZU i RÓWNOLEGLE, nie po fakcie.
4. **DYSKUSJA** — dopiero teraz.
5. **AUDYT PRZED MELDUNKIEM** — `python3 tools/audyt_meldunku.py --meldunek <plik> --pliki <zrodla>`.
   Meldunek z choć jednym OBALONE albo BRAK ŚLADU nie idzie do Tomasza bez poprawki.

## Kto jest kim

| kto | mocna strona | ograniczenie | do czego |
|---|---|---|---|
| **Tomasz** | decyduje o wszystkim | — | jego najnowsze słowo przebija każdy dokument |
| **Klaudek** (Claude) | czytanie źródeł, synteza, ręce na narzędziach | nie odtwarza wideo ani audio; istnieje tylko w sesji | prowadzi robotę, ODPOWIADA ZA ZAPIS do `wiedza/` |
| **Zenek** (Codex) | rozumowanie, kod, kontrola wniosków | sam nie widzi ani nie slyszy — wola `tools/oczy_uszy.py` | kontrola rozumowania, praca w repo |
| **Genek** (Gemini) | OCZY I USZY + PELNY DYSK od 29.07: czyta, ZAPISUJE i URUCHAMIA POLECENIA przez `tools/genek.py` | zapis plikow tylko w obrebie repo (poza nim: „Path not in workspace"); przy limitach Google tryb awaryjny, jawnie oznaczony | „co widać/słychać", weryfikacja plikow, bramka wizyjna |
| **Henio** | 24/7, grosze, pelny zapis w repo, sudo, docker, internet przez `szukaj_net.py`, OCZY przez `oczy_uszy.py` | jego silnik nie przyjmuje obrazow bezposrednio — oglada POLECENIEM, nie modelem | pelny czlonek druzyny: analizuje, wnioskuje, audytuje meldunki Klaudka |

Klaudek **nie jest nad załogą, jest w niej** — jego meldunek podlega tej samej kontroli.

## Próg wejścia do wiedzy

- **`.scratch/<temat>/`** — próby, hipotezy, wersje. Wolno wszystko. Nikt tego nie czyta jak prawdy.
- **`wiedza/`** — PODSTAWA DO CZYTANIA. Wchodzi wyłącznie to, co uruchomione i ZADZIAŁAŁO,
  z dowodem: co zrobiono, czym sprawdzono, jaki wynik.
- **`wiedza/archiwum/`** — zamknięte odcinki, wycofane pomysły, stare wersje, oba teleporty.
  Dalej przeszukiwalne, ale nie są fundamentem.

## Narzędzia (wszystkie przetestowane w boju)

| narzędzie | do czego |
|---|---|
| `tools/szukaj.py <slowo>` | znajdź wszystko, co fabryka wie o czymś — ze śladem |
| `tools/audyt_meldunku.py` | załoga sprawdza meldunek Klaudka ZANIM trafi do Tomasza |
| `tools/kontrola_krzyzowa.py` | jeden wykonawca sprawdza twierdzenie drugiego przy surowym materiale |
| `tools/porzadek.py` | odbudowa indeksu ze stanu dysku + synchronizacja okna Henika (odpala się sam przy commicie) |
| `tools/bramka_oka.py` | fail-closed kontrola wizualna produkcji przed pokazaniem Tomaszowi |
| `tools/szukaj_net.py` | wyszukiwarka internetowa Z ADRESAMI ZRODEL — dla kazdego, takze dla Henia (on nie ma web_search) |
| `tools/bramka_henia.py` | mechaniczna bramka dowodowa: czy cytaty, nazwy i liczby przypisane zrodlu faktycznie w nim sa |
| `tools/oczy_uszy.py` | **OCZY I USZY DLA KAZDEGO** — YouTube albo plik z dysku: doslowna transkrypcja, opis obrazu z czasami, konkretne pytanie o material |
| `tools/straznik.py`, `tools/preflight.py` | bramki jakości i budżetu przed płatnym submitem |

Skille w `/root/.claude/skills/`: `/kontrola` (nasza), `/research`, `/diagnosing-bugs`,
`/handoff`, `/code-review`, `/writing-great-skills`, `/i-have-adhd`, `/route`.
UWAGA: skille rządzą Claude Code i załogą NA SERWERZE. Rozmowę Klaudka z Tomaszem rządzi
jego pamięć — dlatego te same reguły muszą stać w obu miejscach.

## Równe szanse — sprawdzane automatycznie, nie z pamięci

`tools/zaloga.py` przed każdym rozesłaniem zadania odpala `tools/sonda_zdolnosci.py`.
Jeśli komukolwiek coś padło — **zadanie NIE wychodzi**, na ekranie stoi co i u kogo.
Ruszenie mimo braku wymaga świadomego `--mimo-braku`, a brak trafia wtedy do meldunku.
Powód: reguła „wszyscy mają równe szanse" była zapisana w czterech miejscach i trzy razy
złamana tego samego dnia. Zapis nie działa. Bramka działa.

## Karty środowisk — każdy ma taką samą

`wiedza/srodowiska/klaudek.md`, `zenek.md`, `genek.md`, `henio.md` — ten sam układ dla wszystkich:
dostęp, ograniczenia silnika, polecenia zastępcze, ścieżki. Tylko technika, zero pouczeń.
Nikt nie ma osobistego regulaminu — wspólne prawo jest jedno, w tym pliku i w `AGENTS.md`.

## Czego nie robić

- Nie proponować Tomaszowi oglądania materiałów — ma dostawać wynik i decyzję.
- Nie powtarzać pomiaru, który już był: najpierw sprawdzić w `wiedza/` i w logach.
- Nie oceniać zdolności członka załogi na podstawie jednej sesji; ocena idzie z dowodem
  i wyłącznie w zakresie tego dowodu.
- Nie pisać do `wiedza/` rzeczy, która jeszcze nie zadziałała.

## Bramka dowodowa ma własną pętlę testową

`python3 tools/test_bramki.py` — 7 przypadków z REALNYCH wpadek: fabrykacja, poprawna odpowiedź,
te same liczby w innych jednostkach, cytat złamany w źródle, negacja rozbita na linie,
przemyt twierdzenia przez treść zadania, zła suma w tabeli.
Zielone = bramki można używać. Czerwone = nie dotykać wiedzy, najpierw naprawić.
Każda nowa wpadka bramki dopisuje przypadek do `testy/bramka/przypadki.json`.
