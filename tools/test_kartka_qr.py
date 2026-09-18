#!/usr/bin/env python3
"""Test rozstrzygalny kartki QR (D-0419): kazdy format musi dekodowac sie do ADRES na 300/100/72 dpi,
arkusz A4 4/4 na 300 i 100 dpi; geometria bez wad (_wyniki.json). Wyjscie 0 = zielony."""
import json, sys
sys.path.insert(0, "/root/rod-ai-studio/tools")
import kartka_qr as K

wyn = K.test_dekod()
bledy = []
for k, v in wyn.items():
    if "odczyt" in v and not v["ok"]: bledy.append(f"{k}: odczyt '{v['odczyt']}'")
    if "odczytane" in v and v["odczytane"] != v["z"]: bledy.append(f"{k}: {v['odczytane']}/{v['z']}")  # Zenek: bez wyjatku dla 72 dpi
g = json.load(open(K.WY / "_wyniki.json"))
for k, v in g.items():
    if isinstance(v, dict) and v.get("wady"): bledy.append(f"{k}: wady geometrii {v['wady']}")
if g.get("arkusz_A4_4xA6", {}).get("kartek") != 4: bledy.append("arkusz: liczba kartek != 4")
if g["qr"]["adres"] != "https://rodwozniki.pl" or g["qr"]["moduly_z_cisza"] != 37: bledy.append(f"qr: {g['qr']}")
print("BLEDY:", bledy if bledy else "brak")
print("ZIELONY" if not bledy else "CZERWONY")
sys.exit(1 if bledy else 0)
