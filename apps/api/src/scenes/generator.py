from src.ai.ollama import generate
from src.config import SCENE_COUNT

def generate_scenes(text: str):
    prompt = f"""
Jesteś reżyserem krótkich rolek.

Na podstawie tekstu przygotuj {SCENE_COUNT} scen.

Każda scena ma dokładnie taki format:

SCENA 1
UJĘCIE: ...
LEKTOR: ...

SCENA 2
UJĘCIE: ...
LEKTOR: ...

Nie używaj markdown.
Nie dodawaj komentarzy.

Tekst:
{text}
"""
    return generate(prompt).strip()
