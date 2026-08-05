# NAUKI — lekcje z produkcji (destylat)

## Obrazy / prompty
- **Kotwica przedmiotu**: opis samych cech ("przygaszona biel, pęknięcia") to za mało —
  Gemini zrobił z mydła cegłę. Zawsze nazwać przedmiot wprost i kontrastem:
  "klasyczne szare mydło do prania, z wytłoczonym napisem — NIE cegła, NIE kamień".
- **Akcja NA DZIAŁCE**: Bielik bez reguły przenosi akcję do kuchni/doniczki. Reguła
  w PROMPT_TEMPLATE_CZYSTY (14.07): grządki/altana/alejki, nigdy mieszkanie/parapet.
  Widz-działkowiec musi zobaczyć SWÓJ świat.
- **"Lektor patrzy w kamerę" w UJĘCIU** = przypadkowy człowiek na obrazie. Wycinać.
- Pętla powtórzeń Bielika (to samo zdanie ×20) zdarza się w promptach — wykrywać
  (zdanie >40 zn. powtórzone ≥3×) przed wysłaniem do fal.ai.
- ŻADNYCH napisów do namalowania: "wiadro z napisem X", kartony Z ETYKIETĄ, kalendarze
  z datą — Gemini psuje polskie napisy. Karton mleka = "gładki, bez etykiety".
- "Kolaż/trzy rośliny" → Gemini robi panele z ramkami i podpisami. Pisać: "JEDEN spójny
  kadr, bez podziału na panele, bez ramek, bez napisów".
- Fizyka kadru musi się spinać: konewka "stojąca obok" nie może jednocześnie "lać wody
  pod łodygi" — Gemini namaluje lewitujący strumień. Jedna akcja, jeden wykonawca.

## Merytoryka (botanical accuracy)
- Bielik WYMYŚLA liczby, których nie ma w źródle: "1 kostka mydła na litr" = 5-10×
  za stężone (poprawnie 10-20 g/l — poparzy rośliny). Proporcje/dawki ZAWSZE sprawdzać.
- Bielik wymyśla też zachowania zwierząt (turkuć "skaczący po liściach" — turkuć kopie).
  Wątpliwy temat → dezaktywować, nie publikować.
- Odbiorcy to doświadczeni działkowcy — rozpoznają fałsz natychmiast. Checkpoint
  istnieje właśnie po to; złapał kostkę-truciznę zanim poszła do 25 tys. ludzi.

## Lektor (TTS)
- Liczby w LEKTORZE ZAWSZE słownie z polską gramatyką: "dziesięć minut", "co trzy dni",
  "dziesięć razy tańsze", "jeden do dziewięciu". Cyfry i skróty (10 minut, 3 dni, 10x,
  1:9) Marek czyta bezsensownie. Reguła wpisana w 3 szablony Bielika + prompt pomocnika
  Claude + audytora Fable (14.07). Opublikowana 000093 ma jeszcze "10x" — świadomie
  zostawiona (koszt podmiany posta > zysk).
- Edycja SAMEGO lektora nie wymaga przeliczania promptów obrazów — edytować scenes.txt
  bezpośrednio na dysku, potem tylko audio+napisy+render (patch).

## Tryby i pipeline
- **ZAWSZE tryb_jezykowy="czysty_bielik"** przy odpalaniu przez API (wpadka 000092:
  "pl" = stary szablon + prompty Qwenem po angielsku).
- Endpoint /reel-checkpoint/zapisz sam przelicza prompty po zmianie scenariusza —
  ale synchronicznie (~10 min Bielikiem); prompts.txt nadpisuje się NA KOŃCU.
  Czytanie po 60 s = stary plik. Czekać na zmianę mtime.
- Status.json nie zawsze nadąża za logiem (etap "sceny" gdy lecą prompty) —
  prawdę mówi /live-log.

## Czas/UI
- Timestampy serwera są UTC BEZ "Z" — JS czyta je jako czas lokalny (licznik kłamał
  o 2 h). Zawsze doklejać "Z" przy parsowaniu w przeglądarce.
- Bielik/Qwen na CPU: artykuł ~1 min, sceny ~2 min, prompty 9 szt. ~10 min,
  Qwen thinking ~11 min. 1100% CPU = pracuje, nie wisi.

