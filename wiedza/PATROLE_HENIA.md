# PATROLE HENIA — działają od 29.07.2026 (przetestowane, dlatego zapisane)

Powód: sam Henio wskazał w opinii, że działa 24/7 i nie ma ani jednego zadania cyklicznego —
„to absurd przy 24/7 za grosze". Zenek i Genek niezależnie wskazali to samo: domyślnie ma
robić monitoring i patrole. Tomasz: „Niech coś robi".

## ZASADA: WARTOWNIK MILCZY, GDY JEST DOBRZE
Wszystkie patrole chodzą w trybie `--no-agent` — to skrypt jest zadaniem, jego wyjście idzie wprost
na Telegram. Pusty wynik = cisza. **Zero kosztu modelu, zero spamu.** Odzywa się tylko, gdy coś jest nie tak.

## CO CHODZI

| zadanie | kiedy | co robi | gada? |
|---|---|---|---|
| `patrol-zasoby` | co 30 min | load vs liczba rdzeni, wolna RAM, dysk (% i GB), procesy w stanie D | tylko przy przekroczeniu progu |
| `patrol-fabryki` | co godzinę | błędy w logu API (≥3 na 500 linii), martwy log (>24 h), produkcja stojąca ≥7 dni | tylko przy znalezisku |
| `meldunek-poranny` | 7:00 czasu lokalnego | STAN → LICZBY → WNIOSEK: load, RAM, dysk, błędy w logu, ostatnia rolka | zawsze |

Progi z §2 podręcznika (opracowane przez Zenka): load > 2× liczba rdzeni, RAM < 10 % wolne,
dysk ≥ 90 % lub < 5 GB. Skrypty: `/home/hermes/.hermes/scripts/`.

## CO ZMIERZONE PRZY WDROŻENIU
- `patrol_zasoby.sh` na zdrowym systemie → CISZA. Poprawne zachowanie.
- `patrol_fabryka.sh` → najpierw BŁĄD SKŁADNI: `grep -c` przy zerze trafień drukuje 0 **i** zwraca kod
  błędu, więc zapasowe `|| echo 0` dokładało drugie zero i psuło porównanie liczbowe. Poprawione na
  `BLEDY=${BLEDY:-0}`. Po poprawce → CISZA.
- `meldunek_poranny.sh` → pełny meldunek z prawdziwymi liczbami.
- Wymuszone uruchomienie patrolu przez `hermes cron run` → `completed`, wpis w historii wykonań.

## PUŁAPKA STREFY CZASU (druga odsłona tego samego problemu)
Zadania zarejestrowane przed poprawką miały `Next run` w **+00:00**, mimo że gateway miał już
`TZ=Europe/Vienna` w drop-inie systemd. Powód: zmienna nie była w `.env` ani w `.profile` usera,
więc powłoka i harmonogram liczyły w UTC — „7:00" oznaczałoby 9:00 u Tomasza.
Naprawa: `TZ=Europe/Vienna` dopisane do `~/.hermes/.env` i `~/.profile`, gateway zrestartowany,
zadania **przerejestrowane**. Dopiero wtedy `Next run` pokazał `+02:00`.
WNIOSEK OGÓLNY: po zmianie strefy czasu istniejące zadania trzeba utworzyć od nowa — zapamiętały starą.
