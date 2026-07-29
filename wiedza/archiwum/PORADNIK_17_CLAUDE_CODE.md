# PORADNIK: 17 porad praktyka o pracy z Claude Code
(dostarczony przez Tomasza 27.07.2026, plik 17_260727_230902.txt — notatki z materiału praktyka;
zasada Tomasza: "Czytać! Analizować, Uczyć się na czyichś błędach!")

1. **Ask user question w skillach** — dodać do skilli komendę "ask user question", żeby AI zadawało pytania po kolei w sformatowany sposób zamiast wielu pytań w jednym bloku. Można audytem znaleźć skille, gdzie to dodać.

2. **Własne komendy inicjujące zamiast /init** — przeanalizować najczęstsze zadania i zrobić szablony (np. /init-projekt-X), które automatycznie ustawiają środowisko i przepływ pracy.

3. **Auto approve** — zmienić domyślne ustawienie, żeby system nie prosił o zgodę na akcje już wcześniej zatwierdzone (mniej przerywania pracy).

4. **Przypomnienia startowe (session start hook) z logiką dni tygodnia** — akcja przy starcie sesji, np. w piątki przypomnienie o przeglądzie i optymalizacji systemu.

5. **Dyktowanie ze słownikiem mapowania** — narzędzie mowa→tekst (Hex/Whisper Flow) ze słownikiem poprawiającym najczęściej przekręcane słowa.

6. **Kontrola paska statusu / tokenów** — pilnować modelu, effort i zużycia kontekstu; przy ~60% kontekstu /compact lub /clear; przy braku tokenów przejść na słabszy model.

7. **Sub-agenci równolegle** — niezależne zadania zlecać równolegle kilku sub-agentom; nie dzielą kontekstu, więc świetni do niezależnych zadań i OBIEKTYWNEJ weryfikacji pracy innych agentów (eliminuje uprzedzenia AI).

8. **Tańsze modele gdzie się da** — proste zadania (np. weryfikacja źródeł) na mniejszych modelach (Haiku); wyłączać przekazywanie zbędnego kontekstu do nowych wątków.

9. **Wielowątkowość / separacja projektów** — osobne, nazwane sesje; odrębne projekty w osobnych folderach, żeby AI miało tylko właściwy kontekst.

10. **Skrypty osadzone w skillach** — podzielić pracę na "ocenę" (LLM) i "powtarzalne czynności" (skrypt); skrypt robi czarną robotę i oszczędza tokeny, model tylko osądza.

11. **Lista gotchas w skillach** — do kodu skilla dopisywać zbiór "czego NIE robić" na bazie napotkanych błędów i kłopotliwych przypadków.

12. **"Interview me" / "grill me" w plan mode** — przed działaniem kazać AI przepytać użytkownika (wykrycie luk), a "grill me" = surowa krytyka strategii, szukanie dziur.

13. **Audit trail przepływów** — każda automatyzacja loguje co zrobiła/naprawiła/co wraca; raz w tygodniu przegląd: "które powtarzające się problemy warto rozwiązać?".

14. **Weryfikacja w skillach** — na końcu skryptu jasny krok walidacji: konkretny werdykt ZDAŁ/OBLAŁ wobec kryteriów jakości.

15. **Pętle orkiestracji** — systemy w pętli do osiągnięcia celu: wyzwalacz → skill wykonawczy → weryfikacja celu (werdykt z pkt 14) → pamięć poprzednich kroków. Najpierw "tryb treningowy" (ręczna akceptacja każdego kroku), żeby błędy nie spaliły tokenów.

16. **Automatyzuj "od środka", nie end-to-end** — wystrzegać się 100% automatyzacji bez kontroli; zidentyfikować strefy ludzkiej walidacji: człowiek diagnozuje i deleguje, AI robi 95% "w środku", człowiek ocenia efekt przed upublicznieniem.

17. **"Stay desperate always"** — postawa ciągłego ucznia; nic nie jest dane na zawsze, umiejętności trzeba stale szlifować.
