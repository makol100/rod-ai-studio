# RAPORT HENIA — ZADANIE 3: CZY NARZĘDZIA MOGĄ SAME WYKRYWAĆ MARTWĄ WIEDZĘ?

Data: 04.08.2026 02:28 CEST

## ODPOWIEDŹ: CZĘŚCIOWO TAK, ALE NIE W PEŁNI

Moje narzędzia mogą wykrywać NIEKTÓRE typy nieaktualności — mechaniczne, sprawdzalne
bez rozumienia znaczenia. Nie mogą wykrywać nieaktualności semantycznej, która wymaga
zrozumienia, co plik opisuje i porównania tego ze stanem faktycznym.

---

## CO JUŻ WYKRYWAM (automatycznie)

### 1. Kod bez powiązania w wiedzy (i odwrotnie)

`hans.py --niedokonczone-slady` sprawdza:
- Czy każdy plik `tools/*.py` ma odpowiadający wpis w `wiedza/*.md` (po nazwie i słowach kluczowych)
- Czy każdy plik `wiedza/*.md` o narzędziach ma odpowiadający plik w `tools/*.py`

**CO TO ŁAPIE:** kod zmieniony bez aktualizacji dokumentacji. Wzorzec Klaudka: zmienia
`tools/xyz.py`, zapomina zaktualizować `wiedza/XYZ.md`.

**CZEGO TO NIE ŁAPIE:** błędnych ścieżek WEWNĄTRZ plików wiedzy. Np. ARCHITEKTURA.md
pisze `src/zarty.py`, a plik jest w `apps/api/src/zarty.py`. Funkcja nie sprawdza,
czy ścieżki wymienione w tekście wiedzy istnieją na dysku.

### 2. Środowisko Henia

`hans.py --srodowisko-henia` sprawdza:
- Czy model to PRO (nie FLASH)
- Czy limit pamięci nie jest przekroczony
- Czy uprawnienia zapisu do repo działają

**CO TO ŁAPIE:** problemy z moim własnym środowiskiem.

**CZEGO TO NIE ŁAPIE:** problemów w plikach wiedzy.

### 3. Kontrola dzienników

`hans.py --dzienniki` (automatycznie dołączane do wszystkich wywołań Hansa):
- Czy teleporty nie mają zaległości >1 dnia

---

## CZEGO NIE WYKRYWAM — I DLACZEGO

Poniższe rozbieżności wykryłem RĘCZNIE w trakcie tego zadania. Żadne z moich narzędzi
by ich nie znalazło:

### A. Błędne ścieżki wewnątrz plików wiedzy

PRZYKŁAD: ARCHITEKTURA.md linia 61: `Moduł \`src/zarty.py\``
STAN FAKTYCZNY: plik jest w `apps/api/src/zarty.py`

DLACZEGO NIE WYKRYWAM: `sprawdz_niedokonczone_slady` porównuje nazwy plików i słowa
kluczowe między katalogami `tools/` i `wiedza/`, ale NIE parsuje ścieżek wymienionych
w tekście plików .md i NIE weryfikuje ich istnienia na dysku.

### B. Nieaktualne nazwy modeli/usług

PRZYKŁAD: ARCHITEKTURA.md linia 14: `Qwen3:14b`
STAN FAKTYCZNY: jedyny model Qwen to `qwen2.5vl:7b`

DLACZEGO NIE WYKRYWAM: wykrycie tego wymagałoby:
1. Sparsowania nazw modeli z plików .md
2. Odpytania API Ollama o dostępne modele
3. Porównania
To jest MOŻLIWE technicznie — ale wymaga dedykowanej funkcji, której nie ma.

### C. Zmiany procedur i dróg

PRZYKŁAD: PROCEDURY.md linia 7: `silnik=\"fal-ai/nano-banana-pro\"`
STAN FAKTYCZNY: GENEROWANIE_OBRAZU.md (01.08) ustanawia Genka jako drogę główną.

DLACZEGO NIE WYKRYWAM: to jest zmiana SEMANTYCZNA — plik A mówi "używaj X", nowszy
plik B mówi "używaj Y". Wykrycie wymaga zrozumienia, że A i B mówią o tym samym
i że B jest nowsze. To rozumowanie, nie mechaniczny test.

### D. Nieaktualne statusy

PRZYKŁAD: ARCHITEKTURA.md: `Fabryka Żartów (Droga B — w budowie, 15.07)`
STAN FAKTYCZNY: 7 odcinków wyprodukowanych, 10010 opublikowany i zamknięty.

DLACZEGO NIE WYKRYWAM: wymaga zrozumienia znaczenia frazy "w budowie" i porównania
z zawartością `data/zarty/` i gitem. To rozumowanie, nie prosty test.

---

## CO MOŻNA BYŁOBY DODAĆ (jeśli Tomasz zechce)

### Wykrywanie A (błędne ścieżki) — DA SIĘ

Można dodać funkcję, która:
1. Parsuje wszystkie ścieżki w formacie \`ścieżka/do/pliku\` z plików .md
2. Sprawdza `os.path.exists()` dla każdej
3. Raportuje brakujące

To jest mechaniczne i wykonalne. Nie wymaga AI — to prosty skrypt.

### Wykrywanie B (modele) — DA SIĘ CZĘŚCIOWO

Można sprawdzać nazwy modeli Ollama względem `ollama list`. Ale tylko dla modeli,
które mają ustalony format nazwy.

### Wykrywanie C i D (semantyka) — NIE DA SIĘ AUTOMATYCZNIE

Wykrycie, że procedura jest nieaktualna, albo że status "w budowie" jest fałszywy,
wymaga ZROZUMIENIA tekstu. To jest właśnie to, co zrobiłem w tym zadaniu ręcznie —
i żaden prosty skrypt tego nie zastąpi. Trzeba by porównywać każdy plik .md z każdym
nowszym plikiem .md i oceniać, czy opisują to samo — to zadanie dla LLM, nie dla regexpa.

---

## WNIOSEK KOŃCOWY

**Nie mogę uczciwie powiedzieć, że moje narzędzia same wykryją martwą wiedzę.**
Wykryją kod bez dokumentacji (--niedokonczone-slady) i problemy środowiska
(--srodowisko-henia). Ale rozbieżności, które znalazłem w ARCHITEKTURA.md
(błędna ścieżka, nieaktualny model, zmieniona droga, fałszywy status) —
żadna nie zostałaby wykryta automatycznie.

To NIE JEST wina projektu Hansa. Hans został zaprojektowany do wykrywania
niedociągnięć Klaudka w PROWADZENIU dzienników i narad — i to robi dobrze.
Wykrywanie martwej wiedzy to OSOBNE zadanie, wymagające albo:
- dedykowanego skryptu (dla mechanicznych testów: ścieżki, modele)
- albo okresowego przeglądu przez załogę (dla semantycznych: procedury, statusy)

Nie będę udawał, że mam narzędzie, którego nie mam.

Podpis: HENIO
