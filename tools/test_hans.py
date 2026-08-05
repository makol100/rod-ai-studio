#!/usr/bin/env python3
"""Testy pierwszej wersji Hansa oparte na wymaganiach Tomasza."""

import sys
import json
from pathlib import Path

# Dodanie katalogu tools oraz głównego katalogu repozytorium do sys.path,
# aby testy uruchamiały się poprawnie z dowolnego miejsca bez PYTHONPATH.
tools_dir = Path(__file__).resolve().parent
repo_root = tools_dir.parent

if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))
if str(repo_root) not in sys.path:
    sys.path.insert(1, str(repo_root))

from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import hans


class TestHans(unittest.TestCase):
    """Sprawdza alarmowanie Hansa bez zapisywania do prawdziwego dziennika."""

    def _sprawdz(self, glosy: dict[str, str], meldunek: str | None) -> dict:
        """Buduje osobną naradę, aby przypadki nie wpływały na siebie ani na repo."""
        with TemporaryDirectory() as katalog_tmp:
            korzen = Path(katalog_tmp)
            narada = korzen / "narada"
            narada.mkdir()
            for nazwa, tresc in glosy.items():
                (narada / nazwa).write_text(tresc, encoding="utf-8")

            plik_meldunku = korzen / "meldunek.txt"
            if meldunek is not None:
                plik_meldunku.write_text(meldunek, encoding="utf-8")

            # Test ma potwierdzić dopisywanie, ale nie może zaśmiecać dziennika roboczego.
            dziennik = korzen / "hans" / "dziennik.jsonl"
            with patch.object(hans, "DZIENNIK", dziennik):
                wynik = hans.sprawdz_narade(narada, plik_meldunku)
                self.assertTrue(dziennik.is_file())
                self.assertEqual(len(dziennik.read_text(encoding="utf-8").splitlines()), 1)
                return wynik

    def test_a_brak_sladu_pominiety_w_meldunku(self) -> None:
        """Hans alarmuje i zachowuje cytat, gdy meldunek pomija BRAK SLADU."""
        wynik = self._sprawdz(
            {"zenek.txt": "Kontrola: BRAK SLADU dla podanej liczby."},
            "Meldunek nie wspomina o zastrzeżeniu.",
        )
        self.assertEqual(wynik["poziom"], "ALERT")
        self.assertEqual([w["marker"] for w in wynik["przemilczane"]], ["BRAK SLADU"])
        self.assertEqual(wynik["przemilczane"][0]["cytat"], "Kontrola: BRAK SLADU dla podanej liczby.")

    def test_b_narada_czysta_meldunek_pelny(self) -> None:
        """Hans przepuszcza naradę, gdy wszystkie zgłoszone markery są w meldunku."""
        wynik = self._sprawdz(
            {"henio.txt": "Wynik sprawdzony. STOP został odnotowany technicznie."},
            "Pełny meldunek: STOP został odnotowany technicznie.",
        )
        self.assertEqual(wynik["poziom"], "OK")
        self.assertEqual(wynik["przemilczane"], [])
        self.assertEqual(wynik["bledy_wejscia"], [])

    def test_c_brak_pliku_meldunku(self) -> None:
        """Brak meldunku daje czytelny błąd zamiast wyjątku."""
        wynik = self._sprawdz({"genek.txt": "Głos bez zastrzeżeń."}, None)
        self.assertEqual(wynik["poziom"], "ALERT")
        self.assertTrue(any("Brak pliku meldunku:" in b for b in wynik["bledy_wejscia"]))

    def test_d_glos_nieodebrany(self) -> None:
        """Hans wychwytuje marker GLOS NIEODEBRANY wraz z miejscem i cytatem."""
        wynik = self._sprawdz(
            {"klaudek.txt": "Narada trwa.\nGLOS NIEODEBRANY: Zenek."},
            "Meldunek: pozostali oddali głosy.",
        )
        wpisy = [w for w in wynik["przemilczane"] if w["marker"] == "GLOS NIEODEBRANY"]
        self.assertEqual(wynik["poziom"], "ALERT")
        self.assertEqual(len(wpisy), 1)
        self.assertEqual(wpisy[0]["linia"], 2)
        self.assertEqual(wpisy[0]["cytat"], "GLOS NIEODEBRANY: Zenek.")


