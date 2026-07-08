from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.topics import router as topics_router

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
