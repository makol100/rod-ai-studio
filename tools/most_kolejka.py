#!/usr/bin/env python3
"""most_kolejka.py — Klaudek: pokaz oczekujace zapytania Zenka/Henia w kolejce web."""
import os, glob
IN="/tmp/most_web/in"
qs=sorted(glob.glob(f"{IN}/*.query"))
if not qs: print("(kolejka pusta)")
for p in qs:
    qid=os.path.basename(p).replace(".query","")
    print(f"{qid}\t{open(p, encoding='utf-8').read().strip()}")
