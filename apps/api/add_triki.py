# -*- coding: utf-8 -*-
from src.db.database import add_topic, get_connection

CAT_NAZWA = "Sprawdzone triki dzialkowca"

TRIKI = [
 # --- Walka ze Szkodnikami i Chwastami (Naturalne Bariery) ---
 ("Taśma miedziana na ślimaki: Zbliżenie na szorstką, czerwoną cegłę podniesionej grządki. Wokół krawędzi naklejona jest idealnie płaska, lśniąca, gładka taśma z czystej miedzi, odbijająca promienie słoneczne niczym lustro.", "4,5,6,7,8,9"),
 ("Bariera ze skorupek jaj: Makrofotografia ziemi. Wokół zielonej, kruchej łodyżki sałaty usypany jest gęsty pierścień z ekstremalnie ostrych, poszarpanych, białych i jasnobrązowych, pokruszonych skorupek jaj, tworzących geometryczny mur.", "4,5,6,7,8,9"),
 ("Wrzątek na chwasty w kostce: Pęknięcie między szarymi kostkami brukowymi. Z metalowego, błyszczącego czajnika wylewa się gruby strumień wrzącej wody bezpośrednio na zielony chwast. Wokół rośliny unosi się gęsta, biała para wodna, a liście natychmiast ciemnieją.", "4,5,6,7,8,9"),
 ("Popiół drzewny przeciw mrówkom: Kopiec z sypkiego, szarego piasku między płytami chodnikowymi. Z góry posypywany jest bardzo drobnym, jasnoszarym, suchym popiołem z węgielkami. Kontrast między szorstkim piaskiem a matowym, gładkim pyłem.", "4,5,6,7,8,9"),
 ("Żółte lepy (Pułapki chromatyczne): Jaskrawożółta, prostokątna, plastikowa tabliczka zawieszona na sznurku w szklarni. Powierzchnia tabliczki jest nienaturalnie lepka i błyszcząca, a w gęstym kleju uwięzione są dziesiątki mikroskopijnych, czarnych muszek.", "4,5,6,7,8,9"),
 ("Odstraszacz z płyt CD na ptaki: Zwisająca z gałęzi jabłoni stara płyta CD. Powierzchnia płyty działa jak pryzmat – w ostrym słońcu rozszczepia światło, rzucając agresywny, tęczowy blask na otaczające, matowe liście.", "6,7,8,9"),
 ("Oprysk z szarego mydła (Na mszyce): Półprzezroczysta butelka ze spryskiwaczem. Wewnątrz widać mętną, spienioną wodę z zanurzonymi wiórkami szarego, kostkowego mydła. Z dyszy wystrzeliwuje bardzo gęsta mgiełka pokrywająca mszyce na róży.", "4,5,6,7,8"),
 ("Plastikowe widelce przeciw kotom: Ciemna, świeżo przekopana ziemia na grządce. W regularnych odstępach, pionowo w ziemię powbijane są rzędy tanich, białych, plastikowych widelców zębami do góry, tworzących ostrą zaporę.", "4,5,6,7,8,9"),
 ("Kawałki mydła na sarny/dziki: Gałązka młodego drzewka owocowego. Do kory przywiązany jest surowym sznurkiem mały, różowy, pachnący kawałek mydła w kostce, odcinający się kolorem od natury.", None),
 ("Aksamitki jako gąbka na nicienie: Korzeń wyrwanej, pomarańczowej aksamitki umazany w mokrej ziemi. Zbliżenie na bardzo gęstą, białą siatkę korzeniową, która w naturalny sposób czyści glebę przed posadzeniem warzyw.", "5,6,7,8,9"),
 # --- Sprytne Nawadnianie i Oszczedzanie Wody ---
 ("Gliniane dzbany Olla (System korzeniowy): Przekrój gleby. W ziemi zakopany jest pękaty, surowy, porowaty dzban z pomarańczowej terakoty z pokrywką na górze. Woda z dzbana powoli przesiąka przez pory naczynia, a wokół niego owijają się białe korzenie.", "4,5,6,7,8,9"),
 ("Kroplownik z butelki PET: Odwrócona do góry dnem przezroczysta butelka po wodzie mineralnej, ze ściętym dnem. Nakrętka butelki jest zakopana w ziemi przy pomidorze, a woda wewnątrz powoli i równomiernie opada.", "4,5,6,7,8,9"),
 ("Nawadnianie sznurkiem (Knot): Mosiężna konewka pełna wody stojąca wyżej. Z niej zwisa gruby, bawełniany, biały sznurek, który nasiąkł wodą na całej długości i wchodzi prosto do czarnej ziemi w doniczce poniżej.", "4,5,6,7,8,9"),
 ("Gąbka na dnie doniczki: Pusta, plastikowa doniczka. Na samym jej dnie, przed nasypaniem ziemi, ułożona jest docięta, gruba, żółta gąbka kąpielowa z widocznymi, dużymi porami, pochłaniającymi resztki wody.", None),
 ("Łańcuch deszczowy (Zamiast rynny PCV): Krawędź drewnianego dachu altany. Zamiast plastikowej rury spustowej zwisa gruby, mosiężny łańcuch ze spiętymi ze sobą małymi dzwoneczkami. Po ogniwach spływa lśniąca, kaskadowa woda z deszczu.", None),
 ("Butelkowy klosz (Miniszklarenka): Na ziemi rośnie mikroskopijna, delikatna zielona siewka. Jest szczelnie przykryta przezroczystą górną połówką dużej butelki PET. Wewnątrz plastiku osadziły się gęste, parujące krople rosy.", "3,4,5"),
 ("Podstawka z keramzytem (Wilgotność): Pod szeroką, płaską podstawką doniczki leży warstwa brązowych, kulistych, wypalanych kulek glinianych. Keramzyt zanurzony jest w wodzie tylko do połowy, tworząc wilgotny mikroklimat.", None),
 ("Kostki lodu dla storczyków: Na chropowatej, jasnej korze sosnowej w przezroczystej doniczce ułożone są trzy idealnie kwadratowe, krystalicznie czyste kostki lodu. Lód zaczyna się topić, powoli uwalniając pojedyncze krople lodowatej wody.", None),
 ("Zakopana doniczka rezerwowa: Pomiędzy gęsto posadzonymi dyniami wkopana jest na równo z ziemią duża, pusta plastikowa doniczka z wielkimi otworami na dnie. Dłoń wlewa wodę z węża prosto do pustej doniczki, nie mocząc liści wokół.", "5,6,7,8"),
 ("Ściółkowanie grubym kartonem: Szary karton z tektury falistej rozłożony bezpośrednio na zarośniętej chwastami ziemi. Na karton sypana jest gruba, czarna warstwa świeżej ziemi kompostowej, całkowicie dusząc niechcianą roślinność bez użycia chemii.", "3,4,9,10"),
 # --- Upcykling, Rozsada i Zero Waste ---
 ("Rozsada w rolkach po papierze: Zbliżenie na ułożone ciasno obok siebie w plastikowym pojemniku szare, tekturowe rurki. Wypełnione są czarną, wilgotną ziemią, a z każdej wyrasta jeden gruby, zielony pęd. Tektura na dole rurek jest już namoknięta i miękka.", "3,4"),
 ("Szufelka z bańki po mleku: Przecięta ukośnie nożem do tapet biała, półprzezroczysta, duża butelka z grubego plastiku z uchwytem. Wycięty kształt tworzy idealną, mocną szuflę, za pomocą której ktoś przesypuje garść perlitu ogrodniczego.", None),
 ("Wytłoczki po jajkach (Siew): Otwarty, szary kartonik po 10 jajkach. W każdym małym wgłębieniu z wytłoczonego papieru znajduje się szczypta ziemi i dwa mikroskopijne nasionka. Tektura ma chropowatą, gąbczastą teksturę chłonącą wodę z atomizera.", "3,4"),
 ("Znaczniki ze starych żaluzji: Twarda, brązowa ziemia na grządce. Wbity w nią jest krótki, docięty kawałek wygiętego, jasnego paska ze starych rolet okiennych. Czarnym, wodoodpornym markerem zapisano na plastiku gruby napis nazwy warzywa.", None),
 ("Mini-szklarenka z pudełka po płytach CD: Stare, przezroczyste opakowanie po płytach CD nałożone na małą doniczkę. Środkowy, plastikowy, czarny trzpień został ucięty. Pokrywa z lśniącego, gładkiego poliwęglanu tworzy doskonałą ochronę z idealnym dostępem światła.", "3,4,5"),
 ("Puszka po brzoskwiniach jako doniczka: Błyszcząca, cynowa puszka z charakterystycznym falistym żebrowaniem po bokach. Dno puszki zostało przebite grubym gwoździem. Wewnątrz rośnie gęsta bazylia.", None),
 ("Siatka z pomarańczy (Na czosnek): Czerwona, bardzo cienka i gęsta plastikowa siateczka po owocach z supermarketu, zawiązana na pęk. Wewnątrz niej suszą się brudne główki czosnku, zawieszone na starym gwoździu w cieniu drewnianej wiaty.", "7,8"),
 ("Rurki PCV na siatce (Organizer): Odcięte pod kątem prostym kawałki białych rur kanalizacyjnych o średnicy 5 cm, przymocowane trytytkami do stalowej siatki zbrojeniowej w altanie. W rurkach pionowo wetknięte są długie pędzle i nożyce.", None),
 ("Pionowy ogród z palety euro: Klasyczna drewniana paleta postawiona pionowo. Pod każdą poprzeczną deską zszywaczem tapicerskim przymocowano czarną agrowłókninę, tworząc kieszenie wypchane ziemią, z których wylewają się kaskady czerwonych pelargonii.", "5,6,7,8,9"),
 ("Wiszący kosz z durszlaka: Stary, emaliowany, biały cedzak z odpryskami farby, zawieszony na trzech łańcuszkach. Otwory durszlaka idealnie przepuszczają wodę, a w środku rośnie bujna, zwisająca truskawka.", "5,6,7"),
 # --- Apteka Dzialkowca (Nietypowe Zasilanie Roslin) ---
 ("Skórki banana pod krzakiem róż: Makrofotografia ziemi. Zżółknięta skórka od banana, pokrojona w małe, centymetrowe, geometryczne kostki, mieszana małymi pazurkami ogrodniczymi z czarną glebą tuż przy kolczastej łodydze.", "4,5,6,7,8"),
 ("Roztwór z drożdży piekarskich: Stara, szara szklanka z grubego szkła. W połowie napełniona jest mętną, beżową cieczą. W cieczy widać potężną, gazującą pianę, pęczniejącą po dodaniu ciepłej wody i cukru do kruszących się, świeżych drożdży z kostki.", "4,5,6"),
 ("Uzupełnianie żelaza rdzą: Głęboka, czarna bryła korzeniowa hortensji. Pomiędzy białe korzenie wrzucana jest garść bardzo starych, całkowicie zardzewiałych, chropowatych gwoździ i mosiężnych śrub, powoli uwalniających związki żelaza do gleby.", "4,5,6,7,8"),
 ("Sól Epsom dla zielonego trawnika: Dłoń rozsypująca na krótkiej, zielonej murawie krystalicznie czyste, drobne igiełki siarczanu magnezu. Kryształki lśnią w słońcu niczym stłuczone szkło, powoli rozpuszczając się w porannej rosie.", "4,5,6,7,8,9"),
 ("Wywar z łupin cebuli: Słoik z jasnym, pomarańczowo-złotym, krystalicznym płynem o barwie bursztynu, w którym pływają cienkie, niemal przezroczyste łuski z cebuli. Strumień z wężyka opryskiwacza nakłada tę ciecz na gładkie liście storczyka.", None),
 ("Oprysk z mleka na zarazę: Biały osad na ciemnozielonym, szorstkim liściu pomidora. Z małego zraszacza wydobywa się mgła rozcieńczonego mleka. Mleczne krople zasychają na powierzchni liścia, tworząc bardzo cienką, chroniącą przed grzybami, błyszczącą powłokę.", "6,7,8"),
 ("Aspiryna jako ukorzeniacz: W szklance czystej wody leży biała, rzeźbiona tabletka aspiryny. Tabletka właśnie się rozpuszcza, wypuszczając gęstą strugę mikrobąbelków w górę. W wodzie zanurzona jest zielona, odcięta łodyżka pelargonii z gładkim cięciem.", "6,7,8,9"),
 ("Cynamon na rany po cięciu: Ostra, bolesna rana na grubym, zdrewniałym pędzie drzewa owocowego tuż po odcięciu konara. Powierzchnia cięcia jest gęsto pudrowana drobnym, rudo-brązowym, matowym proszkiem cynamonu.", None),
 ("Ocet spirytusowy do zmiany pH: Czysta konewka. Z butelki wylewa się krystaliczny ocet spirytusowy. Kadr skupia się na falowaniu powierzchni wody w konewce przed podlaniem kwasolubnej borówki amerykańskiej rosnącej w torfie.", "4,5,6,7,8,9"),
 ("Żelatyna jako azot pod korzeń: Przesuszona ziemia w doniczce tarasowej. Ktoś posypuje wierzchnią warstwę żółtymi, szklistymi, twardymi grudkami surowej żelatyny wieprzowej, która pod wpływem wilgoci pęcznieje i staje się miękka.", "4,5,6,7,8,9"),
 # --- Ergonomia i Majsterkowanie (Sprytny Warsztat) ---
 ("Wiadro z piaskiem i olejem na narzędzia: Czerwone wiadro wypełnione po brzegi gęstym, drobnym, mokrym i ubitym piaskiem nasączonym olejem silnikowym. Ostrza lśniących sekatorów i metalowych łopatek są mocno wbite na sztorc w środek piasku.", None),
 ("Mydło pod paznokciami (Przed pracą): Zbliżenie na dłonie. Paznokcie są twardo przeciągane po solidnej, białej kostce szarego mydła. Między paznokciem a skórą wbija się zwarta masa mydlana, blokując fizycznie drogę dla czarnej ziemi podczas pielenia.", None),
 ("Magnes na kiju teleskopowym: Rura ukryta w gęstej, wysokiej trawie. Na końcu wysuniętego, srebrnego kija teleskopowego znajduje się silny magnes neodymowy, do którego przykleiła się rozsypana garść zardzewiałych, stalowych gwoździ dekarskich.", None),
 ("Złączki drukowane w 3D z żywicy: Zbliżenie na zawór wody na zewnątrz. Do kranu podpięta jest idealnie gładka, twarda przejściówka węża wydrukowana z szarej, utwardzanej promieniami UV żywicy. Geometria krawędzi jest ostra jak brzytwa, idealnie spasowana z gwintem.", None),
 ("Taśma izolacyjna jako znacznik głębokości: Jasny, drewniany, profilowany trzonek małej łopatki. Na trzonku, w odmierzonych odstępach, owinięto ciasno trzy pasy jaskrawoczerwonej taśmy izolacyjnej z PCV, tworząc niezmywalną miarkę głębokości do sadzenia cebulek.", "3,4,5"),
 ("Opaski zaciskowe (Trytytki) na stelaż: Łączenie dwóch grubych, śliskich, aluminiowych rurek w namiocie tunelowym. Spięte krzyżowo dwiema bardzo grubymi, czarnymi, zębatymi opaskami zaciskowymi, tworzącymi sztywne, nierozerwalne łączenie węzła.", None),
 ("Kołeczki do golfa do odstępów: Linia posiana na grządce. Zamiast znaczników, w ziemi równo co 10 cm osadzone są jaskrawe, czerwone, żółte i białe drewniane kołeczki golfowe z wyraźnym, wklęsłym łebkiem na górze.", "3,4,5"),
 ("Karabińczyk na rękawice robocze: Pasek od spodni roboczych z grubego dżinsu. Do szlufki przypięty jest aluminiowy, metaliczny karabińczyk alpinistyczny, na którym wiszą za pętelki szorstkie, skórzane rękawice spawalnicze/ogrodowe.", None),
 ("Jaskrawa farba na narzędziach: Trzonki drewnianych łopat, sekatorów i grabi leżących swobodnie w wysokiej trawie. Same końcówki każdego trzonka zostały zanurzone w absolutnie jaskrawej, odblaskowej, żółtej i różowej farbie emaliowej, krzycząc na tle zieleni ogrodu.", None),
 ("Organizer z worka na buty: Zwykły, płaski organizer wiszący przymocowany do drzwi wiaty narzędziowej. W każdej foliowej komorze precyzyjnie posegregowane są kolorowe, papierowe saszetki z nasionami, wyeksponowane jak w aptece.", None),
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

    for tekst, mies in TRIKI:
        tid = add_topic(cid, tekst)
        if mies is not None:
            c = get_connection(); c.execute("UPDATE topics SET miesiace=? WHERE id=?", (mies, tid)); c.commit(); c.close()

    c = get_connection()
    po = c.execute('SELECT COUNT(*) x FROM topics WHERE category_id=?', (cid,)).fetchone()['x']
    tc = c.execute("SELECT COUNT(*) x FROM categories").fetchone()['x']
    tt = c.execute("SELECT COUNT(*) x FROM topics").fetchone()['x']
    c.close()
    print("OK dodano %d tematow do '%s' (id=%s)." % (len(TRIKI), CAT_NAZWA, cid))
    print("Kategoria: bylo %d, jest teraz %d." % (przed, po))
    print("RAZEM w bazie: %d kategorii, %d tematow." % (tc, tt))
