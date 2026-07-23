# -*- coding: utf-8 -*-
from src.db.database import add_topic, get_connection

# Dokladamy do ISTNIEJACEJ kategorii "Iglaki" (nie tworzymy nowej)
CAT_NAZWA = "Iglaki"

# Wiekszosc iglakow jest zimozielona (miesiace=None -> zawsze w puli).
# Konkretne miesiace tylko tam, gdzie roslina ma realny sezonowy moment
# (modrzewy zrzucajace igly, miloziab zloty jesienia, mikrobiota zmieniajaca kolor).
IGLAKI = [
 ("Sosna pospolita: Korona w kształcie rozłożystego, nieregularnego parasola. Górna część pnia pokryta łuszczącą się, jaskrawo rdzawą (pomarańczową) korą. Igły szarozielone, sztywne, wyrastające zawsze parami (po dwie) i lekko skręcone wokół własnej osi. Szyszki małe, jajowate, matowo-szare.", None),
 ("Świerk pospolity: Idealny, ostry, trójkątny stożek. Gęste gałęzie zwisające ku ziemi. Igły bardzo krótkie, kłujące, sztywne, wyrastające pojedynczo dookoła gałązki. Szyszki długie, gładkie, w kształcie cygar, zawsze zwisające pionowo w dół.", None),
 ("Jodła pospolita: Płaskie, poziome gałęzie. Igły płaskie, elastyczne, niekłujące, z góry ciemnozielone, a od spodu posiadające dwa wyraźne, śnieżnobiałe paski. Szyszki: grube, cylindryczne, zawsze stojące pionowo do góry na gałęziach (jak świeczki).", None),
 ("Modrzew europejski: Kształt stożkowaty, ale o luźnej, prześwitującej koronie. Igły niezwykle miękkie, jasne, limonkowe, zebrane w gęste pędzelki (rozety) wyrastające z krótkich wypustek na gałązkach. Małe, okrągłe szyszki przypominające drewniane różyczki. Zimą bez igieł.", "4,5,9,10"),
 ("Sosna czarna: Pokrój gęsty, masywny. Kora na pniu gruba, głęboko spękana, w kolorze ciemnoszarym, wpadającym w czerń. Igły są niezwykle długie (do 15 cm), ciemnozielone, sztywne i również rosną parami. Szyszki duże, symetryczne, błyszczące.", None),
 ("Świerk kłujący (Srebrny): Geometria perfekcyjnego, bardzo gęstego, szerokiego stożka. Igły niezwykle twarde, ostre, układające się promieniście pod kątem prostym do gałązki. Kolor igieł: jednolity, intensywnie srebrzysto-stalowo-niebieski.", None),
 ("Daglezja zielona: Pokrój podobny do świerka, ale igły są miękkie, płaskie, przy roztarciu pachnące cytrusami. Unikalna cecha wizualna szyszek: spomiędzy właściwych, brązowych łusek szyszki wystają długie, trójdzielne, trójzębne języczki (przypominające rozwidlone ogony węży).", None),
 ("Choina kanadyjska: Bardzo delikatny, płaczący pokrój z miękko przewieszającymi się końcówkami pędów. Igły drobniutkie, płaskie, ułożone w dwóch rzędach. Szyszki są miniaturowe (do 2 cm), owalne, licznie wiszące na końcach wiotkich gałązek.", None),
 ("Jodła szlachetna (Nobilis): Igły o barwie niebiesko-zielonej, bardzo wygięte w górę i do przodu (w kształcie kija hokejowego), całkowicie zakrywające górną stronę gałązki. Olbrzymie, stojące, beczkowate szyszki z mocno wystającymi, zagiętymi w dół, papierowymi wypustkami łusek.", None),
 ("Sosna żółta (Ponderosa): Ogromne, masywne drzewo. Kora pęka na wielkie, płaskie, wielokątne tarcze przypominające puzzle w kolorze żółto-pomarańczowym. Igły ekstremalnie długie (do 25 cm), wyrastające w pęczkach po trzy. Olbrzymie szyszki zaopatrzone w ostre kolce na każdej łusce.", None),
 ("Tuja (Żywotnik zachodni) 'Smaragd': Bardzo zwarty, regularny, wąski stożek bez prześwitów. Pędy płaskie, układające się wachlarzowato, całkowicie pokryte płaskimi, nakładającymi się na siebie łuskami (bez igieł) w jaskrawym, szmaragdowozielonym kolorze.", None),
 ("Cis pospolity: Gałęzie wzniesione. Igły płaskie, niekłujące, ciemnozielone na górze i matowe (bez białych pasków) od spodu. Zamiast drewnianych szyszek tworzy kuliste, jaskrawoczerwone, mięsiste osnówki (kubki) z widocznym, twardym, ciemnym nasionem w środku.", "8,9,10,11"),
 ("Cyprysik Lawsona: Pędy gęste, przypominające paprocie, spłaszczone, ale ich same końcówki delikatnie i charakterystycznie przewieszają się (opadają) w dół. Łuski niebieskawo-zielone. Szyszki mikroskopijne, okrągłe jak piłki futbolowe z wyraźnymi szwami.", None),
 ("Żywotnik wschodni (Biota/Platycladus): Różni się od tui ułożeniem pędów – u tego gatunku płaskie, wachlarzowate pędy są ułożone absolutnie pionowo (jak ustawione obok siebie kartki w książce). Szyszki grube, niebieskawe z wyraźnymi rogami na łuskach, z czasem drewniejące.", None),
 ("Jałowiec chiński 'Stricta': Bardzo gęsty, ostro zakończony stożek. Zamiast płaskich łusek posiada krótkie, szydłowate, ostre igły, które nadają gałązkom drapiącą teksturę. Całość o wyraźnie szaro-niebieskim odcieniu.", None),
 ("Cyprysowiec Leylanda: Niezwykle szybkorosnąca ściana zieleni. Pędy ułożone chaotycznie w różnych kierunkach, okrągłe w przekroju (nie płaskie jak u tui). Kolor głębokiej, matowej zieleni. Cienkie, długie przyrosty zwisające z korony.", None),
 ("Cis pośredni 'Hicksii': Pokrój wąsko-kolumnowy, w kształcie litery V lub U (wielopniowy z samego dołu). Igły wyjątkowo ciemne, błyszczące. Ściany z tego cisa są tak gęste, że przypominają solidny, architektoniczny mur bez okien.", None),
 ("Jałowiec skalny 'Skyrocket': Najwęższe iglaste drzewo. Kształt niezwykle chudej, pionowej rakiety lub igły. Łuski całkowicie przylegające do pędów, dające gładką fakturę. Kolor jednolity: bardzo jasny, srebrzysto-niebieski.", None),
 ("Jałowiec pospolity (forma kolumnowa 'Hibernica'): Pokrój wrzecionowaty (szerszy w środku, węższy na dole i na górze). Igły zebrane w okółkach po 3, bardzo kłujące, odstające, z wyraźnym białym rowkiem na wewnętrznej stronie. Granatowe szyszkojagody z siwym nalotem.", None),
 ("Cyprysik groszkowy 'Plumosa': Pędy miękkie, przypominające puszyste, pierzaste chmury. Łuski miękkie, odstające, nadające krzewowi mocno teksturowany, trójwymiarowy, pluszowy wygląd, często w lekko żółtawym lub niebieskawym zabarwieniu.", None),
 ("Jałowiec płożący 'Wiltonii': Pędy ścielące się całkowicie płasko po ziemi, pełzające. Igły i łuski bardzo drobne, mocno przylegające, tworzące szczelny, gładki, lodowo-niebieski dywan nieprzekraczający kilku centymetrów wysokości.", None),
 ("Mikrobiota syberyjska: Niski, rozłożysty krzew. Pędy płaskie, wachlarzowate, ale rosnące horyzontalnie, układające się warstwowo jedne na drugich. Jesienią i zimą łuski zmieniają kolor z zielonego na intensywnie miedziano-fioletowy (brązowy).", "10,11,12,1,2"),
 ("Jałowiec łuskowaty 'Blue Star': Rośnie w formie zwartej, nieregularnej, gwiaździstej poduszki. Krótkie pędy naszpikowane są gęstymi, bardzo twardymi, kłującymi, łuskowato-szydlastymi igłami w stalowoniebieskim, połyskującym kolorze.", None),
 ("Sosna górska (Kosodrzewina) 'Pumilio': Krzewiasty, gęsty, wielopniowy pokrój pokładający się przy ziemi. Pędy wyginają się ku górze (jak fajki). Igły krótkie, bardzo ciemnozielone, sztywne, gęsto ułożone (parami), otaczające pęd jak szczotka do butelek. Małe, niesymetryczne, czekoladowe szyszki.", None),
 ("Jałowiec pospolity 'Repanda': Płoży się bardzo szeroko. Ulistnienie to drobne, kłujące igły, które tworzą gęstą plecionkę tuż przy samej ziemi, ale z wyraźnym, soczyście zielonym, nieniebieskim zabarwieniem.", None),
 ("Cis pospolity 'Repandens': Rzadko spotykany płaski cis. Szeroko rozpostarte na boki główne gałęzie o charakterystycznym parasolowatym (horyzontalnym) ułożeniu, końcówki gałązek lekko przewieszające się w dół. Brak głównego pnia.", None),
 ("Świerk pospolity 'Nidiformis' (Gniazdkowy): Rośnie w formie gęstej, płaskiej poduszki z wyraźnym wklęśnięciem (gniazdem) na samym środku korony, co daje efekt zielonej, kolczastej miski z drobnych, jasnozielonych igieł.", None),
 ("Jałowiec rozesłany 'Nana': Tworzy ekstremalnie gęsty, sztywny, kłujący dywan formujący się na kamieniach i murkach niczym wylewające się z donicy sztywne macki. Pędy krótkie, nakładające się na siebie dachówkowato.", None),
 ("Cyprysik groszkowy 'Filifera Nana': Pokrój kopulasty. Cechą absolutnie rozpoznawalną są pędy: nitkowate, bardzo długie, nierozgałęzione, zwisające łukowato w dół, przypominające dredy lub gruby sznurek, o żywo zielonym kolorze.", None),
 ("Jałowiec sabiński: Silnie rosnący, rozłożysty krzew z pędami wznoszącymi się ukośnie. Mieszanka sztywnych igieł u nasady gałęzi z płaskimi łuskami na końcach. Charakterystyczny ostry zapach uwalnia się po roztarciu igieł.", None),
 ("Tuja zachodnia 'Danica': Rośnie samoczynnie w kształt idealnej, symetrycznej, bardzo zbitej kuli. Składa się wyłącznie z ułożonych obok siebie jak tarcze, płaskich, pionowych, jasnozielonych wachlarzyków.", None),
 ("Świerk biały 'Conica': Absolutnie geometryczny, pełny stożek bez prześwitów. Igły są tak mikroskopijne (kilka milimetrów) i gęsto upakowane, że pędów w ogóle nie widać. Przypomina idealnie przycięty szkielet rzeźbiarski z soczyście zielonego mchu.", None),
 ("Sosna gęstokwiatowa 'Umbraculifera': Pokrój podobny do klasycznego afrykańskiego baobabu. Z krótkiego pnia, o charakterystycznie łuszczącej się pomarańczowo-czerwonej korze, wyrasta w górę parasolowata, idealnie płaska (horyzontalna) z góry korona z jasnych igieł.", None),
 ("Świerk kłujący 'Glauca Globosa': Półkolista, nieco asymetryczna kępa gęstych pędów. Wszystkie cechy dużego świerka srebrnego (stalowo-niebieski kolor, ostre jak igły szczepionkowe liście) skompresowane w zbity, jeżowaty kształt nad ziemią.", None),
 ("Jodła koreańska (forma karłowa na pniu): Gęsta, płaska kula zaszczepiona na wysokości. Bardzo krótkie igły, z wierzchu zielone, a od spodu kredowobiałe (kula wydaje się migotać na biało od spodu). Wyrastają z niej miniaturowe, jaskrawo fioletowo-niebieskie, pionowe szyszki.", None),
 ("Sosna wejmutka 'Radiata': Przypomina puszystą, bardzo miękką i nieregularną chmurę złożoną z bardzo długich (do 10 cm), cieniutkich i niezwykle wiotkich igieł w jasnym, niebiesko-zielonym odcieniu, zebranych aż po 5 w pęczku.", None),
 ("Modrzew japoński 'Diana' (szczepiony): Pędy i gałązki są fantazyjnie poskręcane w spiralę niczym korkociągi. Nawet limonkowe, pęczkowate igły są pokarbowane. Rośnie jako nieregularna kula pogniecionego drutu na prostej nodze.", "4,5,9,10"),
 ("Cyprysik tępołuskowy (Hinoki) 'Nana Gracilis': Gałązki tworzą ciemnozielone, miseczkowate zagłębienia, ułożone w charakterystyczne, powykręcane na boki wachlarzyki wyglądające jak ciemne muszle morskie nałożone jedna na drugą.", None),
 ("Sosna czarna 'Brepo': Kula na długim pniu. Ze środka gęstych, zwartych, wzniesionych gałązek wystają, typowe dla sosny czarnej, niezwykle sztywne, ostre, grube i długie ciemnozielone igły, sterczące we wszystkich kierunkach na podobieństwo gigantycznego jeżowca.", None),
 ("Jałowiec łuskowaty 'Meyeri': Duży, nieregularny, wazowaty krzew o pędach sterczących sztywno pod kątem. Koniuszki gałęzi są mocno zagięte w dół. Liście to grube, mięsiste szydła wybarwione na głęboki błękit.", None),
 ("Araukaria chilijska (Igłowa Małpa): Konstrukcja fraktalna i niemal obca. Grube gałęzie rosną symetrycznie w okółkach. Pędy są w całości oblepione sztywnymi, trójkątnymi, niezwykle ostrymi niczym brzytwa łusko-igłami, dachówkowato zachodzącymi na siebie, przypominającymi najeżone ogony dinozaurów. Olbrzymie kuliste szyszki.", None),
 ("Świerk pospolity 'Inversa' / 'Pendula': Żywy wodospad igliwia. Brak przewodnika (roślina nie rośnie w górę bez podpory). Wszystkie gałęzie i pędy opadają prostopadle w dół, szorując po ziemi jak rozpuszczone włosy lub draperie grubego, zielonego materiału.", None),
 ("Cypryśnik błotny: Jedyny iglak rosnący w płytkiej wodzie. Pień u podstawy uformowany w masywne skrzydła (nabiegi korzeniowe). Wokół pnia z wody wystają zdrewniałe kolana (pneumatofory). Igły delikatne, pierzaste, jasnozielone, opadające jesienią po zrudzeniu.", "9,10,11"),
 ("Miłorząb dwuklapowy (Ginkgo): Gałęzie z krótkopędami. Liście (nie igły) w kształcie rozłożonych wachlarzy z drobnymi, równoległymi żyłkami i charakterystycznym, głębokim wcięciem na samym środku u góry. Jesienią stają się jednorodnie żarówiasto-złote.", "10,11"),
 ("Sośnica japońska (Umbrella Pine): Zamiast typowych igieł na końcach łysych gałązek tworzą się okółki (jak w konstrukcji parasola). Igły są ogromne (do 12 cm), bardzo grube, skórzaste, błyszczące, z wyraźnym rynienkowatym wgłębieniem wzdłuż całej osi.", None),
 ("Sosna himalajska (Płacząca): Z daleka wygląda, jakby zwisała z niej siwa trawa. Igły rosną po pięć, są absurdalnie długie (nawet 25 cm), bardzo wiotkie, ołowiano-szare, i zwieszają się ciężko, pionowo w dół w kaskadach. Szyszki o rozmiarze przedramienia mocno pokryte żywicą.", None),
 ("Świerk wężowy (Cranstonii / Virgata): Rzadka i łysa konstrukcja. Pędy są ekstremalnie długie, grube, wężowate, bez pędów bocznych drugiego rzędu. Przypomina szkielet porośnięty sztywnymi, ciemnozielonymi igłami zakończonymi ogromnymi pąkami.", None),
 ("Modrzewnik chiński (Złoty Modrzew): Igły w kształcie miękkich rozet rosną na sztywnych krótkopędach, dużo szersze, dłuższe i bardziej płaskie niż u modrzewia europejskiego. Szyszki przypominają małe, drewniane karczochy z trójkątnymi łuskami, które jesienią otwierają się jak kwiat lotosu i rozpadają w dłoniach.", "9,10,11"),
 ("Kryptomeria japońska: Igły bardzo ostre, szydłowate, krótkie, mocno zakrzywiające się (wygięte) do wewnątrz gałązki, tworzące kształt lisiej kity. Pień okryty wyraźnie włóknistą, odchodzącą płatami czerwono-brązową korą (jak wióry). Małe, okrągłe szyszki z kolczastymi tarczkami na końcach pędów.", None),
 ("Mamutowiec olbrzymi (Sekwojadendron): Potężny obwód pnia z bardzo grubą, czerwonobrązową (cynamonową), miękką i głęboko bruzdowaną, pionowo pękającą korą przypominającą gąbkę i struny. Igły łuskowato-szydlaste, spiczaste, odstające, szarawe. Małe, baryłkowate szyszki z twardymi, wklęsłymi tarczkami przypominającymi wyschnięte usta.", None),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT_NAZWA,)).fetchone()
conn.close()
if not row:
    print("BLAD: kategoria '%s' nie istnieje - przerywam." % CAT_NAZWA)
else:
    cid = row['id']
    przed = None
    c0 = get_connection()
    przed = c0.execute('SELECT COUNT(*) x FROM topics WHERE category_id=?', (cid,)).fetchone()['x']
    c0.close()

    for tekst, mies in IGLAKI:
        tid = add_topic(cid, tekst)
        if mies is not None:
            c = get_connection(); c.execute("UPDATE topics SET miesiace=? WHERE id=?", (mies, tid)); c.commit(); c.close()

    c = get_connection()
    po = c.execute('SELECT COUNT(*) x FROM topics WHERE category_id=?', (cid,)).fetchone()['x']
    tc = c.execute("SELECT COUNT(*) x FROM categories").fetchone()['x']
    tt = c.execute("SELECT COUNT(*) x FROM topics").fetchone()['x']
    c.close()
    print("OK dodano %d gatunkow iglakow do kategorii '%s' (id=%s)." % (len(IGLAKI), CAT_NAZWA, cid))
    print("Kategoria Iglaki: bylo %d, jest teraz %d tematow." % (przed, po))
    print("RAZEM w bazie: %d kategorii, %d tematow." % (tc, tt))
