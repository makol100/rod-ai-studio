# ZADANIE (Henio, prawa reka): jak nowy STAN ma sie do CALEGO ekosystemu pamieci — i czy w ogole potrzebny

Masz dostep do dysku — PRZEJRZYJ pliki, nie zgaduj. Podpisany glos, ze sladem. To idzie do Tomasza.

## NOWY STAN (oceniany)
- Spec: `.scratch/spec_pamiec_stan.md`. Kod: `tools/pamiec_stan.py` (test `tests/test_stan.py` zielony).
- Zamysl: pamiec KROTKOTRWALA sesji. Duze wyniki -> pliki `.scratch/refs/<agent>/<node_id>.md`; w kontekscie zostaje graf Mermaid stanu zadania (co zrobione/w toku/bloker) z `node_id`; drill-down zwraca surowy dowod. Wariant 3 = przestrzenie per agent. NIE dotyka `wiedza/`.
- Cel: po kompakcji okna Klaudek odtwarza stan + dowody bez wklejania calej historii.

## ISTNIEJACY EKOSYSTEM PAMIECI (przejrzyj KAZDY)
- `teleport.py` + `TELEPORT_fabryka.md` (283KB, PRZEBIEG: co sie stalo i dlaczego) + `/root/TELEPORT_HA.md`
- `decyzje.py` (rejestr decyzji Tomasza, pole "zastepuje")
- `wiedza/` (WNIOSKI: jak ma byc) + przewodniki INDEX/START/GDZIE_SIE_ZAPISUJE/ARCHITEKTURA/PROCEDURY
- HANS (Twoj, Henio): 9 logow w `.scratch/hans/` — `most.jsonl` (komendy MCP mostu), `dziennik.jsonl` (457KB), `oczy.jsonl` (159KB), `glosy.jsonl`, `meldunki.jsonl`, `limit.jsonl`, `zmiany.jsonl`, `proby_zapisu_henia.jsonl`, `ucho_awarie.jsonl`; serwisy: `hans-oczy` (co 15 min zrzut, Genek) + `hans-ucho` (nasluch Telegram)
- `meldunek.py` + `audyt_meldunku.py`, `zmiany.py` (odcisk plikow przed/po), `TECZKI/`

## ROZSTRZYGNIJ (konkretnie, ze sladem)
1. Jak STAN ma sie do KAZDEGO elementu: co DUBLUJE, co UZUPELNIA. SZCZEGOLNIE sprawdz `hans-oczy` (przeczytaj `hans_oczy.py` i `oczy.jsonl` — co dokladnie zapisuje co 15 min? stan zadania czy stan systemu/HA?), `teleport` (przebieg), `most.jsonl` (komendy).
2. Czego Klaudek NIE UWZGLEDNIL projektujac STAN (luki w spec).
3. CZY STAN JEST POTRZEBNY obok tego, co juz jest? Jesli TAK — co konkretnie dodaje, czego nie ma ZADEN istniejacy mechanizm. Jesli NIE — ktory istniejacy mechanizm juz to pokrywa.
4. Jesli potrzebny: jak spiac z Hansem (drill-down do `most.jsonl`) i reszta, zeby NIE dublowac.

Rozbieznosc/watpliwosci zostaw widoczne. Nie wygladzaj.
