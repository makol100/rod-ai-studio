# NARADA 03.09.2026 — strona WWW ROD Wozniki (glosy doslownie)


## ZENEK
Zbudowane i nieopublikowane. Gotowy szkielet znajduje się w [www_rod](/root/rod-ai-studio/www_rod/README.md).

## POTWIERDZONE

1. Powstała statyczna strona bez frameworków:

   - treści: JSON i Markdown,
   - generator: [build.py](/root/rod-ai-studio/www_rod/build.py),
   - jasny/ciemny motyw,
   - responsywna nawigacja,
   - mapa z pinezką `[DO POTWIERDZENIA]`,
   - SEO, Open Graph, sitemap, robots i własne 404.

2. `dist/` zawiera 9 stron HTML, 2 pliki SEO i 5 zasobów statycznych. Łączny rozmiar: 969 975 bajtów. Użyto prawdziwego logo, mapy i zdjęcia elektryfikacji. Koszt: 0 zł.

3. Ogłoszenia są w `content/announcements.json`. Docelowa integracja Hansa:

   1. `/ogloszenie Tytuł | Treść | data-do`
   2. walidacja,
   3. podgląd,
   4. `PUBLIKUJ <kod>`,
   5. build, testy i atomowe wdrożenie.

4. Kandydat [Caddyfile](/root/rod-ai-studio/www_rod/Caddyfile) obsługuje domenę główną, przekierowanie `www`, ścisłe nagłówki bezpieczeństwa oraz proxy `/api/barometr.json`. Kamery pozostają osobną strefą za hasłem.

5. Wyniki kontroli:

   - źródła JSON/Markdown: `OK`,
   - build: 11 plików stron/SEO,
   - testy: 5/5 `OK`,
   - JavaScript: kod wyjścia 0,
   - Caddy 2.11.4: `Valid configuration`,
   - HTTP: 200 dla 10 sprawdzonych ścieżek, 404 dla nieistniejącej,
   - bramka źródeł: `PRZEPUSCIC`.

Pełny podpisany głos: [zenek.txt](/tmp/n_strona_rod/zenek.txt).

## HIPOTEZY

1. Najlepsza v1 to autentyczny ROD: duże logo, ciepła oprawa CSS, prawdziwe materiały, Barometr, kamery i ogłoszenia Hansa. Grafiki generowane nie są potrzebne na start.

2. Kolejność strony: hero → ogłoszenie → Barometr/kamery/Hans → prąd w 5 krokach → mapa → patron → kontakt.

3. Plan wdrożenia od otrzymania brakujących danych:

   - 0:00–0:30 — uzupełnienie treści,
   - 0:30–1:00 — kontrola telefonu i RODO,
   - 1:00–1:30 — DNS oraz Caddy,
   - 1:30–2:00 — testy HTTPS i integracji,
   - 2:00–2:30 — Lighthouse i poprawki.

## NIE WIEM

1. Wynik Lighthouse — środowisko nie ma Chromium, a domena główna jeszcze nie działa.
2. Prawidłowe położenie pinezki na mapie.
3. Publiczny telefon, e-mail, godziny zarządu i dane administratora RODO.
4. Jakie lokalne dokumenty oraz opłaty mają być publiczne.

Tomasz: podaj dane kontaktowe i RODO, wskaż pinezkę oraz wybierz tryb Hansa — `PODGLĄD + PUBLIKUJ` albo publikacja natychmiastowa.

— Zenek


## GENEK
[GENEK — DROGA 1: wlasny dostep do dysku przez CLI]

I have successfully provided my answer as Genek and saved it to the required file.

The process completed was:
1. I checked the current date and time (`Thu Sep  3 09:20:35 AM UTC 2026`).
2. I inspected the logo (`assets/branding/rod_profilowe.png`) via a Python script (Pillow) to extract the dominant color: `#183a26`.
3. I checked the directory `data/rolka-prad/do-rolki/` to view the available real images from electrification.
4. I formatted the answer according to the team's rules (no preamble, numbered steps, one actionable task at the end, signed) and addressing Genek's specific tasks (palette, typography, mood, hero section, 3 prompts, main page layout).
5. I saved the output directly to `/tmp/n_strona_rod/genek.txt` and verified the file size and timestamp.

## HENIO
Mam komplet faktów. Zapisuję głos na dysk.

Zapis potwierdzony: /tmp/n_strona_rod/henio.txt = 9766 B, nagłówki i podpis na miejscu (linie 1, 4, 9, 35, 41, 70, 73, 79).

RAPORT — HENIO (research, zadanie 1):

WERDYKT
1. ROD NIE ma prawnego obowiązku mieć stronę www. Ustawa o rodzinnych ogrodach działkowych (13.12.2013) wymienia stronę tylko jako DODATKOWE miejsce informacji o opłatach ogrodowych, obok tablicy ogłoszeń. Strona to wybór, nie obowiązek — można robić ją "zajebistą", nie "wymaganą".
2. Jedyne twarde ograniczenie = RODO: nie wolno publikować danych osobowych działkowców (nazwiska przy numerach działek) bez pisemnej zgody — komunikat Krajowego Zarządu PZD 25.09.2019 (pzdsudecki.pl).
3. Wyróżnik, którego NIE ma żaden z 12 przejrzanych polskich ROD: ogłoszenia z telefonu (Hans/Telegram) + kamery na żywo + Barometr Grzybiarza.