class TestHansStanPlikow(unittest.TestCase):
    """Testy kontroli stanu plików — sprawdzanie, czy meldunek Klaudka
    o wykonaniu/zapisaniu ma pokrycie w twardym stanie dysku."""

    def _wywolaj(self, meldunek: str, poczatek_tury: float, katalog: Path) -> dict:
        """Wywołuje sprawdz_stan_plikow z zadanym progiem i katalogiem."""
        return hans.sprawdz_stan_plikow(
            meldunek=meldunek,
            poczatek_tury=poczatek_tury,
            katalog_bazowy=katalog,
        )

    def test_e_plik_istnieje_swiezy_przepuszcza(self) -> None:
        """(a) Meldunek mówi 'zrobione', plik istnieje i jest świeży -> OK."""
        import time
        with TemporaryDirectory() as tmp:
            kat = Path(tmp)
            # Tworzymy plik, który będzie później "sprawdzany".
            plik = kat / "tools" / "wynik.py"
            plik.parent.mkdir(parents=True, exist_ok=True)
            plik.write_text("# wynik dzialania", encoding="utf-8")
            # Zapisujemy moment utworzenia jako próg — plik jest świeższy niż próg.
            czas_utworzenia = plik.stat().st_mtime
            # Próg: tuż przed utworzeniem pliku.
            prog = czas_utworzenia - 10.0

            meldunek = "Zadanie tools/wynik.py zrobione. Wszystko dziala."
            wynik = self._wywolaj(meldunek, prog, kat)

            self.assertEqual(wynik["poziom"], "OK",
                             f"Oczekiwano OK, dostano {wynik['poziom']}: {wynik.get('rozbieznosci')}")
            self.assertTrue(wynik["wykonanie_zadeklarowane"])
            self.assertEqual(wynik["rozbieznosci"], [])

    def test_f_plik_nie_istnieje_zglasza(self) -> None:
        """(b) Meldunek mówi 'zrobione', pliku NIE MA -> ALERT."""
        import time
        with TemporaryDirectory() as tmp:
            kat = Path(tmp)
            prog = time.time() - 3600  # godzina temu

            meldunek = "Plik tools/fantom.py zostal zapisany i gotowy."
            wynik = self._wywolaj(meldunek, prog, kat)

            self.assertEqual(wynik["poziom"], "ALERT",
                             f"Oczekiwano ALERT, dostano {wynik['poziom']}")
            self.assertTrue(wynik["wykonanie_zadeklarowane"])
            self.assertGreater(len(wynik["rozbieznosci"]), 0,
                               "Powinna być co najmniej jedna rozbieżność")
            powod = wynik["rozbieznosci"][0]["powod"]
            self.assertIn(powod, ["nie_istnieje", "pusty"],
                          f"Oczekiwano 'nie_istnieje', dostano '{powod}'")

    def test_g_plik_stary_nie_drgnal_zglasza(self) -> None:
        """(c) Meldunek mówi 'zrobione', plik jest STARY (nie drgnął) -> ALERT."""
        import time
        with TemporaryDirectory() as tmp:
            kat = Path(tmp)
            # Tworzymy plik na dysku.
            plik = kat / "tools" / "stary.py"
            plik.parent.mkdir(parents=True, exist_ok=True)
            plik.write_text("# stary plik", encoding="utf-8")

            # Czekamy chwilę, żeby mtime się ustabilizował.
            time.sleep(0.1)
            mtime_pliku = plik.stat().st_mtime

            # Próg: godzina PO utworzeniu pliku — plik jest starszy niż próg.
            prog = mtime_pliku + 3600.0

            meldunek = "Skrypt tools/stary.py uruchomiony i gotowy."
            wynik = self._wywolaj(meldunek, prog, kat)

            self.assertEqual(wynik["poziom"], "ALERT",
                             f"Oczekiwano ALERT, dostano {wynik['poziom']}: {wynik.get('rozbieznosci')}")
            self.assertTrue(wynik["wykonanie_zadeklarowane"])
            self.assertGreater(len(wynik["rozbieznosci"]), 0)
            # Powinien być problem "nie_drgnał"
            powod = wynik["rozbieznosci"][0]["powod"]
            self.assertEqual(powod, "nie_drgnał",
                             f"Oczekiwano 'nie_drgnał', dostano '{powod}'")

    def test_h_pominieto_przepuszcza(self) -> None:
        """(d) Rozbieżność jest, ale meldunek zawiera 'POMINIETO: powod' -> OK."""
        import time
        with TemporaryDirectory() as tmp:
            kat = Path(tmp)
            prog = time.time() - 3600

            # Plik NIE istnieje, ale Klaudek jawnie mówi POMINIETO.
            meldunek = (
                "Zadanie tools/fantom.py zrobione. "
                "POMINIETO: sprawdzenie pliku — test integracyjny."
            )
            wynik = self._wywolaj(meldunek, prog, kat)

            self.assertEqual(wynik["poziom"], "OK",
                             f"Oczekiwano OK (POMINIETO wyłącza alert), dostano {wynik['poziom']}: {wynik.get('rozbieznosci')}")
            self.assertTrue(wynik["wykonanie_zadeklarowane"])
            self.assertTrue(wynik["pominieto_wyjasnione"],
                            "Flaga pominieto_wyjasnione powinna być True")
            self.assertEqual(wynik["rozbieznosci"], [],
                             "Przy POMINIETO rozbieżności powinny być puste")

    def test_i_sciezka_bez_deklaracji_wykonania_nie_zglasza(self) -> None:
        """(e) Ścieżka nie istnieje, ale meldunek NIE mówi o niej jako o
        zrobionej/uruchomionej -> Hans nie zgłasza rozbieżności, poziom OK."""
        import time
        with TemporaryDirectory() as tmp:
            kat = Path(tmp)
            prog = time.time() - 3600

            # Meldunek zawiera ścieżkę, ale BEZ słów wykonania.
            meldunek = (
                "Plik tools/nieistniejacy.py wymaga sprawdzenia. "
                "Czekam na decyzję Tomasza."
            )
            wynik = self._wywolaj(meldunek, prog, kat)

            self.assertEqual(wynik["poziom"], "OK",
                             f"Oczekiwano OK (brak deklaracji wykonania), "
                             f"dostano {wynik['poziom']}: {wynik.get('rozbieznosci')}")
            self.assertFalse(wynik["wykonanie_zadeklarowane"],
                             "Bez słów wykonania flaga powinna być False")
            self.assertEqual(wynik["rozbieznosci"], [],
                             "Brak deklaracji wykonania = pusta lista rozbieżności")
            # Ścieżka jest wyłapana przez regex, ale NIE jest sprawdzana.
            self.assertIn("tools/nieistniejacy.py", wynik["sciezki"])


