# -*- coding: utf-8 -*-
from src.db.database import add_category, add_topic, get_connection

CAT = "Kwiaty w ROD"

KWIATY = [
 ('Tulipan: Pojedynczy, idealnie gładki, kielichowaty kwiat na długiej, grubej, jasnozielonej łodydze. Szerokie, mięsiste, szarozielone liście wyrastające u podstawy. Płatki owalne, zamykające się w owalną misę.', '4,5'),
 ('Krokus: Niewielki kwiat w kształcie wąskiego, pionowego pucharu wyrastający prosto z ziemi na minimalnej łodyżce. Sześć płatków, w centrum wyraźny, jaskrawopomarańczowy, postrzępiony słupek. Wąskie, trawiaste liście z białym paskiem wzdłuż środka.', '2,3'),
 ('Hiacynt: Bardzo gęsty, walcowaty (kolumnowy) kwiatostan na grubej, pionowej łodydze. Zbudowany z dziesiątek małych, gwiaździsto-dzwonkowatych kwiatuszków o sześciu wywiniętych na zewnątrz płatkach. Rynienkowate, błyszczące liście w kształcie łódek.', '3,4'),
 ('Narcyz (Żonkil): Złożony kwiat, którego centrum stanowi wysunięta, rurkowata lub pofalowana "trąbka" (przyłbica), otoczona idealnie sześcioma płaskimi, gwiaździstymi płatkami tła. Długie, płaskie, mieczowate liście u podstawy.', '3,4'),
 ('Szafirek: Miniaturowy kwiatostan przypominający odwróconą kiść winogron. Zbudowany z gęsto upakowanych, małych, pękatych, szafirowych kuleczek (zamkniętych dzwoneczków) na cienkiej łodyżce. Bardzo cienkie, trawiaste liście.', '4,5'),
 ('Pierwiosnek (Prymula): Rozeta z marszczonych, jajowatych liści o wyraźnym unerwieniu. W centrum wyrasta gęsty bukiet płaskich, pięciopłatkowych kwiatuszków, z których każdy ma w samym środku charakterystyczne, kontrastowe, żółte "oczko".', '3,4,5'),
 ('Sasanka: Kwiat w kształcie dużego, otwartego, sześciopłatkowego dzwonka. Cała roślina, w tym łodyga i pierzaste liście, pokryta jest wyraźnym, gęstym, srebrzystym, puszystym meszkiem (futerkiem). Duży żółty środek (pręciki).', '3,4'),
 ('Konwalia majowa: Cienka, wygięta w łuk łodyżka, z której jednostronnie zwisają malutkie, śnieżnobiałe, kuliste dzwoneczki z lekko wywiniętymi na zewnątrz ząbkami. Roślina otoczona dwoma, rzadziej trzema, szerokimi, eliptycznymi liśćmi.', '5'),
 ('Fiołek wonny: Maleńki, asymetryczny kwiatuszek na cienkiej szypułce. Posiada pięć płatków: dwa górne, dwa boczne i jeden dolny z charakterystyczną "ostrogą" z tyłu. Liście małe, nerkowate lub w kształcie idealnego serca z karbowanym brzegiem.', '3,4'),
 ('Irys (Kosaciec) bródkowy: Bardzo rzeźbiarski kwiat: trzy wewnętrzne płatki są uniesione pionowo i zwinięte do środka (tworząc kopułę), a trzy zewnętrzne opadają w dół. Na dolnych płatkach widać gęstą, puszystą "bródkę" przypominającą gąsienicę. Sztywne, szarozielone, płaskie jak szabla liście.', '5,6'),
 ('Piwonia (Peonia): Ogromny, ciężki, kulisty kwiat przypominający puszystą kapustę, zbudowany z setek cienkich, gładkich, jedwabistych płatków, często zachodzących na siebie falami. Liście ciemnozielone, dłoniasto-złożone, lekko błyszczące.', '5,6'),
 ('Lilia: Ogromny, lejkowato-gwiaździsty kwiat z sześcioma wyraźnymi, spiczastymi płatkami. Ze środka wystają bardzo długie, wygięte pręciki zakończone dużymi pylnikami w kształcie litery "T". Sztywna, wysoka łodyga gęsto oklejona wąskimi, spiczastymi liśćmi.', '6,7,8'),
 ('Róża rabatowa: Kwiat zbudowany w oparciu o geometryczną spiralę rozwijającą się ze stożkowego pąka. Płatki owalne, gładkie. Sztywna łodyga pokryta ostrymi kolcami. Liście ciemnozielone, ząbkowane na brzegach.', '6,7,8,9'),
 ('Róża pnąca: Morfologia kwiatu klasycznej róży (spirala płatków), ale wyrastająca kaskadowo w gęstych klastrach (wiechach) na bardzo długich, wiotkich i wspinających się pędach owijających się wokół pergoli.', '6,7,8,9'),
 ('Mieczyk (Gladiola): Bardzo długa, prosta jak strzała łodyga zakończona pionowym kłosem (wieżą) asymetrycznych, lejkowatych kwiatów z falbaniastymi brzegami, kwitnących od dołu do góry. Liście ściśle przylegające, pionowe, w kształcie mieczy.', '7,8,9'),
 ('Hortensja ogrodowa: Masywny, gęsty, idealnie kulisty kwiatostan (wielkości głowy), zbudowany z setek płaskich, czteropłatkowych kwiatuszków bez widocznego środka. Grube pędy i duże, szerokie, ząbkowane, owalne liście.', '7,8,9'),
 ('Dalia (Georginia): Kwiat o idealnej, często fraktalnej geometrii. W zależności od odmiany: rurkowate płatki ułożone w symetryczną kulę (pomponowa) lub płaskie, szerokie płatki promieniście rozchodzące się od środka (dekoracyjna). Brak widocznego słupka/pręcików w centrum u form pełnych.', '7,8,9,10'),
 ('Ostróżka: Bardzo wysoka, kolumnowa wieża gęsto obsypana kwiatami. Każdy pojedynczy kwiatuszek ma z tyłu długą, spiczastą "ostrogę" (ogonek) sterczącą poziomo. Liście dłoniaste, głęboko powycinane.', '6,7,8'),
 ('Łubin: Strzelisty, stożkowaty kwiatostan przypominający grubą, gęstą szczotkę, złożony z setek zamkniętych, kaskadowo ułożonych małych kwiatów motylkowych. Rozpoznawalne liście dłoniaste, przypominające parasolki lub rozłożone palce (złożone z 9-15 listków).', '6,7'),
 ('Malwa: Wysoka, gruba łodyga, do której niemal bezpośrednio (bez długich ogonków) przyklejone są duże, szeroko otwarte, lejkowate kwiaty o cienkich, pogniecionych jak bibuła płatkach. Duże, szorstkie, lekko klapowane liście.', '7,8'),
 ('Aster (Marcinek): Klasyczny kwiat typu stokrotka: mały, płaski, żółty środek w kształcie guzika (tarcza) otoczony jednym lub dwoma rzędami bardzo wielu wąskich, igiełkowatych płatków. Rosną w gęstych, półkolistych kępach.', '9,10'),
 ('Wrzos: Niska, gęsta krzewinka. Zamiast płaskich liści ma bardzo drobne, igiełkowate, zachodzące na siebie łuski na pędach. Kwiaty to mikroskopijne, wrzecionowate lub dzwonkowate kuleczki gęsto oblepiające górne części pędów w pionowych kłosach.', '8,9,10'),
 ('Chryzantema: U form pełnych tworzy geometryczną, wypukłą półkulę, gdzie płatki są wąskie, łódeczkowate (rynienkowate) i idealnie zachodzą na siebie, całkowicie zasłaniając środek. Liście "dębowe", głęboko klapowane.', '9,10,11'),
 ('Rozchodnik okazały: Ogromny, płaski jak talerz, baldachowaty kwiatostan zbudowany z tysięcy mikroskopijnych, pięcioramiennych gwiazdeczek. Łodygi grube, liście bardzo grube, mięsiste (sukulentowate), gładkie i owalne, magazynujące wodę.', '8,9,10'),
 ('Zimowit: Kształt dużego krokusa (wąski kielich rozszerzający się ku górze z sześcioma płatkami), wyrastający wprost z gołej ziemi całkowicie bez towarzystwa liści (kwiat sterczący z gleby pozbawiony jakiejkolwiek zieleni).', '9,10'),
 ('Jeżówka (Echinacea): Kwiat przypominający lotkę do badmintona: w centrum znajduje się ogromny, bardzo wypukły, kolczasty stożek (często brązowo-miedziany), od którego w dół zwisają sztywne, wąskie, długie płatki.', '7,8,9'),
 ('Rudbekia: Morfologia podobna do jeżówki, ale środek tworzy czarne, gładkie, wypukłe "oczko", otoczone promieniście rozłożonymi (poziomo), szerokimi żółtymi płatkami. Łodygi i liście pokryte szorstkim, drobnym włosem.', '7,8,9,10'),
 ('Zawilec japoński: Zwiewny, płaski kwiat z 5-7 bardzo cienkimi, asymetrycznie pofalowanymi płatkami. W środku znajduje się kulisty, zielono-żółty "guziczek" otoczony obwódką żółtych pręcików. Łodygi cienkie, mocno rozgałęzione.', '8,9,10'),
 ('Dzielżan: Unikalny środek kwiatu tworzący twardą, wypukłą, ciemną kulkę (jak mały pompon), od której w dół odchylają się szerokie, rudo-złote płatki, z których każdy ma na końcach wyraźne, faliste wcięcia (ząbki).', '7,8,9'),
 ('Krwawnik: Bardzo płaski, geometryczny baldach tworzący gęstą "platformę" złożoną z dziesiątek malutkich koszyczków kwiatowych. Charakterystyczne są liście: niezwykle drobno powycinane, gęste, przypominające miękkie pierze ptaka lub miniaturową paproć.', '6,7,8,9'),
 ('Floks (Płomyk) wiechowaty: Na szczycie prostej łodygi stożkowata, gęsta wiecha. Pojedynczy kwiatuszek składa się z pięciu okrągłych, płaskich płatków osadzonych na końcu krótkiej, cienkiej rurki. Wąskie liście osadzone symetrycznie naprzeciwko siebie.', '7,8,9'),
 ('Liatra kłosowa: Wysoki, puszysty kłos przypominający szczotkę do butelek. Kwiatuszki są drobne i "włochate". Unikalna cecha wizualna: kłos zawsze rozkwita od samego czubka w dół. Wąskie, trawiaste liście tworzą kępę.', '7,8'),
 ('Żurawka: Główny akcent wizualny to przyziemna rozeta liści. Liście duże, klapowane, często z mocno pofalowanym, karbowanym brzegiem, z siatką ciemniejszych nerwów na kolorowym (bordowym, karmelowym, żółtym) tle. Kwiaty to mikroskopijne, rzadkie dzwoneczki na cienkim, długim patyku.', '6,7,8'),
 ('Hosta (Funkia): Geometryczna rozeta ogromnych, rozłożystych liści w kształcie serca lub szerokiej kropli. Liście mają niezwykle wyraźne, głębokie żebrowanie (żyłkowanie) biegnące równolegle od nasady po czubek. Pędy kwiatowe wysokie i bezlistne.', '6,7,8'),
 ('Tawułka Arendsa: Kwiatostan przypomina miękką, rozmytą, puchatą chmurę lub pióropusz strusia, zwężający się ku górze, bez możliwości rozróżnienia pojedynczych płatków w masie. Liście złożone, podwójnie pierzaste, ciemnozielone.', '6,7,8'),
 ('Kocimiętka: Rozłożysta kępa gęstych, kanciastych pędów. Liście małe, trójkątne, matowe, o karbowanych brzegach i widocznej teksturze przypominającej zamsz. Kwiatostany to smukłe kłosy złożone z bardzo małych, rurkowato-dwuwargowych kwiatuszków.', '6,7,8,9'),
 ('Barwinek pospolity: Roślina płożąca ściśle po ziemi. Małe, owalne, bardzo błyszczące (jak woskowane), ciemnozielone skórzaste liście. Kwiat płaski, wiatraczkowaty, o pięciu skośnie ściętych na brzegach płatkach (zwykle fioletowo-niebieski).', '4,5'),
 ('Dąbrówka rozłogowa: Płoży się za pomocą rozłogów, tworząc dywan. Liście łopatkowate, ciemne, z połyskiem, ułożone naprzeciwlegle. Z dywanu wyrastają niskie, pionowe "wieże" kwiatostanowe z ułożonymi piętrowo małymi, wargowymi kwiatuszkami.', '5,6'),
 ('Lawenda wąskolistna: Sztywne, zdrewniałe u dołu pionowe pędy. Liście przypominają tępe igły - są wąskie, linearne i pokryte srebrzystym nalotem. Na szczycie pędu wąski kłosik pełen drobniutkich, rurkowatych, przylegających, fioletowych kwiatów.', '6,7,8'),
 ('Goździk brodaty (Kamienny): Płaski, baldaszkowaty i bardzo zbity kwiatostan tworzący wizualną tarczę. Pojedynczy kwiatuszek składa się z pięciu płatków o ostro powycinanych, ząbkowanych krawędziach. Często występuje mocno kontrastujące, koliste przebarwienie w środku ("oczko").', '6,7'),
 ('Aksamitka: Kwiat w kształcie gęstej, pomarszczonej kopułki, przypominającej gąbkę lub puszysty goździk, bez widocznego środka, o głębokiej teksturze przypominającej aksamit. Liście ciemnozielone, złożone z drobnych, ostro ząbkowanych wąskich listków (pierzastodzielne).', '6,7,8,9,10'),
 ('Nasturcja: Długie, wijące się łodygi. Bardzo charakterystyczne liście w kształcie idealnych, okrągłych, płaskich tarcz (jak parasolki), gdzie ogonki liściowe wyrastają bezpośrednio ze środka blaszki, a nie z krawędzi. Kwiat asymetryczny z długą, spiczastą ostrogą z tyłu.', '6,7,8,9,10'),
 ('Kosmos (Onętek): Kwiat miseczkowaty, lekko wklęsły, z ośmioma szerokimi płatkami ułożonymi płasko wokół okrągłego, żółtego środka. Płatki często mają pofalowane brzegi. Liście niezwykle zredukowane, przypominające nitki koperku (pierzaste), tworzące przejrzystą "mgiełkę".', '7,8,9,10'),
 ('Słonecznik ozdobny: Masywny, geometryczny kwiat tarczy na szczycie grubej łodygi. Środek stanowi olbrzymi, płaski, ciemny dysk, w którym rurkowate kwiatki układają się we fraktalną spiralę Fibonacciego, otoczony kołnierzem dużych, żółtych, wiotkich płatków języczkowatych. Duże sercowate liście.', '7,8,9'),
 ('Cynia: Kwiat osadzony na sztywnej, idealnie prostej, bezlistnej na górze łodydze. Zbudowany z licznych, sztywnych, spatulkowatych płatków ułożonych symetrycznie, dachówkowato w wyraźnych, koncentrycznych kręgach (jak ułożone warstwy sztywnego papieru).', '7,8,9,10'),
 ('Nagietek: Płaski koszyczek o jaskrawo-pomarańczowej barwie. Płatki (kwiaty języczkowate) liczne, wąskie, ułożone w kilku rzędach, o lekko ściętych, ząbkowanych wcięciach na samych czubkach. Liście długie, łopatkowate, lekko lepkie i owłosione.', '6,7,8,9,10'),
 ('Groszek pachnący: Roślina pnąca. Kwiat budowy motylkowej (jeden duży płatek "żagielek" sterczący do góry i boczne "skrzydełka"). Na cienkich łodygach, oprócz owalnych parzystych listków, występują wyraźne, cienkie, sprężynkowato zakręcone wąsy czepne oplatające tyczki.', '6,7,8'),
 ('Kobea pnąca: Pnącze tworzące ogromne (do 8 cm), dzwonkowate kwiaty w kształcie filiżanek, z mocno wywiniętymi na zewnątrz brzegami falistych płatków. Ze środka kielicha na kilkanaście centymetrów wystaje pęk długich, zawiniętych pręcików. Duży, zielony podstawek kielicha w kształcie gwiazdy.', '8,9,10'),
 ('Maciejka: Niepozorna budowa: mocno rozgałęzione, pokładające się, bardzo cienkie pędy. Kwiatuszki są zminiaturyzowane, płaskie, w kształcie czteropłatkowych krzyżyków, bladoróżowo-fioletowe (oświetlenie wieczorne lub księżycowe, kiedy się otwierają).', '6,7,8,9'),
 ('Facelia błękitna: Pędy grube i szczeciniasto owłosione. Charakterystyczny kształt kwiatostanu to "skrętka" - puszysty wałeczek zwinięty w ślimaka na końcu pędu, rozwijający się z biegiem kwitnienia. Kwiaty dzwonkowate, z bardzo długimi, wystającymi nitkami pręcików dającymi efekt puchu.', '6,7,8,9'),
]

conn = get_connection()
row = conn.execute("SELECT id FROM categories WHERE nazwa=?", (CAT,)).fetchone()
conn.close()
if row:
    print("UWAGA: kategoria '%s' juz istnieje (id=%s) - przerywam, zeby nie dublowac tematow." % (CAT, row['id']))
else:
    cid = add_category(CAT)
    for tekst, mies in KWIATY:
        tid = add_topic(cid, tekst)
        c = get_connection(); c.execute("UPDATE topics SET miesiace=? WHERE id=?", (mies, tid)); c.commit(); c.close()
    c = get_connection()
    n = c.execute("SELECT COUNT(*) x FROM topics WHERE category_id=?", (cid,)).fetchone()['x']
    tc = c.execute("SELECT COUNT(*) x FROM categories").fetchone()['x']
    tt = c.execute("SELECT COUNT(*) x FROM topics").fetchone()['x']
    c.close()
    print("OK dodano kategorie '%s' (id=%s) z %d tematami kwiatow." % (CAT, cid, n))
    print("RAZEM w bazie: %d kategorii, %d tematow." % (tc, tt))
