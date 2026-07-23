# -*- coding: utf-8 -*-
from src.db.database import add_topic, get_connection

CAT_NAZWA = "Najczestsze bledy"

BLEDY = [
 # --- Bledy Nawadniania i Wody ---
 ("Podlewanie liści w pełnym słońcu: Makrofotografia liścia pomidora z okrągłymi, wypalonymi soczewkami – jasnobrązowymi, suchymi plamami o wyraźnie wypalonych brzegach, powstałymi przez krople wody działające jak soczewki.", "5,6,7,8"),
 ("Przelanie doniczki (Zgnilizna): Zbliżenie na dno doniczki, w której widać brązowy, śluzowaty osad. Przez otwory drenażowe wylewa się mętnawa, śmierdząca woda, a korzenie wystające z otworów są czarne i całkowicie rozmoczone.", "4,5,6,7,8,9"),
 ("Zalewanie stożka wzrostu: Zbliżenie na środek młodej rozety sałaty. W zagłębieniu między listkami stoi mętna, zielona woda, z której wyłaniają się ślady gnicia – ciemne, śluzowate plamy na styku liści.", "4,5,6,7,8,9"),
 ("Nawadnianie lodowatą wodą: Krzew hortensji w pełnym słońcu. Liście są całkowicie zwiędnięte i oklapnięte mimo wilgotnej ziemi. Widoczny kontrast między gorącym powietrzem a kapiącą wężem lodowatą wodą bezpośrednio pod korzeń.", "6,7,8"),
 ("Brak ściółkowania (Parowanie): Pęknięta w geometryczny wzór, sucha, jasna i wyjałowiona skorupa gleby wokół łodygi rośliny. Ziemia jest tak przesuszona, że odsuwa się od łodygi, tworząc głęboką na kilka centymetrów szczelinę.", "6,7,8"),
 ("Zalanie nawożonej rośliny: Połączenie granulek nawozu mineralnego z nadmiarem wody. Granulki są częściowo rozpuszczone w żelową masę, która przypomina klej, oblepiła korzenie i powoduje ich poparzenie.", "4,5,6,7,8,9"),
 ("Nieregularne podlewanie (Pękanie owoców): Pomidor malinowy z potężną, głęboką, zbliznowaconą rysą w kształcie gwiazdy, która rozrywa skórkę owocu na pół. Rysa jest sucha, z ciemnym strupem.", "7,8,9"),
 ("Brak drenażu w donicy: Przekrój przez doniczkę ceramiczną. Widać, że dno jest całkowicie wypełnione ciężką, zbitą ziemią, bez warstwy keramzytu. Widoczna strefa błota na dnie.", None),
 ("Węże zaginające się na ostrych kantach: Zbliżenie na wąż ogrodowy, który pod wpływem ciśnienia strzela w miejscu silnego załamania o ostry róg betonowego obrzeża.", "4,5,6,7,8,9"),
 ("Podlewanie w czasie przymrozków: Pędy młodej sadzonki pokryte sztywną, przezroczystą warstwą lodu, która całkowicie rozerwała tkanki miękkie rośliny.", "4,5,9,10"),
 # --- Bledy Techniczne i Budowlane ---
 ("Brak izolacji pod legarami: Drewniany legar tarasowy leżący bezpośrednio na mokrym, betonowym podłożu. Drewno jest czarne, miękkie i całkowicie zjedzone przez grzyby.", None),
 ("Zbyt gęste nasadzenia (Brak cyrkulacji): Zbliżenie na krzak pomidora w tunelu. Krzaki są tak gęsto splątane, że nie widać głównej łodygi, a wewnątrz panuje całkowity mrok i widać szare, puszyste skupiska pleśni.", "5,6,7,8"),
 ("Zły kąt dachu altany: Dach płaski bez żadnego spadku, na którym stoi potężna, brudna kałuża wody o głębokości 5 cm, z której wyłaniają się mchy i gnijące liście.", None),
 ("Użycie wkrętów nieocynkowanych: Zardzewiałe, brązowe zacieki wyciekające spod łebka wkręta wkręconego w jasne drewno. Drewno wokół śruby jest poczerniałe i spróchniałe.", None),
 ("Zbyt wczesne zrywanie folii (Szok termiczny): Sadzonki w tunelu, które po nagłym otwarciu folii w południe padły w kilka minut. Wyraźny kontrast między ciepłym wnętrzem a zimnym podmuchem powietrza.", "3,4,5"),
 ("Brak zabezpieczenia końców rur: Otwarta rura drenażowa wbita w piach, która jest całkowicie zapchana błotem i korzeniami roślin, uniemożliwiając przepływ wody.", None),
 ("Zbyt małe fundamenty pod słupki: Słupek ogrodzeniowy, który stoi pod kątem 45 stopni, bo fundament z betonu jest wielkości pięści i został wyrwany z ziemi przez wiatr.", None),
 ("Malowanie na brudnym drewnie: Zbliżenie na płat farby, który odchodzi od drewna wraz z warstwą kurzu, odsłaniając surowe, szare i spróchniałe podłoże.", None),
 ("Zbyt płytko zakopane kable: Zbliżenie na ziemię po ulewnym deszczu – kabel elektryczny leży na wierzchu ziemi, całkowicie odsłonięty, bez żadnej osłony czy folii ostrzegawczej.", None),
 ("Montaż drzwi na sztywno: Drzwi altany, które się nie domykają, ponieważ zostały zamontowane bez żadnego luzu w ościeżnicy i pod wpływem wilgoci spuchły, rozrywając zawiasy.", None),
 # --- Bledy Uprawowe (Szkodniki, Nawozenie) ---
 ("Przeazotowanie pomidorów: Potężny, ciemnozielony krzak pomidora o nienaturalnie grubych, mięsistych łodygach, z których wyrastają pędy w kształcie zrośniętych wachlarzy, ale zero owoców.", "6,7,8"),
 ("Niedobór magnezu: Liść pomidora, na którym przestrzenie między żyłkami są jaskrawożółte, podczas gdy same żyłki pozostają ostro zielone.", "5,6,7,8"),
 ("Przykrycie agrowłókniną w czasie kwitnienia: Kwiaty pomidora/ogórka, które zaparzyły się pod włókniną i czernieją, nie zawiązując owocu.", "5,6,7"),
 ("Sadzenie pomidorów po ziemniakach: Krzak pomidora z wyraźnymi objawami zarazy, sadzony w ziemi, w której widać jeszcze stare, zgniłe bulwy ziemniaka.", "4,5"),
 ("Zbyt wysoki odczyn pH (Brak wapnowania): Krzak borówki z czerwonawymi brzegami liści, który przestał rosnąć, a w tle widać test kwasomierzem pokazujący jaskrawy błękit.", "4,5,6,7,8"),
 ("Pozostawienie chwastów z nasionami: Zbliżenie na przekwitnięty mniszek, który na wietrze rozsiewa tysiące nasion na idealnie wypielęgnowaną grządkę obok.", "4,5,6"),
 ("Zbyt głębokie sadzenie czosnku: Czosnek, który w ogóle nie wykiełkował, ponieważ w dołku głębokim na 20 cm zgnił, zanim przebił się przez zimną ziemię.", "9,10"),
 ("Sadzenie w nieodkwaszonym torfie: Siewka, która po wykiełkowaniu natychmiast wywinęła liścienie do dołu i zamarła.", "3,4,5"),
 ("Niewłaściwe cięcie drzewa (Sęk): Drzewo owocowe, u którego ucięto gałąź tak, że został 10-centymetrowy kikut, który teraz gnije i wciąga próchnicę do pnia.", "2,3,11,12"),
 ("Niezabezpieczenie ran po cięciu: Świeże cięcie konara, na którym widać płaczącą ranę i czarne zacieki po grzybach wchodzących w nieosłonięte drewno.", "2,3,11,12"),
 # --- Bledy w Zyciu Spolecznym i Prawne ---
 ("Samowola budowlana (Demolka): Altana, która przekracza wymiary i została oblepiona przez sąsiadów tabliczkami samowola. W tle widać notatkę z kontroli nadzoru ogrodowego.", None),
 ("Palenie śmieci (Plastik): Zbliżenie na czarny, oleisty dym unoszący się z beczki, w której widać nadtopione, kolorowe fragmenty butelek PET.", "3,4,10,11"),
 ("Zastawianie przejścia (Konflikt): Kadr na wąską alejkę zastawioną stertą gałęzi. Zza gałęzi wyłania się dłoń sąsiada w geście irytacji, wskazująca na regulamin.", None),
 ("Puszczanie psa luzem: Pies, który wybiega z działki i zadeptuje grządkę sąsiada – widać odciski psich łap na idealnie przygotowanej ziemi.", None),
 ("Hałas w godzinach ciszy: Budzik ustawiony na 14:00 stojący na włączonej, wibrującej głośno kosiarce.", "4,5,6,7,8,9,10"),
 ("Nielegalna wycinka: Świeży, biały pień po wyciętym, dorodnym drzewie, na którym widać brak tabliczki z pozwoleniem, a obok stojący, zdezorientowany sąsiad.", None),
 ("Zasypywanie rowu: Ktoś wrzuca gruz do rowu melioracyjnego, a sąsiad obok pokazuje na zalany ogród.", None),
 ("Monitoring skierowany na sąsiada: Kamera, która swoim czerwonym okiem wisi nad płotem i celuje prosto w okno sąsiedniej altany.", None),
 ("Prowadzenie działalności gospodarczej: Altana, przed którą stoi stos palet handlowych i widać ruch kurierów, co łamie regulamin ROD o charakterze wypoczynkowym.", None),
 ("Zrzut nieczystości do rowu: Woda z mycia auta, która spływa do rowu melioracyjnego, tworząc tęczowe plamy oleju na powierzchni wody.", "4,5,6,7,8,9"),
 # --- Bledy w Majsterkowaniu i Warsztacie ---
 ("Brak konserwacji narzędzi: Stos zardzewiałych, czarnych łopat, których drewniane trzonki są spróchniałe i pękają przy próbie wbicia w ziemię.", None),
 ("Przeciążenie przedłużacza: Cienki, zwinięty w kłębek przedłużacz domowy, który podpięto do kosiarki – kabel jest czarny, stopiony i dymi.", "4,5,6,7,8,9,10"),
 ("Narzędzia leżące w trawie: Sekator, który został zostawiony w mokrej trawie i teraz wygląda jak kawałek rudy żelaza – całkowicie zżarty przez rdzę.", None),
 ("Brak paznokci w pracy: Ręce działkowca, które po pieleniu wyglądają jak po kopalni – brud jest tak głęboki, że nie da się go domyć przez 3 dni.", "4,5,6,7,8,9"),
 ("Stosowanie nieodpowiedniego wkręta: Wkręt, który urwał łebek w połowie wkręcania w twarde drewno dębowe.", None),
 ("Brak drenażu w skrzynkach: Skrzynka balkonowa, z której po ulewie wycieka brązowa, gnijąca woda, ponieważ nie ma ani jednego otworu w dnie.", None),
 ("Złe podłączenie kabli w puszce: Puszka elektryczna, w której kable są skręcone na palce i zaizolowane zwykłą taśmą, która odkleja się od wilgoci.", None),
 ("Użycie młotka zamiast wkrętarki: Śruba, którą próbowano wbić młotkiem w drewno, co kompletnie zniszczyło strukturę deski i sam gwint.", None),
 ("Brak smarowania zawiasów: Stare zawiasy altany, które piszczą tak głośno, że słychać to przez całe ogrodzenie, i widać na nich opiłki metalu z tarcia.", None),
 ("Zły dobór tarczy do piły: Szarpane, wyrwane krawędzie deski, którą cięto tarczą do metalu lub tarczą o złym ułożeniu zębów.", None),
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

    for tekst, mies in BLEDY:
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
