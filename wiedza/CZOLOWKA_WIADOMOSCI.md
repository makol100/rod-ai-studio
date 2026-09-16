# CZOLOWKA WIADOMOSCI — KANON (wariant C, Belzebub)

**STATUS: OBOWIAZUJE. Zatwierdzona przez Tomasza 16.09.2026 („Super!!!").**
**DEKRET D-0350: doklejac do KAZDEGO wydania Wiadomosci z ogrodu, ZAWSZE.**

**PLIK:** `assets/intro_wiadomosci/INTRO_WIADOMOSCI_C_v1.mp4` · SHA-256 (24): `996b664b2887d444504c4f8c`
5,0 s · 1080x1920 · 30 fps · 150 klatek · z dzwiekiem · koszt 0 USD

## PRZEBIEG (spec Belzebuba, D-0349)
| czas | co widac |
|---|---|
| 0,0–0,8 s | tlo krem #fffdf6, logo ROD na srodku, skala 0,92→1,0 |
| 0,8–2,4 s | tytul dwuliniowy WIADOMOSCI / Z OGRODU, Fraunces 96 px, #1f5a37 |
| 2,4–3,8 s | podtytul „ROD im. Jozefa Lompy w Wozniakach" 34 px + zloty pasek #e5b744 wyjezdza do 360 px |
| 3,8–4,6 s | pasek rozszerza sie do 520 px i przygasa do 80% |
| 4,6–5,0 s | zamrozenie, twarde ciecie na wydanie |

## JAK DOKLEJAC (obowiazkowo kazde wydanie)
`python3 tools/dolacz_intro.py WYDANIE.mp4` — filter_complex concat z pelna
normalizacja (NIE concat-demuxer!), bramka klatek + kadr z konca. Test bojowy
16.09 na pierwszy_dzien_v3: 2389 = 150 + 2239 klatek, przejscie czyste.

## JAK POWSTALA (do odtworzenia)
- Scena: `assets/intro_wiadomosci/intro.html` — deterministyczne `ustawKlatke(t)`
- Render: `tools/render_intro_wiadomosci.py` (playwright headless 150 klatek + ffmpeg)
- Dzwiek: Mixkit sfx 1145 „Musical news presentation intro" (7,3 s → atrim 5 s,
  afade out 0,8 s, loudnorm). Licencja Mixkit SFX: komercyjnie, social media,
  BEZ atrybucji (potwierdzona 16.09). Zapasy: sfx 3089, 1151 w assets/audio/kandydaci/
- 30 fps (nie 24 ze spec) — spojnosc montazowa z rolkami; zaakceptowane w v1

---

# ARCHIWUM — STARA CZOLOWKA (WYCOFANA 16.09.2026, Tomasz: „Stara chujowa!")

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
