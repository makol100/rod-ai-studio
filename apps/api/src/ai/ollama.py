import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

# Podział modeli po zadaniu:
DEFAULT_MODEL = "SpeakLeash/bielik-11b-v3.0-instruct:Q6_K"  # polski tekst: artykul, sceny, lektor
# Zwiekszone 08.07.2026 po powiekszeniu VPS (22GB RAM). Bylo: bielik-4.5b-v3.0-instruct:Q8_0.
# Stary model ZOSTAJE pobrany na dysku jako bezpieczna droga powrotu, gdyby trzeba bylo wrocic.
PROMPT_MODEL = "qwen3:14b"  # dlugie angielskie prompty obrazow + zadanie NAPRAW (Bielik sie dlawi na obu)
# Zwiekszone 08.07.2026 po powiekszeniu VPS. Bylo: llama3.1:8b.
# Stara Llama ZOSTAJE pobrana na dysku jako bezpieczna droga powrotu.


def generate(prompt: str, model: str = None, temperature: float = None, repeat_penalty: float = 1.15):
    options = {
        "num_ctx": 8192,  # 8192 to twardy sufit architektury Bielika - wiecej nie ma sensu
        "num_predict": 2048,
        "repeat_penalty": repeat_penalty,
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


def has_repetition_loop(text: str, min_len: int = 15, min_repeats: int = 3) -> bool:
    """Wykrywa czy tekst zawiera petle powtorzen - typowa awaria LLM
    (np. spam emoji albo powtarzajace sie zdanie). Sprawdza czy jakis
    fragment dlugosci min_len powtarza sie min_repeats razy w tekscie.
    Sprawdza tylko poczatek tekstu (petla zwykle zaczyna sie szybko),
    zeby nie bylo to kosztowne obliczeniowo na dlugich tekstach.
    """
    if not text or len(text) < min_len * min_repeats:
        return False
    check_range = min(len(text) - min_len, 300)
    for start in range(0, max(check_range, 1)):
        chunk = text[start:start + min_len]
        if text.count(chunk) >= min_repeats:
            return True
    return False
