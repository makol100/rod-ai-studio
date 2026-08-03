# PIERWSZA ZMIANA GENKA — niezależny audyt sekundnika rolki 10010

Jesteś Genkiem — trzecim członkiem załogi (rodzina Gemini), świeżym okiem. NIE uczestniczyłeś w tworzeniu tego materiału i nikt Ci nie powie, kto co napisał. Twoje zadanie: bezlitosny audyt, czy ta rolka będzie ZAJEBISTA I ŚMIESZNA (rozkaz szefa nad szefami). Odpowiadasz po polsku, zwięźle, konkretnie. Nie czytasz plików — wszystko masz poniżej.

## Zadanie
1. Oceń SEKUNDNIK beat po beacie: czy timing, cisze i dźwięk faktycznie budują śmiech, czy tylko wyglądają mądrze na papierze.
2. Wskaż 3 NAJSŁABSZE punkty architektury i dla każdego konkretną poprawkę montażową (preferuj $0).
3. Zderz z KANONEM autora (niżej): czy architektura niczego z esencji żartu nie zgubiła (ścisk! pisk! niemowa przemówił!).
4. WERDYKT: ZATWIERDZAM / ZATWIERDZAM Z POPRAWKAMI / ODRZUCAM + trzy zdania uzasadnienia.

Format: ## OCENA BEATÓW / ## 3 NAJSŁABSZE PUNKTY / ## ZDERZENIE Z KANONEM / ## WERDYKT

=========== SEKUNDNIK (architektura do audytu) ===========
=== ARCHITEKTURA KOMIZMU 10010 — konsensus trójki (Klaudek+Zenek+strażnicy), 26.07 ===

## SEKUNDNIK

| Beat | Czas | OBRAZ | DŹWIĘK | Funkcja komiczna |
|---:|---:|---|---|---|
| 0 | 0:00–0:45 | Krótkie animowane intro `rod_profilowe`; natychmiastowy cut do sadu | Krótki sting brandu, ucięty bez wybrzmiewania | Szybkie otwarcie, bez zabierania czasu żartowi |
| 1 | 0:45–3:00 | k01, szeroki plan zasadzki; powolny najazd. Plansza: „Kiedy złapiesz złodzieja jabłek... 🍎” przez ok. 1,6 s | Cykady i cichy szelest liści | Mock-seriousness: Tomek zachowuje się jak komandos, choć pilnuje jabłek |
| 2 | 3:00–3:35 | Ostatnie klatki k01: nagły shake/whip w stronę korony | Głośny trzask gałęzi; szelest urywa się natychmiast | Zaskoczenie i przygotowanie ataku |
| 3 | 3:35–4:45 | Gwałtowny punch-in na zaakceptowany chwyt → krótki fragment k02; cięcie ma jednoznacznie pokazać pięść między nogawkami | VINE BOOM dokładnie na pierwszej klatce chwytu; po nim brak cykad i szelestu | Pierwszy właściwy beat śmiechu: niewspółmiernie „epicki” atak i absurdalne miejsce chwytu |
| 4 | 4:45–6:65 | k03, jump-cut do twarzy Tomka; lekki punch-in na „ktoś ty?!” | „Gadaj, ktoś ty?!”; po kwestii 0,30 s absolutnej ciszy | Pierwsza próba przesłuchania; kontrast groźnej formy z absurdalną sytuacją |
| 5 | 6:65–7:20 | Szeroki kadr chwytu/still; bez ruchu poza minimalnym cyfrowym najazdem | Cisza 0,55 s | Widz czeka na odpowiedź, której nie ma — cisza staje się żartem |
| 6 | 7:20–9:55 | k04, chwyt cały czas czytelny; cięcie do mocniejszego punch-inu przy końcu pytania | „Gadaj, pókim dobry, ktoś ty?!” | Eskalacja: Tomek zadaje praktycznie to samo pytanie, tylko jeszcze poważniej |
| 7 | 9:55–10:50 | Freeze/punch-in na nogawki i pięść; żadnej akrobatyki obrazu | 0,15 s ciszy → wyduszone „Józek...” z pitch-upem do zaakceptowanego wariantu A, ok. 0,55 s → 0,15 s ciszy | Drugi mocny beat śmiechu: z korony wychodzi niemożliwie piskliwe jedno słowo |
| 8 | 10:50–13:20 | Zaakceptowany szeroki kadr chwytu jako still; szybki Ken Burns, ok. 100→118%. Obraz k05 nie występuje | Czyste audio k05: „No gadaj draniu, ktoś ty?!”; żadnego podkładu | Eskalacja przez idiotyczną konsekwencję Tomka: usłyszał imię, lecz dalej przesłuchuje |
| 9 | 13:20–13:65 | Bardzo krótki dodatkowy punch-in na sam chwyt | Krótki, suchy SFX ściśnięcia materiału/skrzypnięcia gałęzi; potem 0,20 s ciszy | „Ostatnie ściśnięcie” bez dosłowności; wizualny setup puenty |
| 10 | 13:65–17:80 | Nowy niemy k06: Tomek osłupiały, usta domknięte, chwyt utrzymany. Minimalny ruch; bez napisów-widmo | Puenta wycięta z batchowego k06 i położona z offu: „To ja... Józek... niemowa ze wsi!”. Pitch-up dobrany z dwóch wariantów na bazie źródła 145 Hz; ostatnie „wsi!” kończy się twardo, bez dopowiedzenia | Główny beat śmiechu: absurd logiczny — „niemowa” przemawia dopiero po ściśnięciu, a Tomek nie jest mówcą |
| 11 | 17:80–18:60 | Twardy cut do obowiązkowego outro brandu z oznaczeniem AI | Krótki sting outro, oddzielony od puenty cięciem | Brand jest obecny, ale nie rozcieńcza puenty |

