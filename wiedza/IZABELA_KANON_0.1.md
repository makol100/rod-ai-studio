# IZABELA — KANON 0.1 (decyzja Tomasza, 29.07.2026)

## DECYZJA
Tomasz, 29.07.2026, dosłownie: **„Izabela"** — po naradzie całej załogi nad nową postacią prowadzącą.
Poprzedzone dekretem: *„Nie musimy się trzymać Stanisława i na siłę go odmładzać. Możemy stworzyć nową
postać. Może to być kobieta. Wiek 50 lat. To są osoby w idealnym wieku i wybrani do zarządu, wzbudzają
do siebie zaufanie."*

**To znosi STANISLAW_CANON_1.0 w zakresie postaci prowadzącej.** Pan Stanisław przechodzi do archiwum.
Powód odrzucenia (Tomasz): *„Wieje starocią z tego Stanisława i z jego do zobaczenia przy płocie.
Może tchnąć trochę rozwoju w ten ROD. Wszyscy dzisiaj pracujemy na komputerach, wszystko jest
zcyfryzowane. To są relikty dziadostwa."*

## KIM JEST IZABELA — **AWATAR ZARZĄDU** (decyzja Tomasza 30.07 wieczorem)

Dosłownie: **„Jest Awatarem Zarządu"**.

To rozstrzyga problem, który wcześniej wisiał. Załoga odrzuciła propozycje, w których Izabela miała
być członkinią zarządu (Helena-sekretarz, Danuta-skarbniczka) — bo awatar udający realną funkcję
ośmiesza. Ale nie była też niczyim awatarem, więc nie mogła powiedzieć „jestem awatarem X".

Teraz może: **jest awatarem ZARZĄDU jako organu**, nie konkretnej osoby. Mówi w imieniu zarządu,
nie podszywa się pod żadnego człowieka, a deklaracja mieści się w jednym zdaniu.

Wzorzec z filmu wskazanego przez Tomasza (youtu.be/N91bU7nzo-Q): awatar otwiera wypowiedź zdaniem
„Jestem wirtualnym awatarem [imię]" — deklaracja jest PIERWSZYM zdaniem, krótka, ton rzeczowy,
bez przepraszania i bez chwalenia się. Żadnego „dzień dobry" przed nią.
Różnica: tamten jest awatarem konkretnego człowieka, Izabela jest awatarem ORGANU.

## Poprzednia formuła (nadal obowiązuje w części o zakazach)
Dekret Tomasza, 29.07: *„Zawsze na początku może powiedzieć, że jestem wygenerowanym prezenterem
sztucznej inteligencji i zatrudnionym jako reporter do zarządu."*

- **NIE jest** członkiem zarządu, działkowcem ani realną osobą z ROD
- **JEST** jawnie wygenerowaną prezenterką AI, pracującą jako reporter **dla** zarządu
- mówi w imieniu zarządu, ale nie podaje się za nikogo
- kobieta, ok. 50 lat, imię **Izabela** (sprawdzone: nie występuje w dokumentach ROD ani wśród osób)

## DLACZEGO TAK — trzy powody, każdy ze śladem
1. **Prawo.** Art. 50 AI Act zaczyna być stosowany **2 sierpnia 2026**. Definicja deepfake obejmuje
   wygenerowany materiał wideo przypominający istniejące osoby lub wydarzenia, który może zostać
   uznany za autentyczny; podmiot profesjonalnie korzystający z AI ma ujawnić sztuczny charakter,
   a oznaczenie ma być jasne przy pierwszym kontakcie odbiorcy z materiałem.
   Deklaracja w pierwszym zdaniu spełnia to naturalnie, bez naklejki na obrazie.
2. **Zaufanie.** Badanie CHI 2026 (dwa eksperymenty, 2000 uczestników): wideo z pośrednictwem AI
   obniża postrzegane zaufanie i pewność ocen widzów. Ukrywanie tego pogłębia problem; deklaracja
   zamienia słabość w uczciwość.
3. **Ośmieszenie.** Zenek: *„Najbardziej ośmieszy nas awatar, który udaje prawdziwą działkowiczkę
   albo członkinię zarządu."* Propozycje Henia (Helena, sekretarz) i Genka (Danuta, skarbniczka)
   przypisywały jej REALNĄ funkcję w zarządzie — odrzucone z tego powodu.

