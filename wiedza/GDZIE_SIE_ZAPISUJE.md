# GDZIE SIĘ ZAPISUJE — JEDNO MIEJSCE NA JEDNĄ RZECZ

**Dekret Tomasza 04.08.2026 07:16:**
> „Zrobić dokładny porządek, czyli poukładać historię, żeby była kompletna wszędzie: teleport,
> second brain, github. Ponadpisywać, uporządkować. Żeby to nie było rozjebane wszędzie
> i zapisywał kto gdzie chce.
> **Wszystkie kopie prac i wszystkiego robi KLAUDEK, a HENIEK kontroluje go, żeby nie zapomniał
> i nie pomieszał, gdzie chce.**"

## PODZIAŁ ODPOWIEDZIALNOŚCI (dekret 4.08)
- **KLAUDEK ROBI** wszystkie kopie i zapisy. To jego obowiązek, nie cudzy.
- **HENIO KONTROLUJE**, czy Klaudek zapisał i czy zapisał WE WŁAŚCIWYM MIEJSCU.
- Henio NIE zapisuje za Klaudka. Zgłasza brak — Klaudek uzupełnia.
- Wyjątek: `wiedza/BRIEF_DLA_KLAUDKA.md` — to plik Henia, on go generuje (jego projekt, 4.08).

## TRZY MIEJSCA I CO DO KTÓREGO IDZIE

| co | gdzie JEDYNIE | czym zapisywać |
|---|---|---|
| **PRZEBIEG** — co się stało, w jakiej kolejności, ślepe uliczki | `TELEPORT_fabryka.md` (fabryka), `TELEPORT_HA.md` (Home Assistant) — oba W REPO | `tools/teleport.py --wpis` / `--ha --wpis` |
| **WNIOSKI** (second brain) — jak ma być, trwałe zasady | `wiedza/*.md` | ręcznie + `tools/porzadek.py` (indeks) |
| **KOPIA POZA SERWEREM** | GitHub `makol100/rod-ai-studio` | `git push origin main` |
| **DECYZJE TOMASZA** | `.scratch/decyzje_tomasza.jsonl` + `wiedza/SLOWA_TOMASZA.md` | `tools/decyzje.py --dodaj` |

## STAN PO PORZĄDKU 04.08.2026 07:16
- teleporty: **DWA** (fabryki i HA). Wcześniej leżały w **7 kopiach w 4 miejscach**.
- `/root/TELEPORT_HA.md` = **DOWIĄZANIE** do wersji w repo. Stara ścieżka działa, treść jest jedna.
  Sprawdzone zapisem przez starą ścieżkę — trafił do pliku w repo.
- `data/wiedza_kopia/archiwum/` i `/home/hermes/fabryka/` = **KOPIE AUTOMATYCZNE** dla Henia,
  synchronizowane po SHA-256 przez `tools/porzadek.py`. **NIE ruszać ręcznie** — to nie są oryginały.
- kopia sprzed porządku: `/root/HISTORIA_ZABEZPIECZONA/TELEPORT_HA_przed_porzadkiem.md`

## ZASADA
Nowe miejsce zapisu powstaje **wyłącznie decyzją Tomasza**. Nikt z załogi nie zakłada własnego
katalogu na notatki. Jeśli czegoś nie ma gdzie zapisać — pyta się Tomasza, nie wymyśla miejsca.
