# WZÓR MAP ROD Woźniki (zatwierdzony przez Tomasza 03.09.2026)

Ten układ i paleta są **kanonem** dla wszystkich map ogrodu (etapy, ZK, kable, przyszłe mapy).
Nie zmieniać bez decyzji Tomasza.

## Pliki
- `baza_mapy_WZOR.py` — kopia zatwierdzonej bazy (kod rysujący). Źródło robocze: `tools/mapa_rod/baza_mapy.py`.
- `MAPA_OGRODU_WZOR.jpg` — wygląd docelowy (1920×1080).

## Co jest kanonem (ustalenia Tomasza z 03.09)
1. **Paleta JASNA** (barwy strony ROD): tło krem `#fffdf6`, działki `#eaf3e4` z obrysem `#c3d9b8`, alejki `#e6ddc4`, tekst `#1f3a29`.
2. **Parkingi tym samym odcieniem**: PARKING NR 1 i PARKING NR 2 → `PARK_KOL #f0e6b8`, obrys `#d4c176`.
3. **Plac = JEDEN scalony obszar** (nie osobne kafle): parking nr 1 obejmuje kolumny 0–2 rzędu R4 **plus pas alejki środkowej pod nim**; miejsca parkingowe zaznaczone kreseczkami.
4. **Dom Działkowca** (czerwony `#f2d9d4`, obrys `#c0392b`, oznaczenie „0"): leży NA placu, w kolumnie 1, i **sięga w prawo do połowy szerokości kolumny nad działką 36**.
5. **Proste, ostre krawędzie** — bez zaokrągleń (`rectangle`, nie `rounded_rectangle`).
6. Układ rzędów i numeracja działek 1–51 **bez zmian** (numeracja biegnie wężem: 1→9, 10→18, 19→27, 28→33, 34→42, 43→51).
7. Granica północna ukośna; nad rzędem 43–51 parking nr 2.

## Jak używać
Wszystkie generatory map (`mapa_ogrodu.py`, `mapy_zk.py`, `mapy_etapy.py`) importują `baza_mapy.rysuj_baze()` — więc dziedziczą ten wzór automatycznie.
Przy nowej mapie: `from baza_mapy import rysuj_baze` i rysować swoje elementy na wierzchu.

## Historia poprawek (03.09.2026, Tomasz)
- „podociągaj do prostych linii" → zaokrąglenia usunięte
- „Dom działkowca jest za duży" / „mój czerwony to Dom, reszta to parking" → Dom w środku, parking wokół
- „pod działką 24 jest parking", „plac to plac, rzędy nie ruszaj" → plac scalony, numeracja nietknięta
- „alejka nad 19 20 21 to też część placu" → pas alejki włączony w parking
- „scal parking żeby wyglądało jednym kolorem" → jeden blok zamiast kafli
- „ten sam odcień co parking nr 1" → parking nr 2 ujednolicony
- „przedłużyć dom do połowy działki 36" → dom poszerzony
- 04.09.2026 Tomasz: „Zapisz to jako główna mapa, te przejścia zrób troszeczkę cieńsze" → do kanonu dochodzą 3 PRZEJŚCIA POPRZECZNE (wąskie pomarańczowe pasy w szczelinie między kolumnami, rysowane w rysuj_baze): 36|37 Północna→Środkowa, 21|22→16|15 Środkowa→Południowa, 43|44 Północna→Parking nr 2; wszystkie mapy dziedziczą je automatycznie
