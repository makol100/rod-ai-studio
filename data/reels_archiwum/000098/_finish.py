"""Dokonczenie rolki 000098 v2 (decyzja "B"): audio z POPRAWIONEGO
scenes.txt -> napisy Whisper (stala zgoda) -> render z muzyka.
Obrazy musza juz lezec w images/ (z _gen_images.py, z referencja)."""
from pathlib import Path
from src.audio.generator import generate_audio
from src.subtitles.generator import make_subtitles
from src.video.renderer import render_video

FOLDER = Path("/root/rod-ai-studio/data/reels/000098")

imgs = sorted((FOLDER / "images").glob("*.jpg"))
assert len(imgs) == 8, f"oczekiwano 8 obrazow, jest {len(imgs)} - STOP"

scenes = (FOLDER / "scenes.txt").read_text()
print("[fin] audio (edge-tts, poprawiony scenariusz)...", flush=True)
generate_audio(FOLDER, scenes)
print("[fin] napisy (Whisper)...", flush=True)
make_subtitles(FOLDER)
print("[fin] render + muzyka...", flush=True)
wynik = render_video(FOLDER)
print(f"[fin] GOTOWE: {wynik}", flush=True)
