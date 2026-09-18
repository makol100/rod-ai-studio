# Kartka z QR do rodwozniki.pl + plakat na bramę (D-0419, 18.09.2026)

Dekret: 18.09 08:08 Tomasz „14. Kartka z QR" / „Rób" — jedyny punkt wybrany z narady www/FB (D-0416) po D-0418 „Nic do usunięcia. Tylko do dodania!!!!!!".
Koszt: projekt 0 zł (fabryka). Druk NIE zamawiany — Tomasz drukuje sam; koszt druku NIE WIEM.

## Co powstało (tools/kartka_qr.py → data/kartka_qr/)
- kartka_A6.pdf/.png — 105×148 mm, QR 46 mm
- arkusz_A4_4xA6.pdf — 4 kartki 2×2 z kreskowanymi liniami cięcia; 13 arkuszy = 52 kartki (51 działek + 1)
- plakat_A4.pdf — QR 110 mm (skan z ~1 m), plakat_A3.pdf — QR 170 mm (skan z 1,5–2 m)
- jeden projekt, trzy skale (tekst --s, QR --q niezależnie), paleta strony (zieleń #2e7d4f, krem, logo rod_logo_kolo.png, Fraunces)
- treść: nagłówek „Nasz ogród w Twoim telefonie", duży adres rodwozniki.pl, 5 linii (ogłoszenia zarządu, tablica działkowców, pogoda 8 dni, kamery, dokumenty/regulamin/filmy/poradniki), instrukcja skanowania dla nieskanujących, stopka z adresem Młyńska 40c i e-mailem. Bez „prezes", bez nazwisk, bez pola „Działka nr" (Zenek: nie dodawać).
- wysłane Tomaszowi na Telegram 18.09 08:2x (podgląd A6 + 3 PDF; tools/wyslij_tomaszowi.py — nowe stałe narzędzie sendPhoto/sendDocument/sendVideo botem Hansa)

## Parametry QR (głosy Henia i Zenka, źródła Denso Wave qrcode.com, ISO 18004, reguła 10:1 blinq/qr.technology)
- treść `https://rodwozniki.pl` (z https://, bez śledzenia, bez przekierowań), korekcja H (30 %) → wersja 3, 29×29 modułów, 37×37 ze strefą ciszy 4 moduły
- reguła 10:1: odległość skanu ≈ 10× szerokość kodu → A6 ≥30 mm (mamy 46), A4 ≥100 mm (110), A3 150–200 mm (170)
- QR czarny na białym (Genek: zieleń zabija kontrast w słońcu na laminacie); logo OBOK, nie w środku (starsze telefony); wektor inline SVG w PDF
- laminat MATOWY (połysk = odbłyski), skan pod kątem, nie wieszać na ścianie południowej
- test rozstrzygalny (w skrypcie, `--test`): PNG 300 dpi → 100 i 72 dpi + rozmycie → cv2.QRCodeDetector musi odczytać adres; wynik 18.09: A6/A4/A3 OK na 300/100/72 dpi, arkusz 4/4 na 300 i 100 dpi (na 72 dpi multi-detekcja 0/4 — bez znaczenia dla druku 300 dpi)
- kontrola geometrii JS: treść nie wystaje z karty, elementy ≥5 mm od krawędzi cięcia — 0 wad; oko Genka (oczy_uszy) na A6 i A3: tekst w całości, QR z marginesem, logo całe, „prezes" NIE

## Ryzyka zgłoszone przez załogę (dla Tomasza)
- Zenek: ktoś może nakleić fałszywy QR na publiczny plakat — duży jawny adres ogranicza ryzyko, plakat oglądać co jakiś czas
- Belzebub: kartka A6 w skrzynce ginie pod rachunkami — laminować albo koszulka z klipsem
- Henio: przed drukiem 52 sztuk zeskanować wydruk na ≥3 telefonach, w tym starym
- Belzebub w propozycji tekstu napisał „RODWOZNKI.PL" (brak I) — nie skopiowane; adres na kartce sprawdzony literowo przez oko Genka

## Otwarte
- decyzja Tomasza po obejrzeniu: drukować / poprawić treść (alternatywne nagłówki załogi: Zenek „Twój ogród zawsze pod ręką", Belzebub „Nasz ogród — wszystko na jednej stronie")
- ewentualna zmiana adresu w QR (np. licznik skanów) — tylko na polecenie

## v2 — grafiki (D-0421, 18.09 08:22–08:35)
Tomasz: „Dodaj parę grafik związanych z tematem" / „Zobacz co mamy na fb" / „Powinno to też być na vps".
- Fakt: strona FB ma 13 wgranych grafik (Graph API /me/photos?type=uploaded); ich pliki źródłowe NIE leżały na VPS (tylko logo i og.jpg pasowały wymiarami) → ściągnięte do assets/grafiki_fb/ (+photos.json z opisami). Od teraz: każda grafika publikowana na FB ma mieć kopię na VPS.
- Ocena oka Genka: 11 z 13 to plansze z tekstem; do kartki nadaje się tylko ilustracja tablicy ogłoszeń (04.09, 1024×1024) — kadr 60–90 % szer. × 30–80 % wys. bez napisów i logo.
- Kartka v2: po bokach kodu QR dwa kadry 3:5 (lewa: tablica ze słonecznikami, prawa: alejka ogrodu z gal/alejka/d4_03), QR 42 mm (A6) — bez zmiany wysokości układu. Pliki: data/kartka_qr/grafiki/g1_tablica.jpg, g2_alejka.jpg.
- Kontrola: geometria 0 wad, test dekodowania zielony (tools/test_kartka_qr.py), oko Genka: grafiki bez napisów, nie dotykają QR, spójna kolorystyka, „prezes" NIE. Wysłane Tomaszowi (Telegram 1027–1030).
- Lekcja (Klaudek): podgląd obrazu z VPS do własnego oka — base64 w wyniku narzędzia zjada kontekst; zamiast tego wynik >60k znaków ląduje w pliku tool-results i tam się dekoduje (0 kosztu kontekstu). Właściwe narzędzie do kontroli i tak = oko Genka + testy maszynowe.

## v3 — „Grafikę nie zdjęcia głąbie" (D-0422, 08:29)
- Zdjęcie alejki wypada. Próba innych kadrów z grafik FB (27.06 narzędzia, 28.06 altana): oko Genka najpierw wskazało „czyste" obszary, a po wycięciu stwierdziło w nich tekst → kadry z plansz FB są niepewne; nie ufać jednej odpowiedzi oka, sprawdzać wycięty kadr osobno.
- Prawa strona = WŁASNA ilustracja wektorowa tools/grafika_konewka.py (SVG 3:5: słońce, płotek, krzak pomidorów, konewka, marchewki; paleta strony) — 0 zł, bez ryzyka tekstu, styl płaski jak ilustracja tablicy po lewej. Wbudowana inline w kartkę (wektor w PDF).
- Kontrola: geometria 0 wad, dekodowanie zielone, Genek: obie grafiki to ilustracje bez tekstu/logo, nie dotykają QR, spójny styl; „prezes" NIE. Wysłane Tomaszowi 18.09 (Telegram 1033–1036).
- Opcja płatna zgłoszona Tomaszowi, nieużyta: ilustracja generowana przez Genka ~0,07 USD/obraz (wiedza/GENEROWANIE_OBRAZU.md).

## ZAMKNIĘCIE 18.09 08:35
Tomasz (dosłownie): „Dzięki super" — v3 przyjęta. Druk po stronie Tomasza (pliki na Telegramie 1033–1036 i w data/kartka_qr/).