## Android/telefon
- Chrome Tomasza wiesza pobrania z GitHuba na 100% ("Pobieram...") — dystrybucja
  przez GET /apk z własnego serwera.
- Google Files otwiera APK jak ZIP — instalować przez Moje pliki (Samsung).
- Kopia WhatsApp domyślnie BEZ filmów ("Dołącz filmy" off) — media z czatu
  nie są backupem.
- WorkManager: min. 15 min interwału; Samsung ubija tło → bateria "bez ograniczeń".

## Facebook/prawo
- Grup prywatnych FB NIE scrapować (blokada konta) — sygnał liczyć z danych
  zastępczych (pogoda → barometr).
- CC BY wymaga atrybucji przy KAŻDEJ publikacji (Tomasz akceptuje tylko YT — poinformowany).
- Film "niepubliczny" ≠ "na kanale" — w CTA zawsze "link w opisie".

## Audytor checkpointu (od 14.07 wieczór)
- Przycisk "Sprawdź automatycznie" = Claude Fable 5 (API, grosze/audyt; fallback Qwen
  przy braku klucza). System prompt = lista 10 grzechów Bielika (działka, dawki,
  przyroda, cyfry słownie, urwane zdania, absurdy sprzętowe, lektor w ujęciu, napisy,
  powtórzenia, haczyk+pętla) z rozkazem naprawy.
- Pierwszy audyt złapał proporcję czosnku wpisaną przez Claude — audytor pilnuje
  WSZYSTKICH autorów scenariusza, nie tylko Bielika.

## Sesja 15.07.2026 — pilot "Cukinie" (żarty Veo)
- **Weryfikacja wideo = min. 8 klatek/klip** (ffmpeg select+tile 4x2) + transkrypcja Whisper. 1–3 klatki NIE wykrywają błędów przestrzeni i ruchu (2× wpadka). A i tak ruch może dać inną interpretację niż stopklatki — ostatecznym sędzią jest Tomasz.
- **STYL_KLIPU bez opisu miejsca.** Stały opis pleneru w stylu wymuszał ogród w każdej scenie — wnętrza lądowały na podwórku. Miejsce dyktuje OBRAZ sceny: "WNĘTRZE ALTANY, kamera w środku:" / "OGRÓD:".
- **Imię w OBRAZIE = postać w kadrze.** Parser dodaje każdą wymienioną postać do "In frame". Miejsca bez imion ("altana", nie "altana Tomasza"). Logika między klipami: kto się ukrywa, nie mógł być wcześniej widoczny.
- **Zakazane akcje Veo:** pukanie, otwieranie drzwi, precyzyjne gesty dłoni — model je psuje. Zamiast: wołanie, niesienie, kucanie, patrzenie.
- **Cięcie po puencie:** whisper chunks / silencedetect → `-t koniec_mowy+0.5s` per part. Bez cięć żart tonie w martwych sekundach (było 3.5 s gapienia po puencie). Pipeline NADPISUJE final → ręczny montaż (cuts+plansza) powtarzać po KAŻDEJ regeneracji.
- **Dwuznaczny obraz ≠ zawsze dogrywka.** Gdy Veo odjedzie od zamysłu, ale wynik da się obronić lepszą interpretacją (Tomek "uciekł przez okno") — przyjąć ją i przypieczętować opisem posta ($0) zamiast palić $ na kolejne podejście.
- **Opis rolki NIE zdradza gagu.** Streszczenie fabuły w opisie = widz nie musi oglądać (wpadka: "Tomek uciekł przez okno" w 1. linijce). Opis = tease sytuacji wyjściowej; spoiler/interpretacja → przypięty komentarz PO publikacji.
- **Telegram cache'uje wideo po URL.** Ponowna wysyłka z tego samego linku = stary plik z cache (wpadka 10004: gotowy montaż poszedł jako surówka). Każda wysyłka wideo przez webhook MUSI mieć cache-buster `?v={timestamp}` w URL.
- **Negacje w OBRAZIE zakazane.** "Nikogo nie widać" przywołało do kadru postać, której miało nie być (10004 K2 v3, $1.20 w błoto). Modele obrazu nie rozumieją negacji — opisywać pozytywnie, co MA być w kadrze. Reguła w audycie.
- **Pora dnia zawsze wprost w OBRAZIE** ("o zmierzchu"). Bez niej Veo potrafi zacząć klip nocą i skończyć dniem — wewnętrzne cięcie z teleportacją garderoby (10004 K2 v3).

