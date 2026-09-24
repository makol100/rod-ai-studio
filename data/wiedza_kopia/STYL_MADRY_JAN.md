# STYL ROLEK „JAK MĄDRY JAN" — obowiązuje od 23.09.2026 (dekret Tomasza: „Wdrażamy 1–4 i 7")
Wzorzec: profil FB „Mądry Jan" (24 tys. obs., rolki 8–145 tys. odtworzeń) + YouTube (3,8 tys. sub., hity 91–93 tys.). Obserwacje: data/wzorce/madry_jan/OBSERWACJE_2309.md, research Henia /tmp/n_madryjan (D-0512/D-0513).

## REGUŁY WDROŻONE (każda rolka foto, Wiadomości, relacje)
1. **TYTUŁ = tani konkret + sekret + strata/zysk liczbą.** Wzory: „Czosnek jak pięść — wsyp TO do dołka w październiku", „Tabletka za 3 zł ratuje pomidory przed zarazą — 30 lat nikt mi nie mówił". Zakaz tytułów-etykiet („Sadzenie czosnku zimowego", „Porady na wrzesień").
2. **PIERWSZE 2 SEKUNDY = straszak albo obalenie**, nigdy zapowiedź („dziś opowiem…"). Scena 1 lektora zaczyna się od zdania typu „To nie jest rosa — to zaraza, która zje ogórki w tydzień" / „Większość robi to źle".
3. **NAPIS NA EKRANIE: duże białe litery w CZERWONYM prostokącie** (haczyk z tytułu w scenie 1, kluczowe liczby/słowa w kolejnych). Miniatura = ten sam napis na kadrze, bez ludzi. Styl napisów ASS: BorderStyle=3 (pudełko), BackColour czerwony, tekst biały, Bold, rozmiar duży.
4. **PRAWDZIWE UJĘCIA**: własne zdjęcia/filmy z ogrodu (DCIM Folda, relacje), Wikimedia Commons (zatwierdzone przez Tomasza — D-0477); AI tylko gdy nie ma zdjęcia. Zbliżenia rąk, roślin, ziemi.
7. **ZACZEP DO KOMENTARZY** w ostatniej scenie i w opisie FB: pytanie do widza („Kto jeszcze tak robi? Napiszcie…", „Ile zebraliście w tym roku?").

## NIE WDROŻONE (Tomasz nie wybrał): 5 (jeden temat = jedna rolka — i tak stosujemy), 6 (pilność w tytule — zalecane), 8 (obietnica rytmu w opisie strony).
## Kontrola: każdy scenariusz przed produkcją przechodzi test: tytuł wg reguły 1? scena 1 wg reguły 2? napis-haczyk wg 3? zdjęcia prawdziwe i zatwierdzone wg 4? pytanie na końcu wg 7?

## ZASADA (dekret 23.09.2026, D-0522): KAŻDY obraz NATYCHMIAST na Telegram do podglądu
Każdy wygenerowany obraz i każde zdjęcie do produkcji wysyłać Tomaszowi na Telegram **od razu po powstaniu, pojedynczo, na bieżąco** (z podpisem: co to, do której sceny) — żeby mógł zareagować, zanim wejdzie do montażu. Obowiązuje Klaudka i całą załogę. Narzędzie: `tools/tg_foto.py <plik> "<podpis>"`.

## 24.09.2026 — rolki dłuższe niż 90 s (zmierzone)
- Dokumentacja Meta Reels Publishing API podaje 3–90 s, ale rolka pH gleby (133,4 s, #000108) przeszła przez /{page}/video_reels jako Reel: Graph API status ready, publish_status published, length 133.366 → https://www.facebook.com/reel/2244824996307318
- Wymogi techniczne z dokumentacji Meta do pilnowania: 1080×1920, 24–60 fps, H.264, GOP 2–5 s (-g 60 przy 30 fps), audio AAC 48 kHz STEREO ≥128 kb/s (loudnorm podbija do 96 kHz mono → zawsze -ar 48000 -ac 2).
- Układ „pełny ekran" (dekret Tomasza 24.09, D-0586): bez slajdów/„kartek" u góry — zdjęcie na cały kadr z przesuwem, nagłówek części u góry, napisy narracji słowo w słowo na dole (czerwone pudełka).
