from pathlib import Path
import requests
import fal_client

def generate_image(prompt: str, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)

    result = fal_client.run(
        "fal-ai/flux-1/schnell",
        arguments={
            "prompt": prompt,
            "image_size": "portrait_16_9"
        }
    )

    url = result["images"][0]["url"]

    r = requests.get(url, timeout=120)
    r.raise_for_status()

    output.write_bytes(r.content)

    return {
        "status": "ok",
        "prompt": prompt,
        "output": str(output),
        "url": url
    }
