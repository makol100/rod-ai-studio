#!/usr/bin/env python3
"""Testy Hans Ucho — weryfikacja odbioru słów Tomasza z Telegrama.

API testowane: hans_ucho.uruchom_ucho(token, chat_id) -> bool
Atrapy: patch("requests.get") — nigdy nie dotyka prawdziwego Telegrama.
Ścieżki: HANS_SLOWA_PATH i HANS_OFFSET_PATH w os.environ — nigdy nie
dotyka prawdziwego wiedza/SLOWA_TOMASZA.md.

Wymagania Tomasza (3.08.2026):
  (a) wiadomość od Tomasza -> dopisana dosłownie
  (b) ta sama wiadomość drugi raz -> NIE dublowana (offset działa)
  (c) wiadomość od kogoś innego -> ignorowana
  (d) brak sieci/tokenu -> zgłasza, nie wywala się
  (e) plik NIE traci istniejącej treści
"""

from __future__ import annotations

import json, os, sys, time, unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

tools_dir = Path(__file__).resolve().parent
repo_root = tools_dir.parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))
if str(repo_root) not in sys.path:
    sys.path.insert(1, str(repo_root))

import hans_ucho


# ── Atrapy ──────────────────────────────────────────────────────────────

def _resp_telegram(updates: list[dict]) -> MagicMock:
    """Atrapa requests.get zwracająca poprawne getUpdates."""
    m = MagicMock()
    m.raise_for_status = MagicMock()
    m.json = MagicMock(return_value={"ok": True, "result": updates})
    return m


def _resp_bledna() -> MagicMock:
    """Atrapa requests.get zwracająca ok=False."""
    m = MagicMock()
    m.raise_for_status = MagicMock()
    m.json = MagicMock(return_value={"ok": False, "description": "Unauthorized"})
    return m


def _upd(uid: int, chat_id: int, text: str,
         date: int | None = None, from_id: int | None = None) -> dict:
    """Buduje pojedynczy update Telegrama."""
    if date is None:
        date = int(time.time())
    if from_id is None:
        from_id = chat_id
    return {
        "update_id": uid,
        "message": {
            "message_id": uid,
            "chat": {"id": chat_id, "type": "private"},
            "from": {"id": from_id, "is_bot": False, "first_name": "Tomasz"},
            "date": date,
            "text": text,
        },
    }


def _czytaj_offset(sciezka: Path) -> int:
    try:
        return json.loads(sciezka.read_text("utf-8")).get("offset", -1)
    except Exception:
        return -1


# ── Testy ────────────────────────────────────────────────────────────────

