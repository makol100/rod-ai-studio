> **NOWE OKNO? ZACZNIJ OD `wiedza/START.md`** — zasada nadrzędna, kolejność pracy, kto jest kim, jakie narzędzia.

# AGENTS.md — rod-ai-studio

Repozytorium fabryki rolek AI dla ROD im. Józefa Lompy w Woźnikach.
Pipeline: scenariusz → TTS → obrazy → montaż ffmpeg → publikacja.

## Agent skills

### Issue tracker

Issues i specyfikacje żyją jako pliki markdown pod `.scratch/<feature>/` w tym
repozytorium (wariant local markdown — `gh` CLI nie jest tu zainstalowany).
Patrz `docs/agents/issue-tracker.md`.

### Domain docs

Układ jednokontekstowy — `CONTEXT.md` w korzeniu i `docs/adr/` na decyzje
architektoniczne; oba powstają dopiero wtedy, gdy są realnie potrzebne.
Patrz `docs/agents/domain.md`.

## Zasada dowodu (obowiązuje całą załogę)

Twierdzenie trafia do meldunku razem ze **śladem** — wywołaniem narzędzia z tej
samej sesji, które je wyprodukowało. Bez śladu NIE IDZIE WCALE. Dekret Tomasza 29.07: "Nie ma takiego czegoś jak niesprawdzone".
Albo zdobywasz ślad teraz, albo mówisz NIE WIEM.

Zdanie kolegi (Zenek, Genek, Henik, Klaudek) jest hipotezą. Liczbę rozstrzyga
API, zawartość pliku rozstrzyga grep, stan usługi rozstrzyga jej odpowiedź.

**NIE WIEM** jest odpowiedzią prawidłową i oczekiwaną.

Zlecenie do załogi jest domyślnie KONTROLNE: surowy materiał + jedno pytanie rozstrzygalne.
Autor nie sprawdza sam siebie — dotyczy też meldunków Klaudka.

Procedura: skill `/kontrola`. Kontrola krzyżowa: `tools/kontrola_krzyzowa.py`.

## Zanim odpowiesz na temat, którego nie znasz na pamięć

Uruchom wyszukiwarkę wiedzy — jedno słowo Tomasza, jedno polecenie:

    python3 tools/szukaj.py <slowo> [slowo2]

Przeszukuje wiedza/ (w tym eksport pamięci Klaudka: PAMIEC_INFRASTRUKTURA.md), docs/,
AGENTS.md, podręcznik dyżurnego i skille. Ignoruje wielkość liter i polskie znaki.
Zwraca plik + numer linii + treść — czyli ŚLAD, nie streszczenie.

Brak trafień znaczy: fabryka NIE MA o tym zapisu. Wtedy odpowiedź brzmi NIE WIEM,
a nie domysł.

Henik czyta tę samą wiedzę w swoim oknie: /home/hermes/fabryka/data/wiedza_kopia/

## Próg wejścia do wiedzy (dekret Tomasza, 29.07.2026)

> „Jeżeli coś nie zadziała i będziemy to dalej poprawiać — NIE wpisujemy tego, pilnujemy się.
> Jeżeli coś naprawdę zadziała i będzie dobre — wtedy to zapisujemy i mamy podstawę do czytania."

Dwa miejsca, dwa różne progi:

- **`.scratch/<temat>/`** — robota w toku: próby, hipotezy, plany, wersje, wszystko co jeszcze
  nie udowodniło, że działa. Tu wolno wszystko. Tego nikt nie czyta jak prawdy.
- **`wiedza/`** — PODSTAWA DO CZYTANIA. Wchodzi wyłącznie to, co zostało URUCHOMIONE
  i ZADZIAŁAŁO. Każdy wpis niesie: co zrobiono, czym to sprawdzono, jaki był wynik.

Odrzucone, wycofane i niedokończone pomysły nie zostają w `wiedza/` jako fundament —
idą do `.scratch/` albo dostają nagłówek `STATUS: WYCOFANE` z datą i powodem.

**Odpowiedzialny za zapis: Klaudek.** On decyduje, kiedy coś przekroczyło próg i wpisuje to
z dowodem. Zenek, Genek i Henik zgłaszają mu ustalenia — nie piszą do `wiedza/` sami.

## Dostęp do historii — bez ograniczeń dla całej załogi

Nikt nie zaczyna od zera. Przed analizą i przed dyskusją każdy czyta:

- `wiedza/INDEX.md` — spis całości, generowany z dysku
- `python3 tools/szukaj.py <slowo>` — przeszukuje wiedzę, dokumentację, skille ORAZ oba teleporty
- Henik ma to samo w swoim oknie: `/home/hermes/fabryka/data/wiedza_kopia/`
  (wiedza + `archiwum/` z teleportami)
- Genek nie ma dostępu do dysku — kto go pyta, ten dokłada mu surowy materiał do zlecenia

Kolejność jest zawsze ta sama: **odczytać → ustawić się → przeanalizować → dopiero dyskusja.**

