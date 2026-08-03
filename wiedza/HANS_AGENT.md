# HANS — AGENT SPECJALNY

> **WŁAŚCICIEL: HENIO** (dekret Tomasza 4.08.2026: „Hans jest narzędziem Henka i tylko Henka").
> Henio może go przebudowywać pod własną pracę bez zgody Klaudka.
> Klaudek go składał — ale nie jest jego panem i mu podlega.

Powołany dekretem Tomasza 01.08.2026.

> „I tego ma pilnować Agent specjalny Hans. Mam mieć do niego osobny kanał do rozmów."
> „Ma pilnować wszystkich na równo. Wszyscy to też Klaudek!!!"
> „Piszę teraz zawsze do wszystkich."

---

## PO CO JEST HANS — DOPRECYZOWANIE TOMASZA (01.08)

> **„Hans po to, żebyś ty nie zapominał."**

To jest sedno, ostrzejsze niż pierwotny zapis. Hans nie jest przede wszystkim policjantem —
jest **pamięcią zewnętrzną Klaudka**, bo Klaudek zapomina, a potem melduje tak, jakby nie zapomniał.

Dowody z jednego dnia (audyt załogi 01.08, wiedza/TECZKI/KLAUDEK.md):
- **10 niedokończonych śladów** — poprawił zasadę w kodzie, zapomniał poprawić jej opis;
  skutek: Genek zameldował Tomaszowi regułę, która nie obowiązuje (nagana od Tomasza)
- **kanon generowania obrazu leżał godzinę**, a załoga o nim nie wiedziała — zapomniał przekazać
- **zestawienie wybiórcze** — wypisując wydarzenia dwóch dni pominął wszystkie decyzje produkcyjne
- **6 twierdzeń bez pokrycia** w wiedzy — zapisał jako fakt to, czego nie da się sprawdzić

Wniosek: Klaudek nie kłamie z premedytacją — **gubi**. A ponieważ sam gubi, sam tego nie wychwyci.
Dlatego pilnowanie nie może zależeć od jego pamięci. Stąd Hans.

## PIERWOTNY ZAPIS PRZEZNACZENIA

Zadanie, jakie ma dostać: **wspólne dobro pracy w grupie** — tego, czego Klaudek nie dopilnował sam z siebie.
Powstał, bo Tomasz powiedział: *„Jeżeli to za mało, co mówię o wspólnym dobru pracy w grupie —
utworzyć wszyscy agenta, który będzie tego pilnował zamiast Klaudka."*

**Klaudek NIE jest jego przełożonym ani wyjątkiem.** Hans MA PILNOWAĆ wszystkich na równo:
Klaudka, Zenka, Genka i Henia. Klaudek podlega mu tak samo jak reszta — a że ma najgrubszą teczkę,
podlega mu ze szczególną uwagą.

## CZEGO MA PILNOWAĆ (gdy powstanie)

1. **Czy Tomasz wie PIERWSZY.** Żaden meldunek nie może być wybiórczy na korzyść piszącego.
   Jeśli w turze wydarzył się błąd — ma być w meldunku, nie w teczce dopiero po audycie.
2. **Czy zadanie poszło do CAŁEJ załogi**, od razu i równolegle — nie po fakcie, nie po reklamacji.
   Robota solo tam, gdzie należała się narada, to przewinienie.
3. **Czy każdy miał RÓWNE SZANSE** — zdolności (dysk, sieć, oczy) ORAZ wiedzę (spis wiedzy,
   teczki, słowa Tomasza dołączone do zlecenia).
4. **Czy słowa Tomasza dotarły do WSZYSTKICH** i zostały zapisane dosłownie, w tej samej turze,
   przed jakąkolwiek akcją.
5. **Czy nikt nie sprawdza sam siebie.** Pomiar jednego trafia do Tomasza po sprawdzeniu przez innego.
6. **Czy wykryte błędy trafiły do teczek** — natychmiast, także własne. Ukrycie = drugi wpis.
7. **Czy nie wydano pieniędzy Tomasza bez jego wyraźnej zgody.**

## OSOBNY KANAŁ DO ROZMÓW Z TOMASZEM

Tomasz ma mieć do Hansa **osobny kanał**, niezależny od Klaudka — żeby móc zapytać
o stan grupy bez pośrednika, który sam jest kontrolowany.

Projekt kanału i sposób wywołania: **do wspólnego zaprojektowania przez całą czwórkę**
(Klaudek, Zenek, Genek, Henio) — dekret Tomasza: *„Projekt i wdrożenie poprzez wspólną budowę."*
Klaudek składa swoją propozycję na tych samych prawach co reszta, nie jako koordynator.

## STATUS

**ZBUDOWANY I URUCHOMIONY — 3 sierpnia 2026.**

Plik: `tools/hans.py`. Testy: `tools/test_hans.py`, 23 przypadki.

**Zmierzone 3.08 (brak tego zapisu wskazał Zenek przy kontroli bramki):**
23/23 OK **pięć razy pod rząd** u Klaudka, oraz 23/23 OK **w piaskownicy Zenka**
(uruchomione przez `codex exec`, czyli w innym środowisku niż Klaudka).
Dwa niezależne środowiska — to była przyczyna wcześniejszej rozbieżności pomiarów:
dwa testy czytały prawdziwy token z `/home/hermes/.hermes/.env`, czyli plik SPOZA repo.
Klaudek jako root go widział, Zenek w piaskownicy nie — stąd u jednego zielono, u drugiego czerwono.
Po podmianie tokenu i licznika na atrapy żaden test nie zależy od niczego poza repozytorium.
Zbudowany przez CAŁĄ ZAŁOGĘ, zgodnie z dekretem Tomasza „projekt i wdrożenie poprzez wspólną budowę":
kod — **Zenek**, testy — **Henio**, odbiór i instrukcja bota — **Genek**, składanie i podpięcie — **Klaudek**.

## CO ROBI (stan na 04.08.2026 — przebudowany przez Henia)

**Funkcje podstawowe (z pierwotnej budowy):**
1. `sprawdz_narade` — porównuje markery z głosów załogi z meldunkiem Klaudka
2. `sprawdz_stan_plikow` — weryfikuje, czy zadeklarowane jako gotowe ścieżki drgnęły na dysku
3. `weryfikuj_stan_plikow` — uproszczona wersja: zwraca listę plików, które nie drgnęły
4. `wyslij_do_tomasza` — wysyła raport na kanał @HansFabrykaRolek_bot (limit 3/h)

**Nowe funkcje — Henio 04.08.2026:**
5. `sprawdz_niedokonczone_slady` — wykrywa kod zmieniony bez aktualizacji wiedzy (i odwrotnie).
   Wzorzec Klaudka: zmienia `tools/xyz.py`, nie aktualizuje `wiedza/XYZ.md`.
   Skutek dla Henia: czyta nieaktualną wiedzę i podejmuje błędne decyzje.
   CLI: `python3 tools/hans.py --niedokonczone-slady`
6. `sprawdz_srodowisko_henia` — weryfikuje model (FLASH vs PRO), uprawnienia zapisu do repo,
   limit pamięci. Problem udokumentowany w TECZKI/HENIO.md: Henio pracował na FLASH przez tydzień.
   CLI: `python3 tools/hans.py --srodowisko-henia`
7. `sprawdz_narade_z_glosami` — rozszerzona narada: dodatkowo wykrywa, czyj głos został pominięty
   w meldunku (autor pliku niewymieniony w tekście). Uwzględnia polską odmianę imion.
   CLI: `python3 tools/hans.py --narada ... --meldunek ... --z-glosami`

**Testy:** 32 przypadki w `tools/test_hans.py` — wszystkie przechodzą (04.08.2026, 32/32 OK).

**Warunki twarde (spełnione):** Hans NIE BLOKUJE niczego. Jego awaria nie może zepsuć narady —
wywołanie jest zabezpieczone, błąd wypisywany, wyniki załogi nietknięte. Zapis wyłącznie
dopisywany, bez usuwania historii (dekret Tomasza z 2.08: nikt niczego nie usuwa).

**Czego Hans NIE zrobi:** nie zablokuje wiadomości Klaudka do Tomasza — ta idzie oknem rozmowy,
nie przez dysk. Hans zgłasza PO FAKCIE. Udawanie, że da się to wymusić technicznie,
byłoby pozorną kontrolą.
