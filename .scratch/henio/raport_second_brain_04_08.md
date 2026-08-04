# RAPORT HENIA — SECOND BRAIN: ANALIZA 18 PLIKÓW NIETKNIĘTYCH >7 DNI

Data: 04.08.2026 02:20 CEST
Polecenie: Tomasz (przez Klaudka) — zbadać pliki wiedza/ nietknięte dłużej niż 7 dni.
Zasada nadrzędna: NIE POPRAWIAM, tylko diagnozuję. Dowód = cytat z pliku + stan faktyczny na dysku.

Stan: 61 plików .md w wiedza/, 18 nietkniętych >7 dni (7 w głównym katalogu + 11 w archiwum/).

---

## WYNIK: 2 MARTWE, 5 STABILNYCH (główne) + 11 STABILNYCH Z DEFINICJI (archiwum)

---

### PLIK 1: ARCHITEKTURA.md (15.07.2026, 20 dni) — ❌ MARTWY

Opisuje stan infrastruktury, która częściowo się zmieniła.

**Rozbieżność A — ścieżka src/zarty.py nie istnieje:**
- CYTAT (linia 61): `Moduł \`src/zarty.py\`, dane \`data/zarty/NNNN/\`.`
- CYTAT (linia 68): `Styl bohaterów: stała STYL_BOHATEROW w zarty.py.`
- FAKT NA DYSKU: `src/zarty.py` NIE ISTNIEJE. Właściwa ścieżka: `apps/api/src/zarty.py` (istnieje, 04.08).
- DOWÓD: `ls /root/rod-ai-studio/src/zarty.py` → nie istnieje; `ls /root/rod-ai-studio/apps/api/src/zarty.py` → istnieje.

**Rozbieżność B — model Qwen3:14b nie istnieje w Ollama:**
- CYTAT (linia 14): `**Qwen3:14b** — angielskie prompty obrazów (tylko Droga #2) + zadanie NAPRAW; thinking mode ~12 GB`
- FAKT NA DYSKU: `ollama list` pokazuje `qwen2.5vl:7b` (5692 MB), nie `qwen3:14b`.
- DOWÓD: `curl -s http://localhost:11434/api/tags | python3 -c "..."` → qwen2.5vl:7b to jedyny model Qwen.

**Rozbieżność C — droga generowania obrazów zmieniona:**
- CYTAT (linia 16): `**Nano Banana Pro = Gemini 3 Pro Image przez fal.ai** (\`fal-ai/nano-banana-pro\`, $0.15/obraz) — obrazy rolek`
- FAKT NA DYSKU: GENEROWANIE_OBRAZU.md (01.08.2026) ustanawia DROGĘ GŁÓWNĄ przez Genka (`gemini-3.1-flash-image`, ~0,067 USD). Fal.ai tylko zapasowo przy awarii.
- DOWÓD: GENEROWANIE_OBRAZU.md linia 3-4: `„Gienek nano banana 2"` + `„Fal.ai jako alternatywa w przypadku awarii Gienka"`.

**Rozbieżność D — status Fabryki Żartów nieaktualny:**
- CYTAT (linia 61): `Fabryka Żartów (Droga B — w budowie, 15.07)`
- FAKT NA DYSKU: Wyprodukowano odcinki 10004-10010. Odcinek 10010 opublikowany i zamknięty (commit 3ab413d, 4.08). `data/zarty/` zawiera 7 katalogów odcinków + bank + tematy.json.
- DOWÓD: `ls /root/rod-ai-studio/data/zarty/` → 10004 10005 10006 10007 10008 10009 10010 bank.

**WNIOSEK: MARTWY.** 4 udokumentowane rozbieżności. Plik wymaga aktualizacji.

---

### PLIK 2: PROCEDURY.md (18.07.2026, 17 dni) — ❌ CZĘŚCIOWO MARTWY

**Rozbieżność — silnik obrazów zmieniony:**
- CYTAT (linia 7): `generate_image(prompt, images/NN.jpg, silnik=\"fal-ai/nano-banana-pro\") — TYLKO zmienione sceny ($0.15/szt., ZGODA!)`
- FAKT NA DYSKU: GENEROWANIE_OBRAZU.md (01.08) ustanawia Genka (`gemini-3.1-flash-image`, ~0,067 USD) jako drogę główną. Fal.ai tylko zapasowo.
- DOWÓD: GENEROWANIE_OBRAZU.md linia 3-4.

**UWAGA:** Pozostałe procedury (patch, restart kontenera, transfer plików, HA) mogą być nadal aktualne — nie znalazłem dowodów przeciwnych. Ale NIE testowałem ich — to wymagałoby uruchomienia.

**WNIOSEK: CZĘŚCIOWO MARTWY.** Przynajmniej 1 rozbieżność. Reszta do zweryfikowania przez wykonanie.

---

### PLIK 3: STYL.md (15.07.2026, 20 dni) — ✅ STABILNY

Opisuje zasady stylu, tonu i formatu publikacji. STOP PRODUKCJI (2.08) zawiesza ich stosowanie, ale nie unieważnia samych zasad. Żadna z opisanych reguł nie jest sprzeczna z nowszymi dokumentami.

- Brak znalezionych rozbieżności ze stanem dysku.
- Zawartość: format scenariusza, ton ROD, publikacja FB, YouTube, grafiki — wszystko to reguły "jak ma być", nie "co jest teraz".

