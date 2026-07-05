from pathlib import Path

ROOT = Path("/root/rod-ai-studio/data/reels")

def create_reel_folder():
    ROOT.mkdir(parents=True, exist_ok=True)

    ids = [int(p.name) for p in ROOT.iterdir() if p.is_dir() and p.name.isdigit()]

    next_id = max(ids, default=0) + 1

    folder = ROOT / f"{next_id:06d}"
    folder.mkdir()

    (folder/"images").mkdir()
    (folder/"audio").mkdir()
    (folder/"video").mkdir()

    return folder
