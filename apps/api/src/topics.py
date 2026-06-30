from fastapi import APIRouter

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

from fastapi import Body
from src.ai.ollama import generate

@router.post("/generate")
def generate_text(data: dict = Body(...)):
    return {
        "status": "ok",
        "text": generate(data["prompt"])
    }
