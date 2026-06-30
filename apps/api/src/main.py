from fastapi import FastAPI
from src.topics import router as topics_router

app = FastAPI(title="Fabryka Rolek")

app.include_router(topics_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "Fabryka Rolek"
    }
