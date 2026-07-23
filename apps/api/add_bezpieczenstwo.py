# -*- coding: utf-8 -*-
from src.db.database import add_category, add_topic, get_connection

CAT = "Bezpieczeństwo i Infrastruktura"

BEZPIECZENSTWO = [
 # --- Instalacje Elektryczne i Pomiary ---
 ("Rozdzielnica zmodernizowana (Przejście z TN-C na TN-S): Otwarta biała skrzynka natynkowa. Geometria wnętrza: szyna PE z podpiętymi przewodami w izolacji zielono-żółtej jest fizycznie oddzielona od szyny N z niebieskimi. Obok nowoczesne, czarne wyłączniki różnicowoprądowe (RCD).", None),
 ("Pomiar rezystancji izolacji (L-PE, L-N, N-PE): Zbliżenie (makro) na duży, żółty, cyfrowy miernik z podświetlanym na zielono ekranem LCD. Dwie grube sondy pomiarowe (czerwona i czarna) dotykają odizolowanych, błyszczących miedzianych żył przewodu zasilającego.", "4,5"),
 ("Badanie ciągłości przewodów ochronnych: Stalowa obudowa rozdzielnicy. Dłonie w grubych, pomarańczowych rękawicach dielektrycznych trzymają ostre, stalowe końcówki próbnika precyzyjnie przytknięte do uziomu.", "4,5"),
 ("Zespolona dokumentacja techniczna: Stół z surowego drewna, na nim rozłożony papierowy protokół odbioru instalacji z rzędami wyraźnych tabel. Obok leży profesjonalny stalowy długopis oraz pieczątka z uprawnieniami dozoru i eksploatacji (E i D).", None),
 ("Zabezpieczenie nadprądowe: Rząd nowoczesnych, jasnoszarych bezpieczników modułowych zamontowanych na metalowej szynie DIN. Dźwigienki podniesione w pozycję ON, pod spodem widoczne czerwone wskaźniki załączenia stanu.", None),
 ("Ziemny kabel zasilający (YKY): Przekrój poprzeczny głębokiego, pionowego wykopu w ziemi. Na samym dnie gruba warstwa żółtego, czystego piasku, na niej ułożony falisty gruby, czarny kabel, owinięty z góry jaskrawą, niebieską folią ostrzegawczą.", "4,5,6,7,8,9,10"),
 ("Prawidłowe uziemienie altany: Długa, stalowa szpila (uziom krzyżowy) wbita do połowy w brunatną, zbitą ziemię. Do jej szczytu przykręcony jest masywną śrubą błyszczący, miedziany przewód o bardzo grubym, plecionym splocie.", "4,5,6,7,8,9,10"),
 ("Niebezpieczna degradacja izolacji: Makro na stary, popękany, wyblakły od słońca biały przewód. Z geometrycznych pęknięć zewnętrznej powłoki wystają skorodowane, pokryte zielonkawą patyną druty miedziane na tle wilgotnej, porowatej ściany.", None),
 ("Puszka hermetyczna na zewnątrz: Jasnoszara, kwadratowa puszka natynkowa przymocowana do chropowatej, drewnianej elewacji. Widoczne elastyczne, czarne gumowe dławiki na wejściach przewodów. Na gładkim plastiku kropelki deszczu odbijające światło.", None),
 ("Gniazdo bryzgoszczelne (IP44): Kompaktowe gniazdko osadzone na kafelkach, chronione półprzezroczystą, niebieskawą klapką sprężynową. Spod uchylonej klapki wystaje solidny, mosiężny bolec uziemiający.", None),
 # --- Siec Wodociagowa i Sanitariaty ---
 ("Awaria głównej sieci wodociągowej: Głęboki wykop w mokrej glinie. Z grubej, pękniętej wzdłużnie niebieskiej rury PE tryska pod dużym ciśnieniem fontanna spienionej, zabrudzonej ziemią wody, zalewając rów.", "3,4"),
 ("Zimowanie instalacji (Zasuwa odcinająca): Ciężki, mosiężny zawór kulowy z długą, czerwoną rączką, zainstalowany w okrągłej, betonowej studzience głęboko pod warstwą szronu i ziemi.", "9,10,11"),
 ("Łazienka w altanie (Nowoczesny standard): Wnętrze ostre jak brzytwa. Ściana pokryta wielkoformatowymi, śnieżnobiałymi płytkami na wysoki połysk, geometrycznie zestawiona z minimalistyczną, całkowicie matowo-czarną baterią umywalkową.", None),
 ("Odwodnienie dachu i rynny: Idealnie prosta, miedziana rynna z wyraźną patyną, przymocowana do drewnianego okapu. Woda spływa z niej lśniącym, pionowym strumieniem wprost do ciemnozielonej, plastikowej beczki na deszczówkę.", "4,5,6,7,8,9"),
 ("Podgrzewacz pojemnościowy (Bojler): Gładki, emaliowany na biało cylinder zawieszony pionowo na ceglanej ścianie, z bardzo wyraźnym, okrągłym analogowym zegarem temperatury z czerwoną wskazówką.", None),
 ("Wodomierz ogrodowy: Mosiężny licznik pokryty kroplami rosy. Pod szklaną szybką widoczny obracający się, czerwony, zębaty wiatraczek oraz rząd bardzo wyraźnych, białych cyfr na czarnym tle.", "4,5,6,7,8,9,10"),
 ("Zewnętrzny zawór czerpalny: Matowo-czarny kranik wystający bezpośrednio z surowej elewacji altany, do którego szybkozłączką szczelnie podłączony jest jaskrawo pomarańczowy, karbowany wąż ogrodowy.", "4,5,6,7,8,9,10"),
 ("Syfon i odpływ: Czarny, matowy, geometryczny syfon butelkowy pod wiszącą, białą, kwadratową umywalką. Brak szafki – rury są całkowicie odsłonięte na tle gładkiej, jasnej fugi.", None),
 ("Przydomowe szambo/zbiornik: Płaski, ciemnozielony, okrągły właz wykonany z grubego plastiku z silnym, promienistym żebrowaniem antypoślizgowym, idealnie zlicowany z krótko skoszonym trawnikiem.", None),
 ("Uszkodzony wężyk zbrojony: Makrofotografia stalowej, drobnej plecionki wężyka ciśnieniowego pod zlewem. Plecionka jest rozerwana, a z wnętrza przez oczka siatki pęcznieje czarna guma, tworząc niebezpieczny balonik.", None),
 # --- Smart ROD i Automatyka ---
 ("Panel zarządzania ogrodem: Ekran zamocowany na pionowej desce altany. Wyświetla ciemny, nowoczesny interfejs z układem kafelkowym, zawierający wyraźne suwaki dla Oświetlenia, wskaźniki Wilgotności Gleby oraz mały podgląd z kamery na żywo.", None),
 ("Robot koszący w akcji: Płaska, opływowa maszyna w obudowie o intensywnym, limonkowo-zielonym i czarnym kolorze (tekstura błyszczącego plastiku), precyzyjnie przycinająca idealnie równy trawnik. Z przodu włączone poziome paski białych diod LED.", "4,5,6,7,8,9,10"),
 ("Automatyczne nawadnianie kropelkowe: Cienka, matowo-czarna rurka PCV poprowadzona między brązową korą sosnową. Z małego, plastikowego emitera powoli wydostaje się krystaliczna, idealnie kulista kropla wody.", "4,5,6,7,8,9"),
 ("Inteligentny elektrozawór: Masywna, czarna skrzynka zaworowa z zieloną pokrywą ukryta w trawie. Wewnątrz kłębowisko niebieskich przewodów sterujących podłączonych do szarego modułu elektronicznego z małą, sterczącą antenką Wi-Fi.", "4,5,6,7,8,9"),
 ("Czujnik wilgotności gleby: Smukły, dwuzębny, biało-stalowy widelec (sonda) wbity pionowo w ciemną, sypką ziemię obok krzaka pomidora. Na samej górze obudowy świeci mała, jaskrawozielona dioda.", "5,6,7,8,9"),
 ("Stacja pogodowa na dachu: Biały, plastikowy wiatromierz w kształcie trzech półokrągłych miseczek, obracający się niezwykle szybko na tle ciemnogranatowego, burzowego nieba.", None),
 ("Kamera monitoringu zewnętrznego: Czarna, podłużna (tubowa) kamera z wyraźnym pierścieniem czerwonych diod podczerwieni (IR) ułożonych w okrąg, zamontowana mocno pod drewnianą podbitką dachu altany.", None),
 ("Smart żarówka na tarasie: Klasyczna, kuta latarenka ścienna. Wewnątrz szklanego klosza inteligentna żarówka LED świeci ekstremalnie ciepłym, bursztynowym światłem z ostro zarysowanymi, widocznymi w środku spiralnymi żarnikami (filament).", None),
 ("Czujnik ruchu przy ścieżce: Niewielka, prostokątna, grafitowa obudowa czujki umieszczona bardzo nisko przy ziemi, emitująca niewidoczny dla oka, lekko błękitnawy snop skanujący przestrzeń jasnego, żwirowego chodnika.", None),
 ("Stacja dokująca kosiarki: Czarna, płaska, żebrowana platforma wkopana stabilnie w trawnik. Obok stacji wystaje krótki słupek z zielonym światłem, a na platformę powoli wjeżdża przednie, małe gumowe koło limonkowego robota.", "4,5,6,7,8,9,10"),
 # --- Ochrona Altany, P.Poz. i Antywlamaniowa ---
 ("Gaśnica proszkowa w altanie: Jaskrawoczerwona, błyszcząca, cylindryczna butla. Cechą kluczową jest okrągły manometr ciśnieniowy obok rączki, gdzie czarna wskazówka znajduje się centralnie na zielonym polu. Powieszona na jasnej ścianie z OSB.", None),
 ("Kłódka trzpieniowa (antywłamaniowa): Potężna, geometrycznie prostokątna, matowo-stalowa kłódka. Hartowany, gruby, poziomy trzpień spina na sztywno dwa bardzo grube ogniwa zardzewiałego, spawanego łańcucha na bramie.", None),
 ("Roleta antywłamaniowa: Pancerz z szerokich, aluminiowych profili w ciemnym kolorze szarego antracytu, opuszczony dokładnie do połowy prostokątnego okna. Bardzo wyraźne poziome linie i solidne prowadnice po bokach.", None),
 ("Wykrywacz tlenku węgla (Czad): Małe, okrągłe, białe urządzenie z podświetlanym na lodowaty błękit wyświetlaczem cyfrowym pokazującym 000. Zamontowane na ścianie tuż nad solidnym, żeliwnym piecykiem (kozą).", "10,11,12,1,2,3"),
 ("Prawidłowy komin izolowany: Podwójna rura (komin systemowy) ze stali kwasoodpornej, o lśniącej jak lustro powierzchni, wyprowadzona idealnie pionowo ponad połać dachu pokrytego czarnym gontem bitumicznym.", "10,11,12,1,2,3"),
 ("Wzmocnione drzwi wejściowe: Ciężkie, gładkie skrzydło drzwiowe o teksturze orzecha włoskiego. We framugę i krawędź boczną wpuszczony jest lśniący, stalowy, wielopunktowy zamek z kilkoma wysuniętymi okrągłymi bolcami.", None),
 ("Kraty kute w oknach: Grube, kwadratowe w przekroju stalowe pręty połączone prostopadle, pomalowane na czarny, chropowaty mat. Mocowania zagłębione i zabetonowane bezpośrednio w murowanej, ceglanej ościeży.", None),
 ("Sejf podłogowy: Kwadratowa, gruba, stalowa klapa z idealnie spasowanymi szczelinami, z wpuszczonym okrągłym zamkiem szyfrowym. Zakamuflowana – ukryta do połowy pod odchylonym, szarym dywanikiem na drewnianej podłodze.", None),
 ("Oświetlenie zalewowe (Naświetlacz LED): Płaski, czarny reflektor z potężną, pojedynczą żółtą matrycą COB w centrum. Emituje ostry, twardy snop jaskrawego, niebiesko-chłodnego światła w gęstą, czarną noc.", "10,11,12,1,2"),
 ("Czujnik dymu na suficie: Dyskretny, płaski, biały cylinder przykręcony do surowej, poprzecznej belki dachowej. Obudowa z otworami wentylacyjnymi z boku, na środku jedna, ostro świecąca na czerwono mała dioda awaryjna.", None),
 # --- Przestrzen Wspolna i Architektura Zewnetrzna ---
 ("Brama wjazdowa do sektora: Bardzo wysoka, dwuskrzydłowa brama zbudowana z szerokich stalowych profili (srebrny ocynk). Na jednym skrzydle duża, żółto-czarna tablica z piktogramem ostrzegawczym, pośrodku zamknięty potężny rygiel przesuwny.", None),
 ("Ogrodzenie z siatki powlekanej: Zielona, elastyczna siatka pleciona o oczkach w kształcie idealnych rombów, sztywno naciągnięta za pomocą grubego drutu przechodzącego przez okrągły słupek przelotowy z plastikową przelotką.", None),
 ("Skrzynka energetyczna (Złącze kablowe): Jasnoszara, wąska i wysoka szafka z tworzywa sztucznego stojąca samotnie przy alejce. Drzwiczki zamknięte na specjalny klucz trójkątny, oznakowane wielką, czerwoną błyskawicą ostrzegawczą.", None),
 ("Ścieżka z płyt ażurowych (Jumbo): Szare, betonowe płyty ułożone w rząd, tworzące geometryczną kratownicę. Puste przestrzenie idealnie i równo zarośnięte krótko przystrzyżoną, jaskrawą, zieloną trawą.", "5,6,7,8,9"),
 ("Palisada oporowa ze skarpą: Rząd ciasno zestawionych pionowo, okrągłych, drewnianych palików o powtarzalnej wysokości, z bardzo wyraźnym rysunkiem słojów drewna. Palisada powstrzymuje usypaną, wysoką warstwę ciemnobrązowej ziemi.", None),
 ("Tablica ogłoszeń i komunikatów: Rustykalna, drewniana witryna pod zamkniętą szybą z odbiciami światła. W środku przypięta metalowymi pinezkami jaskrawa infografika z tekstem i symbolem przekreślonego kranu (komunikat awaryjny).", None),
 ("Oznakowanie alejek sektora: Pionowy, ciemnozielony metalowy słupek, do którego przymocowano niewielką, odblaskową, białą tabliczkę z czarnym, prostym i grubym numerem alejki, odcinającą się ostro od tła liści.", "4,5,6,7,8,9,10"),
 ("Mostek nad rowem melioracyjnym: Lekko wygięta w łuk konstrukcja. Pokład wykonany z grubych, głęboko ryflowanych desek kompozytowych w kolorze ciemnego drewna, zabezpieczony obustronnie prostą, spawaną, czarną barierką.", None),
 ("Kompostownik ogólnoogrodowy (Wielkogabarytowy): Potężna infrastruktura. Wysokie na dwa metry prostokątne boksy, których ściany zbudowano z szerokich, poziomych desek z przerwami. Konstrukcja szczelnie wypchana zwałami ściętych, surowych gałęzi.", "3,4,10,11"),
 ("Stacja segregacji odpadów (Pojemniki): Idealnie uporządkowany rząd czterech czystych, pionowych dzwonów do recyklingu z otworami wrzutowymi. Kontrastowe kolory w jednej linii: jaskrawożółty, błękitny, zielony i ciemnobrązowy, stojące na płaskiej, czystej wylewce z szarego betonu.", None),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT,)).fetchone()
conn.close()
if row:
    print("UWAGA: kategoria '%s' juz istnieje (id=%s) - przerywam." % (CAT, row['id']))
else:
    cid = add_category(CAT)
    for tekst, mies in BEZPIECZENSTWO:
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
