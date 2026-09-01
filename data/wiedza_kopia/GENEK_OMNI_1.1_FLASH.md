# Gemini Omni 1.1 Flash — fakty z dokumentacji Google (sprawdzone 01.09.2026 przez Klaudka; Genek NIE ODDAL wiarygodnego glosu — tryb awaryjny halucynowal blog z 2024)
Zrodla: ai.google.dev/gemini-api/docs/changelog (wpis 27.08.2026), ai.google.dev/gemini-api/docs/omni (aktualizacja 30.08.2026), ai.google.dev/gemini-api/docs/pricing (odczyt 01.09).
## Co to jest
- gemini-omni-1.1-flash GA od 27.08.2026 (preview gemini-omni-flash-preview wylaczany 30.09.2026). Konwersacyjny model generowania I EDYCJI wideo przez Interactions API (client.interactions.create, previous_interaction_id = edycja/rozszerzanie bez ponownego uploadu).
- DOSTEP: nasz klucz Gemini WIDZI gemini-omni-1.1-flash, gemini-omni-flash-preview, veo-3.1-generate/fast/lite-generate-preview (lista modeli 01.09, 52 modele).
- CENA: $17,50/1M tokenow wideo, 5 792 tok/s 720p → ~$0,10/s (klamra 12,9 s ≈ $1,29; 60 s ≈ $6,0). Wejscie $1,50/1M (referencje — grosze). Dla porownania: Veo 3.1 Lite przez Gemini API $0,05/s 720p ($0,40 za klip 8 s vs $0,64 na fal.ai), Veo 3.1 Fast $0,10/s, Standard $0,40/s; Kling Std $0,0562/s, Pro $0,115/s.
## Umiejetnosci (doc)
- text→video, image→video, first+last frame, subject reference (<IMAGE_REF_N>, wiele obrazow), VIDEO reference (<VIDEO_REF_N>: "work best with likenesses", max 3 klipy po 3 s, audio w referencji ignorowane), tagi [# Sources ...] [# References ...].
- Klipy 3-10 s; extend po 10 s do 40 s lacznie (multi-turn z mowa: TAK). 9:16/16:9. 360p/720p natywnie, 1080p/4K upscaling. Timecode w promptach ([0-3s] ...). Tekst w kadrze renderowany poprawnie. SynthID w kazdym pliku.
- Domyslnie robi kilka ujec — dla jednej sceny prompt "single continuous shot, no scene cuts".
## OGRANICZENIA (doc, dosłownie)
- "Uploading audio references is unsupported" → NIE mozna podac wlasnego audio (klon glosu ElevenLabs) → brak lip-sync do naszego audio.
- "Voice editing is not supported".
- "English fully supported, other languages have not been evaluated" → polski dialog NIEZWERYFIKOWANY przez Google; wymaga kanarka.
- EOG (VPS Niemcy, Tomasz Austria): edycja/rozszerzanie WGRANYCH wideo niedostepne; obrazy z nieletnimi niedostepne; "certain recognizable people" niedostepne.
- Nie mozna dogenerowac dialogu do wgranego wideo z mowiaca osoba. Wgrane wideo max 10 s. Brak system instructions/temperature/negative prompt (negacje w prompcie). YouTube jako zrodlo nie.
## WERDYKT 01.09
- Awatar Tomasza z jego glosem: NIE (brak audio-input). Werdykt HYBRYDA (D-0190) bez zmian.
- Potencjal dla fabryki: humor (spójna postac z referencji, 40 s w jednym watku, poprawki slowem) i klamra Izabeli — WARUNEK: kanarek polskiego dialogu + Tomasz zatwierdza koszt testu (~$1 za 10 s).
