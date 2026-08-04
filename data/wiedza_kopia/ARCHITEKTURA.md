# ARCHITEKTURA — jak jest teraz

> **AKTUALIZACJA 04.08.2026** — decyzja Tomasza: *„Nadpisać, żeby wiedzieć, jak dążyliśmy do celu.
> To wszystko nasza wiedza."*
> Plik stał 20 dni bez zmian, choć rzeczywistość szła dalej. Rozbieżności wykrył **Henio**
> (4.08, raport w `.scratch/henio/`), cytatem z pliku przeciw stanowi dysku.
> **Stare zapisy NIE SĄ kasowane** — zostają jako ślad drogi, oznaczone `BYŁO`.
> Obowiązuje to, co po `JEST`.

## Infrastruktura
- VPS Hetzner 157.90.155.155 (22 GB RAM), kontener `fabryka-api` (FastAPI, venv: `./venv/bin/python`)
- Repo: github.com/makol100/rod-ai-studio (PUBLICZNE — sekrety tylko w docker-compose.yml, który jest w .gitignore)
- Adresy (Caddy, /root/claude-vps-mcp/Caddyfile):
  - panel: https://panel.157-90-155-155.sslip.io/panel (⚠️ /upload BEZ hasła — NIE publikować tego adresu)
  - barometr (publiczny, izolowany — przepuszcza TYLKO /barometr*): https://barometr.157-90-155-155.sslip.io/barometr
- Panel.html serwowany Z DYSKU przy każdym wejściu → zmiany frontu BEZ restartu kontenera
- Apka Android = natywny ekran kafli + WebView panelu; APK: GitHub Release `apk-latest` ORAZ GET /apk (Chrome Tomasza wiesza pobierania z GitHuba). Podpis v2 (pusty META-INF = NORMALNE)

