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

## 4. TELEPORT_HA.md:90 — Addony w stanie bledu
**Status: MARTWE — ZAMKNIETE 4.08 09:16**
> Serwer: HA DOM (Walding). Zapis pochodzil z 08.07.
> ZMIERZONE 4.08 przez ha_get_addon(source=installed): 19 dodatkow, WSZYSTKIE uruchomione,
> zero zatrzymanych. MQTT IO ani AegisBot NIE MA na liscie — zostaly odinstalowane.
> Problem rozwiazal sie sam przez usuniecie dodatkow.
> PRZY OKAZJI ZAUWAZONE: Whisper i Piper (mowa) maja dostepne aktualizacje.
> Dwa inne addony w stanie bledu: MQTT IO i AegisBot (Telegram group defender)
> - do sprawdzenia kiedys, nie dzisiaj.
Kontekst: HA, oba addony niepowiązane z niczym bieżącym, ale sygnalizują błąd.

## 5. TELEPORT_HA.md:226 — Watchdog Tailscale + sensory PV
**Status: ZALATWIONE — decyzja Tomasza 4.08 09:20**
> Serwer: HA DZIALKA (po migracji na N150).
> ZMIERZONE 4.08 przed zamknieciem:
> - watchdog Tailscale: JUZ ZALATWIONY — stoi w tym samym zapisie, ktory go zglaszal
>   (boot=auto, watchdog=True, checklist migracji domkniety). Znacznik TODO zostal przez pomylke.
> - falownik InfiniSolar: WROCIL, 44 encje z prawdziwymi wartosciami (napiecia, prady,
>   tryb 'Solar and utility simultaneously'). Solar Assistant sam odnalazl nowy adres serwera.
> - encje niedostepne: 377 wobec 488 przy pomiarze odniesienia — spadek o 111 (o jedna piata).
>   Urzadzenia wracaly falami, zgodnie z przewidywaniem.
> Tomasz: *Ten watek uwazam za zalatwiony.*
> TODO otwarte: watchdog addonu Tailscale, sensory PV (SA→.250?),
> re-pomiar unavailable (baseline 488 @ 03:0x).
Kontekst: monitoring HA — watchdog, sensory fotowoltaiki, ponowny pomiar.

