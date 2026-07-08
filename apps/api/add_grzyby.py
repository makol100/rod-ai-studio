# -*- coding: utf-8 -*-
from src.db.database import add_category, add_topic, get_connection

CAT = "Grzyby w śląskich lasach"

GRZYBY = [
 ('Borowik szlachetny (Prawdziwek): Masywny grzyb. Trzon gruby, pękaty (maczugowaty), jasnobeżowy z wyraźną, drobną, białą siateczką w górnej części. Kapelusz w kształcie półkuli, skórzasty, w kolorze ciepłego brązu. Spód kapelusza gąbczasty (zbudowany z rurek), szaro-biały do oliwkowego. Brak blaszek.', '6,7,8,9,10'),
 ('Podgrzybek brunatny: Trzon cylindryczny, często wygięty, żółtobrązowy z podłużnymi, ciemniejszymi pręgami (bez siateczki). Kapelusz ciemnobrązowy, matowy, przypominający zamsz. Rurki pod spodem bladożółte, sprawiające wrażenie zgniecionych i błękitniejących od dotyku.', '6,7,8,9,10,11'),
 ('Maślak zwyczajny: Kapelusz czekoladowo-brązowy, którego powierzchnia jest bardzo śliska, błyszcząca i pokryta gęstym, przezroczystym śluzem. Trzon krótki, żółtawy, z wyraźnym, odstającym, błoniastym białym pierścieniem tuż pod rurkami.', '8,9,10,11'),
 ('Koźlarz babka: Wysmukły grzyb. Trzon długi, cienki, zwężający się ku górze, gęsto pokryty drobnymi, czarnymi lub szarymi łuskami (przypominający fakturę kory brzozy). Kapelusz miękki, wypukły, szaro-brązowy.', '6,7,8,9,10'),
 ('Koźlarz czerwony: Trzon identyczny jak u "babki" (biały z czarnymi kosmkami), ale kapelusz ma jaskrawy, ceglastoczerwony do pomarańczowego kolor, zamszową teksturę, a skórka kapelusza często lekko wystaje (zwisa) poza krawędź rurek.', '6,7,8,9,10'),
 ('Pieprznik jadalny (Kurka): Grzyb w całości intensywnie żółty, bez płynnego podziału na kapelusz i trzon – zwęża się w dół w kształt lejka. Brzegi mocno pofalowane. Pod spodem kapelusza znajdują się grube, rozwidlające się listewki (nie cienkie blaszki), które zbiegają głęboko na nóżkę.', '6,7,8,9,10'),
 ('Czubajka kania: Ogromny, płaski jak talerz kapelusz na bardzo długiej, smukłej nóżce. Kapelusz jasny, gęsto pokryty grubymi, ciemnobrązowymi, dachówkowatymi łuskami, z wyraźnym, ciemnym garbem na samym środku. Na trzonie luźny, gruby, podwójny pierścień.', '7,8,9,10'),
 ('Gąska zielonka: Krępy grzyb wyrastający często głęboko z piasku. Zarówno kapelusz, jak i gęste blaszki pod spodem mają siarkowo-żółto-zielony kolor. Kapelusz płaski z drobnymi, przylegającymi, ciemniejszymi łuseczkami w centrum.', '9,10,11'),
 ('Rydz (Mleczaj rydz): Lejkowaty kapelusz w kolorze pomarańczowo-łososiowym z charakterystycznymi, ciemniejszymi, koncentrycznymi kręgami (strefami). Blaszki gęste, pomarańczowe. W miejscach pęknięć widoczne zielonawe plamy zieleniejącego na powietrzu "mleczka".', '8,9,10'),
 ('Opieńka miodowa: Rośnie w gęstych kępach (dziesiątki sztuk) na pniach drzew. Kapelusze małe, miodowo-żółte, na środku pokryte drobnymi, brązowymi łuseczkami. Cienkie, długie trzony z delikatnym, puszystym pierścieniem u góry.', '9,10,11'),
 ('Podgrzybek złotawy (Zajączek): Matowy, zamszowy, oliwkowo-brązowy kapelusz, którego skórka na brzegach często pęka, odsłaniając wyraźnie różowy miąższ pod spodem. Trzon cienki, żółto-czerwony. Rurki pod spodem duże, kanciaste, jaskrawożółte.', '6,7,8,9,10'),
 ('Maślak sitarz: Kapelusz żółto-pomarańczowo-cielisty, gładki, bez śluzu. Cechą unikalną są rurki pod spodem: bardzo duże, kanciaste, głębokie, wizualnie przypominające plaster miodu lub gęste sito.', '7,8,9,10,11'),
 ('Maślak żółty (modrzewiowy): Cały grzyb (kapelusz, trzon, rurki) ma jaskrawy, cytrynowo-żółty lub złoty kolor. Kapelusz silnie śliski, wypukły. Na trzonie delikatny, żółtawy pierścień.', '6,7,8,9,10'),
 ('Piaskowiec modrzak: Kapelusz w kształcie spłaszczonej bułki, grubo-zamszowy, blado-piaskowy. Uszkodzone miejsca na żółtawym trzonie i gąbce intensywnie barwią się na atramentowy, głęboki chabrowy błękit.', '7,8,9,10'),
 ('Gołąbek zielonawy: Kapelusz płaski z wklęśnięciem na środku. Skórka w kolorze seledynowo-grynszpanowym, gęsto spękana na drobne, mozaikowe poletka (jak wyschnięta ziemia), spod których widać biały miąższ. Blaszki i gruby trzon czysto białe.', '6,7,8,9,10'),
 ('Płachetka kołpakowata (Turkuć): Kapelusz młodych owocników przypomina zamknięty, pomarszczony dzwonek lub wysoki kołpak w kolorze gliniasto-żółtym, często z delikatnym, fioletowo-srebrzystym szronem (nalotem) na samym szczycie. Blaszki gliniaste.', '8,9,10'),
 ('Lejkowiec dęciak (Kominek): Grzyb wyglądający jak cienka, czarna lub ciemnoszara trąbka zwinięta z papieru, głęboko wydrążona w środku aż do samej ziemi. Brzegi kapelusza mocno pofalowane i wywinięte, powierzchnia zewnętrzna szaro-popielata, zamszowa, bez blaszek.', '8,9,10,11'),
 ('Kolczak obłączasty: Z góry wygląda jak jasna, kremowo-żółta kurka (kapelusz gładki, asymetryczny), ale spód kapelusza nie ma blaszek ani rurek – jest gęsto pokryty tysiącami łamliwych, zwisających pionowo w dół, miękkich "kolców" (sopelków).', '7,8,9,10,11'),
 ('Krasnoborowik ceglastopory (Pociec): Potężny grzyb. Kapelusz ciemnobrązowy, zamszowy. Trzon gruby, baryłkowaty, żółty, ale gęsto pokryty czerwoną, punktową szczeciną (kropkami, nie siatką). Rurki pod spodem jaskrawo ceglasto-czerwone.', '7,8,9'),
 ('Lisówka pomarańczowa (Fałszywa Kurka): Cały grzyb intensywnie, jaskrawo pomarańczowy. Kapelusz lejkowaty, ale pod spodem posiada gęste, bardzo cienkie, ostre blaszki wielokrotnie rozwidlające się dychotomicznie w kształt litery Y (w przeciwieństwie do grubych fałd kurki). Cienki, wiotki trzon.', '7,8,9,10,11'),
 ('Muchomor czerwony: Jaskrawoczerwony, błyszczący kapelusz w kształcie szerokiego parasola, regularnie usiany białymi, wypukłymi kropkami (brodawkami). Trzon śnieżnobiały, smukły, z wiszącym obfitym pierścieniem i bulwiastą podstawą na dole.', '8,9,10,11'),
 ('Sromotnik smrodliwy: Z przypominającego jajo białego "wulkanu" u podstawy wyrasta długi, biały, gąbczasty trzon zakończony naparstkowatą "główką" pokrytą śluzowatą, oliwkowo-zieloną, lśniącą i w kratkę spękaną mazią.', '6,7,8,9,10'),
 ('Okratek australijski (Palce diabła): Rozwija się z szarawego jaja, z którego wyrasta od 4 do 7 gąbczastych ramion, rozchylających się na boki jak gwiazda rozgwiazdy. Ramiona mają jaskrawoczerwony kolor od wewnątrz i są pokryte czarnym śluzem.', '8,9,10'),
 ('Czernidłak kołpakowaty: Wąski, cylindryczny, biały kapelusz przypominający nierozwinięty parasol, gęsto usiany odstającymi, białymi łuskami. Dolna krawędź kapelusza czernieje i dosłownie rozpuszcza się, kapiąc w dół jako gęste, czarne krople atramentu.', '5,6,7,8,9,10,11'),
 ('Muchomor sromotnikowy: Kapelusz gładki, bez białych kropek, w kolorze oliwkowo-zielonym, z wrośniętymi promieniście, ciemniejszymi włókienkami. Trzon z wyraźnym, kołnierzykowatym pierścieniem wyrasta z szerokiej, luźnej, skórzastej "pochwy" ukrytej w mchu.', '7,8,9,10'),
 ('Siedzuń sosnowy (Szmaciak): Grzyb bez trzonu i kapelusza. Wygląda jak okrągła, gęsta gąbka morska lub rozgotowany kalafior leżący pod sosną. Składa się z setek pofalowanych, kędzierzawych, kremowo-żółtych, płaskich "listków" zbitych w jedną dużą kulę.', '8,9,10'),
 ('Soplówka jeżowata: Rośnie pionowo na pniach drzew. Biały bochenek w całości złożony z kaskadowo opadających, gęstych, miękkich, śnieżnobiałych igieł (sopli) przypominających gęste futro lub mopa.', '9,10,11'),
 ('Purchawka chropowata: Grzyb w kształcie odwróconej, białej żarówki lub gruszki, całkowicie pozbawiony trzonu i blaszek. Cała zewnętrzna powierzchnia jest gęsto pokryta drobnymi, białymi, stożkowatymi kolcami, które na czubku ciemnieją do brązu.', '7,8,9,10,11'),
 ('Lakownica żółtawa (Reishi): Grzyb nadrzewny w kształcie płaskiej, półkolistej nerki osadzonej asymetrycznie na grubym, krótkim trzonie. Powierzchnia kapelusza wygląda jak grubo polakierowana na wysoki połysk, lśniąca, z płynnymi przejściami kolorów od ciemnej czerwieni do kremowego brzegu.', '5,6,7,8,9,10'),
 ('Czarka szkarłatna: Grzyb w kształcie idealnej, otwartej na górze miseczki. Zewnętrzna strona miseczki jest bladoróżowa i lekko omszona (matowa), natomiast wnętrze ma absolutnie jaskrawy, jednolity, neonowo-szkarłatny kolor pozbawiony jakichkolwiek struktur.', '2,3,4'),
 ('Smardz jadalny: Wiosenny grzyb o beżowym trzonie. Kapelusz w kształcie owalnej główki zbudowanej z głębokich, kanciastych jamek odgrodzonych wypukłymi listewkami (przypomina szary plaster miodu lub zaschniętą gąbkę naciągniętą na patyk).', '4,5'),
 ('Boczniak ostrygowaty: Rośnie zimą w muszlowatych kępach, pionowo na pniach liściastych drzew. Kapelusze asymetryczne, gładkie, w kształcie języków lub uszu, o stalowo-niebieskim do popielatego kolorze. Białe blaszki pod spodem głęboko zbiegają na boczny trzon.', '9,10,11,12,1,2,3'),
 ('Płomiennica zimowa: Rośnie zimą z drewna. Kapelusze małe, płaskie, śliskie, w kolorze bardzo intensywnej, rdzawej pomarańczy z jaśniejszym brzegiem. Cienki, elastyczny trzon, a jego dolna połowa pokryta jest gęstym, aksamitnym, czarnobrązowym meszkiem.', '10,11,12,1,2,3'),
 ('Uszak bzowy (Grzyb mun): Rośnie jesienią/zimą na gałęziach. Kształtem i cienką teksturą przypomina pomarszczone ludzkie ucho. Jest to chrząstkowata, galaretowata miseczka w kolorze półprzezroczystego, czerwonawego brązu, bez żadnych blaszek i rurek.', '10,11,12,1,2,3,4'),
 ('Żółciak siarkowy: Huba wyrastająca kaskadowo na pniach drzew. Kształt ułożonych dachówkowato, falistych, grubych i mięsistych półek. Kolor absolutnie jaskrawy – neonowo cytrynowo-żółty wpadający na brzegach w pomarańcz, przypominający zastygłą pianę poliuretanową.', '5,6,7,8,9'),
 ('Wodnicha późna: Jesienny grzyb spod sosen. Kapelusz wypukły, oliwkowo-brązowy, po deszczu potężnie śliski, pokryty grubą warstwą przezroczystego śluzu. Trzon u góry suchy i biały, a niżej również opasany błyszczącym śluzem. Blaszki żółtawe, rzadkie i grube.', '10,11,12'),
 ('Gąsówka nagus (Fioletowa): Grzyb z późnojesiennej ściółki. Zarówno gładki, matowy kapelusz, jak i gęste blaszki pod spodem oraz gruby, masywny trzon bez pierścienia mają jednolity, intensywny, wręcz sztuczny liliowo-fioletowy kolor.', '9,10,11,12'),
 ('Żagiew łuskowata: Nadrzewny, bardzo duży, płaski i półkolisty grzyb (huba). Powierzchnia w kolorze kremowej ochry jest geometrycznie usiana koncentrycznie ułożonymi, przylegającymi, dużymi brązowymi łuskami, ułożonymi jak pióra na piersi bażanta.', '4,5,6,7'),
 ('Piestrzenica kasztanowata: Grzyb wiosenny. Kapelusz nie ma kształtu parasola, lecz przypomina bezkształtny, niesymetrycznie pofałdowany i pognieciony mózg, w kolorze głębokiego, orzechowo-czerwonawego brązu, nałożony na krótki, nierówny trzon.', '3,4,5'),
 ('Kustrzebka pomarańczowa: Grzyb w kształcie cienkich, beztrzonowych, płaskich lub lekko wklęsłych miseczek, leżących bezpośrednio na mchu. Wewnętrzna (górna) strona miseczki ma kolor intensywnie jaskrawo-pomarańczowy, płaski i gładki.', '8,9,10,11'),
 ('Pieczarka leśna: Kapelusz w kształcie dzwonu lub półkuli, którego powierzchnia przypomina stary pergamin – jasne, kremowe tło gęsto i równomiernie pokryte drobnymi, przylegającymi, brązowo-rudymi łuskami (plamkami). Trzon z wyraźnym, białym kołnierzem, blaszki gęste i ciemnoróżowe.', '7,8,9,10'),
 ('Krowiak aksamitny (Olszówka): Kapelusz o barwie zgniłego, oliwkowego brązu. Krawędzie kapelusza są bardzo wyraźnie, rurkowato i głęboko podwinięte pod spód w stronę blaszek. Blaszki zbiegają na bardzo krótki, centralny trzon.', '6,7,8,9,10'),
 ('Borowik ponury: Grzyb z masywnym trzonem i oliwkowo-brązowym, zamszowym kapeluszem. Rurki pod spodem są intensywnie krwistoczerwone. Na żółtawym trzonie posiada bardzo grubą, wypukłą, bordową siatkę o dużych, wydłużonych oczkach.', '6,7,8,9'),
 ('Mleczaj wełnianka: Grzyb z wklęsłym na środku kapeluszem w kolorze pudrowego różu w wyraźne, koncentryczne paski. Brzegi kapelusza są mocno podwinięte pod spód i okryte gęstą, włochatą "grzywką" długich, wełnistych kosmków.', '7,8,9,10'),
 ('Twardzioszek przydrożny: Malutki, delikatny grzybek na cienkiej, sztywnej, elastycznej nóżce. Kapelusz skórzasty, płaski z tępym garbkiem na środku, w kolorze wyblakłej skóry (jasna ochra). Blaszki pod spodem bardzo szerokie i rzadkie.', '5,6,7,8,9,10,11'),
 ('Lejkówka wonna: Niewielki grzybek o płaskim, z czasem lejkowatym kapeluszu. Kolor całości (kapelusz, trzon, gęste blaszki) to blady, matowy seledyn wpadający w spłowiały, szarawy błękit (przypominający kolor miedzi pokrytej patyną).', '8,9,10'),
 ('Muchomor rdzawobrązowy (Panienka): Kształt otwartego, płaskiego parasola. Wąski, długi trzon całkowicie pozbawiony pierścienia. Kapelusz w kolorze miedzi lub rdzy, bez plamek, z bardzo wyraźnie promieniście prążkowanym na krawędziach brzegiem. Na dole trzon uwięziony jest w workowatej pochwie.', '6,7,8,9,10'),
 ('Gołąbek jadalny (jasnoczerwony): Sztywny, łamliwy grzyb o idealnej geometrii. Trzon gładki, równy, kredowobiały, bez żadnego pierścienia. Kapelusz płasko-wypukły, w kolorze brudnej, matowej, czasem rozmytej czerwieni lub karminu. Blaszki białe.', '6,7,8,9,10'),
 ('Borowik grubotrzonowy (Żółciak): Niezwykle potężny, ciężki grzyb. Kapelusz popielato-szary, suchy. Trzon bardzo pękaty i baryłkowaty, wyraźnie podzielony kolorystycznie – pod rurkami jest jaskrawo cytrynowo-żółty, a u dołu karminowo-czerwony.', '6,7,8,9'),
 ('Goryczak żółciowy (Szatan): Grzyb podszywający się pod borowika. Pękaty trzon na jasnobeżowym tle pokryty jest bardzo grubą, wyraźnie wypukłą i ciemnobrązową (często brązowo-czarną) siateczką. Rurki pod kapeluszem u wyrośniętych osobników mają charakterystyczny, brudnoróżowy odcień.', '6,7,8,9,10'),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT,)).fetchone()
conn.close()
if row:
    print("UWAGA: kategoria '%s' juz istnieje (id=%s) - przerywam, zeby nie dublowac tematow." % (CAT, row['id']))
else:
    cid = add_category(CAT)
    for tekst, mies in GRZYBY:
        tid = add_topic(cid, tekst)
        c = get_connection(); c.execute("UPDATE topics SET miesiace=? WHERE id=?", (mies, tid)); c.commit(); c.close()
    c = get_connection()
    n = c.execute("SELECT COUNT(*) x FROM topics WHERE category_id=?", (cid,)).fetchone()['x']
    tc = c.execute("SELECT COUNT(*) x FROM categories").fetchone()['x']
    tt = c.execute("SELECT COUNT(*) x FROM topics").fetchone()['x']
    c.close()
    print("OK dodano kategorie '%s' (id=%s) z %d tematami grzybow." % (CAT, cid, n))
    print("RAZEM w bazie: %d kategorii, %d tematow." % (tc, tt))
