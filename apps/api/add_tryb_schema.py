# -*- coding: utf-8 -*-
from src.db.database import get_connection

conn = get_connection()

# 1) Schemat: dwie nowe kolumny, bezpieczne (sprawdzone ze nie istnieja)
cols_cat = [r['name'] for r in conn.execute('PRAGMA table_info(categories)').fetchall()]
cols_top = [r['name'] for r in conn.execute('PRAGMA table_info(topics)').fetchall()]

if 'tryb' not in cols_cat:
    conn.execute("ALTER TABLE categories ADD COLUMN tryb TEXT NOT NULL DEFAULT 'organizm'")
    print("Dodano kolumne categories.tryb (domyslnie 'organizm')")
else:
    print("categories.tryb juz istnieje - pomijam")

if 'tryb_override' not in cols_top:
    conn.execute("ALTER TABLE topics ADD COLUMN tryb_override TEXT DEFAULT NULL")
    print("Dodano kolumne topics.tryb_override (domyslnie NULL)")
else:
    print("topics.tryb_override juz istnieje - pomijam")

conn.commit()

# 2) Kategorie w trybie "sprzet" (bohater = narzedzie/urzadzenie/dokument)
SPRZET_KATEGORIE = [
    "Bezpieczeństwo i Infrastruktura",
    "Smart Ogród (Automatyka na Działce)",
    "Architektura Ogrodowa, Remonty i Majsterkowanie",
    "Prawo Działkowe i Życie Społeczności",
]
for nazwa in SPRZET_KATEGORIE:
    cur = conn.execute("UPDATE categories SET tryb='sprzet' WHERE nazwa=?", (nazwa,))
    if cur.rowcount == 0:
        print(f"UWAGA: nie znaleziono kategorii '{nazwa}' - zero wierszy zaktualizowanych")
    else:
        print(f"OK: '{nazwa}' -> tryb=sprzet")
conn.commit()

# 3) Wyjatki w "Kompostownik i gnojowki": 10 tematow infrastruktury -> tryb_override=sprzet
KOMPOST_SPRZET_PREFIXY = [
    "Kompostownik z palet:",
    "Termokompostownik:",
    "Kompostownik bębnowy",
    "Kompostownik z siatki zbrojeniowej:",
    "Pryzma kompostowa:",
    "Beczka na gnojówkę:",
    "Pojemnik Bokashi",
    "Stacja do przesiewania:",
    "Kompostownik murowany:",
    "Widły amerykańskie w kompoście:",
]
trafienia = 0
for prefix in KOMPOST_SPRZET_PREFIXY:
    cur = conn.execute(
        "UPDATE topics SET tryb_override='sprzet' WHERE tekst LIKE ?",
        (prefix + '%',)
    )
    if cur.rowcount == 0:
        print(f"UWAGA: nie znaleziono tematu zaczynajacego sie od '{prefix}'")
    else:
        trafienia += cur.rowcount
conn.commit()
print(f"Nadpisano tryb_override=sprzet dla {trafienia} tematow w Kompostowniku")

# 4) Podsumowanie koncowe
print()
print("=== PODSUMOWANIE ===")
for r in conn.execute("SELECT nazwa, tryb FROM categories ORDER BY id").fetchall():
    n = conn.execute("SELECT COUNT(*) c FROM topics WHERE category_id=(SELECT id FROM categories WHERE nazwa=?)", (r['nazwa'],)).fetchone()['c']
    print(f"  {r['nazwa']}: tryb={r['tryb']} ({n} tematow)")

n_override = conn.execute("SELECT COUNT(*) c FROM topics WHERE tryb_override IS NOT NULL").fetchone()['c']
print(f"\\nTematow z tryb_override ustawionym: {n_override}")

conn.close()
