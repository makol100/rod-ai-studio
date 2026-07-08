# -*- coding: utf-8 -*-
from src.db.database import add_category, add_topic, get_connection

CAT = "Architektura Ogrodowa, Remonty i Majsterkowanie"

BUD_SEZON = "4,5,6,7,8,9,10"

ARCHITEKTURA = [
 # --- Konstrukcje Drewniane i Architektura Zewnetrzna ---
 ("Budowa pergoli tarasowej: Potężne, pionowe słupy z surowego drewna sosnowego z wyraźnym, głębokim rysunkiem słojów. Na samej górze idealnie spasowane, prostopadłe łączenie belek na tzw. jaskółczy ogon, bez widocznych śrub.", BUD_SEZON),
 ("Podniesione grządki (Warzywniki): Solidne skrzynie zbite z grubych, impregnowanych na oliwkowo desek ryflowanych. Wnętrze wyłożone czarną, chropowatą folią kubełkową, po brzegi wypełnione smoliście czarną, gruzełkowatą ziemią kompostową.", "3,4,5,9,10"),
 ("Domek narzędziowy z płyt OSB: Surowa faza budowy. Szkielet z jasnych krawędziaków drewnianych, do których precyzyjnie przykręcone są płyty OSB o bardzo agresywnej, chaotycznej teksturze sprasowanych wiórów z połyskującą żywicą.", BUD_SEZON),
 ("Kratka na pnącza (Treliaż): Geometria w drewnie. Gęsta, ukośna kratownica (romby) ułożona z bardzo cienkich, gładkich, jasnych listewek, przymocowana do białego, tynkowanego muru o silnej strukturze baranka.", "3,4,5,9,10"),
 ("Taras z deski kompozytowej: Zbliżenie na posadzkę. Szare, idealnie równe deski z głębokimi, wzdłużnymi rowkami. Pomiędzy deskami widać czarne, niewidoczne z góry klipsy montażowe ze stali nierdzewnej (brak wkrętów na wierzchu).", BUD_SEZON),
 ("Zadaszenie poliwęglanowe: Patrząc prosto w niebo: transparentne, komorowe płyty z poliwęglanu (widoczne długie, równoległe kanaliki wewnątrz plastiku), podparte na ciemnobrązowych, kanciastych krokwiach. Na plastiku leżą brązowe, opadłe liście dębu.", "9,10,11"),
 ("Skrzynia na poduszki z siłownikiem: Ciężka, podłużna ławka otworzona pod kątem 45 stopni. Kluczowy detal: lśniący, stalowy siłownik gazowy (teleskop) precyzyjnie podtrzymujący ciężką, drewnianą pokrywę.", BUD_SEZON),
 ("Meble z palet (Szlifowanie): Surowa paleta euro ułożona na kozłach. Szlifierka mimośrodowa z czerwoną tarczą ścierną zdziera szarą, starą warstwę drewna, odsłaniając jasny, gładki i czysty rdzeń. W powietrzu unosi się wyraźny pył drzewny.", BUD_SEZON),
 ("Krawędzie płotka myśliwskiego: Klasyczny płot ze sztachet. Zbliżenie na górną krawędź – każda pionowa deska jest idealnie, symetrycznie ścięta w trójkąt, pomalowana gęstą, niebieską farbą olejną, która miejscami lekko popękała ze starości.", "4,5,6,7,8,9"),
 ("Wkręty ciesielskie (Makro): Ekstremalne zbliżenie na lśniący, złoto-żółty wkręt ciesielski z głębokim gniazdem typu Torx. Ostra końcówka z nacięciem frezującym właśnie wgryza się w surowe, jasne drewno, wokół której sypią się malutkie wiórki.", None),
 # --- Remont Wnetrza Altany ---
 ("Łazienka w altanie (Biel i czerń): Wielkoformatowe, śnieżnobiałe płytki ułożone z mikrofugą, tworzące nieskazitelną płaszczyznę ściany. Na ich tle zamontowana jest całkowicie matowo-czarna, ostro ścięta bateria umywalkowa z geometrycznym uchwytem oraz czarny syfon butelkowy pod wiszącą szafką.", BUD_SEZON),
 ("Ocieplenie wełną mineralną: Ściana szkieletowa otworzona od wewnątrz. Między drewnianymi słupkami ciasno upchnięta jest gruba, żółto-brązowa, włóknista i puszysta wełna skalna. Na wierzch naciągana jest połyskująca, przezroczysta folia paroizolacyjna z taśmą.", BUD_SEZON),
 ("Instalacja rozdzielnicy (Z TN-C na TN-S): Zbliżenie na wnętrze nowej, białej skrzynki natynkowej. Czysty, precyzyjny rozdział grubego przewodu PEN na dwie szyny: żółto-zieloną (PE) i niebieską (N). Kable miedziane wygięte w idealnie proste, ostre kąty bez splątania.", BUD_SEZON),
 ("Boazeria świerkowa z pistoletem: Dłonie w rękawicach roboczych trzymające ciężki, pneumatyczny zszywacz (gwoździarkę). Metalowy nos narzędzia dociśnięty jest pod kątem do wąskiego pióra jasnej deski boazeryjnej, gotowy do wbicia niewidocznego sztyftu.", BUD_SEZON),
 ("Wylewka samopoziomująca: Szara, gęsta, płynna masa wylewająca się powoli z czarnego wiadra na surowy beton podłogi. Obok leży długi, stalowy wałek z bardzo gęstymi, długimi, różowymi kolcami z plastiku do odpowietrzania wylewki.", BUD_SEZON),
 ("Obróbka okna pianką PUR: Biała, nowa rama okna PCV osadzona w ceglanym murze. Ze szczeliny między oknem a murem agresywnie pęcznieje i wylewa się gruba, porowata, jasnożółta pianka poliuretanowa, tworząc bąblowate kształty.", BUD_SEZON),
 ("Montaż drzwi przesuwnych (Loft): Grube, ciężkie skrzydło drzwiowe z surowych dech, zawieszone na potężnej, czarnej, matowej szynie stalowej biegnącej tuż pod sufitem. Na szynie opierają się dwa ogromne, stalowe kółka łożyskowe.", BUD_SEZON),
 ("Przejście kominowe kozy: Lśniąca jak lustro, srebrna rura spalinowa z blachy kwasoodpornej (dwuścienna) przechodzi pionowo w górę przez otwór wycięty w drewnianym suficie. Wokół rury widoczna gruba, biała rozeta maskująca na tle drewna.", BUD_SEZON),
 ("Aneks kuchenny ze sklejki: Minimalistyczne szafki podblatowe. Fronty wykonane z surowej, jasnej sklejki brzozowej, gdzie na obrzeżach perfekcyjnie widać ułożone poziomo warstwy (paski) cienkiego drewna.", BUD_SEZON),
 ("Malowanie starych desek: Welurowy, mały wałek malarski, z którego spływa gęsta, matowa, szałwiowa zieleń (farba kredowa), przykrywająca do połowy starą, pożółkłą i lakierowaną boazerię sosnową z ciemnymi sękami.", "4,5,6,7,8,9"),
 # --- Prace Murarskie, Beton i Sciezki ---
 ("Układanie kostki brukowej: Jasnożółty, ubity piasek o równej fakturze. Na nim leży dłoń trzymająca ciężki, gumowy młotek z czarnym obuchem, dobijający szarą, betonową kostkę brukową z fazowanymi krawędziami do reszty ułożonego wzoru.", BUD_SEZON),
 ("Murek oporowy z kamienia: Rustykalna konstrukcja. Szaro-rude, nieforemne kamienie polne różnej wielkości, połączone bardzo grubą, szorstką zaprawą cementową w kolorze jasnoszarym. Spoina jest głęboko wklęsła, uwydatniając trójwymiarowość głazów.", BUD_SEZON),
 ("Grill z cegły klinkierowej: Perfekcyjny mur. Ciemnoczerwona, gładka cegła klinkierowa wymurowana na ostro. Pomiędzy cegłami znajduje się idealnie równa, wygładzona, czarna fuga. W środku wbudowany gruby, żeliwny ruszt posmarowany olejem.", BUD_SEZON),
 ("Betonowanie słupków ogrodzeniowych: Przekrój wykopu w ziemi. Na dnie głębokiego, okrągłego otworu zalegają kamienie, a na nich osadzony jest pionowy, zielony słupek stalowy, wokół którego wlewa się mokry, szary beton pełen kruszywa i pęcherzyków powietrza.", BUD_SEZON),
 ("Obrzeże trawnikowe Eko-Bord: Czarna, giętka listwa plastikowa przybita do twardej ziemi potężnymi, długimi plastikowymi gwoździami. Z lewej strony listwy równo docięta, gęsta, zielona darń, a z prawej gruba warstwa bordowej kory sosnowej.", BUD_SEZON),
 ("Płyty deptakowe w trawie: Zbliżenie od góry. Duża, idealnie okrągła płyta z jasnego betonu o fakturze szczotkowanej, ułożona idealnie w jednej płaszczyźnie z idealnie skoszonym, angielskim trawnikiem.", BUD_SEZON),
 ("Schody wyłożone gresem: Krawędź betonowych schodów zewnętrznych. Do boku przyklejona jest antypoślizgowa płytka gresowa o fakturze szarego kamienia. Na jej rogu wmurowana jest lśniąca, aluminiowa listwa kątowa chroniąca przed ukruszeniem.", BUD_SEZON),
 ("Tynkowanie elewacji (Baranek): Czysta, błyszcząca stalowa paca murarska dociska do szarego ocieplenia białą, gęstą masę tynku silikonowego. Obok widoczna już zatarta struktura – równomierne, drobniutkie rowki przypominające fakturę gąbki.", "5,6,7,8,9"),
 ("Fundament punktowy pod taras: Z ubitej, gliniastej ziemi wystaje okrągła, szara tuba kartonowa (szalunek), szczelnie wypełniona twardym betonem. Z centrum betonu wystaje gwintowany, stalowy, ocynkowany pręt w kształcie litery U podtrzymujący legar.", BUD_SEZON),
 ("Opaska żwirowa przy fundamencie: Mur altany pomalowany lepkim, czarnym lepikiem asfaltowym (izolacja). Poniżej linii tynku rozciąga się równa warstwa perfekcyjnie gładkich, okrągłych, śnieżnobiałych otoczaków zapobiegających chlapaniu.", BUD_SEZON),
 # --- Warsztat, Majsterkowanie i Nowe Technologie ---
 ("Druk 3D do ogrodu: Zbliżenie na kuwetę drukarki żywicznej (LCD/SLA). Z tafli matowej, fioletowej żywicy wynurza się precyzyjnie drukowany, gładki, szary uchwyt z otworami na śruby, z którego powoli ściekają gęste, błyszczące krople nieutwardzonego płynu.", None),
 ("Ścianka narzędziowa (French Cleat): Gruba, jasna płyta ze sklejki przykręcona do ściany, posiadająca poziome listwy ścięte pod kątem 45 stopni. Na nich wiszą precyzyjnie wykonane w drewnie, niestandardowe uchwyty trzymające błyszczące dłuta stalowe.", None),
 ("Mieszanie zaprawy w wiadrze: Duże, czarne wiadro budowlane. Wewnątrz obraca się z dużą prędkością stalowe mieszadło (świder) wiertarki, tworząc głęboki wir w gęstej, ciemnoszarej, gładkiej zaprawie klejowej. Wokół rozpryskują się drobne krople.", BUD_SEZON),
 ("Cięcie płytek maszynką ręczną: Podłużna, czerwona maszynka do glazury z dwoma chromowanymi prowadnicami. Diamentowe, małe, lśniące kółeczko tnące właśnie nacina twardą, szkliwioną powierzchnię białej płytki, tworząc idealnie prostą, mikroskopijną rysę z pyłem.", BUD_SEZON),
 ("Renowacja zardzewiałej łopaty: Mocno zardzewiały, brązowy i chropowaty szpadel zaciśnięty w imadle. Szybko wirująca szczotka druciana na szlifierce kątowej zdziera rdzę, odsłaniając pod spodem lśniącą, czystą, szczotkowaną stal pod gradem pomarańczowych iskier.", None),
 ("Ostrzenie sekatora na mokro: Dwie rozchylone, wygięte w łuk szczęki sekatora kowadełkowego. Kciuk przesuwa po krawędzi tnącej mokrą, szarą osełkę, pozostawiając za sobą ekstremalnie lśniącą, geometrycznie ściętą i naostrzoną krawędź ze stali węglowej.", "2,3,4"),
 ("Lutowanie elektroniki: Dłoń trzymająca precyzyjną lutownicę kolbową. Rozgrzany, cynowany grot dotyka zielonej płytki PCB. Pod wypływem ciepła cienki drut spoiwa roztapia się w błyszczącą, idealnie okrągłą srebrną kroplę, uwalniając cienką strużkę niebieskawego dymu.", None),
 ("Cięcie drewna ukośnicą: Gruba belka z litego drewna na obrotowym blacie żółtej piły ukosowej. Ogromna, stalowa tarcza z widiowymi zębami, w pełnym pędzie i rozmyciu ruchu, wchodzi prostopadle w drewno. Za tarczą wyrzucany jest gęsty strumień złotych trocin.", None),
 ("Impregnacja desek pędzlem: Szeroki, płaski pędzel z włosia syntetycznego przesuwany po jasnej desce. Za pędzlem drewno natychmiast zmienia kolor na głęboki, bursztynowy brąz z mokrym połyskiem, a rysunek słojów staje się skrajnie wyostrzony i kontrastowy.", "4,5,6,7,8,9"),
 ("Klucz dynamometryczny i śruby: Masywny, przedłużony, chromowany klucz grzechotkowy. Skala w okienku klucza ustawiona wyraźnie na 120 Nm. Nasadka klucza mocno obejmuje sześciokątną, ocynkowaną główkę ogromnej śruby wchodzącej w stalowy ceownik.", None),
 # --- Woda, Retencja i Zewnetrzna Hydraulika ---
 ("Instalacja zbiornika Mauzer (1000L): Potężny, sześcienny pojemnik IBC z przezroczysto-matowego, białego polietylenu, zamknięty w zewnętrznym klatkowym stelażu z rur ocynkowanych. Stoi na solidnej podstawie wymurowanej z szarych bloczków betonowych.", BUD_SEZON),
 ("Zlewozmywak gospodarczy (Zewnętrzny): Otwarty, głęboki zlew wykonany w całości z grubej, matowo-szczotkowanej stali nierdzewnej, osadzony w roboczym blacie ze starych, spękanych belek. W zlewie leży ziemia i ubłocona marchewka.", BUD_SEZON),
 ("Budowa studni chłonnej (Drenaż): Przekrój wykopu. Czarna, gruba, karbowana rura (peszel drenażowy) z podłużnymi nacięciami, owinięta ciasno białowłóknistą geowłókniną, ułożona w zasypce z ostrego, płukanego żwiru frakcji 16-32mm.", BUD_SEZON),
 ("Mufy i złączki PE do wody: Dwie grube, twarde, czarne rury polietylenowe z cienkim niebieskim paskiem. Pośrodku połączone są masywną, skręcaną złączką zaciskową z intensywnie niebieskiego plastiku z gwintem, na której widać krople potu po dokręcaniu.", BUD_SEZON),
 ("Montaż rynny PVC: Zbliżenie na połączenie rynnowe na krawędzi dachu. Ciemnobrązowy, geometryczny narożnik rynnowy, w którym wewnątrz widać wyraźnie dociśniętą, szeroką, gumową uszczelkę z EPDM opierającą się na plastiku.", BUD_SEZON),
 ("Filtr siatkowy do deszczówki: Półprzezroczysty, cylindryczny korpus filtra wpięty pod rynną. W środku widoczna jest gęsta, walcowata siatka ze stali nierdzewnej, na której osadziły się mokre paprochy i igły sosnowe, zatrzymane przed zbiornikiem.", BUD_SEZON),
 ("Pompa ręczna (Abisynka): Klasyczna, starodawna, odlewana z surowego, żeliwnego stopu pompa z długim, zdobionym ramieniem. Z rdzewiejącej, otwartej wylewki wylewa się krystalicznie czysta, obfita woda wprost do ocynkowanego, srebrnego wiadra.", BUD_SEZON),
 ("Zawór czerpalny na zimę (Mrozoodporny): Z elewacji wystaje długa, mosiężna rurka z kranikiem o surowej fakturze, skierowanym w dół. Głowica zaworu i pokrętło są nienaturalnie wydłużone na zewnątrz i lekko pochylone, aby woda spłynęła z korpusu.", "9,10,11"),
 ("Korytko odwodnienia liniowego: Ułożone na równi z betonową kostką brukową płytkie koryto. Górę przykrywa lśniący, stalowy ruszt kratowy o prostokątnych oczkach. Poniżej rusztu gładki, szary kanał z polimerobetonu z leżącym na dnie, pojedynczym żółtym liściem.", BUD_SEZON),
 ("Opaska zaciskowa (Cyband): Zbliżenie na zielony wąż ssawny nasunięty na stalowy króciec pompy. Na wężu zaciśnięta jest szeroka, stalowa obejma ślimakowa, a ostra śruba dociska równomierne wcięcia, wbijając opaskę lekko w elastyczną, wzmacnianą gumę.", None),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT,)).fetchone()
conn.close()
if row:
    print("UWAGA: kategoria '%s' juz istnieje (id=%s) - przerywam." % (CAT, row['id']))
else:
    cid = add_category(CAT)
    for tekst, mies in ARCHITEKTURA:
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
