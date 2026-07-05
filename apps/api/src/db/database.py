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
