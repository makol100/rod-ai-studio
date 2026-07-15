from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from src.topics import router as topics_router
import os
import shutil

app = FastAPI(title="Fabryka Obrazów")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(topics_router)
from src.zarty import router as zarty_router
app.include_router(zarty_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "Fabryka Obrazów"
    }


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Fabryka Rolek API"
    }


@app.get("/panel")
def panel():
    from fastapi.responses import HTMLResponse
    with open("/app/src/panel.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


# ---------------------------------------------------------------
# UPLOAD MATERIAŁU (zdjęcia i filmy z telefonu)
#   filmy   (.mp4/.mov/...)  -> data/rolka-prad/filmy/
#   zdjęcia (.jpg/.png/...)  -> data/rolka-prad/budowa/
# ---------------------------------------------------------------
BAZA = "/root/rod-ai-studio/data/rolka-prad"
MUZYKA_KAT = "/root/rod-ai-studio/assets/music"
ROZSZ_FILM = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".3gp"}
ROZSZ_AUDIO = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}


@app.post("/upload")
async def upload(pliki: list[UploadFile] = File(...)):
    wgrane = []
    for p in pliki:
        nazwa = os.path.basename(p.filename or "bez_nazwy")
        ext = os.path.splitext(nazwa)[1].lower()
        if ext in ROZSZ_AUDIO:
            podkatalog, katalog = "muzyka", MUZYKA_KAT
        else:
            podkatalog = "filmy" if ext in ROZSZ_FILM else "budowa"
            katalog = os.path.join(BAZA, podkatalog)
        os.makedirs(katalog, exist_ok=True)
        cel = os.path.join(katalog, nazwa)

        with open(cel, "wb") as f:
            shutil.copyfileobj(p.file, f)

        wgrane.append({
            "plik": nazwa,
            "gdzie": podkatalog,
            "mb": round(os.path.getsize(cel) / 1048576, 1),
        })

    return {"status": "ok", "ile": len(wgrane), "wgrane": wgrane}


@app.get("/upload/lista")
def upload_lista():
    """Co już leży w katalogach materiału."""
    out = {}
    for pod in ("filmy", "budowa"):
        k = os.path.join(BAZA, pod)
        if os.path.isdir(k):
            out[pod] = sorted(
                {"plik": f, "mb": round(os.path.getsize(os.path.join(k, f)) / 1048576, 1)}
                for f in os.listdir(k) if not f.startswith(".")
            ) if False else [
                {"plik": f, "mb": round(os.path.getsize(os.path.join(k, f)) / 1048576, 1)}
                for f in sorted(os.listdir(k)) if not f.startswith(".")
            ]
        else:
            out[pod] = []
    return out


@app.get("/film")
def film():
    """Pobranie gotowego filmu."""
    from fastapi.responses import FileResponse
    p = os.path.join(BAZA, "FILM-ROD-16x9.mp4")
    if not os.path.exists(p):
        return {"status": "brak", "info": "film jeszcze nie zbudowany"}
    return FileResponse(p, media_type="video/mp4", filename="FILM-ROD-16x9.mp4")


@app.get("/kontaktowka")
def kontaktowka():
    """Plansza ze wszystkimi zdjęciami z budowy — do wskazywania kadrów."""
    from fastapi.responses import FileResponse
    p = os.path.join(BAZA, "KONTAKTOWKA-budowa.jpg")
    if not os.path.exists(p):
        return {"status": "brak"}
    return FileResponse(p, media_type="image/jpeg")


@app.get("/klatki")
def klatki():
    from fastapi.responses import FileResponse
    p = os.path.join(BAZA, "KONTAKTOWKA-klatki.jpg")
    return FileResponse(p, media_type="image/jpeg") if os.path.exists(p) else {"status": "brak"}


@app.get("/rolka")
def rolka():
    from fastapi.responses import FileResponse
    p = os.path.join(BAZA, "ROLKA-ZAPOWIEDZ.mp4")
    if not os.path.exists(p):
        return {"status": "brak"}
    return FileResponse(p, media_type="video/mp4", filename="ROLKA-ZAPOWIEDZ.mp4")


# ---------------------------------------------------------------
# OPIS DO PUBLIKACJI — generowany Bielikiem z gotowego scenariusza
# ---------------------------------------------------------------
@app.get("/opis/{reel_id}")
def opis_rolki(reel_id: str):
    from src.opis import generuj_opis
    try:
        return generuj_opis(reel_id)
    except FileNotFoundError as e:
        return {"status": "brak", "info": str(e)}
    except Exception as e:
        return {"status": "blad", "info": str(e)}


@app.get("/apk")
def apk():
    """Instalka apki — omija problemy Chrome z GitHubem."""
    from fastapi.responses import FileResponse
    p = os.path.join(BAZA, "app-debug.apk")
    if not os.path.exists(p):
        return {"status": "brak"}
    return FileResponse(p, media_type="application/vnd.android.package-archive",
                        filename="FabrykaRolek.apk")


# ---------------------------------------------------------------
# TESTOWY BAROMETR GRZYBIARZA — Wozniki i okolice
# ---------------------------------------------------------------
@app.get("/barometr")
def barometr_strona():
    from fastapi.responses import HTMLResponse
    with open("/app/src/barometr.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/barometr.json")
def barometr_dane():
    from src.barometr import dane
    return dane()


@app.get("/barometr/sygnal")
def barometr_sygnal():
    """Sygnał dla apki: czy dziś warto krzyknąć 'idź do lasu'.
    Zwraca datę jako klucz — apka powiadamia raz na dobę, przy wyniku 75+."""
    from src.barometr import dane
    import datetime as dt
    d = dane()
    return {
        "data": dt.date.today().isoformat(),
        "wynik": d["wynik"],
        "status": d["status"],
        "alarm": d["wynik"] >= 75,
    }
