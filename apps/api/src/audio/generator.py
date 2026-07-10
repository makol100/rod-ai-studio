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
    """NAPRAWIONE 09.07.2026 (Dyskusja, rolka 000084) - KRYTYCZNY bug: stara
    wersja czytala TYLKO PIERWSZA LINIE bloku LEKTOR. Jesli Bielik napisal
    LEKTOR jako kilka linii (np. lista punktowana z myslnikami albo
    numeracja 1./2./3.), wszystko po pierwszej linii bylo CICHO gubione -
    nigdy nie trafialo do edge-tts, wiec audio bylo drastycznie krotsze niz
    powinno (potwierdzone: scena z 622 znakami tekstu miala tylko 8s audio
    zamiast ~35-40s). Teraz zbiera WSZYSTKIE linie nalezace do tego samego
    bloku LEKTOR - konczy sie dopiero na pustej linii albo nowym znaczniku
    SCENA/UJECIE/LEKTOR."""
    raw_lines = scenes.splitlines()
    lines = []
    i = 0
    while i < len(raw_lines):
        line = raw_lines[i].strip()
        m = re.match(r"^LEKTO\w*:\s*(.*)", line)
        if m:
            czesci = [m.group(1).strip()]
            i += 1
            while i < len(raw_lines):
                nastepna = raw_lines[i].strip()
                if not nastepna:
                    break
                if re.match(r"^(SCENA|UJ[E\u0118]CIE|LEKTO\w*)\s*:", nastepna, re.IGNORECASE):
                    break
                czesci.append(nastepna)
                i += 1
            text = " ".join(cz for cz in czesci if cz)
            text = text.strip('"').strip("*").replace("*", "").strip()
            # NAPRAWIONE 09.07.2026 (Dyskusja, rolka 000085) - Bielik czasem
            # zaznacza pusta scene doslownym placeholderem "(brak tekstu)" -
            # bez tej naprawy edge-tts to LITERALNIE WYPOWIADAL na glos
            # ("brak tekstu"), a Whisper wiernie to transkrybowal w napisach.
            # Taki placeholder = scena bez lektora (cisza), nie tekst do przeczytania.
            if re.match(r"^\(?\s*brak\s+tekstu\s*\)?\.?$", text, re.IGNORECASE):
                text = ""
            if text:
                lines.append(text)
            else:
                lines.append("")  # pusta scena - zachowuje wyrownanie numeracji scen
            continue
        i += 1
    if not any(lines):
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

        if not text:
            # scena bez lektora (np. placeholder "(brak tekstu)" wykryty w
            # extract_narration) - NIE generujemy pliku audio w ogole.
            # render_video juz i tak obsluguje brakujacy .wav (fallback 2.5s ciszy).
            output.unlink(missing_ok=True)
            results.append({"scene": idx, "text": "", "output": None, "skipped": True})
            continue

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
