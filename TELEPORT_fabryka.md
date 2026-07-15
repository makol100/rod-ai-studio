> ⚡ **SECOND BRAIN (od 14.07.2026):** zanim zaczniesz czytać ten dziennik,
> przeczytaj `wiedza/INDEX.md` i potrzebne destylaty (ARCHITEKTURA / PROCEDURY /
> NAUKI / STYL). Ten plik to DZIENNIK sesji — czytaj tylko ostatnie sekcje
> i zaległości. Trwałe wnioski z każdej sesji lądują w `wiedza/`, nie tutaj.

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
- **"Aktualizuj wszędzie" / "Update wszędzie"** (Tomasz uzywa OBU form — to jedno i to samo haslo) = pelny zapis stanu w TRZECH miejscach jednoczesnie. Domyslny rytual zamkniecia wiekszej zmiany, NIE pomijac zadnego z trzech:
    1. **TELEPORT** — dopisz sesje do TELEPORT_fabryka.md (ten plik) ORAZ do /root/TELEPORT_HA.md jesli zmiana dotyczy HA
    2. **MAPA POLACZEN** — zaktualizuj MAPA_POLACZEN.html (OBIE kopie: /root/ oraz w repo) jesli zmienila sie architektura/polaczenia
    3. **GITHUB** — wypchnij to co w repo (TELEPORT_fabryka.md + MAPA_POLACZEN.html) na makol100/rod-ai-studio; `git add` TYLKO konkretne pliki, NIGDY `docker-compose.yml` (sekrety). TELEPORT_HA.md jest POZA repo, zapisywany lokalnie na VPS.
  (Uwaga do siebie: ten schemat raz sie zgubil — pushowalem kod bez aktualizacji teleportu. Przy KAZDYM "aktualizuj wszedzie" przejsc wszystkie trzy punkty.)
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

---

## SESJA 09.07.2026 (popołudnie-wieczór) — Czysta Droga Bielik, Checkpoint++, FLUX.2, Nano Banana Pro

### CHECKPOINT rozbudowany o kluczowe funkcje
1. **Prompty obrazów widoczne PRZED checkpointem** (nie po) - generowane od razu po scenariuszu, darmowe (lokalny model). Zapisane do `prompts.txt`; przy zatwierdzeniu pipeline SPRAWDZA czy plik juz istnieje i jesli tak, NIE liczy drugi raz. Funkcja: `_przygotuj_prompty_na_checkpoint()` w pipeline.py.
2. **"Zapisz poprawki"** teraz automatycznie przelicza prompty obrazow dla nowego tekstu scenariusza (endpoint `/reel-checkpoint/{id}/zapisz`).
3. **"Pokaż po polsku"** - tlumaczenie CALEGO scenariusza (UJECIE+LEKTOR) na checkpoincie, endpoint `/reel-checkpoint/{id}/tlumacz`, funkcja `przetlumacz_scenariusz_podglad_pl()` w pipeline.py. Bug: przycisk czasem nie wysyla requestu z niewyjasnionej przyczyny (Tomasz obszedl to reczna translacja).
4. **Zdjecia referencyjne per-scena** (Dyskusja - Tomasz chce wplynac na wyglad konkretnej sceny wlasnym zdjeciem): endpoint `POST/DELETE /reel-checkpoint/{id}/referencje/{scena}`, zapisywane do `folder/refs/{scena:02d}_{n}.jpg`. Uzywaja FLUX.1 Kontext [pro] multi (`fal-ai/flux-pro/kontext/multi`, $0.04/obraz) - bierze kilka zdjec + ISTNIEJACY prompt tekstowy (opis sceny ZAWSZE zostaje), generuje NOWA scene inspirowana referencjami. Funkcja `_znajdz_referencje()` w pipeline.py. Wymagalo doinstalowania `python-multipart` (brakujacy pakiet, bez niego caly serwer nie startowal).
5. **Detektor petli powtorzen zlagodzony**: `has_repetition_loop(min_len=15,min_repeats=3)` -> `(min_len=25,min_repeats=4)` - stary lapal falszywe alarmy na naturalnym powtorzeniu krotkich fraz (np. "UJĘCIE: Zbliżenie" w 3 scenach).

### NOWA SCIEZKA: "Czysta Droga Bielik" (`tryb_jezykowy="czysty_bielik"`)
Trzecia sciezka obok PL (baza tematow) i CZYSTA DROGA (Qwen, EN->PL). Bielik robi WSZYSTKO po polsku - artykul, scenariusz (`generate_scenes_czysty`, szablon `PROMPT_TEMPLATE_CZYSTY`), prompty obrazow. ZERO angielskiego, ZERO tlumaczenia (bo nigdy nie przechodzi przez angielski). Idzie przez `_produce_media` (jak zwykla "pl"), nie `_produce_media_en_pl`.

**Krytyczny bug znaleziony i naprawiony (rolka 000081)**: pierwotnie kierowana przez `generate_image_prompts` (zwykla funkcja, SINGLE_SCENE_HEADER ma zaszyta sekcje "kalarepa/koper" dla tematow warzywnych) - model albo ODMAWIAL dla scen niezwiazanych z ogrodem, albo wymyslal warzywa. Naprawione: musi isc przez `generate_image_prompts_czysty` (bez tej sekcji), z `model=DEFAULT_MODEL` (Bielik) i nowym parametrem `jezyk="pl"` (Bielik pisze prompt obrazu PO POLSKU, nie po angielsku jak w oryginalnej wersji dla Qwena - bo FLUX.2 [max] rozumie polski przez Mistral-3, wiec detour przez angielski juz niepotrzebny).

**Nowy szablon**: `SINGLE_SCENE_HEADER_CZYSTY_PL` w images/prompts.py, kopia angielskiej wersji ale po polsku.

**Naprawiona tez naleciałość w SAMEJ angielskiej wersji** (`SINGLE_SCENE_HEADER_CZYSTY`): konczyla sie na sztywno "real Polish allotment garden" - usuniete, teraz neutralne "natural lighting" + jawna instrukcja "nie zakladaj lokalizacji ktorej scena nie opisuje".

**Znacznik trybu na dysku**: `folder/tryb_jezykowy.txt` zapisywany na starcie `generate_reel()` - bo od "czysty_bielik" mamy WIECEJ NIZ DWIE sciezki zapisujace do tego samego `scenes.txt` (zwykla "pl" i "czysty_bielik"), samo istnienie pliku juz nie wystarcza do rozroznienia. Odczytywany w `wznow_po_checkpoincie()` (nadpisuje zgadywany parametr) i w `_odczytaj_tryb_jezykowy()` (topics.py, z fallbackiem na stare zgadywanie dla rolek sprzed tej zmiany).

**Testy jakosci (rolka 000084, prompt o modernizacji rozdzielnicy TN-C->TN-S)**: Bielik dal bardzo dobry artykul+scenariusz+prompty (Tomasz: "Bielik odpierdolil kawal zajebistej roboty"). Model poprawnie zbalansowal sprzeczne instrukcje (np. "unikaj starych zardzewialych" vs "TREŚĆ: przejscie z ukladu TN-C" ktore logicznie wymaga pokazania punktu startowego) - pokazal krotki kontrast tylko w 1 scenie, reszta konsekwentnie nowoczesna.

### Bielik podniesiony na Q8_0
`DEFAULT_MODEL`: `SpeakLeash/bielik-11b-v3.0-instruct:Q6_K` -> **`SpeakLeash/bielik-11b-v3.0-instruct:Q8_0`** (11.87GB, wyzsza precyzja kwantyzacji). Wyraznie wolniejszy (cala Czysta Droga Bielik ~13 min zamiast wczesniejszych ~7 min), ale RAM (22GB, jeden model naraz) spokojnie to udzwiga.

**Sprzatanie modeli Ollama**: usuniete jako martwe (zero realnych wywolan w kodzie): `gemma3:4b`, `llama3.1:8b`, `SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0`, `SpeakLeash/bielik-11b-v3.0-instruct:Q6_K`. Zwolnione ~21GB dysku (57GB->36GB uzyte). Zostaly TYLKO: Bielik-11B-Q8_0 (DEFAULT_MODEL) i qwen3:14b (PROMPT_MODEL).

### KRYTYCZNY bug w audio - `extract_narration()` (audio/generator.py)
Funkcja czytala TYLKO PIERWSZA LINIE bloku LEKTOR. Jesli Bielik napisal LEKTOR jako kilka linii (lista punktowana z myslnikami, numeracja 1./2./3.), wszystko po pierwszej linii bylo CICHO GUBIONE - nigdy nie trafialo do edge-tts. Potwierdzone na rolce 000084: scena z 622 znakami tekstu miala tylko 8s audio (78 znak/s zamiast normalnych ~15-17 znak/s), inna scena z 347 znakami miala tylko 2.6s (134 znak/s - prawie nic nie przeczytane).

Naprawione: zbiera WSZYSTKIE linie nalezace do bloku LEKTOR (konczy na pustej linii albo nowym naglowku SCENA/UJĘCIE/LEKTOR), laczy spacja. Test potwierdzony: po naprawie sceny wroci do normalnego tempa (14-16 znak/s).

**Wniosek dla Tomasza (lekcja na przyszlosc)**: jesli prosisz o poprawki tekstu ze STRUKTURA (myslniki, numeracja), lepiej przepisac na plynne zdania (Tomasz to zrobil recznie dla scen 4/6/7 rolki 000084) - unika i tego bugu (juz naprawionego), i po prostu lepiej sie czyta na glos.

### FLUX.2 - decyzja, potem podwazona, potem ostatecznie ODRZUCONA na rzecz Nano Banana Pro
1. Sprawdzona analiza: FLUX.2 [max] (`fal-ai/flux-2-max`) wybrany mimo zglaszanych przez userow (Hugging Face, community) problemow z anatomia (dlonie/konczyny) - Tomasz swiadomie zaakceptowal ryzyko.
2. **PO TEScie na rolce 000084 (identyczny prompt wygenerowany przez Tomasza recznie w Gemini vs FLUX.2)**: FLUX wygenerowal TYLKO zewnetrzne, puste zdjecie (np. "stare drzwi" zamiast wnetrza skrzynki z bezpiecznikami) - powierzchowna "atrapa" niezwiazana tresciowo z promptem. Gemini/Nano Banana Pro pokazal PRAWDZIWA, szczegolowa tresc (bezpieczniki, przewody, tabliczki). Tomasz: "Flux ze super zajebistym proptem nic nie pomoze... 80% zdjęć do wymiany".
3. **DECYZJA: przelaczenie na Nano Banana Pro** (`fal-ai/nano-banana-pro` na fal.ai, $0.15/obraz vs FLUX.2 $0.07). Sprawdzone przez badania (nie test): negatywne opinie o Nano Banana Pro dotycza SCHEMATOW ELEKTRYCZNYCH (rysunki logiki polaczen) - "produkuje obwody ktore wysadzilyby bezpiecznik" - ale to INNE zadanie niz FOTOREALISTYCZNE ZDJECIA fizycznego sprzetu (to czego potrzebuje Fabryka Rolek). Mocne strony potwierdzone: najlepszy w branzy text rendering, lepsza dokladnosc dłoni/twarzy niz poprzednie modele, wierne trzymanie sie promptu bez niepotrzebnych halucynacji.

**WAZNE ograniczenie odkryte przy okazji**: subskrypcja Gemini Pro (konsumencka, do rozmow) to ZUPELNIE INNA rzecz niz dostep API - nie daje darmowych obrazow przez API.

### Zbudowana integracja Nano Banana Pro (KOD GOTOWY, NIE UZYTY jeszcze produkcyjnie)
- `FAL_MODEL_NANO_BANANA_PRO = "fal-ai/nano-banana-pro"` w image_backend.py
- `generate_image()` ma nowy param `silnik` (nadpisuje domyslna logike referencje/FLUX)
- Argumenty API roznia sie od FLUX: `aspect_ratio="9:16"` (string) zamiast `image_size` (enum)
- **Kluczowy pomysl Tomasza zrealizowany**: `zbuduj_konteksty_gemini()` w images/prompts.py - laczy UJECIE+LEKTOR (oryginalny kontekst sceny) + gotowy prompt fotograficzny Bielika w JEDEN bogaty kontekst wysylany do Nano Banana Pro (bo to pelny model jezykowy z rozumowaniem, nie czysty dyfuzyjny jak FLUX - lepiej rozumie WIECEJ kontekstu, nie tylko oderwany prompt)
- `silnik_obrazow` parametr przeciagniety przez `_produce_media`/`_produce_media_en_pl`/`wznow_po_checkpoincie`
- UI: dropdown na checkpoincie "Silnik obrazów: FLUX.2 [max] (domyslnie) / Nano Banana Pro ($0.15/obraz)"
- Referencje (Kontext FLUX.1) maja PIERWSZENSTWO nad silnik_obrazow jesli sa wgrane dla danej sceny

### ARCHITEKTURA: Muzyka wmiksowana w JEDNYM przebiegu ffmpeg (nie dwoch)
**Problem znaleziony przez Tomasza**: renderowanie tworzylo `final.mp4` (bez muzyki), POTEM osobny przebieg `add_background_music()` tworzyl `final_with_music.mp4` - OBA pliki zostawaly na dysku na zawsze (474MB zbednych duplikatow w sumie na wszystkich rolkach, bo `-c:v copy` = identyczne wideo, final.mp4 nigdy wiecej nie czytany).

**Naprawa (opcja B z dwoch zaproponowanych - Tomasz wybral trudniejsza, "wlasciwa" architektonicznie)**: nowa funkcja `concat_parts_with_music()` w video/renderer.py - sklejanie scen + sidechain ducking muzyki pod lektorem w JEDNYM wywolaniu ffmpeg. `render_video()` przebudowany: zbiera `total_duration` (suma dlugosci wszystkich czesci - intro 2.5s + kazda scena + outro 3.0s) PRZED renderowaniem, zeby przyciac zapetlona muzyke bez potrzeby wczesniejszego pomiaru gotowego pliku. Jesli brak sciezki muzyki w `assets/music/` - fallback na sam "final.mp4" bez muzyki (rzadki przypadek).

`pipeline.py` (`_produce_media`, `_produce_media_en_pl`) i `naprawa.py` zaktualizowane - juz NIE woluja `add_background_music()` osobno, tylko odczytuja `video["music"]` z wyniku `render_video()`.

**Test potwierdzony (darmowy, lokalny ffmpeg na juz istniejacych materialach rolki 000084)**: jeden plik wynikowy `final_with_music.mp4`, 1080x1920, 145s, audio -26.5dB mean/-9.6dB max (poprawne poziomy), muzyka faktycznie wmiksowana.

**Posprzatane rowniez 267.7MB z 15 starych rolek** ktore mialy juz bezpieczny duplikat (final.mp4 usuniety TYLKO tam gdzie final_with_music.mp4 istnial). 52 stare rolki majace WYLACZNIE final.mp4 (bez wersji z muzyka, sprzed tej funkcji) zostawione NIETKNIETE - to ich jedyne prawdziwe wideo.

