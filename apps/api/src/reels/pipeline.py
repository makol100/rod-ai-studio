from pathlib import Path
import traceback

from src.ai.ollama import generate
from src.scenes.generator import generate_scenes
from src.images.prompts import generate_image_prompts
from src.images.generator import generate_images
from src.ai.image_backend import generate_image
from src.video.renderer import render_video
from src.reels import create_reel_folder, save_text
from src.audio.generator import generate_audio
from src.subtitles.generator import make_subtitles


def _log(msg: str):
    # widoczne na żywo w: docker logs -f fabryka-api
    print(f"[reel] {msg}", flush=True)


def _produce_media(folder: Path, scenes: str, result: dict) -> dict:
    """
    Druga połowa pipeline'u: gotowy scenariusz -> audio -> prompty -> obrazy -> wideo.
    Współdzielona przez generate_reel (pełny bieg) i render_from_scenes (z gotowego skryptu).
    Odporna: błąd jednego obrazu nie zabija reszty; render sam pomija brakujące klatki.
    """
    save_text(folder, "scenes.txt", scenes)
    result["scenes_file"] = str(folder / "scenes.txt")

    _log("audio (edge-tts)…")
    audio = generate_audio(folder, scenes)
    result["audio_count"] = len(audio)

    _log("prompty obrazow…")
    image_prompts = generate_image_prompts(scenes)
    save_text(folder, "prompts.txt", image_prompts)
    result["prompts_file"] = str(folder / "prompts.txt")

    images = generate_images(folder)
    total = len(images)
    _log(f"obrazy fal.ai: {total} szt…")

    ok = 0
    failed = []
    for img in images:
        idx = img.get("index")
        try:
            res = generate_image(img["prompt"], Path(img["output"]))
            if res.get("status") == "ok":
                ok += 1
                _log(f"    obraz {idx}/{total} OK")
            else:
                failed.append(idx)
                _log(f"    obraz {idx}/{total} BLAD: {res.get('error')}")
        except Exception as e:
            failed.append(idx)
            _log(f"    obraz {idx}/{total} WYJATEK: {e}")

    result["images_ok"] = ok
    result["images_failed"] = failed

    if ok == 0:
        result["status"] = "error"
        result["error"] = "Zaden obraz sie nie wygenerowal — render pominiety."
        _log("PRZERWANE: brak obrazow, render pominiety.")
        return result

    _log("napisy (whisper)…")
    subs_res = make_subtitles(folder)
    result["subs_count"] = subs_res.get("count", 0)

    _log("renderuje wideo…")
    video = render_video(folder)
    result["video"] = video

    if video.get("status") == "ok":
        from src.audio.music import add_background_music
        video_path = Path(video["output"])
        music_output = video_path.with_name("final_with_music.mp4")
        music_result = add_background_music(video_path, music_output)
        result["music"] = music_result
        if music_result.get("status") == "ok":
            video["output"] = music_result["output"]
    if isinstance(video, dict) and video.get("status") == "ok":
        result["video_file"] = video.get("output")
        _log(f"GOTOWE: {video.get('output')} (obrazy {ok}/{total})")
    else:
        result["status"] = "partial"
        _log(f"Render zwrocil blad: {video}")

    return result


def generate_reel(prompt: str, scene_count=None):
    """Pełny pipeline: prompt -> artykuł -> sceny -> (audio, obrazy, wideo)."""
    folder = create_reel_folder()
    _log(f"START (pelny) folder={folder}")
    result = {"status": "ok", "folder": str(folder), "mode": "generate_reel"}
    try:
        _log("artykul…")
        article = generate(prompt)
        save_text(folder, "article.md", article)
        result["article_file"] = str(folder / "article.md")

        _log("sceny…")
        scenes = generate_scenes(article, scene_count)

        return _produce_media(folder, scenes, result)

    except Exception as e:
        _log(f"BLAD KRYTYCZNY: {e}")
        result["status"] = "error"
        result["error"] = str(e)
        result["trace"] = traceback.format_exc().splitlines()[-3:]
        return result


def render_from_scenes(scenes: str):
    """
    Z gotowego, zatwierdzonego scenariusza: -> (audio, obrazy, wideo).
    Pomija generowanie artykułu i scen — renderuje DOKŁADNIE to, co podasz.
    Scenariusz musi być w formacie: SCENA N: / UJĘCIE: / LEKTOR:.
    """
    folder = create_reel_folder()
    _log(f"START (z gotowego skryptu) folder={folder}")
    result = {"status": "ok", "folder": str(folder), "mode": "render_from_scenes"}
    try:
        if not scenes or not scenes.strip():
            result["status"] = "error"
            result["error"] = "Pusty scenariusz."
            _log("PRZERWANE: pusty scenariusz.")
            return result

        return _produce_media(folder, scenes.strip(), result)

    except Exception as e:
        _log(f"BLAD KRYTYCZNY: {e}")
        result["status"] = "error"
        result["error"] = str(e)
        result["trace"] = traceback.format_exc().splitlines()[-3:]
        return result