Całość: około **18,6 s z intro i outro**. Napisy KOLORY_ASS mają wejść w rytm słów, dzielone po interpunkcji, maksymalnie około sześciu słów. „Józek...” i puenta dostają osobny kolor Józka. Żadnych napisów na ciszy. Wszystkie części przed concat należy znormalizować do 24 fps, 1080×1920, AAC 48 kHz stereo; po montażu różnica długości strumieni audio–wideo poniżej 0,05 s i `faststart`.

## KOMIZM

1. **Atak i VINE BOOM — kontrast + absurd**  
   Tomek zachowuje się jak bohater thrillera, ale „operacja specjalna” dotyczy złodzieja jabłek i kończy się chwytem między nogawkami. Obecnie ścisk pojawia się znikąd. Trzask, shake, punch-in i boom przywracają brakującą przyczynę.

2. **Cisza po pierwszym pytaniu — timing**  
   Pytanie potrzebuje pustego miejsca na odpowiedź. Natychmiastowe przejście do następnej kwestii zgubiłoby fakt, że schwytany nie odpowiada. Około 0,55 s martwej ciszy pozwala widzowi zauważyć problem.

3. **Wyduszone „Józek...” — eskalacja + dźwiękowy absurd**  
   Po drugim nacisku pojawia się jedno piskliwe słowo. Śmiech ginie, jeśli brzmi ono jak zwykły męski głos. Pitch-up i freeze na chwycie łączą przyczynę z reakcją.

4. **Trzecie pytanie mimo podania imienia — eskalacja charakteru**  
   Tomek dostał odpowiedź „Józek”, lecz nadal pyta „ktoś ty?!”. To robi z niego komediowo zacietrzewionego przesłuchującego, nie realistycznego oprawcę. Obraz k05 gubił ten żart, bo Tomek wyglądał jak przypadkowy gapowicz. Szeroki kadr chwytu przywraca relację i ciągłość.

5. **„Niemowa ze wsi” — sprzeczność + puenta**  
   Największy śmiech wynika z logicznego absurdu: niemowa jednak mówi, bo Tomek go „wydusił”. Jeśli puentę wypowiada widoczny Tomek, żart całkowicie znika. Dlatego k06 musi być niemy, a Józek wyłącznie głosem z korony.

