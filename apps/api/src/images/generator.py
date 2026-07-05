from pathlib import Path
import re

def parse_prompts(text: str):
    parts = re.split(r"PROMPT\s+\d+\s*:", text, flags=re.IGNORECASE)
    prompts = []

    for part in parts:
        clean = part.strip()
        if clean:
            if clean.lower().startswith("oto "):
                continue
            prompts.append(clean)

    return prompts

def generate_images(folder: Path):
    text = folder.joinpath("prompts.txt").read_text(encoding="utf-8")
    prompts = parse_prompts(text)

    images_dir = folder / "images"
    images_dir.mkdir(exist_ok=True)

    result = []

    for i, prompt in enumerate(prompts, start=1):
        result.append({
            "index": i,
            "prompt": prompt,
            "output": str(images_dir / f"{i:02}.jpg")
        })

    return result
