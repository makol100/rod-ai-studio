# DECYZJE TOMASZA — SERIA HUMOR (obsada, zasady ponadodcinkowe)
Append-only. Najnowszy wpis wygrywa ze wszystkim.
Format: data | DOSŁOWNY cytat | interpretacja (1 zdanie) | status

## 17.07.2026 — obsada stałego duetu serii
- "Ja. To nowa postać. Janusz nowa postać" + "Ja to przykład." + "Ja będę się
  pojawiał w innych scenariuszach." | Bohater serii to postać AI wzorowana na
  Tomaszu jako typie (NIE dosłowna twarz z fotografii); występuje w wielu
  scenariuszach. | OBOWIĄZUJE
- "Ja mam długie włosy spięte zawsze w kucyk" | Znak rozpoznawczy bohatera:
  długie włosy ZAWSZE w kucyku + pełna szpakowata broda, ok. 50 lat. | OBOWIĄZUJE
- "Janusz typowy ogrodowy strażnik przepisów. Szczupły wysoki po sześćdziesiątce"
  | Rysopis bazowy Janusza. | OBOWIĄZUJE
- "To bierzemy siwy wąsik i okulary na sznurku, kamizelka z kieszeniami i notesik
  do spisywania naruszeń, bo Notes będzie używany w innych historiach" | Znaki
  stałe Janusza; notesik = rekwizyt serii, wraca w kolejnych odcinkach. | OBOWIĄZUJE
- "Zapisz postacie i wygeneruj ich podgląd. Chcę ich zobaczyć." | Zapis obsady
  (ten plik + pamięć) i jeden podgląd duetu nano-banana 2K 9:16. | WYKONANE ($0.15, assets/zarty/karty/duet_podglad_v1.jpg)
- "Idealnie" (po obejrzeniu podglądu) | Podgląd duetu ZAAKCEPTOWANY;
  assets/zarty/karty/duet_podglad_v1.jpg = obowiązujący wzorzec referencyjny
  wyglądu OBU postaci dla wszystkich przyszłych generacji. | OBOWIĄZUJE
- "Idziemy dalej" | Zgoda na następny nazwany krok: karty postaci obu bohaterów
  z wzorca duet_podglad_v1.jpg (2 × nano-edit 2K = $0.30) + przygotowanie cięć
  scenariusza "Ślimak nagi" do akceptacji (słowa, $0). | WYKONANE (karty: bohater_karta.jpg, janusz_karta.jpg, $0.30)
- "Robimy profile postaci tak? I generujesz więcej zdjęć do pamięci żeby na
  przyszłość mieć lepsze źródło" | Biblioteka referencyjna per postać: (a) crop-baza
  z zaakceptowanego duetu ($0, kotwica tożsamości), (b) arkusz front/3-4/profil,
  (c) portret NOCNY (seria gra nocą — łata zmierzony słaby punkt: noc vs zmierzch
  sim 0.12); 4 generacje × $0.15 = $0.60; każda referencja z JEDNĄ osobą na wejściu
  (nauka z odrzuconych kart); bramka A automatem PRZED linkami. | WYKONANE ($0.60; bramka A: twarze 3/1/3/1 zgodne, sim 0.50-0.76 vs baza, separacja postaci czysta)
- "Jeżeli to wystarczy do dalszego generowania idziemy dalej jeżeli nie generujemy
  więcej. To się przyda do następnych historii a mam ich z 10" | Werdykt techniczny
  z pomiarów: WYSTARCZY (3 refy/postać w 2 domenach światła; wczoraj 1 ref trzymał
  0.70-0.88). Zasada: nową referencję dokupujemy dopiero gdy historia wprowadza
  nową domenę światła ($0.15 + bramka A). Seria ma ~10 kolejnych historii. | OBOWIĄZUJE
- "Tu musimy to inaczej liczyć. Stworzyliśmy postacie które kosztowały. To trzeba
  odjąć od ceny rolki a zapisać gdzieś gdzie są koszta takie jak postacie itp"
  | Nowe księgowanie: aktywa serii (postacie, biblioteki, banki głosów) idą do
  wiedza/AKTYWA_SERII.md i NIE wliczają się do limitu $6 odcinka; budżet 10005
  liczy się od zera: kadry $0.60 + klipy $5.12 = $5.72 (POD limitem, S5 zostaje,
  force zbędny). | OBOWIĄZUJE
