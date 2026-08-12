# PRZEGLAD WARSZTATU ZALOGI (12.08.2026) — "czego CI brakuje do produkcji"
Zasada Tomasza: kazdy ma SWOJE narzedzia, nie dziala na cudzych.

## ZENEK (podpisany, ze sladami)
MA: kod/terminal/repo, ffmpeg, lokalny Bielik+Qwen-VL, SearXNG, kontrole (straznik/preflight/koszty), panel HTTP 200, KOMPLET aktywow Izabeli, kod Veo+pipeline foto.
BRAKI: (1) WLASNY klient generacji obrazow (droga Nano Banana przypisana Genkowi -> gdy Genek lezy, foto-rolki STOJA; chce wlasny dostep Gemini Image z tymi samymi bramkami kosztowymi); (2) kompletny powtarzalny pipeline FILMOW 16:9 (montaz jest, sklejki calosci brak); (3) jeden uruchamialny pipeline WIADOMOSCI (aktywa Izabeli sa, warsztat rozproszony). NIE WIEM: fal.ai dzis (zakaz platnych prob).

## GENEK (podpisany; wczesniej tryb awaryjny)
BRAKI z trybu awaryjnego (realne): brak dostepu do dysku w tej sciezce wywolania; kolejka modeli CLI chwilowo nie odpowiadala (3.1-pro, 3.6-flash).
BRAKI z pelnej odpowiedzi: (1) zalezy od JAKOSCI promptow/kanonu od innych (nie ma narzedzia autonomicznej interpretacji stylu serii); (2) nie tworzy sam scenariuszy/projektu awatara — wizualizacje tak, tresc nie; (3) brak modulu kontroli kompozycji 16:9 dla wideo.

## HENIO — GLOS NIEOBECNY (to tez wynik)
3 proby dzis (2x async 0 B, 1x sync timeout) — launcher jednorazowych zadan hermes -z NIESTABILNY (gateway/patrole zyja). BRAK nr 1 Henia = stabilnosc wlasnego launchera. Znane zaleznosci (z jego wczesniejszych raportow): oczy_uszy/YouTube przez Gemini (provider Genka), mozg = platny DeepSeek.

## KLAUDEK (ja)
MAM: niezalezny web_search/fetch, mostek VPS, pamiec trwala, koordynacje, Claude Code + most miedzysesyjny (zweryfikowany), konektory HA/Telegram/Drive.
BRAKI: (1) OCZY na finaly — mp4 z VPS nie obejrze natywnie, ocena wymaga uploadu Tomasza (zelazna zasada 16.07); czesciowe obejscie (kadry/straznik/oczy_uszy) idzie PRZEZ Gemini = dzialam na cudzym; (2) SLUCH — lektora oceniam liczbami, nie uchem; (3) ciaglosc 24/7 (lata: Molty).

## MOLTY (nowy)
Brak dostepu do pipeline'u i publikacji — CELOWO (pilotaz, bramki). Otwarte: sandbox (mur trusted), rola produkcyjna do decyzji.

## WSPOLNE WNIOSKI (do decyzji Tomasza)
A. Pojedynczy punkt awarii na OBRAZACH: Genek lezy => foto-rolki stoja (dzis potwierdzone). Lek: wlasny klient Gemini Image dla Zenka (ten sam cennik, bramki kosztowe bez zmian) = redundancja, 0 nowych abonamentow.
B. Do sklejenia (praca, 0 zl): pipeline 16:9 i pipeline Wiadomosci (Zenek deklaruje ze po tym jest w pelni samodzielny).
C. Naprawa launchera Henia (hermes -z) — 3 ciche pady dzisiaj.
D. Genek: staly odczyt kanonow/kart stylu (dysk read-only dla jego sciezki) + bank promptow-zwyciezcow jako lek na zaleznosc od cudzych promptow.

