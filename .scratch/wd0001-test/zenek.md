# WD_0001 v6 — indywidualna kontrola Zenka, 29.07.2026

## POTWIERDZONE

### Zakres i metoda

- Obejrzałem mapę mastera co 2 s oraz lokalnie wygenerowaną mapę co 1 s.
- Obejrzałem mapy wszystkich pięciu źródeł co 2 s oraz lokalnie wygenerowane mapy co 1 s.
- `ffprobe` potwierdził dla v6: 57.866667 s, 1080×1920, 30 fps, strumień audio, brak strumienia napisów.
- Pełny seans przez `tools/oczy_uszy.py` nie odbył się: narzędzie zakończyło się błędem DNS przed wysłaniem pliku. Dlatego nie wydaję twierdzeń o płynności ruchu ani jakości dźwięku.

### 1. Ocena v6 — słabe sekundy

- **0–3 s:** jest czytelna czołówka, ale obrazem jest nieruchawy prezenter przy stole; nie ma wizualnego haka, problemu ani rezultatu pracy.
- **3–9 s:** nadal sam prezenter w niemal identycznym kadrze. Pierwsza przebitka pojawia się dopiero w 9 s.
- **9–21 s:** dwa kolejne ujęcia pokazują głównie ziemię, chwasty, pieńki i nogi operatora. Razem trwa to 12 s i jest wizualnym powtórzeniem.
- **21–27 s:** koparka i ludzie są pokazani w wąskim poziomym pasie, a większość pionowego ekranu zajmuje rozmyte wypełnienie. Treść jest istotna, lecz prezentacja osłabia szczegół i immersję.
- **27–32 s:** szeroki plan miejsca również jest w poziomym pasie z rozmytym wypełnieniem; bohaterowie i koparka są mali.
- **32–39 s:** przez 7 s pierwszy plan dominuje siatka ogrodzenia, a za nią głównie przekopana ziemia. To najdłuższy redakcyjnie słaby blok w drugiej połowie przebitek.
- **45–57.87 s:** powrót do jednego kadru prezentera na prawie 13 s, bez kolejnej ilustracji i bez napisów mowy.
- **Całe 0–57.87 s:** nie ma napisów dialogowych; jedyny tekst ekranowy to tytuł i nazwa ROD na początku. Potwierdza to obraz mastera, skrypt `_montaz_v6.sh` (dwa `drawtext` tylko do 3.2 s) oraz brak strumienia napisów w `ffprobe`.

Nie stwierdzam na mapach czarnej klatki, złej orientacji ani oczywiście błędnego cięcia granicznego. Płynności ruchu i dźwięku nie rozstrzygam.

### 2. Najlepsze brakujące ujęcia ze źródeł

- **`norm_20260722_093926.mp4`, 0–6 s:** duży pień i odsłonięte korzenie w zarośniętym terenie; mocny detal problemu i dobry materiał na „przed”.
- **`norm_20260722_093926.mp4`, 36–41 s:** bardzo bliski plan dużej bryły korzeniowej/pniaka wyrwanego z ziemi; pokazuje skalę pracy lepiej niż stopy i drobne pieńki użyte w 9–21 s.
- **`norm_20260722_094249.mp4`:** nie znalazłem brakującego ujęcia mocniejszego od materiału już użytego; niemal cały klip pokazuje spacerującego operatora, ziemię, chwasty i pieńki z góry.
- **`norm_VID-20260723-WA0001.mp4`, 12–14 s:** koparka, pracownik i rozkopany teren w jednym szerokim kadrze; krótkie dopełnienie akcji. Źródło jest obrócone w pikselach, więc wymaga tego samego prostowania co użyty fragment.
- **`norm_VID-20260723-WA0005.mp4`, 21–28 s:** człowiek pracuje ręcznie w dole, coraz bliżej kamery; jest człowiek, czynność i wysiłek, a nie sama ziemia za siatką.
- **`norm_VID-20260723-WA0007.mp4`, 16–27 s:** bliski, czysty pionowy plan żółtej minikoparki i operatora; najmocniejszy brak całego montażu. Maszyna wypełnia kadr, a kolejne klatki pokazują zmianę położenia ramienia. Tego źródła manifest v6 w ogóle nie wymienia.

### 3. Aktualne zasady krótkiego pionowego wideo i zgodność v6

