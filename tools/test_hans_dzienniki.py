#!/usr/bin/env python3
"""Testy addytywnej kontroli zaleglosci dziennikow Hansa."""

import os
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import hans  # noqa: E402


class TestHansZalegloscDziennikow(unittest.TestCase):
    def test_swiezy_dziennik_jest_ok(self) -> None:
        with TemporaryDirectory() as tmp:
            plik = Path(tmp) / "teleport.md"
            plik.write_text("przebieg", encoding="utf-8")
            os.utime(plik, (1_000_000, 1_000_000))
            wynik = hans.sprawdz_zaleglosc_dziennikow(
                (("test", plik),), prog_dni=1.0, teraz_epoch=1_000_000 + 86399
            )
        self.assertEqual(wynik["poziom"], "OK")
        self.assertFalse(wynik["dzienniki"][0]["zalegly"])

    def test_dziennik_starszy_niz_doba_alarmuje(self) -> None:
        with TemporaryDirectory() as tmp:
            plik = Path(tmp) / "teleport.md"
            plik.write_text("przebieg", encoding="utf-8")
            os.utime(plik, (1_000_000, 1_000_000))
            wynik = hans.sprawdz_zaleglosc_dziennikow(
                (("test", plik),), prog_dni=1.0, teraz_epoch=1_000_000 + 86401
            )
        self.assertEqual(wynik["poziom"], "ALERT")
        self.assertEqual(wynik["rozbieznosci"][0]["problem"], "przekroczony_prog")

    def test_brak_dziennika_alarmuje(self) -> None:
        with TemporaryDirectory() as tmp:
            brak = Path(tmp) / "nie_ma.md"
            wynik = hans.sprawdz_zaleglosc_dziennikow(
                (("test", brak),), teraz_epoch=1_000_000
            )
        self.assertEqual(wynik["poziom"], "ALERT")
        self.assertEqual(wynik["rozbieznosci"][0]["problem"], "plik_nie_istnieje")

    def test_dolaczenie_nie_zmienia_starego_poziomu(self) -> None:
        stary = {"poziom": "OK", "rozbieznosci": []}
        with patch("hans.sprawdz_zaleglosc_dziennikow", return_value={"poziom": "ALERT"}):
            nowy = hans._dolacz_kontrole_dziennikow(stary)
        self.assertEqual(nowy["poziom"], "OK")
        self.assertEqual(nowy["kontrola_dziennikow"]["poziom"], "ALERT")
        self.assertNotIn("kontrola_dziennikow", stary)

    def test_cli_spoza_repo_odnajduje_teleport_fabryki(self) -> None:
        wynik = subprocess.run(
            [sys.executable, str(Path(hans.__file__).resolve()), "--dzienniki"],
            cwd="/tmp",
            capture_output=True,
            text=True,
            check=True,
        )
        raport = json.loads(wynik.stdout)
        fabryka = next(d for d in raport["dzienniki"] if d["nazwa"] == "fabryka")
        self.assertTrue(fabryka["istnieje"])
        self.assertTrue(Path(fabryka["sciezka"]).is_absolute())


if __name__ == "__main__":
    unittest.main(verbosity=2)
