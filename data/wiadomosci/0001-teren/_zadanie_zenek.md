ZENEK — WIADOMOŚCI DZIAŁKOWE odc. 0001: zaprojektuj produkcję (odpowiadaj PO POLSKU, konkretnie).
WYDARZENIE: zagospodarowanie wspólnego terenu ROD przy domu działkowca (teren zarośnięty → karczowanie koparką przez 2 popołudnia do zmierzchu, 22-23.07).
MATERIAŁ (data/upload/0001-teren/, wszystko pion): 20260722_093926.mp4 71.5s 1920x824 rot-90 30fps (=824x1920 pion); 20260722_094249.mp4 36.5s j.w.; VID-20260723-WA0001.mp4 20.4s 1072x1920 29.58fps; WA0005 29.2s j.w.; WA0007 27.9s j.w. Chronologia creation_time: 22.07 09:39+09:42 rano, 23.07 17:07+19:41+19:44.
KANON (STANISLAW_CANON_1.0): serwis 60-90s pion 1080x1920: czołówka drawtext 3.2s ("WIADOMOŚCI DZIAŁKOWE" 88 + "ROD im. Józefa Lompy w Woźnikach" 50, DejaVu, crf18) → Stanisław intro "Dzień dobry państwu, kłaniam się nisko. Zapraszam na Wiadomości Działkowe." → wieści Z PRZEBITKAMI z materiału co 5-8s → outro "Do usłyszenia przy płocie." Awatar: Kling STANDARD $2.27 z karty karta_stanislaw_CANON.png (1072x1920 po generacji), prompt stały (calm presentation, eye contact). TTS: ElevenLabs Daniel (jak powitanie: eleven_multilingual_v2). Uwaga TTS: "ROD" pełnymi słowami.
ZADANIE:
1) Struktura montażu sekunda-po-sekundzie (ile s awatara na start, kiedy wchodzą przebitki, ile przebitek, chronologicznie 22.07→23.07, powrót do awatara na outro?). Załóż tekst Stanisława ~60-75s mowy.
2) Pipeline ffmpeg krok po kroku: normalizacja 5 źródeł do 1080x1920/30fps (skala+pad? crop?), wycinanie fragmentów (placeholdery czasów — wskazania wizualne da Genek), sklejka awatar+przebitki (overlay audio ciągłe spod awatara), czołówka, crf/preset.
3) KOSZTORYS: co płatne (Kling Standard $2.27? TTS znaki?), co $0. Limit generacji: 1 podejście.
4) Ryzyka i bramki przed submitem (checklist).
Wyjście: pełny plan do pliku data/wiadomosci/0001-teren/_zenek_plan.md (pisz przez cat/tee, masz dostęp do dysku).
