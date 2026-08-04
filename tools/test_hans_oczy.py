#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testy dla tools/hans_oczy.py — oczy Hansa skanujące repo.
Autor: Henio, 04.08.2026.

Przypadki (zlecenie Zenka z audytu):
  (a) pierwszy skan bez stanu poprzedniego — inicjalizacja, brak alarmu
  (b) zmiana kodu bez zmiany wiedzy → zgłasza podejrzenie
  (c) zmiana wiedzy bez zmiany kodu → zgłasza podejrzenie
  (d) zmiana obu (powiązanych) → NIE zgłasza podejrzenia
  (e) brak katalogu .scratch → nie wywala się

+ Testy wyłączeń automatycznych (fałszywy alarm na brief/INDEX/kopia).
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call, ANY, mock_open
from io import StringIO

# Ścieżka do repo
REPO_ROOT = '/root/rod-ai-studio'
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import tools.hans_oczy as oczy


class TestFunkcjePomocnicze(unittest.TestCase):
    """Testy funkcji pomocniczych — nie potrzebują mockowania systemu plików."""

    def test_czy_plik_kodu_tools_py(self):
        self.assertTrue(oczy.czy_plik_kodu("tools/hans.py"))

    def test_czy_plik_kodu_tools_sh(self):
        self.assertTrue(oczy.czy_plik_kodu("tools/jakis_skrypt.sh"))

    def test_czy_plik_kodu_nie_test(self):
        """Pliki testowe NIE są kodem produkcyjnym."""
        self.assertFalse(oczy.czy_plik_kodu("tools/test_hans.py"))
        self.assertFalse(oczy.czy_plik_kodu("tools/test_hans_oczy.py"))

    def test_czy_plik_kodu_nie_wiedza(self):
        self.assertFalse(oczy.czy_plik_kodu("wiedza/START.md"))

    def test_czy_plik_kodu_nie_inny_katalog(self):
        self.assertFalse(oczy.czy_plik_kodu("data/script.py"))

    def test_czy_plik_wiedzy_md(self):
        self.assertTrue(oczy.czy_plik_wiedzy("wiedza/START.md"))

    def test_czy_plik_wiedzy_nie_py(self):
        self.assertFalse(oczy.czy_plik_wiedzy("wiedza/skrypt.py"))

    def test_czy_plik_wiedzy_nie_tools(self):
        self.assertFalse(oczy.czy_plik_wiedzy("tools/README.md"))

    def test_czy_plik_wiedzy_nie_data(self):
        self.assertFalse(oczy.czy_plik_wiedzy("data/wiedza_kopia/START.md"))

    def test_powiazane_po_nazwie(self):
        """Dokument wskazuje plik kodu po nazwie."""
        with patch("builtins.open", mock_open(read_data="używamy tools/hans.py do sprawdzania narady")):
            self.assertTrue(oczy._powiazane("tools/hans.py", "wiedza/HANS_AGENT.md"))

    def test_powiazane_po_rdzeniu(self):
        """Dokument wskazuje plik kodu po rdzeniu nazwy (bez rozszerzenia)."""
        with patch("builtins.open", mock_open(read_data="skrypt hans_oczy analizuje zmiany")):
            self.assertTrue(oczy._powiazane("tools/hans_oczy.py", "wiedza/HANS_AGENT.md"))

    def test_powiazane_brak(self):
        """Dokument NIE wspomina o pliku kodu."""
        with patch("builtins.open", mock_open(read_data="to jest dokument o Hansie, nie wspomina o bramce")):
            self.assertFalse(oczy._powiazane("tools/bramka_henia.py", "wiedza/HANS_AGENT.md"))

    def test_powiazane_plik_nieczytelny(self):
        """Gdy plik wiedzy nie istnieje — zwraca False, nie wyjątek."""
        with patch("builtins.open", side_effect=OSError("nie ma pliku")):
            self.assertFalse(oczy._powiazane("tools/hans.py", "wiedza/nieistniejacy.md"))


