# ZADANIE KONTROLNE: ocena TencentDB Agent Memory pod pamiec Klaudka/fabryki

WAZNE DLA ZENKA (Codex): NIE URUCHAMIAJ narzedzi, NIE odpalaj zaloga.py, NIE tworz plikow, NIE clone'uj repo. TYLKO OCENA TEKSTEM. Podpisany glos.

Kazdy (Zenek, Henio) podpisany glos + werdykt. Rozbieznosc zostaje. Decyduje Tomasz.

## CO OCENIAMY
Repo: **Tencent/TencentDB-Agent-Memory** (MIT, ~7800 gwiazdek, maj 2026). W pelni lokalny system pamieci dla agentow AI (zero external API domyslnie).
Zrodla: film YT (autor pobral kod, sprawdzil configi i arytmetyke tabeli — mowi ze "wiekszosc sie zgadza, JEDNA linia w tabeli benchmarku NIE") + README repo + artykuly (marktechpost, medium).

### Architektura (z README + artykulow)
- **Pamiec KROTKOTRWALA (biezace zadanie), symboliczna:** pelne outputy narzedzi -> pliki `refs/*.md` (offload z okna kontekstu); stan zadania zakodowany jako **graf MERMAID** (kilkaset tokenow) trzymany w kontekscie; agent rozumuje po grafie, a gdy potrzebuje szczegolu -> drill-down po `node_id` do surowego pliku. 3 warstwy: `refs/*.md` (surowe) -> `jsonl` (step summaries) -> Mermaid canvas (top). Progi z filmu: 50% okna = kompresja lagodna, 85% = agresywna; graf capped 20% budzetu, 4000 znakow.
- **Pamiec DLUGOTERMINOWA (co agent wie o userze), warstwowa:** piramida semantyczna 4-poziomowa **L0 Conversation** (surowy dialog) -> **L1 Atom** (fakty atomowe) -> **L2 Scenario** (bloki scen) -> **L3 Persona** (profil usera). Drill-down po `node_id`/`result_ref` zamiast plaskiego vector recall. Deklaruja pelna sledzsalnosc i bezstratne odtworzenie (deterministyczna sciezka od abstrakcji do surowego dowodu).
- **Retrieval:** hybrydowy BM25 + vector + RRF. Domyslnie lokalny **SQLite + sqlite-vec** (bez zewnetrznej bazy). Opcjonalny Tencent Cloud Vector DB.
- **Wyniki (integracja z OpenClaw):** WideSearch pass 33%->50% przy -61.38% tokenow; SWE-bench 58.4%->64.2%; AA-LCR 44.0%->47.5%; PersonaMem accuracy 48%->76%.
- **Stack/dystrybucja:** npm plugin dla OpenClaw ORAZ **obraz Docker dla HERMES** (lub instalacja manualna).

## NASZ KONTEKST (pamiec Klaudka)
Klaudek ma "drugi mozg" na VPS: `wiedza/` (dokumenty), INDEX/destylaty, teleport (`TELEPORT_fabryka.md`, `/root/TELEPORT_HA.md`), dzienniki. Kontekst przekazujemy briefami teleportu (wklejanie tekstu). Pamiec plikowa, lokalna — filozofia zbiezna z TencentDB.
KLUCZOWE: nasz **Henio to HERMES** (`su - hermes -c 'hermes -z ...'`). TencentDB ma **Docker dla HERMES** — czyli potencjalnie wpinalne wprost do naszego Henia.
Kontekst bolu: ta sesja MUSIALA sie kompaktowac (przepelnienie okna) — dokladnie problem, ktory TencentDB adresuje.

## PYTANIA ROZSTRZYGALNE (TAK/NIE + jak)
1. Graf Mermaid + drill-down po node_id (krotkotrwala) zamiast wklejania pelnych logow/historii — warto u nas? Rozwiazuje gubienie kontekstu przy dlugich sesjach?
2. Piramida L0->L3 (dlugoterminowa) vs nasz obecny `wiedza/` + teleport — co konkretnie zyskujemy, czy nasz system juz to pokrywa?
3. Integracja z HERMES (Docker) — skoro Henio=hermes: wpinamy TencentDB do niego? Realne, czy za duzo pracy/ryzyka?
4. Koszt/ryzyko: SQLite+sqlite-vec lokalny (tani). Jak swiezy/dojrzaly projekt (issues)? Sygnal "jedna linia tabeli sie nie zgadza" — powaznie traktowac?
5. WERDYKT per opcja: wdrozyc / podpatrzec sam KONCEPT (Mermaid+node_id) do naszego systemu / odrzucic. Jesli wdrozyc — co pierwsze (krotkotrwala czy dlugoterminowa)?

Zasada 27.07: najnizszy koszt; wyjatek gdy droga pewna. Zasada 17.07: sprawdzic issues, uczyc sie z cudzych bledow, czytac calosc. Sprawdzac u zrodla, nie ufac samemu README.
