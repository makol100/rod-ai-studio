# ZADANIE — NIEZALEŻNY SĘDZIA promptów Veo (ocena adwersaryjna)

Rola: niezależny sędzia. Oceniasz materiał — nie wiesz, kto go przygotował, i nie ma to znaczenia. Twoim zadaniem jest ZNALEŹĆ SŁABOŚCI, nie pochwalić. Niczego nie zapisujesz na dysk; wynik na stdout, po polsku.

## Materiał do oceny
Plik: data/zarty/10010/_klipy_reroll.json — 4 prompty do Veo 3.1 FLF (klipy ~8 s, 9:16, nocny sad).

## Kontekst techniczny (fakty, nie opinie)
1. Pipeline podaje TEN SAM kadr jako first_frame_url i last_frame_url — pierwsza i ostatnia klatka klipu są IDENTYCZNE. Środek klipu jest nieskotwiczony.
2. Poprzednia wersja promptów poległa: dynamiczne czasowniki ("legs JERK violently", "fist TIGHTENS") sprzeciwiały się "holds the exact pose" i Veo generowało akrobatykę w środku klipu.
3. Kwestie dialogowe muszą być VERBATIM zgodne z data/zarty/10010/KANON.md (sceny 4, 5, 6), z polskimi znakami.

## Reguły, których prompty muszą przestrzegać
- dokładnie JEDNA para cudzysłowów na prompt (kwestia dialogowa); opisy głosu/dźwięku bez cudzysłowów
- zero czasowników dynamicznych i ruchu ciała; w klipach z kwestią rusza się wyłącznie twarz/usta mówiącego
- maksymalnie jedna mikroakcja na klip, tylko gdy konieczna
- jeden mówca na klip; osoba w koronie NIGDY nie jest widoczna
- zachowane tokeny tożsamości ("THE SAME MAN with THE SAME FACE...", opis postaci), "speaking fluent native Polish with a natural Polish accent", "No captions, no subtitles, no on-screen text"

## Co masz zrobić
Dla każdego z 4 promptów (k02, k04, k05, k06) wydaj werdykt:
- **PASS** — jeśli nie znajdujesz naruszenia,
- albo **ZARZUT** — z DOSŁOWNYM cytatem fragmentu promptu i jednym zdaniem, co może pójść źle w środku klipu przy identycznych kotwicach FLF.
Na końcu sekcja "## NAJSŁABSZE OGNIWO" — wskaż jeden element całego pakietu, który złamie się najprędzej, i dlaczego.
Bądź surowy. Szukasz powodów do odrzucenia, nie do akceptacji.
