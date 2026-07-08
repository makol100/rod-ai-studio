import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

# Podział modeli po zadaniu:
DEFAULT_MODEL = "SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0"  # polski tekst: artykul, sceny, lektor
PROMPT_MODEL = "llama3.1:8b"                                  # dlugie angielskie prompty obrazow + zadanie NAPRAW (Bielik sie dlawi na obu)


def generate(prompt: str, model: str = None, temperature: float = None):
    options = {
        "num_ctx": 8192,
        "num_predict": 2048,
    }
    if temperature is not None:
        options["temperature"] = temperature

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model or DEFAULT_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": options,
        },
        timeout=600,
    )

    response.raise_for_status()
    return response.json()["response"]
