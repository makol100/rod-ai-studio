import sqlite3
from pathlib import Path

DB_PATH = Path("/root/rod-ai-studio/data/content.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS reels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        prompt TEXT,
        title TEXT,
        text TEXT,
        hashtags TEXT,
        status TEXT DEFAULT 'generated'
    )
    """)
    conn.commit()
    conn.close()


def save_reel(prompt, title, text, hashtags):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO reels(prompt,title,text,hashtags)
        VALUES(?,?,?,?)
        """,
        (prompt, title, text, hashtags),
    )
    conn.commit()
    conn.close()


init_db()

def list_reels(limit=20):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, created_at, prompt, title, text, hashtags, status
        FROM reels
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ============================================================
#  KATEGORIE I TEMATY — rozszerzenie (losowanie wazone + seed)
# ============================================================
import random


def init_topics_db():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazwa TEXT UNIQUE NOT NULL,
        aktywna INTEGER DEFAULT 1
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        tekst TEXT NOT NULL,
        uzyty_razy INTEGER DEFAULT 0,
        ostatnio_uzyty TIMESTAMP,
        aktywny INTEGER DEFAULT 1,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    """)
    conn.commit()
    conn.close()
    _seed_if_empty()


def add_category(nazwa):
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO categories(nazwa) VALUES (?)", (nazwa.strip(),))
    conn.commit()
    row = conn.execute("SELECT id FROM categories WHERE nazwa = ?", (nazwa.strip(),)).fetchone()
    conn.close()
    return row["id"] if row else None


def list_categories():
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.id, c.nazwa, c.aktywna, COUNT(t.id) AS liczba_tematow
        FROM categories c
        LEFT JOIN topics t ON t.category_id = c.id AND t.aktywny = 1
        GROUP BY c.id ORDER BY c.id
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_topic(category_id, tekst):
    conn = get_connection()
    cur = conn.execute("INSERT INTO topics(category_id, tekst) VALUES (?, ?)", (category_id, tekst.strip()))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def list_topics(category_id=None):
    conn = get_connection()
    if category_id is not None:
        rows = conn.execute("""
            SELECT t.id, t.tekst, t.uzyty_razy, t.ostatnio_uzyty, t.aktywny,
                   c.nazwa AS kategoria, t.category_id
            FROM topics t JOIN categories c ON c.id = t.category_id
            WHERE t.category_id = ? ORDER BY t.uzyty_razy ASC, t.id ASC
        """, (category_id,)).fetchall()
    else:
        rows = conn.execute("""
            SELECT t.id, t.tekst, t.uzyty_razy, t.ostatnio_uzyty, t.aktywny,
                   c.nazwa AS kategoria, t.category_id
            FROM topics t JOIN categories c ON c.id = t.category_id
            ORDER BY c.id, t.uzyty_razy ASC
        """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def random_topic():
    from datetime import datetime
    m = datetime.now().month
    okno = {((m - 1 + k) % 12) + 1 for k in range(3)}
    conn = get_connection()
    rows = conn.execute('SELECT t.id, t.tekst, t.uzyty_razy, t.miesiace, c.nazwa AS kategoria FROM topics t JOIN categories c ON c.id = t.category_id WHERE t.aktywny = 1 AND c.aktywna = 1').fetchall()
    kand = [r for r in rows if r['miesiace'] is None or (okno & {int(x) for x in r['miesiace'].split(',')})]
    if not kand:
        conn.close()
        return None
    wagi = [1.0 / (r['uzyty_razy'] + 1) for r in kand]
    wybor = random.choices(kand, weights=wagi, k=1)[0]
    conn.execute('UPDATE topics SET uzyty_razy = uzyty_razy + 1, ostatnio_uzyty = CURRENT_TIMESTAMP WHERE id = ?', (wybor['id'],))
    conn.commit()
    conn.close()
    return {'id': wybor['id'], 'kategoria': wybor['kategoria'], 'temat': wybor['tekst'], 'uzyty_razy': wybor['uzyty_razy'] + 1}


SEED = {
    "Co siac / co robic teraz": [
        "Co wysiac na dzialce w lipcu", "Prace na dzialce w tym miesiacu",
        "Druga tura wysiewu - co jeszcze zdazysz", "Kiedy sadzic czosnek na zime",
        "Co siac we wrzesniu na jesienne zbiory", "Przygotowanie grzadek po zimie",
        "Ostatni moment na wysiew rozsady"],
    "Sprawdzone triki dzialkowca": [
        "Jak podlewac pomidory, zeby nie chorowaly", "Fasola na siatce - wiecej plonu z metra",
        "Ogorki na siatce zamiast na ziemi", "Kawa i fusy w ogrodzie - tak czy nie",
        "Pasynkowanie pomidorow krok po kroku", "Kompost - co wrzucac, czego unikac",
        "Nagietek i aksamitka miedzy warzywami"],
    "Najczestsze bledy": [
        "3 bledy przy sadzeniu rozsady", "Dlaczego twoja rzodkiewka gorzknieje",
        "Najczestszy blad przy podlewaniu w upaly", "Nie rob tego z kompostem",
        "Bledy przy przechowywaniu plonow", "Dlaczego pomidory pekaja"],
    "Zycie ROD Wozniki": [
        "Kwitnace dzialki wiosna na naszym ROD", "Zbiory na dzialkach ROD Wozniki",
        "Przygotowanie dzialki do zimy", "Konkurs na najpiekniejsza dzialke",
        "Prace porzadkowe na ogrodzie"],
    "Ciekawostki i mity": [
        "Czarna rzodkiew - zapomniane warzywo naszych babc",
        "Czy wiedziales, ze nagietek chroni warzywa?",
        "Zapomniane warzywa: pasternak, topinambur",
        "Najwiekszy mit o podlewaniu wieczorem", "5 ciekawostek o komposcie"],
}


def _seed_if_empty():
    conn = get_connection()
    n = conn.execute("SELECT COUNT(*) AS c FROM categories").fetchone()["c"]
    conn.close()
    if n > 0:
        return
    for nazwa, tematy in SEED.items():
        cid = add_category(nazwa)
        for t in tematy:
            add_topic(cid, t)
    print(f"[seed] {len(SEED)} kategorii, {sum(len(v) for v in SEED.values())} tematow")


init_topics_db()


# ============================================================
#  ZAPOWIEDZI SERII — calkowicie osobna sciezka od kategorii/tematow.
#  Uzywane dla rolek typu "odcinek serii / coming soon", ktore NIE
#  pochodza z bazy tematow ogrodniczych. Ustalone w Dyskusji 08.07.2026.
# ============================================================

def init_zapowiedzi_db():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS zapowiedzi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tresc_promptu TEXT NOT NULL,
        utworzony TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        uzyty_razy INTEGER DEFAULT 0,
        ostatnio_uzyty TIMESTAMP,
        reel_id TEXT
    )
    """)
    conn.commit()
    conn.close()


def add_zapowiedz(tresc_promptu, reel_id=None, uzyty_razy=0, ostatnio_uzyty=None):
    """reel_id/uzyty_razy/ostatnio_uzyty opcjonalne - do retroaktywnego
    dopisania juz uzytych zapowiedzi (odcinek 1, 2) z pelna historia."""
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO zapowiedzi(tresc_promptu, reel_id, uzyty_razy, ostatnio_uzyty) VALUES (?, ?, ?, ?)",
        (tresc_promptu.strip(), reel_id, uzyty_razy, ostatnio_uzyty)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def list_zapowiedzi():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, tresc_promptu, utworzony, uzyty_razy, ostatnio_uzyty, reel_id FROM zapowiedzi ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def oznacz_uzyta_zapowiedz(zapowiedz_id, reel_id):
    conn = get_connection()
    conn.execute(
        "UPDATE zapowiedzi SET uzyty_razy = uzyty_razy + 1, ostatnio_uzyty = CURRENT_TIMESTAMP, reel_id = ? WHERE id = ?",
        (reel_id, zapowiedz_id)
    )
    conn.commit()
    conn.close()


init_zapowiedzi_db()
