# -*- coding: utf-8 -*-
from src.db.database import add_category, add_topic, get_connection

CAT = "Prawo Działkowe i Życie Społeczności"

PRAWO = [
 # --- Granice, Odleglosci i Ogrodzenia ---
 ("Wysokość ogrodzenia międzydziałkowego: Makrofotografia. Jaskrawożółta, zwijana miarka stalowa z wyraźnymi, czarnymi cyframi, zahaczona precyzyjnie o górny, naprężony drut zielonej siatki powlekanej. W tle płynnie rozmyty, krótko ścięty trawnik.", None),
 ("Żywopłot na granicy: Zbliżenie na ostre ostrze lśniących, stalowych nożyc do żywopłotu, które tną idealnie w linii prostej równą ścianę gęstych, sztywnych gałązek tui. Ostrze jest ustawione dokładnie równolegle do słupka granicznego.", "5,6,7,8,9"),
 ("Odległość drzewa od płotu (2 metry): Przekrój od góry z drona. Geometryczny, prosty mur z siatki drucianej, od którego pod kątem prostym leży na ziemi rozciągnięta czerwona taśma geodezyjna, dotykająca pnia grubej, starej jabłoni o spękanej, szarej korze.", None),
 ("Zastawianie alejek wspólnych: Perspektywa żabiej (nisko przy ziemi). Wąska, żwirowa alejka, której połowę brutalnie tarasuje pozostawiona, zardzewiała taczka budowlana pełna suchych gałęzi. Światło zachodzącego słońca rzuca z niej długi, ciemny cień.", None),
 ("Kompostownik blisko sąsiada: Drewniany, surowy boks z równych desek, szczelnie wypełniony ciemną materią. Stoi zaledwie na szerokość dłoni od rdzewiejącego, siatkowego płotu, przez który widać zadbaną, kwitnącą rabatę sąsiada.", None),
 ("Brama wjazdowa i kłódka: Potężna, geometryczna brama ze stalowych profili (ocynk). Centralny punkt to masywna, mosiężna kłódka wpięta w solidny rygiel, pokryta drobnymi kroplami porannej rosy, blokująca wjazd na teren sektora.", None),
 ("Tabliczka z numerem działki: Stara, mocno zardzewiała na krawędziach, emaliowana na ciemnozielono kwadratowa tabliczka. Widnieje na niej lekko wypukły, biały, klasyczny font numeryczny, przybita na wskroś gwoździami do szorstkiej deski furtki.", None),
 ("Korony drzew nad inną działką: Kadr z dołu w górę. Prosta linia drutu kolczastego lub siatki na tle jasnego nieba. Z prawej strony drutu gruba, ulistniona gałąź owocowa brutalnie i ciężko przewiesza się na lewą stronę, przekraczając granicę w powietrzu.", "4,5,6,7,8,9,10"),
 ("Rozgraniczenie geodezyjne: Metalowy, świeży, lśniący bolec (palik) z czerwoną, plastikową główką, mocno wbity młotkiem w twardą, suchą ziemię u zbiegu czterech narożników działek, oznaczający nienaruszalny punkt pomiarowy.", None),
 ("Zgoda na zmianę płotu: Dwie dłonie o różnej fakturze skóry, ściskające się mocno nad równym murkiem z czerwonej cegły klinkierowej, symbolizujące zgodę sąsiadów. Ciepłe, przyjazne oświetlenie wolumetryczne.", None),
 # --- Dokumentacja, Zarzad i Walne Zebranie ---
 ("Dokument rezygnacji z funkcji w zarządzie: Elegancki, gruby, matowy papier ułożony na dębowym blacie biurka. Na dokumencie widnieje staranny, wyraźny, męski podpis złożony czarnym atramentem z wiecznego pióra, tuż pod wydrukowanym nagłówkiem Rezygnacja. Obok otwarta, wiązana teczka z ciemnego kartonu.", None),
 ("Dziennik korespondencji (Sekretariat ROD): Gruba, stara księga introligatorska z twardą oprawą, otwarta na środku. Na kremowych stronach widać idealnie równe, geometryczne tabele wypełnione niebieskim długopisem z datami wpłynięcia pism ogrodowych.", None),
 ("Protokół z posiedzenia z pieczątką: Dokumentacja techniczna ułożona na stole. Kluczowy detal: okrągła, tuszowa, lekko rozmazana granatowa pieczątka z napisem Zarząd ROD przybita asymetrycznie w prawym dolnym rogu papieru.", None),
 ("Uchwała Walnego Zebrania: Gęsto zadrukowana kartka formatu A4 włożona do przezroczystej koszulki foliowej, odbijającej światło. Przypięta dwiema metalowymi, srebrnymi pinezkami do korkowej tablicy ogłoszeń o ostrej fakturze kruszywa.", "2,3,4"),
 ("Mandaty głosowania (Walne Zebranie): Ciasny kadr od tyłu na grupę zamazanych sylwetek. W ostrości widać dziesiątki wzniesionych w górę dłoni trzymających jaskrawe, prostokątne, jaskrawozielone lub czerwone kartoniki, odcinające się od ciemniejszego tła świetlicy.", "2,3,4"),
 ("Tytuł prawny (Umowa dzierżawy): Klasyczna teczka wiązana na białą tasiemkę bawełnianą. Tasiemka jest właśnie rozwiązywana przez palce, odsłaniając krawędź pożółkłego dokumentu z wyraźnym godłem i paragrafami.", None),
 ("Skrzynka podawcza na zarządówce: Skrzynka pocztowa z surowego, polakierowanego drewna wisząca na ceglanym murze Domu Działkowca. Przez wąską, ciemną szczelinę na górze widać do połowy wsuniętą, białą kopertę formatu DL.", None),
 ("Legitymacja Działkowca: Mała, zielona, rozkładana książeczka w formacie dowodu ułożona na surowym drewnie stołu ogrodowego. Widoczna tłoczona okładka i fragment zdjęcia z okrągłą pieczęcią suchą.", None),
 ("Opłaty ogrodowe (Kalkulator i rachunki): Widok z góry. Szary, biurowy kalkulator z twardymi plastikowymi przyciskami, obok leży sterta monet, zgięty rachunek za prąd oraz czerwony ołówek kreślarski na szorstkim drewnie.", "3,4,5,6"),
 ("Protokół zdawczo-odbiorczy działki: Makro na pęk ciężkich, stalowych kluczy o różnych, skomplikowanych nacięciach. Klucze leżą bezpośrednio na papierowym, spisanym ręcznie dokumencie z odhaczonymi checkboxami.", None),
 # --- Normy Budowlane i Architektura ---
 ("Dalmierz laserowy w akcji (Powierzchnia 35m2): Kadr w półmroku. Ręka trzyma szaro-czerwoną, gumowaną obudowę dalmierza. Z soczewki urządzenia wystrzeliwuje ostry, prosty jak strzała, czerwony promień lasera uderzający w odległą, ciemną ścianę z desek.", None),
 ("Wysokość altany (5 metrów dla dachu stromego): Rysunek techniczny (blueprint) rozłożony płasko. Białe linie na głębokim, cyjanowym tle. Geometria ostrego dachu dwuspadowego ze strzałką wymiarową, która ostro wskazuje od fundamentu aż po sam szczyt kalenicy.", None),
 ("Taras zadaszony a powierzchnia zabudowy: Deski kompozytowe tarasu i wyraźna krawędź, gdzie zaczyna się trawa. Z góry opada masywny, pionowy pion murarski (stalowy stożek na cienkim białym sznurku), wyznaczający rzut krawędzi dachu na grunt.", None),
 ("Samowola budowlana (Taśma izolacyjna): Surowa ściana budynku budowanego z szarych bloczków betonowych. Przez całą szerokość muru naciągnięta jest pod kątem jaskrawa, żółto-czarna, plastikowa taśma ostrzegawcza układająca się w spirale na wietrze.", None),
 ("Wymiary murowanego grilla: Perspektywa architektoniczna. Ciężki, wymurowany z jasnej cegły paleniskowej komin stojący obok altany. Do cegły przyłożony jest żółty, stolarski kątownik z wyraźną podziałką w centymetrach.", None),
 ("Legalny zbiornik na szambo (Pojemność): Geometryczny, betonowy, szary właz z żeliwną pokrywą na środku idealnego trawnika. Obok w rzędzie stoją 3 duże, niebieskie beczki 200L, tworzące wizualne porównanie dopuszczalnej kubatury.", None),
 ("Zabronione konstrukcje (Szklarnia murowana): Kadr pokazujący solidny, głęboki fundament betonowy, z którego wystają zardzewiałe pręty zbrojeniowe. Na fundamentach zaczęto stawiać grube, szklane ściany na profilach, co przypomina małą halę przemysłową.", None),
 ("Inspekcja zarządu (Dach płaski): Widok z dachu pokrytego czarną papą termozgrzewalną z bardzo widocznymi, stopionymi łączeniami asfaltu. Na papie leży jaskrawożółta poziomica pęcherzykowa z minimalnym spadkiem zielonego płynu w oczku.", None),
 ("Studnia głębinowa (Odwiert): Potężne wiertło świdra (stal węglowa z wgłębieniami pokryta zaschniętą, żółtą gliną) wyciągane prosto z wąskiej, ciemnej dziury w trawniku w otoczeniu brył mokrej ziemi.", "4,5,6,7,8,9,10"),
 ("Rozbiórka starej altany: Sterta zbutwiałych, ciemnoszarych desek z wystającymi, zardzewiałymi gwoździami. Na szczycie góry gruzu leży samotnie stary, czerwony i pęknięty łom budowlany.", "4,5,6,7,8,9,10"),
 # --- Zasady Wspolzycia i Regulaminowe Zakazy ---
 ("Dym z ogniska (Zakaz spalania): Kontrastowe ujęcie. W dolnej połowie kadru zardzewiała taczka, z której wydobywa się gęsty, nieprzenikniony, ciężki, biało-szary dym, dusząco rozlewający się w stronę pięknej, słonecznej i czystej działki obok.", "3,4,10,11"),
 ("Hałas kosiarki i godziny ciszy: Duża, czerwona, brudna kosiarka spalinowa na środku trawnika. Na jej masywnym silniku z żebrowaniem leży starodawny, metalowy budzik ze wskazówkami ostro ustawionymi na godzinę 13:00.", "4,5,6,7,8,9,10"),
 ("Ujadający pies bez smyczy: Ciasny kadr na pysk owczarka niemieckiego. Pies szczeka głośno przez pręty ciemnej bramy z siatki. Obok furtki wyraźny znak na białej, plastikowej tarczy: sylwetka psa przekreślona czerwoną linią.", None),
 ("Głośna muzyka (Boombox): Na surowym, drewnianym stole pośród kwiatów leży masywny, nowoczesny, czarny głośnik Bluetooth o gumowanej teksturze. Wokół niego wizualnie drży powietrze i rozsypana cienka warstwa żółtego pyłku.", "5,6,7,8,9"),
 ("Gołębie i dokarmianie zwierząt: Drewniany płot działki. Na górnej poręczy siedzi pięć miejskich gołębi w rzędzie, ociekających w słońcu fioletowo-zielonym blaskiem piór. Wokół nich na deskach widoczne grube, białe plamy ptasich odchodów psujące estetykę.", None),
 ("Prywatny monitoring (Kamera na sąsiada): Czarna, obła obudowa kamery obrotowej (PTZ) przymocowana do dachu białej altany. Szklane oko obiektywu jest bardzo wyraźnie, w linii prostej i ostro wycelowane w stronę oddalonego, brązowego tarasu na sąsiedniej działce.", None),
 ("Dzikie koty ogrodowe: Pod podłogą drewnianego tarasu, z głębokiego, ciemnego cienia wystają tylko dwoje świecących na jaskrawożółto, pionowych kocich oczu. Przed wejściem leży rozdarta folia z resztkami taniej, suchej karmy.", None),
 ("Brak dbałości o działkę (Chwasty): Geometria kontrastu. Po lewej stronie kadru wypielęgnowany, soczyście zielony trawnik angielski. Linia płotu. Po prawej stronie ekstremalnie gęsty gąszcz metrowych pokrzyw, ostów i zeschłych mleczy wysypujących biały puch.", "5,6,7,8,9"),
 ("Zakaz mycia pojazdów: Duży, błyszczący zderzak srebrnego samochodu na żwirowej alei ogrodowej. Po karoserii ścieka gruba, gęsta, biała piana aktywna, wsiąkając i zanieczyszczając ciemną, chłonną ziemię pod kołami.", "4,5,6,7,8,9"),
 ("Odręczny list za wycieraczką: Przednia szyba samochodu pokryta jesiennymi liśćmi. Pod gumą wycieraczki uwięziona jest wyrwana z zeszytu kartka w kratkę z zapisaną dużymi literami, ostrą, anonimową wiadomością długopisem.", "9,10,11"),
 # --- Infrastruktura Wspolna i Ekologia ROD ---
 ("Kontrola pojemników na śmieci: Duży, otwarty, ocynkowany kontener typu KP-7. Na samej górze piętrzącej się sterty foliowych worków leży brutalnie wrzucona ogromna, zielona tuja z bryłą korzeniową.", None),
 ("Zasypywanie rowu melioracyjnego: Przekrój rowu z mętną, stojącą na dnie wodą. Połowa rowu jest zasypana gruzem budowlanym (czerwona cegła i kawałki betonu), co całkowicie blokuje wąski, szary przepust z rury PCV pod mostkiem.", None),
 ("Brak rynien na dachu altany: Skraj płaskiego dachu pokrytego ciemną papą. Podczas ulewy z krawędzi nieosłoniętego dachu spływa potężny, szeroki wodospad deszczówki, wyrywając i wypłukując w ziemi głęboki, błotnisty kanion tuż przy samej granicy z sąsiadem.", "5,6,7,8,9"),
 ("Nieszczelne, trujące szambo: Mokra plama smolistej, czarnej cieczy o oleistym połysku, powoli sącząca się przez betonową, kruszącą się cembrowinę starego zbiornika wprost do jasnego, czystego piasku gruntu.", None),
 ("Wspólna sieć wodna (Awaria): Gruby, metalowy zawór sektorowy w zardzewiałej, zalanej po brzegi błotem studzience. Powierzchnia wody w studzience kipi od bąbli podwodnego, potężnego wycieku pod ciśnieniem.", "4,5,6,7,8,9,10"),
 ("Pompa hydroforowa: Masywny, niebieski silnik elektryczny połączony z żeliwną pompą ślimakową i manometrem ciśnienia pokazującym 3 BAR. Całość pokryta cienką warstwą kurzu w półmroku skrzynki ogrodowej.", None),
 ("Zamek i klucz dorobiony (Bezpieczeństwo): Surowa fotografia makro. Na chropowatym asfalcie alejki leży upuszczony, lśniący, mosiężny, świeżo nacięty ząbkami klucz (zamiennik do wspólnej bramy) z dołączonym, czerwonym, plastikowym brelokiem.", None),
 ("Śmieci wyrzucone w lesie/za płot ROD: Dzika gęstwina leśnych paproci tuż za zieloną siatką ogrodzenia ogrodu. W samym środku natury leży stos jasnych, porwanych worków foliowych pełnych odpadów, rażących sztucznością.", None),
 ("Gniazdo ptaków (Ochrona w sezonie lęgowym): Gruby konar jabłoni. Misternie uwite, szare gniazdo z suchych traw i mchu, wewnątrz którego leżą trzy jaskrawo błękitne, nakrapiane, idealnie gładkie jajka. Obok leżą nożyce sadownicze powstrzymane przed cięciem.", "3,4,5,6,7,8"),
 ("Oznakowana infrastruktura elektryczna: Szara skrzynka energetyczna ZK na betonowym, pionowym fundamencie. Drzwi rozdzielnicy całkowicie porośnięte gęstym, wijącym się bluszczem, spod którego ledwo widoczna jest naklejka z czerwoną błyskawicą i czarną czaszką.", None),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT,)).fetchone()
conn.close()
if row:
    print("UWAGA: kategoria '%s' juz istnieje (id=%s) - przerywam." % (CAT, row['id']))
else:
    cid = add_category(CAT)
    for tekst, mies in PRAWO:
        tid = add_topic(cid, tekst)
        if mies is not None:
            c = get_connection(); c.execute("UPDATE topics SET miesiace=? WHERE id=?", (mies, tid)); c.commit(); c.close()
    c = get_connection()
    n = c.execute("SELECT COUNT(*) x FROM topics WHERE category_id=?", (cid,)).fetchone()['x']
    tc = c.execute("SELECT COUNT(*) x FROM categories").fetchone()['x']
    tt = c.execute("SELECT COUNT(*) x FROM topics").fetchone()['x']
    c.close()
    print("OK dodano kategorie '%s' (id=%s) z %d tematami." % (CAT, cid, n))
    print("RAZEM w bazie: %d kategorii, %d tematow." % (tc, tt))
