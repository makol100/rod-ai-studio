"""Licznik odwiedzin rodwozniki.pl (dekret 03.09): bez cookies — unikalni goscie dziennie po skrocie (IP+przegladarka+dzien), ktory nie jest przechowywany jako IP."""
import json, os, time, hashlib, datetime, threading
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
router = APIRouter(); PLIK = "/root/rod-ai-studio/data/licznik_rod.json"; _lock = threading.Lock(); _widziani = {"dzien": "", "skroty": set()}
def _wczytaj():
    try: return json.load(open(PLIK, encoding="utf-8"))
    except Exception: return {"start": datetime.date.today().isoformat(), "odslony": 0, "goscie": 0, "dzis": {"data": "", "goscie": 0, "odslony": 0}}
@router.get("/licznik")
def licznik(req: Request, strona: str = "/"):
    dzis = datetime.date.today().isoformat(); ip = req.headers.get("x-forwarded-for", "").split(",")[0].strip() or (req.client.host if req.client else "")
    skrot = hashlib.sha256(f"{ip}|{req.headers.get('user-agent','')}|{dzis}".encode()).hexdigest()[:16]
    with _lock:
        d = _wczytaj()
        if d["dzis"]["data"] != dzis: d["dzis"] = {"data": dzis, "goscie": 0, "odslony": 0}
        if _widziani["dzien"] != dzis: _widziani["dzien"] = dzis; _widziani["skroty"] = set()
        nowy = skrot not in _widziani["skroty"]
        if nowy: _widziani["skroty"].add(skrot); d["goscie"] += 1; d["dzis"]["goscie"] += 1
        d["odslony"] += 1; d["dzis"]["odslony"] += 1
        tmp = PLIK + ".tmp"; json.dump(d, open(tmp, "w", encoding="utf-8")); os.replace(tmp, PLIK)
    return JSONResponse({"goscie": d["goscie"], "odslony": d["odslony"], "dzis": d["dzis"]["goscie"], "od": d["start"]}, headers={"Cache-Control": "no-store"})
