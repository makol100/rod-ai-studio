#!/usr/bin/env python3
"""Ciasna petla sprzezenia dla bramki (faza 1 skilla /diagnosing-bugs).
Kazdy przypadek pochodzi z REALNEJ wpadki. Zielone = bramka gotowa. Czerwone = nie dotykac wiedzy."""
import json, subprocess, sys, os
REPO = "/root/rod-ai-studio"
przypadki = json.load(open(os.path.join(REPO, "testy/bramka/przypadki.json"), encoding="utf-8"))
ok = zle = 0
for p in przypadki:
    cmd = [sys.executable, "tools/bramka_henia.py", "--odpowiedz", p["odp"], "--zrodlo", p["zrodlo"]]
    if p["zadanie"]:
        cmd += ["--zadanie", p["zadanie"]]
    w = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=120)
    wynik = "BLOKADA" if "WERDYKT: BLOKADA" in w.stdout else ("PRZEPUSCIC" if "WERDYKT: PRZEPUSCIC" in w.stdout else "BLAD")
    zgoda = wynik == p["oczekiwane"]
    ok, zle = (ok + 1, zle) if zgoda else (ok, zle + 1)
    print(f"{'ZIELONE' if zgoda else 'CZERWONE'}  {p['nazwa'][:46]:48} oczekiwane={p['oczekiwane']:10} otrzymane={wynik}")
print(f"\nWYNIK: {ok}/{len(przypadki)} zielonych, {zle} czerwonych")
sys.exit(0 if zle == 0 else 1)
