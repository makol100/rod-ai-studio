# POMIAR KASKADY WD_0001 v1→v6 (29.07.2026) — przyrząd, nie opowieść

Metoda: ffprobe (kontener) + ffmpeg psnr klatka po klatce (1736 klatek na porównanie). Zero ocen modelu.

## Kontener — wszystkie sześć wersji IDENTYCZNE
1080×1920, 30/1 fps, 57.866667 s, brak rotacji w metadanych. Różnią się wyłącznie rozmiarem pliku
(v1 149M, v2 112M, v3 118M, v4 129M, v5 122M, v6 152M).

## Gdzie v6 różni się od v1 (psnr < 45 = realna zmiana obrazu)
- 21.00–28.23 s (7.27 s), najsilniejsza różnica psnr 12.2
- 28.90 s (pojedyncza klatka)
- 31.63–38.97 s (7.37 s), psnr 12.3
RAZEM 14.67 s z 57.87 s = **25.3 % materiału**

## Gdzie v6 różni się od v5
- 9.00–20.97 s (12.00 s), psnr 10.3 — realna podmiana obrazu
- 23.27–23.73 s i 25.93–26.97 s, psnr ~43 — poziom szumu kodeka, nie zmiana treści
RAZEM 13.57 s = 23.4 %

## WNIOSKI Z POMIARU (bez interpretacji tego, co widać)
1. 74.7 % materiału v6 jest identyczne z v1 co do klatki — sześć renderów zmieniło jedną czwartą filmu.
2. Okno 39–45 s (przebitka p6 wg manifestu) jest w v6 IDENTYCZNE Z v1. Jeśli p6 była w v1 jedną z leżących,
   to poprawka z v3 została po drodze odrzucona i wróciła wersja wyjściowa. **Do rozstrzygnięcia okiem — pomiar
   mówi tylko, że nic tam nie zmieniono.**
3. Do oceny v6 wystarczy obejrzeć DWA okna: 21–28 s i 32–39 s. Reszta to materiał, który Tomasz już widział w v1.
4. Pomiar potwierdza skład v6 podany w manifeście (p1/p2/p6 z v1, zmienione p3/p4/p5) — manifest w tym punkcie był prawdziwy.

## CZEGO POMIAR NIE MÓWI
Nie mówi, czy obraz w tych oknach jest poprawny. Orientacji zdjęcia nie da się zmierzyć psnr-em — to wymaga oka.
