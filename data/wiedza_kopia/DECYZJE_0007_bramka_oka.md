# DECYZJA 0007 — BRAMKA OKA fail-closed (28.07.2026, dekret Tomasza "Naprawiać")
Po wpadce WD_0001 v2 (Genek 10/10 bez seansu: read >20MB padł, ocena z promptu; kafle 75-160px
nie wykrywają orientacji) powstało stałe narzędzie `tools/bramka_oka.py`:
1. FAIL odczytu źródła = FAIL bramki (ekstrakcja/rozmiar/base64/API/format — każdy krok sprawdzany, exit 2).
2. Ocena na PEŁNEJ rozdzielczości, per klatka — nigdy mozaika kafelków.
3. Prompt BEZ opisu treści materiału; pole "opis" w odpowiedzi = dowód seansu.
4. Henik: manifest-first przed drogimi oczami (PODRECZNIK §8).
Test bojowy na v6: pierwsza runda złapała ucięte odpowiedzi (thinking zjadał tokeny) → 8/8 FAIL;
po poprawce (thinkingBudget=0, max 2048) → 8/8 OK, orient=pion, t=24 blur-fill zamierzony.
Obowiązek: każda przyszła produkcja wideo przechodzi bramkę oka przed pokazaniem Tomaszowi.