## USTALENIA ZAŁOGI, KTÓRE ZOSTAJĄ W MOCY
- **Kobieta ~50 lat** — potwierdzone niezależnie przez wszystkich trzech
- **Postać jest KLAMRĄ, nie całą rolką** (Genek, Henio zbieżnie): wejście i wyjście, środek to
  prawdziwy materiał z ogrodu. Powód: stała obecność awatara przez 60–90 s zwiększa ryzyko wyłapania
  wad mimiki i braku mrugania
- **Czego widzowie nie wybaczą** (Zenek): szklany wzrok, brak mikroruchów twarzy, uśmiech przy
  poważnym komunikacie, ręce bez związku ze zdaniem, zła wymowa lokalnych nazw, zmiana twarzy między
  odcinkami, pewne podanie błędnej daty lub liczby
- **Zakaz udawania doświadczeń**: nigdy „byłam dziś na działce", „rozmawiałam z prezesem" — ona nigdzie
  nie była i z nikim nie rozmawiała
- Otoczenie: **żadnego studia telewizyjnego** — wszyscy trzej odrzucili jako parodię przy 51 działkach

## KANON GŁOSU — CHARLOTTE (wybór Tomasza, 29.07.2026)

Casting płatny, 6 żeńskich głosów, ten sam tekst docelowego intro. Koszt **0,23 USD**
(saldo fal.ai 10,28 → 10,05). Tomasz wskazał **Charlotte**.

    endpoint:        fal-ai/elevenlabs/tts/eleven-v3
    voice:           Charlotte
    language_code:   pl
    stability:       0.4
    similarity_boost:0.75
    speed:           1.0
    output_format:   mp3_44100_128

Referencja zamrożona: `data/awatar/IZABELA_GLOS_CANON_Charlotte.mp3` (444, SHA-256 21e4eb4eb8a8...).
Charlotte była NAJSPOKOJNIEJSZA z szóstki: 460 znaków w 31 s = 14,8 znaku na sekundę
(Alice i Laura 28 s). Przy planowaniu długości: **~15 znaków tekstu na sekundę nagrania**.
Skasowane próbki pozostałych pięciu głosów zostają w `data/awatar/iza_casting_*.mp3` jako materiał
porównawczy — nie kasować, gdyby trzeba było wrócić.

## TEKST INTRO UŻYTY W CASTINGU (do zatwierdzenia lub skrócenia po odsłuchu)

„Dzień dobry, z tej strony Izabela. Jestem prezenterką wygenerowaną przez sztuczną inteligencję,
pracuję jako reporter dla zarządu Rodzinnego Ogrodu Działkowego imienia Józefa Lompy w Woźnikach.
Dziś krótko i konkretnie: co się zmienia w naszym ogrodzie i co trzeba zrobić."

Uwaga: w tekście świadomie użyta PEŁNA nazwa zamiast skrótu „ROD" — przy Stanisławie skrót był
pułapką wymowy. Outro w castingu: „Do zobaczenia w ogrodzie".

## TŁO I OTOCZENIE — DECYZJA TOMASZA 30.07: DROGA B, TŁO NEUTRALNE

Dosłownie: **„Dopracować do perfekcji studio neutralne."**
Odrzucone: fotorealistyczne wnętrze (weranda/kuchnia/kącik) oraz Izabela na tle prawdziwego ogrodu.
Głosy w naradzie pełnego składu: Genek — B, Henio — C, Klaudek — B. Rozstrzygnął Tomasz.

Argument, który przeważył (Genek, z kanonu): skoro Izabela w pierwszym zdaniu deklaruje, że jest
wygenerowana, to budowanie jej hiperrealistycznego, ale fikcyjnego pokoju przeczy tej szczerości.
Argument przeciwny, odrzucony ale wart pamięci (Henio): „Izabela jest reporterką ogrodu, powinna być
na tle ogrodu; postać gadająca o prawdziwym ogrodzie, stojąc w narysowanej kuchni, to właśnie udawanie."

## KARTA IZABELI — ZAAKCEPTOWANA PRZEZ TOMASZA 30.07.2026

Plik: `assets/izabela/IZABELA_CANON.png` (444), SHA-256 b7776412a79d88db2e320cd7, 1536x2752.
Model: `fal-ai/nano-banana-pro`, 9:16, 2K. Koszt pary prób: **0,15 USD** (saldo 10,01 → 9,86).

