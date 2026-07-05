from pathlib import Path
from src.config import SCENE_COUNT
import subprocess


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def make_clip(image: Path, output: Path, duration: float):
    run([
        "ffmpeg", "-y",
        "-loop", "1",
        "-t", str(duration),
        "-i", str(image),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,format=yuv420p",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output),
    ])


def render_video(folder: Path):
    images = folder / "images"
    video = folder / "video"
    video.mkdir(exist_ok=True)

    intro = Path("/root/rod-ai-studio/assets/branding/intro.png")
    output = video / "final.mp4"
    concat_file = video / "concat.txt"
    parts_dir = video / "parts"
    parts_dir.mkdir(exist_ok=True)

    parts = []

    try:
        if intro.exists():
            intro_clip = parts_dir / "00_intro.mp4"
            make_clip(intro, intro_clip, 2)
            parts.append(intro_clip)

        for i in range(1, SCENE_COUNT + 1):
            img = images / f"{i:02}.jpg"
            if img.exists():
                clip = parts_dir / f"{i:02}.mp4"
                make_clip(img, clip, 2.5)
                parts.append(clip)

        if not parts:
            return {"status": "error", "stderr": "No intro or image clips found"}

        concat_file.write_text(
            "".join([f"file '{p}'\n" for p in parts]),
            encoding="utf-8"
        )

        run([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
            "-movflags", "+faststart",
            str(output),
        ])

        return {
            "status": "ok",
            "output": str(output),
            "intro": str(intro),
            "concat": str(concat_file),
            "parts": [str(p) for p in parts],
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "stderr": e.stderr.decode(errors="ignore"),
            "concat": concat_file.read_text(encoding="utf-8") if concat_file.exists() else "",
        }
