from pathlib import Path
import subprocess
import random

MUSIC_DIR = Path("/root/rod-ai-studio/assets/music")


def _ffprobe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def pick_track() -> Path | None:
    if not MUSIC_DIR.exists():
        return None
    tracks = [p for p in MUSIC_DIR.iterdir() if p.suffix.lower() in (".mp3", ".wav", ".m4a")]
    if not tracks:
        return None
    return random.choice(tracks)


def add_background_music(video_path: Path, output_path: Path, music_path: Path | None = None) -> dict:
    chosen = music_path or pick_track()
    if chosen is None:
        return {"status": "skipped", "reason": "brak plikow w assets/music"}

    duration = _ffprobe_duration(video_path)

    filter_complex = (
        "[0:a]asplit=2[narr][sc];"
        f"[1:a]aloop=loop=-1:size=2e9,atrim=0:{duration},volume=0.4[music];"
        "[music][sc]sidechaincompress=threshold=0.02:ratio=10:attack=50:release=500[ducked];"
        "[narr][ducked]amix=inputs=2:duration=first[aout]"
    )

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(video_path),
            "-i", str(chosen),
            "-filter_complex", filter_complex,
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            str(output_path),
        ],
        check=True,
    )
    return {"status": "ok", "output": str(output_path), "music": str(chosen)}