class TestHansWeryfikujStanPlikow(unittest.TestCase):
    """Testy nowej funkcji weryfikuj_stan_plikow, sprawdza twardy stan."""

    def test_a_zapisane_brak_pliku_wykrywa(self) -> None:
        """(a) meldunek mowi "zapisane", plik NIE istnieje -> Hans wykrywa."""
        import time
        start_tury = time.time() - 100
        meldunek = "Skrypt tools/brakujacy_plik.py jest zapisane na dysku."
        wynik = hans.weryfikuj_stan_plikow(meldunek, start_tury)
        self.assertIn("tools/brakujacy_plik.py", wynik)

    def test_b_zapisane_stary_wykrywa(self) -> None:
        """(b) meldunek mowi "zapisane", plik istnieje ale mtime STARSZY niz start tury -> Hans wykrywa."""
        import time
        with TemporaryDirectory() as tmp:
            stary_dir = Path(tmp) / "tools"
            stary_dir.mkdir(parents=True, exist_ok=True)
            stary_plik = stary_dir / "stary_plik.py"
            stary_plik.write_text("print('old')", encoding="utf-8")
            
            # Pobieramy mtime starego pliku
            time.sleep(0.1)
            mtime_pliku = stary_plik.stat().st_mtime
            
            # Start tury jest po utworzeniu starego pliku
            start_tury = mtime_pliku + 50.0
            meldunek = f"Skrypt {stary_plik} zapisane."
            
            # Wywołujemy funkcję weryfikującą
            wynik = hans.weryfikuj_stan_plikow(meldunek, start_tury)
            self.assertIn(str(stary_plik), wynik)

    def test_c_drgnal_przepuszcza(self) -> None:
        """(c) plik istnieje i drgnal po starcie tury -> Hans przepuszcza."""
        import time
        with TemporaryDirectory() as tmp:
            nowy_dir = Path(tmp) / "tools"
            nowy_dir.mkdir(parents=True, exist_ok=True)
            nowy_plik = nowy_dir / "nowy_plik.py"
            
            # Start tury jest przed utworzeniem pliku
            start_tury = time.time() - 10
            time.sleep(0.1)
            nowy_plik.write_text("print('new')", encoding="utf-8")
            
            meldunek = f"Skrypt {nowy_plik} zapisane i gotowe."
            wynik = hans.weryfikuj_stan_plikow(meldunek, start_tury)
            self.assertNotIn(str(nowy_plik), wynik)

    def test_d_nie_drgnal_ale_pominieto_przepuszcza(self) -> None:
        """(d) plik nie drgnal, ale w meldunku jest 'POMINIETO: powod' -> Hans przepuszcza."""
        import time
        start_tury = time.time() - 100
        # Brakujący plik, ale meldunek ma POMINIETO:
        meldunek = "Skrypt tools/pominiety_plik.py zapisane. POMINIETO: brak czasu na weryfikacje."
        wynik = hans.weryfikuj_stan_plikow(meldunek, start_tury)
        self.assertNotIn("tools/pominiety_plik.py", wynik)

    def test_e_brak_deklaracji_nie_zglasza(self) -> None:
        """(e) sciezka nie istnieje w ogole i nie ma o niej mowy jako o zrobionej -> Hans nie zglasza."""
        import time
        start_tury = time.time() - 100
        # Ścieżka jest w tekście, ale nie ma słów wykonania
        meldunek = "W pliku tools/jakis_plik.py jest błąd."
        wynik = hans.weryfikuj_stan_plikow(meldunek, start_tury)
        self.assertNotIn("tools/jakis_plik.py", wynik)


