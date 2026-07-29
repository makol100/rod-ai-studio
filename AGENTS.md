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
samej sesji, które je wyprodukowało. Bez śladu idzie z widoczną etykietą
**[NIESPRAWDZONE]**.

Zdanie kolegi (Zenek, Genek, Henik, Klaudek) jest hipotezą. Liczbę rozstrzyga
API, zawartość pliku rozstrzyga grep, stan usługi rozstrzyga jej odpowiedź.

**NIE WIEM** jest odpowiedzią prawidłową i oczekiwaną.

Procedura: skill `/kontrola`. Kontrola krzyżowa: `tools/kontrola_krzyzowa.py`.