## 17.07 — research praktyków (przed k14, na dyspozycję "odszukaj w necie u ludzi")
- **Jedna akcja na klip** — powtarzane wszędzie: "Veo gets confused with too many
  actions"; sceny atomowe, micro-beats. Wieloczynnościowe klipy = chaos.
- **Front-load**: Veo waży początek prompta — najpierw ujęcie+podmiot+AKCJA, potem
  styl/kamera.
- **Veo 3.1 sam dodaje cięcia i zoomy na twarz**, jeśli nie zakazać wprost — do
  promptów akcji dopisywać: "single continuous take, no cuts, static camera".
- **Gryzienie/jedzenie DZIAŁA w Veo 3/3.1** (test "Will Smith spaghetti" zaliczony,
  komercyjne generatory bite-and-chew na Veo) — ryzyko: przesadnie głośny chrzęst
  w audio → kontrolować w miksie.
- **FLF = interpolacja między klatkami** (potwierdzone przez fal): dwie różne
  kotwice dają płynny, wymuszony ruch — zgodne z naszą lekcją "uścisku".

## 18.07 — DEGENERACJA ŁAŃCUCHA KLATEK (wielka lekcja 10007)
- Łańcuchowanie klipów (start klipu N+1 = ostatnia klatka klipu N) KUMULUJE błędy:
  Veo dostaje skompresowaną klatkę z artefaktami, wzmacnia je i oddaje gorsze —
  "kserowanie kserówki". Zmierzone: kanarek ze świeżego kadru = 38.9 gęstości
  krawędzi; 5. ogniwo łańcucha = 102-107 (tło z liści "ugotowane" w robaczki).
  Praktycy i literatura znają to jako error accumulation przy iteracyjnym
  generowaniu. RECEPTA: każdy klip ze ŚWIEŻEGO kadru; ciągłość robi MONTAŻ
  (sceny z wielu ujęć), nie łańcuch klatek.
- Montaż short-form wg praktyków: ciszę i martwe pozy WYCINAĆ (jump-cuty, rytm
  dialogu A/B to naturalna gramatyka cięcia), cięcia prowadzić audio; crossfade
  0.2s maskuje drobne niespójności; color grade na CAŁOŚCI po sklejeniu (jednolity
  wygląd między generacjami). Hard cut w obrębie dialogu = OK; raziło cofanie
  czasu (powrót do starych klatek) i martwy czas, nie sam brak przejść.

## 18.07 — RYZYKA PRZYSZŁOŚCI (pełna lektura źródeł, nie snippety)
1. TIKTOK WYKRYWA AI SAM: C2PA Content Credentials od 01.2025, >1.3 mld wideo
   oznaczonych automatycznie — wykrycie NIEZALEŻNE od deklaracji twórcy (Veo/Google
   osadza metadane w plikach). Ukrywanie = bez sensu i karalne (auto-label, cięcie
   zasięgu, usunięcie, strajki). Z widocznym labelem: pełna monetyzacja i wg TikToka
   brak wpływu na dystrybucję.
2. TIKTOK — TWARZE REALNYCH OSÓB PRYWATNYCH: synthetic media z realną osobą
   prywatną = BAN CAŁKOWITY, nawet z labelem. Przy nadchodzącej przebudowie
   postaci: Tomek NIGDY dosłowną twarzą Tomasza (kanon "przykład typu" utrzymać
   twardo).
3. YOUTUBE (od 07.2025): czysto-AI bez ludzkiego wkładu = demonetyzacja; ratuje
   "genuine creative value" (autorski scenariusz, montaż, storytelling). Nasza
   polisa = git/DECYZJE/KANON dokumentujące wkład Tomasza. Deklaracja ręczna
   (checkbox), kary za powtarzane braki.
