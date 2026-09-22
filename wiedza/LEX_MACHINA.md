# LEX-MACHINA W FABRYCE (zainstalowane 22.09.2026, dekret D-0455 „Instaluj teraz. Mamy polskie prawo u siebie")

## Co to
33 skille prawa polskiego (GPL v3, github.com/michaleiatrak-star/Lex-Machina, wersja stabilna 8.09.2026) z twardą bramką antyhalucynacyjną:
**żaden przepis, numer Dz.U., stawka, termin ani sygnatura nie pada bez weryfikacji online w tym samym kroku** (ISAP/api.sejm.gov.pl/eli, SAOS, EUR-Lex). Brak numeru artykułu > błędny numer.

## Gdzie
- Skille: `/root/.claude/skills/` — `prawny-router-v3` (wejście: klasyfikacja sprawy, tryb PRAWNIK/LAIK), `prawo-polskie-v2` (mapa), `przewodnik-prawny-v2` (laik), `dr-01..dr-16` (dziedziny), `pisma-procesowe-v3`, `pisma-proste-v2`, `analizator-umow-v1`, `analizator-przepisow-v2`, `orzeczenia-sadowe-v2`, `analiza-sadowa-v6`, `audyt-systemu-v4`; biblioteka bramek `shared/` (PRAWO-HARDGATE, SYGNATURY, WERYFIKACJA-SLAD, HIERARCHIA-ZRODEL) — ścieżka kanoniczna `/root/.claude/skills/shared/`.
- Konektor ISAP: `mcp-isap` (npx @matematicsolutions/mcp-isap 1.3.0) w `/root/rod-ai-studio/.mcp.json` i `~/.claude.json`; narzędzia `search_acts`, `get_act`, `get_act_text`. Sprawdzone 22.09: ustawa o ROD = Dz.U. 2014 poz. 40 (tekst jednolity).
- Klon repo: `/root/lex-machina` (git pull po aktualizacje).

## Jak używać (Claude Code na VPS / załoga)
1. Sprawę zaczynać od `prawny-router-v3` (tryb LAIK dla działkowców, PRAWNIK dla pism zarządu).
2. Dziedziny ROD: `dr-08` (samorząd, prawo miejscowe — plany gmin, użytkowanie wieczyste), `dr-09` (energetyka — przyłącza Tauron, prawo budowlane), `dr-11` (RODO — kamery, monitoring), `dr-02` (KC — umowy, własność kabli), `dr-05` (KPA — organy, PZD jako stowarzyszenie), `dr-16` (pisma/strategia).
3. Każdy cytat przepisu → `get_act`/`get_act_text` z ISAP albo curl `https://api.sejm.gov.pl/eli/acts/DU/<rok>/<poz>`; sygnatury → saos.org.pl. Ślad `✅ [VER: źródło, data]` w odpowiedzi.
4. Pisma mają status DRAFT do akceptacji Tomasza. Lex-Machina = informacja prawna, nie porada.

## Akty kluczowe dla ROD (do weryfikacji w ISAP przy każdym użyciu)
- ustawa z 13.12.2013 o rodzinnych ogrodach działkowych — akt bazowy Dz.U. 2014 poz. 40; OBOWIĄZUJĄCY TEKST JEDNOLITY: Dz.U. 2021 poz. 1073 (obwieszczenie 21.05.2021; brak nowelizacji po t.j. — stan wg ELI 22.09.2026). Wzorzec cytatu: art. 30 ust. 2 ustawy z dnia 13 grudnia 2013 r. o rodzinnych ogrodach działkowych (t.j. Dz.U. z 2021 r. poz. 1073). API tekstu: https://api.sejm.gov.pl/eli/acts/DU/2021/1073/text.html
- ustawa o gospodarce nieruchomościami (użytkowanie wieczyste) — Dz.U. 1997 nr 115 poz. 741 (t.j.)
- Prawo energetyczne — Dz.U. 1997 nr 54 poz. 348 (t.j.)
- RODO — Rozporządzenie (UE) 2016/679 (EUR-Lex)

## Kontrola Henia 22.09.2026 (POTWIERDZONE)
Skille działają w Claude Code 2.1.228 bez zmian w plikach; poprawki wdrożone w /root/rod-ai-studio/CLAUDE.md (trigger prawny = odpowiednik User Preferences z claude.ai, mapa ścieżek shared/, view→Read, allowlista domen nie dotyczy Claude Code, isap.sejm.gov.pl pętla 302 → api.sejm.gov.pl/eli). Łańcuch weryfikacji t.j.: akt bazowy → references 'Inf. o tekście jednolitym' → text.html najnowszego t.j. Genek: błąd #37 (orzeczenia SAOS) w stabilnej 8.09, PR #53 → aktualizacja po scaleniu.
