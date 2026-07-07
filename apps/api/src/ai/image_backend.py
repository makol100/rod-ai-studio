from pathlib import Path
import requests
import fal_client

# Model i limity — dobrane pod FLUX schnell (szybki) na fal.ai.
FAL_MODEL = "fal-ai/flux-1/dev"
FAL_TIMEOUT = 90          # maks. czas generowania jednego obrazu (s)
FAL_START_TIMEOUT = 60    # maks. czas oczekiwania w kolejce fal (s)
DOWNLOAD_TIMEOUT = 120    # maks. czas pobrania gotowego JPG (s)
RETRIES = 1               # ile dodatkowych prób po pierwszym błędzie


def generate_image(prompt: str, output: Path):
    """
    Generuje jeden obraz i zapisuje go do `output`.

    W przeciwieństwie do wersji poprzedniej NIE rzuca wyjątku przy błędzie —
    zwraca {"status": "error", ...}. Dzięki temu pojedynczy zły obraz nie
    wywala całego renderu, a renderer (parujący po numerze pliku) po prostu
    pominie brakującą klatkę.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    last_err = None

    for attempt in range(1, RETRIES + 2):  # domyślnie próby 1 i 2
        try:
            result = fal_client.run(
                FAL_MODEL,
                arguments={"prompt": prompt, "image_size": "portrait_16_9"},
                timeout=FAL_TIMEOUT,
                start_timeout=FAL_START_TIMEOUT,
            )

            url = result["images"][0]["url"]

            r = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
            r.raise_for_status()
            output.write_bytes(r.content)

            return {
                "status": "ok",
                "prompt": prompt,
                "output": str(output),
                "url": url,
                "attempts": attempt,
            }

        except Exception as e:
            last_err = e
            print(f"[image] proba {attempt} nieudana dla {output.name}: {e}", flush=True)

    return {
        "status": "error",
        "prompt": prompt,
        "output": str(output),
        "error": str(last_err),
    }
