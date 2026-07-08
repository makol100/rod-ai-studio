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

## MAPA POŁĄCZEŃ (08.07.2026)
Wizualny diagram calej architektury (nie tylko Fabryki - takze HA Dom/Dzialka/FB/Telegram) zapisany jako `/root/MAPA_POLACZEN.html` (poza tym repo, bo dotyczy calosci). Aktualizuj razem z TELEPORT_HA.md kiedy zmieni sie architektura.

## PUBLIKACJA FB PRZEZ N8N (08.07.2026) - ZBUDOWANE, NIEAKTYWNE
n8n workflow "Fabryka Rolek - Auto Publikacja FB" (id APQh4e32ngf2zlRj) - 7 wezlow, kompletny pipeline: cron pon/sr/pt 17:00 -> /random-topic -> /generate-reel (timeout 20min) -> filtr status=ok -> FB 3-fazowy upload (hosted URL, FB sam sciaga plik z /reels/{id}/video) -> publikacja z opisem.

n8n API key zapisany w /root/.n8n_api_key (chmod 600) - uzywaj `N8N_KEY=$(cat /root/.n8n_api_key)` w naglowku X-N8N-API-KEY.

Credential "Facebook Page Token (ROD Wozniki)" (id JqZNdgyrpWXTCyFS, typ httpQueryAuth, ograniczony do graph.facebook.com/rupload.facebook.com) ma placeholder "WKLEJ_TUTAJ_TOKEN_Z_NODE-RED" - Tomasz musi wejsc w n8n UI (Settings -> Credentials albo bezposrednio z node'a) i wkleic prawdziwy token z Node-RED (flow Ogrodnik, node KONFIG).

**PRZED AKTYWACJA:** przetestowac recznie (Execute workflow w UI) z wypelnionym tokenem, sprawdzic czy realnie posypie sie na FB, dopiero potem workflow.active=true. Workflow celowo utworzony jako NIEAKTYWNY zeby nic nie posz≥o samo na prawdziwa strone spolecznosci przed weryfikacja.

Otwarte do sprawdzenia: czy PAGE_ID 1174205105781401 ma poprawnie przypisane uprawnienia pages_manage_posts dla tokenu; czy plik wideo spelnia wymogi FB Reels (9:16, min 4s/max 60s, min rozdzielczosc 540x960 - Ken Burns 1080x1920 z pipeline'u powinien spelniac).

## SLOWA-KLUCZE OD TOMASZA (ustalone 08.07.2026)
- **"Update wszedzie"** = zaktualizuj TELEPORT (ten plik + TELEPORT_HA.md + MAPA_POLACZEN.html jesli dotyczy) ORAZ wypchnij na GitHub. Oba naraz.
- **"DYSKUSJA"** = zatrzymaj wszelkie akcje (generowanie, publikacja, edycje), tylko rozmawiaj, czekaj na dalsze wyrazne instrukcje zanim cokolwiek zrobisz.

## NAPRAWA: Bielik czasem wypluwal spam emoji zamiast artykulu (08.07.2026)
Zrodlo: proba generalna, rolka 000060 - article.md = powtarzajacy sie ciag emoji, scenes.txt = zupelnie niezwiazany temat (pomidory). generate() w ai/ollama.py nie ustawial repeat_penalty w ogole - klasyczna przyczyna petli powtorzen w LLM, nasilona przez losowosc probkowania bez wymuszonej temperatury.

Test: dokladnie ten sam prompt na SUROWYM Ollama (bez fixu) - 1 z 2 prob sie wysypala (emoji spam), 1 wyszla czysto. Awaria byla LOSOWA, nie deterministyczna dla tego promptu.

Fix: dodano repeat_penalty=1.15 jako domyslny parametr generate() (nadpisywalny, jak temperature). Po fixie: 3/3 czystych wynikow na tym samym prompt (mala proba, ale mechanizm sie zgadza - repeat_penalty wprost adresuje ten typ degeneracji).

Kod: /root/rod-ai-studio/apps/api/src/ai/ollama.py, funkcja generate(). Restart fabryka-api wykonany po zmianie.

UWAGA: to zmniejsza ryzyko, nie eliminuje go w 100% (kwantyzacja Q8_0 ma udokumentowana niestabilnosc per SpeakLeash). Jesli spam emoji wroci mimo fixu, rozwazyc: wyzsza wartosc repeat_penalty (1.2-1.3) albo wymuszona nizsza temperature.

## TESTY + ALARM W PANELU (08.07.2026)
Test skutecznosci repeat_penalty: 23/23 czystych wynikow (3 wczesniejsze + 20 w jednej serii, ten sam prompt co wywolal oryginalna awarie). Uczciwa interpretacja: to NIE dowodzi 99.9% (na to trzeba by tysiecy prob), ale to mocny sygnal ze fix realnie dziala.

Zbudowany system alarmowania (dlugoterminowe rozwiazanie zamiast jednorazowego testu):
- has_repetition_loop(text) w ai/ollama.py - wykrywa czy fragment tekstu dl. 15+ znakow powtarza sie 3+ razy (ogolne, lapie emoji-spam I przyszle petle tekstowe)
- generate_reel() w pipeline.py sprawdza TERAZ artykul i scenariusz po kazdym etapie; jesli wykryje problem, zapisuje WARNING.json w folderze rolki (data/reels/NNNNNN/WARNING.json) z detalami ktory etap i fragment
- _scan_reels_from_disk() w topics.py zwraca teraz pole "warning": true/false per rolka
- panel.html: nowy badge-warn (czerwony, "⚠️ Sprawdz tresc") obok statusu, widoczny gdy r.warning=true
- Rolka 000060 oznaczona retroaktywnie WARNING.json (to ta zepsuta - emoji spam + off-topic scenariusz o pomidorach)

To NIE wykrywa drugiego problemu z rolki 060 (scenariusz niezwiazany tematycznie z promptem) - to osobny, trudniejszy problem (wymagalby sprawdzania spojnosci semantycznej, nie tylko powtorzen). Zostaje otwarte jesli sie powtorzy.

## WDROZONE Z DYSKUSJI (08.07.2026, po probie generalnej #060/#061)

### 1) Osobna sciezka "Zapowiedz serii" (opcja C)
Nowa tabela `zapowiedzi` w content.db, calkowicie niezalezna od categories/topics:
`id, tresc_promptu, utworzony, uzyty_razy, ostatnio_uzyty, reel_id`

Funkcje w db/database.py: init_zapowiedzi_db(), add_zapowiedz(), list_zapowiedzi(), oznacz_uzyta_zapowiedz().
Endpointy w topics.py: GET/POST /zapowiedzi, POST /zapowiedzi/{id}/uzyj.
Panel: nowy dropdown "Zapowiedz serii" nad polem tematu w sekcji 01. Wybor wypelnia prompt + ustawia currentZapowiedzId (analogicznie do currentTopicId). Po udanym wygenerowaniu automatycznie woła /uzyj z reel_id wynikowej rolki.

Retroaktywnie dopisane: odcinek 1 (id=1, reel 000050 - UWAGA, dokladny oryginalny prompt NIEZNANY, tresc to rekonstrukcja z scenariusza, oznaczone w tekscie), odcinek 2 (id=2, reel 000061 - dokladny prompt znany, uzyty dzisiaj).

### 2) Bramka walidacji PRZED kosztownym etapem (fal.ai)
Zrodlo: rolka 000061 - zdublowany caly scenariusz (9 scen -> 18), zabladzony token <|start_eval_id|>, samo-ocena modelu "### Ocena" wpisana do wyniku. Poprzedni alarm (has_repetition_loop) to WYKRYL, ale nie zatrzymal - pipeline poszedl dalej i wygenerowal 18 obrazow zamiast 9 (podwojny koszt fal.ai).

Nowa funkcja validate_scenario(scenes_text, requested_count) w scenes/generator.py sprawdza:
- zabladzone tokeny specjalne (<|...|>)
- komentarz metatekstowy modelu ("### Ocena", "spelnia wszystkie kryteria" itp.)
- POWTORZONE NUMERY SCEN (dziala nawet bez podanego scene_count - kluczowe, bo #061 bylo generowane z "Auto")
- jesli scene_count byl podany: czy liczba unikalnych scen sie zgadza

Wpiete w generate_reel() (pipeline.py) MIEDZY generowaniem scen a _produce_media() - jesli cokolwiek wykryte, zapisuje scenes.txt + WARNING.json z detalami, ustawia status="zatrzymano_walidacja", i **zwraca BEZ wywolania _produce_media()** - zero kosztu fal.ai. To rozni sie od has_repetition_loop (miekki warning, pipeline idzie dalej) - validate_scenario to TWARDA bramka.

Przetestowane na prawdziwym zepsutym scenariuszu z 000061: wszystkie 3 problemy poprawnie wykryte.

Restart fabryka-api wykonany po wszystkich zmianach, panel+endpointy+JS zweryfikowane dzialajace.

## PRAWDZIWY PASEK POSTEPU - ZBUDOWANY I ZWERYFIKOWANY NA ZYWO (08.07.2026)
Nie mozna bylo zmienic /generate-reel na async (n8n zaleza od blokujacego wywolania) - dodano OSOBNY endpoint:
- POST /generate-reel-async - tworzy folder, odpala generate_reel() w watku (threading.Thread daemon), zwraca {reel_id, status:"started"} NATYCHMIAST (zmierzone: 0.014s)
- GET /reel-status/{reel_id} - czyta status.json z folderu rolki
- _write_status(folder, etap, extra) w pipeline.py - zapisuje PRAWDZIWY aktualny etap w 8 punktach przejscia (sceny/lektor/obrazy z i/total/napisy/render/muzyka/gotowe/blad/zatrzymano_walidacja)
- generate_reel() przyjmuje teraz opcjonalny `folder` (jesli podany, nie tworzy nowego - pozwala callerowi znac reel_id z gory)

Panel: STAGES w panel.html poprawione na PRAWDZIWA kolejnosc wykonania (Sceny->Lektor->Obrazy->Napisy->Render->Muzyka, nie zalozona Sceny->Obrazy->Lektor). startLine()/lineDone()/lineError() juz nie symuluja czasu - startStatusPolling() odpytuje /reel-status co 1.5s, mapuje etap->indeks przez STAGE_INDEX, pokazuje prawdziwe i/total dla obrazow. finishGeneration() pobiera finalne dane z /reels po zakonczeniu (spojne pola z reszta panelu).

ZWERYFIKOWANE NA ZYWO (nie zalozone) - pelny przebieg rolki 000062 (prompt zapowiedzi #2, drugi raz uzyty):
0.014s odpowiedz async -> status "sceny" -> "lektor" -> "obrazy" {i:8,total:9} (zgodne z logami co do 1) -> "napisy" -> "render" -> "gotowe" {video: sciezka} zgodna z prawdziwym plikiem na dysku (19.8MB). 9 obrazow, NIE 18 - ten przebieg nie mial pelnej duplikacji scenariusza (tylko drobne powtorzenie zlapane przez miekki alarm, poprawnie przepuszczone przez twarda bramke).

Zasada z Dyskusji: "weryfikacja nie halucynacja" - kazdy etap tej funkcji sprawdzony osobno przeciwko prawdziwym logom/plikom przed uznaniem za dzialajacy.

## NAZEWNICTWO DROG GENEROWANIA (08.07.2026, decyzja koncowa)
Ustalone oficjalne nazwy dla dwoch glownych drog prompt->rolka (dla sciezki "Zapowiedz serii"):

**Droga #1** = tryb_jezykowy="pl" (domyslny) - Bielik pisze artykul i scenariusz po polsku bezposrednio. Uzywana tez przez wszystkie zwykle tematy z bazy kategorii/tematow (tam tryb_jezykowy zawsze="pl", niezmienny).

**Droga #2** = tryb_jezykowy="en_pl" - ZWYCIESKA wersja po testach (test_v4, Przebieg 1, najlepszy wynik ze wszystkich probek). WYMAGA promptu napisanego OD RAZU PO ANGIELSKU (nie polskiego z owijka - to zostalo odrzucone jako gorsze rozwiazanie). Llama pisze szkic i scenariusz po angielsku -> twarda bramka -> obrazy (Llama+fal.ai) -> tlumaczenie TYLKO lektora (Bielik) -> audio/napisy/render/muzyka na przetlumaczonym scenariuszu.

Zapowiedzi w bazie: #1 i #2 po polsku (dla Drogi #1), #3 po angielsku (dla Drogi #2). Wszystkie trzy ZACHOWANE, nic nie skasowane z tej ani wczesniejszych decyzji.

## NAPRAWY DROGI #2 + MONITORING SERWERA (08.07.2026, wieczor)

### Bug: OOM przy tlumaczeniu (rolka 000065)
_translate_lektor_to_pl() wolala Bielika bez zwolnienia Llamy najpierw (Llama byla wlasnie uzywana do promptow obrazow). Potwierdzony OOM-kill w dmesg (PID 938247). Naprawione: dodano _unload_model(PROMPT_MODEL) na poczatku funkcji.

### Bug: "kalarepa" w promptach obrazow (POWAZNY, dotyczy OBU drog)
SINGLE_SCENE_HEADER (images/prompts.py) ma sekcje "Context-aware plant rules" z przykladowymi warzywami (kalarepa, koper, czarna rzodkiew...) dla Drogi #1. Kalarepa ma najdluzszy/najbardziej szczegolowy opis ze wszystkich przykladow. Dla tematow NIEWARZYWNYCH (jak zapowiedzi, iglaki, grzyby) model czasem (5/9 scen w tescie 000065) "przyczepia sie" do tego przykladu zamiast czytac wlasciwa tresc sceny podana na koncu prompta. POTWIERDZONE ze to nie problem danych/kodu - blok {scene} przekazywany do modelu byl w 100% poprawny we wszystkich 9 przypadkach, to czysto kwestia jak model reaguje na dlugi prompt z konkurencyjnym przykladem.

Naprawa dla Drogi #2: nowa funkcja generate_image_prompts_czysty() + SINGLE_SCENE_HEADER_CZYSTY (images/prompts.py) - BEZ sekcji "context-aware plant rules". _produce_media_en_pl() teraz uzywa tej czystej wersji. Droga #1 NIETKNIETA (generate_image_prompts() oryginalny, z przykladami - tam sa uzyteczne dla prawdziwych tematow warzywnych).

Test na tym samym scenariuszu (000065): 0/9 kalarepa (bylo 5/9). ALE ujawnily sie 2 NOWE, mniejsze problemy:
- Scena z "gardener's hand watering" - model ODMOWIL wygenerowania prompta (konflikt z zasada "nigdy nie wspominaj ludzi/rak") - OTWARTE, nie naprawione
- Scena z logo - model doslownie wpisal etykiete "UJECIE:" jako wyryty napis w scenie (kosmetyczne)

### NOWE: /system-health + zywe paski w panelu
Endpoint GET /system-health (topics.py) czyta /proc/meminfo (RAM), os.getloadavg() (CPU, przyblizone jako %load1/cpu_count), shutil.disk_usage (dysk). Panel: 3 poziome paski (RAM/CPU/Dysk) pod statystykami, kolor zielony/zolty(>70%)/czerwony(>90%), odswiezane co 5s. Zbudowane po serii dzisiejszych OOM-killi - Tomasz chce to widziec na biezaco bez SSH.

### Znana usterka UI (niezalatwiona): "w trakcie" dla zatrzymanych walidacja
_scan_reels_from_disk() pokazuje "w trakcie" dla KAZDEJ rolki bez video pliku - nie rozroznia "realnie jeszcze pracuje" od "zatrzymana na bramce walidacji, juz skonczona z problemem". Myli uzytkownika (rolka 064 wyglada jak wciaz dziala). DO NAPRAWIENIA: osobny status w liscie dla zatrzymano_walidacja.

Rolka 000065: nadal PAUZOWANA w polowie (obrazy+tlumaczenie zrobione ze starym, zepsutym tlumaczeniem grzyba - NIE ukonczona z nowym czystym promptem obrazow ani poprawiona botanika. Do decyzji: dokonczyc od nowa czy zostawic jako przypadek testowy.

## POPRAWKA: naprawde czysty prompt obrazow dla Drogi 2 (08.07.2026)
Pierwsza wersja "czysta" usuwala tylko sekcje przykladow warzyw, ale ZOSTAWIALA inne reguly (m.in. "nigdy nie wspominaj ludzi/rak") - to spowodowalo NOWY problem: model odmawial generowania prompta dla scen ze wzmianka o dloni ("I cannot generate... against your strict rules").

Naprawione ostatecznie: SINGLE_SCENE_HEADER_CZYSTY skrocony do absolutnego minimum - tylko dlugosc/format/koncowe zdanie, ZERO dodatkowych regul (zadnego zakazu ludzi, zadnej atmosfery, zadnego forbidden-list). Test na tym samym scenariuszu (000065): 0/9 kalarepa I scena z reka generuje sie poprawnie (wczesniej odmowa). Efekt uboczny: prompty czesciej wspominaja gardenera w tle (oczekiwane, nie problem).

Droga #2 uznana za ZAMKNIETA na dzis w tej formie.

## WIELKA AKTUALIZACJA VPS + MODELI (08.07.2026, poznyy wieczor)

### VPS powiekszony (Hetzner rescale, CPU+RAM only, dysk bez zmian)
- Bylo: CPX32, 4 vCPU, 7.6GB RAM
- Jest: 12 vCPU (AMD EPYC-Genoa), **22GB RAM**, dysk bez zmian (160GB, 111GB wolnego)
- IP bez zmian: 157.90.155.155. Wszystkie uslugi (docker, mcp-fabryka.service, ollama) wystartowaly same po restarcie - restart policy "unless-stopped" + systemctl enabled na wszystkim.
- PO RESCALE: Ollama STRACILA `OLLAMA_HOST=0.0.0.0` z glownego pliku uslugi (reset przy rescale, przyczyna nieznana) - naprawione przez `/etc/systemd/system/ollama.service.d/override.conf`.

### Modele - WIELKA PODMIANA
**DEFAULT_MODEL** (polski tekst): `SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0` -> **`SpeakLeash/bielik-11b-v3.0-instruct:Q6_K`** (8.5GB)
**PROMPT_MODEL** (angielskie prompty obrazow + NAPRAW): `llama3.1:8b` -> **`qwen3:14b`** (8.6GB, ma tryb "thinking" - wolniejszy, ale trzyma sie tematu lepiej niz Llama)

Oba stare modele ZOSTAJA pobrane na dysku jako droga powrotu (nie skasowane).

### Konfiguracja Ollama (`/etc/systemd/system/ollama.service.d/override.conf`)
```
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_MAX_LOADED_MODELS=1    <- SEKWENCYJNIE, nie oba naraz (patrz nizej dlaczego)
OLLAMA_CONTEXT_LENGTH=8192    <- bylo 16384, cofniete
```
**WAZNE odkrycie**: Bielik-11B + Qwen3-14B RAZEM w pamieci = OOM-kill (potwierdzone dmesg, 2x, nawet przy 22GB i kontekscie 8192). Qwen3:14b SAM zajmuje w RAM ~12GB (nie 8.6GB jak plik) - prawdopodobnie efekt trybu "thinking". SUMA obu modeli przekracza budzet. Decyzja: zostac przy SEKWENCYJNYM ladowaniu (jeden model na raz), nie probowac trzymac obu jednoczesnie.

### `_unload_model()` wzmocniony (pipeline.py) + `_unload_text_model()` naprawiony (images/prompts.py)
Dodany bufor bezpieczenstwa: PO potwierdzeniu zniknięcia modelu z `/api/ps`, dodatkowe 10s snu przed pozwoleniem na zaladowanie nastepnego. Powod: nawet z pollingiem, /api/ps czasem raportuje model jako "zniknal" zanim system faktycznie w pelni odzyska pamiec.

**KRYTYCZNY cichy bug znaleziony i naprawiony**: `_unload_text_model()` w images/prompts.py miala ZAHARDKODOWANA STARA nazwe `"SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0"` - po podmianie DEFAULT_MODEL na 11B, ta funkcja w ogole nie zwalniala faktycznie zaladowanego modelu! Naprawione: czyta DEFAULT_MODEL dynamicznie.

**Dodatkowo znalezione i naprawione**: `naprawa.py` i OBIE funkcje w `images/prompts.py` (`generate_image_prompts` i `generate_image_prompts_czysty`) mialy zahardkodowane `"llama3.1:8b"` zamiast uzywac zmiennej `PROMPT_MODEL` - bez tej naprawy Qwen3 nigdy by realnie nie zadzialal w produkcji mimo podmiany zmiennej.

### Kontekst Bielika - twardy limit architektury (NIE do zmiany konfiguracja)
Stary Bielik-4.5B: `llama.context_length: 8192` - twardy sufit modelu, nie RAM-u. Nowy Bielik-11B ma natywnie 32768 (ale globalne OLLAMA_CONTEXT_LENGTH=8192 i tak to ogranicza - decyzja swiadoma, zeby nie ryzykowac OOM).

### System Health w panelu (NOWE)
Endpoint `GET /system-health` (topics.py): czyta /proc/meminfo (RAM), os.getloadavg() (CPU), shutil.disk_usage (dysk). Panel: 3 poziome paski pod statystykami, kolor zielony/zolty(>70%)/czerwony(>90%), odswiezane co 5s.
Przycisk **"Ubij proces (zwolnij pamiec modeli)"** w tej samej karcie - `POST /uwolnij-pamiec`, czyta /api/ps, zwalnia WSZYSTKIE zaladowane modele przez keep_alive=0. Do recznego uzycia gdy pasek RAM pokaze czerwony.

### Test jakosci nowych modeli (Bielik-11B)
Artykul+scenariusz o pomidorach: format poprawny, tresc trafna. JEDNA nowa usterka zaobserwowana: model czasem dokleja dodatkowy fragment ("Puenta...") PO ostatniej scenie, ktory parse_scenes() doklei do LEKTORA ostatniej sceny (sklejone dwa zdania bez naturalnej przerwy). Pojedynczy test, nie wiadomo czy powtarzalne - do obserwacji.

### Sprzatanie (08.07.2026 wieczor)
Usuniete z repo: wszystkie tymczasowe skrypty testowe (test_*.py, faza*.py, wynik_*.txt) ktore przypadkiem trafily do bind-mounta. `data/reels/` dodane do .gitignore (duze pliki multimedialne, dane wynikowe, nie kod).

## POPRAWKI ROLKI 000066 (08.07.2026, pozno w nocy) - POTWIERDZONE PRZEZ TOMASZA
Zastosowane TANIA metoda (patch, nie pelna regeneracja):
1. Obraz 08: aksamitka z poprawnym opisem wizualnym (pomaranczowo-zolte, geste platki, Tagetes) zamiast bialego kwiatka z fioletowymi zylkami (byla niespojnosc UJECIE/LEKTOR z Dyskusji wczesniej tego dnia)
2. Obraz 09: zielona tabliczka "OGRODY ROD" zamiast czerwonej "ROD Wozniki" (redundancja z intro/outro)
3. Napisy: wszystkie 9 scen przez naprawiony transcribe_scene (podstawianie znanego tekstu)

DODATKOWY bug znaleziony i naprawiony przy tej okazji: licznik slow do porownania (transcribe_scene) zle liczyl samodzielne znaki interpunkcyjne (np. "-") jako osobne "slowo" - w mowie nie maja odpowiednika, wiec Whisper nigdy nie da dla nich osobnego tokenu. Naprawione: filtr `any(c.isalnum() for c in w)` przy dzieleniu oczekiwanego tekstu na slowa.

POTWIERDZONE PRZEZ TOMASZA: "Pozytywnie poprawione. Napisy Ok." - wszystkie 3 poprawki dzialaja.

WAZNA LEKCJA (blad Claude'a wczesniej tego dnia): przy prosbie o poprawke 2-3 konkretnych elementow istniejacej rolki, ZAWSZE uzywac tanich metod patchowania (podmiana prompts.txt + generate_image dla pojedynczych obrazow, ponowne wywolanie make_subtitles/render_video/add_background_music) - NIGDY nie odpalac pelnego /generate-reel-async od zera, bo to bezsensownie generuje WSZYSTKIE obrazy na nowo (w tym te ktore juz byly dobre), marnujac koszt fal.ai. Ta zasada byla juz ustalona wczesniej (patrz "Cost-saving rule" na poczatku pliku) ale zostala zignorowana raz w tej sesji - poprawiono przy nastepnej prosbie.

## PUBLIKACJA FB - STAN NA KONIEC DNIA (08.07.2026, noc)
Rolka 000066 gotowa do publikacji (po poprawkach wyzej), opis wygenerowany (2 warianty: szczegolowy + zapowiedz-teaser stylu "kolejne rolki nadchodza").

**Token FB w n8n workflow "Auto Publikacja FB" (credential JqZNdgyrpWXTCyFS) POTWIERDZONY jako wciaz placeholder** - Tomasz potwierdzil "Czeka" (na wklejenie z Node-RED). n8n API nie ujawnia wartosci sekretow, wiec nie da sie tego zweryfikowac zdalnie - trzeba pytac wprost.

Rozwazona i SWIADOMIE ODRZUCONA alternatywa: istnieje inny, dzialajacy token FB do TEJ SAMEJ strony (1174205105781401), uzywany przez system alarmow burzowych (Node-RED, flow "Ogrodnik") na instancji HA Dom - ale ten token nigdy nie byl testowany do wgrywania WIDEO (tylko tekst/alerty), i nie jest podpiety do tej rozmowy/infrastruktury Fabryki. Decyzja: NIE improwizowac nowej sciezki publikacji przez pozyczony token bez testow, szczegolnie na zywej, publicznej stronie bez mozliwosci cofniecia.

**Droga na dzis**: reczne wgranie przez aplikacje Facebook (Tomasz wgrywa final_with_music.mp4 + wkleja opis recznie). Automatyczna publikacja z tego czatu bedzie mozliwa po uzupelnieniu tokenu w n8n.
