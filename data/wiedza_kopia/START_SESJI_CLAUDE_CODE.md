# START SESJI CLAUDE CODE — co ładuje się automatycznie (29.07.2026)

Powód powstania: film „Anthropic's New Rules Break Most Claude Code Setups" (Eric Tech) obejrzała cała
załoga. Werdykt 2:1 za działaniem. Wszystkie trzy zarzuty potwierdzone pomiarem na naszych plikach.

## CO BYŁO ŹLE

1. **Regulamin nie docierał do Claude Code.** Zenek sprawdził dokumentację i dysk: Claude Code czyta
   `CLAUDE.md`, a my mieliśmy w repo tylko `AGENTS.md`. Zweryfikowane: `CLAUDE.md` w repo NIE ISTNIAŁ.
   Cała praca nad regulaminem, łącznie z poleceniem startu od `wiedza/START.md`, była dla niego niewidoczna.
2. **Teleport ładował się na starcie.** Genek wskazał, Klaudek zmierzył: `TELEPORT_fabryka.md` = 130 445 bajtów,
   a w `/root/.claude/CLAUDE.md` stało „czytać na starcie".
3. **216 KB skilli przy każdym zadaniu.** Henio policzył katalog po katalogu.

## CO ZROBIONE

| zmiana | dowód |
|---|---|
| `CLAUDE.md` w repo, 15 linii, importuje `@AGENTS.md` | plik istnieje, import wskazuje na istniejący AGENTS.md |
| teleporty zdjęte ze startu, oznaczone jako ARCHIWUM do przeszukiwania | wpis w `/root/.claude/CLAUDE.md` zmieniony |
| konstytucja startu: `wiedza/START.md` → ogon DECYZJI → narada czwórki przez `tools/zaloga.py` | jw. |
| 3 rzadko używane skille wyłączone, odwracalnie | 216 KB → **108 KB**, spadek o połowę |

Wyłączone leżą w `/root/.claude/skills_wylaczone/`: `setup-matt-pocock-skills` (zadanie jednorazowe,
wykonane), `writing-great-skills` (materiał referencyjny, użyty raz przy pisaniu `/kontrola`),
`i-have-adhd` (styl odpowiedzi, rzadko potrzebny na serwerze). Przywrócenie = przeniesienie z powrotem.

Aktywne: `code-review`, `diagnosing-bugs`, `handoff`, `kontrola`, `research`, `route`.

## CZEGO NIE UDAŁO SIĘ ZROBIĆ
`/doctor` w pełnej wersji wymaga sesji interaktywnej — przez mostek MCP nie startuje („Execution error").
Podkomenda `claude doctor` sprawdza tylko instalację: brak problemów, wersja 2.1.220.
Wybór skilli do wyłączenia oparty na analizie załogi, nie na pomiarze użycia. Do sprawdzenia przy okazji
pracy w sesji interaktywnej.
