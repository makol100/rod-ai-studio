# Głos Zenka — Remotion

## POTWIERDZONE

Obecny renderer robi w ffmpeg:
- dopasowanie 1080x1920, crop, 30 fps i H.264 (`renderer.py:40-50`);
- Ken Burns 6% i napisy ASS (`renderer.py:223-259`);
- animowane intro/outro: maska kołowa, połysk, overlay, zoom i fade (`renderer.py:291-347`);
- sklejanie scen oraz normalizację audio (`renderer.py:54-73`);
- pętlę muzyki, sidechain ducking i miks z narracją w jednym przebiegu (`renderer.py:76-138`).

`pipeline.py` nie tworzy grafiki ruchomej: po TTS, obrazach i Whisperze wywołuje
`render_video(folder)` (`pipeline.py:140-259`; analogicznie `pipeline.py:343-425`).

Remotion daje przede wszystkim inną warstwę autorską: każda klatka jest wynikiem komponentu React,
a właściwości HTML/CSS można zmieniać według numeru klatki; ma też `interpolate()` i `spring()`.
Wynik renderuje przez przeglądarkę do klatek, a kodowanie wykonuje z użyciem ffmpeg.
To upraszcza pisanie odcinkowych animacji tekstu, kart, wykresów, ikon i układów responsywnych
oraz ich podgląd/iterację. Nie znalazłem efektu obrazu, który byłby zasadniczo niemożliwy w ffmpeg;
zysk dotyczy ergonomii i ekosystemu webowego, nie nowej klasy pikseli.

Wejście:
- VPS już ma Node v22.23.1 i npm 10.9.8; nie ma Chromium/Chrome w PATH.
- Remotion potrzebuje przeglądarki; renderer wykrywa ją albo pobiera własną, domyślnie Chrome
  Headless Shell. Nadal używa ffmpeg.
- domyślna współbieżność to połowa wątków CPU, czyli na tym VPS domyślnie 6; można ją ograniczyć;
- renderer ma cache mediów domyślnie równy połowie dostępnej pamięci, a wyłączenie równoległego
  kodowania zmniejsza użycie RAM kosztem czasu.
- VPS ma 12 CPU, 22 GiB RAM, w chwili pomiaru 14 GiB available, 1.5 GiB free i zero swap.

## HIPOTEZY

Na współdzielonym VPS pierwsza próba powinna mieć concurrency 1-2 i jawnie ograniczone cache,
bo ustawienia domyślne konkurują z Ollamą. Integracja oznacza drugi stos (React/TypeScript/npm/
browser) obok Pythona i ffmpeg, a nie zastąpienie ffmpeg.

Tańsza droga: pozostać przy obecnym rendererze i dodać generator SVG/PNG w Pythonie (Pillow jest
już używany w repo), a animować go dostępnymi filtrami ffmpeg (`overlay`, `drawtext`, `xfade`,
`zoompan`, `geq`). Dla plansz, napisów i prostych wykresów daje ten sam efekt końcowy bez browsera
i nowego runtime'u. Remotion ma sens dopiero, gdy konkretny odcinek wymaga wielu niezależnych
elementów animowanych w czasie i koszt napisania filtergraphu przewyższa koszt drugiego stosu.

## NIE WIEM

Nie wiem, ile RAM zużyje nasza rolka 1080x1920, ponieważ nie wykonano renderu porównawczego Remotion
na naszym materiale, a dokumentacja nie podaje jednej stałej wartości. Nie wiem też, jaki dokładnie
wariant licencji obejmuje tę fabrykę bez rozstrzygnięcia, ilu ludzi prawnie tworzy z Remotion i czy
pipeline kwalifikuje się jako „automation”.

## WERDYKT

**ODPUSCIC** — obecne potrzeby pokrywa już ffmpeg, a Remotion poprawiłby głównie wygodę tworzenia
złożonej grafiki ruchomej kosztem browsera, RAM-u i drugiego stosu, bez wskazanego dziś odcinka,
który tego wymaga.

— Zenek
