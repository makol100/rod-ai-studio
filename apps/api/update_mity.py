# -*- coding: utf-8 -*-
from src.db.database import add_topic, get_connection

CAT_NAZWA = "Ciekawostki i mity"

MITY = [
 # --- Mity o Wodzie, Glebie i Podlewaniu ---
 ("Podlewanie w słońcu pali liście (Mit): Ekstremalne makro liścia. Idealnie okrągła, wypukła kropla wody działa jak przezroczysta soczewka optyczna powiększająca zielone komórki liścia. Światło słoneczne przechodzi przez nią, ale nie tworzy żadnego brązowego wypalenia na gładkiej, zdrowej tkance.", "5,6,7,8"),
 ("Fusy z kawy silnie zakwaszają (Mit): Brązowa, grudkowata tekstura mokrych fusów z kawy rozsypana na glebie. W sam środek wbity jest profesjonalny, elektroniczny pehametr z wyświetlaczem LCD wskazującym wynik 6.5, wbrew powszechnemu przekonaniu.", None),
 ("Skorupki jaj ranią ślimaki (Mit): Zbliżenie przy ziemi. Duży, obrzydliwie śliski, brązowy ślimak nagi całkowicie gładko i bez problemu pełznie po zaporze z ekstremalnie ostrych, potłuczonych skorupek jaj, oblewając je grubą warstwą błyszczącego śluzu.", "4,5,6,7,8,9"),
 ("Rdzawe gwoździe dla hortensji (Mit): W czarnej ziemi leży garść starych, całkowicie zardzewiałych, chropowatych, pomarańczowych gwoździ. Nad nimi rośnie w pełni rozwinięty kwiat hortensji o czysto różowym kolorze, udowadniając że rdza z żelaza nie zmienia koloru kwiatów.", None),
 ("Mech zawsze oznacza kwaśną glebę (Mit): Gruby, puszysty, jaskrawozielony dywan wilgotnego mchu, który gęsto i geometrycznie porasta powierzchnię szarej, wysoce zasadowej betonowej płyty chodnikowej w głębokim, zimnym cieniu pod murem.", None),
 ("Wapnowanie razem z obornikiem (Krytyczny błąd): Zjawisko chemiczne. Mokry, słomiasty obornik posypany białym, kredowym pyłem wapna. Z miejsca styku obu substancji unoszą się smugi półprzezroczystego, falującego gazu, zniekształcającego tło.", None),
 ("Drenaż z keramzytu bez dziur w donicy (Mit): Szklana, przezroczysta donica na przekroju. Na dnie gruba warstwa brązowych kulek keramzytu. Cała ta dolna warstwa jest całkowicie zalana mętną, stojącą wodą, w której topią się i czernieją delikatne, białe korzenie.", None),
 ("Częste i płytkie podlewanie (Mit): Przekrój przez wysuszoną glebę. Woda nawilżyła tylko wierzchnie 2 centymetry, a tuż pod nią ziemia jest szara jak pył. Wszystkie korzenie rośliny zawracają nienaturalnie do góry, tuż pod powierzchnię, szukając wilgoci.", "5,6,7,8"),
 ("Sól kuchenna na chwasty (Trucizna): Gruba, geometryczna kostka brukowa. Wokół niej rozsypane krystaliczne, białe kryształki soli. Ziemia wokół jest całkowicie martwa, pokryta białą, zaschniętą skorupą, a chwast jest spalony na ciemnobrązowy węgiel.", "4,5,6,7,8,9"),
 ("Liście orzecha trują kompost (Mit): Wnętrze kompostownika z czarną, gruzełkowatą ziemią. W niej na wpół rozłożony, brązowy, skórzasty liść orzecha włoskiego. Przez jego przegniłą strukturę przechodzą zdrowe, błyszczące dżdżownice kalifornijskie.", "10,11"),
 # --- Kuchnia i Apteczka ---
 ("Zakopywanie banana pod różą: Pod ziemią, w okolicy korzeni róż. Leży tam całkowicie sczerniała, obślizgła, gnijąca skórka banana otoczona białym puchem pleśni, całkowicie zignorowana przez grube korzenie róży.", "4,5,6,7,8"),
 ("Mleko chroni przed zarazą (Półprawda): Ciemnozielony liść pomidora. Na jego gładkiej powierzchni widoczne są zaschnięte, białe, popękane łuski zsiadłego, kwaśnego mleka, formujące na krawędziach skorupę proteinową.", "6,7,8"),
 ("Pikowanie pomidorów aż po liścienie (Fakt): Makrofotografia zakopanego pędu pomidora. Z głęboko zielonej, owłosionej łodygi, która normalnie byłaby nad ziemią, przebijają się agresywnie na boki dziesiątki nowych, śnieżnobiałych, grubych korzeni.", "4,5"),
 ("Drożdże jako nawóz azotowy (Mit): Szklanka w ziemi (przekrój). Gęsta, beżowa, kipiąca piana drożdżowa agresywnie pochłania z ciemnej gleby jaskrawe, wirtualne niebieskie granulki nawozu, okradając z niego delikatne korzenie roślin.", "4,5,6"),
 ("Całkowite obrywanie liści pomidorom (Błąd): Kadr na brutalnie ogoloną, grubą łodygę pomidora. Owoce są całkowicie odsłonięte na palące słońce. Na czerwonej skórce widać ogromne, biało-żółte, pergaminowe plamy.", "7,8,9"),
 ("Oprysk z sody oczyszczonej (Błąd stężeń): Aparat szparkowy liścia w ekstremalnym powiększeniu mikroskopowym. Otwór oddychający liścia jest całkowicie i szczelnie zacementowany matowym, białym kryształem sody oczyszczonej.", "5,6,7,8"),
 ("Ocet na zmiany pH gleby (Działanie chwilowe): Kropla przezroczystego octu uderza w grudkę czarnej gleby z kawałkiem węglanu wapnia, powodując potężne, wizualne musowanie, które znika po kilku sekundach.", None),
 ("Cynamon na rany cięte (Fakt): Świeżo, geometrycznie przycięty, gruby, zielony pęd rośliny. Rana u samej góry zasypana jest gęstym, matowym, rdzawobrązowym proszkiem, który blokuje wejście mikroskopijnym, białym strzępkom pleśni.", None),
 ("Drut miedziany przebijający pomidora (Stary mit na zarazę): Gruba, owłosiona łodyga u podstawy krzaka pomidora. Na wylot, brutalnie przebita lśniącym, czystym kawałkiem miedzianego drutu. Z rany sączy się brązowy, galaretowaty sok.", "6,7,8"),
 ("Gnojówka z pokrzywy = dużo azotu (Mit): W probówce laboratoryjnej znajduje się gęsta, ciemnozielona, śmierdząca gnojówka z liściem pokrzywy. Obok unoszą się jaskrawe, chemiczne symbole: bardzo małe N i ogromne, błyszczące, żółte K.", "5,6,7"),
 # --- Zwierzeta, Owady i Potwory ---
 ("Biedronka Azjatycka vs Polska (Różnice): Ekstremalne zbliżenie ułożonych obok siebie dwóch pancerzyków. Z lewej jaskrawoczerwona, z dokładnie 7 czarnymi kropkami. Z prawej – brudnożółta, wypukła, z kilkunastoma zlewającymi się kropkami i literą M na karku.", "4,5,6,7,8,9"),
 ("Kret zjada korzenie roślin (Mit): Przekrój podziemnego tunelu. Ostre, łopatowate pazury kreta nie naruszają grubych korzeni marchwi, lecz agresywnie rozszarpują potężnego, grubego, białego pędraka w kształcie litery C.", None),
 ("Mrówki niszczą pąki piwonii (Mit): Okrągły, bardzo ciasno zamknięty, twardy, zielony pąk kwiatowy peonii. Obchodzą go powoli małe, czarne mrówki, delikatnie zlizujące błyszczące, lepkie krople słodkiego nektaru wydzielanego przez roślinę.", "4,5"),
 ("Jeże na grzbiecie noszą jabłka (Mit): Pysk jeża w makro, wąchający dżdżownicę. Obok leży idealnie nienaruszone, czerwone jabłko z ostrym światłem. Igły jeża na plecach są gładkie i nie mają możliwości fizycznego wbicia w twardy owoc.", "9,10"),
 ("Skorki wchodzą do ludzkiego ucha (Mit): Owad z potężnymi, zakrzywionymi szczypcami z tyłu odwłoka. Owad nie atakuje ucha, lecz ostro przecina szczypcami i zjada zielone mszyce oblepiające płatki georginii.", "5,6,7,8,9"),
 ("Ćma bukszpanowa nie ma wrogów naturalnych (Mit - już ma): Kontrastowe ujęcie. Ogromna, jaskrawa, neonowo-żółto-zielona gąsienica w czarne paski jest brutalnie pożerana przez ostre żuwaczki potężnej, żółto-czarnej polskiej osy dachowej.", "5,6,7,8,9"),
 ("Złotook – pożyteczny krokodyl: Ekstremalne makro larwy złotooka. Owad przypomina mikroskopijnego, szarego aligatora o potężnych, sierpowatych szczękach, a na własnych plecach nosi absurdalną górę zebranych, wyssanych, białych trucheł mszyc.", "5,6,7,8,9"),
 ("Ropucha wywołuje kurzajki (Mit): Ropucha szara o całkowicie suchej, szorstkiej skórze w kolorze miedziano-brązowym, gęsto pokrytej brodawkami. Jej głaskanie na grafice nie powoduje niczego złego – gruczoły z jadem reagują tylko na atak zębami drapieżnika.", "4,5,6,7,8,9"),
 ("Pszczoła umiera po użądleniu, osa nie (Fakt): Makro na ludzką skórę/grubą rękawicę. Brązowe żądło pszczoły ma wyraźne, skierowane do tyłu haki. Osa (obok) ma żądło idealnie gładkie jak igła medyczna.", "5,6,7,8,9"),
 ("Pająki jako ogrodowe szkodniki (Mit): Piękny, geometryczny pająk tygrzyk paskowany, siedzący w centrum potężnej sieci kołowej rozpiętej między krzewami pomidorów. W sieć złapał się szkodnik – owad latający.", "7,8,9"),
 # --- Kosmiczna Botanika ---
 ("Pomidor to owoc (jagoda): Botaniczny dowód. Przekrojony na pół, lśniący pomidor z ziarnami otoczonymi zielonkawą galaretką. Obok niego, dla uświadomienia, leży tak samo zbudowana przekrojona borówka i winogrono – wszystkie ułożone na czarnej tablicy edukacyjnej.", "7,8,9"),
 ("Zjawisko guttacji (Płacz roślin to nie rosa): Świt, bez rosy na zewnątrz. Ząbkowany brzeg idealnie suchego liścia truskawki. Dokładnie z każdego ząbka wypływa, z wnętrza rośliny, pojedyncza, nieskazitelnie czysta, kulista kropla wody rzucająca blask.", "5,6,7,8,9"),
 ("Symbioza Mikoryzowa (Wood Wide Web): Przekrój geologiczny pod ziemią. Grube, ciemnobrązowe, zdrewniałe korzenie sosny płynnie łączą się i wplatają w gęstą, jarzącą się delikatnym światłem, śnieżnobiałą pajęczynę grzybni.", None),
 ("Dlaczego marchew jest pomarańczowa (Holandia): Na surowym drewnie ułożony jest pęczek dzikich i pierwotnych korzeni marchwi – są one w kolorze głębokiego, ciemnego fioletu, wulgarnej purpury i kredowej bieli. Pomarańczowej brak.", None),
 ("Strzelające nasiona (Niecierpek pospolity): Ujęcie z zamrożonym ruchem. Zielona, nabrzmiała torebka nasienna niecierpka, dotknięta palcem, eksploduje – jej paski błyskawicznie zwijają się w spirale, z ogromną siłą wystrzeliwując czarne kuleczki nasion.", "7,8,9"),
 ("Tigmotropizm (Dotyk u pnączy): Makrofotografia z efektem poklatkowym. Jasnozielony, niezwykle cienki wąs czepny groszku pachnącego, po dotknięciu szorstkiego zardzewiałego drutu, ciasno, wielokrotnie i spiralnie owija się wokół niego.", "4,5,6,7"),
 ("Kwitnienie Agawy (Raz w życiu i śmierć): Olbrzymia rozeta starych, matowych, sinoniebieskich liści agawy, które stają się pomarszczone i brązowe. Z samego jej środka strzela w niebo absurdalnie wysoki, pięciometrowy, zdrewniały słup zakończony żółtymi kwiatostanami.", None),
 ("Fascykulacja (Staśmienie łodygi - Błąd genetyczny): Zamiast okrągłej łodygi u mniszka lekarskiego – rośnie szeroki na kilka centymetrów, płaski, karbowany zielony pas złożony z zrośniętych komórek, na szczycie którego znajduje się monstrualny, zniekształcony, żółty kwiat.", "4,5,6,7"),
 ("Fototropizm Słoneczników (Tylko za młodu): Pole słoneczników. Wszystkie młode, zielone tarcze są ostro i pod równym kątem wygięte w stronę nisko świecącego na zachodzie czerwonego słońca. Stare, wielkie i czarne głowy obok patrzą bezwładnie w dół.", "6,7,8"),
 ("Płeć kwiatów cukinii (Męskie vs Żeńskie): Makro dwóch kwiatów. Z lewej strony żeński – na łodyżce, tuż pod kielichem kwiatu, znajduje się idealnie uformowana, miniaturowa zielona cukinia. Z prawej męski – kwiat osadzony na zupełnie prostej, długiej, łysej łodyżce.", "6,7,8"),
 # --- Prawne i Historyczne Sekrety ROD ---
 ("Najstarszy ROD w Polsce (1897 rok, Grudziądz): Obraz w sepii, stylizowany na wczesną fotografię na szkle. Eleganccy dżentelmeni z epoki w cylindrach i kamizelkach oraz panie w długich sukniach, opierający się o drewniane grabie na tle rzędów uprawianej, starodawnej kapusty.", None),
 ("ROD to nie park publiczny (Prawo własności): Potężna, zamknięta na łańcuch z kłódką ciemnozielona brama wejściowa. Na niej wisi surowa, blaszana, emaliowana na biało tablica z jaskrawoczerwonymi, grubymi literami: Teren Zamknięty ROD - Wstęp Tylko dla Działkowców.", None),
 ("Limit wysokości drzewa na działce (Wymysł vs Regulamin): Rzut drona z góry. Pomiędzy niskimi, słonecznymi działkami z trawnikami rośnie jeden gigantyczny, ciemny, stary, ponury świerk. Drzewo rzuca potężny, czarny cień, który swoją geometrią zakrywa wegetację na trzech sąsiednich działkach.", None),
 ("Zamieszkiwanie na działce (Absolutny zakaz): Mroźna, zimowa, bezksiężycowa noc na terenie ROD, przykrytym metrem białego, gładkiego śniegu. W absolutnej ciemności całego sektora, tylko w jednym oknie murowanej, szczelnej altanki świeci się ostre, pomarańczowe światło i gęsty dym leci z komina.", "11,12,1,2"),
 ("Studnia głębinowa a Prawo Wodne: Potężne, stalowe ramię wiertni wbite głęboko w brązową glinę. Z odwiertu wystaje rura PCV, obok której leży rozciągnięta stalowa taśma miernicza z wyraźną, żółtą cyfrą wskazującą barierę 30 metrów.", None),
 ("Pszczoły w ROD (Wymuszony lot wzwyż): Drewniany, klasyczny ul pomalowany na błękitno. Ul ze wszystkich stron jest niesamowicie szczelnie i wysoko otoczony litym murem z gęsto przyciętych, ostrych tuj, zmuszając wylatujące owady do pionowego startu w niebo.", None),
 ("Spalanie gałęzi na ognisku (Zakaz całoroczny): Ujęcie bardzo bliskie. Czerwony, płonący ogień trawiący zeschłe gałęzie gruszy, z których unosi się duszący dym. Na rozmyty horyzont nakłada się postać funkcjonariusza Straży Miejskiej w mundurze trzymającego bloczek mandatowy.", None),
 ("Altana czy Samowola budowlana (Limit 35m2): Grafika inżynieryjna nakładająca się na zdjęcie altany. Grube, czerwone, wymiarowane linie nałożone tylko na zewnętrzne, ocieplone mury szarego budynku, całkowicie pomijające obrys szerokiego, drewnianego, zadaszonego tarasu.", None),
 ("Kompostownik to przymus regulaminowy: Skrzynia z desek z ciemnym nawozem, otoczona jaskrawą, magiczną, złotą aurą z ulatującymi z niej blaskami, symbolizująca że kompost to obowiązkowe złoto ogrodnika zgodnie z przepisami PZD.", None),
 ("Handel plonami (Zakaz komercyjny): Drewniana, prosta skrzynka z jabłkami i pomidorami stojąca przy alejce wejściowej. Na skrzynce widnieje biała, tekturowa etykieta z nabazgraną, dużą ceną, na którą nakłada się gigantyczny, czerwony krzyżyk i słowo NIELEGALNE.", "7,8,9"),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT_NAZWA,)).fetchone()
