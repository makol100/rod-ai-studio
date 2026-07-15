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

## Merytoryka (botanical accuracy)
- Bielik WYMYŚLA liczby, których nie ma w źródle: "1 kostka mydła na litr" = 5-10×
  za stężone (poprawnie 10-20 g/l — poparzy rośliny). Proporcje/dawki ZAWSZE sprawdzać.
- Bielik wymyśla też zachowania zwierząt (turkuć "skaczący po liściach" — turkuć kopie).
  Wątpliwy temat → dezaktywować, nie publikować.
- Odbiorcy to doświadczeni działkowcy — rozpoznają fałsz natychmiast. Checkpoint
  istnieje właśnie po to; złapał kostkę-truciznę zanim poszła do 25 tys. ludzi.

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