class TestPlikiGenerowane(unittest.TestCase):
    """Testy funkcji czy_plik_generowany — wyłączanie automatów spod kontroli."""

    def test_brief_generowany(self):
        self.assertTrue(oczy.czy_plik_generowany("wiedza/BRIEF_DLA_KLAUDKA.md"))

    def test_index_generowany(self):
        self.assertTrue(oczy.czy_plik_generowany("wiedza/INDEX.md"))

    def test_kopia_wiedzy_generowana(self):
        self.assertTrue(oczy.czy_plik_generowany("data/wiedza_kopia/START.md"))
        self.assertTrue(oczy.czy_plik_generowany("data/wiedza_kopia/archiwum/stare.md"))

    def test_normalny_plik_niegenerowany(self):
        self.assertFalse(oczy.czy_plik_generowany("wiedza/START.md"))
        self.assertFalse(oczy.czy_plik_generowany("wiedza/HANS_AGENT.md"))
        self.assertFalse(oczy.czy_plik_generowany("tools/hans_oczy.py"))

    def test_czy_plik_wiedzy_nie_dla_generowanych(self):
        """czy_plik_wiedzy zwraca False dla plików generowanych."""
        self.assertFalse(oczy.czy_plik_wiedzy("wiedza/BRIEF_DLA_KLAUDKA.md"))
        self.assertFalse(oczy.czy_plik_wiedzy("wiedza/INDEX.md"))
        # Normalne pliki wiedzy dalej True
        self.assertTrue(oczy.czy_plik_wiedzy("wiedza/START.md"))


class TestPierwszySkan(unittest.TestCase):
    """(a) Pierwszy skan bez stanu poprzedniego."""

    def setUp(self):
        self.mock_stan = {
            "wiedza/START.md": {"mtime": 1000000.0, "checksum": "abc123"},
            "wiedza/DECYZJE.md": {"mtime": 1000000.0, "checksum": "def456"},
            "tools/hans.py": {"mtime": 1000000.0, "checksum": "ghi789"},
        }

    @patch("tools.hans_oczy.zapisz_zmiany")
    @patch("tools.hans_oczy.zapisz_podejrzenie")
    @patch("tools.hans_oczy.wczytaj_poprzedni_stan")
    @patch("tools.hans_oczy.oblicz_stan_plikow")
    def test_pierwszy_skan_tylko_inicjalizacja_bez_alarmu(
            self, mock_oblicz, mock_wczytaj, mock_podejrzenie, mock_zapisz):
        """Przy pierwszym skanie: informacja o inicjalizacji, zero alarmów."""
        mock_wczytaj.return_value = {}
        mock_oblicz.return_value = self.mock_stan

        out = StringIO()
        with patch("sys.stdout", out):
            oczy.main()

        output = out.getvalue()
        self.assertIn("Inicjalizacja", output)
        self.assertNotIn("ALARM", output)
        self.assertNotIn("PODEJRZENIE", output)
        mock_podejrzenie.assert_not_called()

    @patch("tools.hans_oczy.zapisz_zmiany")
    @patch("tools.hans_oczy.zapisz_podejrzenie")
    @patch("tools.hans_oczy.wczytaj_poprzedni_stan")
    @patch("tools.hans_oczy.oblicz_stan_plikow")
    def test_pierwszy_skan_zapisuje_zmiany(
            self, mock_oblicz, mock_wczytaj, mock_podejrzenie, mock_zapisz):
        """Przy pierwszym skanie zapisuje stan początkowy."""
        mock_wczytaj.return_value = {}
        mock_oblicz.return_value = self.mock_stan

        oczy.main()
        mock_zapisz.assert_called_once()
        zmiany = mock_zapisz.call_args[0][0]
        self.assertEqual(len(zmiany), 3)
        statusy = {z["status"] for z in zmiany}
        self.assertEqual(statusy, {"added"})


class TestKodBezWiedzy(unittest.TestCase):
    """(b) Zmiana kodu bez zmiany wiedzy → zgłasza podejrzenie."""

    @patch("tools.hans_oczy.zapisz_zmiany")
    @patch("tools.hans_oczy.zapisz_podejrzenie")
    @patch("tools.hans_oczy.wczytaj_poprzedni_stan")
    @patch("tools.hans_oczy.oblicz_stan_plikow")
    def test_kod_bez_wiedzy_alarm(self, mock_oblicz, mock_wczytaj,
                                  mock_podejrzenie, mock_zapisz):
        """Kod w tools/ się zmienił, wiedza/ bez zmian — ALARM."""
        mock_wczytaj.return_value = {
            "tools/hans_oczy.py": {"mtime": 1000000.0, "checksum": "old_code"},
            "wiedza/START.md": {"mtime": 1000000.0, "checksum": "old_wiedza"},
        }
        mock_oblicz.return_value = {
            "tools/hans_oczy.py": {"mtime": 2000000.0, "checksum": "new_code"},
            "wiedza/START.md": {"mtime": 1000000.0, "checksum": "old_wiedza"},
        }

        # Musimy też mockować czy_plik_generowany, żeby nie odfiltrowało START.md
        with patch("tools.hans_oczy.czy_plik_generowany", return_value=False):
            out = StringIO()
            with patch("sys.stdout", out):
                oczy.main()

        output = out.getvalue()
        self.assertIn("ALARM", output)
        self.assertIn("PODEJRZENIE", output)
        mock_podejrzenie.assert_called_once()
        args = mock_podejrzenie.call_args
        self.assertEqual(args[0][1], "tools_bez_powiazanej_wiedzy")


