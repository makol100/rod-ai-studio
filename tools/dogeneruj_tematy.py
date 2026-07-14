# -*- coding: utf-8 -*-
"""
DOGENEROWANIE TEMATÓW do 6 nowych kategorii — Bielik, partie po 10.
Format zgodny z bazą: "Nazwa (kontekst): opis wizualny kadru" ~200-300 znaków.
Miesiące: per PODGRUPA (cięcie jabłoni = wiosna, zbiór porzeczek = lato).
Dedup: nie wstawiamy tematu o tytule, który już istnieje w kategorii.
"""
import sqlite3
import re
import sys
import time

sys.path.insert(0, "/app")
from src.ai.ollama import generate

DB = "/root/rod-ai-studio/data/content.db"

PLAN = {
    "Owoce w ROD (krzewy i drzewka)": [
        ("cięcie i pielęgnacja drzewek oraz krzewów owocowych wczesną wiosną "
         "(jabłoń, grusza, porzeczka, agrest, malina, winorośl)", "2,3,4", 10),
        ("kwitnienie, zawiązywanie owoców, pielęgnacja w sezonie "
         "(truskawki, maliny, porzeczki, drzewka)", "5,6,7", 10),
        ("zbiory owoców miękkich i z drzew, dojrzewanie, ochrona przed ptakami", "7,8,9", 10),
        ("jesienne sadzenie krzewów i drzewek, przygotowanie do zimy", "9,10,11", 10),
    ],
    "Pogotowie: choroby i szkodniki": [
        ("szkodniki warzyw i owoców: mszyce, gąsienice, przędziorki, śmietka, "
         "bielinek — objawy na roślinie i zwalczanie", "5,6,7,8,9", 14),
        ("choroby grzybowe: mączniak, zaraza ziemniaczana, parch, szara pleśń, "
         "rdza — jak wyglądają na liściach i owocach", "5,6,7,8,9", 13),
        ("ślimaki, nornice, turkuć, pędraki — szkodniki glebowe i nocne", "4,5,6,7,8,9,10", 13),
    ],
    "Woda na działce": [
        ("podlewanie warzyw i krzewów: kiedy, ile, jak — rano czy wieczorem, "
         "pod korzeń, błędy podlewania", "5,6,7,8,9", 14),
        ("zbieranie i wykorzystanie deszczówki: beczki, zbiorniki, rynny", "4,5,6,7,8,9,10", 13),
        ("ściółkowanie i oszczędzanie wody: kora, słoma, trawa, agrowłóknina", "5,6,7,8", 13),
    ],
    "Zbiory i przetwory": [
        ("kiszenie i marynowanie: ogórki, kapusta, buraki — słoiki, zalewy, przyprawy", "7,8,9,10", 14),
        ("przetwory z owoców: dżemy, kompoty, soki, suszenie", "7,8,9,10", 13),
        ("przechowywanie plonów: piwnica, kopiec, suszenie ziół, mrożenie", "8,9,10,11", 13),
    ],
    "Działka zimą": [
        ("zabezpieczanie roślin przed mrozem: otulanie, kopczykowanie, "
         "agrowłóknina, bielenie pni", "11,12,1,2", 14),
        ("ptaki i zwierzęta zimą na działce: karmniki, poidła, schronienia", "11,12,1,2", 13),
        ("zimowe planowanie: przegląd nasion, plan zagonów, naprawa narzędzi, "
         "rozsady na parapecie", "12,1,2,3", 13),
    ],
    "Trawnik": [
        ("wiosenne budzenie trawnika: wertykulacja, aeracja, wapnowanie, "
         "pierwsze koszenie, dosiewanie", "3,4,5", 14),
        ("trawnik w sezonie: koszenie w upał, wysokość cięcia, mech, "
         "łysiny, chwasty w trawie", "5,6,7,8", 13),
        ("jesienna pielęgnacja trawnika: ostatnie koszenie, grabienie liści, "
         "nawożenie potasem", "9,10,11", 13),
    ],
}

PROMPT = """Tworzysz tematy rolek dla kanału ogrodniczego (działkowcy ROD).
Każdy temat = jedna linia w formacie:
NAZWA (kontekst): opis wizualny jednego kadru — co dokładnie widać na zdjęciu.

Opis ma być botanicznie i technicznie PRECYZYJNY (kolory, kształty, faktury),
bo na jego podstawie powstanie fotorealistyczny obraz. 150-280 znaków na temat.

PRZYKŁADY DOBREGO FORMATU (z bazy):
Pomidor Malinowy (Dojrzewanie): Ogromny, asymetryczny, żebrowany pomidor o barwie głębokiego, zgaszonego różu. Skórka matowa, na łodydze widoczne drobne włoski.
Usuwanie wilków (Pędy boczne): Zbliżenie na grubą, włochatą łodygę pomidora. W kącie między łodygą a liściem mały boczny pęd chwytany dwoma palcami.

ZASADY:
- Tylko prawdziwe rośliny, narzędzia i zjawiska. Zero wymyślonych odmian.
- Każdy temat INNY — inna roślina, inna czynność albo inny problem.
- Bez numeracji na początku linii. Jedna linia = jeden temat.
- Nie pisz nic poza tematami: żadnych wstępów, nagłówków ani podsumowań.

Wygeneruj dokładnie {n} tematów o: {zakres}
"""


def main():
    db = sqlite3.connect(DB)
    c = db.cursor()
    dodane_razem = 0

    for kat, podgrupy in PLAN.items():
        cid = c.execute("SELECT id FROM categories WHERE nazwa=?", (kat,)).fetchone()
        if not cid:
            print(f"!! brak kategorii {kat}, pomijam", flush=True)
            continue
        cid = cid[0]
        istniejace = {r[0].split(":")[0].strip().lower()
                      for r in c.execute("SELECT tekst FROM topics WHERE category_id=?", (cid,))}

        for zakres, miesiace, n in podgrupy:
            print(f"\n[{kat}] {zakres[:60]}... ({n} szt., mies. {miesiace})", flush=True)
            for proba in range(2):
                try:
                    odp = generate(PROMPT.format(n=n, zakres=zakres),
                                   temperature=0.8, max_tokens=2200)
                    break
                except Exception as e:
                    print(f"  blad ollama ({e}), ponawiam za 20 s", flush=True)
                    time.sleep(20)
            else:
                continue

            dodane = 0
            for linia in odp.split("\n"):
                linia = re.sub(r"^\s*[\d\-\*\.\)]+\s*", "", linia).strip()
                if ":" not in linia or len(linia) < 60 or len(linia) > 400:
                    continue
                tytul = linia.split(":")[0].strip().lower()
                if tytul in istniejace or len(tytul) < 4:
                    continue
                istniejace.add(tytul)
                c.execute("""INSERT INTO topics (category_id, tekst, uzyty_razy, aktywny, miesiace)
                             VALUES (?,?,0,1,?)""", (cid, linia, miesiace))
                dodane += 1
            db.commit()
            dodane_razem += dodane
            print(f"  +{dodane} tematow", flush=True)

    print(f"\n=== RAZEM DODANE: {dodane_razem} ===", flush=True)
    print("\n=== STAN KATEGORII ===", flush=True)
    for r in c.execute("""SELECT c2.nazwa, COUNT(t.id) FROM categories c2
                          LEFT JOIN topics t ON t.category_id=c2.id AND t.aktywny=1
                          WHERE c2.aktywna=1 GROUP BY c2.id ORDER BY c2.id"""):
        print(f"  {r[0]:<42} {r[1]:>3}", flush=True)


if __name__ == "__main__":
    main()
