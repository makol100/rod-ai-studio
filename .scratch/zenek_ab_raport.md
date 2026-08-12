# Raport bieżący — Zenek A+B

## 2026-08-12 — start

- Przeczytano `wiedza/START.md`, `wiedza/GENEROWANIE_OBRAZU.md` i wyniki `tools/szukaj.py`.
- Git: próba `git switch -c zenek-warsztat` zablokowana przez read-only `.git` (`cannot lock ref`).
- Zakaz płatności zachowany: nie uruchomiono żadnego submitu/generacji.
- Dodano klienta `tools/zenek_obraz.py` i dwa orkiestratory fail-closed.
- Pipeline Wiadomości nie importuje historycznych płatnych skryptów z `data/wiadomosci/0001-teren/`.
- Auth Gemini: `.env` zawiera tylko `FIRECRAWL_API_KEY`; brak `GEMINI_API_KEY`, więc `models.list` zakończyło się lokalnym `BRAK AUTH` przed połączeniem.
- Pierwsza kontrola istniejącego filmu wykazała, że strażnik musi znać liczbę planowanych cięć. Pipeline poprawiono: `--planowane-ciecia` jest wymagane, więc cięcia montażowe nie są mylone z obcymi.
- Film 16:9 na istniejącym `FILM-ROD-16x9.mp4`: strażnik PASS (techniczny WARN: wykrył 5/28 cięć), eksport testowy 1920x1080, 331.4 s.
- Pierwsza kontrola Wiadomości poprawnie zatrzymała plik, bo gotowy awatar ma 2 planowane cięcia, a pipeline dostał domyślne 0. Dodano jawne `--planowane-ciecia`.
- Brak SyncNet/torch w środowisku oznacza `usta_sync=POMINIĘTY`. Produkcyjny eksport jest teraz fail-closed; `--test-offline` pozwala wyłącznie sprawdzić lokalne sklejenie i raportuje pominięcie.

## Do sprawdzenia

- testy jednostkowe bramki kosztowej;
- darmowe `models.list` dla aktualnego klucza;
- dry-run requestów wszystkich modeli;
- testy obu montaży na istniejących częściach `data/`;
- kontrola całej załogi i audyt raportu.

## Wynik końcowy testów lokalnych

### POTWIERDZONE

- `python3 -m unittest testy/test_zenek_obraz.py -v`: 3/3 OK. Sprawdzone mapowanie `predict`, `generateContent` oraz cena Pro 4K = 0,24 USD.
- Dwa wywołania bez `--zaplac` zakończyły się `DRY-RUN (NIC NIE WYSLANO)` dla Imagen Fast 0,02 USD i Nano Banana Pro 4K 0,24 USD.
- `python3 tools/zenek_obraz.py --lista`: `BRAK AUTH` przed połączeniem, bo `.env` ma tylko `FIRECRAWL_API_KEY`. Auth API NIE ZWERYFIKOWANO.
- Film 16:9: istniejący master przeszedł strażnika (`werdykt: PASS`) i został skopiowany do `/tmp/zenek_ab/FILM-ROD-16x9.mp4`; ffprobe: 1920x1080, 331,4 s.
- Wiadomości: istniejąca czołówka + istniejący awatar zostały znormalizowane i sklejone do `/tmp/zenek_ab/WIADOMOSCI_TEST_v3.mp4`; ffprobe: 1080x1920, 53,114333 s. Status jawny `TEST_OFFLINE`, `kontrola_ust: POMINIĘTY`.
- `git diff --check` bez błędów; `py_compile` bez błędów.
- Nie wykonano żadnej płatnej generacji ani submitu.

### HIPOTEZY / wymaga płatnego testu i zgody Tomasza

- Jedna próbna generacja Imagen Fast: szacunek 0,02 USD — sprawdzi rzeczywisty format odpowiedzi `predict` i zapis obrazu.
- Jedna próbna generacja kanoniczna Gemini 3.1 Flash Image: szacunek 0,067 USD — sprawdzi `generateContent` i zapis `inlineData`.
- Nano Banana Pro: 0,134 USD (2K) albo 0,24 USD (4K) — niepotrzebne do testu podstawowego klienta; tylko osobna zgoda.
- Produkcja nowego odcinka Izabeli wymaga płatnego TTS i awatara. Nowy pipeline celowo nie ma adaptera submitującego; `--zaplac` kończy się STOP-em, dopóki Tomasz nie zatwierdzi konkretnej próby.

### NIE WIEM / blokery środowiska

- NIE WIEM, czy aktualny klucz autoryzuje wymienione modele: brak `GEMINI_API_KEY` w `.env`, więc darmowe `models.list` nie mogło zostać wykonane.
- NIE WIEM, czy synchronizacja ust istniejącego awatara przechodzi SyncNet: w środowisku brak `torch`, strażnik zwrócił `POMINIĘTY`. Produkcyjny pipeline blokuje wtedy eksport.
- Nie utworzono gałęzi `zenek-warsztat` ani commitu: `.git` jest read-only (`cannot lock ref ... Read-only file system`).
- Narada nie miała równych szans: Henio niedostępny przez zakaz `su`, Genek dwukrotnie w trybie awaryjnym bez dysku, głos Zenka pusty. Wynik narady nie jest podstawą twierdzeń technicznych; dowodami są wyłącznie uruchomione testy powyżej.

## WYNIKI TESTÓW KOSZTOWYCH (12.08.2026, zgoda Tomasza "Daję")
- **Imagen Fast**: API 404 — "no longer available to new users" (migracja do Interactions API). Droga MARTWA na tym koncie. Szac. $0.02 — prawdopodobnie nie naliczone.
- **Gemini 3.1 Flash Image**: PASS — ZAPISANO obraz.png, HTTP 200, format `generateContent` + `inlineData` poprawny. Koszt $0.067.
**Wniosek**: najtańsza działająca droga = Gemini 3.1 Flash Image ($0.067). Imagen Fast usunąć/ukryć z klienta. Nano Banana Pro ($0.134+) — osobna zgoda.

## TORCH — USTALENIE KLAUDKA (12.08, na pytanie Tomasza)
Torch NIE wymaga instalacji na hoscie: kontener fabryka-api MA torch 2.13.0+cpu (dowod: import OK). Venv Henia tez ma (2.13.0+cu130).
DROGA dla usta_sync w pipeline Wiadomosci: adapter przez `docker exec fabryka-api ./venv/bin/python .../run_syncnet.py` (data/ bind-mountowane pod ta sama sciezka). Warunek: katalog tools/syncnet_python z run_syncnet.py — patrz wynik ls powyzej w logu Klaudka; jesli BRAK, to brakiem jest KATALOG syncnet (do sklonowania/odtworzenia), nie torch.
