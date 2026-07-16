# DROGA ROLKA HUMOR 2.0
Obowiązuje od 16.07.2026. Zastępuje v1 (ARCHIWUM_DROGA_HUMOR_v1.md — zawiodła:
MÓWI2 w jednym klipie, kadry z samego tekstu, (GŁOS) dla postaci, zero kontroli wyjścia).
Dział rolek foto (Bielik) — nietykalny, osobne pliki.

## Zasady nadrzędne (przetrwały z v1 — to nie one zawiodły)
- Decyzja zapada na NAJTAŃSZYM możliwym etapie.
- Żaden wydatek bez wyraźnej zgody Tomasza. Limit twardy: 6 USD / odcinek (force = świadoma decyzja).
- WERYFIKACJA, NIE HALUCYNACJA: nic nie jest zrobione, dopóki nie wykonane i sprawdzone.
- Finalne pliki ocenia się natywnie (upload Tomasza do czatu); moja samokontrola: most git
  (tmp_weryfikacja/ → raw.githubusercontent) + strażnik.

## KRĘGOSŁUP: nic nie idzie dalej bez przejścia bramki poprzedniego etapu.

### Etap 0 — KANON
Scenariusz w gicie = jedyne źródło prawdy. Każda praca nad odcinkiem zaczyna się od
odczytu kanonu (git + pamięć /areas/). Zmiana kanonu = commit, nie "ustalenie w locie".

### Etap 1 — KARTY POSTACI (fundament, PRZED scenami)
Każda postać występująca w odcinku MUSI mieć kartę: arkusz front + 3/4 + profil
(assets/zarty/karty/IMIE_karta.jpg), zbudowany nano-banana-edit ze zaakceptowanej
stopklatki/kadru. Bez karty postać nie wchodzi do sceny.
Karta = referencja nr 1 w KAŻDEJ generacji z tą postacią.
BRAMKA: akceptacja karty przez Tomasza (raz na postać, potem reużywalna).

### Etap 2 — SCENARIUSZ + AUDYT
Tomasz + Claude w czacie ($0). Bielik NIE pisze humoru.
Audyt maszynowy scenariusza — twarde reguły (z researchu i krwi 16.07):
- JEDEN mówca na klip (skuteczność lip-sync 80% vs 40% przy dwóch). Wymiana zdań = cięcie na klipy.
- Kwestia 3-6 s, jedno zdanie na oddech; mówca ma widoczne usta (plan średni/zbliżenie).
- Postać mówiąca puentę jest WIDOCZNA na ekranie. (GŁOS) tylko dla narracji spoza sceny.
- Zero negacji w opisach obrazu; pora dnia zapisana w scenie.
BRAMKA: /zapisz bez flag albo świadomy force.

### Etap 3 — KADRY Z REFERENCJAMI (nano-banana-pro/edit)
Kadr pierwszej (i końcowej) klatki każdej sceny generowany WYŁĄCZNIE z referencjami:
- image_urls: [baza sceny (stopklatka/kadr), karta postaci, wzorzec ubioru...] — 2-4 obrazy,
  jedna rola na obraz, najważniejsze w pierwszych slotach; skonfliktowane referencje = model uśrednia.
- Prompt z jawnym identity-lockiem ("te same oczy, nos, linia szczęki, to samo ubranie co obraz N").
- Parametry ZAWSZE: aspect_ratio="9:16", resolution="2K" (ta sama cena co 1K), safety_tolerance wg sceny.
BRAMKA A (automat): straznik.py na kadrach — tożsamość vs karty (cosine ≥0.35) + sędzia VLM
(ubiór/liczba osób/tekst). FAIL → poprawka, Tomasz tego nie ogląda.
BRAMKA B (człowiek): akceptacja kadrów przez Tomasza ZANIM ruszy wideo.

### Etap 4 — GENERACJE FLF
fal-ai/veo3.1 FLF (lite $0.40/8s zwiad ruchu; fast $1.20/8s finał 1080p+audio), submit+poll
(gen3/pull3), nigdy fal_client.run dla wideo.
Prompt = TYLKO ruch + dialog (obraz dyktuje wygląd): identyfikator wizualny mówcy
("mężczyzna w czerwonej czapce mówi po polsku: ..."), emocja/tempo, "no captions, no subtitles".
Poza trzymana: first==last + "holds the exact pose and grip for the entire clip".

### Etap 5 — STRAŻNIK (automat, po KAŻDEJ generacji)
tools/straznik.py: techniczny / OCR napisów-widmo / scenariusz (whisper vs kwestia) /
kotwice FLF (MAD start<10, koniec<25) / tożsamość (insightface vs karty) /
usta (syncnet: FAIL<3.0, WARN 3-5, PASS≥5; przy 2 twarzach conf per twarz wskazuje mówcę) /
sędzia VLM (qwen2.5vl przez 172.17.0.1:11434).
FAIL → klip wraca do poprawki. Do Tomasza trafiają wyłącznie PASS/WARN z raportem.

### Etap 6 — MONTAŻ + AKCEPTACJA + PUBLIKACJA
Cięcia po transkrypcji whisper; napisy własne ASS (KOLORY_ASS); puenta kończy odcinek.
Strażnik na finale z flagą tekst-dozwolony (napisy wypalone są legalne).
BRAMKA: upload finału przez Tomasza do czatu → werdykt → 📣 checkpoint publikuj
(guard stan='gotowy' → n8n → FB). Opis bez spoilera; interpretacja w przypiętym komentarzu.

## Narzędzia i stałe
- tools/straznik.py (bramki automatyczne), tmp_weryfikacja/ (most git — sprzątać po sesji),
  gen3.py/pull3.py (submit+poll), sluch.py (whisper).
- Karty: assets/zarty/karty/. Stare postacie.jpg = materiał źródłowy do kart.
- Endpointy/ceny weryfikować na fal.ai/pricing przy każdej sesji z wydatkami.
- Głos banku: Mieczysław = ElevenLabs Brian + LatentSync (bez zmian z v1).
