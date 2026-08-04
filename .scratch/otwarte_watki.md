# OTWARTE WĄTKI — TODO / do sprawdzenia / do zrobienia

Zebrane przez Zenka (audyt 04.08.2026). Lista dla Tomasza — NIE rozstrzygać samodzielnie.

Legenda:
- **ZYWE** — sprawa wygląda na aktualną, nierozwiązaną
- **MARTWE** — dotyczy rzeczy już zrobionych lub nieaktualnych

---

## 1. TELEPORT_fabryka.md:131 — Uprawnienia FB Reels
**Status: MARTWE — ZAMKNIETE 4.08 przez Tomasza**
> Tomasz 4.08 09:09: *Publikacja na Facebooku dziala, bo sam przeciez wystawiales rolki.*
> DOWOD ZMIERZONY: znaczniki publikacji przy rolkach 000085, 000087, 000088, 000090, 000091
> (daty 10-14.07) + odcinek 10010 zamkniety 4.08 jako OPUBLIKOWANY.
> Zapis w teleporcie pochodzi z 10.07, gdy uprawnienia byly niepewne — od tamtej pory
> publikacja przeszla w praktyce co najmniej 5 razy. Kolejny MARTWY WATEK UDAJACY ZYWY:
> stan poszedl do przodu, opis zostal.
> Otwarte do sprawdzenia: czy PAGE_ID 1174205105781401 ma poprawnie przypisane
> uprawnienia pages_manage_posts dla tokenu; czy plik wideo spelnia wymogi FB
> Reels (9:16, min 4s/max 60s, min rozdzielczosc 540x960)
Kontekst: integracja GitHub Actions → Facebook Reels. Nie wiadomo czy testowane.

## 2. TELEPORT_fabryka.md:445 — Bezpieczeństwo kluczy API
**Status: ZYWE**
> ### BEZPIECZENSTWO - do zrobienia
> docker-compose.yml zawiera FAL_KEY i ANTHROPIC_API_KEY plaintext; plik zostal
> wyswietlony w czacie 10.07 przy diagnostyce. Zalecana rotacja obu kluczy.
Kontekst: klucze wyciekły w czacie, nadal plaintext w docker-compose.yml.

## 3. TELEPORT_fabryka.md:1087 — Automatyzacja APK
**Status: ZROBIONE 4.08 09:14** — polecenie Tomasza: *Automatyzacja kopiowania aplikacji po kazdym zbudowaniu wykonac.*
> Zrobione INACZEJ niz mowil zapis z 15.07 i to celowo: notatka mowila *skopiowac APK do repo*, ale APK ma 2,3 MB i NIE jest sledzony w gicie (0 commitow). Wgrywanie go przy kazdym budowaniu wsadzaloby binaria do historii — to samo, czego Tomasz nie chcial przy rolkach (D-0020).
> ZAMIAST TEGO: `tools/pobierz_apk.sh` sciaga plik z wydania `apk-latest`, ktore workflow i tak juz publikuje. Timer `apk-pobierz.timer` sprawdza co godzine, wstaje po restarcie.
> Zabezpieczenia: sprawdza czy pobrany plik to naprawde APK; przy bledzie NIE rusza lokalnego; stara wersje zachowuje obok (dekret 2.08: nikt niczego nie usuwa).
> Po każdym buildzie skopiować nowy APK do data/rolka-prad/app-debug.apk
> (TODO: zautomatyzować w workflow).
Kontekst: workflow GitHub Actions dla APK — ręczne kopiowanie nie zautomatyzowane.

## 4. TELEPORT_HA.md:90 — Addony w stanie błędu
**Status: ZYWE**
> Dwa inne addony w stanie bledu: MQTT IO i AegisBot (Telegram group defender)
> - do sprawdzenia kiedys, nie dzisiaj.
Kontekst: HA, oba addony niepowiązane z niczym bieżącym, ale sygnalizują błąd.

## 5. TELEPORT_HA.md:226 — Watchdog Tailscale + sensory PV
**Status: ZYWE**
> TODO otwarte: watchdog addonu Tailscale, sensory PV (SA→.250?),
> re-pomiar unavailable (baseline 488 @ 03:0x).
Kontekst: monitoring HA — watchdog, sensory fotowoltaiki, ponowny pomiar.

## 6. TELEPORT_HA.md:326 — Sprawdzić HA Dom
**Status: MARTWE (prawdopodobnie)**
> TODO rano: sprawdzic HA Dom (barometr 8:00 nie pojdzie!); telegram
> wyslac gdy Dom wroci.
Kontekst: zapis z konkretnego dnia („rano"), HA Dom był offline ~9h.
Wygląda na jednorazowe, prawdopodobnie już sprawdzone.

## 7. wiedza/archiwum/DECYZJE_10007_jablko.md:35 — Preflight przez kontener
**Status: ZYWE (narzędziowe)**
> TODO-narzędziowe: preflight przez kontener albo insightface na host.
Kontekst: decyzja 10007 (kanarek), narzędzie do preflightu. W archiwum,
ale technicznie może być nadal potrzebne.

## 8. wiedza/FILM_OPUS5_WNIOSEK.md:33 — Remotion jako kandydat
**Status: ZYWE**
> Remotion pozwala napisać je jako kod pod konkretny odcinek. To kandydat
> do sprawdzenia, nie decyzja.
Kontekst: analiza narzędzi po Opus 5, Remotion nierozstrzygnięty.

---

## Podsumowanie
- **ZYWE: 7** (pozycje 1-5, 7-8)
- **MARTWE: 1** (pozycja 6)
- **Znalezione: 8** — Zenek zapowiadał 16; możliwe że część TODO była
  w plikach, które zostały już zaktualizowane/zmienione między audytem
  a tą chwilą, lub Zenek liczył duplikaty w data/wiedza_kopia/.

Zebrane: 04.08.2026 przez Henia (wykonującego zadanie Zenka).
