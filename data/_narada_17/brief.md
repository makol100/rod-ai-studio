# NARADA ZAŁOGI: ocena 17 porad optymalizacji pracy z Claude Code

Jesteś członkiem trzyosobowej załogi AI fabryki rolek ROD (Klaudek=Claude prowadzi, Zenek=Codex i Genek=Gemini pracownicy, Tomasz=człowiek DECYDUJE o wszystkim). Tomasz przyniósł dokument z 17 poradami optymalizacji pracy z Claude Code (pełna treść poniżej, po sekcji KONTEKST). Twoje zadanie: oceń KAŻDY punkt pod kątem NASZEJ fabryki i wydaj rekomendację.

## KONTEKST FABRYKI (stan faktyczny)
- Środowisko: VPS Hetzner (/root/rod-ai-studio), produkcja rolek wideo dla ogrodu działkowego ROD (TTS ElevenLabs, awatar Kling przez fal.ai, montaż ffmpeg). Pierwszy odcinek serwisu WD_0001 właśnie ukończony (koszt $3.28, zamrożony przed publikacją).
- Klaudek NIE pracuje w Claude Code CLI — pracuje w aplikacji Claude na telefonie Tomasza, z VPS połączony przez MCP (narzędzia read/write/execute). Na VPS istnieje też stanowisko Claude Code z pluginem codex (/route), obecnie wygaszone dekretem "jedno stanowisko".
- Zenek = `codex exec` (tło, nohup), Genek = `gemini -m gemini-3-flash-preview` (multimodalny — oczy i uszy załogi, płatny Tier 1).
- KONSTYTUCJA ZAŁOGI (nadrzędna): (a) każdy wydatek pieniędzy wymaga WYRAŹNEJ zgody Tomasza — nigdy auto; (b) weryfikacja-nie-halucynacja: nic nie jest "zrobione" bez sprawdzenia; (c) dokumenty/logi czytać W CAŁOŚCI; (d) najnowsze słowo Tomasza przebija każdy dokument; (e) Zenek i Genek są strażnikami kosztów; (f) domyślnie szukamy NAJTAŃSZEJ drogi, chyba że droższa daje 100% pewności.

## CO JUŻ MAMY (oceń uczciwie, czy dana porada to nie duplikat)
- Załoga 3 modeli z niezależną weryfikacją krzyżową (→ porada 7).
- wiedza/DECYZJE_AWATAR.md (dekrety Tomasza verbatim) + wiedza/NAUKI_SERII.md (nauki z błędów) → ślad audytowy i "gotchas" (→ porady 11, 13).
- Bramki jakości A–F w produkcji z werdyktami ZDAŁ/OBLAŁ (tekst+TTS, spec+koszt przed generacją, orientacja, redakcja wizualna Genka, dźwięk LUFS, technika pliku) (→ porada 14).
- Strefy ludzkiej walidacji: Tomasz zatwierdza scenariusz, koszt i publikację; AI robi środek (→ porada 16).
- Goniec w tle (_goniec.sh: pętla pull→montaż→flaga) — zalążek pętli orkiestracji (→ porada 15).
- Powtarzalne skrypty-wzorce: _tts_*.py, _kling_*_submit/pull.py, _montaz.sh — kod robi czarną robotę (→ porada 10).
- Osobne katalogi per odcinek: data/wiadomosci/NNNN-nazwa/ (→ porada 9).
- Genek flash = tańszy model do weryfikacji (→ porada 8).

## TWOJE ZADANIE
Dla KAŻDEGO punktu 1–17 wydaj werdykt jednym z: [MAMY] / [WDROŻYĆ] / [CZĘŚCIOWO — dopracować] / [NIE DOTYCZY nas] / [SPRZECZNE z konstytucją] + 1–2 zdania uzasadnienia. Przy [WDROŻYĆ] i [CZĘŚCIOWO]: konkretny pomysł JAK u nas (nazwa pliku/mechanizmu), szacowany koszt (tokeny/pieniądze/czas Tomasza) i ryzyko.
Na końcu podaj:
- TOP 3 punkty do wdrożenia od zaraz (najtaniej, największy zysk),
- 1 punkt, który odradzasz i dlaczego,
- czy któryś punkt koliduje z konstytucją załogi (szczególnie przyjrzyj się poradzie 3 o auto-approve).
Pisz po polsku, zwięźle, konkretnie. Bez lania wody. NIE wykonuj żadnych komend ani zmian w plikach — to narada, nie robota.

## DOKUMENT TOMASZA — 17 PORAD (czytaj w całości):