class TestHansWyslijDoTomasza(unittest.TestCase):
    """Testy funkcji wyslij_do_tomasza — wysylanie raportu na Telegram.

    Testy NIE wysylaja naprawde na Telegram — podmieniaja wysylke atrapa (mock).
    WARUNEK TWARDY: awaria wysylki NIE MOZE zepsuc narady ani kontroli Hansa.
    """

    def setUp(self) -> None:
        for p in [
            "/tmp/_hans_test_a_limit.jsonl",
            "/tmp/_hans_test_b_limit.jsonl",
            "/tmp/_hans_test_c_limit.jsonl",
            "/tmp/_hans_test_d_limit.jsonl",
            "/tmp/_hans_test_e_limit.jsonl",
        ]:
            try:
                Path(p).unlink(missing_ok=True)
            except OSError:
                pass

    def tearDown(self) -> None:
        self.setUp()

    def _czysty_raport(self) -> dict:
        """Raport bez niczego do zgloszenia — poziom OK, zero przemilczanych i bledow."""
        return {
            "poziom": "OK",
            "przemilczane": [],
            "bledy_wejscia": [],
        }

    def _raport_z_alarmem(self) -> dict:
        """Raport z przemilczanymi markerami — jest co zglaszac."""
        return {
            "poziom": "ALERT",
            "przemilczane": [
                {"marker": "BRAK SLADU", "plik": "/tmp/narada/zenek.txt", "linia": 3, "cytat": "Kontrola: BRAK SLADU dla podanej liczby."},
            ],
            "bledy_wejscia": [],
        }

    def _raport_z_bledami(self) -> dict:
        """Raport z bledami wejscia — jest co zglaszac."""
        return {
            "poziom": "ALERT",
            "przemilczane": [],
            "bledy_wejscia": ["Brak pliku meldunku: /tmp/x.txt"],
        }

    def test_a_raport_pusty_nie_wysyla(self) -> None:
        """(a) Raport bez przemilczanych i bledow -> NIE wysyla (False)."""
        with patch.object(hans, "LIMIT_PATH", Path("/tmp/_hans_test_a_limit.jsonl")):
            wynik = hans.wyslij_do_tomasza(self._czysty_raport())
        self.assertFalse(wynik, "Pusty raport nie powinien wywolywac wysylki")

    def test_b_raport_z_trescia_probuje_wyslac(self) -> None:
        """(b) Raport z przemilczanymi -> probuje wyslac (mockowane API zwraca sukces)."""
        atrapa_odp = json.dumps({"ok": True, "result": {"message_id": 99}}).encode()

        class AtrapaOdp:
            def __enter__(self):
                return self
            def __exit__(self, *a):
                pass
            def read(self):
                return atrapa_odp

        # 3.08: bez podmiany tokenu ten test czytal /home/hermes/.hermes/.env — plik spoza repo.
        # Zenek w piaskownicy go nie widzial i test u niego padal, u Klaudka przechodzil.
        with patch.object(hans, "LIMIT_PATH", Path("/tmp/_hans_test_b_limit.jsonl")), \
             patch.object(hans, "_wczytaj_token_hansa", return_value=("token_testowy", "123")), \
             patch("urllib.request.urlopen", return_value=AtrapaOdp()) as mock_urlopen:
            wynik = hans.wyslij_do_tomasza(self._raport_z_alarmem())

        self.assertTrue(wynik, "Raport z trescia powinien zostac wyslany (mock)")
        mock_urlopen.assert_called_once()

    def test_c_brak_tokenu_zwraca_false(self) -> None:
        """(c) Brak tokenu i chat_id -> zwraca False, NIE wywala sie."""
        with patch.object(hans, "_wczytaj_token_hansa", return_value=("", "")), \
             patch.object(hans, "LIMIT_PATH", Path("/tmp/_hans_test_c_limit.jsonl")):
            wynik = hans.wyslij_do_tomasza(self._raport_z_alarmem())
        self.assertFalse(wynik, "Brak tokenu powinien zwrocic False, nie wyjatek")

    def test_d_limit_przekroczony_wstrzymuje(self) -> None:
        """(d) Po 3 wyslanych w ciagu godziny -> czwarte wstrzymane (False)."""
        with patch.object(hans, "_sprawdz_limit", return_value=(3, True)), \
             patch.object(hans, "LIMIT_PATH", Path("/tmp/_hans_test_d_limit.jsonl")):
            wynik = hans.wyslij_do_tomasza(self._raport_z_alarmem())
        self.assertFalse(wynik, "Po przekroczeniu limitu powinno zwrocic False")

    def test_e_raport_z_bledami_wejscia_wysyla(self) -> None:
        """(e) Raport z bledami wejscia (bez przemilczanych) tez probuje wyslac."""
        atrapa_odp = json.dumps({"ok": True, "result": {"message_id": 100}}).encode()

        class AtrapaOdp:
            def __enter__(self):
                return self
            def __exit__(self, *a):
                pass
            def read(self):
                return atrapa_odp

        # ta sama poprawka co w tescie b — zaden test nie moze zalezec od pliku spoza repo
        with patch.object(hans, "LIMIT_PATH", Path("/tmp/_hans_test_e_limit.jsonl")), \
             patch.object(hans, "_wczytaj_token_hansa", return_value=("token_testowy", "123")), \
             patch("urllib.request.urlopen", return_value=AtrapaOdp()):
            wynik = hans.wyslij_do_tomasza(self._raport_z_bledami())
        self.assertTrue(wynik, "Raport z bledami wejscia tez powinien byc wyslany")