## 6. TELEPORT_HA.md:326 — Sprawdzić HA Dom
**Status: MARTWE (prawdopodobnie)**
> TODO rano: sprawdzic HA Dom (barometr 8:00 nie pojdzie!); telegram
> wyslac gdy Dom wroci.
Kontekst: zapis z konkretnego dnia („rano"), HA Dom był offline ~9h.
Wygląda na jednorazowe, prawdopodobnie już sprawdzone.

## 7. DECYZJE_10007_jablko.md:35 — Preflight przez kontener
**Status: ZROBIONE 4.08 09:30** — polecenie Tomasza: *Zrobic ten watek, jezeli jest potrzebny.*
> BYL POTRZEBNY: bez bibliotek kontrola twarzy blokuje produkcje na pierwszym kadrze
> (bramka jest fail-closed — brak narzedzia = FAIL, nie ciche przepuszczenie. To dobrze).
> ZMIERZONE PRZED: cv2 i insightface NIE BYLO ani na serwerze, ani w kontenerze —
> czyli obejscie z 17.07 (uruchomienie w kontenerze) tez juz nie dzialalo.
> ZROBIONE: opencv-python-headless + insightface + onnxruntime w kontenerze fabryka-api,
> model buffalo_l pobrany. Koszt: 0 zl, tylko miejsce na dysku (bylo 82 GB wolne).
> SPRAWDZONE BOJOWO na prawdziwych kadrach 10010: f01 — 1 twarz, pewnosc 0.75; f07 — 0 twarzy.
> KONTEKST HISTORYCZNY: kontrola dzialala normalnie przy odcinkach 10008, 10009 i 10010
> (zapisy pomiarow: Tomek 0.53-0.81, Janusz 0.38-0.61 nad progiem 0.35). Znacznik TODO
> z 17.07 zostal, choc sprawa rozwiazala sie sama — biblioteka zniknela dopiero pozniej,
> przy przebudowie kontenera.
> TODO-narzędziowe: preflight przez kontener albo insightface na host.
Kontekst: decyzja 10007 (kanarek), narzędzie do preflightu. W archiwum,
ale technicznie może być nadal potrzebne.

## 8. wiedza/FILM_OPUS5_WNIOSEK.md:33 — Remotion jako kandydat
**Status: ODRZUCONE 4.08 09:31 — decyzja Tomasza**
> Remotion = pisanie animacji jako kodu (React) zamiast skladania ffmpegiem.
> ZMIERZONE PRZED DECYZJA: uzywamy 6 rodzajow operacji (scale, zoompan, overlay, drawtext,
> crop, boxblur) w 5 narzedziach i 33 skryptach przy odcinkach. To PROSTE rzeczy —
> ffmpeg robi je dobrze. Remotion wygrywa przy animacji ZLOZONEJ (wykresy w rytm mowy,
> kilkanascie elementow naraz, szablony z podmienianymi danymi) — my tego nie robimy.
> Nasza produkcja to material GENEROWANY przez modele; montaz to cienka warstwa na wierzchu.
> Node v22 jest zainstalowany, wiec prog wejscia bylby niski — ale to nie powod, zeby brac.
> GLOSY Z LIPCA: Genek za, Zenek i Henio przeciw ('trzy nowe zaleznosci, trzy miejsca awarii').
> LEKCJA Z WD_0001: rolka zostala odrzucona nie przez slaby montaz, tylko dlatego, ze Izabela
> stala jak na zdjeciu paszportowym. Zadne narzedzie do animacji tego nie naprawi.
> WRACAMY, jesli kiedys zaczniemy robic cos zlozonego graficznie.
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

## EGO LITE — czeka na wersje Windows/Linux (od 5.08.2026)
Przegladarka dzielaca zalogowana sesje z agentem AI. Rozwiazuje realny problem: zadania
wymagajace logowania, do ktorych Klaudek nie siega (Tailscale, Tuya QR, Facebook).
Dzis TYLKO macOS. Sprawdzac lite.ego.app/roadmap i github.com/citrolabs/ego-lite/releases.
Opis: wiedza/EGO_LITE_DO_WROCENIA.md

## EGO LITE — czekamy na wersje Windows (od 5.08.2026)
`citrolabs/ego-lite` — przegladarka dzielaca zalogowana sesje z agentami AI.
Rozwiazuje realne blokady: zatwierdzanie tras Tailscale, kod QR Tuya, publikacja FB.
DZIS TYLKO macOS. Sprawdzic ponownie za jakis czas: czy doszedl Windows.
Opis i ostrzezenia: wiedza/EGO_LITE_ROZPOZNANIE.md

## POMIAR JAKOSCI PRODUKCJI — wskazany przez Zenka 5.08, NIEROZWIAZANY
Zenek (narada „czego fabryce brakuje") wskazal to jako bolaczke NAJWAZNIEJSZA i podparl
naszymi liczbami z wiedza/CENA_BLEDOW.md: 21,86 USD udokumentowanych strat, w odcinku #10009
okolo 10,88 z 13,17 USD to koszt bledow.
Proponowal `HumanSignal/label-studio` (27992 gwiazdki, Apache-2.0).
**Tomasz 5.08: NIE INSTALOWAC.**
Sprawa ZOSTAJE OTWARTA — problem jest realny, tylko rozwiazanie bylo zle dobrane.
Sedno wg Klaudka: nie brakuje FORMULARZA do oceniania (ocenia Tomasz, jeden, i robi to i tak),
tylko ocena przychodzi PO wygenerowaniu i zaplaceniu. Szukac czegos, co ocenia PRZED wydatkiem.
Mamy juz tools/bramka_oka.py (VLM: orientacja, glitche, rozmycie, pusty/podwojny obraz).
