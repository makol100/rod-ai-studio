# ZADANIE KONTROLNE DLA ZALOGI (Zenek + Henio) — ocena skilla /watch (bradautomates/claude-video)

Rozstrzygacie jedno: WPINAC czy NIE w fabryke, i w jakim trybie. Kazdy podpisany glos + uzasadnienie. Rozbieznosc zostaje widoczna. Decyduje Tomasz.

## KONTEKST FABRYKI (pelny — nie macie pamieci, wiec czytajcie)
rod-ai-studio generuje AI rolki wideo (prezenterka Izabela, seria "Wiadomosci Dzialkowe"), publikuje na Facebooku ROD Wozniki. Gotowe rolki lokalnie: data/reels/<id>/video/final_with_music.mp4, krotkie ~30-60s, z lektorem (audio AAC) + muzyka. Scenariusz kazdej rolki (tekst lektora, plan scen) JEST zapisany w repo/gicie przy produkcji.
PROBLEM: weryfikacja jakosci gotowej rolki. Zasada nadrzedna Tomasza (samokontrola): "nie kaz mi ogladac, daj wynik i decyzje" — Klaudek NIE moze prosic Tomasza o obejrzenie. Dzis Klaudek nie umie sam obejrzec rolki (widzi tylko pliki i logi, nie obraz/dzwiek).
Srodowisko wykonawcze: Claude Code na VPS. Skille zyja w /root/.claude/skills/ i odpalaja sie w Claude Code CLI (fabryka) — NIE w biezacej rozmowie Tomasza z Klaudkiem (tam rzadzi pamiec).

## CO OCENIAMY: skill /watch (claude-video, ~14200 gwiazdek, MIT)
Daje agentowi realne "obejrzenie" wideo: yt-dlp pobiera napisy/wideo -> ffmpeg wyciaga klatki (keyframes w trybie 'efficient', scene-change w 'balanced'/'token-burner') -> transkrypcja (napisy zrodla za darmo; Whisper API fallback GDY BRAK napisow: GROQ whisper-large-v3 tanszy albo OpenAI) -> agent Read'uje klatki jako obrazy JPEG + dostaje transkrypcje z timestampami -> odpowiada widzac klatki i slyszac audio.
Instalacja: Claude Code plugin (`/plugin marketplace add bradautomates/claude-video` + `/plugin install watch@claude-video`) albo `npx skills add bradautomates/claude-video -g` (instaluje do ~/.claude/skills, ~/.codex/skills).
Tryby --detail i koszt (z README, pomiar na 49min wideo): 
- transcript: 0 klatek, same napisy, ~4.5s, ~0 image tokenow (ale wymaga NAPISOW w zrodle).
- efficient: keyframes, ~0.5s, ~9.8k image tok.
- balanced: scene-change, ~21s, ~19.7k tok.
- token-burner: uncapped.
Budzet klatek auto: <=30s ~30 klatek, 30-60s ~40 klatek. Klatka 512px ≈ 197 image tokenow. Whisper audio ~480kB/min.

## TWARDE FAKTY ZE SRODOWISKA (zmierzone przez Klaudka 6.08)
- yt-dlp 2026.07.04: JEST na VPS. ffmpeg 8.0.1: JEST. python3, npx: JEST. => skill ruszy na klatkach OD RAZU, zero instalacji zaleznosci.
- Klucz Whisper (GROQ/OPENAI): BRAK nigdzie na VPS.
- Nasza rolka (data/reels/000098 final .mp4): strumienie h264 (video) + aac (audio), BEZ napisow osadzonych. => tryb 'transcript' (same napisy) NIE zadziala na naszych rolkach; transkrypcja audio wymaga Whispera (klucz+koszt) ALBO pomijamy transkrypcje i uzywamy scenariusza z gita (mamy go).

## PYTANIA ROZSTRZYGALNE (odpowiedz TAK/NIE + jak)
1. Czy /watch realnie rozwiazuje NASZ przypadek: Klaudek SAM oglada lokalna rolke 30-60s (klatki) i ocenia jakosc (czy lektor pasuje do obrazu, czy nie ma glitchy, czy trzyma sie scenariusza)?
2. Whisper: konieczny czy pomijalny? Skoro znamy tekst lektora ze scenariusza w gicie, czy wystarczy tryb 'efficient'/'balanced' (same klatki) + porownanie z tekstem z gita — bez placenia za Whisper i bez kolejnego sekretu na VPS?
3. Koszt na jedna rolke 30-60s w trybie 'efficient' (~40 klatek x ~197 tok ≈ 8k image tok, bez Whisper) — akceptowalny do RUTYNOWEJ weryfikacji kazdej rolki przed publikacja?
4. Integracja z przeplywem: weryfikacja przez /watch dziala w Claude Code CLI (fabryka), nie w rozmowie Tomasz<->Klaudek. Czy to pasuje (rolki i tak powstaja w fabryce/Claude Code), czy jest luka?
5. RYZYKA/BLOKERY: cokolwiek co moze ugryzc (np. token-burner wysadza kontekst, dedup, jakosc oceny z 40 klatek na 60s rolke, licencja, aktualizacje pluginu).
6. WERDYKT: wpinac czy nie. Jesli tak — ktory tryb (transcript odpada) i czy z Whisper czy bez.

Zasada 27.07: domyslnie najnizszy koszt; wyjatek tylko gdy droga pewna w 100%. Zasada 17.07: uczyc sie z cudzych bledow — jesli w repo/issues widac znane pulapki, wskazac.

## KOREKTA 6.08 (Tomasz: "Jest whisper")
Klucz Whisper JEST — w /root/rod-agent/.env (poza rod-ai-studio, dlatego pierwszy grep przeoczyl). ALE skill /watch szuka klucza w ~/.config/watch/.env albo env GROQ_API_KEY/OPENAI_API_KEY — integracja wymaga WSKAZANIA klucza skillowi (kopia lub eksport env), nie jest od razu widoczny.
Pytanie 2 stoi inaczej: skoro Whisper DOSTEPNY, czy uzywac go do transkrypcji audio rolki (pelny obraz: obraz+dzwiek), czy wystarczy scenariusz z gita + klatki (taniej, zero zaleznosci od API)? Rekomendujcie z uzasadnieniem.
