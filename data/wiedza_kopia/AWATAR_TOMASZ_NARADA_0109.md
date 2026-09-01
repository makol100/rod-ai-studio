ODPOWIEDŹ: do zbudowania wiarygodnego awatara Tomasza potrzebujemy od Tomasza 12 zdjęć, jednego 5-minutowego nagrania głównego, jednego 2-minutowego ujęcia bocznego, 60 minut czystego polskiego głosu oraz pięciu decyzji redakcyjno-bezpieczeństwowych opisanych w punkcie 3. Moja rekomendacja: HYBRYDA, nie pełne zastąpienie Izabeli. Prawdziwy Tomasz powinien mówić w sprawach pieniędzy, bezpieczeństwa i decyzji zarządu; Izabela zostaje jawną klamrą serii; awatar Tomasza można dopuścić tylko do zatwierdzonych, rutynowych komunikatów z widocznym napisem „CYFROWY AWATAR TOMASZA — TREŚĆ ZATWIERDZONA”.

## POTWIERDZONE

### 1. Technologia 2026 — droga główna

| rozwiązanie | wejście i ograniczenia | koszt aktualny | werdykt dla Tomasza |
|---|---|---:|---|
| Kling AI Avatar v2, obecny kanon | 1 obraz + audio 2–60 s; nie trenuje osobistej mimiki i nie wymaga zgody tożsamości w samym endpointcie | Standard $0,0562/s; Pro $0,115/s | Dobre dla jawnej postaci AI, za słabe jako jedyny dowód tożsamości prezesa znanego osobiście. 60–90 s trzeba dzielić na klipy. [fal](https://fal.ai/models/fal-ai/kling-video/ai-avatar/v2/pro) |
| HeyGen Digital Twin / Avatar IV–V | Digital Twin: ciągłe nagranie; FAQ wskazuje co najmniej 2 min i zaleca do 5 min, min. 1080p/30 fps; obowiązkowe nagranie zgody. Avatar V może korzystać z krótkiej referencji ruchu, ale płaci się za każdą minutę | Creator $29/mies., 600 kredytów; Avatar IV Video Look 31 kred./min, Avatar V 48 kred./min | Najlepszy kandydat do bezpłatnego pilota funkcjonalnego, bo plan Free obejmuje 1 custom video avatar i 3 filmy do 1 min; do produkcji miesięcznej potrzebny plan płatny. [nagranie](https://help.heygen.com/en/articles/12089286-create-your-first-digital-twin-video-avatar-with-avatar-iv), [cennik](https://www.heygen.com/pricing), [kredyty](https://help.heygen.com/en/articles/15126059-how-to-use-credits-on-heygen) |
| Synthesia Personal Avatar | wersja wideo: 1–5 min, jeden niecięty take, jedna osoba; zgoda nagrywana na żywo przez tę samą osobę; jeden kąt kamery. Wersja ze zdjęcia: 1 zdjęcie, lecz producent wprost mówi, że ruch nie odtwarza sposobu poruszania się właściciela | Starter $29/mies. i 10 min, ale 1 Personal Avatar jest wyraźnie gwarantowany przy Starter rocznym; Creator $89/mies., 30 min i 5 Personal Avatars | Bezpieczna organizacyjnie, lecz wariant ze zdjęcia odpada dla Tomasza; sens ma tylko avatar z wideo. Miesięczny dostęp do personal avatar bez rocznej umowy najpewniej wymaga Creator — UI konta musi to potwierdzić przed zakupem. [wymagania](https://docs.synthesia.io/docs/personal-avatars), [cennik](https://www.synthesia.io/pricing) |
| Hedra Character 3 | 1 obraz + wymagane audio + prompt; maks. 10 min; 540p/720p/1080p | $0,025/$0,05/$0,0625 za sekundę, czyli $1,50–$5,625 za 60–90 s | Ta sama wada co Kling: animuje portret, nie uczy się osobistej mimiki Tomasza. Nadaje się do jawnej postaci AI, nie jako domyślny prezes. [Hedra](https://www.hedra.com/models/video/hedra/character-3) |
| Veo 3.1 z referencjami | do 3 obrazów referencyjnych, generacyjne klipy 8 s; Google przyznaje, że naturalna, spójna mowa pozostaje obszarem rozwoju | Fast z audio: $0,10/s 720p, $0,12/s 1080p; Standard $0,40/s 720/1080p | Nie jest trwałym „klonem prezesa”. Osiem osobnych generacji dla 60 s zwiększa ryzyko zmiany twarzy, głosu i mimiki. [dokumentacja](https://ai.google.dev/gemini-api/docs/video), [cennik](https://ai.google.dev/gemini-api/docs/pricing) |

Praktycy nie dają podstawy do obietnicy „niewykrywalnego klona”. W sponsorowanym materiale twórczyni pokazuje użyteczny workflow HeyGen, ale sama deklaruje sponsoring; niezależny tester opisuje Avatar IV jako najlepszy przez niego używany talking head poza studiem, lecz nadal widzi około dziesięciosekundowe fragmenty, w których lip-sync zdradza AI. To jest dokładnie próg ryzyka przy widzach znających Tomasza. [YouTube — oznaczony sponsoring](https://www.youtube.com/watch?v=JXTqQJNu1w4), [test praktyka](https://taskfirstai.com/blog/heygen-review).

### 1A. Open source i fal.ai — droga zapasowa

| rozwiązanie | stan potwierdzony | koszt / realność na naszym VPS |
|---|---|---|
| OmniHuman 1.5 na fal.ai | 1 zdjęcie + audio + prompt; 720p do 60 s, 1080p do 30 s | $0,16/s: $9,60 za 60 s, $14,40 za 90 s. Nie jest self-hostingiem ani osobistym treningiem mimiki. [fal](https://fal.ai/learn/devs/omnihuman-15-user-guide) |
| InfiniteTalk open source | obraz lub wideo + audio; oficjalny kod opiera się na Wan2.1-I2V-14B, CUDA 12.1, xformers/flash-attn i opisuje tryby jednej lub 8 kart GPU; autorzy ostrzegają o zmianie koloru i spadku zachowania ID ponad 1 min | Nasz VPS ma 12 CPU, 22 Gi RAM i tylko Virtio GPU, bez NVIDIA/CUDA. Nie ma potwierdzonej ścieżki CPU ani czasu generacji, więc lokalnie: NIE WIEM, czy w ogóle zakończy 60 s; produkcyjnie nie przyjmuję. [repo](https://github.com/MeiGen-AI/InfiniteTalk) |
| InfiniteTalk na fal.ai | 1 obraz + tekst/głos w endpointcie single-text | $0,20/s, a 720p kosztuje 2×: co najmniej $12–$18 za 60–90 s przed dopłatą za 720p. [fal](https://fal.ai/models/fal-ai/infinitalk/single-text) |
| LivePortrait | obraz/wideo źródłowe + driving video; to przeniesienie ruchu aktora, nie TTS→pełna osobista mimika. Repo zaleca frontalną neutralną pierwszą klatkę driving video i ma ścieżki CUDA; Apple Silicon jest według autorów około 20× wolniejszy niż RTX 4090 | Bez GPU nie mamy benchmarku. Co ważniejsze, ktoś musi dostarczyć driving video do każdego komunikatu, więc narzędzie nie zastępuje nagrywania Tomasza. [repo](https://github.com/KlingAIResearch/LivePortrait) |
| LatentSync | lip-sync istniejącego ujęcia | Odrzucony przez Tomasza: „zdjęcie które rusza ustami”. Nie wraca do rekomendacji. Ślad: `wiedza/archiwum/DECYZJE_AWATAR.md:18`. |

### 2. Głos Tomasza po polsku

1. ElevenLabs Instant Voice Clone: 1–2 min czystego, pojedynczego głosu; nie przekraczać 3 min, bo może pogorszyć wynik; MP3 co najmniej 128 kb/s, rekomendowane 192 kb/s. Starter kosztuje $6/mies. i zawiera IVC. To szybki odsłuch, nie finalny klon dla ludzi znających Tomasza. [IVC](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning), [cennik](https://elevenlabs.io/pricing)

2. Professional Voice Clone: minimum 30 min, producent zaleca co najmniej 60 min, optymalnie 2–3 h; jeden głos, bez pogłosu i muzyki; weryfikacja głosu nagrywana przez właściciela. Polski jest obsługiwany. Wymaga Creator $22/mies. (promocja pierwszego miesiąca może pokazywać $11; cena bazowa to $22). [PVC](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning)

3. fal.ai potwierdza TTS Eleven v3 za $0,10/1000 znaków i przyjmuje głosy wbudowane/voice ID, lecz publiczna strona tego endpointu nie opisuje tworzenia ani weryfikowania PVC. Nie zakładam, że prywatny PVC z konta ElevenLabs zadziała przez fal. Pewna droga: klon i weryfikacja na własnym koncie ElevenLabs, później wywołanie przez ich API. [fal Eleven v3](https://fal.ai/models/fal-ai/elevenlabs/tts/eleven-v3)

4. Open source PL: XTTS ma polski w oficjalnym artykule (198,8 h polskich danych); Fish S1 deklaruje polski; istnieje społecznościowy F5-TTS Polish, ale karta ma 3 polubienia i brak niezależnego testu podobieństwa do realnego Polaka. To dowodzi dostępności, nie jakości wystarczającej dla Tomasza. [XTTS](https://www.isca-archive.org/interspeech_2024/casanova24_interspeech.pdf), [Fish](https://docs.fish.audio/developer-guide/models-pricing/models-overview), [F5-TTS Polish](https://huggingface.co/Sticzu/marek-f5tts-polish)

5. Koszt TTS na fal przy tempie kanonicznym 15 znaków/s: 60–90 s to około 900–1350 znaków, więc $0,09–$0,135. To koszt samego audio. PVC dolicza plan $22/mies. Ślad tempa: `wiedza/IZABELA_KANON_0.1.md:78`; cena: fal wyżej.

### 3. Co dokładnie ma dostarczyć Tomasz

#### Teraz — bank obrazu i wideo

1. Zrób 12 zdjęć tylnym aparatem Fold7, bez trybu portretowego i bez filtrów: 5 neutralnych (front, lewy/prawy półprofil 45°, lewy/prawy profil), 4 mimiki (naturalny uśmiech z zamkniętymi ustami, uśmiech z widocznymi zębami, powaga, lekkie zdziwienie) oraz 3 kadry od pasa w górę z naturalnymi gestami. Każde co najmniej 4K, ostre oczy, aparat na wysokości oczu, jasne miękkie światło z przodu, nieruchome neutralne tło.

2. Strój ma być taki, w jakim działkowcy rozpoznają prezesa, bez drobnych pasków i dużych napisów. Okulary: jeśli Tomasz zwykle w nich występuje, nagranie główne robi w okularach po usunięciu odbić; dodatkowo 6 zdjęć w okularach i 6 bez. Nie każę zdejmować ich zawsze — to zmieniłoby rozpoznawalny wygląd.

3. Nagraj jeden ciągły film 5:00, 4K/30 fps, tylną kamerą, pion 9:16, statyw, kadr od pasa w górę. Patrz w obiektyw, nie w ekran. Zacznij 5 s ciszy i neutralnej twarzy; potem mów naturalnie, rób krótką pauzę co 2–3 zdania, nie zasłaniaj twarzy, nie wychodź z kadru. Standard platform to min. 1080p/30 fps; 4K daje zapas do kadrowania. Fold7 potrafi nagrywać tylną kamerą nawet 8K/30 fps, więc 4K/30 mieści się w możliwościach urządzenia. [Samsung](https://www.samsung.com/at/business/smartphones/galaxy-z/galaxy-z-fold7-jetblack-256gb-sm-f966bzkbeue/)

4. Nagraj drugi film 2:00 z kamery przesuniętej około 30° w bok, z tym samym światłem, strojem i głosem. HeyGen traktuje drugi kąt jako opcjonalny materiał zwiększający elastyczność; Synthesia tworzy osobny awatar jednego kąta.

5. Skrypt kalibracyjny ma zawierać zwykły komunikat oraz trudne słowa i liczby: „Nazywam się Tomasz i jestem prezesem Rodzinnego Ogrodu Działkowego imienia Józefa Lompy w Woźnikach. Nasz ogród ma pięćdziesiąt jeden działek. Dzisiaj jest pierwszy września dwa tysiące dwudziestego szóstego roku. Proszę nie wykonywać żadnego przelewu na podstawie samego filmu, wiadomości ani telefonu. Oficjalne decyzje finansowe zarządu potwierdzamy osobnym, podpisanym komunikatem.” Potem opowiedz 3 min własnymi słowami o pracy elektryka, Austrii i ogrodzie; modele uczą się także tempa, akcentu i oddechu.

#### Później — osobne audio i decyzje

1. Nagraj 60 min polskiej mowy w 4 plikach po 15 min, tym samym mikrofonem i w tym samym pomieszczeniu. MP3 192 kb/s lub więcej; jedna osoba; bez radia, wentylatora, pogłosu i obróbki „odszumiającej”. Mikrofon około dwóch pięści od ust; poziom równy, bez przesteru. To spełnia zalecenie PVC „co najmniej godzina”, ale nie optimum 2–3 h.

2. Zaakceptuj osobno nagranie zgody HeyGen/Synthesia i weryfikację głosu ElevenLabs. Tych kroków nikt z załogi nie może zrobić za Tomasza.

3. Wybierz wygląd: codzienny prezes w ogrodzie, prezes przy stole zarządu albo neutralne studio. Rekomenduję codzienny, rozpoznawalny strój i prawdziwy ogród jako środek rolki; syntetyczna postać tylko w klamrze.

4. Wybierz formułę wypowiedzi: przy osobistej, wcześniej zatwierdzonej wypowiedzi „Ja, Tomasz…”; przy komunikacie organu „Zarząd ROD informuje…”. Awatar nie może sam przypisywać Tomaszowi opinii ani mówić „ja prezes” w tekście, którego Tomasz nie zatwierdził.

5. Zatwierdź zasadę publikacji: jawna etykieta przez cały klip, osobista akceptacja obrazu, głosu i tekstu przed każdym postem oraz bezwzględny zakaz tematów finansowych, kodów, haseł, nagłych wypadków i próśb „prezes prosi”.

### 4. Prawo i bezpieczeństwo

1. AI Act art. 50 ust. 4 obejmuje obraz, audio lub wideo przypominające istniejącą osobę i mogące wyglądać autentycznie. Wdrożeniowiec ma ujawnić, że treść została wygenerowana lub zmanipulowana. Własny wizerunek i zgoda Tomasza nie wyłączają obowiązku. Art. 50 stosuje się od 2 sierpnia 2026 r. Ustawa nie mówi „w pierwszych dwóch sekundach”; to proponowana przez nas mocniejsza praktyka. [tekst UE](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=pl)

2. Meta zmieniła nazwę „Made with AI” na „AI info”. Etykietuje realistyczne treści, gdy wykryje sygnały techniczne albo gdy autor sam je zgłosi; treść wysokiego ryzyka może dostać mocniejszą etykietę. Przy publikacji zaznaczamy AI ręcznie i dodajemy własny widoczny napis. [Meta](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/)

3. Statut PZD nie zawiera reguły „awatar wolno/nie wolno”. Potwierdza natomiast, że zarząd ROD reprezentuje PZD w sprawach zwykłego zarządu, a oświadczenia woli składa prezes łącznie z innym członkiem. Awatar jest nośnikiem, nie organem i nie podpisem. Komunikat zarządu musi najpierw powstać i zostać zatwierdzony właściwym trybem. [PZD §72–73](http://pzd.pl/ogrody.html)

4. Ryzyko jest realne: raport IC3 za 2025 r. odnotował 22 364 zgłoszenia zawierające informację o AI i straty ponad $893 mln; opisuje klonowanie głosu do poleceń przelewu oraz straty ponad $30 mln w oszustwach BEC z AI. To dane zbiorcze, nie sam głos. FTC ostrzega, że krótki klip z internetu może wystarczyć do klonowania głosu i zaleca oddzwonienie na znany numer oraz pytanie, na które zna odpowiedź tylko prawdziwa osoba. [FBI/IC3 2025](https://www.fbi.gov/file-repository/2025_ic3report.pdf), [FTC](https://consumer.ftc.gov/articles/scammers-use-fake-emergencies-steal-your-money)

5. Zabezpieczenia: nie publikować plików treningowych, voice ID ani kluczy API; klon przechowywać na koncie Tomasza z MFA; na kanale opublikować stałą regułę „ROD nigdy nie prosi o przelew/kod przez film, telefon ani komunikator”; każdą sprawę finansową potwierdzać oddzwonieniem na znany numer i podpisanym komunikatem dwóch uprawnionych osób; utrzymywać znak wodny i publiczny rejestr oficjalnych filmów. „Sekret rodzinny” może być dodatkowy, ale nigdy nie wolno go wypowiedzieć ani wpisać w publicznym materiale.

### 5. Zaufanie widzów

Badanie CHI 2026 przeprowadziło dwa prerejestrowane eksperymenty online na łącznie 2000 osobach. Retusz, wymiana tła i awatary obniżały deklarowane zaufanie i pewność ocen, szczególnie gdy część rozmówców używała awatara, a część nie; trafność rozpoznawania kłamstwa się nie zmieniła. To nie dowodzi konkretnego spadku procentowego w Woźnikach, lecz obala tezę, że większe podobieństwo automatycznie podniesie wiarygodność. [CHI 2026](https://arxiv.org/abs/2603.18868)

Moja kolejność zaufania dla komunikacji ROD jest więc następująca: prawdziwe nagranie Tomasza > jawna Izabela oparta na prawdziwym materiale z ogrodu > jawny awatar Tomasza > awatar Tomasza udający prawdziwe nagranie. Ostatni wariant jest jednocześnie prawnie i reputacyjnie najgorszy.

### 6. Kosztorys bez wydawania pieniędzy

| wariant | aktywo / abonament | koszt awatara na 60–90 s | koszt przy obecnej klamrze 12,9 s |
|---|---:|---:|---:|
| obecna Izabela, Kling Standard + fal TTS | istniejące aktywa | $3,372–$5,058 + $0,09–$0,135 TTS | $0,725 + $0,0194 TTS |
| obecna Izabela, Kling Pro + fal TTS | istniejące aktywa | $6,90–$10,35 + $0,09–$0,135 TTS | $1,4835 + $0,0194 TTS |
| Tomasz, HeyGen Avatar IV Video Look | $29/mies., 600 kredytów; voice clone w planie | 31–46,5 kredytu; do 19,35 min/mies. przy samym IV Video Look | 6,665 kredytu |
| Tomasz, HeyGen Avatar V | ten sam plan, jeśli funkcja jest dostępna na koncie | 48–72 kredyty; do 12,5 min/mies. | 10,32 kredytu |
| Tomasz, ElevenLabs PVC + dowolne wideo | $22/mies. za Creator, 121 tys. kredytów | audio około $0,09–$0,135 na fal albo z puli EL; wideo osobno | klon głosu jest kosztem aktywa, nie wolno go dopisywać w całości do każdego odcinka |

Obecna Izabela nie kosztuje $10,20 za odcinek: to byłoby 60 s OmniHuman po $0,17/s, którego kanon nie używa. Kanon używa Klinga i pokazuje postać tylko 7,6 + 5,3 = 12,9 s; ślad: `wiedza/IZABELA_KANON_0.1.md:54,126,180` oraz `wiedza/archiwum/DECYZJE_AWATAR.md:18`.

Jednorazowy koszt przygotowania przed testami wynosi dziś $0, bo zdjęcia, wideo i audio nagra Tomasz Foldem, a niczego nie kupujemy. Jeżeli Tomasz później zatwierdzi test płatny, minimalna ścieżka miesięczna to HeyGen Creator $29 z jego wbudowanym voice clone; ścieżka z osobnym ElevenLabs PVC to $51 za pierwszy pełnopłatny miesiąc przed podatkami. Testy generacyjne i poprawki mają nieznany koszt, dopóki nie ustalimy liczby prób — NIE dopisuję fikcyjnego ryczałtu.

### 7. Rekomendacja Klaudka

HYBRYDA.

1. Izabela zostaje jawną prezenterką-klamrą cyklu; jej sztuczność jest elementem kanonu, więc widz nie porównuje jej z żywym pierwowzorem.

2. Tomasz raz w miesiącu nagrywa prawdziwe 10–20 s intro albo występuje realnie przy sprawach zarządu. To daje widzom okresowy, niepodrabialny punkt odniesienia mimiki i odpowiedzialności.

3. Awatar Tomasza dostaje wyłącznie krótkie, rutynowe przypomnienia, gdy prawdziwe nagranie jest niemożliwe; zawsze ma etykietę AI i link do oficjalnego tekstu.

4. Awatar nie mówi o opłatach, przelewach, bezpieczeństwie, sporach, uchwałach ani nagłych wypadkach. Te sprawy przekazuje prawdziwy Tomasz albo podpisany komunikat zarządu.

5. Po zebraniu materiału robimy najpierw test bezpłatny i ślepy odbiór przez 3–5 osób, które znają Tomasza; pytamy osobno o twarz, głos, mimikę i zaufanie. Dopiero wynik pozwala Tomaszowi zdecydować o jakimkolwiek płatnym pilocie.

## HIPOTEZY I ROZBIEŻNOŚCI

1. Genek w pierwszym głosie także wybrał HYBRYDĘ, ale podał nieaktualne „15 min” HeyGen Creator i błędnie porównał Izabelę do OmniHuman. Aktualny cennik mówi 600 kredytów, a użycie zależy od modelu: IV Video Look 31/min, V 48/min. Jego koszt Izabeli odrzucam.

2. Belzebub rekomenduje TAK i twierdzi, że klon realnej osoby może podnieść wiarygodność. Nie podał źródeł, konkretnych wejść ani cen, więc ten wniosek pozostaje hipotezą i jest sprzeczny z badaniem CHI 2026.

3. Nie da się z dokumentacji przewidzieć, czy polska wymowa nazw „Woźniki”, „Józefa Lompy”, „ROD” i nazwisk będzie wystarczająca. Rozstrzygnie wyłącznie odsłuch testu przez Tomasza i osoby znające jego głos.

4. Henio także rekomenduje HYBRYDĘ: Izabela do Wiadomości, prawdziwe intro Tomasza raz w miesiącu, awatar Tomasza tylko jako zapas. Jego zdanie „Meta ZABRANIA deepfake'ów” jest błędne: oficjalna polityka mówi o etykietowaniu i pozostawianiu treści, o ile nie łamie innych zasad. Jego kosztorys $0,7–$3,3 dla około 20 s nie wskazuje modelu i nie zgadza się z ceną Kling Pro/Standard; nie używam go.

5. Zenek nie oddał opinii. Dwie próby zakończyły się tym samym błędem inicjalizacji Codex CLI: `Read-only file system (os error 30)`. `zenek.txt` jest protokołem braku głosu, nie głosem za ani przeciw.

## NIE WIEM

1. NIE WIEM, czy HeyGen Avatar V odtworzy charakterystyczną mimikę Tomasza wystarczająco dobrze; nie wykonano testu i nie wolno obiecać tego z demo producenta.

2. NIE WIEM, czy prywatny ElevenLabs PVC można bezpośrednio użyć w endpointcie fal.ai; publiczna dokumentacja fal tego jednoznacznie nie potwierdza.

3. NIE WIEM, ile prób i poprawek przejdzie bramkę oka ani jaki będzie finalny jednorazowy koszt testów.

4. NIE WIEM, jak dokładnie działkowcy ROD Woźniki ocenią awatar; badanie CHI nie obejmowało tej społeczności.

5. NIE WIEM, czy miesięczny Synthesia Starter pozwoli utworzyć Personal Avatar; oficjalny cennik gwarantuje go przy Starter rocznym, a miesięczny Creator podaje 5.

KLAUDEK

KONKRETNA RZECZ DO ZROBIENIA: Tomasz ma najpierw wybrać jeden z trzech zakresów — „pełne zastąpienie”, „hybryda” albo „zostaje Izabela”; rekomenduję odpowiedź jednym słowem: HYBRYDA.
