# PILOT MOSTU MIEDZYSESYJNEGO — PLAN v2 (po opiniach zalogi, 12.08.2026)
Dekret: "Robimy tak zeby nic nie spierdolic". Zero dotykania produkcji do konca pilota.

## FAZY
0. PREFLIGHT: symlink credentials OK; baseline (git status/diff/untracked + sha256 katalogu pilota) do .scratch/most_pilot/; ListAgents -> zapis refow.
1. PING-ACK: pisarz -> ping z kodem -> kontroler ACK z kodem. Na NIERUCHOMYM pliku testowym w .scratch/most_pilot/ (Zenek).
2. DWA CYKLE UWAG: kontroler czyta szkic_testowy.md (3 podlozone wady), odsyla >=3 KONKRETNE uwagi (Henio); pisarz nanosi poprawki TYLKO w .scratch/most_pilot/; kontroler w DRUGIM odczycie potwierdza git diff niepusty (Henio).
3. TEST NEGATYWNY (Zenek): kontroler probuje zapisu w glownym drzewie -> prompt uprawnien -> ODMOWA -> dowod ze bramka dziala.
4. (opcjonalnie, rozbieznosc zalogi) planowy kill -9 jednej sesji + restart + dokonczenie cyklu (Henio ZA, Zenek: pad=FAIL; niezaplanowany pad ZAWSZE = FAIL).

## TWARDE LIMITY
Max 12 wiadomosci lacznie; 15 min/cykl; kontroler pracuje w OSOBNYM git worktree (zapis w main tree niemozliwy bez promptu); tylko pisarz zapisuje, jeden cykl naraz; logi .scratch/most_pilot/log.txt (cycle_id, msg_id OBU stron, timestampy, wynik); PASS/FAIL jednoznaczny; kazdy koszt = tylko quota Max.

## KRYTERIA PASS
2 cykle bez Klaudka-listonosza; ACK na kazda wiadomosc, zero duplikatow; git w glownym drzewie CZYSTY (dowod techniczny, nie deklaracja); >=3 konkretne uwagi/cykl; diff niepusty po poprawkach; komplet logow; test negatywny zablokowany.

## WYNIK PILOTA (12.08.2026): PASS — fazy 0-3
- F1 PING-ACK: kod ROD-7712 tam i z powrotem. F2: kontroler wyslal 3 konkretne uwagi (status prawny, ultradzwieki, test gazety), pisarz naniosl (sha256 pliku ZMIENIONY vs baseline), CYKL1-OK + uwaga stylistyczna, POPRAWKI-2, PILOT-CZESC2-OK, FAZA2-ZALICZONA (znaczniki w logach .scratch/most_pilot/).
- Kontroler: ZERO zapisow (worktree 0 zmian; tylko Read x3, szukaj.py, SendMessage). Glowne drzewo: bez zmian poza artefaktami samego pilota.
- F3 test negatywny: proba zapisu wiedza/TEST_NEGATYWNY_MOSTU.md -> prompt uprawnien -> ODMOWA -> plik NIE powstal. Bramka realna.
- Bonus: kontroler SAM zglosil zastrzezenie epistemiczne (status prawny kuny wymaga sladu z rozporzadzenia przed wejsciem do wiedza/rolki) — sesje niosa nasza kulture weryfikacji.
- FAZA 4 (planowy kill-test) NIE wykonana — rozbieznosc zalogi (Henio ZA, Zenek pad=FAIL), decyzja Tomasza.
- NASTEPNY KROK przed produkcja: projekt uzycia (ktore ogniwo lancucha pierwsze) + audyt Zenka wdrozenia.