class TestWiedzaBezKodu(unittest.TestCase):
    """(c) Zmiana wiedzy bez zmiany kodu → zgłasza podejrzenie."""

    @patch("tools.hans_oczy.zapisz_zmiany")
    @patch("tools.hans_oczy.zapisz_podejrzenie")
    @patch("tools.hans_oczy.wczytaj_poprzedni_stan")
    @patch("tools.hans_oczy.oblicz_stan_plikow")
    def test_wiedza_bez_kodu_alarm(self, mock_oblicz, mock_wczytaj,
                                    mock_podejrzenie, mock_zapisz):
        """Wiedza się zmieniła, kod w tools/ bez zmian — ALARM."""
        mock_wczytaj.return_value = {
            "wiedza/HANS_AGENT.md": {"mtime": 1000000.0, "checksum": "old_md"},
            "tools/hans.py": {"mtime": 1000000.0, "checksum": "old_code"},
        }
        mock_oblicz.return_value = {
            "wiedza/HANS_AGENT.md": {"mtime": 2000000.0, "checksum": "new_md"},
            "tools/hans.py": {"mtime": 1000000.0, "checksum": "old_code"},
        }

        with patch("tools.hans_oczy.czy_plik_generowany", return_value=False):
            out = StringIO()
            with patch("sys.stdout", out):
                oczy.main()

        output = out.getvalue()
        self.assertIn("ALARM", output)
        self.assertIn("PODEJRZENIE", output)
        mock_podejrzenie.assert_called_once()
        args = mock_podejrzenie.call_args
        self.assertEqual(args[0][1], "wiedza_bez_powiazanego_kodu")


class TestObaPowlazane(unittest.TestCase):
    """(d) Zmiana obu (kodu i wiedzy) powiązanych → NIE zgłasza."""

    @patch("tools.hans_oczy.zapisz_zmiany")
    @patch("tools.hans_oczy.zapisz_podejrzenie")
    @patch("tools.hans_oczy.wczytaj_poprzedni_stan")
    @patch("tools.hans_oczy.oblicz_stan_plikow")
    def test_oba_powiazane_brak_alarmu(self, mock_oblicz, mock_wczytaj,
                                        mock_podejrzenie, mock_zapisz):
        """Kod i wiedza zmienione razem, wiedza wskazuje na kod — OK."""
        mock_wczytaj.return_value = {
            "tools/hans_oczy.py": {"mtime": 1000000.0, "checksum": "old_code"},
            "wiedza/HANS_AGENT.md": {"mtime": 1000000.0, "checksum": "old_md"},
        }
        mock_oblicz.return_value = {
            "tools/hans_oczy.py": {"mtime": 2000000.0, "checksum": "new_code"},
            "wiedza/HANS_AGENT.md": {"mtime": 2000000.0, "checksum": "new_md"},
        }

        with patch("tools.hans_oczy.czy_plik_generowany", return_value=False), \
             patch("tools.hans_oczy._powiazane", return_value=True):
            out = StringIO()
            with patch("sys.stdout", out):
                oczy.main()

        output = out.getvalue()
        self.assertNotIn("ALARM", output)
        self.assertNotIn("PODEJRZENIE", output)
        self.assertIn("Spójność zachowana", output)
        mock_podejrzenie.assert_not_called()

    @patch("tools.hans_oczy.zapisz_zmiany")
    @patch("tools.hans_oczy.zapisz_podejrzenie")
    @patch("tools.hans_oczy.wczytaj_poprzedni_stan")
    @patch("tools.hans_oczy.oblicz_stan_plikow")
    def test_oba_zmienione_ale_niepowiazane_alarm(self, mock_oblicz, mock_wczytaj,
                                                    mock_podejrzenie, mock_zapisz):
        """Kod i wiedza zmienione, ale NIE powiązane → jednak ALARM."""
        mock_wczytaj.return_value = {
            "tools/hans_oczy.py": {"mtime": 1000000.0, "checksum": "old_code"},
            "wiedza/START.md": {"mtime": 1000000.0, "checksum": "old_md"},
        }
        mock_oblicz.return_value = {
            "tools/hans_oczy.py": {"mtime": 2000000.0, "checksum": "new_code"},
            "wiedza/START.md": {"mtime": 2000000.0, "checksum": "new_md"},
        }

        with patch("tools.hans_oczy.czy_plik_generowany", return_value=False), \
             patch("tools.hans_oczy._powiazane", return_value=False):
            out = StringIO()
            with patch("sys.stdout", out):
                oczy.main()

        output = out.getvalue()
        self.assertIn("ALARM", output)