4. PRAWO UE — AI ACT ART. 50 od 02.08.2026 (ZA 2 TYGODNIE): obowiązek ujawnienia
   AI-generacji; "deepfake" szeroko — realistyczne osoby/sceny nawet BEZ intencji
   oszustwa i bez realnego pierwowzoru. Dzieła EWIDENTNIE satyryczne/fikcyjne
   (nasza seria) = reżim lżejszy: wystarczy nieinwazyjne oznaczenie (wzorzec z
   draft Code of Practice: ikona ~5s w wideo), pełnego zwolnienia BRAK. Kary
   teoretyczne do 15 mln EUR/3% obrotu; egzekwują organy krajowe.
5. Marking maszynowy (art. 50(2)) to obowiązek PROVIDERA (Google/fal — C2PA już
   jest); my jako deployer mamy disclosure (50(4)).
6. Monetyzacja TikTok: wideo >1 min (nasze 80-125s OK), 10k obserwujących +
   100k wyświetleń/30 dni — do zbudowania zanim przyjdą pieniądze.
7. Pozostałe (własna analiza): deprecacja/podwyżki modeli (pin wersji + sonda cen
   przy starcie odcinka), spójność postaci po przebudowie (nowa biblioteka od
   zera), audio wyłącznie PD/CC0 (po lekcji werbla), platformowe czystki
   "AI slop" — bronią nas autorski scenariusz i jakość.

