from pathlib import Path
import os
import re
import subprocess

EDGE_TTS_BIN = "/app/venv/bin/edge-tts"
EDGE_TTS_VOICE = "pl-PL-MarekNeural"

_TTS_ENV = os.environ.copy()
_TTS_ENV["LC_ALL"] = "C.UTF-8"
_TTS_ENV["LANG"] = "C.UTF-8"


def extract_narration(scenes: str) -> list[str]:
    raw_lines = scenes.splitlines()
    lines = []
    i = 0
    while i < len(raw_lines):
        line = raw_lines[i].strip()
        m = re.match(r"^LEKTO\w*:\s*(.*)", line)
        if m:
            text = m.group(1).strip()
            if not text and i + 1 < len(raw_lines):
                next_line = raw_lines[i + 1].strip()
                if next_line and not re.match(r"^(SCENA|UJ[E\u0118]CIE|LEKTO\w*)\s*:", next_line, re.IGNORECASE):
                    text = next_line
                    i += 1
            text = text.strip('"').strip("*").replace("*", "").strip()
            if text:
                lines.append(text)
        i += 1
    if not lines:
        print("[audio] UWAGA: 0 linii LEKTOR w scenach - sprawdz format scenes.txt")
    return lines


def generate_audio(folder: Path, scenes: str) -> list[dict]:
    audio_dir = folder / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    narrations = extract_narration(scenes)
    results = []

    for idx, text in enumerate(narrations, start=1):
        output = audio_dir / f"{idx:02d}.wav"
        mp3_tmp = audio_dir / f"{idx:02d}.mp3"

        subprocess.run(
            [
                EDGE_TTS_BIN,
                "--voice", EDGE_TTS_VOICE,
                "--text", text,
                "--write-media", str(mp3_tmp),
            ],
            check=True,
            env=_TTS_ENV,
        )

        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(mp3_tmp), str(output)],
            check=True,
        )
        mp3_tmp.unlink(missing_ok=True)

        results.append({
            "scene": idx,
            "text": text,
            "output": str(output),
        })

    return results