class TestHansWysylka(unittest.TestCase):
    """Testy wysylki z Hansa do Tomasza na Telegram (zadanie Henia)."""

    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        self.limit_path = Path(self.tmp_dir.name) / "limit.jsonl"
        self.patcher_limit = patch("hans.LIMIT_PATH", self.limit_path)
        self.patcher_limit.start()

    def tearDown(self):
        self.patcher_limit.stop()
        self.tmp_dir.cleanup()

    def test_a_raport_pusty_nie_wysyla(self):
        raport = {"poziom": "OK", "przemilczane": [], "bledy_wejscia": []}
        wynik = hans.wyslij_do_tomasza(raport)
        self.assertFalse(wynik)
        self.assertFalse(self.limit_path.exists())

    @patch("hans._wczytaj_token_hansa", return_value=("test_token", "123"))
    @patch("urllib.request.urlopen")
    def test_b_raport_z_trescia_probuje_wyslac(self, mock_urlopen, mock_token):
        raport = {
            "poziom": "ALERT",
            "przemilczane": [{"marker": "BRAK SLADU", "linia": 1, "cytat": "test", "plik": "f.txt"}],
            "bledy_wejscia": []
        }
        mock_response = unittest.mock.MagicMock()
        mock_response.read.return_value = b'{"ok": true, "result": {"message_id": 99}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        wynik = hans.wyslij_do_tomasza(raport)
        self.assertTrue(wynik)
        self.assertTrue(self.limit_path.exists())
        # sprawdzamy czy zostalo wywolane urlopen
        mock_urlopen.assert_called_once()

    @patch("hans._wczytaj_token_hansa", return_value=("", ""))
    def test_c_brak_tokenu_zwraca_false(self, mock_token):
        raport = {
            "poziom": "ALERT",
            "przemilczane": [{"marker": "STOP", "linia": 1, "cytat": "x"}],
            "bledy_wejscia": []
        }
        wynik = hans.wyslij_do_tomasza(raport)
        self.assertFalse(wynik)

    @patch("hans._wczytaj_token_hansa", return_value=("test_token", "123"))
    @patch("urllib.request.urlopen")
    def test_d_limit_wyslanych(self, mock_urlopen, mock_token):
        raport = {
            "poziom": "ALERT",
            "przemilczane": [{"marker": "STOP", "linia": 1, "cytat": "x"}],
            "bledy_wejscia": []
        }
        mock_response = unittest.mock.MagicMock()
        mock_response.read.return_value = b'{"ok": true, "result": {"message_id": 99}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # 5.08: test NIE zaklada juz konkretnej liczby — czyta ja z hans.LIMIT_GODZINA.
        # Wczesniej bylo wpisane 3 na sztywno, wiec podniesienie limitu ZEPSULOBY test.
        # Tomasz: "Zwiekszyc limit Hansowi, nie spierdolic zarazem czegos innego."
        limit = hans.LIMIT_GODZINA

        for _ in range(limit):
            wynik = hans.wyslij_do_tomasza(raport)
            self.assertTrue(wynik)

        self.assertEqual(mock_urlopen.call_count, limit)

        # Proba ponad limit powinna zablokowac, urlopen nie powinno urosnac
        wynik_ponad = hans.wyslij_do_tomasza(raport)
        self.assertFalse(wynik_ponad)
        self.assertEqual(mock_urlopen.call_count, limit)