Materiał gra zbyt grobowo przede wszystkim w k01 i dialogach Tomka. Nie próbowałbym udawać, że tego nie ma: montaż ma przekodować powagę w **mock-seriousness** przez krótkie jump-cuty, przesadnie filmowy VINE BOOM, kolorowe napisy, bezczelnie długie cisze i pisk będący kompletnie nieadekwatną odpowiedzią na groźne przesłuchanie.

## DŹWIĘK

- **Muzyka: NIE podczas żartu.** Muzyka dramatyczna dołożyłaby serio-powagi, a muzyka komediowa tłumaczyłaby widzowi, kiedy ma się śmiać. Wystarczą krótkie stingi brandowe w intro i outro.
- **0:45–3:00:** nocne cykady około −26 dBFS, liście około −30 dBFS. Naturalnie, bez horrorowego basu.
- **3:00:** trzask gałęzi na ruchu kamery; dokładnie wtedy szelest ustaje.
- **3:35:** jeden krótki VINE BOOM na ujawnieniu chwytu. Bez kolejnych boomów — powtórzenia osłabiłyby pierwszy.
- **Po każdym pytaniu:** prawdziwa cisza, nie „cichy ambience”. Najważniejsze pauzy: 0,30 s po pytaniu pierwszym, 0,55 s przed pytaniem drugim, 0,15 s przed „Józek...” i 0,20 s przed puentą.
- **„Józek...” w k04:** segment odseparowany od głosu Tomka i podniesiony wariantem A do ok. 400 Hz, bez zmiany tempa; lekko zduszony, urwany, dochodzący z góry.
- **Ostatnie ściśnięcie:** pojedyncze skrzypnięcie gałęzi lub ściśnięcie materiału, krótkie i suche. Bez odgłosów slapstickowej sprężyny.
- **Puenta k06:** czyste audio z batchowego k06, dwa warianty pitch-upu odsłuchane na całym zdaniu, ponieważ źródło ma 145 Hz i wcześniejsze ×1,7 da tylko około 247 Hz. Wygrywa wariant naprawdę piskliwy, ale jeszcze czytelny. Głos z góry, centralnie z lekkim pogłosem sadu; żadnego ruchu ust Tomka.
- **Koniec:** po słowie „wsi!” twarde cięcie. Bez śmiechu z puszki, cymbałków i dopowiadającego efektu.

## WERDYKT S1–S4

- **S1 — ZGODA.** Beat ataku jest konieczny; trzask → ustanie szelestu → shake → VINE BOOM → chwyt tworzą brakujące połączenie przyczynowe za $0.
- **S2 — ZGODA.** Audio k05 nad szybkim Ken Burnsem zaakceptowanego chwytu jest komediowo i narracyjnie lepsze niż obraz gapowicza.
- **S3 — ZGODA.** Grobową grę można odzyskać montażem jako mock-seriousness, pod warunkiem że rytm, cisze, pisk i kolorowe napisy są traktowane jako konstrukcja żartu, a nie dekoracja.
- **S4 — ZGODA Z KOREKTĄ.** Rdzeń powinien mieć około 17,35 s, a z krótkim intro i outro około 18,6 s; nie wolno rozciągać sześciu pełnych klipów do ich surowych długości.

## BRAKI

Poza zatwierdzonym planem **niemego k06 za $0.64 nie brakuje żadnego płatnego materiału**.

K01–k04, audio k05, zaakceptowane kadry 2K, czysta puenta z batchowego k06, intro, outro i materiał do darmowych SFX wystarczają. Nie potrzeba nowego k05, nowych kadrów ani nowych generacji postaci. Budżet końcowy: **$11.73/12**.
=========== KANON AUTORA ===========
# KANON odcinka #10010 — "Kiedy złapiesz złodzieja jabłek" (remake żartu Niemowa)
# Źródło: Tomasz, czat 26.07.2026, WKLEJONY SCENARIUSZ — DOSŁOWNIE.
# Komenda: "Idź naszą drogą!" (produkcja wg DROGA_ROLKA_HUMOR)
# UWAGA: ten sam żart co ZAMROŻONY #10004 (chattr +i) — 10004 NIE RUSZAĆ.

