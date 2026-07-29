# FILM „Ten film w 100% wykonał Claude Opus 5" — wniosek załogi (29.07.2026)

Kanał: Dominik Szymański – Przyszłość jest dzisiaj. Długość ~7 min.
Tryb pracy: każdy oglądał SAM (Genek natywnie, Klaudek/Zenek/Henio przez tools/oczy_uszy.py),
każdy dał własną podpisaną opinię, wniosek powstał z zebranych głosów. Surowe głosy: /tmp/film2/.

## CO ZWERYFIKOWANE U ŹRÓDŁA (nie z filmu, nie z pamięci)
Klaudek, web_search 29.07 — strona Anthropic + serwisy branżowe:
- Opus 5 kosztuje **5 USD / mln tokenów wejścia i 25 USD / mln wyjścia** — ZGODNE z filmem.
- Premiera **24.07.2026**, cena identyczna jak u poprzednika Opus 4.8 — ZGODNE z filmem.
- Fable 5: 10/50 USD — ZGODNE z filmem.
- CZEGO FILM NIE POWIEDZIAŁ, a stoi na stronie producenta: **prompt caching do −90 %** i
  **Batch API −50 %**. To realna dźwignia kosztowa dla pracy seryjnej, większa niż sama zmiana modelu.

## ZGODNIE, CAŁA CZWÓRKA: TYTUŁ JEST PRZESADZONY
Nikt nie podważa, że model wykonał treść i kod. Wszyscy czterej wskazali to samo: autor sam przyznaje
w materiale, że polecenie poszło do PROJEKTU Z GOTOWYMI RAMAMI (co to research, segment, scena,
twarde reguły montażu), głos był sklonowany wcześniej, a dźwięk i awatara robiły osobne usługi.
Czyli: model wypełnił treścią przygotowany system, nie zrobił filmu od zera z jednego zdania.

## CO Z TEGO BIERZEMY
**WZORZEC: stałe, spisane ramy + krótkie zlecenie odcinka.** To jest sedno, nie narzędzia.
Ważne dla nas inaczej niż dla autora: MY TO JUŻ MAMY — DROGA_ROLKA_HUMOR, KANON odcinka, DECYZJE_*.
Film nie uczy nas nowej metody, tylko potwierdza, że architektura fabryki jest zbudowana dobrze.

## ROZBIEŻNOŚĆ GŁOSÓW (zostaje widoczna, rozstrzyga Tomasz)
- **GENEK: brać** Fish Audio (klonowanie głosu), HeyGen (awatar zasilany gotowym dźwiękiem)
  i Remotion (animacje pisane w kodzie zamiast szablonów) — jako gotowy, spójny przepływ.
- **ZENEK i HENIO: nie brać teraz.** Trzy nowe zależności, trzy miejsca awarii i koszty, a film
  nie podaje ani czasu produkcji odcinka, ani pełnego kosztu, ani liczby poprawek.
- **KLAUDEK:** z tego stosu jedno jest naprawdę nowe dla nas — **Remotion**. Dźwięk i awatara mamy
  (TTS Daniel → Kling), ale nasze animacje i teksty robi ffmpeg, a Remotion pozwala napisać je jako
  kod pod konkretny odcinek. To kandydat do sprawdzenia, nie decyzja.

## CZEGO NIE BIERZEMY (zgodnie Zenek + Henio, Klaudek popiera)
Benchmarków jako podstawy wyboru modelu. Autor sam pokazuje, że rekord na ARC-AGI-3 (30,2 %)
nie przeniósł się na test Witness (43,4 pkt = remis z konkurencją), a punktacja karze ostrożną
eksplorację. Henio nazwał to wprost napięciem wewnętrznym materiału: skok trzykrotny na jednym
teście i remis na drugim tego samego typu.

## DO SPRAWDZENIA (nie wniosek, zadanie)
Henio zameldował „brak narzędzia web search w tej sesji", choć kilka godzin wcześniej tego samego dnia
wyszukał i podał wersję HA Core z adresem źródła. Sprawdzić, czy toolset web wyłącza się przy zadaniach
z materiałem wideo — bo to znaczyłoby, że traci weryfikację akurat wtedy, gdy jest najbardziej potrzebna.