## Modele
- **Bielik-11B v3 Q8_0** (Ollama, lokalny) — polski tekst: artykuł, sceny, lektor, prompty PL, opisy FB
- BYŁO (do 04.08.2026): **Qwen3:14b** — angielskie prompty obrazów (Droga #2) + zadanie NAPRAW; thinking ~12 GB
- **JEST:** w Ollamie stoi **`qwen2.5vl:7b`** (5692 MB). Modelu `qwen3:14b` NIE MA w systemie —
  sprawdzone `ollama list` / `curl localhost:11434/api/tags` (Henio, 4.08).
- OLLAMA_MAX_LOADED_MODELS=1 — Bielik i Qwen NIE mieszczą się razem; ładowanie sekwencyjne
- BYŁO (do 01.08): **Nano Banana Pro przez fal.ai** (`fal-ai/nano-banana-pro`, $0.15/obraz) — droga główna
- **JEST (od 01.08, decyzja Tomasza):** droga główna to **Genek, `gemini-3.1-flash-image`**
  (~0,067 USD/obraz). Fal.ai **tylko zapasowo, przy awarii Genka**. Kanon: `wiedza/GENEROWANIE_OBRAZU.md`.
  Słowa Tomasza: „Gienek nano banana 2" + „Fal.ai jako alternatywa w przypadku awarii Gienka".; FLUX.2 max w odwodzie
- **edge-tts pl-PL-MarekNeural** — lektor (11.6 znaków/s); działa TYLKO na VPS (proxy sandboxa Claude blokuje Microsoft)
- **Whisper** — napisy; autoryzowany bez pytania (znany tekst podstawiany, gdy liczba słów się zgadza)
- **Claude w panelu**: pomocnik poprawek = claude-sonnet-4-6; AUDYTOR checkpointu ("Sprawdź
  automatycznie") = claude-fable-5 z listą 10 grzechów Bielika (fallback: Qwen). Opisy FB
  na życzenie = claude-sonnet-4-6. Wszystko z klucza API Tomasza (env kontenera).

## Tryby językowe (POST /generate-reel, pole tryb_jezykowy)
- `"pl"` — ZWYKŁA rolka (stary szablon tematyczny)
- `"czysty"` — CZYSTA DROGA: Qwen pisze EN → obrazy → Bielik tłumaczy lektora na PL
- `"czysty_bielik"` — CZYSTA DROGA BIELIK: WSZYSTKO Bielikiem po polsku (artykuł, sceny, prompty). **DOMYŚLNY dla Claude — zawsze ten, chyba że Tomasz każe inaczej**

## Pipeline (czysty_bielik)
artykuł (Bielik) → sceny (PROMPT_TEMPLATE_CZYSTY: haczyk/mięso/pętla, akcja NA DZIAŁCE)
→ prompty obrazów PL (per scena, on_progress "prompt i/n") → **CHECKPOINT** (telegram,
czeka na zatwierdzenie — darmowe do tego miejsca) → obrazy fal.ai (PŁATNE) → audio
edge-tts → napisy Whisper → render (concat_parts_with_music: sceny + ducking muzyki
w JEDNYM ffmpeg; wynik: video/final_with_music.mp4)

## Struktura rolki (data/reels/NNNNNN/)
scenes.txt (SCENA N:/UJĘCIE:/LEKTOR:) · prompts.txt (PROMPT N:) · article.md ·
audio/01..NN.wav · images/01..NN.jpg · video/final_with_music.mp4 · status.json ·
tryb_jezykowy.txt · opublikowano.txt

## Kluczowe endpointy
/generate-reel · /aktywne-generowanie · /live-log · /reel-checkpoint/{id} (+/zapisz: zapis + przeliczanie promptów W TLE, flaga przeliczanie.lock, front polluje; +/zatwierdz wznawia; +/audytuj = Fable 5; +/popraw-przez-claude = Sonnet) · /reel-stop/{id} · /reels · /opis/{id}
(Bielik pisze opis FB) · /upload (filmy→filmy/, audio→assets/music/, reszta→budowa/)
· /film /rolka /apk /kontaktowka /klatki · /barometr /barometr.json /barometr/sygnal

## Baza tematów (data/content.db)
categories(id,nazwa,aktywna,tryb organizm/sprzet) · topics(category_id, tekst
"Nazwa (kontekst): opis wizualny ~220 zn", miesiace CSV, aktywny, uzyty_razy,
tryb_override). 20 kategorii, ~930 tematów. Losowanie: sezon (miesiace) + najrzadziej użyte.

## Powiadomienia
- Apka: NotifWorker co 15 min — gotowa rolka (tap→panel) + barometr ≥75 (1×/dobę)
- Telegram (bot w HA Dom): checkpoint (webhook fabryka_checkpoint_gotowy) + gotowa rolka
  (link https://panel...*/video) + barometr 8:00 (automation, sensor REST, próg 75)

## Barometr grzybiarza
apps/api/src/barometr.py — Open-Meteo (bez klucza), 4 lokalizacje (Woźniki, Lubliniec,
Koszęcin, Boronów), cache 3 h. Algorytm 0-100: opady 10d (→45) + deszcz 4-10 dni temu
(→15) + temp 5d (→40, optimum 12-19°C) − przymrozek (−20). Progi: 75/55/30.

## Fabryka Żartów (Droga B) — BYŁO „w budowie" (15.07). **JEST: DZIAŁA i produkuje.**
Odcinki 10004–10010 wyprodukowane; **10010 „Kiedy złapiesz złodzieja jabłek" OPUBLIKOWANY
i zamknięty** (04.08.2026, decyzja Tomasza). W `data/zarty/`: 7 katalogów odcinków + bank + tematy.
Moduł: BYŁO `src/zarty.py` — **JEST `apps/api/src/zarty.py`** (przeniesiony; stara ścieżka
NIE ISTNIEJE, sprawdzone 04.08.2026). Dane bez zmian: `data/zarty/NNNN/`. Pipeline docelowy: Bielik pisze żart
(KLIP/RUCH/DIALOG, bohaterowie: HENIEK + HALINKA przy płocie) → CHECKPOINT z wyceną $
→ kadr referencyjny NB Pro ($0.15) → klipy Veo 3.1 Fast image-to-video (fal.ai,
$0.10/s bez audio, 8s/klip, 9:16) → dialogi edge-tts (Marek+Zofia) → ffmpeg concat.
Żart 3×8s ≈ $2.55. Endpointy: POST /generate-zart, GET /zart-checkpoint/{id},
POST .../zapisz, GET /zarty. ZBUDOWANE: scenariusz+checkpoint+wycena.
DO ZBUDOWANIA: produkcja (kadr → Veo → audio → render) + karta w panelu.
Styl bohaterów: stała STYL_BOHATEROW w `apps/api/src/zarty.py` (ścieżka poprawiona 4.08).
