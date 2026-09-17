# PREZENTER TOMASZ — KANON 0.1 (dekret Tomasza 01.09.2026)
Dekret DOSLOWNIE: "Zapisac go kolo Izabeli jako prezenter Tomasz" / "Tym samym mamy dwoch prezenterow". Werdykt na test: "Zajebiscie!!!!".
Status: DRUGI PREZENTER ROD obok Izabeli (wiedza/IZABELA_KANON_0.1.md — bez zmian). Nie zastepuje Izabeli.
## Tozsamosc
- Awatar PREZESA ROD im. Jozefa Lompy z JEGO wlasnego wizerunku i za jego zgoda (selfie Fold7 01.09.2026).
- Nazwa: Prezenter Tomasz. Mowi jako Tomasz — tresc kazdego klipu ZATWIERDZA Tomasz osobiscie (ustalenie zalogi 01.09, D-0190; Tomasz nie odrzucil).
## Wyglad (dekrety 01.09, doslownie): "Mam byc w krotkich wlosach. Bez brody." / "Mam byc w bialej koszuli z rozpietym guzikiem" / "Tlo to ogrod"
## Aktywa
- Referencja twarzy: data/awatar_tomasz/test1/ref_tomasz_720.jpg (720x1280, z Telegrama przez skrzynke Hansa). Embedding: ref_embedding.npy (jesli zapisany).
- WZORZEC ZAAKCEPTOWANY: data/awatar_tomasz/test1/omni_test1_1.mp4 (8 s, 720x1280, 24 fps, interaction v1_ChdLNUdX..., 01.09) — kandydat na <VIDEO_REF> (do 3 s) dla spojnosci wygladu; link panel: /zarty/awatar_test1/klip/omni_test1_1.mp4
- Prompt wzorcowy: data/awatar_tomasz/test1/_gen_omni.py (PROMPT) — zmieniac tylko kwestie i akcje, nie opis wygladu.
## Narzedzie i koszt
- Gemini Omni 1.1 Flash (gemini-omni-1.1-flash), Interactions API, task reference_to_video, response_format video 720p 9:16 inline; ~0,10 USD/s (46 336 tok/8 s = 0,81 USD). Venv: /root/omni_venv. Klucz: GEMINI_API_KEY (/root/.gemini/.env).
- Glos: WLASNY glos modelu Omni po polsku (Omni nie przyjmuje audio) — zaakceptowany 01.09. Klon ElevenLabs NIE jest potrzebny do czasu, az Tomasz zdecyduje inaczej.
- Bramki obowiazkowe przed pokazaniem: straznik.py (kwestia PL, usta, tozsamosc --wzorzec TOMASZ=ref_tomasz_720.jpg) + VLM 3 klatki (host, qwen2.5vl) na dekrety wygladu + brak tekstu.
## Wyniki testu #1 (01.09): polski 1.0 (whisper), usta 5.34 PASS, tozsamosc 0.65/10 trafien, VLM 3/3 dekrety, 36 s generacji.
## OTWARTE (decyzje Tomasza / testy)
- ZAMKNIETE 02.09 (dekret doslownie: 'Zaden podzial rol miedzy Izabela a prezydentem Tomaszem to nasi dwoje prezenterow i na moje widzi misie powiem ktorego uzywamy'): brak podzialu rol; ktory prezenter prowadzi rolke — wskazuje Tomasz kazdorazowo. Etykieta AI (art. 50) zostaje: plansza AI w filmie + zdanie w opisie.
- Formula jawnosci AI dla Prezentera Tomasza (u Izabeli: deklaracja w intro).
- SPOJNOSC miedzy klipami (twarz + glos): test #2 = extend w tym samym watku (previous_interaction_id) + porownanie; potem test 'nowy watek z VIDEO_REF'.
- Zakaz tematow w ustach awatara prezesa (ustalenie zalogi): przelewy, kody, spory, nagle wypadki, "prezes prosi".

## 17.09.2026 — GŁOS PREZENTERA TOMASZA BEZ OMNI (dekret D-0410, doslownie: „Kandydat 3 poprawiony od teraz jako głos Tomasz")
- Do rolek BEZ mowiacej twarzy (plansze + lektor) glos Tomasza robi KLON VoxCPM2 lokalnie, 0 zl: tools/glos_tomasz.py (modele /root/modele/voxcpm2, GGUF, CPU ~60 s na kwestie 25 slow). Przepis V2: referencja data/glos_tomasz/ref_W1_1.wav + jej tekst, seed 7, timesteps 30, cfg 2.0; wzorzec brzmienia: data/glos_tomasz/WZORZEC_V2_N0.wav.
- Historia wyboru: Chatterbox ODRZUCONY przez Tomasza („ukraiński akcent"), MOSS-Nano przekreca slowa, XTTS-v2 7/10 (licencja CPML), VoxCPM2 V2 = 7–8/10 uchem Gemini (slepy ranking 5 wersji), akcent NIE. Tomasz zaakceptowal po odsluchu.
- BRAMKA OBOWIAZKOWA przed uzyciem kazdej kwestii: whisper (tekst 1.00) + ucho Gemini pytane WPROST o akcent i bledy wymowy. Ogolne „czy naturalnie" nie jest bramka (lekcja 17.09, teczka Klaudka).
- Twarz + glos w jednym (mowiacy awatar) nadal tylko Omni (~1 USD/10 s) — decyzja Tomasza kazdorazowo.
