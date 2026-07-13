from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from src.topics import router as topics_router
import os
import shutil

app = FastAPI(title="Fabryka Rolek")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(topics_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "Fabryka Rolek"
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
