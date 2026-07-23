# -*- coding: utf-8 -*-
from src.db.database import add_category, add_topic, get_connection

CAT = "Smart Ogród (Automatyka na Działce)"

SMART = [
 # --- Mozg Operacji i Czujniki (Centrale i Monitoring) ---
 ("Ekran centrali w altanie: Ciemny, matowy tablet ścienny wyświetlający zaawansowany, kafelkowy interfejs z wykresami liniowymi i okrągłymi wskaźnikami poziomu baterii, osadzony w idealnie gładkiej, wydrukowanej z żywicy, szarej matowej ramce.", None),
 ("Zewnętrzny czujnik temperatury: Półprzezroczysta, idealnie gładka obudowa wykonana z żywicy światłoutwardzalnej, zamontowana pod drewnianym dachem, przez którą ledwo przenikają zarysy ciemnozielonej płytki PCB.", None),
 ("Czujnik wilgotności gleby: Sztywny, dwuzębny widelec z czarnego tworzywa, w całości wbity w zbitą, ciemną ziemię. Na górze wystaje kwadratowa kostka z migającą, jaskrawozieloną diodą LED na tle szorstkich liści.", "5,6,7,8,9"),
 ("Stacja pogodowa na maszcie: Minimalistyczny, biały walec z obracającym się anemometrem (trzy półkoliste miseczki) i miniaturowym, czarnym panelem słonecznym, zamocowany na lśniącym, aluminiowym maszcie na tle nieba.", None),
 ("Czujnik otwarcia furtki (Kontaktron): Dwa małe, białe, prostokątne magnesy. Jeden przykręcony na sztywno do rdzewiejącego stalowego słupka, drugi do ruchomej ramy zielonej furtki. Bardzo wąska, równa szczelina między nimi.", None),
 ("Kamera z panelem solarnym: Czarna, podłużna kamera tubowa z okiem obiektywu mocno odbijającym światło. Tuż nad nią płaski, prostokątny, czarny panel fotowoltaiczny pokryty cienką, geometryczną siatką srebrnych linii.", None),
 ("Wzmacniacz sygnału Wi-Fi (Mesh): Biała, błyszcząca, geometryczna kostka z dwiema pionowymi, grubymi antenami, ukryta w półotwartej szafce na tle surowych, sosnowych desek, otoczona plątaniną kabli.", None),
 ("Czujnik jakości powietrza: Owalne urządzenie z szerokim, perforowanym, aluminiowym grillem wiszące na gwoździu. Wnętrze grilla rozświetla się od spodu gradientowym, płynnym, fioletowo-niebieskim chłodnym światłem.", None),
 ("Brama sieciowa (Gateway Zigbee): Niewielki, matowo-czarny, płaski krążek leżący na drewnianym stole, spięty z płaskim, białym kablem USB. Wokół dolnej krawędzi krążka biegnie pulsujący, subtelny błękitny pierścień świetlny.", None),
 ("Pomiar nasłonecznienia (Luksomierz): Szklana, idealnie przezroczysta półkula przypominająca bioniczne oko, nałożona na szarą obudowę. W centrum pod szkłem błyszczy kwadratowy, krzemowy element przypominający mikroprocesor.", None),
 # --- Roboty Koszace i Pielegnacja Trawnika (sezon koszenia) ---
 ("Robot w gęstej trawie: Niska, opływowa maszyna kosząca o głębokiej, limonkowo-zielonej barwie obudowy, połączonej z matowo-czarnymi panelami z boku. Przedziera się z impetem przez bardzo gęstą, mokrą od porannej rosy trawę.", "4,5,6,7,8,9,10"),
 ("Stacja dokująca w deszczu: Szeroka, płaska, czarna platforma wkopana w ziemię, posiadająca wyraźne żebrowania antypoślizgowe. Na jej śliskiej powierzchni rozbijają się idealnie okrągłe krople ulewnego deszczu.", "4,5,6,7,8,9,10"),
 ("Stalowe ostrza koszące (Makro): Ekstremalne zbliżenie na podwozie robota. Czarny, wirujący dysk ze śrubami centralnymi, do którego zamocowano trzy małe, ekstremalnie ostre, srebrne nożyki przypominające żyletki pokryte sokiem z trawy.", "4,5,6,7,8,9,10"),
 ("Przewód ograniczający: Przekrój geologiczny przez trawnik (makro). Tuż pod zbitymi korzeniami darni znajduje się cienki, miedziany kabelek w grubej, jaskrawozielonej izolacji, przytwierdzony do ziemi czarnym, wbijanym śledziem z plastiku.", "4,5,6,7,8,9,10"),
 ("Czujnik zderzeniowy w akcji: Przód zielono-czarnego robota, który delikatnie opiera się o pień starej jabłoni pokryty głęboko spękaną, szarą korą. Widoczna krawędź czarnego zderzaka maszynki uginająca się na ułamek milimetra.", "4,5,6,7,8,9,10"),
 ("Zimowanie robota (Czyszczenie): Wnętrze warsztatu, chłodne światło. Czysty, odwrócony na plecy robot na stole. Potężny strumień powietrza ze sprężarki wydmuchuje chmurę pyłu ze szczelin głębokiego bieżnika potężnych, gumowych kół.", "9,10,11"),
 ("Smart-kontrola na ekranie: Ręka w skórzanej, żółtej rękawicy monterskiej trzymająca smartfon. Na ekranie widać plan ogrodu z drona z naniesionymi, wirtualnymi czerwonymi strefami wykluczenia wokół rabat kwiatowych.", "4,5,6,7,8,9,10"),
 ("Omijanie przeszkody: Jaskrawozielony robot robiący płynny, rzeźbiarski łuk na równym trawniku, z centymetrową dokładnością omijający starą, cynkową, pofalowaną konewkę leżącą na trasie.", "4,5,6,7,8,9,10"),
 ("Garaż dla robota koszącego: Miniaturowa wiata o nowoczesnej architekturze. Płaski dach pokryty cienką, grafitową blachą na rąbek, pod którym odpoczywa zielony robot, rzucając ostry cień w słoneczny dzień.", "4,5,6,7,8,9,10"),
 ("Ślad pracy na trawniku: Precyzyjne, geometryczne, równoległe pasy na przemian jasnej i ciemnej zieleni na dużym trawniku, uzyskane jak od linijki, na końcu których widać tył małej, pracującej maszyny.", "4,5,6,7,8,9,10"),
 # --- Inteligentne Nawadnianie i Retencja (sezon wegetacyjny) ---
 ("Smart elektrozawór w skrzynce: Zielona klapa skrzynki otworzona w trawniku. W głębi, na czarnej agrowłókninie, masywny mosiężny zawór połączony z szarą, geometryczną cewką elektromagnetyczną usianą błyszczącymi kroplami wody.", "4,5,6,7,8,9"),
 ("Kroplownik z kompensacją ciśnienia: Makrofotografia z boku. Do grubościennej, czarnej rury PCV wbity jest malutki, czerwony walec. U jego podstawy grawitacja formuje jedną, perfekcyjną, przezroczystą kroplę wody spadającą na zrąbki.", "4,5,6,7,8,9"),
 ("Ultradźwiękowy pomiar beczki: Wnętrze niebieskiej, chropowatej beczki. Głęboko w dole tafla spokojnej wody odbijającej światło. Pod pokrywką zamontowany mały, czarny moduł z dwoma cylindrycznymi otworami (sonar) skierowanymi w dół.", "4,5,6,7,8,9"),
 ("Sterownik nawadniania Wi-Fi: Prostokątna, szczelna puszka przykręcona do surowego muru. Przez przezroczystą klapkę widoczny jaskrawy wyświetlacz LCD oraz dziesiątki miedzianych, cienkich przewodów wpiętych w dolną listwę zaciskową.", "4,5,6,7,8,9"),
 ("Zraszacz wynurzalny w locie: Czarny cylinder wysuwający się z idealnej trawy. Szybko obracająca się dysza wystrzeliwuje geometryczny, trójwymiarowy wachlarz rozproszonej wody układającej się w kształt łuku, z mikrotęczą pod słońce.", "4,5,6,7,8,9"),
 ("Automatyczny zawór kulowy (Silnikowy): Instalacja rur mosiężnych. Na korpusie zaworu osadzona kanciasta, niebieska obudowa silnika krokowego z małym, okrągłym szkiełkiem rewizyjnym pokazującym napis OPEN na zielonej tabliczce.", "4,5,6,7,8,9"),
 ("Zautomatyzowana linia w szklarni: Równy tunel pomidorów. Bezpośrednio na suchej glebie leży lśniący, czarny i gruby wąż nawadniający. Z małych, powtarzalnych co 30 cm otworów wylewają się płaskie strumyczki, nasycając ziemię na ciemny kolor.", "3,4,5,6,7,8,9,10"),
 ("Deszczomierz elektroniczny (Kubełkowy): Pionowy przekrój szarej, stożkowej tuby. Mechanizm pokazuje czarną, wychylaną kołyskę zamontowaną na stalowej osi, która właśnie zrzuca dużą kroplę wody z zebranego wcześniej opadu.", "4,5,6,7,8,9"),
 ("Pompa zatapialna z pływakiem: Na dnie potężnego zbiornika leży ciężki, ze stali nierdzewnej, gładki walec pompy. Wyżej w wodzie unosi się pękata, pomarańczowa gruszka pływaka sterującego na naprężonym, czarnym kablu.", "4,5,6,7,8,9"),
 ("Rozdzielacz (Kolektor) wody: Rozbudowany układ trójników. Na jednej ścianie trzy wyjścia wody jedno nad drugim, zakończone nowoczesnymi, szarymi zaworami i podpiętymi pod nie jaskrawo pomarańczowymi szybkozłączkami z wężami.", "4,5,6,7,8,9"),
 # --- Oswietlenie, Atmosfera i Bezpieczenstwo ---
 ("Girlanda LED (Smart Żarówki): Gruba, pleciona, czarna lina rozwieszona nad stołem, pełna przezroczystych, całkowicie szklanych kuli. W każdym kloszu świecą hiperrealistyczne, poskręcane, jaskrawe żarniki LED o głębokiej, bursztynowej barwie.", "5,6,7,8,9"),
 ("Podświetlenie z czujnikiem ruchu: Rząd niskich, matowo-czarnych, kwadratowych słupków stojących wzdłuż żwirowej alei. Pierwsze dwa emitują w dół na biały kamień ostro zarysowany, pomarańczowy trójkąt światła, pozostałe w tle są martwe.", None),
 ("Zamek szyfrowy na kłódkę: Stalowa, masywna kłódka z hartowanym pałąkiem wpinająca zardzewiały łańcuch. Pośrodku znajduje się płaski, czarny, lśniący panel akrylowy z wyświetloną bardzo wyraźną, białą klawiaturą cyfrową.", None),
 ("Projektor laserowy na elewacji: Surowa, ciemna ściana drewnianej altany w nocy. Powierzchnię pokrywają setki niezwykle ostrych, jaskrawych, szmaragdowo-zielonych, maleńkich kropek, układających się w przestrzenną siatkę.", None),
 ("Reflektor z kamerą i głośnikiem: Solidna bryła nad drzwiami. Dwa symetryczne, płaskie panele LED COB rzucające agresywne, oślepiająco białe światło. Centralnie osadzony głęboki obiektyw kamery przypominający soczewkę aparatu.", None),
 ("Taśma LED RGB-IC pod pergolą: Drewniana oheblowana belka widziana prosto od spodu nocą. Zatopiona w półprzezroczystym silikonie płaska taśma LED generuje światło przypominające zorzę polarną – w jednym paśmie przenika się fiolet, róż i błękit.", "5,6,7,8,9"),
 ("Lampka solarna z efektem płomienia: Bambusowa laska z czarnym grotem. Szklana, prążkowana bańka, a wewnątrz siatka gęsto ułożonych, 96 mikroskopijnych pomarańczowych diod emitujących asymetryczny kształt realistycznego, migoczącego ognia.", "4,5,6,7,8,9"),
 ("Kinkiety Góra-Dół: Matowo-czarna, anodowana z aluminium, długa, kwadratowa obudowa przytwierdzona do cegły. Lampa emituje dwa identyczne, geometryczne, bardzo długie i równe stożki zimnego światła – jeden prosto pod dach, drugi na posadzkę.", None),
 ("Klawiatura dostępowa (Keypad): Cienki, kwadratowy, grafitowy panel na stalowym słupku w ostrym słońcu. Przyciski pojemnościowe w jednej płaszczyźnie, na tafli widać mikroskopijne ziarenka kurzu i jedno mocne odbicie soczewki słońca.", None),
 ("Smart gniazdko w deszczu: Zewnętrzna oprawa IP55. Lewa, niebieskawa, przezroczysta klapka sprężynowa jest podniesiona, dociskając gumowy, czarny kabel wtyczki. Wokół samej wtyczki świeci jarzący, zielony okrąg aktywnego poboru prądu.", None),
 # --- Energia, Zasilanie i Eko-Technologia (Dozor Instalatorski) ---
 ("Złącza MC4 przy panelu PV: Zbliżenie na czarną taflę krzemu ułożoną pod kątem. Głęboki fokus na grube kable solarne zakończone twardymi, ząbkowanymi, czarnymi wtyczkami, z wystającą spod nakrętki czerwoną, gumową uszczelką dławika.", None),
 ("Regulator ładowania MPPT: Duży, masywny radiator z matowego aluminium ze zintegrowanym niebieskim wyświetlaczem. Na samym dole precyzyjnie wykonane, mocne, krzyżakowe śruby zaciskające odizolowane, grube końcówki miedzianych żył przewodu zasilającego.", None),
 ("Akumulator LiFePO4 w obwodzie: Gładka, granatowa, bezszwowa obudowa akumulatora stojąca na drewnianej, wytrzymałej płycie OSB. Na miedzianych terminalach zaciśnięte kluczem masywne klemy plus i minus, a ekran BMS informuje o napięciu 13.2V.", None),
 ("Smart licznik na szynie DIN: Ujęcie wewnątrz rozdzielnicy, pełne zaciśniętych miedzianych splotów. Pośrodku malutki moduł (szerokość bezpiecznika) z matrycą OLED prezentującą żółte cyfry poboru mocy czynnej i mierzących prąd cewek wokół grubszych izolacji.", None),
 ("Stycznik modułowy (Duży Prąd): Wysoki na dwa rzędy, szaro-biały moduł ze zintegrowanym, fizycznym, czerwonym przełącznikiem (0/1/Auto). Na górnych wejściach wprowadzone pionowo grube, czarne kable fazowe sztywno utrzymywane przez śruby dokręcone z wyczuciem instalatora.", None),
 ("Kabel grzewczy do rur: Makro na grubą rurę dobiegającą ze studni. Rura jest precyzyjnie opleciona szeroką, szarą taśmą o spiralnym skoku (przewód samoregulujący z węglem), z fragmentem przykrytym aluminiową osłoną termoizolacyjną z błyszczącą warstwą zewnętrzną.", "10,11,12,1,2,3"),
 ("Bank energii z inwerterem (Magazyn): Wysoka, płaska, designerska szafa naścienna o perfekcyjnie gładkich, zagiętych na bokach obudowach krawędziach. W wąskiej szczelinie pośrodku jarzy się pionowy, zielony wskaźnik naładowania z idealnie płynnym światłem.", None),
 ("Inteligentny przekaźnik dopuszkowy: Ciasne wnętrze czarnej okrągłej puszki umieszczonej w ścianie, z której wystają kolorowe kable. Wciśnięta w wolną przestrzeń miniaturowa, niebieska kostka, na bokach której znajduje się zarysowany, śnieżnobiały, miniaturowy schemat połączeń styku z fazą.", None),
 ("Gniazdko z pomiarem mocy (Smart Plug): Zbliżenie na białą, okrągłą przejściówkę zamontowaną w zwykłym gniazdku podtynkowym. Przejściówka ma boczny, fizyczny przycisk włączenia otoczony szerokim, jarzącym, głębokim fioletowym światłem LED oznaczającym bardzo obciążony obwód instalacji.", None),
 ("Czujnik zaniku fazy/asymetrii napięcia: Zbliżenie na otwartą w altanie metalową tablicę pełną bezpieczników nadprądowych. Kluczowym elementem obrazu jest moduł, na którym dwie diody świecą na zielono, a trzecia (L3) jest wygaszona, jasno sygnalizując instalatorowi problem na przyłączu ROD.", None),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT,)).fetchone()
conn.close()
if row:
    print("UWAGA: kategoria '%s' juz istnieje (id=%s) - przerywam." % (CAT, row['id']))
else:
    cid = add_category(CAT)
    for tekst, mies in SMART:
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
