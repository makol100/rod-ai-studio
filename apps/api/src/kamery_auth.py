"""Logowanie do strony kamer ROD (dekret 03.09: formularz z widocznym haslem zamiast okienka przegladarki).
Caddy: forward_auth -> GET /kamery/auth (cookie kamery_auth = user:wygasa:hmac). Hasla: data/.secrets/kamery_uzytkownicy.json (600)."""
import hmac, hashlib, json, time, os
from urllib.parse import quote
from fastapi import APIRouter, Request, Form
from fastapi.responses import Response, RedirectResponse, PlainTextResponse
router = APIRouter()
UZYTK = "/root/rod-ai-studio/data/.secrets/kamery_uzytkownicy.json"
SEKRET = "/root/rod-ai-studio/data/.secrets/kamery_cookie_secret"
WAZNOSC = 365 * 24 * 3600
def _sekret() -> bytes:
    return open(SEKRET, "rb").read().strip()
def _podpis(user: str, exp: int) -> str:
    return hmac.new(_sekret(), f"{user}:{exp}".encode(), hashlib.sha256).hexdigest()[:32]
def _user_z_cookie(req: Request):
    c = req.cookies.get("kamery_auth", "")
    try:
        user, exp, sig = c.split(":", 2); exp = int(exp)
    except ValueError:
        return None
    if exp < time.time() or not hmac.compare_digest(sig, _podpis(user, exp)):
        return None
    return user
@router.get("/kamery/auth")
def kamery_auth(req: Request):
    user = _user_z_cookie(req)
    if not user:
        # forward_auth kopiuje te odpowiedz do klienta: przegladarka trafia na formularz, API (ws/frame) dostaje 401
        if req.headers.get("x-forwarded-uri", "").startswith("/api/") or "text/html" not in req.headers.get("accept", ""):
            return PlainTextResponse("zaloguj", status_code=401)
        return RedirectResponse("/login.html", status_code=302)
    uri = req.headers.get("x-forwarded-uri", "")
    if "/api/ws" in uri or "/api/frame.jpeg" in uri or uri in ("/", "/index.html"):
        try:  # dziennik "kto oglada" — Caddy redaguje Cookie w logach, wiec zapis idzie stad
            with open("/root/rod-ai-studio/data/kamery_dostepy.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps({"ts": time.time(), "user": user, "uri": uri, "ip": req.headers.get("x-forwarded-for", "").split(",")[0].strip()}) + "\n")
        except Exception:
            pass
    return Response(status_code=200, headers={"X-Kamery-User": user})
@router.post("/kamery/login")
def kamery_login(login: str = Form(""), haslo: str = Form("")):
    login = login.strip().lower(); haslo = haslo.strip()
    try:
        users = json.load(open(UZYTK, encoding="utf-8"))
    except Exception:
        users = {}
    if login in users and hmac.compare_digest(users[login], haslo):
        exp = int(time.time()) + WAZNOSC
        r = RedirectResponse("/", status_code=303)
        r.set_cookie("kamery_auth", f"{login}:{exp}:{_podpis(login, exp)}", max_age=WAZNOSC, path="/", secure=True, httponly=True, samesite="lax")
        return r
    return RedirectResponse("/login.html?blad=1&login=" + quote(login), status_code=303)
@router.get("/kamery/wyloguj")
def kamery_wyloguj():
    r = RedirectResponse("/login.html", status_code=303); r.delete_cookie("kamery_auth", path="/"); return r
