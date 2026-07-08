# -*- coding: utf-8 -*-
from src.db.database import add_category, add_topic, get_connection

CAT = "Ekologia, Zwierzęta i Bioróżnorodność"

EKOLOGIA = [
 # --- Hotele, Schronienia i Mala Architektura dla Fauny ---
 ("Hotel dla owadów (Murarki): Architektoniczna drewniana rama zawieszona na ceglanej ścianie. Wnętrze szczelnie, geometrycznie wypełnione równo przyciętymi, okrągłymi rurkami trzcinowymi. Niektóre rurki są naturalnie zalepione z zewnątrz szarą, zaschniętą gliną.", "3,4,5"),
 ("Budka lęgowa dla sikorki: Prosta, zbita z surowych, nieoheblowanych, szorstkich desek. Centralnym punktem jest idealnie okrągły otwór wejściowy (dokładnie 32 mm średnicy), wokół którego widać ślady pazurków i leciutko zdartą korę.", "2,3,4"),
 ("Jeżownik (Schronienie dla jeża): Przestrzeń pod deskami tarasu. Sterta luźno rzuconych, suchych, brązowych liści dębu i drobnych gałązek, pod którymi ukryta jest niska, odwrócona do góry dnem drewniana skrzynka po jabłkach.", "9,10,11,12,1,2"),
 ("Poidełko dla owadów: Płytka, surowa, gliniana misa leżąca na trawie. Wewnątrz ułożona płasko mozaika z szorstkich kamieni polnych i mchu, zalanych krystaliczną wodą tylko do połowy, tworząc bezpieczne lądowiska dla pszczół.", "4,5,6,7,8,9"),
 ("Skrzynka dla nietoperzy: Bardzo płaska, wąska, pionowa skrzynka z ciemnego drewna przymocowana wysoko na pniu. Cechą absolutnie kluczową jest wejście: nie ma okrągłego otworu, lecz poziomą, wąską, ciemną szczelinę na samym dole konstrukcji.", "4,5,6,7,8,9"),
 ("Zimowisko dla ropuch (Amfibia): Kupa zbutwiałych, omszonych, grubych gałęzi leżąca w głębokim cieniu starych paproci. Pod gałęziami wykopana mała niecka wysypana gliną i zeschłymi, wilgotnymi, poczerniałymi liśćmi.", "9,10,11"),
 ("Budka dla trzmieli (Doniczka): Zwykła, odwrócona do góry dnem, terakotowa doniczka o rdzawym kolorze, wkopana do połowy w miękką ziemię. W otworze drenażowym na szczycie znajduje się wciśnięty krótki kawałek szarego peszla instalacyjnego.", "3,4,5"),
 ("Pozostawiony martwy pień: Pionowy, gruby fragment uciętego, martwego drzewa. Kora mocno odchodzi grubymi płatami. Pień jest gęsto porośnięty półokrągłymi, sztywnymi, popielatymi hubami układającymi się dachówkowato.", None),
 ("Karmnik zimowy ze słoniną: Drewniana stacja w śniegu. Do wystającego z boku grubego, rdzawego gwoździa przywiązany jest sznurek jutowy, na którym wisi pofałdowany, geometryczny blok idealnie białej, surowej słoniny.", "11,12,1,2"),
 ("Tratwa dla żab (Pływająca wysepka): Płaski, ucięty plaster grubego pnia z korą, swobodnie unoszący się na spokojnej, ciemnej tafli przydomowego oczka wodnego. Na drewnie ukorzeniła się drobna kępka zielonej trawy.", "4,5,6,7,8,9"),
 # --- Skrzydlaci Sprzymierzency (Ptaki i Owady) ---
 ("Pszczoła Murarka (Makro): Ekstremalne zbliżenie owada. Ciało wyraźnie rude, pokryte gęstym, puszystym futerkiem na tułowiu i odwłoku. Skrzydła są w połowie rozłożone, a pszczoła przednimi łapkami wgniata mokrą, szarą glinę.", "3,4,5"),
 ("Sikora Bogatka: Makrofotografia ptaka na gałązce wiśni. Brzuch jest jaskrawożółty z bardzo ostrą, pionową, czarną pręgą biegnącą przez środek. Głowa czarna z wyraźnymi, uderzająco białymi policzkami.", None),
 ("Motyl Rusałka Pawik: Rozłożone, płaskie skrzydła na tle fioletowego kwiatu. Cechą kluczową są cztery ogromne, fotorealistyczne pawie oka – niebiesko-czarno-żółte, geometryczne okręgi na rogach rdzawo-czerwonych skrzydeł.", "4,5,6,7,8,9"),
 ("Biedronka Siedmiokropka: Owad o kształcie wypukłej, błyszczącej, jaskrawoczerwonej kuli z maleńką, czarną główką. Na pancerzyku musi znajdować się dokładnie siedem czarnych, równych kropek.", "4,5,6,7,8,9"),
 ("Złotook (Drapieżnik mszyc): Smukły, jasnozielony, niemal neonowy owad na liściu. Kluczowy detal: potężne, kuliste, dosłownie złote, lśniące oczy i niezwykle delikatne, duże, całkowicie przezroczyste skrzydła o koronkowej, geometrycznej siateczce użyłkowania.", "5,6,7,8,9"),
 ("Kopciuszek (Ptak miejski): Niewielki, smukły ptaszek w odcieniach głębokiego, ciemnego, popielatego grafitu, niemal czarny na pyszczku. W ostrym wizualnym kontraście drży jego podniesiony, jaskrawo-rdzawo-pomarańczowy ogon.", "4,5,6,7,8,9"),
 ("Trzmiel Ziemny w kwiecie: Ogromny, pękaty, puszysty owad nurkujący głową w dół do kielicha kwiatu cukinii. Wyraźne pasy grubego futra na ciele: czarne, jaskrawożółte oraz śnieżnobiała końcówka samego tyłu.", "4,5,6,7,8,9"),
 ("Biegaczowate (Chrząszcz): Widok z poziomu mchu. Duży, drapieżny, twardy chrząszcz z długimi nogami i potężnymi żuwaczkami. Jego gładki, czarny, zbrojny pancerz mieni się metalicznie w słońcu na głęboki fioletowo-niebieski kolor.", "4,5,6,7,8,9"),
 ("Ważka (Husarz Władca): Owad zawieszony w locie nad wodą. Korpus w kształcie długiej, sztywnej, błękitno-zielonej igły. Cztery sztywne, szerokie, całkowicie przezroczyste skrzydła o gęstej siatce czarnych żyłek rozpostarte poziomo.", "6,7,8"),
 ("Fruczak Gołąbek (Koliber polski): Ćma w locie zawisająca przed długim kielichem petunii. Skrzydła całkowicie rozmyte w szary ruch. Szary, pękaty, włochaty tułów i ekstremalnie długa, prosta trąbka ssąca zanurzona w kwiatku.", "6,7,8,9"),
 # --- Czworonozni Goscie i Mieszkancy ---
 ("Jeż Europejski w jesieni: Niskie makro w liściach. Zwierzę nie jest w pełni zwinięte w kulkę. Igły są szaro-brązowe z wyraźnie jasnymi końcówkami. Spod igieł wystaje czarny, wilgotny, skórzasty, ruchliwy nosek i czarne, okrągłe oczko.", "9,10,11"),
 ("Wiewiórka Pospolita z orzechem: Smukłe zwierzę o sierści w kolorze płonącej, rudej czerwieni i z białym, czystym puszkiem na brzuchu. Siedzi w kucki, trzymając w drobnych łapkach brązowy orzech włoski. Na uszach długie, sterczące pionowo pędzelki z włosów.", "9,10,11"),
 ("Ropucha Szara (Ziemnowodny sojusznik): Zwierzę o krępej, asymetrycznej budowie. Skóra jest matowa, sucha w wyglądzie, brązowo-szara, i gęsto pokryta nieregularnymi brodawkami. Oczy mają potężną, poziomą, złotą źrenicę.", "3,4,5,6,7,8,9"),
 ("Jaszczurka Zwinka (Samiec): Długa, smukła jaszczurka wygrzewająca się płasko na jasnym, matowym betonie. Grzbiet ma wzór brązowej szachownicy, ale jej boki ubarwione są na absolutnie jaskrawy, szmaragdowo-neonowy odcień zieleni.", "4,5,6,7,8"),
 ("Kret wynurzający się z kopca: Kontrast na trawniku. Czarna, aksamitna sierść, stercząca z samego środka kopca idealnie sypkiej, czarnej ziemi. Na pierwszym planie ogromne, zrogowaciałe, łopatowate, różowe przednie łapy zakończone potężnymi pazurami.", "3,4,5,9,10,11"),
 ("Ryjówka aksamitna (Makro w mchu): Bardzo mały ssak, przypominający mysz, jednak o ciele kulistym i aksamitnym brązowym futrze. Jej pyszczek jest nieproporcjonalnie wydłużony w formę ruchliwego, spiczastego, stożkowatego ryjka z wibrysami.", "4,5,6,7,8,9"),
 ("Kot Działkowy (Dachowiec): Smukły, pręgowany, szaro-czarny kot o chropowatej sierści, leżący w leniwej, asymetrycznej pozie bezpośrednio na świeżo spulchnionej, brązowej ziemi między siewkami marchwi, łapiący ostre promienie słońca.", "4,5,6"),
 ("Zaskroniec Zwyczajny (Niegroźny wąż): Płynnie wijące się, ciemnoszare, stalowe, pokryte suchymi łuskami ciało w wysokiej trawie. Detal rozstrzygający o gatunku: tuż za małą, spłaszczoną głową znajdują się dwie bardzo wyraźne, jaskrawożółte plamy w kształcie półksiężyców.", "4,5,6,7,8,9"),
 ("Nietoperz Gacek (Odpoczynek): Ujęcie we wnętrzu ciemnej krokwi na strychu altany. Zwierzę wisi precyzyjnie pionowo w dół, zawieszone na tylnych pazurkach. Ma szare, gładkie futerko i ogromne, nienaturalnie wielkie, półprzezroczyste, pofałdowane uszy.", "4,5,6,7,8,9"),
 ("Żaba Trawna (Skok w kałuży): Faza odbicia. Zwierzę o gładkiej, śliskiej, brązowo-oliwkowej skórze z ciemną, wyraźną maską za dużym, wypukłym okiem. Długie tylne nogi są w pełni wyprostowane i naprężone w powietrzu nad mokrym piaskiem.", "3,4,5,6,7,8,9"),
 # --- Mikroretencja i Cykl Wodny ---
 ("Beczka na deszczówkę (Przelew): Potężna, zardzewiała, stara stalowa beczka. Podczas ulewy woda całkowicie wypełnia pojemność. Z krawędzi beczki ciężko, szeroką kurtyną przelewa się obfity, gładki strumień lustrzanej wody, rzeźbiąc kanał w trawie.", "4,5,6,7,8,9"),
 ("Zanurzony Ogród (Oczko z nenufarami): Spokojna, ciemna, prawie czarna woda jak szkło. Na niej leżą płasko, okrągłe, gładkie liście lilii wodnej z wyciętym w literę V klinem z boku. Pomiędzy nimi wystaje jeden pionowy, różowy, gwiaździsty kwiatostan.", "6,7,8"),
 ("Błotna strefa brzegowa (Poidełko naturalne): Geologiczny przekrój przejścia wody w ląd. Wąski pasek rzadkiego, szarego błota, w którym niezwykle precyzyjnie odciśnięte są idealne trójpalczaste, małe ślady ptasich łapek, wypełnione krystaliczną wodą.", None),
 ("Niecka Deszczowa (Ogród bioretencyjny): Delikatne, owalne obniżenie terenu w trawniku obłożone polnymi kamieniami. Wypełnione czystą, stojącą wodą po deszczu, z której prosto do nieba wystają ostre, mieczowate, zielone liście kosaćców wodnych.", None),
 ("Pływająca rzęsa wodna: Widok makro z góry na powierzchnię małego stawu. Woda jest w 100% niewidoczna, szczelnie pokryta absolutnie jaskrawym, jasnozielonym dywanem stworzonym z setek tysięcy mikroskopijnych, owalnych, płaskich listków.", "5,6,7,8,9"),
 ("Przepuszczalna ścieżka z grysu: Chodnik ogrodowy. Zamiast płaskiego betonu, ścieżkę tworzy gruba, chrupiąca warstwa nieregularnego, jasnoszarego, ostrego grysu. Między kamyczkami widać głębokie cienie i przestrzenie ułatwiające natychmiastowe wsiąkanie wody.", None),
 ("Filtracja biologiczna (Korzenie w wodzie): Akwarystyczne makro podwodne. Z grubej kępy wodnych roślin zwisa gęsta, biała plątanina zdrowych, nitkowatych korzeni, w które wplątane są mikroskopijne, filtrujące pęcherzyki tlenu.", "4,5,6,7,8,9"),
 ("Kijanki w nagrzanej kałuży: Perspektywa pod powierzchnią ciepłej wody tuż przy brzegu. Rojowisko setek maleńkich, galaretowatych, całkowicie czarnych ciałek w kształcie owalnych główek z długimi, wiotkimi ogonkami, zbijające się w chaotyczne kłębowisko.", "4,5,6"),
 ("Glony nitkowate (Zachwiana równowaga): Płytka tafla wody w ostrym, bezlitosnym świetle słonecznym. Podwodne liście roślin są szczelnie owinięte i uduszone agresywną, bardzo gęstą, zieloną formacją glonów przypominającą namokniętą, śliską, zieloną watę.", "6,7,8"),
 ("Krople rosy na pajęczynie: O świcie, pomiędzy sztywnymi źdźbłami trawy rozciągnięta jest geometryczna, okrągła sieć pająka krzyżaka. Absolutnie każda nić jest gęsto i perliście oblepiona mikroskopijnymi, kulistymi kroplami wody, które działają jak pryzmaty dla wschodzącego słońca.", "8,9,10"),
 # --- Rosliny Wspierajace Ekosystem ---
 ("Facelia błękitna (Łan poplonu): Gęste, splątane, owłosione, sztywne pędy. Kwiatostany układają się w puszyste, spiralne skrętki. Same kwiaty są dzwonkowate, o liliowo-błękitnym, chłodnym kolorze, a ze środka wystają bardzo długie, wyraźne nitki pręcików.", "6,7,8,9"),
 ("Chwasty jako schronienie (Pokrzywy): Gąszcz wysokich pokrzyw o asymetrycznych, mocno ząbkowanych na brzegach liściach. Z bliska na ciemnozielonej łodydze widać sterczące, przezroczyste, krzemionkowe, ostre i kruche włoski parzące.", "4,5,6,7,8,9"),
 ("Kwietna Łąka (Nieskoszona dzikość): Brak trawnika. Płynny chaos roślin w różnym stadium kwitnienia na wysokości pół metra. Królują jaskrawo, krwisto czerwone pogniecione kielichy maków polnych, intensywnie niebieskie chabry oraz płaskie, białe baldachy krwawnika.", "6,7,8"),
 ("Koniczyna Biała (Trawnikowy ratunek): Widok z góry. Pomiędzy zielonymi źdźbłami trawy gęsto ścielą się charakterystyczne listki złożone z trzech mniejszych. Wyrastają okrągłe, puszyste główki kwiatostanowe z setek rurkowatych, śnieżnobiałych kwiatuszków.", "5,6,7,8,9"),
 ("Owoce dzikiej róży (Zimowy pokarm): Nagi, brązowy, mocno zdrewniały pęd osadzony na tle białego śniegu, wyposażony w ostre, wygięte do tyłu haczykowate kolce. Zwisa z niego ciężkie grono twardych, wydłużonych, pomarszczonych od mrozu, jaskrawoczerwonych owoców.", "11,12,1,2"),
 ("Budleja Dawida (Krzew Motyli): Grube, łukowato opadające w dół pędy krzewu zakończone olbrzymimi, wydłużonymi wiechami kwiatostanowymi barwy fioletowo-liliowej, po brzegi obsypane obsiadującymi je kolorowymi motylami we wszystkich fazach lotu.", "6,7,8,9"),
 ("Dziki Żywopłot Mieszany: Ściana ochronna, niesymetrycznie przycinana. Złożona z mocno przeplatających się warstw: ząbkowanych i gładkich liści grabu połączonych z potężnymi, długimi na 3 cm, niebezpiecznie sztywnymi i lśniącymi, brązowymi cierniami głogu.", None),
 ("Słonecznik pastewny ptasi: Zaschła i zwieszona w dół okrągła tarcza potężnego słonecznika, na wpół ogołocona przez sikorki. Prawa strona ukazuje jeszcze ułożone w spirale Fibonacciego pękate, czarne pestki, lewa – idealnie gładką, pustą geometryczną siatkę.", "8,9,10,11"),
 ("Bluszcz pospolity owijający drzewo: Masywny pień chropowatego, starego dębu owinięty zimozielonym gatunkiem. Płaskie, trójklapowe, bardzo skórzaste liście o błyszczącej, woskowej powierzchni i wyraźnych, grubych, jasnozielonych nerwach ściśle przylegają do szarej kory.", None),
 ("Nawłoć kanadyjska (Inwazyjna piękność): Gruby łan sztywnych, pionowych, prosto ułożonych łodyg. Na samej ich górze tworzą się gęste, ciężkie, puszyste, asymetryczne, wiechowate kwiatostany w rażącym, matowo-żółtym kolorze odcinające się bardzo ostro na tle błękitnego, czystego nieba.", "8,9,10"),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT,)).fetchone()
conn.close()
if row:
    print("UWAGA: kategoria '%s' juz istnieje (id=%s) - przerywam." % (CAT, row['id']))
else:
    cid = add_category(CAT)
    for tekst, mies in EKOLOGIA:
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
