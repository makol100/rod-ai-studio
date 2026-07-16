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
