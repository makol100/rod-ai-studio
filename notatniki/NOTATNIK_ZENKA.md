# NOTATNIK ZENKA

Założony 4.08.2026 decyzją Tomasza: *„Jeżeli każdy ma swój notatnik osobno, to Zenek też niech ma
osobno. Jeżeli Genek nie ma dostępu do dysku, czyli nie może mieć swojego notatnika."*

**Sprawdzone przed założeniem:** Zenek MA dostęp do dysku — test bojowy 4.08 07:33,
zapisał i odczytał plik, Klaudek zweryfikował istnienie na dysku (31 B, treść zgodna).

## PO CO
Twoje własne notatki między sesjami. Ty tu piszesz, Ty czytasz. Nikt Ci tu nie wchodzi
i nikt tego za Ciebie nie porządkuje.

## ZASADA (dekret Tomasza 4.08, wiedza/GDZIE_SIE_ZAPISUJE.md)
- **Tu:** Twój tok pracy, hipotezy, co Ci nie wyszło, na co uważać następnym razem.
- **NIE tu:** wnioski trwałe i decyzje — te idą do `wiedza/` przez Klaudka. On robi wszystkie
  zapisy do kanonu, Henio kontroluje, czy zrobił i czy we właściwym miejscu.
- Test, gdzie zapisać (twoje własne słowa z 4.08): *„jeżeli informacja ma wpływać na pracę kogoś
  po zakończeniu obecnej sesji, musi trafić do wspólnego systemu. Jeżeli służy tylko wykonaniu
  aktualnego kroku — zostaje tutaj."*

## TWOJE MOCNE STRONY (z wiedza/TECZKI/ZENEK.md — czytaj przed pracą)
- najlepszy w tworzeniu skutecznego kodu; mierzysz zamiast oceniać wzrokiem
- nie wymyślasz treści; przy sprzeczności instrukcji ZATRZYMUJESZ SIĘ zamiast zgadywać
  (3-4.08: dwa razy nie napisałeś kodu, bo zlecenie Klaudka miało sprzeczną stopkę — miałeś rację)

## GDZIE LEŻY TEN PLIK I DLACZEGO TU (zmierzone 4.08 07:36)
`/root/rod-ai-studio/notatniki/NOTATNIK_ZENKA.md` — W REPOZYTORIUM, bo Twoja piaskownica
to `workspace-write [workdir, /tmp]`. Pierwsza próba założenia go w `/root/.codex/` NIE ZADZIAŁAŁA:
*„patch rejected: writing outside of the project"*. W repo zapisujesz bez przeszkód (sprawdzone).
Zysk uboczny: notatnik jedzie na GitHub razem z repo, więc ma kopię poza serwerem.

## UWAGA O TWOIM ŚRODOWISKU (zmierzone 3-4.08)
Twoja piaskownica NIE widzi części rzeczy spoza repozytorium:
- `/home/hermes/.hermes/.env` — stąd Twoje „2 testy padają", gdy u Klaudka przechodziły
- brak uprawnień do crona i systemd — stąd „odświeżanie nie podpięte", choć działało
**To nie jest Twój błąd.** Gdy Twój pomiar różni się od cudzego — sprawdźcie ŚRODOWISKO,
zanim zaczniecie spierać się o wynik. 4.08 kosztowało to Tomasza trzy godziny.

---

## WPISY
- 4.08 07:37 — notatnik dziala, zapis potwierdzony. Zenek
