"""Proxy radaru+prognozy opadow IMGW SCENE/MERGE (INCA, do ~6h w przod) dla rodwozniki.pl.
GET /radar/meta -> timeline klatek (teraz-60min .. +6h) jako JSON. GET /radar/kafel/... -> kafel PNG (cache).
Zrodlo: IMGW-PIB (tilesources-*.imgw.pl). Uwaga: konczowka IMGW to z/y/x (nie z/x/y)."""
import json, time, re, urllib.request, datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
router = APIRouter()
XML_URL = "https://tilesources-a.imgw.pl/vector/tms.xml"
NAGL = {"User-Agent": "rodwozniki.pl radar (ROD Wozniki)", "Referer": "https://rodwozniki.pl/"}
_cache = {"t": 0, "d": None}
def _get(url, timeout=20):
    return urllib.request.urlopen(urllib.request.Request(url, headers=NAGL), timeout=timeout)
@router.get("/radar/meta")
def radar_meta():
    if time.time() - _cache["t"] < 120 and _cache["d"]:
        return JSONResponse(_cache["d"], headers={"Cache-Control": "public, max-age=120"})
    try:
        xml = _get(XML_URL).read().decode("utf-8", "ignore")
        klatki = sorted(set(re.findall(r"inca-prec-0-sfc-(\d{8}T\d{6}Z)", xml)))
        teraz = datetime.datetime.now(datetime.timezone.utc)
        past, nowcast = [], []
        for ts in klatki:
            dt = datetime.datetime.strptime(ts, "%Y%m%dT%H%M%SZ").replace(tzinfo=datetime.timezone.utc)
            delta_h = (dt - teraz).total_seconds() / 3600
            if -1.05 <= delta_h <= 0.05:   # ostatnia godzina (przeszlosc+teraz)
                past.append({"ts": ts, "time": int(dt.timestamp())})
            elif 0.05 < delta_h <= 6.05:    # do 6h w przod (prognoza)
                nowcast.append({"ts": ts, "time": int(dt.timestamp())})
        wynik = {"past": past, "nowcast": nowcast, "zrodlo": "IMGW"}
        _cache.update(t=time.time(), d=wynik)
        return JSONResponse(wynik, headers={"Cache-Control": "public, max-age=120"})
    except Exception as e:
        return JSONResponse({"past": [], "nowcast": [], "blad": str(e)[:120]}, status_code=502)
@router.get("/radar/kafel/{ts}/{z}/{x}/{y}.png")
def radar_kafel(ts: str, z: int, x: int, y: int):
    if not re.fullmatch(r"\d{8}T\d{6}Z", ts):
        return Response(status_code=400)
    # IMGW: z/y/x !
    url = f"https://tilesources-a.imgw.pl/tileserver.php?/index.json?/inca-prec-0-sfc-{ts}/{z}/{y}/{x}.png"
    try:
        dane = _get(url, 15).read()
        return Response(content=dane, media_type="image/png", headers={"Cache-Control": "public, max-age=180"})
    except Exception:
        pusty = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d4944415478da6360000000020001e221bc330000000049454e44ae426082")
        return Response(content=pusty, media_type="image/png", headers={"Cache-Control": "public, max-age=30"})
