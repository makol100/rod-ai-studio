from pathlib import Path

from src.ai.ollama import generate
from src.scenes.generator import generate_scenes
from src.images.prompts import generate_image_prompts
from src.images.generator import generate_images
from src.ai.image_backend import generate_image
from src.video.renderer import render_video
from src.reels import create_reel_folder, save_text
from src.audio.generator import generate_audio


def generate_reel(prompt: str):
    folder = create_reel_folder()

    article = generate(prompt)
    save_text(folder, "article.md", article)

    scenes = generate_scenes(article)
    save_text(folder, "scenes.txt", scenes)

    audio = generate_audio(folder, scenes)

    image_prompts = generate_image_prompts(scenes)
    save_text(folder, "prompts.txt", image_prompts)

    images = generate_images(folder)

    generated_images = []
    for img in images:
        generated_images.append(
            generate_image(
                img["prompt"],
                Path(img["output"])
            )
        )

    video = render_video(folder)

    return {
        "status": "ok",
        "folder": str(folder),
        "article_file": str(folder / "article.md"),
        "scenes_file": str(folder / "scenes.txt"),
        "prompts_file": str(folder / "prompts.txt"),
        "article": article,
        "scenes": scenes,
        "image_prompts": image_prompts,
        "images": images,
        "generated_images": generated_images,
        "audio": audio,
        "video": video,
    }
