# -*- coding: utf-8 -*-
from src.db.database import add_topic, get_connection

CAT_NAZWA = "Co siac / co robic teraz"

KALENDARZ = [
 # --- Wiosenny Start (Siewy, Rozsady, Budzenie Gleby) ---
 ("Wysiew nasion pomidorów (Rozsada): Makrofotografia. Na idealnie czarnej, wilgotnej i puszystej ziemi leżą ułożone w równych odstępach mikroskopijne, płaskie, okrągłe nasionka o wyraźnie włochatej (omszonej), jasnobeżowej powierzchni.", "3"),
 ("Pikowanie siewek (Kluczowy chwyt): Zbliżenie na opuszki palców ubrudzone ziemią. Palce delikatnie trzymają mikroskopijną, jasnozieloną siewkę wyłącznie za dwa idealnie symetryczne, owalne liścienie, unikając dotykania cieniutkiej jak włos, białej łodyżki.", "3,4"),
 ("Siew rzodkiewki do gruntu: Geometria grządki. W zbitej, szarej ziemi wyciągnięty jest idealnie prosty, płytki na 2 centymetry rowek o przekroju litery V. Na dnie rowka leżą równo rozsypane, jaskrawo ubarwione, idealnie okrągłe nasiona.", "3,4,5"),
 ("Sadzenie cebuli dymki: Powierzchnia pulchnej gleby. Kciuk dociska w dół małą, suchą, miedziano-złotą cebulkę, wciskając ją w czarną ziemię tak, że na zewnątrz wystaje jedynie suchy, poskręcany w szpic sam czubek.", "4"),
 ("Siew groszku zielonego: Płytka, długa bruzda w ciemnej ziemi. Na jej dnie leżą duże, wyraźnie pomarszczone (faktura zaschniętego mózgu), jasnozielone lub żółtawe, nieregularne nasiona grochu.", "4"),
 ("Przygotowanie wielodoniczek: Kwadratowa paleta z czarnego, cienkiego plastiku, podzielona na dziesiątki idealnie równych, kwadratowych komórek. Każda komórka jest równo po brzegi wypełniona brązowym, suchym torfem, z centralnym, okrągłym wgłębieniem od ołówka.", "2,3"),
 ("Rozkładanie białej agrowłókniny (P17): Rząd niskich, wygiętych w łuk stalowych pałąków wbitych w brązową ziemię. Na nich mocno naprężona jest przepuszczająca światło, śnieżnobiała włóknina z drobną krateczką splotu. Brzegi materiału szczelnie przysypane są równym wałem ziemi.", "3,4,5"),
 ("Hartowanie rozsady pomidorów: Drewniany, surowy stół na zewnątrz w chłodnym, porannym słońcu. Na nim stoją rzędy czarnych doniczek z krępymi, ciemnozielonymi, owłosionymi sadzonkami pomidorów o mocno fioletowych spodach liści i łodygach.", "5"),
 ("Sadzenie podkiełkowanych ziemniaków: Wnętrze ciemnego dołka zrobionego w ziemi szpadlem. Na jego dnie leży mocno pomarszczona, stara, bladożółta bulwa ziemniaka, z której sterczą pionowo do góry potężne, grube, poskręcane, fioletowo-zielone kiełki.", "4,5"),
 ("Zraszanie siewek (Mgła): Przezroczysty, plastikowy opryskiwacz ręczny. Z mosiężnej, precyzyjnej dyszy wydobywa się szeroki, przestrzenny stożek absolutnie drobnej, mikroskopijnej mgiełki wodnej, osiadającej w postaci błyszczących pereł na malutkich, zielonych listkach.", "3,4,5"),
 # --- Letnia Pielegnacja (Ciecie, Woda i Zbiory) ---
 ("Ogławianie pomidorów (Koniec lata): Makro na sam szczyt potężnego krzaka. Ostre, lśniące ostrza sekatora przecinają grubą, włochatą łodygę główną dokładnie centymetr nad najwyższym, żółtym gronem kwiatowym, zatrzymując wzrost rośliny w górę.", "8,9"),
 ("Uszczykiwanie pędów ogórka: Zbliżenie na dłoń. Paznokcie szczypią i ułamują sam, niezwykle cienki, jaskrawozielony czubek pędu bocznego ogórka z maleńkimi, kolczastymi zawiązkami liści, tuż za małym, żółtym kwiatkiem.", "6,7,8"),
 ("Przerywanie buraczków ćwikłowych: Gęsty rządek młodych roślin o bordowych łodygach. Dłoń brutalnie wyrywa całą garść nadmiarowych, ciasno rosnących listków z korzeniami, pozostawiając w ziemi pojedyncze, silne sztuki oddalone od siebie o równe 5 cm.", "5,6"),
 ("Zbiór czosnku zimowego: Mocno spieczona, pęknięta z gorąca żółtawa ziemia. Z pęknięcia wyciągana jest do połowy potężna, biało-fioletowa główka czosnku, której dolna część tworzy pęk brudnych, suchych, szarych, nitkowatych korzeni.", "7"),
 ("Siew poplonu letniego (Gorczyca): Kadr zamrożony w ruchu. Z rozwartej ludzkiej dłoni sypie się w dół gęsty grad idealnie okrągłych, twardych, lśniących kuleczek w musztardowo-żółtym kolorze, na tle sypkiej, rozgrabionej ziemi.", "7,8"),
 ("Ściółkowanie skoszoną trawą: Gruba, mięsista łodyga pomidora wychodząca z czarnej ziemi. Wokół łodygi rozłożony jest gęsty, kilkucentymetrowy pierścień ze skompresowanej, niezwykle jaskrawej, jasnozielonej, mokrej od soku, drobno pociętej trawy.", "5,6,7,8"),
 ("Podlewanie kropelkowe w upały: Zbliżenie (makro) na czarną, grubą, matową rurę z polietylenu wijącą się na wysuszonej na wiór ziemi. Z małego otworu w rurze formuje się idealnie kulista kropla wody, rzucająca ostry cień w rażącym, letnim słońcu.", "6,7,8"),
 ("Usuwanie przekwitłych kwiatostanów róż: Zielone, kolczaste pędy krzewu. Srebrne nożyce ogrodowe odcinają tuż nad pierwszym zdrowym liściem całkowicie brązowy, wyschnięty, pomarszczony pąk dawnej róży.", "6,7,8,9"),
 ("Zbiór ogórków (Faktura kolców): Duży, ciemnozielony liść ogórka odchylony palcami. Pod spodem ukryty jest idealnie cylindryczny, jasnozielony owoc, po brzegi obsypany białymi, sterczącymi, kłującymi mikrowypustkami.", "6,7,8"),
 ("Uszczykiwanie wilków na winorośli: Gruba, brązowa, łuszcząca się łoza. Kciuk wyłamuje z jej boku mały, zielony, kruchy, wodnisty pęd, który zaczął rosnąć w niewłaściwym, pionowym kierunku.", "5,6,7"),
 # --- Jesienne Porzadki (Poplony, Kopanie, Przechowywanie) ---
 ("Sadzenie czosnku zimowego: Twarda, jesienna, chłodna ziemia. Kciuk w grubej rękawicy wciska pojedynczy, duży, geometryczny ząbek czosnku w nieobieranej fioletowej łusce pionowo w dół, ostrą końcówką skierowaną idealnie do góry.", "9,10"),
 ("Wykopki marchwi (Widły szerokozębne): Lśniące, srebrne, grube zęby amerykańskich wideł wbite pod kątem w zbitą, czarną ziemię. Ziemia jest podważona do góry pękając, a spomiędzy grud ukazuje się pięć idealnie prostych, jaskrawo pomarańczowych korzeni marchwi.", "9,10,11"),
 ("Przekopywanie na ostrą skibę: Powierzchnia ogrodu w głębokim, jesiennym cieniu. Gleba leży w chaotycznych, potężnych, czarnych bryłach wielkości piłki, odwróconych do góry dnem przez szpadel. Powierzchnia brył jest mokra i błyszcząca w punktowym świetle.", "10,11"),
 ("Siew koperku ozimego: Chłodna, szara ziemia bez grudek. Na jej powierzchni leżą mikroskopijne, płaskie, brązowo-żółte nasionka z delikatnym paseczkiem wokół krawędzi, oczekujące na przysypanie cienką warstwą piasku.", "8,9"),
 ("Przycinanie bylin na zimę: Rząd zeschłych, całkowicie brązowych, pustych w środku, rurkowatych łodyg po jeżówkach. Duże, dwuręczne nożyce tną je wszystkie równo, zaledwie 5 centymetrów nad zmarzniętą ziemią przysypaną opadłymi liśćmi dębu.", "10,11"),
 ("Zbiór dyni na przechowywanie: Ogromna, twarda, intensywnie pomarańczowa dynia. Sekator odcina jej gruby, całkowicie skorkowaciały, pokryty głębokimi, jasnoszarymi bruzdami, twardy ogonek, zostawiając 10 cm pędu, niezbędny do długiego leżakowania.", "9,10"),
 ("Czyszczenie i dezynfekcja tunelu foliowego: Wnętrze dużego namiotu. Folia jest zmatowiała od wilgoci. Wewnątrz nie ma już żadnych roślin, pozostaje tylko gładka, odchwaszczona, brązowa ziemia i zawieszone pod dachem żółte lepce ociekające starym, miodowym klejem.", "10,11"),
 ("Zbieranie liści orzecha włoskiego: Grabie wachlarzowe o sprężystych, stalowych drutach zagarniają z trawnika na jedną kupę charakterystyczne, ciemnobrązowe, skórzaste liście orzecha, które ze względu na garbniki nie mogą trafić na główny kompost.", "10,11"),
 ("Zbiór jabłek z szypułkami: Dłoń chwyta ciemnoczerwone jabłko pokryte matowym, siwym nalotem. Palec wskazujący delikatnie obraca owoc w górę, aby ułamać ogonek idealnie od gałązki drzewa, nie wyrywając go z samego jabłka.", "9,10"),
 ("Rozrzucanie obornika (Jesienne nawożenie): Widły rozrzucają ciężki, słomiasto-brązowy, przefermentowany obornik w grubych, wilgotnych, ciemnych płatach bezpośrednio na odchwaszczoną, gołą, zmarzniętą ziemię tuż przed przekopaniem.", "10,11"),
 # --- Zimowe Przygotowania (Ochrona przed Mrozem i Szkodnikami) ---
 ("Kopczykowanie róż: Grube, ciemnozielone pędy róży z ostrymi, haczykowatymi kolcami, ścięte do połowy. U podstawy krzewu usypany jest wysoki na 30 cm, geometryczny, równy stożek z puszystej, ciemnej ziemi, całkowicie zakrywający miejsce szczepienia.", "10,11"),
 ("Bielenie pni drzew owocowych: Zbliżenie na bardzo chropowatą, głęboko spękaną, szarą korę starej jabłoni. Szeroki, okrągły pędzel o grubym włosiu wciera w bruzdy gęstą, idealnie śnieżnobiałą, matową pastę z wapna palonego.", "10,11,12"),
 ("Zakładanie osłonek przed zającami: Cienki, gładki pień młodej wisienki owijany jest sztywną, jasnoniebieską, plastikową spiralą z perforacją. Plastik szczelnie sprężynuje wokół kory na tle białego, zmrożonego śniegu.", "10,11"),
 ("Okrywanie bylin stroiszem: Rabata ogrodowa. Na ziemi ułożone są płasko i dachówkowato bardzo gęste, ciemnozielone, odcięte gałęzie świerkowe. Ostre igły tworzą trójwymiarową warstwę izolacji pokrytą lekkim szronem.", "11,12"),
 ("Owijanie agrowłókniną (Kaptury zimowe): Smukły, pionowy krzew owinięty w bardzo grubą, sztywną, białą tkaninę formującą geometryczny kształt kolumny lub stożka, mocno ściśniętą na samym dole grubym, brązowym sznurkiem jutowym.", "10,11"),
 ("Przegląd zapasów w piwnicy: Chłodne, skąpe światło. Skrzynka z surowego drewna, w której obok zdrowych jabłek leży jedno, wyraźnie zepsute: całkowicie pokryte koncentrycznymi kręgami mchu i białego/brązowego zarodnika grzyba. Dłoń ostrożnie je wyciąga.", "12,1,2"),
 ("Strząsanie śniegu z iglaków: Ołowiane zimowe niebo. Ciężka, gruba czapa puszystego, zlodowaciałego śniegu mocno wygina w łuk cieniutką, giętką gałązkę tui. Z boku uderza w nią kij, powodując eksplozję setek mikroskopijnych płatków białego śniegu.", "12,1,2"),
 ("Czyszczenie narzędzi i smarowanie: Wnętrze narzędziowni. Ostrze sekatora rozkręcone na dwie połowy. Na lśniącej, naostrzonej stalowej powierzchni spoczywa jedna, gęsta, żółta kropla oleju technicznego z aplikatora wężykowego.", "12,1,2"),
 ("Oczko wodne zimą (Przerębel): Zamarznięta na beton i pokryta szronem powierzchnia stawu. W pokrywie lodowej znajduje się ucięty krąg, w którym leży styropianowy, biały pływak w kształcie oponki, zapobiegający zamarznięciu i wpuszczający tlen do czarnej wody.", "12,1,2"),
 ("Planowanie siewów (Zeszyt w kratkę): Widok z góry na gruby zeszyt w kratkę otwarty na stole z drewna. Zapisany kaligraficznym pismem kalendarz, a obok odręcznie narysowany rzut grządek z wyraźnymi, kolorowymi polami oznaczającymi Marchew i symetrycznymi krzyżykami.", "1,2"),
 # --- Caloroczne Prace Specjalistyczne (Ciecie, Gleba, Nawozy) ---
 ("Cięcie prześwietlające jabłoni (Wilki): Wysoko w koronie starego drzewa, bezlistne, szare gałęzie na tle chłodnego nieba. Sekator obcina idealnie pionowy, długi, całkowicie gładki, brązowy, tegoroczny pęd rosnący prostopadle z grubszej gałęzi.", "2,3"),
 ("Jesienne cięcie malin (Teren ostry): Zbliżenie na krzak przy samej ziemi. Dwie grube, całkowicie brązowe, puste w środku i wyschnięte pędy maliny są twardo cięte dużym sekatorem idealnie równo z poziomem gleby. Pozostają tylko młode, zielone gałązki na przyszły rok.", "10,11"),
 ("Siew nawozów mineralnych na trawnik: W słońcu. Zielony siewnik obrotowy z zawrotną prędkością wyrzuca we wszystkich kierunkach małe, geometrycznie kuliste kuleczki w kolorze jasnoszarym, różowym i białym, ponad krótko skoszoną murawą.", "4,5,8,9"),
 ("Aeracja trawnika (Nakłuwanie): Zbliżenie na ciężki, zielony wał stalowy jeżdżący po trawniku. Na walcu przyspawane są pionowo długie na 10 cm, ostre, zardzewiałe stalowe szpikulce, które pod ciężarem maszyny zagłębiają się w ubitą ziemię, robiąc równomierne otwory z mchem.", "4,5,9,10"),
 ("Wertykulacja (Zrywanie filcu): Pionowe noże wertykulatora w brutalnej akcji. Stalowe tarcze przecinają ziemię i wyrzucają za siebie na wierzch trawę potężną ilość gęstej, brunatnej, zbutwiałej waty, odsłaniając zdrową ziemię pod spodem.", "4,9,10"),
 ("Cięcie winorośli (Płacząca łoza): Późna zima/Wczesna wiosna. Przecięta na ukos, bardzo gruba, brązowa, drewniejąca gałąź winogrona. Z precyzyjnie wykonanego cięcia spływa pojedyncza, ogromna, krystalicznie czysta kropla soku.", "2,3"),
 ("Rozsypywanie kompostu: Brudna od sadzy raca ogrodowa równomiernie rozsypuje łopatą kruche, smoliście czarne Złoto Ogrodnika po wierzchniej, suchej, beżowej skorupie piaskowej ziemi. Widoczne granulki i brak większych cząstek.", "3,4,5,9,10"),
 ("Formowanie żywopłotu: Bardzo długie, lśniące i ząbkowane ostrza spalinowych nożyc do żywopłotu. Ścinają pędy iglastej tui tak, że krawędź boczna i górna ściany stykają się tworząc absolutnie perfekcyjny, ostry niczym od linijki, kąt 90 stopni.", "5,6,7,8"),
 ("Pobieranie próbek gleby (Laska Egnera): Użycie profesjonalnego sprzętu. Długi, stalowy, półotwarty walec wbijany w poprzek stopy pionowo w ziemię. Po wyciągnięciu widać w rowku laski wyraźny profil przekroju gleby, od jasnej do czarnej.", "3,4,9,10"),
 ("Sprawdzanie odczynu pH (Kwasomierz Helliga): Na małej, białej ceramicznej płytce leży szczypta czarnej gleby zalana przezroczystym płynem. Po chwili płyn wokół ziemi zmienia kolor na rażąco krwisto-czerwony/pomarańczowy, obok leży żółta podziałka barwna.", "3,4,9,10"),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT_NAZWA,)).fetchone()
