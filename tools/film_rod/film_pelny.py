# -*- coding: utf-8 -*-
"""
FILM ROD — pełny scenariusz. 5 bloków, ~6 min, 1920x1080.
Uruchomienie:  python3 film_pelny.py
"""
import sys
sys.path.insert(0, "/root/rod-ai-studio/tools/film_rod")
from buduj_film import buduj, panel_tlo, TMP

D = "/root/rod-ai-studio/data/rolka-prad"
M = f"{D}/mapy-16x9"
B = f"{D}/budowa"
F = f"{D}/filmy"
MUZYKA = "/root/rod-ai-studio/assets/music/Morning.mp3"

# --- plansze tekstowe (bez zdjęcia — sam panel) ---
def plansza(nazwa, tytul, linie):
    p = f"{TMP}/pl_{nazwa}.png"
    panel_tlo(tytul, linie, okno_w=0).save(p)
    return p

PL_KROKI = plansza("kroki", "Pięć rzeczy", [
    "1.  Wkopujesz kabel — od siatki do skrzynki",
    "2.  Elektryk + protokół",
    "3.  Karta z zarządu",
    "4.  Umowa z Tauronem — Ty, na siebie",
    "5.  Zarząd przepina, stary licznik odczytany",
])

sceny = [
    # ============ 1. ROBOTA (bez lektora) ============
    ("klip", f"{F}/VID-20260712-WA0000.mp4", None,
     "ROD im. Józefa Lompy", ["Przebudowa sieci elektrycznej"], 7.0),

    ("klip", f"{F}/VID-20260712-WA0004.mp4", None,
     "", ["Woźniki, Młyńska 40c"], 6.0),

    # ============ 2. PO CO ============
    ("foto", f"{D}/01-SPALONA-SKRZYNKA.jpg",
     "Ta skrzynka stała w naszym ogrodzie. Nie wytrzymała. "
     "Nie dlatego, że ktoś zrobił głupstwo. Dlatego, że nasza instalacja powstała w czasach, "
     "kiedy na działce paliła się jedna żarówka i grało radio. "
     "A dziś stoją lodówki, czajniki, kosiarki, pompy.",
     "Nie wytrzymała", ["Instalacja z czasów", "jednej żarówki."]),

    ("mapa", f"{M}/ETAP1-16x9.jpg",
     "Tak było od początku. Jedno przyłącze przy domu działkowca. Jeden licznik główny. "
     "Z niego trzy przewody — po jednym w każdą alejkę. I wszyscy na nich wiszą. "
     "Każda działka ma tylko podlicznik."),

    ("mapa", f"{M}/ETAP2-16x9.jpg",
     "W pewnym momencie przestało wyrabiać. Więc zrobiliśmy łatkę. "
     "Siedem działek najbliżej drogi wypięliśmy z domu i podpięliśmy do słupa przy drodze. "
     "Pomogło. Na chwilę. Bo czterdzieści cztery działki nadal wisiały na starym. "
     "Łatanie się skończyło."),

    # ============ 3. CO ZBUDOWALIŚMY ============
    ("mapa", f"{M}/MAPA-OGRODU-16x9.jpg",
     "To jest nasz ogród. Pięćdziesiąt jeden działek, trzy alejki. "
     "Postanowiliśmy skończyć z podlicznikami — każda działka ma dostać własny licznik "
     "i własną umowę. Ale do każdej musi dojść osobny kabel."),

    ("mapa", f"{M}/ZK1-16x9.jpg",
     "Zaczęliśmy od alejki południowej. Złącze ZK 1, osiemnaście liczników. "
     "Osobny kabel do każdej działki."),

    ("foto", f"{B}/1000098548.jpg",
     "To nie jest rysunek. To jest nasza alejka. Tyle kabli poszło w jeden rów. "
     "Nikt już nie wisi na wspólnym przewodzie.",
     "Osiemnaście kabli\nw jednym rowie", ["Każdy do innej działki."],
     "18", "osobnych kabli"),

    # --- SKAŁA (najlepsze ujęcie: WA0008) ---
    ("klip", f"{F}/VID-20260712-WA0008.mp4",
     "A kopanie proste nie było. Pod alejkami jest skała. Nie ziemia — skała.",
     "Pod alejką\njest skała", ["Nie ziemia. Skała."], 15),

    ("foto", f"{B}/1000098522.jpg",
     "Gdzie koparka nie dała rady, trzeba było rozkuwać młotem. Ręcznie. Metr po metrze.",
     "Młot udarowy", ["Metr po metrze."]),

    # --- LUDZIE ---
    ("foto", f"{B}/1000098552.jpg",
     "Koparka chodziła po nocach.", "Po nocach", []),

    ("foto", f"{B}/1000098532.jpg",
     "Kto miał łopatę, ten brał łopatę.", "Kto miał łopatę", ["ten brał łopatę."]),

    ("foto", f"{B}/1000098519.jpg",
     "Po pracy. W weekendy.", "Po pracy", ["W weekendy."]),

    ("foto", f"{B}/1000098520.jpg",
     "Robili to nasi ludzie. Za darmo. Nikt za to nie wziął ani złotówki.",
     "Nasi ludzie", ["Za darmo.", "Nikt nie wziął ani złotówki."]),

    # --- BEDNARKA ---
    ("foto", f"{B}/1000098539.jpg",
     "W tym rowie leży jeszcze coś. Obok kabli — stalowa taśma. Bednarka. "
     "To jest uziom. Wspólny, dla całej alejki. Ogród położył go raz, dla wszystkich. "
     "Nikt nie musi robić własnego uziomu u siebie. Zapamiętajcie — za chwilę wróci.",
     "Bednarka", ["Uziom. Wspólny.", "Dla całej alejki."]),

    ("mapa", f"{M}/ZK2-16x9.jpg",
     "Potem alejka środkowa. ZK 2, piętnaście liczników. Ten sam schemat."),

    ("klip", f"{F}/VID-20260712-WA0012.mp4",
     "I rów zniknął. Alejka wróciła do normy. Kabel został w ziemi.",
     "Rów znika", ["Kabel zostaje."], 30),

    ("foto", f"{D}/SZAFKA-gotowa.jpg",
     "A złącze stoi. Gotowe.", "Gotowe", []),

    # ============ 4. CO ZOSTAŁO ============
    ("mapa", f"{M}/ZK3-16x9.jpg",
     "Została alejka północna. Złącze już stoi, osiemnaście liczników czeka w środku. "
     "Ale kable nie są jeszcze wkopane. To następny etap."),

    # ============ 5. TERAZ TWOJA KOLEJ ============
    ("mapa", f"{M}/ETAP3-16x9.jpg",
     "I teraz najważniejsze. Ogród swoje zrobił. Złącze stoi. Kable leżą w ziemi. "
     "Licznik czeka w szafie — Twój, z numerem Twojej działki. "
     "Dalej nikt tego za Ciebie nie zrobi."),

    ("foto", f"{D}/KABEL-NA-PLOCIE.jpg",
     "Ten kabel wisi na Twojej siatce, od strony alejki. "
     "Ogród doprowadził go pod sam płot. Dalej to już Twoja łopata.",
     "Ten kabel\nwisi u Ciebie", ["Od strony alejki."]),

    ("mapa", PL_KROKI,
     "Żeby przejść na nowe, potrzebujesz pięciu rzeczy. "
     "Raz. Wkopujesz ten kabel u siebie — od siatki do skrzynki — i zabezpieczasz go. "
     "Dwa. Elektryk z uprawnieniami robi instalację i wystawia protokół: zabezpieczenia, "
     "rozdział PEN na PE i N, oraz uziom. I tu wraca ta bednarka z rowu — to do niej się podepniesz. "
     "Własnego uziomu robić nie musisz. "
     "Trzy. Karta z zarządu. "
     "Cztery. Idziesz do Taurona i podpisujesz umowę. Sam, na siebie. Nie ogród — Ty. "
     "Pięć. Elektryk zarządu przepina Cię na nowe, a stary licznik odczytujemy i rozliczamy."),

    ("foto", f"{D}/KABEL-NA-PLOCIE.jpg",
     "Tyle. Kabel wisi na Twojej siatce. Licznik czeka w szafie, z numerem Twojej działki. "
     "Brakuje jednego papieru — i Twojej łopaty. "
     "A kiedy cała alejka przejdzie na nowe, stary obwód zostanie zdjęty. Nie z zemsty. "
     "Po prostu nie ma po co wisieć — każdy będzie miał swój licznik.",
     "Teraz\nTwoja kolej", ["Brakuje jednego papieru.", "Twojego."]),
]

buduj(sceny, "/root/rod-ai-studio/data/rolka-prad/FILM-ROD-16x9.mp4", muzyka=MUZYKA)
