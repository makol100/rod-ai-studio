# CZOLOWKA WIADOMOSCI DZIALKOWYCH — KANON

**Zatwierdzona przez Tomasza 4.08.2026 20:2x.**

**PLIK:** `assets/izabela/CZOLOWKA_CANON.mp4` · SHA-256 (24): `a3edf964096f7d42c9d6a8c6`
6,0 s · 1080x1920 · 30 fps · 180 klatek · z dzwiekiem

## JAK POWSTALA — do odtworzenia

| element | narzedzie | koszt |
|---|---|---|
| obraz | `tools/czolowka.py` (PIL + ffmpeg) | **0 zl** |
| dzwiek | Freesound id=827121 „Minimalist news transition", 4,6 s | **0 zl** |
| zlozenie | ffmpeg, `apad` do 6 s | 0 zl |

**CALA CZOLOWKA KOSZTOWALA ZERO.**

## PRZEBIEG (6 s)

| czas | co widac |
|---|---|
| 0,0–0,9 s | swiatla studia wychodza z czerni |
| 0,9–1,9 s | logo ROD w kole (prawy gorny rog) + etykieta „PREZENTERKA AI" |
| 1,9–3,4 s | zlota linia rozsuwa sie od srodka, wchodzi **WIADOMOSCI DZIALKOWE** + podtytul **ROD im. Jozefa Lompy w Wozniakach** |
| 4,4–6,0 s | plynne przejscie do Izabeli w studiu |

Dzwiek gra od 0,0 i wygasa na 4,6 s — **cichnie dokladnie tam, gdzie wchodzi Izabela**,
wiec jej glos wchodzi w cisze, nie w muzyke.

## LICENCJA DZWIEKU — WAZNE

**CC0, domena publiczna. ZERO atrybucji.** Nie trzeba podawac autora pod postem.
To byl warunek Tomasza po sprawdzeniu, ze nasza wlasna muzyka (Kevin MacLeod, katalog
`music_atrybucja`) wymaga podawania nazwiska.
Klucz do Freesound zalozyl Tomasz 4.08 (zapisany w `/root/.gemini/.env`).

## CO ODRZUCONE PO DRODZE

1. **Wlasny sygnal z czystych tonow** (`tools/sygnal_wiadomosci.py`, dwie wersje).
   Tomasz: *„Mocarty kurwa"*, potem *„Tragedia"*. **Bledna podpowiedz Klaudka** — z sinusow
   liczonych kodem nie da sie zrobic muzyki, zawsze zabrzmi jak sygnal w windzie.
   Skrypt zostaje na dysku, ale NIE jest kanonem.
2. **Muzyka z naszych rolek** — sprawdzone: intro rolek jest NIEME (glosnosc 0),
   a biblioteka to Kevin MacLeod + katalog `music_atrybucja` = wymaga podania autora.
3. **Zrodla niedostepne:** Pixabay blokuje serwer (403), FreePD ZAMKNIETY, Musopen 403.
4. **PULAPKA:** w Archive.org lezy „Sintonia Telediario 1983-1985" oznaczona jako domena
   publiczna — to sygnal hiszpanskich wiadomosci TV, **cudza wlasnosc**. Nie tykac.

## GLOSY ZALOGI

Wszyscy trzej (Zenek, Henio, Genek) byli ZA czolowka i wszyscy wskazali, ze da sie ja zrobic
kodem za zero. Tytul „WIADOMOSCI DZIALKOWE" — zgodnie u wszystkich trzech.
Dlugosc: Genek 5 s, Zenek 6 s, Henio 7 s — **Tomasz wybral 6**.
Zastrzezenie Zenka (przyjete): czolowka ma rozgrywac sie NA kanonicznym studiu,
zeby wygladala na otwarcie serwisu, a nie doklejke z przodu.
Pelne glosy: `data/wiadomosci/0000-premiera/czolowka/`