if not row:
    print("BLAD: kategoria '%s' nie istnieje - przerywam." % CAT_NAZWA)
else:
    cid = row['id']

    # usun stare 7 tematow (potwierdzone przez Tomasza mimo historii uzycia)
    stare = conn.execute("SELECT id, tekst FROM topics WHERE category_id=?", (cid,)).fetchall()
    print("Usuwam %d starych tematow:" % len(stare))
    for t in stare:
        print("  -", t['tekst'][:50])
    conn.execute("DELETE FROM topics WHERE category_id=?", (cid,))
    conn.commit()

    for tekst, mies in KALENDARZ:
        tid = add_topic(cid, tekst)
        c = get_connection(); c.execute("UPDATE topics SET miesiace=? WHERE id=?", (mies, tid)); c.commit(); c.close()

    c = get_connection()
    po = c.execute('SELECT COUNT(*) x FROM topics WHERE category_id=?', (cid,)).fetchone()['x']
    tc = c.execute("SELECT COUNT(*) x FROM categories").fetchone()['x']
    tt = c.execute("SELECT COUNT(*) x FROM topics").fetchone()['x']
    c.close()
    print("\nOK: kategoria '%s' (id=%s) ma teraz %d tematow (bylo 7, usuniete, dodane 50)." % (CAT_NAZWA, cid, po))
    print("RAZEM w bazie: %d kategorii, %d tematow." % (tc, tt))
conn.close()
