#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buduje szkielet rolki o pradzie w ROD Wozniki: folder + scenes.txt + images/.
NIE generuje audio ani nie renderuje - to osobne kroki (weryfikacja po kazdym)."""
import shutil
from pathlib import Path

BAZA = Path("/root/rod-ai-studio/data")
SRC = BAZA / "rolka-prad" / "do-rolki"

# (nr, plik_obrazu, UJECIE, LEKTOR)
S = [
(1,"SKRZYNKA-1-pelna","Spalona skrzynka rozdzielcza w naszym ogrodzie, pelny kadr.",
 "To zdjęcie zrobiono w naszym ogrodzie. Stąd idzie prąd do Twojej działki."),
(2,"SKRZYNKA-2-najazd","Najazd: zweglona izolacja, stopiona kostka, sczernila miedz.",
 "To nie jest zwykłe zużycie. Tak wygląda coś, co się grzało. Latami."),
(3,"00-MAPA-OGRODU","Mapa ogrodu: 51 dzialek, trzy alejki, dom dzialkowca.",
 "Zacznijmy od czegoś, co może Cię zdziwić. Tauron nie zna Twojej działki. Nie ma Twojego nazwiska. Nie zna Twojego licznika. Dla Tauronu istnieje jeden klient: nasz ogród."),
(4,"ETAP1","Schemat: jedno przylacze do domu dzialkowca, licznik glowny, trzy obwody na alejki.",
 "Prąd przychodzi do jednego miejsca — do domu działkowca. Tam stoi licznik główny. I tam kończy się Tauron. Wszystko dalej — każdy kabel, każda skrzynka, każde złącze — jest nasze. Ogrodu. To nasz majątek. I nasz problem, kiedy się psuje."),
(5,"GRAF-faktura","Faktura z Tauronu: suma do zaplaty podzielona przez kilowatogodziny.",
 "Skoro ogród kupuje prąd, a Ty go zużywasz — kto ustala cenę? Nikt jej nie ustala. Ona się po prostu wylicza. Bierzemy fakturę od Tauronu. Dzielimy przez zużyte kilowatogodziny. I tyle wychodzi za jedną. Ani grosza więcej."),
(6,"00-MAPA-OGRODU","Mapa ogrodu - ogrod jako jeden odbiorca.",
 "Ogród nie sprzedaje prądu. Nie wolno mu. Na handel prądem trzeba koncesji — takiej, jaką ma zakład energetyczny. Ogród prąd kupuje i dzieli między działki. Złotówka w złotówkę."),
(7,"ETAP1","Schemat etapu 1: trzy obwody, dzialki kaskadowo na jednym przewodzie.",
 "Kiedyś wszystko szło z jednego miejsca. Trzy kable na trzy alejki. A wzdłuż alejki wisiały działki — jedna za drugą, na tym samym przewodzie. Ktoś włączył czajnik na końcu alejki? Sąsiadowi mrugało światło."),
(8,"ETAP2","Schemat etapu 2: drugie przylacze ze slupa, siedem dzialek przepietych.",
 "Więc zaczęliśmy łatać. Najpierw podzieliliśmy prąd na trzy strony. Potem postawiliśmy drugie przyłącze — na słupie przy drodze. Siedem działek najbliżej drogi przepięliśmy na nie."),
(9,"GRAF-faktura","Faktura - dwa osobne rachunki, dwie stawki.",
 "I stąd bierze się to, o co pytacie: dlaczego ogród ma dwa rachunki i dwie różne ceny za prąd? Bo każdy rachunek dzieli się osobno. Tak wychodzi z faktury."),
(10,"ETAP2","Schemat etapu 2 - latanie starej struktury.",
 "I to działało. Do czasu. Bo można dzielić prąd na trzy strony. Można wypiąć siedem działek na osobny słup. I nic to nie da. Bo żadna sztuczka nie odmłodzi starych kabli."),
(11,"SKRZYNKA-1-pelna","Spalona skrzynka - powrot do kadru z otwarcia.",
 "Instalacja jest stara. I po prostu do wymiany."),
(12,"ETAP3","Schemat etapu 3: trzy zlacza kablowe przy bramach.",
 "Podpisaliśmy umowy z Tauronem. Przy każdej alejce, przy bramie, stanęło złącze kablowe."),
(13,"ZK-z-tablica-ROD","Nowe zlacze kablowe, tablica ogrodu w tle.",
 "Te trzy szafy postawił Tauron. Za darmo. Nie z dobroci serca. Po burzliwych negocjacjach. Zarząd wywalczył to, za co ogród musiałby zapłacić z własnej kieszeni."),
(14,"ZK1-poludniowa","Zblizenie ZK 1: osiemnascie licznikow, dzialki 1 do 18.",
 "W środku każdej szafy są liczniki. Po jednym na każdą działkę. Osiemnaście, piętnaście, osiemnaście. Razem pięćdziesiąt jeden. Koniec z podlicznikami."),
(15,"BUD-2-wachlarz-kabli","Row w alejce, wachlarz kabli rozchodzacych sie do dzialek.",
 "I najważniejsze: do każdej działki idzie osobny kabel — prosto ze złącza. Nie wisisz już na wspólnym przewodzie z całą alejką. Masz swoją linię."),
(16,"BUD-3-wykop-alejka","Wykop biegnacy alejka w dal.",
 "Ale szafy to jedno. Kable trzeba było jeszcze wkopać."),
(17,"BUD-5-bednarka","Bednarka w rowie: skrecony krzyz zlacza uziemiajacego.",
 "Najpierw poszła bednarka — uziemienie. Zrobiliśmy o tym osobny film — obejrzyjcie, warto."),
(18,"BUD-7-kable-w-rowie","Kable ulozone na dnie rowu.",
 "Dopiero na to poszły kable."),
(19,"BUD-6-folia-zasypywanie","Czerwona folia ostrzegawcza nad kablami, dzialkowiec z lopatami.",
 "Każdy z nich został pomierzony. Każdy ma protokół."),
(20,"BUD-4-koparka-ludzie","Row w alejce, koparka i ludzie przy pracy.",
 "A teraz najważniejsze. Tych rowów nie kopała żadna firma."),
(21,"BUD-1-portret-kopacz","Dzialkowiec w rowie, patrzy prosto w obiektyw.",
 "Kopali je działkowcy. Nasi sąsiedzi. Po swoich godzinach. W błocie. Za darmo. Nikt nie wziął za to złotówki. Gdyby nie oni — ta inwestycja kosztowałaby dużo więcej."),
(22,"BUD-8-kabel-do-dzialki","Kabel z zapasem doprowadzony pod granice dzialki.",
 "Kabel dochodzi do Twojej działki. Pomierzony, z protokołem. Ogród swoje zrobił."),
(23,"ETAP3","Schemat etapu 3 - nowy uklad.",
 "Dobrze. To teraz najważniejsze pytanie. Co Ty z tego masz?"),
(24,"GRAF-faktura","Faktura z Tauronu - z Twoim nazwiskiem.",
 "Własną umowę z Tauronem. I własną fakturę — prosto od nich. Do tej pory rozliczenia robił zarząd. Sam. Ktoś chodził po ogrodzie, spisywał podliczniki, dzielił fakturę, liczył, kto ile. Teraz to znika. Płacisz Tauronowi za swoje. Kropka."),
(25,"ZK2-srodkowa","Zblizenie ZK 2 - osobny kabel do kazdej dzialki.",
 "Twój własny kabel. Stabilne napięcie — koniec z mruganiem światła, gdy sąsiad włączy czajnik. Porządne uziemienie."),
(26,"ZK-z-tablica-ROD","Nowe zlacze kablowe.",
 "I jeszcze jedno: całe przepięcie robi ogród. Za darmo. Przychodzi elektryk oddelegowany przez zarząd. Wypina Cię ze starego obwodu."),
(27,"STARY-LICZNIK","Stary licznik tarczowy w starej skrzynce.",
 "Demontuje stary licznik. Zabezpiecza stary obwód tak, żeby dalej działał — bo sąsiedzi, którzy jeszcze nie przeszli, muszą mieć prąd. I wpina nowy kabel w instalację Twojej działki. Za to nie płacisz ani grosza."),
(28,"ETAP3","Schemat etapu 3 - zlacza gotowe, liczniki czekaja.",
 "To już stoi. Kable są w ziemi. Liczniki czekają w szafach. Ale prąd jeszcze nie płynie. I tu wchodzisz Ty."),
(29,"SZAFKA-gotowa","Szafka na dzialce, przygotowana do przepiecia.",
 "Krok pierwszy. Uprawniony elektryk zabezpiecza przyłącz w Twojej szafce na działce — tak, żeby dało się wpiąć nowy kabel. Krok drugi. Wystawia Ci za to protokół."),
(30,"GRAF-kroki","Grafika: piec krokow, etykiety placisz i za darmo.",
 "Krok trzeci. Z protokołem idziesz do zarządu i dostajesz Kartę Techniczną. Krok czwarty. Z Kartą idziesz do Tauronu w Lublińcu i podpisujesz swoją umowę. Krok piąty. Przychodzi elektryk z zarządu i przepina Cię — za darmo. Płacisz tylko za jedno: za elektryka, który zabezpieczy Twoją szafkę. I za protokół. Tyle. Nic więcej."),
(31,"00-MAPA-OGRODU","Mapa calego ogrodu.",
 "Powiem wprost, bo się to należy: za to płacisz sam. Ta inwestycja pochłonęła wszystkie środki ogrodu. Do zera. Ale wszystko, co da się zrobić po naszej stronie — robimy za darmo."),
(32,"STARY-LICZNIK","Stary licznik - ostatnie wskazanie.",
 "Ostatnie wskazanie na starym liczniku to Twoje ostatnie rozliczenie z ogrodem. Płacisz, co zużyłeś — i umowa z ogrodem przestaje istnieć."),
(33,"KABEL-NA-PLOCIE","Kabel przewieszony przez plot - niedokonczone przylacze.",
 "Złącza czekają gotowe. Ale prąd popłynie dopiero wtedy, gdy każdy zrobi swoje. Kiedy alejka będzie gotowa, stary obwód zostanie wyłączony. Kto nie będzie miał wtedy umowy z Tauronem — w tym dniu prądu nie będzie miał. Nie zwlekaj. Przyjdź do zarządu — pogadamy."),
(34,"SKRZYNKA-1-pelna","Spalona skrzynka - ten sam kadr co na poczatku.",
 "Zaczęliśmy od tego zdjęcia."),
(35,"ZK-z-tablica-ROD","Ciecie: nowe zlacze, czyste, tablica ogrodu w tle.",
 "A skończymy na tym."),
(36,"GRAF-klamra","Grafika klamry: do teraz Tauron nie zna Twojej dzialki.",
 "Na początku powiedziałem, że Tauron nie zna Twojej działki. Że dla nich jesteś numerem w cudzej fakturze. Że między Tobą a prądem stoi ogród, podlicznik i ktoś, kto to wszystko przelicza."),
(37,"ZK1-poludniowa","Kabel ze zlacza prosto do jednej dzialki.",
 "Od teraz będzie inaczej. Będziesz miał swoją umowę. Swój licznik. Swój kabel. I swoją fakturę — z Twoim nazwiskiem."),
(38,"GRAF-klamra","Grafika klamry: od teraz Tauron zna Twoja dzialke.",
 "Od teraz Tauron będzie znał Twoją działkę."),
(39,"BUD-1-portret-kopacz","Dzialkowiec w rowie - ludzie, ktorzy to wykopali.",
 "Ogród zrobił, co mógł. Wywalczyliśmy złącza. Wykopaliśmy rowy własnymi rękami. Wydaliśmy wszystko, co mieliśmy. Została ostatnia rzecz. Twoja działka."),
(40,"ZK-z-tablica-ROD","Nowe zlacze i tablica ogrodu - zaproszenie.",
 "Przyjdź do zarządu. Pogadamy, wytłumaczymy, pomożemy. Zróbmy to razem."),
]

# --- numer rolki: pierwszy wolny ---
reels = BAZA / "reels"
istniejace = sorted(int(p.name) for p in reels.iterdir() if p.name.isdigit())
nr = max(istniejace) + 1
folder = reels / f"{nr:06d}"
folder.mkdir(parents=True, exist_ok=False)
(folder / "images").mkdir()

# --- scenes.txt ---
with open(folder / "scenes.txt", "w", encoding="utf-8") as f:
    for n, img, uj, lk in S:
        f.write(f"SCENA {n}:\nUJĘCIE: {uj}\nLEKTOR: {lk}\n\n")

# --- tryb + prompt (dla panelu / _odczytaj_tryb_jezykowy) ---
(folder / "tryb_jezykowy.txt").write_text("pl", encoding="utf-8")
(folder / "prompt_oryginalny.txt").write_text(
    "Rolka o przebudowie zasilania w ROD im. Jozefa Lompy w Wozniach - "
    "scenariusz i material wlasny (nie z pipeline'u AI). "
    "PUBLIKACJA: TYLKO strona ROD Wozniki, zadnych grup ogolnopolskich.",
    encoding="utf-8")

# --- obrazy ---
braki = []
for n, img, _, _ in S:
    src = SRC / f"{img}.jpg"
    if not src.is_file():
        braki.append(img); continue
    shutil.copy2(src, folder / "images" / f"{n:02d}.jpg")

print(f"ROLKA: {folder}")
print(f"scenes.txt: {len(S)} scen, {sum(len(x[3]) for x in S)} znakow lektora")
print(f"obrazy skopiowane: {len(list((folder/'images').glob('*.jpg')))} / {len(S)}")
if braki:
    print(f"!!! BRAKUJACE OBRAZY: {braki}")
else:
    print("BRAKOW: 0")

# --- weryfikacja: extract_narration musi zwrocic dokladnie 40 tekstow ---
import sys
sys.path.insert(0, "/root/rod-ai-studio/apps/api/src")