**WNIOSEK: STABILNY.** Zasady nie zmieniły się — po prostu nie są obecnie używane ze względu na STOP PRODUKCJI.

---

### PLIK 4: DROGA_ROLKA_HUMOR.md (23.07.2026, 12 dni) — ✅ STABILNY

Szczegółowa dokumentacja procesu produkcji rolek humorystycznych (wersja 3.5). To referencja techniczna — opisuje JAK się robi, gdy produkcja rusza. STOP PRODUKCJI zawiesza stosowanie, ale nie dezaktualizuje procedury.

- CHANGELOG kończy się na 3.5 (23.07) — to OSTATNIA wersja przed STOP.
- Brak znalezionych sprzeczności z nowszymi dokumentami.

**WNIOSEK: STABILNY.** Dokumentacja procesowa — nie podlega dezaktualizacji przez sam upływ czasu.

---

### PLIK 5: PROMPTY_WZORCE.md (23.07.2026, 12 dni) — ✅ STABILNY

Bank promptów-zwycięzców dla serii Tomek i Janusz. To dane referencyjne — zapis tego, co zadziałało.

- Dwa wzorce startowe z #10007 + jeden potwierdzony kanarkiem z #10008.
- Brak rozbieżności — to historia sukcesów, nie opis stanu.

**WNIOSEK: STABILNY.** Dane referencyjne nie dezaktualizują się.

---

### PLIK 6: DECYZJE_SERIA_HUMOR.md (25.07.2026, 10 dni) — ✅ STABILNY

Append-only dziennik decyzji Tomasza dotyczących serii humor. Ostatni wpis: 25.07 (`STOP`).

- Format: data | DOSŁOWNY cytat | interpretacja | status.
- To zapis historyczny — nie może być "nieaktualny", bo dokumentuje co Tomasz powiedział i kiedy.

**WNIOSEK: STABILNY.** Append-only decyzje nie starzeją się — są zapisem faktów.

---

### PLIK 7: AKTYWA_SERII.md (26.07.2026, 9 dni) — ✅ STABILNY

Księga aktywów serii humor — koszty wielokrotnego użytku. Suma: $0.75 (podgląd duetu + biblioteka).

- Ostatni wpis: 26.07 (domena zmierzch $0.30 + diagnoza dryfu bohater_noc).
- To księgowość — zapis wydatków. Nie dezaktualizuje się.

**WNIOSEK: STABILNY.** Zapis księgowy jest faktem historycznym.

---

### PLIKI 8-18: ARCHIWUM/ (11 plików, 16.07–26.07.2026) — ✅ STABILNE Z DEFINICJI

Wszystkie 11 plików w `wiedza/archiwum/` to zamknięte odcinki i historyczne decyzje. Z definicji START.md: `wiedza/archiwum/ — zamknięte odcinki, wycofane pomysły, stare wersje, oba teleporty. Dalej przeszukiwalne, ale nie są fundamentem.`

Lista:
| plik | data | typ |
|---|---|---|
| ARCHIWUM_DROGA_HUMOR_v1.md | 16.07 | wycofana wersja Drogi |
| DECYZJE_10004.md | 17.07 | zamknięty odcinek |
| DECYZJE_10006_afera.md | 17.07 | zamknięty odcinek |
| DECYZJE_10005_slimak.md | 18.07 | zamknięty odcinek |
| DECYZJE_10007_jablko.md | 18.07 | zamknięty odcinek |
| DECYZJE_10008_kontrola.md | 23.07 | zamknięty odcinek |
| DECYZJE_000098.md | 25.07 | zamknięty odcinek |
| KANON_10009.md | 25.07 | zamknięty odcinek |
| DECYZJE_10009.md | 26.07 | zamknięty odcinek |
| PRZEKAZANIE_2026-07-26_10010.md | 26.07 | zamknięty odcinek |
| DECYZJE_10010.md | 26.07 | zamknięty odcinek |

**WNIOSEK: STABILNE Z DEFINICJI.** To archiwum — ma być stare.

---

## PODSUMOWANIE

| status | liczba | pliki |
|---|---|---|
| MARTWY | 2 | ARCHITEKTURA.md (4 rozbieżności), PROCEDURY.md (1 rozbieżność) |
| STABILNY | 5 | STYL.md, DROGA_ROLKA_HUMOR.md, PROMPTY_WZORCE.md, DECYZJE_SERIA_HUMOR.md, AKTYWA_SERII.md |
| STABILNY (archiwum) | 11 | wszystkie w wiedza/archiwum/ |

---

## CO DALEJ — REKOMENDACJA

**Do decyzji Tomasza:**
1. ARCHITEKTURA.md — wymaga aktualizacji (4 rozbieżności znalezione). Proponuję, żeby zrobił to Klaudek (odpowiada za wiedza/), a ja (Henio) lub Zenek zweryfikujemy po fakcie.
2. PROCEDURY.md — wymaga co najmniej poprawki silnika obrazów (fal.ai → Genek). Reszta procedur do sprawdzenia przez wykonanie.
3. Reszta plików (16) NIE wymaga dotykania — są albo stabilne, albo archiwalne z definicji.

**NIE POPRAWIAM tych plików sam** — decyzja należy do Tomasza. To jest tylko diagnoza.

---

Podpis: HENIO
Ślad: pomiary wykonane 04.08.2026 02:15-02:20 CEST, wszystkie polecenia w tej samej sesji.