### WAZNA ZASADA USTALONA DZIS: kontrola kosztow
Tomasz jednoznacznie: **KAZDA decyzja wiazaca sie z realnym kosztem (zatwierdzenie checkpointu, generowanie obrazow fal.ai, cokolwiek platnego) wymaga wyraznego, jednoznacznego polecenia Tomasza** - nigdy nie zgadywac/domyslac sie zgody z niejasnych sformulowan, nawet entuzjastycznie brzmiacych ("Teraz FLUX2" NIE bylo zgoda na zatwierdzenie checkpointu - bylem zbyt pochopny i sam kliknalem, co wywolalo silna reakcje "kto ci pozwolil"). Zapisane jako trwala pamiec (memory_user_edits #17).

### Rolka 000084 - STATUS: TEMAT ZAMKNIETY (09.07.2026 wieczor)
Miala sluzyc jako testowa/robocza dla Czystej Drogi Bielik + naprawy audio + test FLUX.2 vs Nano Banana Pro. Tomasz zamknal temat tej konkretnej rolki (nie bedzie dalej dopracowywana) - wiedza z niej wykorzystana do napraw kodu (extract_narration, prompty Nano Banana, render+muzyka), ale sama rolka NIE jest kandydatem do publikacji w obecnym stanie (obrazy FLUX.2 w duzej czesci odrzucone przez Tomasza).

### OTWARTE / DO ROZWAZENIA na przyszlosc
- Nano Banana Pro - POTWIERDZONE DZIALA W PRODUKCJI (Tomasz uzyl przy zatwierdzeniu rolki 000085 - wszystkie 9/9 obrazow "OK (Nano Banana Pro)" w logu, rolka opublikowana). Sprawa zamknieta.
- Przycisk "Pokaz po polsku" na checkpoincie - czasem nie wysyla requestu, przyczyna nieznana (obejscie: recznie w zewnetrznym tlumaczu). ODLOZONE na pozniej, nie priorytet.

---

## SESJA 10.07.2026 — Poprawki rolki 000085, publikacje, zasięg FB

### Rolka #000085 — wielorundowa korekta (przed publikacją)
Testowa rolka "Czysta Droga Bielik" (rozdzielnica TN-C→TN-S) przeszła przez wiele rund poprawek po checkpoincie i PO zatwierdzeniu (Tomasz ręcznie podmieniał zdjęcia, zgłaszał błędy stopniowo zamiast za jednym razem):

1. **Błąd wymowy "altanka"**: Whisper transkrybował "w Twojej altance" jako "Altans" - ustalone że to prawdopodobnie wada wymowy samego glosu edge-tts (nie halucynacja Whisper), bo tekst zrodlowy byl poprawny. Docelowo zmieniono cala forme "altanka"->"altana" (regex na wszystkie odmiany: altanki->altany, altance->altanie, altanke->altane) w scenes.txt, article.md, subs/*.ass, potem PRZELICZONO CALY LEKTOR OD NOWA (nie tylko napisy) - bo problem siedzial w samym audio, nie tylko w transkrypcji.
2. **Blad semantyczny "nie porazi" -> zle brzmiace w syntezie**: przeformulowano na "ryzyko porazenia pradem jest duzo mniejsze" (rzeczownik zamiast odmienionego czasownika - omija slowo ktore zle sie syntetyzowalo).
3. **KRYTYCZNY bug w kodzie**: `extract_narration()` (audio/generator.py) czytal TYLKO PIERWSZA LINIE bloku LEKTOR - gdy Bielik pisal LEKTOR jako liste punktowana (myslniki, numeracja "1.","2.","3."), wszystko po pierwszej linii bylo CICHO GUBIONE, nigdy nie trafialo do edge-tts. NAPRAWIONE: zbiera teraz WSZYSTKIE linie bloku (konczy na pustej linii albo nowym naglowku SCENA/UJĘCIE/LEKTOR).
4. **Placeholder "(brak tekstu)" byl dosłownie wypowiadany na glos**: gdy Bielik oznaczal pusta scene doslownym tekstem "(brak tekstu)", stary kod to syntetyzowal i transkrybowal. NAPRAWIONE: `extract_narration()` rozpoznaje wzorzec `^\(?\s*brak\s+tekstu\s*\)?\.?$` (regex, case-insensitive) i zwraca pusty string dla tej sceny (zachowujac wyrownanie numeracji), a `generate_audio()` pomija generowanie pliku .wav dla pustych scen (renderer i tak ma fallback 2.5s ciszy dla brakujacego audio).
5. **"Styl artykulowy" w mowionym scenariuszu**: frazy jak "Zdjęcie poniżej: ..." (redundantne, widz i tak WIDZI obraz) i numerowane/wypunktowane listy w LEKTORZE ("1. Szyny miedziane...", "• Bezpieczeństwo: ...") brzmia sztucznie czytane na glos. Przeformulowane na naturalny mowiony styl ("Kolejny element to...", "Po pierwsze/drugie/trzecie..."). Tomasz (elektryk) zlapał tez merytoryczne bledy: RCD opisywany w liczbie mnogiej i zlym kolorze (bialy zamiast pomaranczowy), mieszanie RCD z bezpiecznikami nadpradowymi, i błędna rama bezpieczeństwa "wcisnij przycisk RCD gdy cos nie tak" (przycisk TEST sluzy do okresowego sprawdzania, RCD dziala automatycznie, nie recznie).
6. **Usuwanie calych scen**: Tomasz kazal usunac scene 9 (i wczesniej analogicznie 5) CALKOWICIE z rolki - usuwajac tylko images/NN.jpg (renderer automatycznie pomija scene bez obrazu). Znaleziony i naprawiony bug przy tym: `real_scene_count = len(list(images.glob('*.jpg')))` liczyl PLIKI, nie NAJWYZSZY NUMER - przy usunieciu srodkowej sceny (np. 09), liczba plikow spadala, wiec petla `range(1, upper_bound+1)` nie docierala juz do wyzszych numerow (np. 10) mimo ze istnialy. NAPRAWIONE: liczy teraz najwyzszy numer wsrod plikow (`max(int(p.stem) for p in images.glob('*.jpg') if p.stem.isdigit())`), nie sama ich ilosc.
7. **Wydluzanie sceny przez pad audio**: gdy usunieto scene 5, Tomasz chcial zeby scena 6 "wyswietlala sie dluzej" (zeby dlugosc calosci nie skrocila sie gwaltownie). Zrobione przez `ffmpeg -af apad=pad_dur=Xs` na audio/06.wav (dopisanie ciszy na koncu) - `render_video()` i tak liczy duration z `audio_duration(wav)`, wiec dluzsze audio automatycznie wydluza klatke obrazu.

Wszystkie te poprawki (poza transkrypcja Whisper, na ktora Tomasz dal stala zgode bez pytania - patrz pamiec #18) byly darmowe - edycja tekstu + lokalny edge-tts + lokalny ffmpeg, zero fal.ai.

### Rolka #000085 finalnie OPUBLIKOWANA na Facebooku
Pierwsza w pelni opublikowana rolka z nowego pipeline'u (Czysta Droga Bielik + FLUX.2 [max] + Nano Banana Pro reference). Opis do posta wygenerowany w stylu "Bezpieczeństwo i Infrastruktura | [temat]" z emoji, konkretnymi punktami tresci i pytaniem na koncu zachecajacym do komentarzy.

### Nowa funkcja: oznaczanie rolek jako "opublikowana"
Dodany prosty znacznik plikowy `folder/opublikowano.txt` (data w srodku) + endpointy:
- `POST /reels/{reel_id}/opublikowano` - oznacza
- `DELETE /reels/{reel_id}/opublikowano` - cofa oznaczenie
`_scan_reels_from_disk()` (topics.py) zwraca teraz pole `opublikowana: bool`. W panelu przy kazdej gotowej rolce jest przycisk 📤 (nieoznaczona) / ✅ (oznaczona), klikniecie przelacza stan (`data-action="toggle-published"`).

**Trzy rolki potwierdzone jako faktycznie opublikowane na FB** (ustalone przez rozmowe + sprawdzanie folderow na dysku pod katem obecnosci wideo): **#000050** (pierwsza zapowiedz serii), **#000066** (angielski szkic "Exciting News! ROD Wozniki video series..." o iglakach/grzybach - poprawna tresc bez halucynowanej nazwy hosta), **#000085** (dzisiejsza, rozdzielnica). WAZNE odkrycie przy tej okazji: proby #000061/#000062/#000064/#000071 (rozne wersje "zapowiedzi drugiego odcinka") WSZYSTKIE mialy halucynowana, blednas nazwe hosta/serii ("Roza Wozniak", "Rod Wojniki") - zadna nie nadawala sie do publikacji bez recznej edycji, i dwie z nich (#000064, #000071) nie mialy nawet dokonczonego wideo.

### Duze sprzatanie dysku (na wyrazne polecenie Tomasza)
Usuniete BEZPOWROTNIE wszystkie foldery rolek OPROCZ trzech opublikowanych (#000050, #000066, #000085) - 82 foldery, 1,1GB zwolnione. Potwierdzone: serwer nie ma zadnego mechanizmu "kosza" (zwykly Linux bez GUI, `shutil.rmtree()` kasuje natychmiast i bezpowrotnie).

### Strategia zasiegu na Facebooku (Dyskusja z Tomaszem, research)
Sprawdzone aktualne (2026) zasady algorytmu FB: czas oglądania do konca > wszystko inne, pierwsze 3 sekundy decyduja, zapisy/udostepnienia wazniejsze niz lajki, odpowiadanie na komentarze w pierwszych 6h podbija zasieg, 2-4 trafne hashtagi (nie wiecej). **KLUCZOWE ograniczenie techniczne**: Meta calkowicie wylaczyla Graph API dla Grup w kwietniu 2024 (ochrona przed spamem) - **zaden kod/automatyzacja nie moze postowac do Grup FB**, to musi zostac krok reczny Tomasza (Udostepnij → Udostepnij w grupie). Nie ma tez zadnego dostepnego MCP connectora do przegladania/postowania na Facebooku (sprawdzone przez search_mcp_registry - sa tylko narzedzia do analityki Meta Ads, nie do zwyklego Facebooka).

**Ustalone docelowe grupy do reczneho udostepniania kazdej rolki** (po researchu + dyskusji, kilka rund zmian decyzji Tomasza): **"Rodzinne Ogrody Działkowe"** (20 tys. czlonkow) i **"Rodzinne Ogródki Działkowe - Cała Polska"** (4,8 tys. czlonkow). Odrzucone (swiadomie): grupy scisle slaskie/lokalne (Dzialki ROD Slask, Gmina WOZNIKI) i najwieksza ogolna (Fajny Ogrod 851 tys.).

**NOWA STALA ZASADA (zapisana w pamieci #21)**: przy KAZDYM generowaniu opisu/tekstu posta do rolki, Claude ma przypominac Tomaszowi o reczne udostepnienie w tych dwoch grupach.

### Otwarte/niedokonczone z tej sesji
- Strona "ROD im. Józefa Lompy Woźniki." (typ Spolecznosc, 15 obserwujacych) - POTWIERDZONE przez Tomasza, to JEGO oficjalna grupa, nie martwy duplikat. Sprawa zamknieta.

## SESJA 10.07.2026 (popoludnie) — STOP/Pauza, wskrzeszenie #000088, odzysk kontekstu przez teleport

### Incydent: padniety widget w czacie
Czat z 16:04 wywalil sie na widgecie "Asking User Input" (czerwony trojkat) - to blad renderowania WIDGETU, nie smierc czatu. Kontynuacja w nowym oknie przez odczyt tego teleportu. Wniosek: teleport zadzialal dokladnie tak jak mial.

### AKTUALIZACJA NARZEDZI CONNECTORA (wazne - sekcja ostrzezen na gorze pliku czesciowo nieaktualna)
Connector `fabryka` ma teraz PIEC narzedzi: execute_command, write_file, **read_file, append_file, list_dir**. Zasada "write_file NADPISUJE caly plik" wciaz obowiazuje - do dopisywania do TEGO pliku uzywac append_file albo bash cat >>.

### Mechanizm Totalny STOP - fakty z kodu (nie z pamieci)
POST /reel-stop/{id} (topics.py ~442): zapisuje STOP.flag + status.json etap="przerwano". **Folder NIE jest kasowany** - artykul, scenariusz, prompty zostaja na dysku. "Nieodwracalne" znaczy tylko: watek pipeline'u zakonczony, panel pokazuje "przerwana". Rolka zatrzymana NA CHECKPOINCIE = zero poniesionego kosztu fal.ai, cala darmowa robota Bielika ocalona.

### Wskrzeszenie #000088 ("Kawa i fusy w ogrodzie", czysty_bielik) - WYKONANE
Recepta (uzyta i zweryfikowana):
1. rm STOP.flag
2. status.json -> {"etap":"checkpoint","extra":{"warning":false},"ts":...,"kolejnosc":"pl"}
   (kolejnosc dla czysty_bielik i zwyklej "pl" = "pl"; dla en_pl/czystej-Qwen = "en"; odczytac tryb z tryb_jezykowy.txt)
3. Weryfikacja: /reel-status/{id} pokazuje checkpoint, /reels pokazuje status "w trakcie" (= klikalna w panelu, otwiera checkpoint z poprawkami z scenes.txt)
UWAGA dla #000088: prompts.txt (13:24) STARSZY niz scenes.txt (13:27) - po otwarciu checkpointu kliknac "Zapisz poprawki" zeby przeliczyc prompty pod ostatnie poprawki (darmowe, lokalny Bielik).
#000087 = ukonczona rolka (Kompostownik i gnojowki), status gotowa, NIEopublikowana.

### Zaproponowane ulepszenia mechanizmu (czekaja na decyzje Tomasza)
A) Przycisk "Przywroc na checkpoint" przy rolkach "przerwana" - endpoint robiacy dokladnie recepte wyzej (STOP przestaje byc pulapka)
B) Osobny status "czeka na checkpoint" w liscie rolek - dzis etap=checkpoint wyswietla sie jako "w trakcie", nieodroznialne od realnie mielacej rolki (_scan_reels_from_disk, topics.py ~137)
C) Poprawka tekstu confirma przed STOP (panel.html ~1825) - obecny tekst "Nie da sie jej juz wznowic" jest nieprawdziwy

### BEZPIECZENSTWO - do zrobienia
docker-compose.yml zawiera FAL_KEY i ANTHROPIC_API_KEY plaintext; plik zostal wyswietlony w czacie 10.07 przy diagnostyce. Zalecana rotacja obu kluczy przy okazji. NIE catowac docker-compose.yml w czacie - uzywac grep pod konkretny klucz konfiguracyjny.

### UZUPELNIENIE (10.07 ~16:30): rekonstrukcja popoludnia z git diff + porzadki w gicie
ODKRYCIE: zaden kod nie byl commitowany od 08.07 23:03 - cale sesje 09.07 i 10.07 (12 plikow, ~2268 linii) wisialy niezapisane w working tree. Teraz zacommitowane i wypchniete. data/reels wyjete z indeksu gita (git rm -r --cached - dopelnienie decyzji .gitignore z 08.07; pliki na dysku nietkniete).

Zmiany z popoludniowej sesji (ta z padlym czatem), odtworzone z git diff - NIE bylo ich wczesniej w teleporcie:
1. **System grup FB per rolka**: grupy_fb.json w folderze rolki; GRUPY_FB = {rod: Rodzinne Ogrody Dzialkowe, rodcp: ...Cala Polska, dio: Dzialkowicze i Ogrodnicy}; endpointy POST/DELETE /reels/{id}/grupa/{grupa_id}; pole grupy_fb w /reels; checkboxy w panelu przy kazdej gotowej rolce. Wylacznie RECZNE odhaczanie przez Tomasza (Meta nie ma API do grup).
2. **Funkcja "referencje" (FLUX.1 Kontext, zdjecia referencyjne per-scena) USUNIETA z kodu na wyrazne polecenie Tomasza** - sekcja z 09.07 wyzej opisuje ja jako istniejaca: JUZ NIEAKTUALNA.
3. **prompt_oryginalny.txt** - surowy prompt Tomasza zapisywany do folderu rolki (naprawa: /reels pokazywalo poczatek artykulu Bielika zamiast tego, co user faktycznie wpisal).
4. Fix statusow w liscie rolek: przerwana / blad / zatrzymana (walidacja) zamiast wiecznego "w trakcie" (komentarz "NAPRAWIONE 10.07.2026" w topics.py).
5. Przebieg #000088: wygenerowana 12:09 (kawa i fusy, czysty_bielik) -> checkpoint -> poprawki Tomasza do 13:27 -> Totalny STOP 13:30 (nieporozumienie co do znaczenia przycisku) -> wskrzeszona 14:14 (recepta wyzej).

Czego NIE da sie odtworzyc: samej tresci rozmowy z padlego czatu (uzasadnienia/decyzje poza sladami w kodzie i komentarzach).

### docker-compose.yml - PULAPKA, NIE COMMITOWAC
Popoludniowa sesja dodala tez ANTHROPIC_API_KEY do environment kontenera (compose zmodyfikowany 12:13, cel nieznany - pewnie planowana funkcja z API Claude). Plik celowo zostawiony NIEZACOMMITOWANY, bo zawiera sekrety plaintext (FAL_KEY + ANTHROPIC_API_KEY). UWAGA: stara wersja z FAL_KEY JUZ SIEDZI w historii GitHuba. Docelowo: przeniesc sekrety do .env (gitignore) + env_file w compose, zrotowac oba klucze. Do tego czasu: NIGDY git add docker-compose.yml.

### PO CO ANTHROPIC_API_KEY W KONTENERZE (potwierdzone Tomasz + kod) — Claude API w panelu
Dwie funkcje w panelu wołaja api.anthropic.com BEZPOSREDNIO (model `claude-sonnet-4-6`, biblioteka `requests`, x-api-key z env). To OSOBNY, PLATNY dostep API - nie ma nic wspolnego z subskrypcja Claude.ai (osobne rozliczenie, kazde wywolanie kosztuje). Klucz jest w docker-compose environment (dlatego compose zyskal ANTHROPIC_API_KEY o 12:13). Dwa endpointy (topics.py):
1. **POST /asystent-promptu** (~856) — sekcja "00 Asystent promptu" w panelu. Bierze slaby/ogolnikowy temat + instrukcje Tomasza, rozbudowuje na gotowy precyzyjny prompt do wklejenia w "Temat rolki". (To ta funkcja co Tomasz nazwal "okno chata w app".)
2. **POST /reel-checkpoint/{id}/popraw-przez-claude** (~627) — pole "🤖 Popraw przez Claude" NA CHECKPOINCIE. Bierze artykul (kontekst) + obecny scenariusz + instrukcje ("usun wymyslony fakt w scenie 3", "scena 5 zbyt fachowa"), zwraca poprawiony scenariusz w tym samym formacie SCENA/UJECIE/LEKTOR. System prompt kaze zmieniac TYLKO to o co proszono, zachowac format i liczbe scen.
Uwaga: to jedyne miejsca w Fabryce uzywajace Claude API. Reszta pipeline'u (artykul, scenariusz, prompty obrazow, NAPRAW) chodzi na LOKALNYCH modelach Ollama (Bielik-11B, Qwen3-14B) - darmowych. Claude API to swiadomy wyjatek: platny model wyzszej klasy do zadan gdzie lokalne modele nie wystarczaja (rozbudowa slabego promptu, celna redakcja scenariusza).

### NAPRAWIONY MECHANIZM PAUZA/STOP (10.07.2026, ~15:20) - PRZYCZYNA + FIX + ZWERYFIKOWANE
Prawdziwa przyczyna auto-otwierania okna checkpointu po Pauzie (znaleziona w kodzie, nie zgadywana):
`$('#cpPause')` byl CZYSTO frontendowy (tylko closeCheckpoint()+toast) - NIGDY nie mowil backendowi ze user pauzuje. status.json zostawal "checkpoint" na zawsze. `/aktywne-generowanie` (heartbeat co 15s, `checkAktywneGenerowanie()`) nie ma limitu wieku dla etap=="checkpoint" - wiec co 15s ZNOWU zglaszal ta rolke jako "aktywna", co wywolywalo `startStatusPolling()` -> `openCheckpoint()` od nowa. Stad wrazenie "zamykam X, samo sie otwiera".

FIX (zaimplementowany, wdrozony, zweryfikowany 8-krokowym testem end-to-end):
- Nowy plik-znacznik `PAUZA.flag` (analogiczny do STOP.flag) - zapisywany przez nowy endpoint `POST /reel-checkpoint/{id}/pauza`
- `/aktywne-generowanie` wyklucza checkpointy z PAUZA.flag (dokladnie jak juz wykluczal STOP.flag)
- Nowy endpoint `POST /reel-checkpoint/{id}/wznow` - usuwa STOP.flag I PAUZA.flag, przywraca status.json na checkpoint z poprawna kolejnoscia (pl/en, czytane z tryb_jezykowy.txt). Dziala dla OBU przypadkow (Pauza i Totalny STOP) - realizuje wprost prosbe Tomasza "Stop to Stop ale odwracalne po przycisnieciu edytuj".
- `_scan_reels_from_disk`: nowe statusy w liscie "checkpoint" i "pauza" (zamiast mylacego "w trakcie" ktore bylo nieodrozniane od realnie mielacej rolki - stary, znany bug tez przy okazji naprawiony)
- Panel: nowy przycisk ✏️ (`data-action="wznow-checkpoint"`) w karcie rolki na liscie Ostatnie Rolki, widoczny dla status pauza/checkpoint/przerwana. To JEDYNY sposob ponownego otwarcia checkpointu - zero automatyki (zgodnie z wyrazna prosba: "Aktywowac tylko przyciskiem kolo ostatnie rolki")
- Poprawiony nieprawdziwy tekst confirm() przy Totalny STOP (mowil "nie da sie wznowic" - teraz zgodny z prawda)

Test end-to-end na #000088 (8 krokow, wszystkie potwierdzone): pauza -> PAUZA.flag na dysku -> /aktywne-generowanie poprawnie zwraca null -> lista pokazuje status "pauza" -> wznow -> PAUZA.flag skasowany -> lista wraca do "checkpoint" -> status.json poprawny.

Metoda edycji: recznie napisany python (count-i-replace, analogiczne do str_replace) przez fabryka:execute_command, bo VPS-owy connector nie ma str_replace. Restart TYLKO kontenera fabryka-api (nie Ollama, nie VPS) - 4s do gory.

---

## SESJA 10.07.2026 (wieczór) — APKA ANDROID + HTTPS PANELU + BUILD GITHUB ACTIONS

Tego NIE bylo w teleporcie (robota po ostatnim zapisie ~16:30). Wczesniejszy czat zaczal temat apki, ale padl na widgecie "Asking User Input" zanim cokolwiek powstalo — kontynuacja w nowym oknie, odzysk przez teleport, potwierdzone ze na VPS nie bylo jeszcze zadnych plikow apki (samo planowanie).

### DECYZJA: panel po HTTPS (opcja A, nie cleartext)
Panel siedzi na czystym http://157.90.155.155:8000; Android domyslnie blokuje cleartext. Wybor Tomasza: **A — HTTPS przez sslip.io** (odrzucone B — cleartext exception). Uzasadnienie: HTTPS dla MCP juz stal, wiec panel = jedna dodatkowa trasa w Caddy; a panel steruje platnymi operacjami (fal.ai) i publikacja na publicznej stronie ROD, wiec hasla/dane nie moga leciec otwartym tekstem.

### HTTPS PANELU — ZROBIONE I ZWERYFIKOWANE
Caddy (`caddy-mcp`, obraz caddy:2) jedzie na **sieci host** — siega uslug przez localhost, nie przez siec docker. Aktywny Caddyfile: `/root/claude-vps-mcp/Caddyfile` (montowany read-only do /etc/caddy/Caddyfile). Mial jeden blok MCP: `157-90-155-155.sslip.io { reverse_proxy localhost:8765 }` — ZADNEGO sekretu w Caddyfile (token waliduje serwer MCP).
Dodany DRUGI blok (backup Caddyfile.bak-20260710-1800 zrobiony najpierw):
```
panel.157-90-155-155.sslip.io {
	reverse_proxy localhost:8000
}
```
Reload: `docker exec caddy-mcp caddy reload --config /etc/caddy/Caddyfile` (plynny, MCP nietkniety — komendy tego czatu leca przez MCP = zywy dowod). Cert Let's Encrypt wystawil sie sam. Zweryfikowane: `https://panel.157-90-155-155.sslip.io/panel` → 200, `/system-health` → 200 JSON. **Panel wola API jako same-origin** (`API_BASE=''` w panel.html, wszystkie fetch wzgledne), wiec jeden host HTTPS obsluguje /panel I wszystkie endpointy naraz. NOWY adres panelu: **https://panel.157-90-155-155.sslip.io/panel**.
UWAGA: `caddy fmt --overwrite` NIE dziala w kontenerze (config read-only) — ostrzezenie o formatowaniu przy reloadzie jest kosmetyczne.

### APKA ANDROID — ZBUDOWANA (repo, katalog android/)
Swiadomie minimalna dla pewnosci buildu: **Java, ZERO AndroidX** (framework: android.app.Activity + android.webkit.WebView), minSdk 26 (ikona adaptacyjna w samym XML, zadnych binarnych PNG), compile/target 34, AGP 8.5.2, Gradle 8.7, JDK 17. applicationId `pl.rod.fabryka`.
- **MainActivity = natywny dashboard z kartami** (budowany programowo): zielony naglowek z gradientem + 6 kart (Nowa rolka→01, Ostatnie rolki→02, Tematy→03, Asystent→00, Diagnostyka→04, Caly panel→gora), kazda: kolorowy kafelek emoji + tytul + podtytul + strzalka, zaokraglenie + cien + ripple.
- **WebActivity = WebView** ladujacy panel po HTTPS. Karty deep-linkuja: intent extra "section" → po onPageFinished JS skroluje do `.sec-head` ktorej `.idx`==numer (panel ma sekcje `.sec-head > .idx` 00–04). Back (webview history), file chooser (WebChromeClient), zapamietywanie stanu przy obrocie.
- Manifest: MainActivity=LAUNCHER, WebActivity=child, `usesCleartextTraffic="false"` (bo HTTPS). KLUCZOWE: `compileOptions.encoding "UTF-8"` w app/build.gradle — konieczne przez emoji/polskie znaki w literalach String.

### BUILD: GITHUB ACTIONS → APK JAKO RELEASE
`.github/workflows/build-apk.yml` (repo nie mialo wczesniej workflow): trigger push do `android/**` + workflow_dispatch. checkout → JDK17 (temurin) → android-actions/setup-android@v3 → gradle/actions/setup-gradle@v4 (gradle-version 8.7; NIE ma commitowanego wrapper-jara, gradle instaluje akcja) → `gradle assembleDebug` → upload artefaktu → **Release** (softprops/action-gh-release@v2, tag ruchomy `apk-latest`, `continue-on-error:true`, `permissions: contents:write`).
**Bezposredni link do APK** (jeden tap, bez zipa): https://github.com/makol100/rod-ai-studio/releases/download/apk-latest/app-debug.apk

### APK ZWERYFIKOWANY (verify not hallucinate)
Build zielony. APK pobrany na VPS: kompletny (AndroidManifest + classes.dex + classes2.dex + resources.arsc + zasoby), **podpisany v2** (blok "APK Sig Block 42" obecny; minSdk 26 → v2 wystarcza, instalowalny). Rozmiar ~17 KB = NORMALNE przy zerowych zaleznosciach (framework w telefonie, nie w APK). versionCode 2 / versionName 1.1.

### MAPA POLACZEN zaktualizowana
Dodane: blok "Apka Android", Caddy jako reverse proxy z 2 hostami HTTPS, panel po HTTPS, git→Actions→APK, oraz brakujace fal.ai i Claude API. Bielik Q6_K→Q8_0. Obie kopie zsynchronizowane, wypchniete.

### PLIKI APKI (repo)
android/{settings.gradle, build.gradle, gradle.properties, .gitignore}, android/app/build.gradle, android/app/src/main/AndroidManifest.xml, android/app/src/main/java/pl/rod/fabryka/{MainActivity,WebActivity}.java, android/app/src/main/res/{values/{strings,colors,themes}.xml, drawable/{card_bg,card_ripple,header_bg,ic_launcher_foreground}.xml, mipmap-anydpi-v26/{ic_launcher,ic_launcher_round}.xml}, .github/workflows/build-apk.yml

### OTWARTE
- Apka: po odpaleniu na telefonie ew. poprawki wygladu (kolory/kolejnosc kart/tresc) → push → Release sam sie aktualizuje pod tym samym linkiem apk-latest.
- Nierobione ulepszenia apki: pull-to-refresh, zapamietywanie ostatniej sekcji, natywny wskaznik "serwer online".
- Jesli krok Release kiedys da 403: Settings→Actions→Workflow permissions → Read and write (na razie Release sie utworzyl = uprawnienia OK).

### Mapa przebudowana na GALAKTYKE (10.07.2026 pozno)
MAPA_POLACZEN.html przeprojektowana z pionowej listy ("jedno pod drugim", odrzucone przez Tomasza wraz z siatka blueprintu) na **diagram-galaktyke**: Claude jako swiecace zlote JADRO w centrum, VPS/Dom/Dzialka jako systemy na orbitach trzymane zlotymi wiazkami MCP, uslugi (GitHub/fal.ai/Claude API/apka) jako ksiezyce, Facebook/Telegram jako ksiezyce Domu, Tailscale jako przerywany luk Dom<->Dzialka. Tlo kosmiczne: gradient przestrzeni, mgławice (fiolet/turkus/magenta), obracajace sie pierscienie orbit + zarys ramion spiralnych, pole gwiazd (gestsze w centrum = zgrubienie galaktyki). Inline SVG + JS starfield (center-weighted) + animacje (CSS twinkle/pulse, SMIL rotacja pierscieni). POLACZENIA identyczne jak wczesniej - zmiana czysto wizualna. Obie kopie (/root/ i repo) zsynchronizowane, wypchniete. Zatwierdzone przez Tomasza ("To jest to").

### Edytor rolki (checkpoint) = PELNA STRONA zamiast modala (10.07.2026)
Tomasz: przycisk edycji rolki (✏️ na liscie / checkpoint) otwieral bottom-sheet modal - niewygodny na telefonie. Zamienione na PELNA STRONE: #cpOverlay full-screen opaque (var(--bg), flex-direction:column), #cpSheet 100% wys/szer bez zaokraglen/cienia, #cpBody = obszar przewijania (flex:1 1 auto; min-height:0), naglowek przebudowany: strzalka "<-" (Wroc) po lewej + tytul "Edycja rolki". Dodana obsluga FIZYCZNEGO przycisku Wstecz: openCheckpoint robi history.pushState (flaga cpBackActive), listener popstate zamyka edytor, przycisk "<-" idzie przez history.back - w apce back telefonu zamyka edytor jak strone. Zmiana czysto w panel.html (CSS + JS, 8 chirurgicznych podmian), zero backendu. Panel czytany przy KAZDYM zadaniu (@app.get("/panel") w main.py, bind-mount apps/api->/app) => zmiana NA ZYWO bez restartu kontenera. Backup: apps/api/src/panel.html.bak-20260710-edycja. Zweryfikowane: HTTP 200, klamry/nawiasy zbilansowane.

### NOWA STALA ZASADA: sprawdzaj VPS przed wdrozeniem (10.07.2026, pamiec #22)
Przed KAZDYM wdrozeniem/restartem sprawdzic czy VPS nie jest zajety: /aktywne-generowanie == {"aktywna":null}, brak procesow ffmpeg/whisper/pipeline, load spokojny, Ollama bez modelu - zeby nie ubic trwajacego generowania ani nie zawiesic serwera. Dopiero po potwierdzeniu wolnego wdrazac. Fakt pomocny: panel.html idzie na zywo bez restartu (odczyt z dysku per request), wiec jego edycja = zero ryzyka przerwania.

### TRIK: naprawa zlej wymowy edge-tts (potwierdzony 10.07 - "fusy" czytane jako "Fjusy", rolka 000088)
Problem: edge-tts (pl-PL-MarekNeural) czasem czyta POPRAWNIE zapisane polskie slowo zle - "fusy" -> "Fjusy" (wstawka [j], jakby po angielsku). To wada glosu, nie danych; tekst zrodlowy poprawny.
Naprawa (ZERO kosztu - tylko edge-tts + ffmpeg lokalnie; obrazy i napisy NIETKNIETE):
1. Znalezc ktore SCENY maja slowo w LEKTORZE (nie w UJECIU - UJECIE nie jest czytane). Tu: sceny 1,7,8 (grep "fus" scenes.txt, patrzec tylko na linie LEKTOR:).
2. Regenerowac audio TYLKO tych scen z FONETYCZNA respisownia slowa w tekscie podawanym do edge-tts: "fusy" -> "fósy". Polskie "ó" = ta sama gloska [u], wiec czyta "fusy" bez [j]. KLUCZOWE: NIE zmieniac scenes.txt ani napisow na dysku - tylko tekst podany do edge-tts. Dzieki temu na EKRANIE zostaje poprawne "fusy", zmienia sie tylko glos.
   Metoda: python w kontenerze -> import audio.generator (EDGE_TTS_BIN, EDGE_TTS_VOICE, _TTS_ENV=locale C.UTF-8); dla wybranych scen edge-tts --write-media NN.mp3 potem ffmpeg -i NN.mp3 NN.wav (dokladnie jak generate_audio robi). Nadpisuje audio/NN.wav.
3. render_video(folder) - renderuje z ISTNIEJACYCH obrazow + audio + napisow (subs/*.ass burnowane as-is, ZERO transkrypcji = zero fal.ai). Dlugosc sceny liczona z audio_duration(wav), wiec drobna zmiana dlugosci audio (tu -24..48ms bo "fósy" krotsze od "fjusy") uwzglednia sie sama; napisy zostaja w sync.
Ogolna zasada: przy zlej wymowie edge-tts probowac fonetycznej respisowni SAMEGO tekstu-do-lektora (ó zamiast u itp.), trzymajac scenes.txt i napisy poprawne - zamiast SSML (edge-tts nie wspiera pewnie <phoneme>) czy zmiany calego slowa/formy (jak przy "altanka"->"altana" na 000085, gdzie akurat forma tez byla ok w napisach). Weryfikacja zawsze uchem u Tomasza. Backup audio (.bak) usuwac po potwierdzeniu.

### PUBLIKACJA NA FB Z PANELU — ZBUDOWANA (10.07.2026), NIETESTOWANA END-TO-END
Zrobione BEZPOSREDNIO w backendzie (nie przez n8n - to byla droga dla auto-crona), publikacja per rolka na zadanie.
- **Token**: dziala, w `/root/rod-ai-studio/data/.secrets/fb_page_token` (chmod 600, `.gitignore data/.secrets/`, kontener czyta bo `data` bind-mount). To TEN SAM token co alarmy burzowe (Node-RED flow Ogrodnik, app "Ogrodnik ROD" app_id 2107627323468141). ZWERYFIKOWANY z serwera: type=PAGE, strona 1174205105781401 (ROD Wozniki), **expires_at=0 (WIECZNY)**, scopes maja `pages_manage_posts`, test `video_reels upload_phase=start` = SUKCES. NIE trzeba bylo robic nowego tokenu. Token czytany TYLKO z pliku, nigdy nie logowany/wyswietlany.
- **Endpoint**: `POST /reels/{id}/publikuj-fb` (topics.py, na koncu pliku) - 3-fazowy `video_reels`: start -> upload przez naglowek `file_url` (FB sciaga publiczny mp4 z `https://panel.157-90-155-155.sslip.io/reels/{id}/video`) -> finish `video_state=PUBLISHED` + `description`. Body `{opis}`. Oznacza `opublikowano.txt`. Graph API v21.0. WYMAGA RESTARTU kontenera przy zmianie (uvicorn bez --reload).
- **Panel**: przycisk "📘 Publikuj na strone FB" w rozwinietej karcie gotowej rolki (po sekcji grup FB), okienko `#fbPubOverlay` z edytowalnym opisem (prefill: r.text+r.hashtagi przez base64 data-opis) + ostrzezenie + PODWOJNE potwierdzenie (dialog + confirm). Przycisk to zwykly fetch POST -> **DZIALA W OBECNEJ APCE bez nowego APK** (inaczej niz pobieranie, ktore wymagalo DownloadListener). Zmiana panelu na zywo, bez restartu.
- **WAZNE**: publikuje TYLKO na STRONE (Meta ubila API grup 04.2024). Grupy (20k/4.8k/142k) dalej RECZNIE - okienko przypomina.
- **NIETESTOWANE na zywej publikacji**: 000087 i 000088 Tomasz wrzucil recznie ZANIM zdazylismy testnac (kazdy test bylby duplikatem). Pierwsza prawdziwa proba = NASTEPNA NOWA rolka (klik przycisku = test end-to-end). Jesli upload/finish sie wywali, poprawic mechanizm file_url/finish.
- Higiena: fragment tokenu mignal na screenie od Tomasza (prefix EAAd84D..., bezuzyteczny kawalek) - token dziala, ale kiedys warto zrotowac.

### POBIERANIE ROLKI + EDYTOR JAKO STRONA (10.07.2026) - w skrocie
Przycisk ⬇️ pobierz w panelu + WebView DownloadListener (menedzer pobieran Androida, zapis do Downloads) - WYMAGA APK v1.2 (rebuild na GitHub). Endpoint /reels/{id}/video ma juz Content-Disposition attachment. Edytor rolki (checkpoint) zamieniony z modala na pelna strone + fizyczny Wstecz zamyka. Szczegoly w commitach.

### AUTO-OPIS FB + POPRAW PRZEZ CLAUDE (10.07.2026) — ZBUDOWANE, przetestowany Bielik
- `POST /reels/{id}/generuj-opis-fb` (topics.py) — Bielik (generate(), DARMOWY) pisze gotowy opis FB (hook+emoji, 3-5 korzysci, pytanie, 3-4 hashtagi) z article.md. CACHE: zapisuje opis_fb.txt; kolejne wolania zwracaja cache (chyba ze ?force=true). Zweryfikowany na 000088 = dobry opis (fusy).
- `POST /reels/{id}/opis-przez-claude` (topics.py) — Claude API (claude-sonnet-4-6, PLATNE, ANTHROPIC_API_KEY z env, wzor jak asystent-promptu). Bierze {opis}+article.md, dopracowuje, zapisuje opis_fb.txt. Import Bielika: `from src.ai.ollama import generate` (fallback ai.ollama).
- Panel: okienko Publikuj przy OTWARCIU auto-generuje opis Bielikiem (1. raz ~30s bo laduje model, potem cache natychmiast) -> textarea. Przycisk "✨ Popraw opis przez Claude (platne)" z confirm (klik=zgoda na koszt) -> podmienia opis. Panel na zywo; endpointy wymagaly restartu.

### UPDATE WSZEDZIE 10.07.2026 (koniec sesji FB)
Mapa zaktualizowana: VPS → Facebook JUZ DZIALA (nie "planowane") - publikacja Reels z panelu + auto-opis. Droga PRZEZ BACKEND (endpoint /reels/{id}/publikuj-fb) - SUPERSEDES starsza droge przez n8n workflow "Auto Publikacja FB" (ta zostaje jako opcja crona, ale nieuzywana; token juz nie jest placeholderem - siedzi w data/.secrets/fb_page_token). Wszystkie 3 miejsca (teleport + mapa + GitHub) zsynchronizowane.

### 🔴 WYCIEK KLUCZA FAL + ROTACJA (11.07.2026) — ZAMKNIETE
CO SIE STALO: `docker-compose.yml` byl SLEDZONY PRZEZ GIT od pierwszego commita (de3af46 "ETAP 1", repo utworzone 29.06) i zawieral PRAWDZIWY FAL_KEY plaintext. Repo `makol100/rod-ai-studio` jest **PUBLICZNE** -> klucz byl do pobrania z raw.githubusercontent.com bez logowania przez ~2 tygodnie. Zasada "nigdy git add docker-compose.yml" chronila tylko przed NOWYMI zmianami - plik juz byl w indeksie, wiec to nie wystarczalo.
WYKRYTE: audytem kodu (`git ls-files --error-unmatch docker-compose.yml` = sledzony; GitHub API `private: False`; raw fetch potwierdzil publiczna dostepnosc).
SKALA: fal.ai dashboard pokazal zuzycie zgodne z wlasnym (310 req/7dni, modele whisper/nano-banana-pro/flux-2-max, $9.98/7dni, 0 bledow) - brak sladow obcego uzycia. Forkow 0.
NAPRAWIONE: (1) Tomasz utworzyl NOWY klucz fal (Scope: **API** - wezsze, bez dostepu do billingu/kluczy) i SKASOWAL stary. (2) Nowy klucz w `data/.secrets/fal_key` (chmod 600) + wstawiony do lokalnego docker-compose.yml. (3) `git rm --cached docker-compose.yml` + wpis w `.gitignore` (+ `*.bak*`). (4) Dodany `docker-compose.yml.example` z placeholderami (repo dalej odtwarzalne). (5) Kontener ODTWORZONY (`docker compose up -d --force-recreate api`) - UWAGA: zwykly `docker restart` NIE przeladowuje env z compose, trzeba recreate. Zweryfikowano, ze kontener ma nowy klucz.
CZYSTE: ANTHROPIC_API_KEY nigdy nie byl w gicie (sprawdzone `git log --all -S`). Token FB czysty (w repo tylko 7-znakowy prefiks z mojej notatki). Stary klucz zostaje w HISTORII gita na zawsze, ale po revoke jest martwy = nieszkodliwy (nie trzeba filter-repo).
LEKCJA NA PRZYSZLOSC: sekrety NIGDY w plikach sledzonych przez git. Przed kazdym `git add` sprawdzac `git ls-files` czy plik z sekretami nie jest juz w indeksie. Nazwa uslugi w compose to `api` (nie `fabryka-api` - to container_name).

---

## 🗺️ MAPA FUNDAMENTALNA ROD WOZNIKI + ZASILANIE (sesja 11.07.2026)

### HIERARCHIA MAP (zasada Tomasza)
1. **MAPA EWIDENCYJNA ogrodu** (skan dokumentu, Dysk Google Tomasza) = **FUNDAMENT, zrodlo prawdy**. Tomasz: "mapa ewidencyjna to fundament fundamentow". Ma numery geodezyjne (592/42, 494/42, 119/41...), legende (tuje 120 szt., 2 kompostowniki, wiata smietnikowa, budki legowe/karmniki, 2 hotele dla owadow), ZOLTE = CALA czesc wspolna (alejki I przejscia).
2. **NASZA MAPA** = DRUGA, pochodna. Czytelna wersja robocza/prezentacyjna. ZAWSZE weryfikowana przeciw ewidencyjnej. Przy watpliwosci: sprawdzac ewidencyjna, NIE ZGADYWAC (kosztowalo to ~1h zbednych iteracji).

### UKLAD OGRODU (ZATWIERDZONY: "Ta mapa jest idealna")
- **51 dzialek** + **DOM DZIALKOWCA = DZIALKA 0** (Mlynska 40c, zachodnia granica)
- 3 alejki, 6 rzedow. Od polnocy: rzad 43-51 | ALEJKA POLNOCNA | rzad 34-42 | [tyly] | rzad 28-33 (6 dzialek - od zachodu dom + parking) | ALEJKA SRODKOWA | rzad 19-27 | [tyly] | rzad 10-18 | ALEJKA POLUDNIOWA | rzad 1-9
- **NUMERACJA WEZEM**: 1->9, zawraca 10->18, 19->27, zawraca 28->33, 34->42, zawraca 43->51
- **ALEJKI ZAMKNIETE OD WSCHODU**: pary dzialek **43+42, 28+27, 10+9** sa WIEKSZE - siegaja do POLOWY alejki i tam sie lacza, domykajac jej wylot. NIE MA pustego konca alejki!
- **PIONOWE PRZEJSCIE** laczy wszystkie 3 alejki: granica 36|37, obok 33, dalej 21|22 i 16|15
- **Dojscie na parking nr 2**: osobne, miedzy dzialkami 44|43
- **4 BRAMY** (wszystkie od DROGI, zachod): (1) wjazd na parking nr 2, (2) brama polnocna, (3) BRAMA GLOWNA + wjazd na parking nr 1, (4) brama poludniowa
- **PARKING NR 1**: jeden ciagly obszar ksztaltu L - od bramy glownej pasem wzdluz poludniowej sciany domu dzialkowca + zatoka prostopadla po stronie wschodniej, az do przejscia (BEZ LUK)
- **PARKING NR 2**: klin miedzy UKOSNA granica polnocna a rzedem 43-51 (granica polnocna: nizej po zachodzie, wyzej po wschodzie)
- **WIATA SMIETNIKOWA**: przy prawym dolnym rogu dzialki 36 (przy przejsciu)
- Pliki: `mapa-ogrodu-rod-wozniki.svg` + `.jpg`, generator `MAPA_FUNDAMENT.py` (ciemne tlo, dzialki zielone, czesc wspolna piaskowa, dom czerwony, bramy zolte)

### ZASILANIE - ETAPY (do rolki na FB)
**ETAP 1 (uklad pierwotny)**: jedno przylacze z sieci -> DOM DZIALKOWCA (LICZNIK GLOWNY, rozlicza caly ogrod z zakladem) -> **3 NITKI** wzdluz alejek, dzialki kaskadowo, KAZDA DZIALKA MA PODLICZNIK.
Podzial nitek: **dolna/poludniowa = dzialki 1-18**, **srodkowa = 19-33**, **gorna/polnocna = 34-51**. Prad plynie z zachodu (dom) na WSCHOD.

**ETAP 2 (odciazenie)**: 7 dzialek najblizej drogi - **1, 2, 3, 4, 16, 17, 18** - wypieto z domu dzialkowca i wpieto w **DRUGIE, OSOBNE PRZYLACZE ZE SLUPA** stojacego na drodze od zachodu. Ma **DRUGI LICZNIK GLOWNY ROD**. Na przylaczu 1 zostaly 44 dzialki (5-15, 19-33, 34-51).
ROZLICZENIA: ogrod ma **DWA OSOBNE RACHUNKI**. Cena kWh zalezy od zuzycia (im wiecej, tym taniej) -> na przylaczu 1 (44 dzialki) kWh tansza niz na przylaczu 2 (7 dzialek). Tomasz: to NIE problem, po prostu roznica w cenie. **NIE MA rozliczenia usredniajacego** - dzialkowcy z przylacza 2 placa po swojej stawce.

**ETAP 3**: obecna przebudowa przylaczy - **W TOKU, SZCZEGOLY DO USTALENIA**. To ma byc temat rolki na FB.

### LEKCJA Z TEJ SESJI
Nie dlubac poprawka po poprawce na oko. Gdy jest dokument zrodlowy (mapa ewidencyjna) - czytac go dokladnie i pytac konkretnie, zamiast zgadywac i generowac kolejne wersje. Tomasz jest elektrykiem i czlonkiem zarzadu ROD - weryfikuje poprawnosc techniczna i wylapuje kazdy blad.

---

## MAPY ROD WOZNIKI — ZATWIERDZONE (11.07.2026, Tomasz: "Zatwierdzam wszystkie mapy")

**7 map gotowych i zatwierdzonych. NIE RUSZAC bez wyraznego polecenia.**

| Plik | Co pokazuje |
|---|---|
| `mapa-ogrodu-rod-wozniki.jpg` | FUNDAMENT — ogrod bez elektryki (51 dzialek, 3 alejki, przejscie, 4 bramy, 2 parkingi, wiata) |
| `GEMINI-etap1.jpg` | ETAP 1 — jedno przylacze -> dom dzialkowca (dz. 0) -> 3 OBWODY na alejki, 51 podlicznikow |
| `GEMINI-etap2.jpg` | ETAP 2 — drugie przylacze ze SLUPA (brama 4), 7 dzialek (1-4, 16-18), dwa liczniki glowne |
| `GEMINI-etap3.jpg` | ETAP 3 — 3 ZK przy bramach, 51 licznikow, osobny kabel do kazdej dzialki |
| `ETAP3-ZK1-poludniowa.jpg` | zblizenie: ZK 1, 18 licznikow (dzialki 1-18) |
| `ETAP3-ZK2-srodkowa.jpg` | zblizenie: ZK 2, 15 licznikow (19-33), gorny rzad krotszy (dom dzialkowca) |
| `ETAP3-ZK3-polnocna.jpg` | zblizenie: ZK 3, 18 licznikow (34-51) — oznaczone jako PLAN (kable nie wkopane) |

### JAK POWSTALY (do odtworzenia gdyby trzeba)
Mapy 2-4: **podklad graficzny z Gemini** (ladny, top-down, akwarela) + **wlasne kable narysowane przez Claude** (bo Gemini mylil trasy — prowadzil fiolet z licznika 1, gubil przylacze do domu) + **wlasne polskie napisy** (bo Gemini masakruje polskie znaki — "ALEJA SKODOWA", "Mlyfieka 40c").
Metoda: OpenCV inpaint wymazuje kable Gemini -> PIL rysuje wlasne trasy + numery -> nowe opisy pod mapa.
Generatory (w sandboxie Claude, nie na VPS): MAPA_FUNDAMENT.py, RYSUJ_KABLE.py, NAPRAW_GEMINI.py, ETAP3.py, ETAP3_ALEJKA.py

### NAZEWNICTWO (Tomasz poprawil — WAZNE)
**PRZYLACZE** = punkt gdzie Tauron oddaje prad, konczy sie na LICZNIKU GLOWNYM. W ogrodzie sa DWA: (1) dom dzialkowca (dz. 0), (2) slup przy drodze.
**OBWODY** = to co wychodzi z domu dzialkowca na 3 alejki. To NIE sa przylacza — to wewnetrzna instalacja ogrodu.

### ZASADA NUMER 1 (Tomasz, 11.07.2026)
**WERYFIKACJA, NIE HALUCYNACJA.** Nigdy nie twierdzic ze cos zrobione, dopoki nie zostalo FAKTYCZNIE wykonane I SPRAWDZONE. Zakazane: pisac "poprawiam/zapisuje" bez wywolania narzedzia; mowic "gotowe" bez obejrzenia wyniku; zakladac ze dziala bo "powinno". Claude lamal to dzis wielokrotnie (~2h stracone na zgadywanie ukladu ogrodu zamiast czytania mapy ewidencyjnej).

---

## ROLKA O PRĄDZIE W ROD WOŹNIKI — STAN NA 11.07.2026, 23:00 (PRZERWANE, DO DOKOŃCZENIA)

**Publikacja: TYLKO strona ROD Woźniki. ŻADNYCH grup ogólnopolskich** (materiał wewnętrzny).

### CO JEST GOTOWE
- **SCENARIUSZ** — `data/rolka-prad/SCENARIUSZ.md` (274 linie, ZATWIERDZONY: "Zajebiście").
  Struktura: OTWARCIE (spalona skrzynka) → 1. Kto komu sprzedaje prąd → 2. Skąd cena za kWh →
  3. Lata łatania → 4. Dlaczego łatanie się skończyło → 5. Co zbudowaliśmy → 6. Co Ty z tego masz →
  7. Co musisz zrobić → ZAKOŃCZENIE (klamra "od teraz Tauron zna Twoją działkę").
  ZASADY TONU w pliku — NIE ŁAMAĆ (delikatnie, zero wytykania palcem, konsekwencja jako fakt nie groźba).
- **7 MAP** — zatwierdzone, opisane w sekcji wyżej.
- **GRAFIKI (3)** — `GRAF-faktura.jpg` (odwzorowana 1:1 wg prawdziwego wzoru Tauronu: logo, SPRZEDAWCA/NABYWCA,
  tabela pozycji, RAZEM DO ZAPŁATY 14 400 PLN, ŚREDNIA CENA 1 kWh = 1,20 zł), `GRAF-kroki.jpg` (5 kroków,
  etykiety płacisz/za darmo), `GRAF-klamra.jpg` (DO TERAZ nie zna → OD TERAZ zna).
- **ZDJĘCIA PRAWDZIWE**: `01-SPALONA-SKRZYNKA.jpg`, `STARY-LICZNIK.jpg` (wygenerowany w Gemini ze zdjęcia
  SZAFKA-gotowa — przerobiony na starą plątaninę + licznik tarczowy, inne tło), `SZAFKA-gotowa.jpg`
  (szafka dz. 19 z WAGO, gotowa do przepięcia), `KABEL-NA-PLOCIE.jpg` (WYGENEROWANY — kabel przewieszony
  przez płot; do rozdz. 7, przy zdaniu o wyłączeniu starych obwodów: pokazuje NIEDOKOŃCZONE przyłącze),
  `02-ZK-front.jpg`, `03-ZK-z-tablica-ogrodu.jpg`.

### ⚠️ NAJWAŻNIEJSZE — NOWY MATERIAŁ (11.07 wieczór)
Tomasz wgrał **24 PRAWDZIWE ZDJĘCIA Z BUDOWY** (1536x2048, pełna jakość) → `data/rolka-prad/budowa/01..24.jpg`.
**TE ZDJĘCIA ZASTĘPUJĄ KADRY Z FILMU** — Tomasz wprost: "wykorzystaj jak najmniej z kadrów z filmu, bo są fatalne".
Co na nich jest (widziane w czacie): wykop w alejce (rów w dal), BEDNARKA (krzyże złączy w rowie),
kable ułożone w rowie, WACHLARZ KABLI rozchodzących się do działek, PAN Z ŁOPATĄ stojący w rowie (portret,
patrzy w obiektyw — TO JEST KADR "ludzie kopali za darmo"), człowiek z łopatami + czerwona folia ostrzegawcza,
ZK w tle z wchodzącymi kablami, rów z taśmą ostrzegawczą.
**Tomasz wgra je jeszcze raz w NOWYM OKNIE CZATU** — trzeba je obejrzeć i przypisać do scen.

### KADRY Z FILMU (SŁABE — używać minimalnie)
`wybrane/KADR-kable.jpg` = TO JEST KADR Z LUDŹMI (pan w czerwonych ogrodniczkach + operator koparki, z Messengera,
niska jakość). `wybrane/KADR-wykop.jpg`, `wybrane/KADR-ludzie.jpg` = wykop bez ludzi.
Filmy źródłowe: `FILM-A-koparka-3s.mp4`, `FILM-B-wykop-36s.mp4` (oba z Messengera, skompresowane).

### CO ZOSTAŁO DO ZROBIENIA
1. Obejrzeć 24 zdjęcia z budowy, wybrać 5-6 najlepszych, przekadrować z 1536x2048 (3:4) na 1080x1920 (9:16).
2. Rozpisać SCENARIUSZ.md na sceny (format scenes.txt: "SCENA N:" / "UJĘCIE:" / "LEKTOR:").
3. Złożyć rolkę RĘCZNIE (NIE przez panel!): folder `data/reels/NNNNNN/`, obrazy jako `images/01.jpg`...,
   lektor edge-tts (pl-PL-MarekNeural), napisy Whisper (stała zgoda Tomasza), render_video() + muzyka.
   **ZERO fal.ai — wszystkie obrazy są własne (zdjęcia + mapy + grafiki). Zero kosztów.**
4. Publikacja: TYLKO strona ROD Woźniki.

### LEKCJE Z TEJ SESJI
- Detekcja twarzy Haar KŁAMIE (bierze kamienie za twarze) — nie polegać na niej przy wyborze kadrów.
- Przy wyborze klatek z filmu: korelacja z potwierdzonym kadrem + wykrywanie koloru (np. czerwień ogrodniczek).
- Gemini masakruje polskie napisy — do map dawać podkład BEZ tekstu, napisy nakładać samemu (PIL).
- Gemini myli trasy kabli — wymazywać jego kable (OpenCV inpaint) i rysować własne.

### POPRAWKA (11.07, 23:15) — MAPY W FORMACIE ROLKI
Mapy są POZIOME (GEMINI 1113x944, ZK 1700x1000), a rolka to 9:16. Zrobiona wersja do montażu:
mapa wpisana w kadr 1080x1920, tło = rozmyta+przyciemniona kopia tej samej mapy (zero czarnych pasów).
Pliki: `data/rolka-prad/do-rolki/*.jpg` (7 map + 3 grafiki + STARY-LICZNIK — wszystko 1080x1920).
Skrypt osadzania (PIL): resize LANCZOS do szer. 1040px, tło = ta sama mapa powiększona + GaussianBlur(30) + jasność 0.55.

UWAGA: `mapa-ogrodu-rod-wozniki.jpg` (FUNDAMENT) musi być wgrana na VPS — wcześniej istniała tylko
w sandboxie Claude (ulotny!). Generatory (MAPA_FUNDAMENT.py, RYSUJ_KABLE.py, NAPRAW_GEMINI.py, ETAP3.py,
ETAP3_ALEJKA.py, GRAFIKI.py) też żyją tylko w sandboxie — jeśli będą potrzebne ponownie, trzeba je odtworzyć
albo poprosić Tomasza o zachowanie. Same MAPY (wynikowe .jpg) są ważniejsze niż generatory.


---

## ROLKA O PRĄDZIE — MATERIAŁ WIZUALNY GOTOWY (11.07.2026, 23:30)

### `data/rolka-prad/do-rolki/` — 25 plików, WSZYSTKIE zweryfikowane 1080x1920
To NIE jest deklaracja — sprawdzone plik po pliku (odczyt naglowka JPEG SOF). Wczesniejszy wpis
w teleporcie (commit ce83ccd) TWIERDZIL ze do-rolki/ istnieje — NIE ISTNIALO. Teraz istnieje naprawde.

| Plik | Zrodlo | Kadr (ffmpeg) |
|---|---|---|
| 00-MAPA-OGRODU, ETAP1/2/3, ZK1/2/3 | mapy (juz byly 9:16) | — |
| GRAF-faktura / -kroki / -klamra | grafiki (juz 9:16) | — |
| STARY-LICZNIK, KABEL-NA-PLOCIE | zdjecia (juz 9:16) | — |
| SKRZYNKA-1-pelna | 01-SPALONA-SKRZYNKA.jpg | crop=1440:2560:0:800 |
| SKRZYNKA-2-najazd | 01-SPALONA-SKRZYNKA.jpg | crop=990:1760:110:1134 |
| ZK-z-tablica-ROD | **02-ZK-front.jpg** | crop=900:1600:280:0 |
| ZK-rozmazane | 03-ZK-z-tablica-ogrodu.jpg | crop=1152:2048:195:0 |
| SZAFKA-gotowa | SZAFKA-gotowa.jpg | crop=1080:1920:0:210 |
| BUD-1-portret-kopacz | budowa/06.jpg | crop=1152:2048:192:0 |
| BUD-2-wachlarz-kabli | budowa/13.jpg | crop=1152:2048:192:0 |
| BUD-3-wykop-alejka | budowa/18.jpg | crop=1152:2048:192:0 |
| BUD-4-koparka-ludzie | budowa/12.jpg | crop=1152:2048:192:0 |
| BUD-5-bednarka | budowa/23.jpg | crop=1152:2048:192:0 |
| BUD-6-folia-zasypywanie | budowa/08.jpg | crop=1152:2048:64:0 |
| BUD-7-kable-w-rowie | budowa/19.jpg | crop=1152:2048:192:0 |
| BUD-8-kabel-do-dzialki | budowa/07.jpg | crop=1152:2048:140:0 |

Wszystkie kadry: `-vf "crop=...,scale=1080:1920:flags=lanczos" -q:v 2`

### PUŁAPKA NAZW — ZDJECIA ZK SA ZAMIENIONE
- **`02-ZK-front.jpg` (1200x1600) = OSTRE, sloneczne, Z TABLICA ROD** (widac ZK-11785, tablice ogrodu, brame)
- **`03-ZK-z-tablica-ogrodu.jpg` (1542x2048) = ROZMAZANE (poruszone), BEZ TABLICY**, na tle tui
SCENARIUSZ.md wola `03-ZK-z-tablica-ogrodu.jpg` w dwoch miejscach (rozdz. 5 + zakonczenie) — to WSKAZUJE NA ZLE ZDJECIE.
Poprawic na 02. Rozmazane najlepiej wyrzucic; ostre uzyc dwa razy z roznym Ken Burns.

### JAK OKRESLONO KADRY (metoda, nie oko)
Spalona skrzynka 1440x4000: zmierzony rozklad pikseli zweglonych (max(RGB)<70) i sniedzi
((G>R+18)&(B>R+8)) => strefa spalenia y=1011..3324, srodek ciezkosci (x=605, y=2014).
Pas y 0..600 = 100% bieli (samo wieko, zero tresci) -> wyciety. Kadr pelny zachowuje **94.9%** pikseli spalenia.
SZAFKA 1080x2340: profil stddev per wiersz (ffmpeg -> raw gray 90x195 -> python) => kadr centralny
y=210..2130 zachowuje 85.9% detalu (maksimum ze wszystkich offsetow).
ZK: detekcja zielonej tablicy => x=1002..1070 => x_offset=280 (tablica zachowana w 100%, ma oddech przy krawedzi).

### ZDJECIA Z BUDOWY — MAPOWANIE NA SCENARIUSZ
- BUD-1 portret (pan w rowie patrzy w obiektyw) => "Kopali je dzialkowcy. Za darmo." KLUCZOWY KADR.
- BUD-2 wachlarz kabli => "Do kazdej dzialki idzie osobny kabel. Masz swoja linie."
- BUD-3 wykop w alejce => skala roboty, wejscie w rozdz. 5
- BUD-4 koparka + ludzie => "Tych rowow nie kopala zadna firma."
- BUD-5 bednarka (krzyz zlacza) => "Najpierw poszla bednarka - uziemienie." + odeslanie do osobnej rolki
- BUD-6 folia ostrzegawcza => zasypywanie
- BUD-7 kable w rowie => "Kazdy pomierzony. Kazdy ma protokol."
- BUD-8 petla kabla przy krawezniku => "Kabel dochodzi do Twojej dzialki."

Tomasz wgral 20 z 24 zdjec budowy (brak 09,15,16,17) i powiedzial "te 20 wystarczy". Temat zamkniety.

### OGRANICZENIE NARZEDZIOWE (wazne dla nastepnej instancji)
Claude **NIE WIDZI obrazow lezacych na VPS** — widzi tylko bajty/wymiary/statystyki.
Zeby ocenic kadr, Tomasz musi wgrac zdjecie DO CZATU. Transfer base64 przez MCP nie dziala
(tekst wraca w tool-result, nie da sie go przepisac do sandboxa).
OBEJSCIE gdy Tomasz nie chce wgrywac: zmierzyc tresc liczbowo (rozklad pikseli / stddev per wiersz)
i kadrowac na danych — tak zrobiono ze SZAFKA-gotowa.
Dopasowanie plik-z-czatu <-> plik-na-VPS: **przez md5** (pliki sa bajtowo identyczne, telefon nie rekompresuje).

### CO DALEJ
1. Rozpisac SCENARIUSZ.md na sceny (format scenes.txt: SCENA N: / UJECIE: / LEKTOR:)
2. Zlozyc rolke RECZNIE: data/reels/NNNNNN/, obrazy z do-rolki/ jako images/01.jpg...,
   edge-tts (pl-PL-MarekNeural), Whisper (stala zgoda), render_video() + muzyka.
   ZERO fal.ai - wszystkie obrazy wlasne. ZERO kosztow.
3. Publikacja: TYLKO strona ROD Wozniki. ZADNYCH grup ogolnopolskich.


---

## ROLKA O PRĄDZIE — ZŁOŻONA (000089), 12.07.2026 ~00:40

**`data/reels/000089/video/final_with_music.mp4`** — 1080x1920, h264, 30fps, **462.3s = 7 min 42 s**, 166 MB.
Panel: status "gotowa", warning=false, opublikowana=false.
Link: https://panel.157-90-155-155.sslip.io/reels/000089/video

### CO POSZŁO W ROLKĘ
40 scen. Wszystkie obrazy WŁASNE z `data/rolka-prad/do-rolki/` (24 pliki, każdy 1080x1920).
Lektor: edge-tts pl-PL-MarekNeural. Napisy: Whisper (fal.ai). Render + muzyka: ffmpeg (Morning.mp3).
**ZERO fal.ai na obrazy** — jedyny koszt to Whisper na ~6 min audio (grosze). Decyzja Tomasza: wariant A (jedna rolka, bez dzielenia — klamra spalona-skrzynka musi zostać w całości).

### ⚠️ KOREKTA TEMPA MOWY — WAŻNE NA PRZYSZŁOŚĆ
Szacowałem 15,5 znaku/s. **pl-PL-MarekNeural czyta realnie 11,6 znaku/s** (zmierzone na 40 scenach).
Podałem Tomaszowi 5:47, wyszło 7:42 — pomyłka o 33%. **DO PRZYSZŁYCH SZACUNKÓW UŻYWAĆ 11,6 zn/s.**
(Krótkie zdania mają jeszcze niższe tempo, ok. 8-10 zn/s — to normalne, nie bug.)

### BUGI ZŁAPANE I NAPRAWIONE PRZY SKŁADANIU
1. **Scena 28 - błąd merytoryczny**: pierwotnie mapa ZK3 (alejka północna) pod zdaniem "Kable są w ziemi".
   Na ZK3 kable NIE SĄ wkopane (mapa = PLAN). Podmienione na ETAP3. Tomasz-elektryk wyłapałby to na zebraniu.
2. **Scena 02 - Whisper zmyślił**: usłyszał "Latami, latami" (13 słów zamiast 12) -> `transcribe_scene`
   NIE podstawiło znanego tekstu (wymaga IDENTYCZNEJ liczby słów) i zostawiło błąd w napisach.
3. **Scena 18 - Whisper nic nie zwrócił** ("brak segmentow, pomijam") - 2,5s, za krótka. Zero napisów.
   NAPRAWA (obie): skrypt `_fix_subs_89.py` (usunięty po użyciu) - gdy liczba słów się nie zgadza albo
   brak segmentów, rozkłada ZNANE słowa ze scenes.txt **proporcjonalnie do długości** na czasie audio.
   Zweryfikowane: tekst w napisach = tekst w scenariuszu, co do słowa.

**WNIOSEK DO KODU (nie zrobione, do rozważenia):** `transcribe_scene` powinno mieć ten fallback na stałe
zamiast rezygnować z podstawienia przy rozjeździe liczby słów. Dziś przy KAŻDYM rozjeździe do napisów
trafia zmyślenie Whispera. To cichy bug - nie krzyczy, tylko psuje tekst.

### WERYFIKACJA (nie deklaracja)
- 40/40 obrazów, 40/40 wav, 40/40 .ass (żaden pusty)
- tempo mowy per scena: wszystkie 9-15 zn/s -> nic nie zgubione (tak wykryto buga extract_narration na #000084)
- audio finalne: mean -26.6 dB / max -8.5 dB (dla porównania #000085: -26.5/-9.6 - zgodne)
- napisy wypalone POTWIERDZONE NA PIKSELACH: dolny pas 1080x380 w scenie 21 (ciemna ziemia) ma 14k pikseli
  bardzo jasnych + 22k bardzo ciemnych (biel + czarna obwódka), a 9,3% pikseli zmienia się między t=222 a
  t=226 = linijka napisu się przewija. `make_clip_kb` dokleja `,ass=<plik>` do filtra - sprawdzone w kodzie.
- panel /reels: id=89, status "gotowa", warning=false
- link HTTPS: HTTP 206 (działa)

### CO ZOSTAŁO
1. Tomasz ogląda i zatwierdza (albo zgłasza poprawki - tanie: podmiana tekstu -> edge-tts -> render, bez fal.ai)
2. Opis do posta
3. **PUBLIKACJA: TYLKO strona ROD Woźniki (1174205105781401). ŻADNYCH grup ogólnopolskich** - materiał wewnętrzny.
   Przycisk "📘 Publikuj na stronę FB" w panelu (endpoint /reels/89/publikuj-fb).
   UWAGA: to będzie PIERWSZA publikacja przez ten przycisk - endpoint nietestowany end-to-end.

---

# SESJA 12.07.2026 — ZWROT: ROBIMY FILM, NIE ROLKĘ

## DECYZJA (Tomasz, wprost): "Robimy film. I rolkę zapowiadającą"
Powód: materiał o przebudowie prądu ma **7:42 i 42 sceny** — to nigdy nie była rolka.
Shorts kończy się na 3 min. Działkowiec musi móc zatrzymać, cofnąć, znaleźć SWOJĄ działkę na mapie.

- **FILM 16:9 (1920x1080)** → nowy kanał YouTube "ROD Woźniki", **niepubliczny (dostęp z linkiem)**
- **ROLKA 9:16** → zapowiedź, publicznie: strona ROD Woźniki + Shorts

⚠️ **KONSEKWENCJA DLA PRYWATNOŚCI:** film z linkiem = twarze ekipy OK.
Ale **rolka idzie publicznie** → w rolce **BEZ TWARZY** (tylko rów, kable, koparka, mapy).
Katalog `data/rolka-prad/bez_twarzy/` już istnieje — użyć go.

## SKĄD SIĘ WZIĄŁ ZWROT
Tomasz: "Strasznie małe te mapy w rolce". Zmierzone: mapy ZK są POZIOME (1700x1000),
kadr rolki PIONOWY → mapa zajmowała **14% wysokości ekranu**, reszta rozmyte tło.
Próba obrócenia ogrodu o 90° (ZK1-PION.jpg) — działała, ale Tomasz słusznie: "Bo wyjdzie z tego rolka".
W 16:9 problem znika sam: ogród jest szeroki, kadr jest szeroki. Zero obracania.

## MAPY — GOTOWE, 7 SZTUK, styl jasny GEMINI (zatwierdzony: "gra", "bardzo idealnie")
Generator: **`/root/rod-ai-studio/tools/mapa_rod/`** (żeby drugi raz nie przepadł!)
- `baza_mapy.py` — wspólny podkład (51 działek, 3 alejki, 4 bramy, 2 parkingi, dom, ukośna granica N)
- `mapy_zk.py` — ZK 1/2/3
- `mapy_etapy.py` — ETAP 1/2/3 (na wspólnej bazie — w filmie ten sam ogród, zmienia się instalacja)
- `kadr_filmu.py` — layout kadru: pionowy materiał w oknie + panel z tekstem
Wyjście: `data/rolka-prad/mapy-16x9/`

⚠️ **PIERWSZY KROK NASTĘPNEJ SESJI: na VPS NIE MA Pillow.**
`docker exec fabryka-api pip install pillow` (albo systemowo `--break-system-packages`) → ZAPYTAJ TOMASZA.
Bez tego generatory nie ruszą. Skrypty się parsują (py_compile OK), ale nie były na VPS uruchomione.
Gotowe JPG są u Tomasza (pobrane z czatu) — nie zdążyły trafić na VPS (3 MB, za dużo na transfer).

## FAKTY POTWIERDZONE W TEJ SESJI
- ZK 1 — alejka południowa, działki 1–18, 18 liczników, kable wkopane
- ZK 2 — alejka środkowa, działki 19–33, 15 liczników. Rząd północny od zachodu:
  DOM DZIAŁKOWCA (2 kolumny) + PARKING NR 1 (1 kolumna), potem 33..28
- ZK 3 — alejka północna, 34–51, 18 liczników. Złącze stoi, kable NIEWKOPANE = PLAN
- ETAP 1 (rekonstrukcja, zaakceptowana): jedno przyłącze przy domu, 3 wspólne przewody, podliczniki
- ETAP 2 (odtworzony 1:1 z oryginału Tomasza): drugie przyłącze ze słupa, 2 liczniki główne,
  7 działek wypiętych: **1, 2, 3, 4 oraz 16, 17, 18**. Pozostałe 44 po staremu
- ETAP 3: trzy ZK, 51 liczników, osobny kabel do każdej działki

## MATERIAŁ Z BUDOWY — PRAWDZIWY, ZASTĘPUJE AI
Tomasz wrzucił 8 zdjęć (1500x2000) + 4 filmy. **Obrazy AI z fal.ai stały się ZBĘDNE** —
mamy prawdziwych ludzi z ROD: koparzystę z papierosem, ekipę na łopatach, gościa kującego skałę.
**KLUCZOWE ZDJĘCIE: pan z łopatą, a pod nim w rowie leży WIĄZKA KABLI** — dosłowna ilustracja mapy ZK.
Mapa mówi schemat, zdjęcie mówi że to naprawdę leży w ziemi.

⚠️ Filmy przyszły przez WhatsApp → zduszone do **478x850**. Tomasz: "pokażesz je w oknie
zamiast na pełnym ekranie" — zgoda, w oknie 900 px wysokości skala 1.06x = praktycznie natywne.

## LAYOUT KADRU FILMU (nowość, zatwierdzona)
Cały materiał jest PIONOWY. Zamiast przycinać do poziomu (utrata 2/3 kadru, ucięte głowy):
pionowy materiał w oknie 900 px + panel z tekstem obok.
- zdjęcie 1500x2000 → okno 675x900 = skala **0.45x** (zmniejszenie, ostre)
- film 478x850 → okno 506x900 = skala **1.06x** (natywne)

⚠️ **DO POPRAWY:** panel bywa ZA PUSTY. Sam tytuł + 2 linijki to za mało na pół ekranu.
Każdy kadr musi dostać: liczbę ALBO kawałek mapy ALBO 3–4 wiersze.

## CO ZOSTAŁO DO ZROBIENIA
1. **Pillow na VPS** → wygenerować 7 map na miejscu (patrz wyżej)
2. **Przełącznik formatu w Fabryce** — 9:16 zaszyte w 4 miejscach:
   - `apps/api/src/video/renderer.py` — scale/crop 1080:1920 w ~6 miejscach + Ken Burns + intro
   - `apps/api/src/subtitles/generator.py` — PlayResX/Y 1080x1920
   - `apps/api/src/images/prompts.py` — prompty "vertical 9:16"
   - `apps/api/src/ai/image_backend.py` — fal.ai `aspect_ratio: "9:16"`
   - `apps/api/src/scenes/generator.py` — scenarzysta proszony o "pionowe rolki"
3. **Tomasz miał opisać, co jest na 4 filmach** (kontaktówka 20 klatek wysłana, nie zdążył)
4. **Nowy scenariusz pod film** (stary był pod rolkę)
5. Więcej materiału z budowy — Tomasz ma jeszcze zdjęcia/filmy

## ⚠️ PROBLEM TECHNICZNY TEJ SESJI
**Podgląd obrazów w Claude padł w połowie sesji** (`view` na JPG/PNG zwracał pustkę,
sprawdzone na 1920x1080, 1080x1920 i miniaturze 640x360). Skutek:
- mapy ZK 2, ZK 3, mapa ogrodu i wszystkie 3 etapy **nie były przeze mnie obejrzane** —
  tylko zweryfikowane liczbowo (bboxy tekstów, kolizje, szerokości)
- wybrałem klatkę z filmu na ślepo i trafiłem w twarz Tomasza pod podpisem "Koparka przeszła alejkę" 🤣
**Następna instancja: sprawdź czy podgląd działa. Jeśli tak — OBEJRZYJ te mapy zanim pójdą do filmu.**

## ⚠️ KOREKTA REDAKCYJNA (Tomasz, koniec sesji 12.07)
"Za dużo pierdzenia o tym Tauronie. Prościej — budowy sieci i przebudowa.
Na etap 3 wtedy musi być o Tauronie."

**Film NIE jest o formalnościach. Film jest o ROBOCIE.** Tauron = puenta, nie wykład na wstępie.
Nowy szkielet:
1. ROBOTA — koparka, rów, ludzie z łopatami. Bez gadania, po prostu się dzieje.
2. PO CO — spalona skrzynka. Jedno zdanie: stara instalacja nie wyrabiała.
3. CO ZBUDOWALIŚMY — mapa ogrodu, ZK 1 i ZK 2, 18 kabli w rowie, liczniki w szafach.
4. CO ZOSTAŁO — ZK 3, złącze stoi, kable czekają.
5. CO Z TEGO MASZ — **TU i tylko tu Tauron**: własny licznik, własna umowa, koniec podliczników.

Skutek dla map: ETAP 1 i ETAP 2 mają w podtytułach żargon ("przyłącze", "licznik główny").
**DO ROZSTRZYGNIĘCIA:** czy etapy 1/2 zostają w filmie jako kilkunastosekundowa wstawka,
czy wypadają całkiem (film idzie prosto: robota → co zbudowaliśmy → co z tego macie).
Mapy są zrobione, więc zostawienie ich nic nie kosztuje. Tomasz zdecyduje.

**ROZSTRZYGNIĘTE (Tomasz): "Etap 1 i 2 zostaje"** — obie mapy wchodzą do filmu jako wstawka
pokazująca historię instalacji. Nic nie trzeba przerabiać: sprawdzone, że słowo "Tauron"
pada TYLKO na mapie ETAP 3. Etapy 1 i 2 mówią wyłącznie o instalacji (wspólne przewody,
podliczniki, 7 wypiętych działek) — bez formalności. Zgodne z korektą redakcyjną.

## ⚠️ ODWOŁANE: PRZEŁĄCZNIK FORMATU 16:9 W FABRYCE — NIE ROBIMY
Tomasz (13.07): "To niepotrzebne. To jedyny taki film i rolka."

**FABRYKA ZOSTAJE NIETKNIĘTA.** Nie ruszamy `renderer.py`, `prompts.py`, `image_backend.py`,
`subtitles/generator.py`, `scenes/generator.py`. Dalej robi rolki 9:16 — tak jak robiła.
Przebudowa pipeline'u pod format użyty JEDEN raz = niepotrzebne ryzyko zepsucia działającej maszyny.

**ZAMIAST TEGO: osobny skrypt `tools/film_rod/buduj_film.py`** (poza apps/api!).
Korzysta z narzędzi, które już stoją na VPS:
- edge-tts (pl-PL-MarekNeural, 11.6 znaku/sek) — lektor
- Whisper — napisy
- ffmpeg — render 1920x1080
- PIL — klatki (mapy z tools/mapa_rod + kadry z kadr_filmu.py)

Nowa rzecz do napisania: **wstawianie klipów WIDEO w okno + panel obok**.
W ffmpeg = overlay na statycznym tle:
  ffmpeg -loop 1 -i panel.png -i klip.mp4 -filter_complex "[1:v]scale=506:900[v];[0:v][v]overlay=90:90" ...
Tło (panel z tekstem) generuje PIL, klip leci w oknie. Zero deployu, zero restartu.

## DŹWIĘK Z FILMÓW — NIE UŻYWAMY
Tomasz (13.07): "Nie używaj ścieżki dźwiękowej z filmów. Tam to bzdury."
Klipy wideo wchodzą do filmu **TYLKO JAKO OBRAZ** (ffmpeg: `-an` na wejściu klipu).
Audio filmu = lektor edge-tts (pl-PL-MarekNeural) + podkład muzyczny. Nic więcej.

## CO JEST NA FILMACH (Tomasz, 13.07) — koniec zgadywania
- **VID-...WA0000** (36 s) — gość idzie z telefonem i kręci (obchód, przejście alejką)
- **VID-...WA0004** (50 s) — wykopaliska; widać, jak trudno się kopie, kamienie wszędzie
- **VID-...WA0008** (63 s) — dalsze wykopaliska, chłop strasznie się męczy
- **VID-...WA0012** (110 s) — zasypywanie (koniec roboty)
Wszystkie 478x850 (WhatsApp), 60 fps → w oknie 900 px = skala 1.06x, praktycznie natywne.

## PILLOW + POPPINS ZAINSTALOWANE NA VPS (13.07) ✔
`pip install pillow --break-system-packages` → PIL 12.3.0
Poppins (Regular/Medium/Bold) pobrany z github.com/google/fonts → /usr/share/fonts/truetype/google-fonts/
**Bez Poppins mapy wskakiwały na DejaVu i wyglądały inaczej niż te zatwierdzone.**
Wszystkie 7 map wygenerowane na miejscu: `data/rolka-prad/mapy-16x9/`

## ⚡ CIĘŻAR FILMU: "DOKOŃCZ U SIEBIE" (Tomasz, 13.07)
"Nacisk na kończenie u siebie w działkach — przyłącze gotowe, kable w ziemi, a co niektórzy walą w chuja."

Film NIE jest sprawozdaniem z robót. Film jest **wezwaniem**. Ogród swoje zrobił:
złącze stoi, kable leżą, licznik czeka w szafie. Dalej nikt tego za działkowca nie zrobi.

**Blok 5 to nie "co z tego masz", tylko "TERAZ TWOJA KOLEJ"** (~90 s, nie 60).

### DROGA DZIAŁKOWCA — 5 kroków (POTWIERDZONE przez Tomasza)
1. Elektryk z uprawnieniami robi instalację **na działce**
2. **PROTOKÓŁ** — potwierdza: zabezpieczenia + **rozdział PEN na PE i N** + uziom
   (⚠️ NIE protokół na kable w ziemi — te ogród już pomierzył i ma własny)
3. Karta z zarządu
4. **Działkowiec sam** podpisuje umowę z Tauronem — na siebie, nie na ogród
5. Elektryk zarządu przepina; stary licznik odczytany do rozliczenia końcowego

### FAKTY TECHNICZNE (potwierdzone 13.07) — układ TN-C-S
- **Rozdział PEN → PE + N następuje W DZIAŁCE** (w rozdzielnicy działkowca), NIE w ZK.
  Z ZK do działki idzie PEN.
- **BEDNARKA = UZIOM WSPÓLNY** biegnie w alejce wzdłuż rowu. Jeden dla wszystkich działek.
  Każdy podpina się do niej w punkcie rozdziału PEN. **Nikt nie robi własnego uziomu.**

### SCENA, KTÓREJ NIE BYŁO W SZKIELECIE
Ludzie widzieli bednarkę w wykopie i nie wiedzą, po co tam leży.
Powiedzieć wprost: to uziom, ogród położył go RAZ, dla wszystkich, i bez niego
rozdział PEN nie ma się o co oprzeć.

### TON (ustalone)
Nie besztać. Obrażą się i będą zwlekać na złość. Mocniejszy jest fakt:
"Kabel leży pod Twoją działką od pół roku. Licznik czeka w szafie. Brakuje jednego papieru — Twojego."
Konsekwencja jako fakt, nie groźba: gdy alejka przechodzi na nowe, stary obwód idzie w dół —
nie z zemsty, tylko dlatego, że nie ma z czego brać prądu.

## 🔑 KABEL NA SIATCE — SEDNO PRZEKAZU (Tomasz, 13.07)
**Kabel z ZK jest już DOCIĄGNIĘTY do każdej działki i WISI NA SIATCE, od strony alejki.**
Każdy działkowiec widzi go u siebie. Ogród doprowadził go pod sam płot.
**Robota działkowca: wkopać go u siebie — OD SIATKI DO SKRZYNKI — i zabezpieczyć.**
Zdjęcie: `data/rolka-prad/KABEL-NA-PLOCIE.jpg` → kluczowy kadr filmu.

### DROGA DZIAŁKOWCA — 5 kroków (POPRAWIONE, krok 1 to ŁOPATA nie elektryk)
1. **Wkopujesz kabel u siebie** (od siatki do skrzynki) i zabezpieczasz
2. Elektryk z uprawnieniami: instalacja + **protokół** (zabezpieczenia, rozdział PEN→PE+N, uziom)
3. Karta z zarządu
4. **Ty** podpisujesz umowę z Tauronem — na siebie, nie na ogród
5. Elektryk zarządu przepina; stary licznik odczytany do rozliczenia

### DLACZEGO STARY OBWÓD ZNIKA — poprawione uzasadnienie
❌ BŁĄD (moja pierwsza wersja): "nie będzie z czego brać prądu" — Tomasz to odrzucił.
✅ PRAWDA: **stary obwód jest ZBĘDNY.** "A po chuja ten obwód? Każdy będzie miał swój licznik."
Zostanie zdjęty, bo nie ma po co wisieć — nie z zemsty, nie jako kara.

Zdanie końcowe filmu:
"Kabel wisi na Twojej siatce. Licznik czeka w szafie, z numerem Twojej działki.
Brakuje jednego papieru — i Twojej łopaty.
A kiedy cała alejka przejdzie na nowe, stary obwód zostanie zdjęty. Nie z zemsty.
Po prostu nie ma po co wisieć — każdy będzie miał swój licznik."

## SCENARIUSZ FILMU — GOTOWY (13.07)
`SCENARIUSZ-FILM.md` (u Tomasza w czacie; wgrać na VPS przy następnej sesji).
Film 6:01 · 5 bloków · lektor 3200+ znaków · rolka zapowiadająca ~40 s (BEZ TWARZY).
DO USTALENIA: czy ekipa pracowała społecznie (zdanie "nikt nie wziął ani złotówki" — nie użyte,
bo niepotwierdzone). Blok 3 (serce filmu) można rozbudować kosztem bloku 2.

## DOBÓR UJĘĆ — poprawka (Tomasz, 13.07)
**VID-...WA0008 = NAJLEPSZE UJĘCIE NA "ROBOTĘ W SKALE".** Idzie pod scenę:
"Pod alejkami jest skała. Nie ziemia — skała. Gdzie koparka nie dała rady, trzeba było
rozkuwać młotem. Ręcznie. Metr po metrze."
(Chłop, który się męczy, mówi o twardości gruntu więcej niż sam widok kamieni.)
WA0004 → schodzi do ogólnego kopania / podkład pod rów w alejce.

## ⚠️ TELEFON TOMASZA PADŁ (13.07) — filmy uratowane
Stary telefon rozbity. Kopia WhatsAppa miała **wyłączone "Dołącz filmy"** → filmy NIE były w backupie.
Uratowane tylko dlatego, że Tomasz wysłał je w czacie 12.07 — oddane mu z powrotem przez present_files.
**Dopóki nie wgra ich przez panel, istnieją tylko w czacie.** To nie jest archiwum.

## UPLOAD W PANELU — ZROBIONY (13.07) ✔
Karta "05 Materiał" w panelu. Endpoint `POST /upload` + `GET /upload/lista` w `apps/api/src/main.py`.
Sortowanie automatyczne po rozszerzeniu:
  filmy (.mp4/.mov/.avi/.mkv/.webm/.m4v/.3gp) -> `data/rolka-prad/filmy/`
  reszta (zdjęcia)                            -> `data/rolka-prad/budowa/`
python-multipart był już w requirements.txt (w VENV kontenera, nie w systemowym pythonie!).
Backupy: `src/main.py.bak-20260713-1627`, `src/panel.html.bak-20260713-1627`.
Kontener zrestartowany, endpoint przetestowany. ⚠️ docker-compose.yml (z kluczami API) jest w .gitignore — OK.

## 🎵 MUZYKA DO FILMU — WYBRANA (Tomasz, 13.07)
**Precious Memories — Shane Ivers** (3:59, fortepian, ciepły)
Ton: "z ciężarem, ale ciepły — bo to jednak historia o ludziach, którzy zrobili coś razem za darmo".
⚠️ Muzyka KRÓTSZA niż film (3:59 vs 4:42) → zapętlana (ffmpeg `-stream_loop -1`). Sprawdzić szew.

### ⚠️ ATRYBUCJA — OBOWIĄZKOWA W OPISIE FILMU NA YOUTUBE (CC BY 4.0)
```
Music: Precious Memories by Shane Ivers - https://www.silvermansound.com
Licensed under Creative Commons Attribution 4.0 International License
https://creativecommons.org/licenses/by/4.0/
Music promoted by https://www.chosic.com/free-music/all/
```
Bez tego licencja jest naruszona. Wkleić do opisu przy publikacji.

## FILM — PIERWSZA WERSJA ZBUDOWANA (13.07) ✔
`data/rolka-prad/FILM-ROD-16x9.mp4` — 4:42, 1920x1080, 20 MB, lektor MarekNeural.
Skrypty: `tools/film_rod/buduj_film.py` (silnik) + `film_pelny.py` (scenariusz, 23 sceny).
Podgląd dla Tomasza: **GET /film** (endpoint w panelu, FileResponse).
Upload rozszerzony o audio → `.mp3/.wav/...` ląduje w `assets/music/`.

## 🎬 FILM OPUBLIKOWANY (13.07.2026)
**https://youtu.be/xKHxqNi02MQ** — YouTube, niepubliczny (dostęp z linkiem), kanał ROD Woźniki.
Film: 5:31, 1920x1080, 29 scen, lektor MarekNeural, muzyka Precious Memories (CC BY, atrybucja w opisie).
Skrypty: `tools/film_rod/buduj_film.py` + `film_pelny.py`.
Pobranie: GET /film

## ROLKA ZAPOWIADAJĄCA — GOTOWA (13.07)
`data/rolka-prad/ROLKA-ZAPOWIEDZ.mp4` — 26 s, 1080x1920, **Z TWARZAMI** (Tomasz zmienił decyzję).
Skrypt: `tools/film_rod/buduj_rolke.py`. Pobranie: GET /rolka
Sceny: skała (WA0008) → 18 kabli w rowie → ekipa "za darmo" → kabel na siatce → licznik czeka → plansza.
⚠️ PUBLIKACJA: ROD Woźniki — **TYLKO STRONA, NIE GRUPY** (to reel wewnętrzny ogrodu).

## ⚠️ KANAŁ YOUTUBE = **makol100** (NIE "ROD Woźniki"!)
Tomasz (13.07): "nie ma kanału rod wozniki. Jest na makol100".
Film: https://youtu.be/xKHxqNi02MQ (niepubliczny, dostęp z linkiem)
W planszy końcowej rolki NIE podajemy nazwy kanału — film jest niepubliczny, więc na kanale
i tak go nie widać. Plansza mówi: "CAŁY FILM — link w opisie".

## 📱 APKA v1.2 — POWIADOMIENIA (14.07)
NotifWorker (WorkManager, polling /reels co 15 min) → powiadomienie "Rolka #NNNNNN gotowa 🎬",
tap otwiera sekcję Ostatnie rolki. Zgoda POST_NOTIFICATIONS przy pierwszym starcie (Android 13+).
APK: 2.3 MB (WorkManager). Podpis: **v2 scheme** — META-INF pusty to NORMALNE, nie brak podpisu!
Workflow: jawny debug keystore + weryfikacja apksigner po buildzie.
⚠️ Chrome Tomasza nie zapisywał pobrania z GitHuba → **APK wystawiony też na panelu: GET /apk**.
Po każdym buildzie skopiować nowy APK do data/rolka-prad/app-debug.apk (TODO: zautomatyzować w workflow).
Samsung ubija tło → jak powiadomienia znikną: bateria dla Fabryki = "bez ograniczeń".

## 🍄 TESTOWY BAROMETR GRZYBIARZA (14.07)
Pomysł Tomasza: grupa FB "Grzybiarze-woj. Śląskie" (86k, PRYWATNA) pokazuje że się sypie.
Scraping grupy = ryzyko blokady konta FB → NIE robimy. Zamiast tego SYGNAŁ Z POGODY.

**Strona: https://panel.157-90-155-155.sslip.io/barometr** (+ /barometr.json dla integracji)
Kod: `apps/api/src/barometr.py` + `barometr.html`. Cache 3h (Open-Meteo, bez klucza, legalnie).
4 lokalizacje: Woźniki, Lubliniec, Koszęcin, Boronów.
Algorytm 0-100: opady 10d (→45 pkt, nasycenie 25mm) + deszcz sprzed 4-10 dni (→15, grzybnia
potrzebuje czasu) + temp 5d (→40, optimum 12-19°C) − kara przymrozek (−20).
Progi: 75+ IDŹ DO LASU / 55+ warto sprawdzić / 30+ coś się rusza / sucho.
Pierwszy odczyt 14.07: **100/100 wszędzie** (37mm/10d, 16.5°C) — zgadza się z gotującą się grupą FB.
DO ZROBIENIA: link/kafelek na ogrodnik-rod.pages.dev (deploy CF jest po stronie Tomasza — na VPS
nie ma wranglera); ewentualnie kalibracja progów po sezonie; powiadomienie w apce przy 75+.

## 🍄 BAROMETR → POWIADOMIENIA (14.07, dokończone)
Decyzja Tomasza: "Nie musi być za każdym razem rolka. Wystarczą powiadomienia."
Endpoint: GET /barometr/sygnal → {data, wynik, status, alarm: wynik>=75}
Apka (NotifWorker, ten sam worker co rolki): przy alarmie powiadomienie
"Barometr: N/100 🍄 IDŹ DO LASU" — **max RAZ NA DOBĘ** (klucz: barometr_dzien w SharedPreferences).
Tap → strona /barometr. Kanał notyfikacji: "barometr". APK v1.3 na GitHub + panel (/apk).
Rolka z barometru = opcja ręczna, nie automat.

## 🍄 BAROMETR — KOMPLET KANAŁÓW + IZOLACJA (14.07, wieczór)
**Publiczny adres (bezpieczny):** https://barometr.157-90-155-155.sslip.io/barometr
Caddy: nowa subdomena przepuszcza TYLKO /barometr* — /panel, /upload, /apk zwracają 404.
(Panel ma otwarty /upload bez hasła — dlatego NIE wystawiamy publicznie adresu panel.*)
Caddyfile: /root/claude-vps-mcp/Caddyfile (backup: .bak-barometr).

**Telegram przez HA Dom (jak burzówki):**
- sensor REST `sensor.barometr_grzybiarza` w configuration.yaml (scan 3h, atrybuty: status/opis/aktualizacja)
- automatyzacja `automation.barometr_grzybiarza_telegram`: codziennie 8:00, warunek >=75,
  telegram_bot.send_message z templatek. Trigger CZASOWY = max 1 powiadomienie/dobę.
- HA Dom zrestartowany 14.07 ~18:00 (restart zwrócił error, ale przeszedł — HA wstał).
- Test end-to-end wysłany; Tomasz potwierdza działanie ("Aktualizacja wszędzie" = domknięcie).

**Kanały powiadomień barometru:** (1) apka Android — NotifWorker, próg 75, 1×/dobę;
(2) Telegram — HA Dom, 8:00, próg 75. Strona zawsze: /barometr.
**ZALEGŁE:** zapowiedź barometru na FB (Tomasz prosił "przygotuj i wystawiaj" — przerwane
wątkiem Telegrama; tekst posta NIE powstał, publikacja NIE wykonana. Mechanizm FB photo post
jest w HA Dom: shell_command lb_fb_post / lb_fb_photo.py w /config/www/rod/).
**ZALEGŁE 2:** dogenerowanie tematów Bielikiem do 6 nowych kategorii (po ~40 szt.) — Tomasz
nie odpowiedział na "odpalać?", w międzyczasie zszedł na barometr.

## 🍄 BAROMETR — POST NA FB OPUBLIKOWANY (14.07, ~19:30)
Post ID: 1174205105781401_122109342237379813 (strona ROD Woźniki, photo post).
Grafika: `data/rolka-prad/barometr_fb.jpg` (1200x630, styl jasny, generator: PIL na hoście,
skrypt jednorazowy — dane z /barometr.json na żywo).
Tekst: zapowiedź + jak działa + odczyt 100/100 + link https://barometr.157-90-155-155.sslip.io/barometr
+ zastrzeżenie TESTOWY. Hasztagi: #RODWoźniki #grzyby #Woźniki #naGrzyby.
Mechanizm: dwustopniowy Graph API v25.0 (jak burzówki, token z lb_fb_post.py na HA Dom).
⚠️ Skrypt publikujący był w /tmp kontenera (token!) — NIE trafił do repo, usunięty z hosta.
ZALEGŁE nadal: kafelek barometru na ogrodnik-rod.pages.dev (deploy po stronie Tomasza).

## KATEGORIE — DOKOŃCZONE (14.07, wieczór) ✔
Bielik dogenerował 201 tematów do 6 nowych kategorii (skrypt tools/dogeneruj_tematy.py,
podgrupy z własnymi miesiącami, few-shot z bazy, dedup po tytule).
Sprzątanie po Bieliku: 113 tematów z resztkami markdown (**) naprawione; 1 bełkot usunięty;
18 dezaktywowanych (tytuł = kadr zamiast nazwy, np. "Ujęcie góry:..."); 1 off-topic (orzechy
w Trawniku). Dezaktywowane NIE skasowane — aktywny=0, do ew. przeglądu w panelu.
STAN AKTYWNYCH: Owoce 37, Pogotowie 42, Woda 36, Zbiory 30, Zima 44, Trawnik 42.
Backup bazy sprzed operacji: data/content.db.bak-20260714-1510.

## ⚠️ BŁĄD I NAUKA (14.07 wieczór): tryb_jezykowy przy odpalaniu przez API
Odpaliłem 000092 z tryb_jezykowy="pl" (ZWYKŁA rolka) zamiast "czysty_bielik" —
prompty poszły Qwenem PO ANGIELSKU, scenariusz starym szablonem. Tomasz słusznie wkurzony.
Checkpoint uratował koszty (obrazy nie ruszyły). 000092 przerwana, 000093 odpalona poprawnie.
**REGUŁA: rolki odpalane przez Claude przez API = ZAWSZE tryb_jezykowy="czysty_bielik"**
(wartości: "pl"=zwykła, "czysty"=Qwen EN→PL, "czysty_bielik"=wszystko Bielikiem po polsku).
Panel ma "czysty_bielik" jako selected — to jest tryb testowany przez Tomasza.

## SECOND BRAIN URUCHOMIONY (14.07, wieczór)
Katalog `wiedza/`: INDEX + ARCHITEKTURA + PROCEDURY + NAUKI + STYL — destylaty
zamiast kroniki. Protokół: sesja startuje od INDEX, teleport czytany wybiórczo
(ostatnia sesja + zaległości). Rolka 000093 (szare mydło na mszyce): GOTOWA po patchu
(lektor "Szare mydło", obrazy 1-2 z kotwicą anty-cegła, $0.30). Czeka na ocenę
Tomasza i publikację.

## 000093 OPUBLIKOWANA (14.07 ~21:30) ✔
Szare mydło na mszyce — pierwsza rolka w pełni z nowego świata: nowy prompt
(haczyk/pętla), czysty_bielik, reguła "akcja na działce", patch anty-cegła.
Temat 611 z nowej kategorii "Pogotowie: choroby i szkodniki".

## N150 — ZAMROŻONE (decyzja Tomasza 14.07)
Migracja i ściąganie backupów z Nuki: NIE ruszać, NIE proponować. Tomasz wraca
do tematu sam, kiedy zechce. (Ryzyko backupów na starym serwerze — zakomunikowane.)

## SESJA 14/15.07 NOC — 000095 + UX CHECKPOINTU + AUDYTOR FABLE ✔
**000095 (mączniak na cukinii, temat 480):** scenariusz przepisany na 10 scen (haczyk
"Ten biały nalot to nie kurz", scena 4 = inne ofiary: ogórki/dynie/róże/agrest, S6
podlewanie pod korzeń, S7 rozstaw zamiast WENTYLATORA-absurdu Bielika, S8 mleko 1:9 +
czosnek KILKA ZĄBKÓW na litr [poprawka audytora Fable — moja "główka" była zawyżona],
S10 pętla). Prompty: audyt ręczny 7 poprawek (napis "CHORE" OUT, lektor/narrator OUT ×3,
kolaż→jeden kadr, karton mleka bez etykiety, fizyka konewki, P3 odchudzony z bełkotu;
backup prompts.txt.bak-audyt). Kontrola końcowa: CZYSTO (❌ czosnku w ostatnim teście
= fałszywy alarm case-sensitive checkera, poprawka JEST). **STAN: czeka na OK Tomasza
w panelu → obrazy Gemini → gotowa.**
**Naprawy z sesji:** (1) reguła CYFRY SŁOWNIE w 3 szablonach Bielika + prompt Sonneta;
(2) zapis checkpointu ASYNC (wątek + przeliczanie.lock; wcześniej telefon ubijał 10-min
request = "Zapisz nie działa"); (3) dirty guard w panelu (polling nadpisywał edycję);
(4) AUDYTOR = Claude Fable 5 z listą 10 grzechów Bielika, fallback Qwen — pierwszy audyt
złapał błąd Claude'a, nie Bielika; (5) S2 lektor od Sonneta ("Grzyb potrafi opanować
całą roślinę w kilka dni"). Commity: 7942981, 5606f6b + wiedza.
**000093:** opublikowana; ma "10x"/"3 dni"/"10 minut" w lektorach — ŚWIADOMIE zostawione.

## POST: SOWA Z MŁODYMI (15.07) ✔
Post tekstowy na stronę ROD (ID 122109501771379813): zachęta do wrzucania zdjęć sowy
z młodymi w komentarzach. Bez gatunku (ludzie zweryfikują sami). Pomysł na później:
post zbiorczy / rolka z najlepszych zdjęć mieszkańców. Skrypt z tokenem usunięty z /tmp.

## FABRYKA ŻARTÓW — FUNDAMENT (15.07 noc)
Decyzja Tomasza: Droga B, profesjonalnie — klipy wideo Veo 3.1 Fast (fal.ai), sklejka
u nas. Ceny zweryfikowane 15.07: Veo3.1 Fast $0.10/s bez audio (8s klip = $0.80),
NB Pro kadr $0.15 → żart 3 klipy ≈ $2.55. Moduł src/zarty.py DZIAŁA: Bielik pisze
scenariusz (Heniek+Halinka), checkpoint z wyceną, zero kosztów bez zatwierdzenia.
Żart #0001 na checkpoincie (ślimaki vs granulki Heńka) — dobra puenta, ALE Bielik
wsadził NAPISY do RUCHU mimo zakazu ("Eko-Ślimak", transparent "Wielka Wyżerka 2023")
— poprawić przed produkcją (transparent → ślimak z liściem jak trofeum).
NASTĘPNA SESJA: (1) produkcyjna połowa żartów: kadr referencyjny → fal Veo i2v →
edge-tts dialog 2 głosy → ffmpeg concat+napisy; (2) pierwszy żart TYLKO za wyraźną
zgodą Tomasza na $2.55; (3) karta Żarty w panelu; (4) rozważyć audyt Fable dla żartów.
STAN 000095: sprawdzić czy Tomasz kliknął OK (ostatnio aktywna:null — możliwe że
przeszła produkcję; zweryfikować /reels i ewentualnie przypomnieć o publikacji).

## FABRYKA ŻARTÓW — KOMPLET W APCE (15.07 rano) ✔
Panel: karta 06 "Fabryka żartów" (+ zakładka 🎭): nowy żart (Bielik), checkpoint
z wyceną $, Zapisz/Sprawdź(Fable)/PRODUKUJ(confirm ceny), log produkcji na żywo
(poll 5 s), lista z playerami /zarty/{id}/video, podgląd castingu.
APK v1.4: kafel 🎭 (solo karta 06) + NotifWorker powiadamia o gotowym żarcie
(kanał "zarty", klucz zart_ostatni). Backend: GET /zarty/{id}/log, POST
/zart-checkpoint/{id}/audytuj (Fable 5, 7 grzechów żartowych: napisy, format
DIALOG, cyfry, ≤7 s mowy/klip, jedna akcja/klip, puenta, życzliwość).
CASTING zatwierdzony przez Tomasza ("Zajebiście") — assets/zarty/postacie.jpg
NA ZAWSZE. Żart 0002 (odstraszacz ślimaków) na checkpoincie, wycena $2.40 —
CZEKA NA PIERWSZĄ PRODUKCJĘ (zgoda Tomasza przy przycisku PRODUKUJ).

## FABRYKA OBRAZÓW — REBRANDING + PRZEŁOM AUDIO (15.07 rano) ✔
Decyzja Tomasza: "Fabryka Rolek" → **FABRYKA OBRAZÓW** z działami: (1) Rolki ROD,
(2) Rolki ROD HUMOR. Zmienione: panel (tytuł+karty 01/02/06), health, APK v1.5
(nazwa, kafle). **STAŁY KEYSTORE** w repo (openssl p12, alias androiddebugkey) +
workflow kopiuje zamiast generować → OD 1.5 AKTUALIZACJE PO WIERZCHU (1.4→1.5
jeszcze wymaga odinstalowania!). Ryzyko: keystore w publicznym repo — świadomie
zaakceptowane (apka prywatna).
**ARCHITEKTURA HUMORU — PRZEŁOM:** Veo i2v blokuje obrazy z ludźmi (deepfake policy,
potwierdzone testami: bez ludzi przechodzi, z ludźmi nigdy; forum Google potwierdza).
Rozwiązanie z researchu viralowych twórców: **t2v z NATYWNYM AUDIO VEO** — kwestia
po polsku w cudzysłowie = lip-sync + głos z modelu. Zasady: JEDNA kwestia/klip,
<8 s, emocja+akcja+kwestia, opis postaci IDENTYCZNY w każdym prompcie, styl
realistyczny (nie kreskówka!), "No subtitles, no text overlay". Test #9999 ($1.20):
Mieczysław mówi "W przyrodzie nic się nie ukryje" — Whisper potwierdził idealną
polszczyznę, klatki: realizm, timing, uśmiech. CZEKA NA OCENĘ UCHA TOMASZA w apce.
Koszt żartu w nowej architekturze: 3 klipy × $1.20 = $3.60.
**BIZNES:** research monetyzacji — AdSense Shorts PL grosze (0,06-0,2 zł/1k);
pieniądze: brand deals (od 5k subów), afiliacja, reklamy szyte dla lokalnych firm
(800-1500 zł/odc przy koszcie $3.60). Plan "Mieczysław z działki" 3-torowy zapisany
w rozmowie. NASTĘPNE: po akceptacji #9999 → przebudowa zarty.py na format 1 kwestia/
klip + natywne audio; pilot serialu; kanały YT/TT.
KOSZTY dnia: diagnoza i2v ~$1.40 + żart 0002 $2.40 + test 9999 $1.20.

## Sesja 15.07.2026 (cd.) — PILOT #10001 "CUKINIE" ZAAKCEPTOWANY I OPUBLIKOWANY
**Wynik:** final.mp4 29 s (4 klipy cięte po puentach + plansza "MIECZYSŁAW Z DZIAŁKI / NOWA SERIA"). Koszt łączny **$8.40** (v1 4.80 + dogrywka K1 1.20 + dogrywka K1+K2 2.40). Link: /zarty/10001/video. Publikacja: **strona ROD Woźniki** (humor = bez grup), wideo wgrywa Tomasz ręcznie, opis dostał w czacie.
**Kanon serii:** Tomek w K2 wygląda jakby siedział na zewnątrz — przyjęta interpretacja: **uciekł przez okno przed cukiniami** (przypieczętowana w opisie posta). Nie regenerować.
**Stan kodu po sesji:** `zarty.py` — zasady 8–11 w szablonie (imię=kadr, logika między klipami, OBRAZ zaczyna się od miejsca, zakaz pukania/drzwi/gestów) + audytor 0a; `zarty_produkcja.py` — STYL_KLIPU odchudzony (bez opisu ogrodu). Wszystkie fixy przez stringowy replace z assertami.
**Iteracje (dla historii):** v1 — parser wsadził Tomka w drzwi (imię w OBRAZIE); v2 — pukanie halucynowane + K2 plener (wina STYL_KLIPU); v3/v4 — furtka, wołanie bez pukania, wnętrze żelazne. Szczegóły → wiedza/NAUKI.md.
**Następne kroki:** (1) żart #0002 na starej architekturze — skasować lub przeprodukować; (2) kolejne odcinki z banku tematów `data/zarty/tematy.json`; (3) decyzja o osobnej marce "Mieczysław z działki" odroczona — na razie wszystko na stronie ROD; (4) po publikacji zebrać zasięgi odcinka 1 przed produkcją odcinka 2.
