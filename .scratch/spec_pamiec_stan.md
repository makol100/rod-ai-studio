# SPEC: Pamiec krotkotrwala Klaudka (prototyp) — "STAN"

Zatwierdzone przez Tomasza 6.08.2026 ("To ma Klaudku ma byc"). Werdykt zalogi: podpatrzec KONCEPT TencentDB (Mermaid + node_id + drill-down), zbudowac WLASNE, bez zaleznosci od TencentDB. Pierwszenstwo: KROTKOTRWALA. Dlugoterminowa (L0-L3) NIE — nasz wiedza/ + teleport pokrywa, i nie omijac bramki Klaudka (do wiedza/ tylko sprawdzone).

## CEL
Po kompakcji sesji (przepelnienie okna) Klaudek ma odtworzyc STAN zadania (co zrobione / w toku / blokery) + DOWODY (surowe pliki), bez wklejania calej historii ani pelnego TELEPORT tail. Zamiast tysiecy tokenow logu — maly graf stanu (kilkaset tokenow) + drill-down po node_id do surowego pliku na dysku.

## ZASADY PROJEKTU (z glosow Zenka i Henia — TRZYMAC SIE)
1. DANE KANONICZNE w JSONL (rejestr wezlow) — to zrodlo prawdy. Mermaid to TYLKO warstwa prezentacji generowana z JSONL, NIGDY jedyne zrodlo stanu.
2. Kazdy wezel MUSI wskazywac istniejacy surowy plik (drill-down dowodowy). Kontrola: graf nie moze miec wezla bez pliku.
3. Offload NIE moze byc irreversible — z node_id zawsze wraca pelny surowy tekst (jak TencentDB: "zlozona mapa, ktora mozna rozlozyc", nie streszczenie).
4. Graf capped: max ~4000 znakow / max 20% budzetu startowego — nie moze zjesc okna, ktore oszczedza.
5. To NIE zastepuje bramki Klaudka do wiedza/. STAN to pamiec ROBOCZA sesji (.scratch/), nie trwala wiedza. Do wiedza/ dalej trafia tylko sprawdzone, recznie.

## STRUKTURA PLIKOW
- `.scratch/stan/rejestr.jsonl` — KANON. Jedna linia = jeden wezel:
  `{"node_id":"n001","ts":"2026-08-06T17:40","opis":"krotki opis kroku","status":"zrobione|w_toku|bloker","zrodlo":".scratch/refs/n001.md","zaleznosci":["n000"]}`
- `.scratch/refs/<node_id>.md` — surowy dowod (pelny output narzedzia / log / tresc), offloadowany z kontekstu.
- `.scratch/stan/graf.md` — GENEROWANY z rejestru. Mermaid `graph TD` (boxes + arrows wg zaleznosci), status kolorem/oznaczeniem, kazdy box z node_id. Capped 4000 znakow.

## NARZEDZIA (tools/pamiec_stan.py, jeden plik, subkomendy)
- `dodaj --opis "..." --status w_toku --zrodlo PLIK [--zaleznosci n000,n001]`
  -> auto-nadaje node_id (kolejny), dopisuje linie do rejestru.jsonl. Jesli --tresc-z-stdin: zapisuje surowy tekst do .scratch/refs/<node_id>.md i ustawia zrodlo na ten plik (offload).
- `graf` -> czyta rejestr.jsonl, generuje .scratch/stan/graf.md (Mermaid), waliduje ze KAZDY zrodlo istnieje (jak nie -> ostrzezenie), pilnuje capa 4000 znakow (jak przekracza -> zwija najstarsze zrobione wezly w jeden "[... N zrobionych ...]").
- `pokaz [--node_id X]` -> bez arg: wypisuje graf.md. Z --node_id: drill-down = wypisuje .scratch/refs/<X>.md (surowy dowod).
- `status` -> podsumowanie: ile wezlow, ile w_toku/bloker, czy wszystkie zrodla istnieja.