Scenariusz do wygenerowania w AI (Reel 15-20 sek.)
Tytuł/Tekst na ekranie (do dodania w montażu): Kiedy złapiesz złodzieja jabłek... 🍎
🌳 Scena 1: Zasadzka
Czas trwania: 3 sekundy
Prompt Video/Image (ENG): Cinematic wide shot, dark apple orchard at night, illuminated by moonlight. A grumpy middle-aged gardener in a flat cap is hiding in the bushes, looking off-camera with intense focus, fog, moody lighting, highly detailed, photorealistic, 4k.
Ruch kamery (Motion Prompt): Slow zoom in on the gardener's face.
Audio (SFX): Dźwięk cykad, ciche szeleszczenie liści.
⚡ Scena 2: Atak
Czas trwania: 2 sekundy
Prompt Video/Image (ENG): Dynamic action shot, low angle. The angry gardener rushes forward and reaches down aggressively with one hand out of the lower frame, night setting, motion blur, intense atmosphere.
Ruch kamery (Motion Prompt): Fast camera shake, dynamic zoom.
Audio (SFX): Głośny trzask gałęzi, nagły dźwięk "bass drop" / "vine boom". Szelest ustaje.
🗣️ Scena 3: Pierwsze pytanie
Czas trwania: 3 sekundy
Prompt Video/Image (ENG): Close-up portrait of the angry gardener talking aggressively, shouting, night orchard background, dramatic cinematic lighting, deep shadows.
Ruch kamery (Motion Prompt): Slight handheld camera movement.
Dialog (Voice AI - PL):
Tekst: "Gadaj, ktoś ty?!"
Emocja (TTS): Głośno, agresywnie, stanowczo. Zwykły, niski męski głos.
😧 Scena 4: Ból w milczeniu i drugie pytanie
Czas trwania: 4 sekundy
Prompt Video/Image (ENG): Close-up portrait of a young rustic man (the thief). His face is distorted in extreme pain, eyes bulging wide, mouth open trying to scream but no sound comes out, comedic exaggeration, sweaty forehead, moonlit.
Ruch kamery (Motion Prompt): Slow tilt up, character's face shaking slightly from pain.
Dialog (Voice AI - PL):
Tekst: "Gadaj, pókim dobry, ktoś ty?!"
Emocja (TTS): Głos ogrodnika zza kadru (Voiceover). Mówiony przez zaciśnięte zęby, jeszcze bardziej wściekły, powolny i groźny.
💢 Scena 5: Ostatnie ściśnięcie
Czas trwania: 3 sekundy
Prompt Video/Image (ENG): Extreme close-up of the gardener's face. He is furious, veins popping on his forehead, he makes a hard clenching motion with his jaw, absolute anger.
Ruch kamery (Motion Prompt): Quick zoom in on the gardener's eyes.
Dialog (Voice AI - PL):
Tekst: "No gadaj draniu, ktoś ty?!"
Emocja (TTS): Krzyk, maksymalna wściekłość i zniecierpliwienie.
🎭 Scena 6: Puenta (Józek)
Czas trwania: 4 sekundy
Prompt Video/Image (ENG): Extreme close-up of the young rustic man's face (the thief). He looks like he is about to pass out, tears in his eyes, face extremely red, absolute agony, comical expression.
Ruch kamery (Motion Prompt): Static shot, character slowly blinking in pain while speaking.
Dialog (Voice AI - PL):
Tekst: "To ja... Józek... niemowa ze wsi!"
Emocja (TTS): To najważniejszy element. Wygeneruj głos, który jest niezwykle piskliwy, nienaturalnie wysoki, zduszony i łamiący się (jak po wciągnięciu helu lub przy zgnieceniu krtani). Musi brzmieć jak wyciśnięty z resztek sił.