if not row:
    print("BLAD: kategoria '%s' nie istnieje - przerywam." % CAT_NAZWA)
else:
    cid = row['id']
    stare = conn.execute("SELECT id, tekst FROM topics WHERE category_id=?", (cid,)).fetchall()
    print("Usuwam %d starych tematow:" % len(stare))
    for t in stare:
        print("  -", t['tekst'][:50])
    conn.execute("DELETE FROM topics WHERE category_id=?", (cid,))
    conn.commit()

    for tekst, mies in MITY:
        tid = add_topic(cid, tekst)
        if mies is not None:
            c = get_connection(); c.execute("UPDATE topics SET miesiace=? WHERE id=?", (mies, tid)); c.commit(); c.close()

    c = get_connection()
    po = c.execute('SELECT COUNT(*) x FROM topics WHERE category_id=?', (cid,)).fetchone()['x']
    tc = c.execute("SELECT COUNT(*) x FROM categories").fetchone()['x']
    tt = c.execute("SELECT COUNT(*) x FROM topics").fetchone()['x']
    c.close()
    print("\nOK: '%s' (id=%s) ma teraz %d tematow." % (CAT_NAZWA, cid, po))
    print("RAZEM w bazie: %d kategorii, %d tematow." % (tc, tt))
conn.close()
