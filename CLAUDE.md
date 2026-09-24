# CLAUDE.md — rod-ai-studio

Claude Code czyta ten plik automatycznie. Cały regulamin załogi stoi w AGENTS.md — importuję go tutaj,
żeby nie było dwóch wersji prawa.

@AGENTS.md

## Start sesji

Zacznij od `wiedza/START.md` — zasada nadrzędna, kolejność pracy, kto jest kim, jakie są narzędzia.
Spis całej wiedzy: `wiedza/INDEX.md` (generowany z dysku, nie edytować ręcznie).
Szukanie: `python3 tools/szukaj.py <slowo>` — przeszukuje wiedzę, archiwum i oba teleporty.

TELEPORT_fabryka.md i /root/TELEPORT_HA.md to ARCHIWUM (127 KB i 43 KB) — NIE czytać na starcie,
przeszukiwać wyszukiwarką.

## PRAWO POLSKIE — Lex-Machina (dekret 22.09.2026, D-0455)
Każdą sprawę prawną (pisma do Taurona/PZD/gminy, uchwały, RODO, umowy, opłaty, spory) zaczynaj od wczytania `/root/.claude/skills/prawny-router-v3/SKILL.md` i wykonaj HARD GATE (`/root/.claude/skills/shared/PRAWO-HARDGATE.md`) PRZED każdym cytatem przepisu lub sygnatury: weryfikacja online w tym samym kroku (api.sejm.gov.pl/eli → tekst jednolity przez `/references`; saos.org.pl dla sygnatur), ślad `✅ [VER: źródło, data]`. Brak numeru artykułu > błędny numer.
Mapa ścieżek skilli: `shared/` = `/root/.claude/skills/shared/`; `references/`, `modules/`, `assets/` = podkatalog bieżącego skilla; operacja `view` = Read z absolutną ścieżką. Allowlista domen z claude.ai NIE dotyczy Claude Code (WebFetch/curl działa). Kanał maszynowy isap.sejm.gov.pl jest martwy (pętla 302) — używać api.sejm.gov.pl/eli. Konektor `mcp-isap` w .mcp.json (search_acts, get_act, get_act_text). Orzeczenia (SAOS) w wersji stabilnej 8.09 mają otwarty błąd #37 — sygnatury sprawdzać ręcznie na saos.org.pl do czasu aktualizacji.

## ZASADA D-0522 (23.09.2026): kazdy wygenerowany obraz/zdjecie do produkcji -> NATYCHMIAST na Telegram Tomasza (tools/tg_foto.py <plik> "podpis"), pojedynczo, na biezaco.

## ZASADA (24.09.2026): przed kazdym platnym krokiem czytaj wiedza/MOZLIWOSCI_ZALOGI.md i pytaj zaloge o darmowa droge (obrazy AI = Zenek za darmo).
