"""Licznik odwiedzin rodwozniki.pl (dekret 03.09): GET /licznik.json — liczy unikalne wizyty (skrot IP+dzien), zwraca razem i dzis."""
import json, os, time, hashlib, datetime, threading
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
router = APIRouter(); PLIK = "/root/rod-ai-studio/data/licznik_rod.json"; LOCK = threading.Lock()
def _wczytaj():
    try: return json.load(open(PLIK, encoding="utf-8"))
    except Exception: return {"razem": 0, "dni": {}, "odslony": 0, "start": datetime.date.today().isoformat()}
@router.get("/licznik.json")
def licznik(req: Request):
    ip = req.headers.get("x-forwarded-for", "").split(",")[0].strip() or (req.client.host if req.client else "?")
    dzis = datetime.date.today().isoformat(); klucz = hashlib.sha256(f"{ip}|{dzis}|rod".encode()).hexdigest()[:16]
    with LOCK:
        d = _wczytaj(); d["odslony"] = d.get("odslony", 0) + 1
        dzien = d["dni"].setdefault(dzis, {"n": 0, "k": []})
        if klucz not in dzien["k"]:
            dzien["k"].append(klucz); dzien["n"] += 1; d["razem"] = d.get("razem", 0) + 1
        for k in list(d["dni"].keys()):  # skroty IP tylko z ostatnich 2 dni
            if k < (datetime.date.today() - datetime.timedelta(days=1)).isoformat(): d["dni"][k]["k"] = []
        tmp = PLIK + ".tmp"; json.dump(d, open(tmp, "w", encoding="utf-8")); os.replace(tmp, PLIK)
    return JSONResponse({"razem": d["razem"], "dzis": dzien["n"], "od": d.get("start")}, headers={"Cache-Control": "no-store"})
