# TELEPORT — Fabryka Rolek (ROD Woźniki)
**Ostatnia pełna rekonstrukcja: 08.07.2026, ~14:00 (po odkryciu że plik był nadpisywany zamiast dopisywany — patrz sekcja na końcu)**

Jeśli czytasz to jako nowa instancja Claude w nowym oknie czatu: przeczytaj całość, potem działaj tak, jakbyś był mną. Tomasz komunikuje się po polsku, pracuje z telefonu, woli gotowe działanie niż pytania — ale docenia gdy dopytasz przy realnej niejednoznaczności z konsekwencjami (patrz "Konwencje" niżej).

## ⚠️ NARZĘDZIA — PRZECZYTAJ ZANIM COKOLWIEK ZROBISZ
Connector w Claude nazywa się **`fabryka`** (NIE „fabryka-vps" — ten drugi usunięty po podwójnym wycieku sekretu). Ma TYLKO DWA narzędzia:
- `fabryka:execute_command(command, cwd?, timeout?)` — pełny bash root na VPS
- `fabryka:write_file(content, path)` — **NADPISUJE cały plik, nie dopisuje!**

**Nie ma `append_file` ani `read_file` w tym connectorze.** Żeby:
- **czytać plik** → `fabryka:execute_command("cat /sciezka")`
- **dopisać do pliku** (np. do tego właśnie pliku TELEPORT) → NIGDY nie używaj `write_file` z samą nową treścią, bo skasujesz wszystko wcześniejsze. Zamiast tego: `fabryka:execute_command('cat >> /root/rod-ai-studio/TELEPORT_fabryka.md << \'EOF\'\n\n## Nowa sekcja...\nEOF')` — prawdziwy bash append.
- **nadpisać cały plik świadomie** (np. panel.html, kod .py) → `write_file` jest OK, bo tam zawsze budujesz pełną, nową treść całego pliku.

To dokładnie ten blad ktory dzis popelnilem - uzywalem write_file do tego pliku mysląc ze dopisuje, i kasowalem ~15 wczesniejszych aktualizacji. Nie powtarzaj tego.

## Dostęp do VPS
- VPS: `157.90.155.155`, root, Ubuntu, Docker
- Repo: `github.com/makol100/rod-ai-studio`, branch `main`, zmapowane na `/root/rod-ai-studio/`
- **UWAGA dwa drzewa kodu:** `/root/rod-ai-studio/src/` = STARA/martwa kopia. Prawdziwy, działający kod (to co jedzie w kontenerze) jest w `/root/rod-ai-studio/apps/api/src/`. Zawsze edytuj tam.
- Kontener: `fabryka-api` (FastAPI, port 8000), panel pod `http://157.90.155.155:8000/panel`
- MCP server: `/root/claude-vps-mcp/mcp_server.py`, systemd `mcp-fabryka.service`, port 8765, za Caddy (`caddy-mcp` kontener), HTTPS przez sslip.io. Sekret NIGDY nie ląduje w czacie ani w tym pliku — jeśli trzeba go odczytać, robi to Tomasz sam na VPS i wkleja bezpośrednio do Ustawień → Connectors, nigdy przez mnie.

## Modele Ollama — PO DZISIEJSZEJ KONSOLIDACJI: TYLKO 2
- **Bielik-4.5B-v3.0-Q8_0** (5.1GB) — `DEFAULT_MODEL` w `ai/ollama.py`, używany gdy `generate()` woła się BEZ podanego `model=`. Robi: artykuły, scenariusze (SCENA/UJĘCIE/LEKTOR), tytuły, hashtagi. **NIETYKALNY — Tomasz wyraźnie powiedział "Bielik zostaje nieodwołalnie", nie proponuj już jego zmiany.**
- **llama3.1:8b** (4.9GB) — `PROMPT_MODEL`, używany explicite (`model="llama3.1:8b"`). Robi: prompty obrazów FLUX (`images/prompts.py`) ORAZ zadanie NAPRAW (`naprawa.py`). Wygrał przetestowany przeciwko Bielikowi i gemma3:4b (dla NAPRAW) oraz przeciwko gemma3:4b (dla obrazów, po wzmocnieniu promptu o twardy wymóg długości/zamknięcia).
- **gemma3:4b, qwen3:8b, qwen3:4b — USUNIĘTE z Ollamy dziś** (`ollama rm`), przetestowane i odrzucone:
  - gemma3:4b: OK do obrazów, ale gorszy niż llama3.1:8b (gubił duplikaty przy NAPRAW, mylił reguły botaniczne przy obrazach)
  - qwen3:8b: DYSKWALIFIKACJA SPRZĘTOWA — w praktyce 6.7GB RAM (nie 5.2GB jak plik), zepchnął system na 7.3/7.6GB, nie skończył zadania nawet po 5,5 min (prawdopodobnie "tryb myślenia" Qwen3)
  - qwen3:4b: dobra trafność (jak Llama), ale 168s na proste zadanie — za wolno na interaktywny panel
- **KRYTYCZNE — RAM (7.6GB total, 2× dziś OOM-kill z tego powodu):** Bielik + cokolwiek innego NIGDY nie mieszczą się razem. Przed KAŻDYM przełączeniem modelu jawnie zwolnij poprzedni: `curl http://localhost:11434/api/generate -d '{"model":"NAZWA_MODELU","keep_alive":0}'`. Nie wystarczy zrobić to raz na początku sesji testów — trzeba przed KAŻDYM pojedynczym przełączeniem, nawet między dwoma udanymi testami tego samego dnia (keep_alive domyślnie 5 min, łatwo o kolizję jeśli się zapomni. Dokładnie to spowodowało oba dzisiejsze OOM-kille).
- Bielik ma poprawnie skonfigurowany szablon czatu w Ollamie (Llama-3-style, `<|start_header_id|>` itd.) — sprawdzone i zgodne z oficjalnym Modelfile SpeakLeash. Jego słabość przy zadaniu "przepisz prawie bez zmian" to udokumentowana cecha KWANTYZACJI (Q8_0), nie błąd konfiguracji ("DISCLAIMER: quantised models show reduced response quality and possible hallucinations" — z oficjalnej dokumentacji SpeakLeash).

## Baza tematów (SQLite w `data/content.db`, kontener `fabryka-api`)
Stan na koniec dzisiejszej sesji: **14 kategorii, 730 tematów** (sprawdź dokładnie przez `/categories` i `/topics-db`, bo mogło się zmienić w kolejnej sesji).

Schemat `topics`: `id, category_id, tekst, uzyty_razy, ostatnio_uzyty, aktywny, miesiace, tryb_override`
Schemat `categories`: `id, nazwa, aktywna, tryb`
- `miesiace`: CSV miesięcy (np. "6,7,8") albo NULL = cały rok. `random_topic()` filtruje po oknie [bieżący miesiąc, +2].
- `tryb` / `tryb_override`: `organizm` (bohater kadru = roślina/grzyb/zwierzę) albo `sprzet` (bohater = narzędzie/urządzenie/dokument). Wybiera wariant `PROMPT_TEMPLATE` w `scenes/generator.py`. Kategorie `sprzet`: Bezpieczeństwo i Infrastruktura, Smart Ogród, Architektura Ogrodowa/Majsterkowanie, Prawo Działkowe. Reszta domyślnie `organizm`. Kompostownik i gnojówki ma 10 tematów z `tryb_override='sprzet'` (same kompostowniki/beczki), reszta tej kategorii zostaje `organizm`.

**UWAGA ID kategorii:** NIE są ciągłe (np. brakuje id=4, usunięta "Życie ROD Woźniki") — zawsze filtruj po `nazwa`, nigdy nie zakładaj sekwencji ID.

**Konwencje ustalone z Tomaszem dla nowych partii tematów (potwierdzone wielokrotnie dziś):**
- Brak prefiksu / "Nowa kategoria" = tworzysz nową kategorię
- "Do X" / "Kolejne tematy" = dołączasz do ISTNIEJĄCEJ kategorii (nie usuwasz starych)
- "Aktualizacja" / nawet literówka "Akualizacja" = **USUŃ stare tematy w kategorii + zastąp nowymi w całości** (potwierdzone wprost przez Tomasza pierwszy raz, potem stosowane konsekwentnie bez ponownego pytania)
- "Usuń kategorię z tematami" = DELETE całej kategorii i wszystkich jej topics
- Zawsze sprawdzaj obecny stan (`SELECT` przed akcją) i pokazuj co dokładnie usuwasz/dodajesz, zanim to zrobisz

Dzisiejsze partie (10 nowych kategorii rano + 3 przebudowy + 1 dodatek + 1 usunięcie popołudniu): Kwiaty w ROD, Grzyby w śląskich lasach, Iglaki (+50), Kompostownik i gnojówki (+50), Bezpieczeństwo i Infrastruktura, Smart Ogród, Prawo Działkowe, Architektura Ogrodowa/Majsterkowanie, Klasyczny Warzywniak, Ekologia/Zwierzęta/Bioróżnorodność, Co siać/co robić teraz (przebudowana 7→50), Sprawdzone triki działkowca (dołożone 7→57), Najczęstsze błędy (przebudowana 6→50), Życie ROD Woźniki (USUNIĘTA), Ciekawostki i mity (przebudowana 5→50).

## Pipeline Fabryki (temat → gotowa rolka)
1. `POST /generate-reel {prompt, scene_count, topic_id?}` → `generate_reel_endpoint` w `topics.py`
2. Jeśli `topic_id` podany: JOIN topics+categories, `tryb = tryb_override or categories.tryb or "organizm"`. Brak topic_id → domyślnie `organizm` (bezpieczne dla ręcznie wpisanych tematów).
3. `article = generate(prompt)` — Bielik (domyślny), BEZ żadnego szablonu, goły tekst leci wprost do modelu
4. `scenes = generate_scenes(article, scene_count, tryb)` w `scenes/generator.py` — wybiera `PROMPT_TEMPLATE_ORGANIZM` albo `PROMPT_TEMPLATE_SPRZET`
5. `_produce_media()`: audio (edge-tts, darmowe) → prompty obrazów (`generate_image_prompts`, llama3.1:8b, darmowe) → obrazy (fal.ai FLUX-1/dev, **KOSZTOWNE**) → napisy (fal.ai Whisper, **KOSZTOWNE**) → render (ffmpeg) → muzyka w tle

## Funkcja NAPRAW (naprawa.py + panel)
Cel: poprawić jedną scenę w istniejącej rolce bez płacenia za regenerację całości.
1. **Sprawdź** (`POST /napraw-sprawdz {reel_id, skarga}`): llama3.1:8b przepisuje CAŁY scenariusz zgodnie ze skargą użytkownika (podawanie POPRAWNEJ wartości wprost w skardze działa dużo lepiej niż liczenie na zgadywanie modelu — sprawdzone empirycznie na literówce w łacińskiej nazwie). Kod (`parse_scenes`, naprawiony pod wieloliniowy format UJĘCIE/LEKTOR) diffuje stary vs nowy scena-po-scenie. Zwraca listę zmian (`zmiana_obrazu`, `zmiana_audio` per scena) — ZERO KOSZTU, tylko lokalny model.
2. Panel pokazuje diff z checkboxami (domyślnie zaznaczone) — Tomasz może odznaczyć niechciane zmiany (model czasem dokłada szum, np. nieproszone "poprawki" wyrazów).
3. **Zastosuj** (`POST /napraw-zastosuj {reel_id, nowy_scenariusz, zaakceptowane_sceny}`): scala stary+nowy wg zaznaczonych numerów, regeneruje CHIRURGICZNIE tylko zaakceptowane sceny (obraz: fal.ai, kosztowne, TYLKO zaakceptowane+zmienione; audio+napisy: edge-tts+Whisper, TYLKO zaakceptowane+zmienione — bo napisy/Whisper TEŻ kosztują, więc nie regeneruje się audio dla wszystkich scen na wszelki wypadek), re-renderuje wideo raz na końcu.
4. `confirm()` w panelu przed Zastosuj pokazuje ile obrazów się przegeneruje (koszt).

## Panel (`apps/api/src/panel.html`)
- **01 Nowa rolka**: temat + liczba scen + Losuj temat (`/random-topic`, zapamiętuje `currentTopicId` żeby przekazać `tryb`) + Generuj rolkę
- **02 Ostatnie rolki**: karta per rolka, w nagłówku zawsze widoczne: ▶ Odtwórz (tylko gdy `status==='gotowa'`, wstrzykuje `<video>` do rbody) + 🗑 Usuń (confirm, `DELETE /reels/{id}`, kasuje cały folder z dysku, nieodwracalne). W rozwiniętej karcie: 🔧 Zgłoś problem → cały flow NAPRAW opisany wyżej.
- **03 Tematy sezonowe**: edytor kategorii/tematów
- **04 Diagnostyka serwera**: host/prompts/write status

**Krytyczne bugi znalezione i naprawione dziś w panelu (dwa oddzielne, w tym samym miejscu!):**
1. `/reels` (backend) czytał z MARTWEJ tabeli SQL `reels` (wypełnianej tylko przez stary `generate_text()`, sam tekst bez wideo) — prawdziwe rolki z pełnym pipelinem nigdy tam nie trafiały. Naprawione: `_scan_reels_from_disk()` skanuje `data/reels/NNNNNN/` bezpośrednio.
2. `loadReels()` (frontend) po tamtej naprawie WCIĄŻ pokazywał "brak rolek" — `/reels` zwraca `{status,reels:[...]}`, a JS robił `Array.isArray(CAŁY_OBIEKT)` (zawsze false) zamiast sprawdzać `.reels`. Naprawione osobno, zweryfikowane przez `node -e` symulujący dokładnie logikę przeglądarki, nie tylko surowy curl na endpoint.
**Lekcja:** przy "X nie działa w panelu" sprawdzaj OSOBNO backend (curl) i to jak frontend JS faktycznie konsumuje odpowiedź — to dwa różne miejsca na buga.

Inne naprawione dziś bugi: `_LEKTOR_RE` regex nie łapał wariantów typu "LEKTOOR"/"LEKTORA" (teraz `lekt[o]{1,2}r\w*`); `parse_scenes()` nie obsługiwał wieloliniowego formatu UJĘCIE:/LEKTOR: (etykieta i treść w osobnych liniach) — teraz śledzi "aktywne pole" i doklejaj kolejne linie; `/host/status` sprawdzał martwą ścieżkę `/app/prompts/prompts.py` sprzed reorganizacji (teraz `/app/src/images/prompts.py`).

## Otwarte wątki (nie dziś, ale nie zapomnij)
- **Publikacja FB (Etap 7):** token trzeba wyciągnąć z Node-RED (flow "Ogrodnik" na Dom HA, node `KONFIG — WKLEJ KLUCZE`), potem bramka 3-fazowa `{page_id}/video_reels`. Token NIGDY nie ląduje w czacie.
- **Apka Android:** WebView APK budowany na VPS. Nie zaczęte.
- **Balans losowania:** `random_topic()` waży tylko `1/(uzyty_razy+1)`, nie waży kategorii. Setki nowych tematów vs kilkadziesiąt starych — bez wagi per-kategoria nowe zdominują latem. Jedno zapytanie do dorobienia, jeszcze nie zrobione.
- Komentarz "schnell" nad `FAL_MODEL = "fal-ai/flux-1/dev"` w `image_backend.py` — kosmetyczna literówka w komentarzu, nieistotna.

## Zasady i konwencje ogólne
- Tomasz: telefon (Samsung), komunikacja wyłącznie po polsku, woli gotowe działanie/kod niż długie wyjaśnienia, ale docenia pytanie przy realnej niejednoznaczności z konsekwencjami (np. usunięcie danych z historią użycia)
- Poprawki pojedynczego obrazu/sceny w ISTNIEJĄCEJ rolce: NIE renderować całości od nowa — patrz sekcja NAPRAW wyżej, to jest teraz zbudowana, właściwa droga
- Zawsze commituj i pushuj na GitHub (`makol100/rod-ai-studio`, branch `main`) po każdej znaczącej zmianie — to stało się nawykiem tej sesji, kontynuuj go
- "Działka" w innych projektach Tomasza (HA) = zawsze ogród w Walding, nie mylić z Fabryką
