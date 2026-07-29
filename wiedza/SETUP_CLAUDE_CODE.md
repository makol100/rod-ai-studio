# SETUP CLAUDE CODE — poprawki z 29.07.2026 (film Eric Tech + pomiar)

Powód: film „Anthropic's New Rules Break Most Claude Code Setups" obejrzała cała czwórka.
Zenek i Genek: DZIAŁAĆ. Henio: OBSERWOWAĆ. Trzy zarzuty sprawdzone na naszych plikach.

## 1. NAPRAWIONE — regulamin był NIEWIDOCZNY dla Claude Code
Zenek: „Claude Code czyta CLAUDE.md, nie AGENTS.md". Sprawdzone: `CLAUDE.md` w repo NIE ISTNIAŁ,
a `AGENTS.md` miał 115 linii. Cała nasza konstytucja — zasada dowodu, drużyna zawsze, próg wiedzy,
polecenie startu od `wiedza/START.md` — nie docierała do narzędzia, które miało ją wykonywać.
NAPRAWA: `CLAUDE.md` (14 linii) importuje `@AGENTS.md`. Jedna prawda, dwa wejścia:
Codex/Zenek czyta AGENTS.md natywnie, Claude Code czyta CLAUDE.md i podciąga to samo.

## 2. NAPRAWIONE — teleport zdjęty ze startu sesji
Genek: konfiguracja kazała czytać teleport na starcie. Zmierzone: **130 445 bajtów** (+ 43 KB teleportu HA).
NAPRAWA: w `/root/.claude/CLAUDE.md` start sesji = `wiedza/START.md`; teleporty oznaczone jako ARCHIWUM
przeszukiwane przez `tools/szukaj.py`. Przy okazji zaktualizowany opis narady: `tools/zaloga.py`, cała czwórka.

## 3. ODRZUCONE PO POMIARZE — skille nie obciążają kontekstu tak, jak zakładaliśmy
Henio policzył 216 KB skilli i przyjął za filmem, że „Claude Code wczytuje je wszystkie przy każdym żądaniu".
POMIAR OBALIŁ TĘ PRZESŁANKĘ. Kontekst zajmują wyłącznie OPISY skilli model-invoked:

| ładuje się zawsze | opis |
|---|---|
| code-review, diagnosing-bugs, kontrola, research, route | razem **1410 znaków ≈ 352 tokeny** na zadanie |

| tylko na wywołanie (zero kosztu) |
|---|
| handoff, i-have-adhd, setup-matt-pocock-skills, writing-great-skills |

Trzy skille, które Henio proponował wyłączyć, są dokładnie tymi, które i tak nic nie kosztują
(`disable-model-invocation: true`). Wyłączanie ich nie oszczędziłoby ani jednego tokena.
DECYZJA: nic nie wyłączamy. 352 tokeny to cena, której nie warto optymalizować.

## LEKCJA
Dwie z trzech rzeczy z filmu okazały się u nas prawdziwe i kosztowne, trzecia — nie. Różnicę zrobił pomiar,
nie autorytet filmu ani zgodność załogi. Henio miał rację co do liczby (216 KB), a mylił się co do skutku.