- "Domknij wszystko a potem powiedz czy jest czysto żeby iść dalej" | Domknięte
  i zweryfikowane podwójnie (sesja równoległa commit 45cf694 + moje niezależne
  pomiary): duplikat JÓZEK usunięty (przyczyna kurtki z 16.07), brama językowa
  strażnika działa (cut_05: pl 1.0 PASS; final_k1: sk 0.5 FAIL — "Znovu mi ktos
  jablka podzera" — wczorajszy finał nie przeszedłby dziś), most tmp_weryfikacja
  sprzątnięty, kontener zrestartowany. Poza zamrożonym 10004 repo czyste. | WYKONANE
- "Ja inne okno chatu" | Rozstrzygnięcie zagadki równoległej sesji: to Tomasz
  w drugim oknie Claude'a (komputer). Nocne latentsynci, v6 safety6 i poranne
  domknięcia (commity 45cf694/db5d995) = jego ręka; księga 10004 (15.90) stoi;
  alarm bezpieczeństwa odwołany. Obie sesje czytają DECYZJE + git przed pracą,
  żeby się nie zderzać na tych samych plikach. | ZAMKNIĘTE
- "Bo jest bałagan a potem chujnia" | DROGA podbita do 2.1 — dokument zrównany
  z praktyką i pomiarami (biblioteka referencyjna, lite $0.64 robi finały,
  strażnik języka pl-only, progi kotwic 64px 12/18). | WYKONANE
- "Jaki numer faktyczny numer drogi 2.1, 2.2, 2,3" | Audyt gita: po 2.0 były
  trzy merytoryczne rewizje → faktyczny numer 2.3; nagłówek poprawiony, wstawiony
  CHANGELOG z zasadą "każda merytoryczna zmiana = +0.1 i wpis" — numeracja
  odtąd mechaniczna, z commitami jako dowodami. | WYKONANE
- "Wdrażaj wszystkie 8. Zrób jeszcze raz dokładną analizę żeby nie narobić sobie
  więcej kłopotów a nic to nie da. Sprawdź wszędzie gdzie masz zasięg. Doczytaj
  ludzi bo to oni mówią prawdę" | DROGA 2.4: tarcze przeciwbłędowe wdrożone
  z korektami od praktyków (suite = pas bezpieczeństwa nie dowód, tylko realne
  przypadki, testy fałszywych alarmów, bieg szybki 3 min, lock wygasa po 2h,
  słowa-miny flagują nie blokują). | WYKONANE (commit 6606f61 + suite 8/8 PASS na pierwszym biegu)
- "Jeszcze raz weryfikacja w internecie" | Zweryfikowane: (1) język — zapis kwestii
  po polsku nie wystarcza, do promptu idzie stały opis głosu postaci + native Polish
  accent; (2) kanarek: 1 klip → strażnik → dopiero batch; (3) veo3.1/reference-to-video
  na fal istnieje, $3.20/klip 8s z audio — poza limitem, tylko punktowo za zgodą.
  DROGA podbita do 2.5. GŁOSY duetu do klepnięcia przez Tomasza. | WYKONANE
- "Głos potwierdzam" | Głosy duetu KANON: BOHATER = niski, szorstki, zdecydowany
  męski głos po polsku; JANUSZ = suchy, urzędniczy głos starszego pana.
  Wpisane do GLOSY_VEO w kodzie. | OBOWIĄZUJE
- "Weryfikacja nie twoja halucynacja że jest dobrze!!! Ma iść 1000% pewna rzecz
  w veo!!!" | Bramka PREFLIGHT (tools/preflight.py): automat sprawdza PRZED
  każdym submitem do Veo — kwestia verbatim z kanonu, blok głosu + native Polish
  + no captions w prompcie, jeden mówca, słowa-miny, kadry (istnienie, twarze,
  proporcje), budżet; submit bez zielonego preflight = zakazany. | WYKONANE (15 kontroli; pozytyw ZIELONY, negatyw CZERWONY; złapana dziura mountów wiedza/)
- "Jest bardzo dobrze ale za poważnie jak na żart. Ogólnie jest zajebiście!!!
  Mamy podstawę do produkcji" | NUTA REŻYSERSKA SERII: system produkcji
  potwierdzony jako podstawa (~10 historii); ton przyszłych odcinków grać
  LŻEJ — komediowe przerysowanie i mock-seriousness zamiast serio-powagi;
  moje dyrektywy promptowe ("dramatic", "grave determination", "spy-movie
  tension") grały na serio — do wymiany na komediowe. | OBOWIĄZUJE
- "A gdzie intro i outro?? / Teleport i do second brain" | ZASADA SERII: każdy
  finał humoru dostaje brandowe intro (animowane rod_profilowe) i outro —
  identycznie jak rolki foto (assets/branding/, machineria renderer.py);
  Droga podbita, zasada w pamięci trwałej. | OBOWIĄZUJE

## 17.07.2026 — imiona duetu + zapowiedź przebudowy postaci
- "Ja to Tomek. Janusz to Janusz." | Imiona kanoniczne duetu: bohater (wersja AI
  Tomasza — długie włosy w kucyk + szpakowata broda, ~50 lat) = TOMEK; drugi = JANUSZ.
  Duet debiutuje pod tymi imionami od odcinka 10006 (publikacja dziś). | OBOWIĄZUJE
- "Po opublikowaniu robimy/poprawiamy od nowa dwie postacie. Starego Tomka
  usuniemy. Ale to za chwilę." | Po publikacji 10006: przebudowa OBU postaci od
  zera (nowe referencje/biblioteka); stare assety "starego Tomka" do usunięcia.
  NIE ruszać NICZEGO do osobnej wyraźnej komendy Tomasza ("za chwilę"). | ZAPLANOWANE (po publikacji 10006)

- 17.07 | "Pójdziemy w następny odcinek" | Start prac nad odcinkiem #10007 (10006
  wgrywa ręcznie sam; naprawa auto-publikacji n8n ODŁOŻONA na później). Wybór tematu
  i kolejność względem zapowiedzianej przebudowy postaci — do rozstrzygnięcia. | W REALIZACJI

- 17.07 | "Obecny duet. Czyli Janusz i Tomek." | Odcinek #10007 jedzie na OBECNEJ
  bibliotece referencyjnej duetu (przebudowa postaci ODŁOŻONA — nadal zaplanowana,
  wciąż czeka na osobną komendę). Temat: własny scenariusz Tomasza "Zasada
  spadającego jabłka" (~40s, Tomek=właściciel jabłoni, Janusz=łowca okazji). | OBOWIĄZUJE
- 17.07 | "Zawsze doczytuj co mówią fachowcy z branży. Wydaje swój pomysł ale to
  ich praktyka ich kosztowała. Nas nie musi wcale!" | Zasada ponadodcinkowa →
  DROGA 2.8: research praktyków w sieci OBOWIĄZKOWY przed każdym ryzykownym/nowym
  elementem produkcji; wnioski do NAUK przed wydatkiem. | OBOWIĄZUJE (DROGA 2.8)
- 17.07 | "Widocznie rolka humorystyczne musi kosztować do 12$" + "Czytać!
  Analizować, uczyć się na czyiś błędach to zajebista metoda" | NOWY LIMIT SERII:
  rolka humorystyczna do $12/odcinek (poprzednio $6; powyżej $12 nadal osobny
  force). Metoda researchu branżowego (DROGA 2.8) potwierdzona po efektach. | OBOWIĄZUJE (DROGA 2.9)
- 17.07 | "Czytać zawsze do końca. Nie wybiórczo i już wiem.... Całość czytać" |
  Zasada ponadodcinkowa → DROGA 2.10: źródła (dokumenty, logi, wyniki narzędzi,
  poradniki) czytać w całości, nie fragmentami. | OBOWIĄZUJE (DROGA 2.10)
- 17.07 | "Niech to będzie Już DROGA V3" | Zasada JEDEN ODCINEK = JEDNO OKNO
  wchodzi jako wersja główna: DROGA 3.0 (po potrójnej generacji kadrów esencji
  10007 przez dwie równoległe sesje). | OBOWIĄZUJE (DROGA 3.0)
- 18.07 | "Przeanalizuj co może stać się jeszcze w przyszłości. Pomóż sobie
  czytając ludzi nie po troszku tylko pełna weryfikacja" | Analiza ryzyk
  przyszłości pipeline (platformy, prawo, technika, proces) z PEŁNĄ lekturą
  źródeł (całe artykuły, nie snippety). Wnioski → NAUKI + ew. DROGA. | W REALIZACJI
- 18.07 | "Następna sprawa cenzory i poprawność polityczna. Jeżeli gemini wypluł
  ten scenariusz o ślimakach to jest jak najbardziej dopuszczalne. W rolce o
  ŚLIMAKACH wyjebana cała esencja żartu dlatego poszło to na dysk. Nie poprawiaj
  rolki teraz. Weź to pod uwagę w następnych rolkach" (korekta Tomasza: chodzi o
  ślimaki #10005, nie "śmieci") | ZAKAZ AUTOCENZURY ESENCJI ŻARTU w produkcji:
  zaakceptowany scenariusz idzie w całości, bez łagodzenia poprawnościowego z
  własnej inicjatywy (test dopuszczalności: skoro duży model typu Gemini scenariusz
  wypluł, treść jest dopuszczalna). Złagodzenia słów WYŁĄCZNIE decyzją Tomasza
  (wzorzec: "płuca trenuję" przy 10007 — jego wybór, nie cicha podmiana).
  #10005 NIE poprawiać teraz; zasada obowiązuje OD NASTĘPNYCH rolek. | OBOWIĄZUJE (DROGA 3.3)
- 18.07 | "Dodaj powiadomienie do telegrama jak już ha Dom stoi" | Powiadomienia
  Telegram wpięte w pipeline publikacji: helper tools/tg_powiadom.sh → webhook
  fabryka_rolka_gotowa na HA Dom (bot+token w HA Dom, wg PROCEDUR nie na VPS;
  Dom stoi — HTTP 200 przez Nabu Casa). Pierwsze powiadomienie wysłane:
  publikacja 10007 z permalinkiem. Zasada: powiadomienie nigdy nie blokuje
  publikacji; HTTP 200 nie dowodzi dostarczenia — weryfikacja na telefonie.
  | WDROŻONE (czeka potwierdzenie odbioru)
- 18.07 | "Jest powiadomienie wszystko dobrze" | Tomasz POTWIERDZA odbiór na
  telefonie. Pętla domknięta end-to-end: publikacja Graph API + Telegram przez
  webhook HA Dom (tg_powiadom.sh) działają. Standard po każdej publikacji. | POTWIERDZONE ✓

## 23.07.2026 — KASACJA CAŁKOWITA STAREGO TOMKA (Mieczysław)
- "Mówię samego starego Tomka wypierdol wszystko co jest z nim związane. Reszta
  ma zostać" | WYKONANE, zweryfikowane w żywym systemie. USUNIĘTE: (a) baza wideo
  data/zarty/bank/mieczyslaw_plot.mp4; (b) stare foldery Mieczysława/testy sprzed
  duetu: zarty/10000, 10001 (pilot Cukinie 216MB), 10002, 0002, 9999; (c) z kodu
  produkcji zarty_produkcja.py: głos MIECZYSŁAW, kolor ASS, oba opisy (PL+EN),
  styl głosu, cała funkcja _klip_bank (LatentSync na bazie Mieczysława) + haczyk
  wywołujący (BANK) w pętli klipów + wzmianka w normalizatorze imion. Łącznie
  ~286MB. ZOSTAWIONE świadomie: próbki głosów TTS w banku (probka_EL_Brian/
  Marek/Zofia — nie należą do Mieczysława), Janusz+Bohater+Helena+Józek+Jacuś,
  martwe-ale-bezpieczne warunki "(BANK) not in mowi" w zarty.py (zawsze true,
  nie ruszają parsera). health 200, MIECZYSŁAW w GLOSY_VEO/KOLORY_ASS = False,
  duet żyje. Backup kodu: /tmp/zp_backup.py (sesyjny). | ZAMKNIĘTE
- 23.07 | "Usuń resztę bohaterów! Zostaw Tomasza i Janusza z serii" | WYKONANE,
  zweryfikowane w żywym systemie (health 200). Z kodu produkcji zarty_produkcja.py
  wycięci wszyscy poza duetem: HELENA, TOMASZ (sąsiad-kombinator w hawajskiej
  koszuli — INNA postać niż Tomek serii!), JACUŚ, JÓZEK (Mieczysław usunięty
  wcześniej). Zostali TYLKO: BOHATER (=Tomek serii, kucyk+broda) i JANUSZ.
  GLOSY_VEO=[BOHATER,JANUSZ], KOLORY_ASS=[BOHATER,JANUSZ], parser _kwestie zna
  tylko tych dwóch. Wygląd duetu z biblioteki kart (bohater_baza/janusz_baza),
  nie z OPISY_POSTACI. Backup: /tmp/zp_pre_czystka.py. | ZAMKNIĘTE
