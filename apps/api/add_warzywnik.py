# -*- coding: utf-8 -*-
from src.db.database import add_category, add_topic, get_connection

CAT = "Klasyczny Warzywnik i Sadownictwo"

WARZYWNIK = [
 # --- Krolowie Tunelu (Pomidory i Psiankowate) ---
 ("Pomidor Malinowy (Dojrzewanie): Ogromny, asymetryczny, żebrowany pomidor o barwie głębokiego, zgaszonego różu (nie jaskrawoczerwony). Skórka matowa, a wokół szypułki widoczne głębokie, zielonawe pęknięcia. Na owocu grube krople porannej rosy.", "7,8,9"),
 ("Usuwanie wilków (Pędy boczne): Zbliżenie na grubą, włochatą łodygę pomidora umazaną zielonym sokiem. W kącie między łodygą główną a liściem ułożonym pod kątem 90 stopni, palce wyłamują ostro zakończony, jasny, nowy pęd (wilk).", "6,7,8"),
 ("Kwiatostan pomidora: Małe, intensywnie żółte, pięcioramienne kwiatki w kształcie ostrych gwiazdek. Zebrane w luźne grono. Środek kwiatu tworzy zwarta, rurkowata stożkowa struktura (zrośnięte pręciki), skierowana mocno w dół.", "6,7,8"),
 ("Zaraza ziemniaczana na liściach: Makrofotografia. Duży, pierzasty liść pomidora. Na krawędziach i w środku blaszki widoczne rozległe, nieregularne, brązowo-czarne, zaschnięte plamy o wodnistych brzegach, otoczone bladożółtą obwódką.", "7,8,9"),
 ("Papryka słodka (Kształt typu Blok): Idealnie geometryczny, grubościenny owoc o kształcie sześcianu z czterema wyraźnymi, wypukłymi komorami na samym dole. Skórka nienaturalnie lśniąca, gładka, w kolorze głębokiej czerwieni. Gruba, zielona szypułka.", "8,9"),
 ("Papryka Chili (Cayenne): Krzak oblepiony dziesiątkami bardzo długich, cienkich, pomarszczonych, ostro zakończonych strąków. Strąki sterczą pionowo w górę lub zwisają łukowato, we wszystkich fazach przejścia kolorystycznego: od zieleni, przez pomarańcz, do ognistej czerwieni.", "8,9,10"),
 ("Kwitnące Ziemniaki: Gęsty łan ciemnozielonych, szorstkich, głęboko żyłkowanych liści ułożonych kaskadowo. Nad nimi wznoszą się proste, sztywne łodyżki z pięciopłatkowymi, białymi kwiatami, w których centrum znajduje się bardzo wyraźny, jaskrawożółty stożek.", "6,7"),
 ("Stonka ziemniaczana (Makro): Owad siedzący na nadgryzionym liściu ziemniaka. Kształt wypukłej, błyszczącej kropli. Pancerz jest jaskrawo pomarańczowy, a na twardych pokrywach skrzydeł biegnie dokładnie dziesięć idealnie równych, podłużnych, czarnych pasków.", "5,6,7,8"),
 ("Bakłażan (Oberżyna): Masywny owoc w kształcie idealnej, obłej kropli. Skórka ekstremalnie błyszcząca, jak polakierowana, w kolorze tak głębokiego, ciemnego fioletu, że wpada w czerń. U góry otoczony kolczastym, zielonym, sztywnym kielichem.", "8,9"),
 ("Podwiązywanie w szklarni: Sztywny, owłosiony pęd pomidora owinięty luźno grubym, szarym, polipropylenowym sznurkiem rolniczym. Sznurek biegnie pionowo prosto do dachu stelaża z ocynkowanych rurek, w tle rozmyta folia tunelowa.", "5,6,7"),
 # --- Skarby Ziemi (Korzeniowe i Cebulowe) ---
 ("Wyrwana Marchewka: Świeżo wyrwany z ziemi, długi, stożkowy, jaskrawopomarańczowy korzeń. Skórka ma delikatne, poprzeczne, cienkie bruzdy i oblepiona jest grudkami czarnej, wilgotnej ziemi. Na samej górze gęsta czupryna pierzastej naci.", "8,9,10"),
 ("Cebula Dymka w redlinie: Powierzchnia brązowej gleby. Do połowy z ziemi wystaje okrągła, sucha, złoto-miedziana łuska cebulki. Z jej czubka strzelają w górę idealnie proste, puste w środku, sztywne, rurkowate szczypce o woskowym, niebiesko-zielonym nalocie.", "4,5,6"),
 ("Czosnek Zimowy (Główka): Przecięta w poprzek duża główka czosnku leżąca na drewnianej desce. Geometria ukazuje wyraźne, łezkowate ząbki otoczone fioletowo-białą, papierową łuską, ciasno zaciśnięte wokół centralnego, twardego rdzenia.", "6,7"),
 ("Burak Ćwikłowy: Kształt spłaszczonej z góry i z dołu kuli o barwie krwistego, bardzo ciemnego burgunda. Z samej góry wyrastają długie, fioletowo-czerwone ogonki liściowe zakończone błyszczącymi, ciemnozielonymi liśćmi z mocno czerwonym użyłkowaniem.", "8,9,10"),
 ("Seler Korzeniowy (Bulwa): Niezwykle chropowata, guzowata, kulista bryła w kolorze brudnego, jasnego beżu. Dolna połowa pokryta plątaniną grubych, ciemnych i poskręcanych korzeni przypominających pajęczynę.", "9,10,11"),
 ("Pory na grządce: Rząd roślin przypominających grube, geometryczne cylindry. Dolna część łodygi ukryta w ziemi jest śnieżnobiała, wyżej płynnie przechodzi w chłodną zieleń, a na samej górze rozkłada się w płaskie, sztywne, wygięte w łuk szerokie liście.", "9,10,11,12"),
 ("Rzodkiewki tuż przed zbiorem: Ziemia skompresowana do pęknięć. Z pęknięć mocno wystają idealnie okrągłe, gładkie, jaskrawoczerwone piłeczki. Krótkie, szorstkie, owłosione liście o powcinanych brzegach leżą niemal płasko na glebie.", "4,5,6,9"),
 ("Śmietka Cebulanka (Szkodnik): Przekrój zepsutej cebuli. Miąższ jest szklisty, brązowawy i rozkładający się. W gniciu wiją się mikroskopijne, kremowo-białe, beznogie, grube larwy przypominające ziarenka ryżu.", "5,6,7"),
 ("Przerywanie siewek (Kluczowy błąd): Zbliżenie na dłoń, która wyciąga pęczek zgniecionych, miniaturowych roślinek marchewki z mikroskopijną pomarańczową niteczką korzenia. W ziemi, w równych, 3-centymetrowych odstępach zostają tylko pojedyncze, silne, równe siewki.", "4,5,6"),
 ("Pietruszka korzeniowa vs Pasternak: Dwa ułożone obok siebie korzenie. Pietruszka ma korzeń gładki, biały i płaską nasadę u góry. Pasternak jest większy, kremowy, z widocznym rdzawym nalotem u góry i głębokim wklęśnięciem w miejscu po liściach.", "9,10,11"),
 # --- Olbrzymy i Pnacza (Dyniowate i Ogorki) ---
 ("Ogórek Śremski: Krótki, cylindryczny, jasnozielony owoc ze stłumionymi, jasnymi smugami wzdłuż. Skórka jest gęsto pokryta bardzo wyraźnymi, sterczącymi, chropowatymi, drobnymi brodawkami zakończonymi białym lub czarnym kolcem.", "6,7,8"),
 ("Kwiat żeński z zawiązkiem: Ogromny, delikatny, pognieciony żółty kwiat w kształcie dzwonka. U samej jego podstawy znajduje się mikroskopijny, kilkucentymetrowy, kolczasty mini-ogórek. Ostre, zakręcone wąsy czepne oplatają tło.", "6,7,8"),
 ("Krzew Cukinii: Potężna roślina niepnąca. Rozeta ogromnych, powycinanych, owłosionych liści. Na liściach widoczne są naturalne, srebrzysto-szare plamy wzdłuż nerwów (często mylone z chorobą). W centrum ukryty prosty, ciemnozielony, błyszczący owoc w kształcie maczugi.", "6,7,8,9"),
 ("Dynia Hokkaido (Red Kuri): Kształt owocu przypominający pękatą, asymetryczną cebulę lub łzę. Skórka gładka, twarda, matowa, w ekstremalnie intensywnym, jaskrawo-pomarańczowo-czerwonym kolorze. Gruby, suchy, skorkowaciały i szary ogonek.", "9,10"),
 ("Dynia Olbrzymia (Tekstura): Ogromna, spłaszczona kula w kolorze wyblakłej, łososiowej pomarańczy. Powierzchnia głęboko pofalowana w symetryczne żebra, gęsto pokryta chropowatymi naroślami i grubą siatką zbliznowaceń na skórce.", "9,10"),
 ("Mączniak Prawdziwy: Duży, płaski liść cukinii (ciemnozielony). Na jego powierzchni znajdują się wyraźne, białe, proszkowate, okrągłe plamy, wyglądające dokładnie jak nierównomiernie rozsypana garść drobnej mąki lub wapna. Plamy łączą się ze sobą.", "7,8,9"),
 ("Uprawa pionowa ogórków: Półprzezroczysty namiot z agrowłókniny. Równe rzędy wznoszących się pionowo, cienkich, owłosionych pędów ogórka, z których każdy sztywno owija się wokół własnego, naprężonego z góry na dół białego sznurka.", "6,7,8"),
 ("Patison (Scallop Squash): Owoc o kosmicznym kształcie spłaszczonego dysku lub UFO. Środek płaski lub lekko wypukły, a brzegi mocno i regularnie pofalowane. Kolor idealnie gładkiej, mlecznej bieli lub żółci.", "7,8,9"),
 ("Nasiona wewnątrz dyni: Przekrojona na pół ogromna dynia. W jaskrawopomarańczowym miąższu znajduje się pusta komora z wielką gęstwiną lepkich, śliskich, żółtawych włókien, w które zaplątane są setki dużych, płaskich, owalnych i białych pestek z twardą łupiną.", "9,10,11"),
 ("Liść dyniowy w zbliżeniu: Ogromny, rozłożysty, klapowany liść. Ekstremalne makro na blaszki i łodygę, ukazujące gęstą szczecinę sztywnych, kłujących, półprzezroczystych, stożkowych włosków pokrywających absolutnie każdą zieloną część rośliny.", "6,7,8,9"),
 # --- Zielen i Chrupkosc (Liسciaste, Kapustne, Straczkowe) ---
 ("Sałata Masłowa (Rozeta): Zwarta, niska półkula. Liście niezwykle gładkie, wiotkie, o niemal woskowej, miękkiej teksturze i żółtawo-jasnozielonym kolorze, łagodnie zachodzące na siebie i luźno tworzące jasny środek główki.", "4,5,6,9,10"),
 ("Kapusta Głowiasta Biała: Potężna, ekstremalnie twarda, zbita, ciężka kula. Zewnętrzne liście w kolorze niebiesko-zielonym (z siwym nalotem), sztywne, grube, z wyraźnymi, białymi, wystającymi, wypukłymi nerwami przypominającymi grubą siatkę naczyń krwionośnych.", "8,9,10"),
 ("Bielinek Kapustnik (Gąsienice): Postrzępiony, wyjedzony aż do nerwów liść kapusty. Na nim żerują charakterystyczne gąsienice: tło ciała zielonkawo-żółte, z wzdłużnymi paskami, gęsto pokryte czarnymi kropkami i drobnymi, szczeciniastymi włoskami.", "6,7,8"),
 ("Jarmuż (Mroźny Poranek): Wysoka, gruba łodyga, z której wyrastają pionowo potężne, niezwykle silnie pokarbowane liście w głębokim, sino-niebieskawym kolorze, których brzegi pokryte są drobnymi, lodowymi igłami porannego szronu.", "10,11,12"),
 ("Bób (Strąki i pędy): Sztywna, mięsista, pionowa i kanciasta łodyga bez wąsów czepnych. Z kątów liści sterczą grube, mięsiste, welurowe w dotyku, potężne zielone strąki, odznaczające się na tle matowych liści.", "6,7"),
 ("Fasola Szparagowa (Żółta karłowa): Niski, gęsty, krępy krzaczek. Spod parasola trójdzielnych, szorstkich liści zwisają masowo idealnie proste, długie, gładkie, bezwłókniste, jaskrawożółte strąki o okrągłym przekroju.", "7,8"),
 ("Groch Siewny (Wąsy): Wiotkie, zygzakowate, błękitnawo-zielone pędy wspinające się po siatce. Na końcach gładkich, okrągławych liści wyrastają długie, sprężynkowato zakręcone wąsy czepne, ciasno zaciskające się wokół zardzewiałego drutu.", "5,6"),
 ("Brokuł (Faktura Róży): Ścisły, zbity kwiatostan ułożony w ciemnozieloną, matową kopułę. Makro tekstury: powierzchnia składa się z tysięcy mikroskopijnych, zamkniętych pączków kwiatowych, tworzących ułożony promieniście, drobnoziarnisty wzór przypominający gęsty mech.", "6,7,8,9"),
 ("Koper Ogrodowy: Puste, niebiesko-zielone, woskowate, pionowe łodygi. Liście ekstremalnie nitkowate. Na szczycie pędów rozpostarty jest ogromny, płaski baldach złożony z dziesiątek rozgałęzionych, maleńkich, żółtych kwiatuszków przypominających parasol bez materiału.", "6,7,8"),
 ("Szpinak Nowozelandzki: Roślina płożąca. Liście mięsiste, bardzo grube, w kształcie trójkąta. Skórka jest intensywnie ciemnozielona i z wierzchu gęsto pokryta mikroskopijnymi, błyszczącymi, krystalicznymi pęcherzykami.", "6,7,8,9"),
 # --- Praca u Podstaw (Agrotechnika i Ochrona) ---
 ("Przekopywanie szpadlem (Ostra Skiba): Zbliżenie przy ziemi. Lśniąca, ostra stalowa łyżka szpadla zagłębiona z siłą buta roboczego. Wyrzucona ziemia leży w nierównych, potężnych, czarnych i błyszczących bryłach odwróconych spodem do góry (zimowa orka), nietkniętych grabiami.", "10,11"),
 ("Wysiew punktowy z dłoni: Brudna od ziemi, poorana pracą dłoń. Pomiędzy kciukiem a palcem wskazującym spoczywają trzy mikroskopijne, czarne, geometrycznie okrągłe nasiona, gotowe spaść do idealnie prostej, zrobionej trzonkiem rowka o głębokości 2 cm.", "3,4,5"),
 ("Pikowanie rozsady (Pikownik): Na czarnym, gładkim piasku leży drewniany, stożkowy, rzeźbiony patyk. Tuż obok niego w przygotowaną, głęboką okrągłą dziurę wsuwana jest ostrożnie siewka pomidora, zakopywana pod same liścienie.", "4,5"),
 ("Ściółkowanie słomą na grządce: Geometrycznie czysty, bezchwastowy rząd sadzonek truskawek lub czosnku. Pomiędzy krzaczkami równomiernie rozłożona jest gruba (5 cm) warstwa chrupiących, złotych, błyszczących, pustych w środku rurek suchej, twardej słomy zbożowej.", "4,5,6"),
 ("Płodozmian (Przekrój wizualny): Dzielony kadr ogrodu na cztery strefy. 1. Ziemia czarna. 2. Wybujałe, wysokie zielone rośliny (strączkowe). 3. Gęsty dywan okopowych korzeni z liśćmi. 4. Ogromne liście kapusty. Graficzna granica między strefami na tle jednego, słonecznego ogrodu.", None),
 ("Taśma kroplująca T-Tape: Płaska, matowo-czarna taśma z niebieskim paskiem rozwinięta na jasnej, wyschniętej wiórowato ziemi. Z małych, prostokątnych szczelin w taśmie co 20 cm wypływa i powoli nasiąka okrągła, czarna, mokra plama w kształcie aureoli wokół młodej rzodkiewki.", "5,6,7,8,9"),
 ("Biała Agrowłóknina (P17) na pałąkach: Z daleka: Rząd niskich, zaokrąglonych, tunelowych półkoli z drutu stalowego przykrytych zwiewną, przepuszczającą światło białą tkaniną z mikro-krateczką, naprężoną na wietrze i przyciśniętą do brzegów brązową ziemią.", "3,4,9,10"),
 ("Czarna folia i nacięcia krzyżowe: Powierzchnia równej, głęboko czarnej agrotkaniny. W materiale wypalone lub wycięte ostrym nożem równe nacięcia w kształcie litery X, z których wyrasta zwarta kępka zdrowej, ciemnozielonej sałaty.", "4,5,6"),
 ("Mszyce na pędzie bobu: Ekstremalne zbliżenie (makro). Młody, jeszcze nie rozwinięty, wiotki pęd na szczycie rośliny. Cała jego łodyga o długości 3 centymetrów jest absolutnie szczelnie oblepiona setkami czarnych, małych, obłych, nieruchomych owadów, obok których stacjonuje czerwona biedronka z 7 kropkami.", "5,6"),
 ("Zbiór do wiklinowego kosza: Kosz upleciony z grubej, szarobrązowej, chropowatej wikliny, stojący na trawniku. Wnętrze jest chaotycznie, ale po brzegi wypchane warzywami z ziemią: karbowany jarmuż wychyla się za brzeg, pod nim sterczy czerwony burak, błyszcząca cukinia i kilka asymetrycznych pomidorów leżących na zielonej naci.", "7,8,9,10"),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT,)).fetchone()
conn.close()
if row:
    print("UWAGA: kategoria '%s' juz istnieje (id=%s) - przerywam." % (CAT, row['id']))
else:
    cid = add_category(CAT)
    for tekst, mies in WARZYWNIK:
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
