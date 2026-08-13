# KRYMINALISTYKA LUKI — RAPORT HENIA 6.08.2026 07:15 CEST

Zlecenie: znalezc material, ktory ISTNIEJE a NIE jest ujety w rejestrach
(rejestry = tools/decyzje.py, TELEPORT_fabryka.md, /root/TELEPORT_HA.md, wiedza/, git).

---

## WERYFIKACJA USTALEN KLAUDKA

### (1) D-0067 to ostatnia decyzja — POTWIERDZONE
- git HEAD: fa5095a, 2026-08-05 22:45:44 CEST (D-0067, "ROUTER NA DZIALCE — NIE DOTYKAC")
- `python3 tools/decyzje.py --lista`: ostatnia linia = D-0067
- `.scratch/decyzje_tomasza.jsonl`: 67 linii, ostatnia modyfikacja 2026-08-05 22:45:44 CEST
- **Wniosek Kladka: ZERO decyzji Tomasza po D-0067 — POTWIERDZONY**

### (2) Miedzy 5.08 20:46 a 6.08 ruszały sie tylko pliki automatow — NIE W PELNI
Pliki zmodyfikowane po D-0067 (2026-08-05 22:45:44):
| plik | data modyfikacji | typ |
|---|---|---|
| data/barometr_cache.json | 2026-08-06 05:01 | automat (potwierdzone) |
| .scratch/hans/most.jsonl | 2026-08-06 06:59 | automat + NOWA TRESC Klaudka (patrz LUKA #4) |
| .scratch/hans/oczy.jsonl | 2026-08-05 22:46 | automat + NOWE WPISY Hansa (patrz LUKA #5) |
| wiedza/BRIEF_DLA_KLAUDKA.md | 2026-08-06 06:38 | automat (cron brief-klaudka) |

Klaudek NIE wychwycil, ze most.jsonl i oczy.jsonl to nie tylko "automaty" — zawieraja NOWA TRESC (62 nowe linie w moscie, 6 w oczach) z pelnym sladem operacyjnym jego wlasnej pracy 5.08 wieczorem.

### (3) TELEPORT_HA.md stoi na 4.08 — POTWIERDZONE
- Ostatnia sesja: 04.08.2026 09:22 CEST
- Brak CALEGO dnia 5.08: D-0054 do D-0067, Tuya, zawor gazu, trasy Tailscale, router Dzialki
- Rozmiar: 583 linie, 49 KB

### (4) TELEPORT_fabryka.md ~1 dzien z tylu — POTWIERDZONE
- Ostatnia sesja: 04.08.2026 09:29 CEST
- Brak opisu D-0061, D-0062, D-0063, EGO LITE, CLAWMEM, i calego 5.08
- Rozmiar: 2798 linii, 280 KB

### (5) Untracked gora plikow to stare pliki 27.07-4.08 — POTWIERDZONE
- data/awatar, data/wiadomosci/0001-teren, data/_narada_17, assets/zarty/karty, work, archiwum
- Wszystkie datowane przed 5.08, swiadomie poza gitem (D-0020)
- NIE sa swiezym materialem z okna

### (6) Luzne fix_*.py w korzeniu to debug z 3.08 — POTWIERDZONE
- fix_zaloga.py, fix_test_hans.py, fix_test_hans2.py, test_script.py
- Nie modyfikowane po 3.08

---

## LUKI — CZEGO KLAUDEK NIE WYMIENIL

### LUKA #1: ARTEFAKTY NARAD W /tmp (284 KB, niezarejestrowane nigdzie)

Cztery pelne katalogi narad zalogi, ktore NIE zostaly posprzatane po zakonczeniu.
Zawieraja kompletne glosy calej czworki + manifest + przebieg.log.

**/tmp/czego_brakuje/** (76 KB, 2026-08-05 20:41-20:47 CEST)
- genek.txt, henio.txt, zenek.txt + manifest.json + _przebieg.log
- Narada "czego fabryce brakuje" — zrodlo dla D-0061, D-0062, D-0063
- WNIOSEK: same decyzje sa w rejestrze, ale PELNE GLOSY ZALOGI (razem ~14 KB surowego tekstu) nie sa nigdzie poza /tmp

**/tmp/zaczep_hans/** (92 KB, 2026-08-05 09:27-09:31 CEST)
- genek.txt, henio.txt, zenek.txt + manifest.json + _przebieg.log
- Narada o zaczepie Hansa — zrodlo dla D-0051
- STATUS: LUKA — pelne glosy nie sa w rejestrze

**/tmp/clawmem2/** (92 KB, 2026-08-05 09:07-09:19 CEST)
- genek.txt, henio.txt, zenek.txt + manifest.json + _przebieg.log
- Narada o ClawMem — zrodlo dla D-0048, D-0049
- STATUS: LUKA — pelne glosy nie sa w rejestrze

**/tmp/narada_clawmem/** (24 KB, 2026-08-05 08:43-08:46 CEST)
- henio.txt, zenek.txt + manifest.json
- Pierwsza narada ClawMem
- STATUS: LUKA — pelne glosy nie sa w rejestrze

**Dodatkowe pliki luźne w /tmp:**
- /tmp/clawmem_zrodla (5.08 09:05)
- /tmp/clawmem_full.md (5.08 09:05)
- /tmp/clawmem_zadanie.md (5.08 08:43)
- /tmp/clawmem_narada_20260805.md (5.08 08:43)
- /tmp/clawmem_narada_glosy (5.08 08:43)
- /tmp/clawmem_narada_0508.txt (5.08 08:26)
- /tmp/narada_clawmem_0508, 0508b, 0508c (5.08 08:26)

**Werdykt: LUKA. 284 KB surowego materialu — pelne glosy zalogi z 4 narad.**
Decyzje D-0048, D-0049, D-0051, D-0061, D-0062, D-0063 sa w rejestrze,
ale same glosy (uzasadnienia, analizy, NIE WIEM, rozbieznosci) NIE sa zapisane
w zadnym trwalym miejscu. /tmp moze zostac wyczyszczone przy restarcie.
Zalecenie: przeniesc do .scratch/ lub archiwum.

---

### LUKA #2: SKASOWANY .scratch/_sonda_zenek_siec.txt (niezacommitowane usuniecie)

Git status pokazuje:
```
D .scratch/_sonda_zenek_siec.txt
```

Plik zostal USUNIETY z dysku, ale usuniecie NIE jest zacommitowane.
Ostatnia znana zawartosc (z git HEAD): "200" — pojedyncza liczba (prawdopodobnie kod HTTP).

**Werdykt: LUKA (niewielka).** Nie wiadomo, co dokladnie zawieral i dlaczego zostal skasowany.
Usuniecie nie jest w git, wiec jest to zmiana stanu, ktora nie trafila do rejestru.

---

### LUKA #3: NIEZACOMMITOWANA ZMIANA W tools/mcp_wybickiego.py

```diff
-            print(c["text"][:2500])
+            print(c["text"])
```

Usunieto limit 2500 znakow na odpowiedzi z HA Wybickiego. Zmiana funkcjonalna,
niezacommitowana, z 2026-08-05 13:03 CEST.

**Werdykt: LUKA.** Kazdy diagnostyczny odczyt HA przez MCP bedzie teraz zwracal
pelna odpowiedz zamiast obcietej. To moze wplywac na dlugosc odpowiedzi Klaudka.
Zmiana nie jest w git, nie ma jej w rejestrach.

---

### LUKA #4: PELNY SLAD OPERACYJNY KLAUDKA W most.jsonl (62 nowe linie)

Hans `most.jsonl` zawiera NIEZACOMMITOWANE 62 linie z pelnym sladem dzialan
Klaudka 5.08 wieczorem (21:10-22:53) ORAZ dzis rano (06:50-06:59):

5.08 wieczor — praca nad Tailscale i routerem:
- 21:10-21:13: sprawdzanie tras, `tailscale up --accept-routes`, skanowanie sieci 192.168.0.x
- 21:13: D-0064 (trasy dla Wybickiego)
- 21:19-21:36: monitorowanie propagacji tras, D-0065 (uklad koncowy)
- 21:40-21:52: SSH na router Wybickiego, proba logowania, analiza JS szyfrowania hasla
- 22:35-22:53: dalsze sondowanie tras, SSH tunel na 8081, D-0066 + D-0067

6.08 rano — przygotowanie do kryminalistyki:
- 06:50: odczyt BRIEF_DLA_KLAUDKA.md
- 06:50: sprawdzenie teleportow i decyzji
- 06:55: git status
- 06:57: sprawdzenie decyzje_tomasza.jsonl
- 06:59: zlecenie dla zalogi (to wlasnie Klaudek delegowal to zadanie do Henia)

**UWAGA BEZPIECZENSTWA:** linia z 21:48 zawiera credentials routera w base64:
`printf 'admin:<USUNIETE>' | base64` — NIE cytowane w raporcie, ale obecne w surowym logu.

**Werdykt: LUKA.** Most.jsonl to NAJBOGATSZY slad operacyjny 5.08 wieczorem —
pelniejszy niz decyzje.py, pelniejszy niz git log. Zawiera PROBY (udane i nie),
sciezki diagnostyczne, i kontekst, ktorego NIE MA w zadnym rejestrze.
Dodatkowo: Klaudek uznal to za "automat", ale te 62 linie to NOWY material,
nie automatyczny zapis.

---

### LUKA #5: NOWE WPISY HANSA W oczy.jsonl (6 nowych linii)

Hans wykryl i zapisal podejrzane modyfikacje plikow wiedzy:

```
2026-08-05 19:15:59 — HA_WYBICKIEGO.md modified (wiedza_bez_powiazanego_kodu)
2026-08-05 19:46:12 — HA_WYBICKIEGO.md modified ponownie
2026-08-05 20:46:59 — NAUKI.md modified (wiedza_bez_powiazanego_kodu)
```

To byly falszywe alarmy (pliki zmodyfikowane w ramach normalnych commitow),
ale same wpisy Hansa to NOWY material — niezacommitowany, niezarejestrowany.

**Werdykt: NIE-LUKA (falszywe alarmy), ale same wpisy sa LUKA (niezacommitowane).**
Wykrycia sa bledne, ale 6 nowych linii w oczy.jsonl nie jest w git.

---

### LUKA #6: REEL 000098 WYGENEROWANY DZIS RANO (poza rejestrami)

Fabryka wygenerowala pelny reel 000098 dzis rano 06:51-07:10 CEST:
- tryb: sprzet, czysty_bielik
- 8 scen, 8 obrazow (fal.ai Nano Banana Pro)
- audio edge-tts, napisy whisper
- final_with_music.mp4 gotowy o 07:10
- powiadomienie Telegram wyslane

Reel NIE jest w content.db (tabela `reels` jest pusta — 0 wierszy).
Jedyny slad to live.log i pliki w data/reels/000098/.

**Werdykt: LUKA.** Reel 000098 powstal miedzy D-0067 a teraz. Nie ma go w decyzjach
(produkcja to nie decyzja Tomasza), nie ma w TELEPORT (ostatnia sesja 4.08),
nie ma w content.db (tabela pusta). Jedyny pelny slad: live.log + pliki na dysku.

---

### LUKA #7: SESJA CODEX (ZENEK) Z 06:30 DZIS RANO

Plik: `/home/hermes/.codex/sessions/2026/08/06/rollout-2026-08-06T06-30-15-019fd556-...jsonl`
- 11 linii, data 06:30 CEST
- Sesja prawdopodobnie nieudana (wszystkie pola content puste)
- Brak sladow w repo, decyzjach, teleportach

**Werdykt: NIE-LUKA (nieudana sesja).** Sesja nie wyprodukowala tresci.
Ale sam fakt jej istnienia nie jest w rejestrach — warto odnotowac.

---

### LUKA #8: CRON HERMESA — brief-klaudka co 30 min (automat, potwierdzone)

Cron 1078b045d791 (`brief-klaudka`) chodzi co 30 min i nadpisuje
BRIEF_DLA_KLAUDKA.md. Ostatnie wykonania: 23:00, 23:30 (5.08), 00:01, 00:31,
01:02 (6.08). Kazde generuje ten sam plik zaktualizowany tylko o timestamp
i wiek teleportow.

**Werdykt: NIE-LUKA.** Automat, ktory Klaudek juz wymienil. Generuje tylko
BRIEF_DLA_KLAUDKA.md — ten sam plik, bez nowej tresci merytorycznej.

---

## PODSUMOWANIE

### Znalezione luki (material ISTNIEJE, NIE jest w rejestrach):

| # | Co | Gdzie | Data | Waga |
|---|---|---|---|---|
| L1 | Pelne glosy zalogi z 4 narad | /tmp/{czego_brakuje,zaczep_hans,clawmem2,narada_clawmem}/ | 5.08 08:43-20:47 | **WYSOKA** — 284 KB, zniknie po restarcie |
| L2 | Skasowany _sonda_zenek_siec.txt | .scratch/ (usuniety, niezacommitowany) | przed 5.08 | niska |
| L3 | tools/mcp_wybickiego.py bez limitu | tools/mcp_wybickiego.py (diff) | 5.08 13:03 | srednia |
| L4 | Pelny slad operacyjny Klaudka 5.08 wieczor | .scratch/hans/most.jsonl (62 linie diff) | 5.08 21:10-22:53 + 6.08 06:50-06:59 | **WYSOKA** — zawiera credentials routera |
| L5 | Nowe wpisy Hansa w oczy.jsonl | .scratch/hans/oczy.jsonl (6 linii diff) | 5.08 19:15-20:46 | niska (falszywe alarmy) |
| L6 | Reel 000098 wygenerowany dzis rano | data/reels/000098/ + live.log | 6.08 06:51-07:10 | **WYSOKA** — nowa produkcja poza rejestrami |
| L7 | Sesja Codex Zenka | ~hermes/.codex/sessions/.../rollout-...jsonl | 6.08 06:30 | niska (pusta) |
| L8 | Cron brief-klaudka | ~hermes/.hermes/cron/output/ | 5.08 23:00 - 6.08 01:02 | brak (automat, Klaudek juz wie) |

### Najwazniejsze, czego Klaudek NIE WYMIENIL:

1. **284 KB glosow zalogi w /tmp** — najcenniejszy nieutrwalony material.
   Przy restarcie serwera przepadnie bez sladu.

2. **Reel 000098** — nowa produkcja dzis rano. Nie ma w content.db, nie ma w TELEPORT.
   Gdyby ktos szukal tylko w rejestrach, nie wiedzialby, ze powstal.

3. **62 linie sladu operacyjnego Klaudka w most.jsonl** — bogatsze niz decyzje.py.
   Zawiera m.in. credentials w base64 (admin:<USUNIETE>).

4. **Nie zacommitowana zmiana w mcp_wybickiego.py** — diagnostyka HA bez limitu znakow.

### Co Klaudek ustalil POPRAWNIE:

- D-0067 ostatnia decyzja
- TELEPORT_HA.md i TELEPORT_fabryka.md stoja na 4.08
- Untracked gora to stare pliki
- fix_*.py to debug z 3.08
- Automaty dzialaja (brief, barometr)

### Czego NIKT nie znalazl (a nie ma):

- Nowych plikow wiedzy po D-0067: NIE MA
- Nowych decyzji Tomasza po D-0067: NIE MA
- Nowych wpisow w content.db: NIE MA (tabela reels pusta)
- Sesji Hermesa z nowym materialem: sesja Codex pusta, sesja glowna to ta
- Plikow .scratch/mlodych: NIE MA

---

*Raport wygenerowany: 2026-08-06 07:15 CEST przez Henia.*
*Zlecenie od Klaudka przez Hans most (06:59).*
*NIE POPRAWIANO, NIE USUWANO, NIE COMMITOWANO.*