**Akceptacja Tomasza:** po obejrzeniu wersji drugiej napisał dosłownie **„Super"**.
Wersja pierwsza została przez niego ODRZUCONA słowami **„Zwykła baba"** — powód po stronie Klaudka:
w prompcie stało „naturally attractive in an ordinary, believable way", czyli dosłowne polecenie
zrobienia przeciętnej, plus płaskie frontalne światło i zakaz jakiegokolwiek uśmiechu.

**Co zmieniono w wersji drugiej (i tylko to):** uroda przez strukturę (wyraźniejsze kości policzkowe,
większe i lepiej osadzone oczy, harmonijne proporcje), światło pętlowe z lewej pod 40 stopni zamiast
płaskiego frontalnego, cień uśmiechu w oczach zamiast twarzy całkowicie neutralnej.
Nietknięte: wiek, siwizna, brak makijażu, faktura skóry, tło do wycięcia, pusty pas u góry.

**Zmierzone na v2:** wiek odczytany 50–55, uroda 8/10, zmarszczki wokół oczu TAK, fałdy nosowo-wargowe
TAK, linie na szyi TAK, siwe pasma TAK, światło modeluje twarz, tło jednolite, górne 16% puste.

## TEKST WEJŚCIA — KANON (decyzja Tomasza 30.07, wariant 2)

**„Jestem Izabela, wirtualny awatar zarządu. Dwa popołudnia koparka karczowała zarośnięty teren
przy domu działkowca."**

114 znaków = ok. 7,6 s przy tempie Charlotte (15 znaków/s).

**Formuła przedstawiania się — Tomasz, dosłownie: „Jestem wirtualnym awatarem zarządu."**
Wzorzec z filmu youtu.be/N91bU7nzo-Q wskazanego przez Tomasza: awatar otwiera zdaniem
„Jestem wirtualnym awatarem [imię]" — BEZ powitania, bez wstępu. Deklaracja jest pierwszym słowem.
Zenek i Henio obejrzeli niezależnie i podali identyczne brzmienie. Ton rzeczowy, neutralny,
bez przepraszania i bez chwalenia się. Tempo ok. 140 słów/minutę.

**Dlaczego bez „dzień dobry":** kosztuje ok. 0,7 s i osłabia wejście (Henio: „Izabela to nie
recepcjonistka — pierwsze słowo to jej imię"). Wzorzec z filmu też go nie ma.

**Ujawnienie AI — DWA KANAŁY, każdy osobno wystarczalny:**
- OBRAZ: stały napis „PREZENTERKA AI" w studiu, widoczny od pierwszej klatki, także bez dźwięku
- GŁOS: „wirtualny awatar zarządu" — mówi, że jest bytem cyfrowym i czyim jest awatarem
Uwaga Henia z analizy filmu: „wirtualny awatar" NIE jest tożsame z „jestem AI" — tamten awatar
ani razu nie mówi, że jest AI. U nas lukę zamyka napis na ekranie.

## CZOŁÓWKA I NAPISY — KANON (decyzja Tomasza 30.07)

**BEZ osobnej planszy czołówkowej.** Napis nakładany NA pierwsze ujęcie.

| element | wartość |
|---|---|
| tytuł | „WIADOMOŚCI DZIAŁKOWE" na pierwszym ujęciu, **2,5 s**, miękkie wejście i zniknięcie |
| dźwięk czołówki | **brak** — pierwsze sekundy należą do obrazu |
| daty na zdjęciach | **„20 LIPCA"** na zarośniętym terenie (data podana przez Tomasza — plik FB_IMG nie ma daty w nazwie), „30 LIPCA" na wykarczowanym |
| outro | ostatni kadr zatrzymany ~1 s z napisem o zgłaszaniu pomocy; **bez planszy z logo** |
| podtytuł z tematem | **odrzucony** — za dużo warstw tekstu naraz na jednym ujęciu |

