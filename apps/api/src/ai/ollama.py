import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"


def generate(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": False,
        },
        timeout=600,
    )

    response.raise_for_status()
    return response.json()["response"]