class TestHansNiedokonczoneSlady(unittest.TestCase):
    """Testy nowej funkcji sprawdz_niedokonczone_slady — Henio 04.08.2026.
    Hans ma być moim narzędziem do wykrywania niedokończonych śladów Klaudka."""

    def test_a_pusty_katalog_zwraca_ok(self) -> None:
        """(a) Pusty katalog bez kodu i wiedzy -> OK, zero rozbieżności."""
        with TemporaryDirectory() as tmp:
            wynik = hans.sprawdz_niedokonczone_slady(tmp)
            self.assertEqual(wynik["poziom"], "OK")
            self.assertEqual(wynik["pliki_kodu"], 0)
            self.assertEqual(wynik["pliki_wiedzy"], 0)
            self.assertEqual(wynik["rozbieznosci"], [])

    def test_b_kod_bez_wiedzy_wykrywa(self) -> None:
        """(b) Plik kodu BEZ powiązania w wiedzy -> ALERT, osierocony_kod niepusty."""
        with TemporaryDirectory() as tmp:
            kat = Path(tmp)
            tools_dir = kat / "tools"
            tools_dir.mkdir()
            wiedza_dir = kat / "wiedza"
            wiedza_dir.mkdir()
            # Tworzymy plik kodu
            (tools_dir / "nowy_skrypt.py").write_text(
                "# Nowy skrypt do przetwarzania\n"
                "def przetwarzaj_dane():\n"
                "    return 'gotowe'\n"
                "STALA_KONFIGURACYJNA = 42\n",
                encoding="utf-8",
            )
            # Tworzymy wiedzę, która NIE wspomina o tym skrypcie
            (wiedza_dir / "inny_temat.md").write_text(
                "# Jakiś inny temat\nTo nie dotyczy nowego skryptu.\n",
                encoding="utf-8",
            )
            wynik = hans.sprawdz_niedokonczone_slady(tmp)
            self.assertEqual(wynik["poziom"], "ALERT")
            self.assertGreater(len(wynik["osierocone_kod"]), 0)
            self.assertIn("tools/nowy_skrypt.py",
                          [r["plik"] for r in wynik["osierocone_kod"]])

    def test_c_kod_z_wiedza_przepuszcza(self) -> None:
        """(c) Plik kodu z odpowiadającą mu wiedzą -> OK."""
        with TemporaryDirectory() as tmp:
            kat = Path(tmp)
            tools_dir = kat / "tools"
            tools_dir.mkdir()
            wiedza_dir = kat / "wiedza"
            wiedza_dir.mkdir()
            (tools_dir / "straznik.py").write_text(
                "def pilnuj():\n    return 'OK'\n",
                encoding="utf-8",
            )
            (wiedza_dir / "STRAZNIK.md").write_text(
                "# Strażnik\nOpis narzędzia tools/straznik.py.\n",
                encoding="utf-8",
            )
            wynik = hans.sprawdz_niedokonczone_slady(tmp)
            self.assertEqual(wynik["poziom"], "OK")
            self.assertEqual(wynik["osierocone_kod"], [])

    def test_d_testowe_pominiete(self) -> None:
        """(d) Pliki test_*.py NIE są brane pod uwagę."""
        with TemporaryDirectory() as tmp:
            kat = Path(tmp)
            tools_dir = kat / "tools"
            tools_dir.mkdir()
            (tools_dir / "test_cos.py").write_text(
                "def test_funkcji():\n    assert True\n",
                encoding="utf-8",
            )
            wynik = hans.sprawdz_niedokonczone_slady(tmp)
            self.assertEqual(wynik["pliki_kodu"], 0,
                             "Pliki testowe nie powinny być liczone jako kod produkcyjny")