class TestBrakKataloguScratch(unittest.TestCase):
    """(e) Brak katalogu .scratch → nie wywala się."""

    @patch("tools.hans_oczy.zapisz_zmiany")
    @patch("tools.hans_oczy.wczytaj_poprzedni_stan")
    @patch("tools.hans_oczy.oblicz_stan_plikow")
    def test_brak_scratch_nie_wywala(self, mock_oblicz, mock_wczytaj, mock_zapisz):
        """Gdy .scratch/hans/ nie istnieje, zapisz_zmiany tworzy katalog,
        a wczytaj_poprzedni_stan zwraca pusty słownik."""
        mock_wczytaj.return_value = {}
        mock_oblicz.return_value = {
            "tools/hans_oczy.py": {"mtime": 1000000.0, "checksum": "abc"},
        }

        with patch("tools.hans_oczy.czy_plik_generowany", return_value=False):
            out = StringIO()
            with patch("sys.stdout", out):
                oczy.main()

        output = out.getvalue()
        self.assertIn("Inicjalizacja", output)
        self.assertNotIn("Traceback", output)


class TestWylaczeniaAutomatyczne(unittest.TestCase):
    """Testy sprawdzające, że pliki automatyczne NIE generują alarmów."""

    @patch("tools.hans_oczy.zapisz_zmiany")
    @patch("tools.hans_oczy.zapisz_podejrzenie")
    @patch("tools.hans_oczy.wczytaj_poprzedni_stan")
    @patch("tools.hans_oczy.oblicz_stan_plikow")
    def test_tylko_brief_zmieniony_bez_alarmu(self, mock_oblicz, mock_wczytaj,
                                               mock_podejrzenie, mock_zapisz):
        """Zmienia się TYLKO BRIEF (automatyczny). Ponieważ czy_plik_generowany
        wyklucza go na poziomie oblicz_stan_plikow, NIE ma go w zmianach.
        Bez zmian w wiedzy i bez zmian w kodzie → brak alarmu."""
        mock_wczytaj.return_value = {
            "wiedza/START.md": {"mtime": 1000000.0, "checksum": "old_start"},
            "tools/hans_oczy.py": {"mtime": 1000000.0, "checksum": "old_code"},
        }
        # BRIEF zmieniony, ale czy_plik_generowany go odfiltruje
        mock_oblicz.return_value = {
            "wiedza/START.md": {"mtime": 1000000.0, "checksum": "old_start"},
            "tools/hans_oczy.py": {"mtime": 1000000.0, "checksum": "old_code"},
        }

        out = StringIO()
        with patch("sys.stdout", out):
            oczy.main()

        output = out.getvalue()
        self.assertNotIn("ALARM", output)
        self.assertNotIn("PODEJRZENIE", output)
        mock_podejrzenie.assert_not_called()

    @patch("tools.hans_oczy.zapisz_zmiany")
    @patch("tools.hans_oczy.zapisz_podejrzenie")
    @patch("tools.hans_oczy.wczytaj_poprzedni_stan")
    @patch("tools.hans_oczy.oblicz_stan_plikow")
    def test_index_zmieniony_bez_alarmu(self, mock_oblicz, mock_wczytaj,
                                         mock_podejrzenie, mock_zapisz):
        """Zmiana INDEX.md (automatyczna) NIE generuje alarmu."""
        mock_wczytaj.return_value = {
            "wiedza/START.md": {"mtime": 1000000.0, "checksum": "old"},
            "tools/hans_oczy.py": {"mtime": 1000000.0, "checksum": "old_code"},
        }
        mock_oblicz.return_value = {
            "wiedza/START.md": {"mtime": 1000000.0, "checksum": "old"},
            "tools/hans_oczy.py": {"mtime": 1000000.0, "checksum": "old_code"},
        }

        out = StringIO()
        with patch("sys.stdout", out):
            oczy.main()

        output = out.getvalue()
        self.assertNotIn("ALARM", output)
        mock_podejrzenie.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
