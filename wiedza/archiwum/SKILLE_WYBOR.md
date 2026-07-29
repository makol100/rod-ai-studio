# WYBÓR SKILLI — z przeczytanego kodu, nie z opisów (28.07.2026)
Repozytoria sklonowane do /root/repo-recon/ (skills 1.7M, i-have-adhd 656K) i przeczytane.

## KOREKTA WCZEŚNIEJSZEGO MELDUNKU KLAUDKA
Skill **"caveman" NIE ISTNIEJE**. CHANGELOG, commit 47bde84: autor USUNĄŁ go razem ze "zoom-out" ("caveman był duplikatem innego skilla, nigdy nie miał być publiczny"). Wcześniejsza rekomendacja Klaudka "/caveman = -75% tokenów" pochodziła z opisu w sieci, nie z repo — BŁĄD, wycofany. Realne nazwy: diagnosing-bugs (nie "/diagnose"), triage, to-spec.

## STAN FAKTYCZNY REPO A (mattpocock/skills)
41 plików SKILL.md: engineering (19), productivity (5+), misc (4), in-progress (9), deprecated (4).

## WERDYKT ZAŁOGI
KONSENSUS (Zenek + Genek zgodnie) — wdrożyć 4:
1. **research** — badanie na źródłach pierwotnych + zapis ustaleń jako Markdown w repo = dokładnie nasza zasada "czytać całość" i katalog wiedza/.
2. **diagnosing-bugs** — pętla diagnostyczna zamiast zgadywania w pipeline TTS→obrazy→ffmpeg→FB.
3. **handoff** — sprasowanie rozmowy w dokument przekazania; nasz codzienny ból (kompakcje kontekstu, przekazywanie między Klaudkiem/Zenkiem/Genkiem/Henikiem).
4. **code-review** — niezależna kontrola zmian przed produkcją.
SPÓR o piątego: Genek → grill-with-docs (stress-test decyzji + wytwarza ADR-y); Zenek → writing-great-skills (piszemy własne skille fabryki) i wprost odrzuca rodzinę grill ("bezlitosne przepytywanie uciążliwe na telefonie").
ODRZUCONE ZGODNIE: tdd, implement, prototype, codebase-design, domain-modeling, improve-codebase-architecture (ciężka inżynieria, ryzyko przebudowy działającego); to-spec, to-tickets, triage, wayfinder (wymagają issue trackera — nie mamy); wszystko z in-progress i deprecated.

## REPO B (ayghri/i-have-adhd) — WERDYKT: PRZYJĄĆ CZĘŚCIOWO, JAKO PROFIL KOMUNIKACJI
Zachować: akcja/konkret w pierwszej linii; numerowane kroki; stan pracy w każdym meldunku; konkretne szacunki czasu; błędy rzeczowo (przyczyna+naprawa, bez "ojej"); PRZERWANIE SPIRALI DEBUGOWANIA po 3 nieudanych turach (nazwać błędne założenie zamiast dłubać dalej); potwierdzanie przed akcją niszczącą.
Zmodyfikować pod nasze zasady: "listy max 5" = preferencja interfejsu, nie prawo — pełny raport/audyt/research może być dłuższy, ale z werdyktem na początku; "zero wstępów" = kasować grzecznościową watę, ALE meldunek "sprawdziłem kod i dokumentację" to DOWÓD wykonania weryfikacji, nie wstęp; "zero podsumowań" nie dotyczy raportów końcowych i przekazań.

## RYZYKO I OGRANICZENIE (zgodnie obaj)
Zagrożenie: skill odpali się w złym kontekście i nakłoni agenta do zmiany kodu/konfiguracji/publikacji na podstawie własnych założeń.
Ograniczenie: wdrażać przypięte, przejrzane kopie; domyślnie WOLNO analizować i proponować, a modyfikacje produkcji, publikacja i operacje destrukcyjne — dopiero po jawnej zgodzie Tomasza. Wdrażać stopniowo, nie wszystko naraz.

## STATUS: NIC NIE ZAINSTALOWANE — czeka na słowo Tomasza.
Miejsce docelowe: /root/.claude/skills/ (tam już mieszka skill "route"). i-have-adhd ma gotowe warianty dla Claude, Codex, Gemini i Cursor.