**Dlaczego bez osobnej planszy** (zbieżnie Zenek + Henio, ze źródłami):
- Meta: pierwsze sekundy na szybkie rozpoczęcie historii; filmy startują bez dźwięku
- BBC: zaczynać od obrazu przyciągającego także bez dźwięku
- Reuters: branding WEWNĄTRZ materiału (napis, watermark), nie przed nim
- osobna plansza = dodatkowy plik o innych parametrach = ryzyko narastającego rozjazdu A/V
  (zmierzone 2,25 s na 70 s przy odcinku #10009)
- logo ROD jest już na stałe w prawym górnym rogu studia — czołówka byłaby zdublowaniem
- Henio sprawdził całe repo: decyzja „intro i outro obowiązkowe" z 17.07 dotyczy WYŁĄCZNIE
  serii humorystycznej; dla Wiadomości nie było żadnej

**Dlaczego 2,5 s a nie 1,5 s:** widownia to często starsi działkowcy, „WIADOMOŚCI DZIAŁKOWE"
to dwa długie słowa. Nieprzeczytany tytuł szkodzi bardziej niż sekunda różnicy.

**Dlaczego daty:** rolka jest „przed i po". Z datami cała historia czyta się BEZ DŹWIĘKU
w trzy sekundy, samym porównaniem dwóch kadrów — a tak ogląda większość widzów na Facebooku.

## TEKST WYJŚCIA — KANON (decyzja Tomasza 30.07, wariant 1)

**„Zostały doły po ciężkiej pracy. Chęć pomocy można zgłosić do zarządu."**

POPRAWKA Tomasza 30.07 po kontroli Zenka: pierwotne „stosy gałęzi" NIE MIAŁY POKRYCIA —
Zenek sprawdził wszystkie pięć zdjęć z 30.07, gałęzi nie ma na żadnym (widać stosy korzeni i pni),
a w OPIS.md ich nie ma. Gałęzie widać wyłącznie na zdjęciu „przed". Tomasz zmienił na
„doły po ciężkiej pracy" — nie opisuje przedmiotu, którego nie widać.

80 znaków = ok. 5,3 s. Najpierw FAKT, który widz właśnie zobaczył na zdjęciach, potem PROŚBA.
Tomasz: „Tu trzeba napisać, że potrzebujemy pomocy działkowiczów" + „Że można zgłosić chęć pomocy".

Nie podajemy terminu, zakresu prac ani sposobu kontaktu — **tych szczegółów jeszcze nie ma**
i nie wolno ich zmyślać. Gdy będą, wchodzą do następnych wiadomości.
Odrzucone: „do usłyszenia przy płocie" (zostało po Stanisławie, uznane za staroć).

**Odrzucone warianty:** pełna nazwa ogrodu w wejściu (zjada 9,8 s, nie zostaje czasu na treść),
„awatar zarządu naszego ogrodu" (dłuższe bez zysku), wersje bez imienia.

## STUDIO — DECYZJA TOMASZA 4.08.2026: ZOSTAJA TYLKO WERSJE Z 1 SIERPNIA

> Tomasz 4.08 09:39, po obejrzeniu wszystkich 15 wariantow: **„Zostaja tylko te z pierwszego sierpnia."**

**OBOWIAZUJA:** `TV_STUDIO.png` (1.08, 20:46) i `TV_STUDIO_v2.png` (1.08, 21:07).

**WYGASLY** wszystkie warianty z 30.07: kanon `STUDIO_IZABELI_CANON.png`, cztery warianty tonacji
(t1 zielen z logo, t2 ciemniejsza, t3 zgaszona, t4 srednia), cztery warianty kadru (w1 kwadrat,
w2 kolo, w3 kolo przygaszone, w4 kolo male), tlo i podglad kanonu.
Nie usuniete (dekret 2.08) — oryginaly w `assets/izabela/` i `data/upload/podglad/`,
kopie robocze odstawione do `.scratch/studio_odrzucone_4.08/`.

**LUKA W ZAPISACH, ktora to ujawnilo:** obie wersje z 1.08 powstaly wieczorem (20:46 i 21:07)
i NIE MA o nich ani slowa w kanonie ani w teleporcie — mimo ze waza po ponad megabajcie,
czyli sa pelnymi obrazami, nie podgladami. Klaudek meldowal 4.08, ze „studio bylo do poprawki
i wszystkie warianty odrzucone", nie sprawdziwszy, ze dzien przed odrzuceniem rolki powstaly dwa nowe.

## STUDIO — KANON ZAMKNIĘTY 30.07.2026 (wersja po wygenerowaniu Izabeli)

Generator: `tools/tlo_izabeli.sh` — **kod, nie model AI**. Dwa przebiegi = plik identyczny co do piksela.
Plik kanoniczny: `assets/izabela/STUDIO_IZABELI_CANON.png` (444), SHA-256 7acfd27acbfa056a47260b2e

| element | wartość | decyzja Tomasza |
|---|---|---|
| baza tła | `#A89464` „zboże jasne" | „Poproszę jaśniejsze tło" → wariant 2 z czterech |
| rozjaśnienie góry | +38/+36/+30, sigma 520×640, środek (540,560) | — |
| cień za postacią | −30, sigma 300×520, środek (540,1150) | wariant B „cień delikatny" z trzech |
| logo | prawy górny róg, koło 110 px, odsunięte 45 px | „logo najmniejsze w kółku" |
| napis | „PREZENTERKA AI", biel 95% na czarnym pasku 26% | skrócony na jego polecenie |
| elementy w tle | **żadne** | cała załoga: każdy element może się przesunąć |

### Dlaczego ten kolor — dobrany do NIEJ, nie na oko
Tomasz: „Ma być dopasowany do tej pięknej Izabeli". Kolory wyciągnięte z jej karty:
bluzka `#466270` zajmuje 12% kadru (największa powierzchnia po tle), włosy i skóra `#624638`.
Ciepłe zboże kontrastuje z turkusem bluzki.

### Separacja postaci — CIENIEM, nie samym kolorem
Propozycja Zenka z narady 30.07. Bramka oka na wersji bez cienia: „kontrast jest, ale nie ma
wyraźnego odcięcia, obraz wydaje się nieco płaski". Cień za postacią na wysokości tułowia
naśladuje realne studio i przywraca głębię bez zmiany koloru tła.

### Postać — jak została odklejona (robota Zenka)
Plik: `assets/izabela/IZABELA_ODKLEJONA.png` (444), kod: `tools/wytnij_izabele.py`
Model **`birefnet-portrait`** przez rembg w `/opt/rembg-venv`, plus krok kluczowy:
**usunięcie domieszki starego tła wyłącznie z pikseli częściowej alfy**.
Zmierzone: miękka krawędź 1,41%, przezroczyste 46,1%, pełne 52,5%,
twarz/szyja/bluzka — zero przezroczystych pikseli, zero zmodyfikowanych pikseli kryjących,
krawędź o 29% ciemniejsza od wnętrza (brak jasnej obwódki).

**Czego NIE robić:** `colorkey` w ffmpeg — wyżera fragmenty czoła, policzków, nosa i szyi,
bo odcień skóry bywa zbliżony do tła. Wykrył to Zenek, mierząc kanał alfa.
`u2net_human_seg` z erozją 3 px daje maskę praktycznie binarną — włosy „jak wycięte nożyczkami".

## UJAWNIENIE AI — NAPIS OBOWIĄZKOWY W PIERWSZYM KADRZE
Zenek i Henio niezależnie ustalili, że ujawnienie **wyłącznie głosowe nie wystarcza**: film może
wystartować bez dźwięku, a wymóg mówi o formie jasnej i postrzegalnej przy pierwszym kontakcie,
bez potrzeby narzędzi technicznych. Wdrażający nie może polegać tylko na oznaczeniu maszynowym.
Treść napisu: **PREZENTERKA AI** (rozstrzygnięcie Tomasza 30.07: „Napis o AI krótki").
Wcześniej kanon miał w dwóch miejscach różne wersje — dłuższą „IZABELA — PREZENTERKA WYGENEROWANA
PRZEZ AI" i krótszą. Obowiązuje KRÓTKA, ta sama, którą wpisuje generator studia.
Napis nakłada MONTAŻ, nie generator obrazu (generatory psują tekst).

## OŻYWIENIE — KANON: OmniHuman 1.5 (decyzja Tomasza 30.07)

Model: **`fal-ai/bytedance/omnihuman/v1.5`** przez fal.ai.
Cena zmierzona: **~0,17 USD za sekundę** (2 filmy po 5 s = 1,73 USD; saldo 9,70 → 7,97).
UWAGA na rozliczenie opóźnione: pierwszy test pokazywał 0,0087 USD, prawdziwy koszt doszedł później.
Nie ogłaszać ceny, dopóki saldo się nie ustabilizuje.

**Parametry, które mają znaczenie** (schemat z fal):
- `prompt` — OPIS RUCHU. Bez niego model robi minimum: rusza się sama twarz, ramiona stoją.
  Z opisem ruchu dostajemy oddech, ruch tułowia i ramion. To była różnica między pierwszą a drugą próbą.
- `resolution` — domyślnie 1080p. **Audio musi być krótsze niż 30 s dla 1080p.**
- `turbo_mode` — szybciej kosztem jakości; NIE używać.

**Zmierzone na drugiej próbie (bramka oka):** mruga, głowa się porusza, ruch brwi i policzków,
ramiona i tułów się poruszają, wygląda żywo, tło/logo/napis nietknięte.

### ZNANE OGRANICZENIE: polska artykulacja
Tomasz: „Izabela mówi pięknie wyraźnie. Te usta nie pasują."
Zbieżna diagnoza Zenka i Henia, każdy inną drogą, ze źródłami:
- polskie kontrasty rozgrywają się GŁÓWNIE WEWNĄTRZ jamy ustnej (język, podniebienie) — model może
  otwierać usta estetycznie, a mimo to pokazywać błędną artykulację; pojedyncza klatka tego nie wykryje
- polski ma trzy serie szumiące (`s/z/c`, `ś/ź/ć`, `sz/ż/cz`) — tabela Amazon Polly rozdziela je na trzy
  wizemy, model uczony na angielskim ma dla nich jeden
- nosowe `ą`/`ę` nie mają fonemicznego odpowiednika w angielskim
- Henio z obejrzenia filmu: „wargi zaokrąglone" = pozycja domyślna angielska; polski wymaga częściej
  układu PŁASKIEGO (nosowe, miękkie) i WYSUNIĘCIA warg (szumiące)
- polski zestaw wizemów istnieje TYLKO w pracach naukowych (Janicki i in. 2010, Lorenc 2015);
  narzędzia komercyjne mapują na 14-15 wizemów MPEG-4 opartych na fonetyce angielskiej
- HeyGen jako JEDYNY wymienia polski wprost w synchronizacji ust; Kling deklaruje chiński, angielski,
  japoński, koreański, hiszpański — bez polskiego; OmniHuman nie podaje listy języków

**Decyzja Tomasza mimo tego ograniczenia: zostajemy przy OmniHuman.**
**30.07: „Izabela niech zostanie tak jak ją widziałem. Nie spowalniały."** — czyli kanonem ruchu jest
wersja B (żywsza) z NORMALNYM tempem mowy. Test ze spowolnieniem o 11% NIE został uruchomiony,
mimo że nagranie było gotowe (`data/upload/podglad/iza_audio_wolne10.mp3`) — Tomasz odrzucił.
Powód odrzucenia parametru `speed=0.9` u ElevenLabs: zmierzone, wydłuża nagranie o 1%, nie o 10%.
Nie próbować naprawiać tego promptem — Zenek sprawdził, nie ma udokumentowanego parametru artykulacji.
Niesprawdzona przesłanka warta jednej próby: audio wolniejsze o 5-10%.

## CO ZOSTAŁO DO ZROBIENIA (stan 30.07 wieczorem)

Postać, głos i studio są ZAMKNIĘTE. Otwarte jest to, co dzieje się DALEJ:

1. [~] **Ożywienie Izabeli** — model: OmniHuman 1.5 (dwie próby wykonane 29-30.07, $1.73 łącznie,
   patrz sekcja OŻYWIENIE wyżej). Do decyzji: czy jakość ust jest akceptowalna dla polskiego.
   Kling NIE jest już modelem docelowym — został zastąpiony przez OmniHuman.
2. [ ] **Tekst pierwszego wejścia** — intro z deklaracją AI jest napisane i nagrane w castingu.
   Do decyzji: czy zostaje w obecnym brzmieniu, czy skrócić.
3. [ ] **Montaż WD_0001** — materiał zweryfikowany klatka po klatce (koparka WA0007 17-27 s,
   człowiek WA0005 19-29 s, teren 093926 0-52 s, gałęzie 62-70 s). Czeka na decyzję.
4. [ ] **Zdjęcia „przed i po"** — Tomasz miał je zrobić (korzenie i cały teren), nie ma ich na dysku.

## PAN STANISŁAW — NA PÓŁKĘ
Decyzja Tomasza 29.07: *„Pan Stanisław jest gotową postacią. Odstawiamy na półkę i wiemy, że go mamy."*
Nie kasować: karta kanoniczna, głos Daniel, sześć wersji WD_0001. Gotowy do użycia, jeśli wróci potrzeba.