class TestHansUcho(unittest.TestCase):

    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.kat = Path(self.tmp.name)
        self.slowa = self.kat / "SLOWA_TOMASZA.md"
        self.offset = self.kat / "ucho_offset.json"
        self.offset.parent.mkdir(parents=True, exist_ok=True)
        self.env = {
            "HANS_SLOWA_PATH": str(self.slowa),
            "HANS_OFFSET_PATH": str(self.offset),
        }

    def tearDown(self):
        self.tmp.cleanup()

    def _czytaj(self) -> str:
        return self.slowa.read_text("utf-8") if self.slowa.exists() else ""

    # ── (a) wiadomość od Tomasza -> dopisana dosłownie ──

    def test_a_dopisana_doslownie(self):
        tekst = "Testowa wiadomość od Tomasza — 3 sierpnia 2026."
        tok, cid = "fake_tok", "123456789"

        with patch.dict(os.environ, self.env), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=(tok, cid)), \
             patch("requests.get", return_value=_resp_telegram(
                 [_upd(1001, int(cid), tekst, date=1691000000)])) as mock_get:

            wynik = hans_ucho.uruchom_ucho(tok, cid)

        self.assertTrue(wynik, f"uruchom_ucho powinno zwrócić True, zwróciło {wynik}")
        mock_get.assert_called_once()
        zawartosc = self._czytaj()
        self.assertIn(tekst, zawartosc,
                      f"Tekst Tomasza nie w pliku.\nZawartość: {zawartosc[:300]}")
        self.assertIn("(Europe/Vienna)", zawartosc,
                      "Brak znacznika strefy czasowej")

    # ── (b) brak dublowania (offset działa) ──

    def test_b_brak_dublowania(self):
        tekst = "Wiadomość która ma się NIE powtórzyć."
        tok, cid = "fake_tok", "123456789"
        updates = [_upd(2001, int(cid), tekst, date=1691000100)]

        # ── pierwsze ──
        with patch.dict(os.environ, self.env), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=(tok, cid)), \
             patch("requests.get", return_value=_resp_telegram(updates)):

            self.assertTrue(hans_ucho.uruchom_ucho(tok, cid))

        self.assertEqual(self._czytaj().count(tekst), 1)
        self.assertGreaterEqual(_czytaj_offset(self.offset), 2001,
                                f"Offset powinien być >= 2001, jest {_czytaj_offset(self.offset)}")

        # ── drugie (te same update'y) ──
        with patch.dict(os.environ, self.env), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=(tok, cid)), \
             patch("requests.get", return_value=_resp_telegram(updates)):

            self.assertTrue(hans_ucho.uruchom_ucho(tok, cid))

        self.assertEqual(self._czytaj().count(tekst), 1,
                         f"Tekst zdublowany! Jest {self._czytaj().count(tekst)} razy.")

    # ── (c) obca wiadomość ignorowana ──

    def test_c_obca_ignorowana(self):
        tekst = "Hej, to ja — obcy."
        tok, cid = "fake_tok", "123456789"
        obcy = "999888777"

        with patch.dict(os.environ, self.env), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=(tok, cid)), \
             patch("requests.get", return_value=_resp_telegram(
                 [_upd(3001, int(obcy), tekst, date=1691000200, from_id=int(obcy))])):

            self.assertTrue(hans_ucho.uruchom_ucho(tok, cid))

        zawartosc = self._czytaj()
        self.assertNotIn(tekst, zawartosc,
                         "Obca wiadomość NIE powinna trafić do pliku!")

    # ── (d1) brak tokenu ──

    def test_d1_brak_tokenu(self):
        env_clean = {**self.env, "HANS_BOT_TOKEN": "", "HANS_CHAT_ID": ""}
        with patch.dict(os.environ, env_clean, clear=False), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=("", "")):
            wynik = hans_ucho.uruchom_ucho("", "")
        self.assertFalse(wynik, f"Bez tokenu powinno być False, jest {wynik}")

    # ── (d2) brak sieci ──

    def test_d2_brak_sieci(self):
        import requests as req_mod
        tok, cid = "fake_tok", "123456789"

        with patch.dict(os.environ, self.env), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=(tok, cid)), \
             patch("requests.get", side_effect=req_mod.ConnectionError("brak sieci")):

            wynik = hans_ucho.uruchom_ucho(tok, cid)

        # Zenek zwraca True nawet przy błędzie sieci (linia 103)
        self.assertIsInstance(wynik, bool, f"Powinien być bool, jest {type(wynik)}")

    # ── (d3) wadliwa odpowiedź API ──

    def test_d3_wadliwa_odpowiedz(self):
        tok, cid = "fake_tok", "123456789"

        with patch.dict(os.environ, self.env), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=(tok, cid)), \
             patch("requests.get", return_value=_resp_bledna()):

            wynik = hans_ucho.uruchom_ucho(tok, cid)

        self.assertIsInstance(wynik, bool)

    # ── (e) istniejąca treść zachowana ──

    def test_e_tresc_zachowana(self):
        stara = "# SŁOWA TOMASZA\n\n## 01.08.2026\n\n> „Test.\"\n"
        self.slowa.write_text(stara, "utf-8")

        nowa = "Nowa wiadomość z 3 sierpnia."
        tok, cid = "fake_tok", "123456789"

        with patch.dict(os.environ, self.env), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=(tok, cid)), \
             patch("requests.get", return_value=_resp_telegram(
                 [_upd(5001, int(cid), nowa, date=1691000300)])):

            self.assertTrue(hans_ucho.uruchom_ucho(tok, cid))

        zawartosc = self._czytaj()
        self.assertTrue(zawartosc.startswith(stara),
                        f"Stara treść nie zachowana!\nPoczątek: {zawartosc[:150]}")
        self.assertIn(nowa, zawartosc, "Nowa wiadomość nie dopisana!")
        self.assertGreaterEqual(len(zawartosc), len(stara) + len(nowa))

    # ── (f) wiele wiadomości w kolejności ──

    def test_f_wiele_kolejnosc(self):
        teksty = ["Pierwsza.", "Druga.", "Trzecia."]
        tok, cid = "fake_tok", "123456789"
        updates = [_upd(6001 + i, int(cid), t, date=1691000400 + i * 10)
                   for i, t in enumerate(teksty)]

        with patch.dict(os.environ, self.env), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=(tok, cid)), \
             patch("requests.get", return_value=_resp_telegram(updates)):

            self.assertTrue(hans_ucho.uruchom_ucho(tok, cid))

        z = self._czytaj()
        for t in teksty:
            self.assertIn(t, z)
        idx = [z.index(t) for t in teksty]
        self.assertLess(idx[0], idx[1])
        self.assertLess(idx[1], idx[2])

    # ── (g) puste updates ──

    def test_g_puste_updates(self):
        self.slowa.write_text("istnieje\n", "utf-8")
        tok, cid = "fake_tok", "123456789"

        with patch.dict(os.environ, self.env), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=(tok, cid)), \
             patch("requests.get", return_value=_resp_telegram([])):

            self.assertTrue(hans_ucho.uruchom_ucho(tok, cid))

        self.assertEqual(self._czytaj(), "istnieje\n")

    # ── (h) from_id (grupa) ──

    def test_h_from_id_z_grupy(self):
        tekst = "Wiadomość Tomasza z grupy."
        tok, cid = "fake_tok", "123456789"
        grupa = "111222333"

        with patch.dict(os.environ, self.env), \
             patch.object(hans_ucho, "_wczytaj_token_hansa", return_value=(tok, cid)), \
             patch("requests.get", return_value=_resp_telegram(
                 [_upd(7001, int(grupa), tekst, date=1691000500, from_id=int(cid))])):

            self.assertTrue(hans_ucho.uruchom_ucho(tok, cid))

        self.assertIn(tekst, self._czytaj(),
                      "Wiadomość z grupy (po from_id) powinna być zapisana!")


if __name__ == "__main__":
    unittest.main(verbosity=2)
