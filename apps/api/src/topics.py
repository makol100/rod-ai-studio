import re
from pathlib import Path
import subprocess
import shutil
from fastapi import APIRouter, Body, HTTPException

from src.ai.ollama import generate
from src.db.database import save_reel, list_reels
from src.scenes.generator import generate_scenes
from src.images.prompts import generate_image_prompts
from src.reels.pipeline import generate_reel

router = APIRouter()


@router.get("/topics")
def get_topics():
    return {
        "status": "ok",
        "topics": [
            "5 ciekawostek o...",
            "3 błędy, które popełnia każdy",
            "Czy wiedziałeś, że...?",
            "Największy mit na temat...",
            "TOP 10 faktów"
        ]
    }


def clean_hashtags(raw: str):
    tags = re.findall(r"#[A-Za-zÀ-ž0-9_]+", raw)
    out = []
    for tag in tags:
        if tag.lower() not in [x.lower() for x in out]:
            out.append(tag)
    return " ".join(out[:10])


@router.post("/generate")
def generate_text(data: dict = Body(...)):
    prompt = data["prompt"]

    text = generate(prompt)

    title_prompt = (
        "Wygeneruj krótki, chwytliwy tytuł do rolki na podstawie tego tekstu. "
        "Zwróć tylko sam tytuł, bez cudzysłowów i bez dodatkowego komentarza:\n\n"
        + text
    )
    title = generate(title_prompt).strip()

    hashtags_prompt = (
        "Jesteś generatorem hashtagów Instagrama.\n"
        "Wygeneruj dokładnie 10 trafnych hashtagów.\n"
        "Odpowiedz WYŁĄCZNIE hashtagami.\n"
        "Każdy hashtag musi zaczynać się od #.\n"
        "Oddziel je pojedynczą spacją.\n"
        "Nie dodawaj żadnych zdań, komentarzy ani wyjaśnień.\n\n"
        + text
    )
    hashtags = clean_hashtags(generate(hashtags_prompt))

    save_reel(prompt, title, text, hashtags)

    return {
        "status": "ok",
        "title": title,
        "text": text,
        "hashtags": hashtags,
        "saved": True
    }


@router.get("/reels")
def get_reels():
    return {
        "status": "ok",
        "reels": list_reels()
    }


@router.post("/generate-scenes")
def generate_scenes_endpoint(data: dict = Body(...)):
    return {"status": "ok", "scenes": generate_scenes(data["text"])}


@router.post("/generate-image-prompts")
def generate_image_prompts_endpoint(data: dict = Body(...)):
    return {
        "status": "ok",
        "prompts": generate_image_prompts(data["scenes"])
    }


@router.post("/generate-reel")
def generate_reel_endpoint(data: dict = Body(...)):
    return generate_reel(data["prompt"])

PROMPTS_FILE = Path(__file__).resolve().parent / "images" / "prompts.py"

@router.get("/host/prompts-py")
def host_get_prompts_py():
    return {
        "status": "ok",
        "path": "apps/api/src/images/prompts.py",
        "content": PROMPTS_FILE.read_text(encoding="utf-8")
    }




@router.get("/host/status")
def host_status():
    from pathlib import Path

    prompts = Path("/app/prompts/prompts.py").exists()

    return {
        "host": True,
        "prompts": prompts,
        "write": True,
    }

@router.post("/host/prompts-py")
def host_set_prompts_py(payload: dict = Body(...)):
    content = payload["content"]

    if not content.strip():
        raise HTTPException(status_code=400, detail="Odmowa wdrożenia: plik jest pusty.")

    old_size = PROMPTS_FILE.stat().st_size
    new_size = len(content.encode("utf-8"))

    if old_size > 3000 and new_size < 500:
        raise HTTPException(status_code=400, detail=f"Odmowa wdrożenia: nowy plik ma tylko {new_size} bajtów.")

    shutil.copy2(PROMPTS_FILE, PROMPTS_FILE.with_suffix(".py.bak"))
    PROMPTS_FILE.write_text(content, encoding="utf-8")

    return {
        "status": "ok",
        "path": "apps/api/src/images/prompts.py",
        "bytes": new_size,
        "backup": str(PROMPTS_FILE.with_suffix(".py.bak"))
    }


@router.post("/host/restart-api")
def host_restart_api():
    r = subprocess.run(
        ["docker","restart","fabryka-api"],
        capture_output=True,
        text=True
    )
    return {
        "status":"ok" if r.returncode==0 else "error",
        "stdout":r.stdout,
        "stderr":r.stderr
    }
