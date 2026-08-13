# Ocena skilla /watch — zadanie kontrolne

Rozstrzygnij: WPINAĆ czy NIE do fabryki rolek i w jakim trybie. Daj podpisany głos i odpowiedz TAK/NIE + jak na sześć punktów.

## Surowe fakty wejściowe od Tomasza

- Lokalne rolki 30–60 s, H.264 + AAC, bez osadzonych napisów; scenariusz lektora jest w repo.
- VPS ma yt-dlp 2026.07.04, ffmpeg 8.0.1, Python i npx.
- Klucz Whisper jest w `/root/rod-agent/.env`, ale `/watch` oczekuje `~/.config/watch/.env` albo zmiennej `GROQ_API_KEY`/`OPENAI_API_KEY`.
- Opisany mechanizm `/watch`: ffmpeg wyciąga klatki, agent czyta JPEG; transkrypcja z napisów lub Whisper. Tryby: transcript, efficient, balanced, token-burner.
- Dla 30–60 s opisany budżet efficient to około 40 klatek; transcript odpada bez napisów, o ile nie użyje się Whispera.

## Pytania

1. Czy rozwiązuje przypadek samodzielnej oceny obrazu, zgodności obrazu z lektorem, glitchy i scenariusza?
2. Whisper używać rutynowo czy pominąć na rzecz tekstu z repo? Uwzględnij, że scenariusz nie dowodzi faktycznie wyrenderowanego audio.
3. Czy efficient (~40 klatek / około 8k image-tokenów według opisu wejściowego) jest akceptowalny rutynowo?
4. Czy praca w Claude Code CLI pasuje do pipeline'u, czy zostawia lukę?
5. Ryzyka/blokery, szczególnie próbkowanie ruchu, deduplikacja, token-burner, sekrety, licencja i aktualizacje oraz znane upstream issues.
6. Werdykt: WPINAĆ/NIE; tryb; Whisper tak/nie; czy najpierw pilot.

Oddziel fakty wynikające z materiału od opinii. Nie zakładaj, że marketing README jest dowodem jakości. Jeśli nie zweryfikujesz upstream/issues, napisz NIE WIEM.