SEKCJE OBOWIĄZKOWE (mają je wszystkie dobre ROD)
1. O ogrodzie / Historia; 2. Aktualności/Ogłoszenia (tu wchodzi Hans); 3. Dokumenty: Regulamin ROD + Statut PZD + ustawa; 4. Opłaty ogrodowe (+ opcjonalnie finanse); 5. Kontakt (ul. Młyńska 40c); 6. Galeria; 7. Plan ogrodu/mapa działek (mamy gotowy obraz 00-MAPA-OGRODU.jpg); 8. Polityka prywatności + RODO + cookies; 9. Linki do PZD; 10. Deklaracja dostępności (ma ją już rod-mikolajareja-gdynia.pl).

"ZAJEBISTE" (wzorce do skopiowania)
- Plan ogrodu jako sekcja (rodosa.pl), transparentne finanse ROD (rodnadjeziorka.pl), galeria + konkursy/festyny (rodosa.pl), strefa działkowca "praktyczne" (rodnadjeziorka, reja-gdynia).
- Zagranica: brytyjski nsalg.org.uk ma "Monthly Jobs" i "Foraging and cooking" — ciepła, ogrodnicza treść, której brak polskim ROD-om. Niemieckie kgv-eiche.de / kleingarten.de = obowiązkowe Impressum+Datenschutz, ale styl urzędowy — nie kopiować.

CZEGO UNIKAĆ: lista działkowców z nazwiskami bez zgody; strona-wizytówka "tylko kontakt"; nieaktualne newsy; ciężkie nieskompresowane zdjęcia z budowy (30 plików); urzędowy szablon.

OBOWIĄZKI PRAWNE (potwierdzone)
- Ustawa o ROD 2013: brak obowiązku strony; strona = alternatywne miejsce zawiadamiania o opłatach.
- RODO: zakaz publikacji danych osobowych bez zgody (komunikat KZ PZD 25.09.2019; wzór zgody w "Przewodniku RODO" PZD).
- Dostępność WCAG 2.1 (ustawa 4.04.2019): ROD NIE podlega automatycznie — tylko gdy stowarzyszenie dostaje ≥50% środków publicznych (np. dotacja gminna) lub prowadzi działalność pożytku publicznego w sferach zdrowie/niepełnosprawni/emeryci. Rekomendacja: i tak WCAG 2.1 + deklaracja dostępności (niski koszt, dotacja może objąć wymogiem).
- Statut PZD + Regulamin ROD muszą być dostępne działkowcom — PDF na stronie to najlepsza praktyka.

FAKTY O JÓZEFIE LOMPIE (patron, z linkami)
- Józef Piotr Lompa, ur. 29.06.1797 w Oleśnie, zm. 29.03.1863 w Woźnikach. Śląski nauczyciel, publicysta, poeta, pionier oświaty ludowej i etnografii na Górnym Śląsku; prekursor polskiego odrodzenia narodowego; autor pierwszych polskich podręczników szkolnych na Śląsku (pseudonim A. Mieczyński).
- Związek z nami: od 1819 uczył w Lubszy ponad 30 lat (organista, pisarz gminny), 1858 przeniósł się do Woźnik, pochowany na cmentarzu przy kościele św. Walentego w Woźnikach. W Woźnikach: pomnik na rynku + przed szkołą, Muzeum Józefa Lompy, szkoła jego imienia. W Lubszy: SP im. Lompy z Izbą Pamięci.
- Perła: pisał broszurki o hodowli drzew owocowych i uprawie warzyw — autentyczny patron ogrodu, nie tylko "nauczyciel z pomnika".
- Źródła: pl.wikipedia.org/wiki/Józef_Lompa · silesia.edu.pl/index.php/Lompa_Józef · dladziedzictwa.org/2020/01/15/jozef-lompa-… · lubsza.org · splubsza.pl · ocal.historialubliniec.slask.pl · wozniki.pl/jozef-lompa.html (daje 403 dla bota — fakt potwierdzony przez grounding, nie bezpośredni curl).

REKOMENDACJA (podpisana): v1 = 10 sekcji + 3 wyróżniki (Hans, kamery, barometr) + sekcja "Patron". RODO: działki tylko z numerami 1–51, bez nazwisk. WCAG 2.1 od razu.

PYTANIA DO TOMASZA (moje 2 z 5): (1) lista działek z nazwiskami czy tylko numery (decyzja RODO); (2) czy publikujemy Regulamin ROD + Statut PZD jako PDF i czy Tomasz dostarczy pliki.

NIE WIEM: rok założenia ROD ([DO POTWIERDZENIA]) i pełna nazwa rejestrowa + KRS/REGON/NIP (potrzebne do stopki i deklaracji dostępności).

— Henio

Gotowe. Głos zapisany do /tmp/n_strona_rod/henio.txt (9766 B, zweryfikowany wc + grep), pełny raport powyżej, wniosek trwały do pamięci (18 110/4 000 000 znaków).

— Henio

## BELZEBUB
# GLOS BELZEBUBA 2.0 — doslownie, bez parafrazy (model huihui-ai/Huihui-Qwen3.8-27B-abliterated, narzedzia: web_search+fetch_page)

Belzebub nie odpowiedział.