- **Hak natychmiast:** TikTok for Business podaje, że pierwsze 2 s są kluczowe, a aktualny przewodnik zaleca zaczynać energią, ruchem, humorem albo zaskoczeniem. V6 zaczyna się statycznym prezenterem i ujawnia pracę dopiero w 9 s.  
  Źródła: https://ads.tiktok.com/business/creativecenter/quicktok/online/5_creative_tips/pc/en?rid=qpfv5nqwvae  
  https://ads.tiktok.com/business/en/guides/what-is-ad-creative-guide
- **Pion, dźwięk, bezpieczna strefa:** Meta zaleca natywny format 9:16, dźwięk oraz kluczowe elementy w safe zone. V6 spełnia 9:16 i ma audio; bez pełnego seansu nie potwierdzam jakości dźwięku ani bezpiecznej strefy względem interfejsu aplikacji.  
  Źródło: https://www.facebook.com/business/ads/facebook-instagram-reels-ads
- **Napisy i szybkie zmiany:** aktualny przewodnik TikToka zaleca napisy/tekst dla odbioru bez dźwięku i szybkie cięcia; oficjalny materiał TikToka wskazuje też, że szybsze zmiany scen pomagają przyciągnąć uwagę. V6 nie ma napisów mowy, a bloki 9–21 s, 32–39 s i 45–57.87 s są za długie i mało zróżnicowane.  
  Źródła: https://ads.tiktok.com/business/en/guides/what-is-ad-creative-guide  
  https://ads.tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads
- **Oryginalność:** Meta w marcu 2026 potwierdziła priorytet dla treści oryginalnych i produkowanych przez właściciela profilu. Materiał Tomasza oraz autorski prezenter spełniają ten kierunek.  
  Źródło: https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/
- **Długość pojedynczego ujęcia:** nie znalazłem aktualnej, oficjalnej reguły platformy typu „każde ujęcie ma trwać dokładnie X sekund”. Oficjalne źródła mówią o szybkim tempie i szybszych zmianach scen, nie o sztywnym limicie.

### 4. Werdykt

**NIE — v6 nie nadaje się do publikacji bez zmian, jeśli warunkiem jest profesjonalna rolka zgodna z najnowszym językiem krótkiego wideo.**

Zmiany od najważniejszej:

1. **0–3 s:** otworzyć bliską akcją koparki z `WA0007` 16–19 s albo detalem wielkiego korzenia z `093926` 36–39 s; nałożyć krótki hak, np. „Ten teren był nie do przejścia”.
2. **0–57.87 s:** dodać zsynchronizowane, duże napisy mowy w bezpiecznej strefie; nie tylko czołówkę.
3. **9–21 s:** skrócić 12 s ziemi/stóp do 2–3 s łącznie; zastąpić resztę koparką `WA0007` 16–27 s i pracą człowieka `WA0005` 21–28 s.
4. **21–32 s:** ograniczyć poziome pasy z rozmytym tłem; zostawić najwyżej krótki kadr ustanawiający, a sedno pokazać natywnym pionowym planem WA0007.
5. **32–39 s:** skrócić siatkę/ziemię do 1–2 s albo zastąpić detalem korzeni `093926` 36–41 s.
6. **45–57.87 s:** przełamać 13 s prezentera obrazem efektu końcowego z `093926` 54–62 s i skrócić końcówkę; jeśli tekst pozwala, zakończyć konkretnym rezultatem lub prostym CTA.

## HIPOTEZY

- Po takim przemontowaniu rolka może zachować około 50–58 s, ale będzie nowocześniejsza dzięki zmianie kolejności i rytmu; alternatywnie warto przygotować drugi test 25–35 s. To rekomendacja redakcyjna, nie oficjalny limit platformy.
- Najmocniejsza struktura z dostępnego materiału to: **akcja koparki → zarośnięty detal → ludzie i korzenie → oczyszczony teren → krótki prezenter/CTA**. Jest to mój wniosek z map, nie pomiar retencji.

## NIE WIEM

- Nie wiem, czy dźwięk, wymowa i lipsync są bezbłędne, ponieważ `oczy_uszy.py` nie zdołał wysłać pliku z powodu DNS.
- Nie wiem, jak dokładnie porusza się kamera między próbkami co 1 s; dlatego nie wskazuję „trzęsie” ani „złe cięcie” bez dowodu.
- Nie wiem, gdzie są sześć oryginalnych zdjęć wymienionych w `OPIS.md`: w katalogu znalazłem mapy i klatki wyciągnięte z filmów, ale nie sześć jednoznacznie oznaczonych oryginałów. Nie oceniam zdjęć, których nie potrafię zidentyfikować.

— **Zenek**