## WYKONANIE DEKRETU "WSZYSTKO" (12.08, ta sama sesja)
- C NAPRAWIONE: kanoniczny launcher Henia = /home/hermes/uruchom_zadanie.py (bez shellowego cytowania, log, exit-code, 1 retry); zadania w /tmp/zadania_henio/ (644). Henio PRZEMOWIL (exit=0).
- GLOS HENIA (uzupelnienie): foto-rolki = samowystarczalny; do humor/Wiadomosci brakuje: wlasny FAL_KEY (dzis tylko przez docker exec Klaudka), fal_client i whisper w jego venv, wlasne tools/veo.py. => DECYZJA E dla Tomasza.
- D DOMKNIETE: (1) genek.py +--skip-trust (CLI odzyskal warsztat po zmianie zasad trust folderu), (2) ZASADA: wywolania stylowe Genka zawsze z --material (kanony doklejane niezaleznie od CLI), (3) wiedza/BANK_PROMPTOW.md utworzony.
- BONUS: Henio dostal FIRECRAWL_API_KEY do wlasnego modulu web agenta.
- A+B W TOKU u Zenka (branch zenek-warsztat, raport .scratch/zenek_ab_raport.md): pipeline Wiadomosci juz lapie realne problemy (planowane ciecia, fail-closed bez SyncNet); przed nim testy bramki kosztowej, darmowe models.list, montaze na istniejacych parts, kontrola zalogi.

## TORCH/SYNCNET — USTALENIE (12.08)
Torch NIE wymaga instalacji: kontener fabryka-api ma 2.13.0+cpu, venv Henia 2.13.0+cu130. tools/syncnet_python/run_syncnet.py JEST i kontener widzi go przez bind pod ta sama sciezka. Droga usta_sync w pipeline Wiadomosci: docker exec fabryka-api ./venv/bin/python /root/rod-ai-studio/tools/syncnet_python/run_syncnet.py <mp4>. Zenek wpina adapter przy odbiorze.

## ODBIOR WARSZTATU A+B (12.08, wieczor) — ZAMKNIETY
- NAPRAWA STRAZNIKA UST (Klaudek): raportowany przez Zenka "brak torcha" byl BLEDNA diagnoza. Torch jest w kontenerze. Prawdziwa przyczyna: straznik_ust uruchamial syncnet z ZLEGO katalogu roboczego -> syncnet nie znajdowal wag i milczal -> status wiecznie POMINIETY. Poprawka: cwd=str(syncdir) w obu wywolaniach (_run przyjmuje teraz cwd). DOWOD PO POPRAWCE: PASS, confidence 6.639, av_offset 1 (awatar_stanislaw_powitanie_v3_pro.mp4, uruchomione w kontenerze fabryka-api).
- KONTROLA ZALOGI NA ROWNYCH PRAWACH (Henio wlasnym launcherem, Genek z --material; Zenek jako autor NIE ocenial sam siebie):
  * Bramka kosztowa zenek_obraz.py: SZCZELNA — zgodnie oba glosy (Genek wskazal wczesny return, linie 105-106). Bez --zaplac zadnego platnego zadania.
  * pipeline_wiadomosci.py: flaga --test-offline PRZEPUSZCZA eksport mimo POMINIETEJ kontroli ust (Henio: linie 58-60, "nie bug, swiadome obejscie, ale plik fizycznie powstaje"). Do pamietania przy produkcji.
  * Zadnej sciezki do wydania pieniedzy bez zgody Tomasza — potwierdzone niezaleznie przez obu.
- SPRZATNIETE: imagen-4.0-fast usuniety z MODELE w zenek_obraz.py (martwy 404), z komentarzem ostrzegawczym.
- DECYZJA TOMASZA 12.08: GLOS IZABELI ZOSTAJE KANONICZNY (ElevenLabs v3 przez fal.ai, voice Charlotte) — nie schodzimy na darmowy edge-tts mimo kosztu; glos to znak rozpoznawczy postaci.
- OTWARTE (czeka na Tomasza): pierwszy platny odcinek Izabeli przez nowy pipeline — wymaga adaptera platnego TTS+awatara, dzis --zaplac twardo STOP.
