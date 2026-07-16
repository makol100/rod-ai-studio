# DROGA ROLKA HUMOR
Obowiązująca ścieżka produkcji rolek humorystycznych (seria "Mieczysław z działki").
Dostępna WYŁĄCZNIE w karcie panelu: Rolki ROD HUMOR. Dział rolek foto (Bielik) — nietykalny, osobne pliki.

## Zasada nadrzędna (Tomasz)
Decyzja zapada na NAJTAŃSZYM możliwym etapie. Parę centów na kadr eliminuje błędy warte dolarów.
Żaden wydatek bez wyraźnej zgody Tomasza. Limit twardy: 6 USD / odcinek (force = świadoma decyzja).

## Etapy
1. SCENARIUSZ + REŻYSERIA — Tomasz + Claude w czacie ($0). Bielik NIE pisze humoru.
2. AUDYT MASZYNOWY — /zapisz flaguje zakazane akcje (negacje, pukanie, chwyt w kadrze,
   dwie postacie, korona...). Blokada zatwierdzenia; force tylko świadomie.
3. KADRY KLUCZOWE ($0.03-0.08/obraz, nano-banana-pro) — pierwsza klatka każdej sceny jako OBRAZ.
   Tomasz akceptuje kadry ZANIM ruszy wideo. Scena z trzymaną pozą: kadr startowy = kadr końcowy.
   Darmowa alternatywa: czysta stopklatka z dobrego klipu (reference propagation).
4. ZWIAD RUCHU (Lite FLF 720p, ~$0.40/8s) — dla scen ryzykownych; ocena RUCHU (audio pomijalne).
   Plik zwiad_NN.mp4, nie nadpisuje klipów.
5. FINAŁ (fast first-last-frame 1080p + audio, $1.20/8s — ta sama cena co ślepe t2v) —
   klatka startowa i końcowa wymuszają pozę mechanicznie; uścisk nie może puścić.
6. MONTAŻ — cięcia po transkrypcji whisper; puenta kończy odcinek (koda tylko gdy puenta
   wymaga dopowiedzenia). Opis publikacyjny bez spoilera; interpretacja w przypiętym komentarzu.

## Rzemiosło promptów (z researchu rynku 02-06.2026)
- i2v/FLF: obraz dyktuje wygląd — prompt opisuje TYLKO ruch i dialog. Krótko, bez elaboratów.
- Poza trzymana (first==last): dopisz "holds the exact pose and grip from the frame for the
  entire clip, speaks through clenched teeth, no gesturing".
- Zero negacji w opisach obrazu. Pora dnia w kadrze. Ruch kamery świadomie (dolly-in na puentę).
- Karta postaci: assets/zarty/postacie.jpg (+ przyszłe turnaroundy 4 kąty nano-banana).
- Głos spoza kadru: MÓWI: IMIĘ (GŁOS). Wymiana zdań: MÓWI2/KWESTIA2. Bank: MÓWI: MIECZYSŁAW (BANK).

## Endpointy fal (ceny z 07.2026, weryfikować na fal.ai/pricing)
- fal-ai/veo3.1/fast/first-last-frame-to-video — $0.15/s z audio (1080p) = $1.20/8s
- fal-ai/veo3.1/lite/first-last-frame-to-video — $0.05/s 720p = $0.40/8s (zwiad)
- fal-ai/nano-banana-pro — kadry (grosze/obraz)
- safety_tolerance 1-6 (domyślnie 4) — poluzować przy fałszywych blokadach scen