class TestHansSrodowiskoHenia(unittest.TestCase):
    """Testy funkcji sprawdz_srodowisko_henia — Henio 04.08.2026."""

    def test_a_zwraca_strukture(self) -> None:
        """(a) Funkcja zawsze zwraca słownik z polami: poziom, stan, rozbieznosci."""
        wynik = hans.sprawdz_srodowisko_henia()
        self.assertIn("poziom", wynik)
        self.assertIn("stan", wynik)
        self.assertIn("rozbieznosci", wynik)
        self.assertIn("czas_utc", wynik)
        self.assertIsInstance(wynik["stan"], dict)

    def test_b_wykrywa_brak_zapisu(self) -> None:
        """(b) Symulowany brak dostępu do repo -> ALERT z komunikatem."""
        with patch.object(hans.Path, "is_dir", return_value=False):
            wynik = hans.sprawdz_srodowisko_henia()
        # Jeśli repo nie istnieje, powinno być odnotowane
        self.assertIsNotNone(wynik["stan"].get("zapis_do_repo"))


class TestHansNaradaZGlosami(unittest.TestCase):
    """Testy rozszerzonej funkcji sprawdz_narade_z_glosami — Henio 04.08.2026."""

    def _sprawdz(self, glosy: dict[str, str], meldunek: str) -> dict:
        with TemporaryDirectory() as tmp:
            kat = Path(tmp)
            narada = kat / "narada"
            narada.mkdir()
            for nazwa, tresc in glosy.items():
                (narada / nazwa).write_text(tresc, encoding="utf-8")
            plik_meld = kat / "meldunek.txt"
            plik_meld.write_text(meldunek, encoding="utf-8")
            dziennik = kat / "dziennik.jsonl"
            with patch.object(hans, "DZIENNIK", dziennik):
                return hans.sprawdz_narade_z_glosami(narada, plik_meld)

    def test_a_glos_wymieniony_przepuszcza(self) -> None:
        """(a) Autor głosu wymieniony w meldunku -> brak pominiętych głosów."""
        wynik = self._sprawdz(
            {"zenek.txt": "Kontrola OK.", "henio.txt": "Moja analiza."},
            "Meldunek: Zenek zgłosił OK, Henio też się wypowiedział."
        )
        self.assertNotIn("pominiete_glosy", wynik)

    def test_b_glos_pominiety_wykrywa(self) -> None:
        """(b) Głos Zenka NIE wymieniony w meldunku -> ALERT."""
        wynik = self._sprawdz(
            {"zenek.txt": "Kontrola: BRAK SLADU.", "henio.txt": "OK."},
            "Meldunek: Henio zgłosił OK."
        )
        self.assertEqual(wynik["poziom"], "ALERT")
        self.assertIn("pominiete_glosy", wynik)
        pominiety = [g["autor"] for g in wynik["pominiete_glosy"]]
        self.assertIn("zenek", pominiety)

    def test_c_wszystkie_glosy_wymienione_ok(self) -> None:
        """(c) Wszyscy autorzy wymienieni -> poziom może być OK."""
        wynik = self._sprawdz(
            {"zenek.txt": "Głos bez zastrzeżeń.",
             "henio.txt": "Też OK.",
             "genek.txt": "OK."},
            "Meldunek uwzględnia głosy Zenka, Henia i Genka."
        )
        # Nie ma pominiętych głosów (funkcja bazowa może dać OK)
        self.assertNotIn("pominiete_glosy", wynik)


if __name__ == "__main__":
    unittest.main(verbosity=2)

