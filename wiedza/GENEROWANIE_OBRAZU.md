# GENEROWANIE OBRAZU — KANON DRÓG I CEN

Decyzja Tomasza 01.08.2026: **„Gienek nano banana 2"** + **„Fal.ai jako alternatywa w przypadku
awarii Gienka"**. Powód zmiany: Tomasz — „Na Was wydaje pieniądze, więc nie interesują mnie
generowania na próby". Genek generuje ~2x taniej niż fal.ai, więc próby przestają być luksusem.

## DROGA GŁÓWNA — GENEK (klucz Gemini, konto Tomasza)

**Model kanoniczny: `gemini-3.1-flash-image` (Nano Banana 2)** — ~0,067 USD za obraz 1K,
0,045–0,15 USD zależnie od rozdzielczości. Trzykrotnie taniej niż Nano Banana Pro.

Modele obrazowe potwierdzone na naszym kluczu (sprawdzone 01.08, lista z API):

| model | zastosowanie | cena za obraz |
|---|---|---|
| `imagen-4.0-fast-generate-001` | najtańsze, gdy jakość wystarczy | **0,02 USD** |
| `gemini-3.1-flash-image` | **KANON** — tekst + obraz w jednym modelu | ~0,067 USD |
| `gemini-3.1-flash-lite-image` | jeszcze taniej, niższa jakość | poniżej 0,067 USD |
| `gemini-3-pro-image` / `nano-banana-pro-preview` | najwyższa jakość, ostateczna wersja | 0,134 USD (2K), 0,24 USD (4K) |
| `imagen-4.0-generate-001` / `-ultra-` | dedykowany generator obrazu | 0,02–0,06 USD |
| `gemini-2.5-flash-image` | stary Nano Banana, **wycofanie 2.10.2026** | ~0,039 USD |

Wywołanie: `generateContent` (nie `predict`) dla rodziny `gemini-*-image`;
`predict` dla rodziny `imagen-*`.

**Tryb wsadowy (`batchGenerateContent`) daje 50% zniżki** — używać przy seriach niepilnych.

## DROGA ZAPASOWA — FAL.AI (tylko przy awarii Genka)

`fal-ai/nano-banana-pro` — ~0,15 USD za obraz. Saldo konta: 5,74 USD (01.08).
Używać, gdy: klucz Gemini zwraca 429/503, wyczerpany dobowy limit, albo Genek na L4.
NIE używać domyślnie — jest droższa i to osobne konto.

## CO NIE JEST SPRAWDZONE

- **ile z dobowego limitu Tier 1 (250 zapytań na model) zjadają obrazy** — nie zmierzone
- czy obrazy liczą się do tej samej puli co zapytania tekstowe
- Nano Banana Pro NIE jest dostępny w darmowym poziomie API (źródło: dokumentacja cenowa Google)

## POWIĄZANE

- Genek ma kolejkę modeli tekstowych: `gemini-3.1-pro-preview` → `gemini-3.6-flash`
  (dekret Tomasza „najwyższy WOLNY dla nas model"), patrz `tools/genek.py`
- Dobowy limit Tier 1 na `gemini-3.1-pro`: 250 zapytań, wyczerpany 30.07 o 17:50
- Ceny sprawdzone 01.08.2026 w sieci; **ceny się zmieniają — przy dużym wydatku sprawdzić ponownie**
