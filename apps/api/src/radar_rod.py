"""Proxy radaru opadow LibreWXR (api.librewxr.net) dla rodwozniki.pl — omija CORS, dodaje wymagany naglowek.
GET /radar/meta -> timeline (past+nowcast) jako JSON. GET /radar/kafel/... -> pojedynczy kafel PNG (cache 60s)."""
import json, time, urllib.request
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
router = APIRouter()
BAZA = "https://api.librewxr.net"
NAGL = {"User-Agent": "rodwozniki.pl radar (ROD Wozniki)", "Referer": "https://rodwozniki.pl/", "Origin": "https://rodwozniki.pl"}
_meta_cache = {"t": 0, "d": None}
def _pobierz(url, timeout=20):
    req = urllib.request.Request(url, headers=NAGL); return urllib.request.urlopen(req, timeout=timeout)
@router.get("/radar/meta")
def radar_meta():
    if time.time() - _meta_cache["t"] < 60 and _meta_cache["d"]:
        return JSONResponse(_meta_cache["d"], headers={"Cache-Control": "public, max-age=60"})
    try:
        d = json.loads(_pobierz(f"{BAZA}/public/weather-maps.json").read())
        r = d.get("radar", {})
        wynik = {"past": [{"time": f["time"], "path": f["path"]} for f in r.get("past", [])],
                 "nowcast": [{"time": f["time"], "path": f["path"]} for f in r.get("nowcast", [])]}
        _meta_cache.update(t=time.time(), d=wynik)
        return JSONResponse(wynik, headers={"Cache-Control": "public, max-age=60"})
    except Exception as e:
        return JSONResponse({"past": [], "nowcast": [], "blad": str(e)[:120]}, status_code=502)
@router.get("/radar/kafel/{ts}/{size}/{z}/{x}/{y}/{color}/{smooth}_{snow}.png")
def radar_kafel(ts: int, size: int, z: int, x: int, y: int, color: int, smooth: int, snow: int):
    url = f"{BAZA}/v2/radar/{ts}/{size}/{z}/{x}/{y}/{color}/{smooth}_{snow}.png"
    try:
        dane = _pobierz(url, timeout=15).read()
        return Response(content=dane, media_type="image/png", headers={"Cache-Control": "public, max-age=120"})
    except Exception:
        # przezroczysty 1x1 PNG gdy brak kafla
        pusty = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d4944415478da6360000000020001e221bc330000000049454e44ae426082")
        return Response(content=pusty, media_type="image/png", headers={"Cache-Control": "public, max-age=30"})
