# -*- coding: utf-8 -*-
from src.db.database import add_topic, get_connection

# Dokladamy do ISTNIEJACEJ kategorii "Kompostownik i gnojowki" (nie tworzymy nowej)
CAT_NAZWA = "Kompostownik i gnojowki"

KOMPOST = [
 # --- Architektura i Infrastruktura (strukturalne, uniwersalne) ---
 ("Kompostownik z palet: Surowa, rustykalna struktura. Zbudowany z surowych, jasnych desek paletowych z wyraźnymi szczelinami. Wnętrze wypełnione organiczną masą, przez szpary wystają suche źdźbła trawy.", None),
 ("Termokompostownik: Nowoczesna, zamknięta bryła. Gładki, czarny, matowy plastik o żebrowanej powierzchni, z zamkniętą klapą od góry i małymi drzwiczkami u dołu. Zero widocznych resztek na zewnątrz.", None),
 ("Kompostownik bębnowy (obrotowy): Konstrukcja mechaniczna. Czarna lub zielona plastikowa beczka zamontowana poziomo na metalowym, srebrnym stelażu, wyposażona w korbę do obracania.", None),
 ("Kompostownik z siatki zbrojeniowej: Cylindryczna forma. Otwarty, pionowy walec utworzony z zardzewiałej, grubej metalowej siatki oczkowej, szczelnie wypchany brązowymi, suchymi liśćmi dębu.", "9,10,11"),
 ("Pryzma kompostowa: Naturalny, dziki kształt. Stożkowaty kopiec materii organicznej usypany bezpośrednio na ziemi, bez żadnych ścianek. Widoczne chłodne, poranne światło i gęsta, biała para unosząca się ze szczytu kopca.", "3,4,9,10,11"),
 ("Beczka na gnojówkę: Stara, niebieska beczka z polietylenu lub drewniana, okuta blachą, z otwartym wiekiem, po brzegi wypełniona mętną, zieloną cieczą.", None),
 ("Pojemnik Bokashi (balkonowy): Niewielki, elegancki, gładki pojemnik w kuchni z kranikiem na samym dole, przypominający stylowy kosz na śmieci, w jasnoszarym kolorze.", None),
 ("Stacja do przesiewania: Drewniana, gruba rama z naciągniętą stalową siatką pod kątem 45 stopni. Na dół osypuje się idealnie czarna, puszysta ziemia, a na siatce zostają większe frakcje gałązek.", None),
 ("Kompostownik murowany: Trwała architektura. Trzy ściany zbudowane z czerwonej, starej cegły, lekko porośniętej mchem, tworzące solidny boks wypełniony ciemną ziemią.", None),
 ("Widły amerykańskie w kompoście: Zbliżenie na lśniące, srebrne, płaskie zęby solidnych wideł wbite głęboko w ciemnobrązową, wilgotną strukturę kompostu.", None),
 # --- Alchemia Kompostu (frakcje zielone i brazowe) ---
 ("Skoszona trawa: Tekstura gęsta, zbita, w kolorze absolutnie jaskrawej, wręcz neonowej zieleni. Zbliżenie na mokre, posklejane ze sobą cienkie źdźbła z kroplami wody.", "4,5,6,7,8,9"),
 ("Surowe resztki kuchenne: Feeria barw. Geometryczny chaos składający się z pomarańczowych obierzyn z marchwi, pofalowanych liści kapusty i połówek zielonych jabłek, bez śladów pleśni.", None),
 ("Zrębki drewniane: Ostrokrawędzista tekstura. Jasne, słomkowo-żółte, połamane kawałki drewna i kory ułożone w stertę. Twarde, kanciaste kształty.", None),
 ("Suche liście (Ziemia liściowa): Szeleszcząca faktura. Brązowe, czerwone i żółte, poskręcane z suchości liście o wyraźnie zarysowanym, chrupiącym użyłkowaniu.", "9,10,11"),
 ("Fusy z kawy: Tekstura gęstego, ciemnobrązowego, wilgotnego piasku z mikroskopijnymi granulkami.", None),
 ("Skorupki jajek: Mozaika kształtów. Ostre, postrzępione, wypukłe i wklęsłe fragmenty białych oraz jasnobrązowych skorupek, wewnątrz z resztkami przezroczystej błonki.", None),
 ("Popiół drzewny: Ekstremalnie drobny, matowy, jasnoszary do białego pył, w którym zanurzone są pojedyncze, kanciaste, smoliście czarne kawałki węgla drzewnego.", "10,11,12,1,2,3"),
 ("Szary karton (celuloza): Tekstura brązowego papieru pakowego o rozerwanych, nieregularnych i włochatych brzegach, uwidaczniająca falistą warstwę wewnątrz (tektura falista).", None),
 ("Sucha słoma: Puste w środku, gładkie, lśniące, złoto-żółte rurki ułożone w równoległe lub krzyżujące się warstwy.", None),
 ("Chwasty z korzeniami: Zwiędnięte, wiotkie, bladozielone łodygi, na których końcach znajdują się gęste, splątane wiązki białych korzeni oklejonych ciemnymi grudkami ziemi.", "4,5,6,7,8,9"),
 # --- Plynne Zloto (gnojowki i wywary, sezon jak dojrzale gnojowki w bazie) ---
 ("Gnojówka z pokrzywy (fermentująca): Mroczny, gęsty, ciemnozielony płyn. Gruba warstwa żółto-białej, bąbelkującej piany znajduje się na samej górze płynu, z wystającymi, zębatymi liśćmi pokrzywy.", "5,6,7"),
 ("Gnojówka ze skrzypu polnego: Płyn o barwie brązowawej herbaty. W cieczy unoszą się zielone, segmentowane, choinkowate igiełki skrzypu przypominające prehistoryczne rośliny. Brak dużej piany.", "6,7,8"),
 ("Gnojówka z żywokostu: Płyn smoliście czarny, gęsty jak szlam. W nim macerują się ogromne, owalne, ciemnozielone liście o bardzo wyraźnej, włochatej lub szorstkiej fakturze.", "6,7,8"),
 ("Wywar z łupin cebuli: Krystalicznie czysty, płyn w kolorze głębokiego, świetlistego bursztynu (jak mocna herbata), z unoszącymi się na powierzchni cienkimi, pomarańczowo-złotymi, półprzezroczystymi łuskami.", None),
 ("Wyciąg z czosnku: Mleczno-biały, mętny płyn w przezroczystej butelce z atomizerem. Na dnie widać całe ząbki czosnku o gładkiej, białej powierzchni.", "5,6,7,8,9"),
 ("Gnojówka z mniszka lekarskiego: Żółtawo-zielonkawy, mętny płyn, w którym rozkładają się charakterystyczne, mocno powycinane (w kształt zębów lwa) liście oraz resztki żółtych płatków kwiatowych.", "4,5,6"),
 ("Rozcieńczanie (mieszanie z wodą): Fotografia makro podwodna – strumień gęstej, ciemnozielonej mazi z pokrzywy wlewa się do wiadra z krystalicznie czystą wodą, tworząc zjawiskowe, dymne, hipnotyzujące wiry.", None),
 ("Herbata kompostowa: Ciemnobrązowy płyn, w którym kluczowym elementem wizualnym są agresywne, gęste bąbelki powietrza tłoczone przez rurkę (napowietrzanie), tworzące wrzącą teksturę na powierzchni.", "4,5,6,7,8,9"),
 ("Gnojówka z liści pomidorów: Mętnawa, ciemnozielona ciecz. Pływają w niej ostre, pierzastodzielne liście, charakterystyczne wyłącznie dla krzewów pomidorowych.", "6,7,8"),
 ("Nawóz z drożdży: Płyn w kolorze kawy z mlekiem (beżowy). Posiada zbitą, drobną, kremową piankę, wlewaną z plastikowego, czerwonego wiadra wprost na ziemię.", "4,5,6"),
 # --- Magia Procesu (mikrobiologia, w wiekszosci uniwersalne) ---
 ("Faza termofilna (gorące serce): Nocne ujęcie lub o świcie. Rozgarnięty środek kompostownika ujawnia czarną masę, która żarzy się lub intensywnie dymi parą wodną ze względu na temperaturę sięgającą 60-70 stopni.", "10,11,12,1,2,3"),
 ("Dżdżownice kompostowe (Kalifornijskie): Makrofotografia. Pęki lśniących, wilgotnych, ciemnoczerwonych pierścienic z wyraźnymi segmentami, splątanych ze sobą w idealnie czarnej, sypkiej ziemi.", "4,5,6,7,8,9,10"),
 ("Promieniowce (biały nalot): Zbliżenie na rozkładające się liście, które są w całości pokryte drobnym, białym, proszkowatym nalotem (wyglądającym jak rozsypany popiół lub siwy szron na kompoście).", None),
 ("Grzybnia kompostowa (mikoryza): Makro na wilgotny kawałek drewna otoczony czarną ziemią, z którego we wszystkie strony rozchodzą się ekstremalnie cienkie, białe, pajęczynowate nici.", None),
 ("Struktura Lasagne: Przekrój geologiczny kompostownika. Wyraźne, poziome warstwy na przemian: cienka zielona linia trawy, grubsza brązowa warstwa suchych liści, linia szarego kartonu i znów trawa.", None),
 ("Czarne Złoto (gotowy kompost): Tekstura idealnej, gruzełkowatej gleby. Przypomina czarne, wilgotne, matowe kuleczki wielkości maku lub drobnej kaszy, rozsypujące się w czystych ludzkich dłoniach.", None),
 ("Destrukcja materii: Ujęcie poklatkowe w jednym obrazie. Pół jabłka, którego jedna strona jest czerwona i jędrna, a druga strona (płynne przejście) zamienia się w czarną, porowatą ziemię.", None),
 ("Bąble tlenowe gnojówki: Ekstremalne zbliżenie (makro) na powierzchnię fermentującej cieczy, gdzie napęczniały, błyszczący w świetle słonecznym bąbel gazu właśnie pęka, uwalniając esencję.", "5,6,7,8"),
 ("Krople wilgoci: Zbliżenie na ciemny, gąbczasty materiał kompostu, na którym osadziły się idealnie kuliste, błyszczące krople wody, świadczące o odpowiedniej wilgotności złoża.", None),
 ("Przewietrzanie (Aeracja): Dynamiczne ujęcie – ciemna, ciężka masa kompostowa wyrzucana w górę na ostrzach wideł, rozpadająca się w powietrzu na mniejsze, gruzełkowate kawałki.", None),
 # --- Rezultaty i Zastosowanie na Dzialce (sezon wegetacyjny) ---
 ("Podlewanie pod korzeń (Gnojówka): Gruby, włochaty pęd pomidora u samej ziemi. Szyjka zielonej konewki precyzyjnie aplikuje strumień ciemnozielonego płynu tuż przy wejściu łodygi w glebę.", "5,6,7,8"),
 ("Oprysk dolistny (Mgiełka): Szeroki, płaski, szorstki liść dyni. Powietrze wypełnia zawiesina (chmura) mikroskopijnych, półprzezroczystych kropel rozpylanych ze zraszacza ciśnieniowego w złotych promieniach słońca.", "5,6,7,8"),
 ("Zaprawianie dołków: Makro na stalową, lśniącą łopatkę ogrodową, która wrzuca czarną, puszystą masę kompostową na samo dno wykopanego w jasnym piasku dołka.", "3,4,5,9,10"),
 ("Ściółkowanie kompostem: Płaska powierzchnia nagiej, szarej ziemi wokół truskawki, która do połowy zostaje pokryta grubą na 5 cm warstwą, czarnego, równego kompostu.", "4,5,6"),
 ("Eksplozja korzeni: Wyciągnięta z doniczki bryła korzeniowa – setki grubych, śnieżnobiałych, zdrowych korzeni ciasno oplotło czarną, kompostową ziemię.", "4,5,9,10"),
 ("Gigantyczne plony: Obraz potężnych, idealnie kulistych i błyszczących czerwonych pomidorów malinowych, których waga aż wygina grubą łodygę w dół.", "7,8,9"),
 ("Witalność liści: Zbliżenie na liść ogórka potraktowanego wywarem. Ciemnozielony, mięsisty liść z ekstremalnie widoczną siatką jaśniejszych żyłek, bez najmniejszych śladów chorób grzybowych czy żółknięcia.", "5,6,7,8"),
 ("Kwiaty po żywokoście: Ogromne, trąbkowate, jaskrawożółte kwiaty cukinii rozwijające się z w pełni wykształconych, grubych pąków na tle intensywnej zieleni.", "6,7,8"),
 ("Siewki w kompoście (Rozsada): Kontrast kolorystyczny. Z czystej, smoliście czarnej i gruzełkowatej ziemi wyrastają dwa miniaturowe, grube, idealnie symetryczne, jasnozielone liścienie.", "3,4,5"),
 ("Ochrona przed szkodnikami: Zbliżenie (makro) na mszyce, które masowo uciekają i odrywają się od zielonej łodygi róży spryskanej mgiełką z wywaru czosnkowego.", "5,6,7,8"),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT_NAZWA,)).fetchone()
conn.close()
if not row:
    print("BLAD: kategoria '%s' nie istnieje - przerywam." % CAT_NAZWA)
else:
    cid = row['id']
    c0 = get_connection()
    przed = c0.execute('SELECT COUNT(*) x FROM topics WHERE category_id=?', (cid,)).fetchone()['x']
    c0.close()

    for tekst, mies in KOMPOST:
        tid = add_topic(cid, tekst)
        if mies is not None:
            c = get_connection(); c.execute("UPDATE topics SET miesiace=? WHERE id=?", (mies, tid)); c.commit(); c.close()

    c = get_connection()
    po = c.execute('SELECT COUNT(*) x FROM topics WHERE category_id=?', (cid,)).fetchone()['x']
    tc = c.execute("SELECT COUNT(*) x FROM categories").fetchone()['x']
    tt = c.execute("SELECT COUNT(*) x FROM topics").fetchone()['x']
    c.close()
    print("OK dodano %d tematow kompostowo-gnojowkowych do kategorii '%s' (id=%s)." % (len(KOMPOST), CAT_NAZWA, cid))
    print("Kategoria: bylo %d, jest teraz %d tematow." % (przed, po))
    print("RAZEM w bazie: %d kategorii, %d tematow." % (tc, tt))
