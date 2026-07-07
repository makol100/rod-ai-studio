import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

# Podział modeli po zadaniu:
DEFAULT_MODEL = "SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0"  # polski tekst: artykul, sceny, lektor
PROMPT_MODEL = "gemma3:4b"                                    # dlugie angielskie prompty obrazow (Bielik sie dlawi)


def generate(prompt: str, model: str = None):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model or DEFAULT_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 8192,
                "num_predict": 2048,
            },
        },
        timeout=600,
    )

    response.raise_for_status()
    return response.json()["response"]