## TEST (FAZA 1 = PETLA ZDAJ/OBLEJ, przed uznaniem za gotowe — zasada 29.07)
`tests/test_stan.py` — musi zapalac sie czerwono na bledach, zielono gdy dziala:
1. Dodaj 8 wezlow (mix statusow, z zaleznosciami, 2 z offloadem surowej tresci do refs/).
2. Wygeneruj graf -> sprawdz: jest Mermaid, ma wszystkie node_id, <4000 znakow, kazdy wezel ma istniejacy plik zrodlowy.
3. Symuluj KOMPAKCJE: odrzuc wszystko z pamieci OPROCZ graf.md (kilkaset tokenow).
4. Odtworz: z graf.md wyciagnij node_id blokerow i w_toku -> drill-down po node_id -> sprawdz, ze surowy dowod wraca kompletny (bajt w bajt jak zapisany).
5. ZDAJ tylko gdy: (a) wszystkie decyzje/statusy odtworzone z samego grafu, (b) kazdy drill-down zwraca pelny oryginal, (c) cap 4000 trzymany. Oblej jak cokolwiek zgubione.

## KOLEJNOSC (Zenek buduje)
1. Najpierw tests/test_stan.py (petla — definiuje "dziala"). 
2. Potem tools/pamiec_stan.py az test zielony.
3. Commit. Meldunek z wynikiem testu (nie "gotowe" bez zielonego testu — zasada weryfikacji).
NIE dotykac wiedza/. NIE wpinac TencentDB. Dane kanoniczne JSONL, Mermaid tylko prezentacja.

## ZASIEG: WARIANT 3 (zatwierdzony 6.08 — "narzedzie ogolne, Klaudek pierwszy klient")
- Narzedzie tools/pamiec_stan.py jest OGOLNE (fabryka) — uzywa go kazdy agent na VPS (Klaudek przez most, Claude Code, Zenek, przyszle sesje).
- PRZESTRZENIE NA AGENTA, zeby stany sie nie mieszaly: rejestr i refs pod przestrzenia:
  - `.scratch/stan/<agent>/rejestr.jsonl`, `.scratch/stan/<agent>/graf.md`, `.scratch/refs/<agent>/<node_id>.md`
  - domyslny agent = "klaudek"; wybor przez `--agent NAZWA` (albo env STAN_AGENT).
- Klaudek = PIERWSZY realny klient: czyta swoj graf.md na starcie sesji (zamiast pelnego TELEPORT tail) i dopisuje wezly w trakcie. Reszta zalogi moze dojsc pozniej — narzedzie juz to obsluguje.
- node_id unikalne w obrebie przestrzeni agenta (n001, n002... per agent).
- Reszta specu (JSONL kanon, Mermaid prezentacja, offload odwracalny, cap 4000, test zdaj/oblej, nie dotykac wiedza/) bez zmian.

## LUKA 2 ROZSTRZYGNIETA: HYBRYDA (Tomasz 6.08)
- AUTOMAT surowych komend JUZ ISTNIEJE: Hans loguje kazda komende MCP do .scratch/hans/most.jsonl. NIE budujemy nowego automatu — most.jsonl JEST warstwa surowa.
- KLAUDEK dodaje wezly ZNACZENIOWE recznie (pamiec_stan.py dodaj): tylko bloker / decyzja / sukces / kluczowy krok. Graf czysty, bez drobiazgow.
- Wezel linkuje do dowodu: albo zakres w most.jsonl (--zrodlo-most, luka 1), albo .scratch/refs/<agent>/ (duza tresc, ktorej Hans nie lapie). NIE kopiuje tego, co Hans juz ma.

## LUKA 1: --zrodlo-most (do budowy przez Zenka)
- Nowa opcja: `dodaj ... --zrodlo-most "TS_OD..TS_DO"` (zakres czasu ISO) LUB `--zrodlo-most "OD:DO"` (numery linii) — wezel WSKAZUJE zakres w .scratch/hans/most.jsonl, nie kopiuje tresci.
- `pokaz --node_id X` dla wezla z --zrodlo-most: wycina i wypisuje odpowiedni fragment most.jsonl (drill-down do surowej komendy).
- Walidacja: zakres istnieje w most.jsonl; jak brak — ostrzezenie (nie cichy blad).
- ZACHOWAC dotychczasowe --zrodlo PLIK i --tresc-z-stdin (duze tresci -> refs/). --zrodlo-most to trzecia opcja zrodla.

## LUKA 3: zasada, nie kod
- STAN czyta sie RAZEM z teleportem+decyzjami na starcie (graf = CO, teleport/decyzje = DLACZEGO/co Tomasz kazal). STAN nie zastepuje ich. Dopisac do protokolu startu jako czwarty czlon: `python3 tools/pamiec_stan.py pokaz`.
