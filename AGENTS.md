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
