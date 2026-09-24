# MOŻLIWOŚCI ZAŁOGI — kto co umie i ile to kosztuje (24.09.2026, dekret: „Takie coś masz wiedzieć sam… zapytać się pracowników to żaden problem")
**PRZED KAŻDYM PŁATNYM KROKIEM: przeczytaj tę tabelę i zapytaj załogę „kto zrobi to za darmo/taniej". Płatna droga tylko gdy darmowej nie ma albo zawiodła.**

| Zadanie | Za darmo (najpierw) | Płatnie (dopiero potem) |
|---|---|---|
| Obraz AI (generacja) | **ZENEK** — Codex `image_generation`, abonament ChatGPT Plus; **GENEK** `gemini-3.1-flash-image` (limit darmowy AI Studio = 0 zł) | Genek `gemini-3.1-flash-image` poza limitem 0,067 USD (test 24.09 OK); fal.ai 0,15 USD (awaria) |
| Szukanie zdjęć (prawdziwe) | Genek szuka + oko Genka (tools/genek_szuka.py, oko_genka.py) — Wikimedia Commons | — |
| Ocena zdjęcia / wideo (oko) | oko Genka (Gemini flash, ułamki centa); qwen2.5vl lokalnie NIE nadaje się do gatunków/scen | — |
| Tekst polski / scenariusz | Bielik (lokalnie), Henio (DeepSeek, własne saldo), Genek | — |
| Research, źródła | Henio (szukaj_net), Genek (Google) | — |
| Lektor | edge-tts Marek, klon V2 głosu Tomasza (lokalnie); **GENEK** `gemini-3.8-flash-tts` (limit darmowy AI Studio = 0 zł) | Genek `gemini-3.8-flash-tts` (~0,84 USD/1h audio); Omni/ElevenLabs — tylko za zgodą |
| Wideo z ruchem | Ken Burns/ffmpeg (0 zł); **GENEK** `veo-3.1-generate-preview` (limit darmowy AI Studio = 0 zł, test 24.09 OK) | Genek `veo-3.1-generate-preview` (od ~0,64 USD za 8s Lite do ~3,20 USD za 8s Standard); fal/Kling/Omni — tylko za zgodą |
| Montaż, napisy | ffmpeg, whisper lokalnie | — |
| Henio, Belzebub | NIE generują obrazów | |
| Serwer | brak GPU — lokalna generacja obrazów niepraktyczna | |

## WIDEO ZA DARMO — research ZENKA 24.09.2026 (Codex + web, źródła w decyzji D-0555)
| Droga | Za darmo | Automat z VPS |
|---|---|---|
| **Google Flow** (labs.google/flow) | 50 kredytów/dzień ≈ **5 klipów Veo 3.1 Lite 4–8 s**, 9:16 | nie (brak API) — ew. przez telefon/przeglądarkę Tomasza |
| **Kling** (klingai.com) | 66 kredytów/dzień ≈ 6 podstawowych filmów | nie (UI) |
| Runway | 125 kredytów jednorazowo | nie |
| Gemini API Veo 3.1 Lite (Genek) | brak darmowego; **0,05 USD/s** (8 s = 0,40 USD) | **tak** |
| Sora | wg Zenka wyłączona (app/WWW 26.04.2026, API 24.09.2026) | — |
| CPU lokalnie | niepraktyczne (~12 min na 9 klatek 256 px) | — |
Rekomendacja Zenka: Flow ręcznie (5/dzień za darmo), automat = Veo Lite API.
