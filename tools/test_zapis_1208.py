#!/usr/bin/env python3
"""Test zapisu sesji 12.08: artefakty istnieja i zawieraja kluczowe sekcje."""
from pathlib import Path
def main():
    wymagane = {
        "TELEPORT_fabryka.md": "MOLTY/OpenClaw",
        "wiedza/DECYZJE_OPENCLAW.md": "DEKRET E",
        "wiedza/PILOT_MOST_PLAN.md": "WYNIK PILOTA",
        "wiedza/GENEROWANIE_OBRAZU.md": "KOREKTA 12.08",
        "wiedza/PRZEGLAD_WARSZTATU_2026-08-12.md": "TORCH/SYNCNET",
        "scenariusze/kuny_scenariusz_final.md": "CZESC 6",
    }
    for p, fraza in wymagane.items():
        t = Path(p)
        assert t.exists() and t.stat().st_size > 200, f"BRAK/PUSTY: {p}"
        assert fraza in t.read_text(encoding="utf-8"), f"BRAK SEKCJI '{fraza}' w {p}"
    print("ZIELONY: zapis sesji kompletny")
if __name__ == "__main__":
    main()
