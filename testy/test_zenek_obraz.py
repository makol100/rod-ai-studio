import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("zenek_obraz", Path(__file__).parents[1] / "tools/zenek_obraz.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class KosztowaBramka(unittest.TestCase):
    def test_imagen_uzywa_predict(self):
        url, payload, cena = MOD.opis_requestu("imagen-4.0-fast", "test", "16:9", "1K")
        self.assertTrue(url.endswith(":predict"))
        self.assertEqual(cena, 0.02)
        self.assertEqual(payload["instances"][0]["prompt"], "test")

    def test_gemini_uzywa_generate_content(self):
        url, _, cena = MOD.opis_requestu("gemini-3.1-flash-image", "test", "16:9", "1K")
        self.assertTrue(url.endswith(":generateContent"))
        self.assertEqual(cena, 0.067)

    def test_pro_4k_ma_cene_024(self):
        _, _, cena = MOD.opis_requestu("nano-banana-pro", "test", "16:9", "4K")
        self.assertEqual(cena, 0.24)


if __name__ == "__main__":
    unittest.main()
