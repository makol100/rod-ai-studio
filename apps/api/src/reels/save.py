from pathlib import Path

def save_text(folder: Path, name: str, content: str):
    (folder / name).write_text(content, encoding="utf-8")
