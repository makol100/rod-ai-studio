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