## iPXE/netboot.xyz: martwa klawiatura w UEFI (18.07, N150)
Znany bug (ipxe#1746): na czesci firmware AMI klawiatura USB w menu iPXE nie
dziala (strzalki/Ctrl-N gluche), bo prebuilt netboot.xyz nie ma USB_HCD_USBIO.
W BIOS klawiatura dziala, w Linuksie tez — martwa TYLKO w iPXE. Obejscie
uzyte u nas: wlasny build iPXE z EMBED= (zero menu, zero interakcji):
sieć→Alpine netboot→apkovl autorun→instalacja. Wniosek: przy bootowaniu
sieciowym NIE zakladac dzialajacej klawiatury — automat embedded pewniejszy.


## KRYSTYNA / greenworks-optimow — publikacja repo HACS (22.07.2026)
- Integracja kosiarki spakowana jako publiczne repo HACS: **makol100/greenworks-optimow** (droga A). Krok 1 planu (JEDNO gotowe, działające repo — dla nas i do pobrania przez innych) DOMKNIĘTY i zweryfikowany na GitHubie (commit 6006c63).
- const.py zawiera wspólny sekret apki Greenworks (GUC_CLIENT_SECRET, wyciągnięty z APK — NIE konto Tomasza). Email/hasło NIGDY w kodzie — tylko config_flow w runtime (UI).
- LEKCJA FUNDAMENTU: gdy MCP pada, tool_search zwraca tylko część namespace'ów (u nas: sam telefon+Chrome, bez fabryki/HA). Sprawdzić kanał PRZED akcją, nie zakładać że żyje bo żył. Push w martwy kanał = halucynacja "gotowe". Telefon jako plan B na SSH działa tylko gdy host/klucz zapisany (Fold7 nie ma — roboczy SSH to S24).
- ZOSTAŁO (krok 2): wdrożenie na HA Działka (HACS custom-repo + restart + config z creds Tomasza) → mirror-podgląd na HA Dom (token Działki w sesji, bez drugiego logowania do chmury) → usunięcie starego wpisu z Dom.

## 23.07 audyt startu vs Google Veo blog: 5 punktow rozwazonych, WSZYSTKIE odrzucone. "Nic nie wchodzi. Nic nie poprawia w 100% a moze pogorszyc. Mamy wiedze co mozna poprawic jakby cos sie wydarzylo." Szczegoly w pamieci trwalej /areas/fabryka-rolek.md. Droga bez zmian, w dwoch miejscach (domenowe swiatlo, jeden mowca) madrzejsza od poradnika bo oparta na pomiarach. Nie ruszac bez zmierzonego problemu.

- 23.07 USTERKA kanarka do naprawy: --zapis-bank pada w kontenerze (FileNotFoundError /root/rod-ai-studio/wiedza/PROMPTY_WZORCE.md), bo kontener fabryka-api NIE widzi katalogu wiedza/ (repo montowane jako /app, wiedza tylko na hoscie). Obejscie: zwyciezce dopisywac do banku Z HOSTA. Do naprawy: kanarek powinien zapisywac przez sciezke widoczna w kontenerze albo publikacja/zapis-bank ma isc z hosta.
- test hooka 06:55:24

## 04.08.2026 — HENIO ZDLAWIONY PRZEZ WLASNE ZADANIE (5 godzin martwy)

**Objaw:** Henio nie odpowiadal na NIC, nawet na slowo „TEST". Bramka `active`, proces zyje,
silnik DeepSeek sprawdzony osobno — odpowiada w sekunde. Ale ostatnie wywolanie silnika: 10:07,
przez 5 godzin ANI JEDNEGO.

**Prawdziwa przyczyna:** proces `tools/wytnij_izabele.py` (rembg, model birefnet-portrait na CPU)
uruchomiony przez Henia o 11:50 **wisial 2h56min i puchl do 6154 MB**. Klatka pamieci uzytkownika
hermes miala `MemoryHigh=1536M / MemoryMax=2048M` — z czasow probnego dyzuru read-only w lipcu,
NIGDY NIE ZDJETA mimo pelnych praw od 29.07.
Jadro zdlawilo CALA grupe: bramka Henia utknela w stanie `D (disk sleep)`,
stos: `__mem_cgroup_handle_over_high`. **Henio nie padl — zostal uduszony przez wlasne zadanie.**

**Tomasz nazwal to od razu i trafnie:** *„Wycinal, a ty cos innego musiales robic. I sie Henio posral."*
W tym samym czasie Klaudek generowal obrazy u Genka i uruchamial rozpoznawanie twarzy w kontenerze.

**BLAD KLAUDKA — SZUKAL NIE TAM 3 RAZY:**
1. obwinil swoja zmiane `reasoning_effort: high` (00:16) — cofnal, nie pomoglo
2. obwinil `memory_char_limit: 4000000` — cofnal cala konfiguracje, nie pomoglo
3. obwinil plik blokady `MEMORY.md.lock` — odlozyl, nie pomoglo
Dopiero za CZWARTYM podejsciem zapytal `ps -u hermes --sort=-rss` — JEDNO polecenie,
ktore od razu pokazalo winowajce. **Diagnoze zaczynac od pytania „co zjada zasoby",
a nie od „co ja ostatnio zmienilem".**

**NAPRAWA:** klatka podniesiona do `MemoryHigh=6G / MemoryMax=8G`
(`/etc/systemd/system/user-1000.slice.d/pamiec.conf`). Nic nie kosztuje — serwer ma 22 GB,
wolnych bylo 18. Ustawienia Henia przywrocone (tryb wysoki, pamiec 4 mln) — nie byly winne.

**ZASADA NA PRZYSZLOSC:** ciezkie zadania na procesorze (rembg, modele wizyjne) NIE uruchamiac
rownolegle z inna ciezka praca. Przy poprzedniej karcie wycinal Zenek — spoza klatki hermesa,
wiec problem sie nie ujawnil.

## 05.08.2026 — ZERWANIA MOSTU: NIE NASZA WINA, ALE DA SIE ZEJSC Z LINII OGNIA

**Podejrzenie Tomasza:** *„Co jest z tym mostem? Nie zepsułeś go? Działało to bez żadnych zarzutów."*

**ZMIERZONE (dziennik `caddy-mcp`, doba wstecz):**
- `mcp-fabryka.service`: **zero restartow, zero bledow wlasnych**, proces zyje 5 dni,
  obciazenie serwera 0,23. Chodzi w `/system.slice` — **zmiana klatki pamieci z 4.08
  dotyczyla `user-1000.slice` (Henio) i mostu NIE DOTYKA.**
- Zerwania fabryki: **21 w dobe**, komunikat `aborting with incomplete response`,
  czas trwania **0,003 s** — polaczenie ginie natychmiast po nawiazaniu.
  Zrywa adres `160.79.106.x` = **STRONA ANTHROPICA**, nie serwer.
- **Naprawic z naszej strony SIE NIE DA.**

**OSOBNE ZNALEZISKO:** 363 bledy `dial tcp 100.101.116.106:8080 i/o timeout` dotycza
`telefon.157-90-155-155.sslip.io` — Galaxy Z Fold7 jest **offline w Tailscale**.
To nie szkodzi niczemu poza dziennikiem, ale **lacznik do telefonu jest martwy**.

**CO DA SIE ZROBIC — I ZOSTALO ZROBIONE:**
Klaudek odpalal zlecenia zalogi wzorcem `nohup ... & sleep 20-25` i TRZYMAL polaczenie,
czekajac az ruszy. Kazda sekunda to okazja do zerwania, a zerwanie w trakcie = Klaudek
NIE WIE, czy zlecenie wystartowalo.

**`tools/odpal.py`** — odpala i wraca **w 0,08 s** (zmierzone), stan sprawdza sie osobno:
```
python3 tools/odpal.py --zadanie /tmp/x.md --kto zenek,henio --katalog /tmp/x
python3 tools/odpal.py --stan
```
**300 razy krocej trzymane polaczenie.** Nie naprawia zrywania — schodzi mu z drogi.

## 05.08.2026 — NAPRAWIAJAC JEDNO, CICHO ZABRALEM DRUGIE

**Uwaga Tomasza:** *„Powinienem dostać odpowiedź, że są gotowi, przez telegrama."*

**Co sie stalo:** Klaudek napisal `tools/odpal.py`, zeby zlecenia zalogi nie trzymaly
polaczenia MCP (naprawa realnego problemu — 21 zerwan na dobe). Stary wzorzec brzmial:
```
nohup bash -c 'zaloga.py ...; python3 tools/dzwonek.py "gotowe"' &
```
Nowy `odpal.py` uruchamial samo `zaloga.py` — **bez czlonu z dzwonkiem.**
Tomasz przestal dostawac powiadomienia i musial pytac o stan sam.

**To jest ten sam blad, przed ktorym ostrzega dekret Tomasza o teleporcie (26.07):
„wolno dopisac funkcje, NIGDY odebrac podstawowego zadania".**
Klaudek nie zrobil tego zlosliwie — po prostu przepisujac narzedzie od nowa
NIE SPRAWDZIL, co stary wzorzec robil poza tym, co wlasnie naprawial.

**ZASADA:** przepisujac cokolwiek, co dzialalo, najpierw WYPISAC WSZYSTKIE jego funkcje,
dopiero potem pisac nowe. Inaczej naprawa jednej rzeczy jest cicha strata innej.

**Naprawione:** `odpal.py` wysyla dzwonek ZAWSZE po zakonczeniu narady (wbudowane w powloke,
nie doklejane przez wolajacego — zeby nie dalo sie znowu zapomniec).
Test 5.08 09:12: wiadomosc doszla, Tomasz potwierdzil.

## 05.08.2026 — NIGDY NIE GUBIC GODZINY TOMASZA

**Tomasz:** *„U mnie jest 10:39. Poprawić i nigdy nie zgubić mojej godziny."*

**Co bylo zle:** zaczep w moscie i dziennik audytu zapisywaly `datetime.now()` — czyli czas
SERWERA (UTC). W pliku stalo `07:39`, gdy u Tomasza bylo `09:39`. Miedzy soba wpisy zgadzaly sie,
wiec bledu nie widac — **ale przy zestawieniu z decyzjami Tomasza i jego slowami wszystko
wychodziloby przesuniete o 2 godziny.** Hans mial na tym liczyc.

**Poprawione:** `STREFA_TOMASZA = ZoneInfo("Europe/Vienna")` w `mcp_server.py`.
Znacznik ma teraz jawne przesuniecie: `2026-08-05T10:40:46+02:00`.
Poprawione W OBU miejscach — zaczep i `_audit` — zeby w jednym systemie nie bylo dwoch czasow.

**REGULA:** kazdy znacznik czasu, ktory Tomasz zobaczy albo ktory bedzie porownywany
z jego zapisami, **MA BYC W JEGO STREFIE, z jawnym przesunieciem.**
Serwer chodzi na UTC — to jest pulapka, ktora wraca. Sprawdzac przy KAZDYM nowym narzedziu,
ktore cokolwiek datuje.

**Wdrozone ta sama procedura co zaczep:** kopia -> proba na porcie 8799 -> test funkcji ->
podmiana -> restart -> sprawdzenie dostepu. Stara wersja: /tmp/mcp_przed_czasem.py