## Drużyna zawsze (dekret Tomasza 29.07.2026)

Każde zadanie idzie równolegle do całej czwórki (Klaudek, Zenek, Genek, Henio). Każdy daje własną,
podpisaną opinię. Wniosek powstaje z zebranych głosów, nie z jednej głowy. Do `wiedza/` trafia
wyłącznie to, co z wniosków wynika i zostało sprawdzone. Rozbieżność zostaje w meldunku widoczna —
rozstrzyga Tomasz. Szczegóły: `wiedza/START.md`.

## Manifest przed drogimi narzędziami

Zanim uruchomisz kosztowne oczy, model albo generację — przeczytaj manifest i zapisy zadania,
które już leżą na dysku. Odpowiedź często tam jest, za darmo. (Reguła urodziła się przy WD_0001
i obowiązuje każdego, nie tylko dyżurnego.)

## Format odpowiedzi na zadanie otwarte

1. **POTWIERDZONE** — konkretne fragmenty źródła z cytatem i miejscem. Ta sekcja nie może być pusta.
2. **HIPOTEZY** — własne wnioski, wyraźnie oznaczone jako wnioski.
3. **NIE WIEM** — czego nie dało się ustalić.

Jeśli nic nie przechodzi weryfikacji, odpowiedź brzmi: „Nie mogę wydać rzetelnego werdyktu —
nic z zamierzonej analizy nie przeszło weryfikacji narzędziami." To odpowiedź PRAWIDŁOWA.

## Bramka dowodowa

Odpowiedź o źródle przepuść przez `python3 tools/bramka_henia.py --odpowiedz PLIK --zrodlo ŹRÓDŁA`.
Sprawdza mechanicznie, czy cytaty, nazwy i liczby przypisane źródłu naprawdę w nim są, i czy sumy
w tabelach się zgadzają. Dotyczy każdego, kto pisze o źródle — Klaudka tak samo jak reszty.

## Karty środowisk

`wiedza/srodowiska/` — jedna karta na członka załogi, ten sam układ dla każdego: czym się loguje,
co ma, czego jego silnik nie potrafi i jakim poleceniem to obchodzi. Wyłącznie technika.
Wspólne prawo stoi tutaj i w `wiedza/START.md` — identyczne dla wszystkich.

## GENEROWANIE OBRAZU — CO POTRAFI GENEK (od 01.08.2026)

**Genek generuje obrazy sam, swoim kluczem — i to jest DROGA GŁÓWNA.**
Decyzja Tomasza: „Gienek nano banana 2" + „Fal.ai jako alternatywa w przypadku awarii Gienka".
Powód: „Na Was wydaje pieniądze, więc nie interesują mnie generowania na próby" — Genek generuje
ponad dwa razy taniej niż fal.ai, więc próba przestaje być luksusem.

Model kanoniczny: **`gemini-3.1-flash-image`** (Nano Banana 2), ~0,067 USD za obraz 1K.
Najtańszy: `imagen-4.0-fast-generate-001` — 0,02 USD. Najlepszy: `gemini-3-pro-image` — 0,134 USD (2K).
Wywołanie: `generateContent` dla `gemini-*-image`, `predict` dla `imagen-*`.
`batchGenerateContent` = 50% taniej na serie niepilne.

**FAL.AI (`fal-ai/nano-banana-pro`, ~0,15 USD) tylko przy AWARII Genka** — 429/503, wyczerpany
limit dobowy, L4. Nie domyślnie.

Pełna tabela, zastrzeżenia i to, czego NIE zmierzyliśmy: **`wiedza/GENEROWANIE_OBRAZU.md`**.

**Skoro Genek to potrafi — przy zadaniach wymagających obrazu proponujcie jego drogę, nie fal.ai.**


## GENEROWANIE OBRAZU — KAŻDY MUSI TO WIEDZIEĆ

Decyzja Tomasza 01.08.2026: **droga główna to GENEK, model `gemini-3.1-flash-image`**
(Nano Banana 2), ~0,067 USD za obraz. **fal.ai (`fal-ai/nano-banana-pro`, ~0,15 USD) TYLKO
przy awarii Genka** — 429/503, wyczerpany limit dobowy, L4.

Inne modele na kluczu Gemini: `imagen-4.0-fast-generate-001` (0,02 USD, najtańszy),
`gemini-3-pro-image` / `nano-banana-pro-preview` (0,134 USD 2K, 0,24 USD 4K — wersje ostateczne),
`gemini-3.1-flash-lite-image`, `imagen-4.0-generate-001`.
Wywołanie: `generateContent` dla rodziny `gemini-*-image`, `predict` dla `imagen-*`.
`batchGenerateContent` = 50% taniej na serie niepilne.

Pełna tabela i zastrzeżenia: `wiedza/GENEROWANIE_OBRAZU.md`.
Powód decyzji, słowami Tomasza: „Na Was wydaje pieniądze, więc nie interesują mnie
generowania na próby" — tańsze próby = wolno próbować.
