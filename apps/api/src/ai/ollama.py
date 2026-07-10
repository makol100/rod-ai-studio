import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

# Podział modeli po zadaniu:
DEFAULT_MODEL = "SpeakLeash/bielik-11b-v3.0-instruct:Q8_0"  # polski tekst: artykul, sceny, lektor (Q8_0 - podniesione z Q6_K 09.07.2026 na zyczenie Tomasza, wyzsza precyzja kwantyzacji, 11.87GB)
# Zwiekszone 08.07.2026 po powiekszeniu VPS (22GB RAM). Bylo: bielik-4.5b-v3.0-instruct:Q8_0.
# Stary model ZOSTAJE pobrany na dysku jako bezpieczna droga powrotu, gdyby trzeba bylo wrocic.
PROMPT_MODEL = "qwen3:14b"  # dlugie angielskie prompty obrazow + zadanie NAPRAW (Bielik sie dlawi na obu)
# Zwiekszone 08.07.2026 po powiekszeniu VPS. Bylo: llama3.1:8b.
# Stara Llama ZOSTAJE pobrana na dysku jako bezpieczna droga powrotu.


def generate(prompt: str, model: str = None, temperature: float = None, repeat_penalty: float = 1.15, max_tokens: int = 2048):
    options = {
        "num_ctx": 8192,  # 8192 to twardy sufit architektury Bielika - wiecej nie ma sensu
        "num_predict": max_tokens,  # domyslnie 2048; podbij dla dlugich odpowiedzi (np. audyt = wady + caly przepisany scenariusz)
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


def has_repetition_loop(text: str, min_len: int = 25, min_repeats: int = 4) -> bool:
    """Wykrywa czy tekst zawiera petle powtorzen - typowa awaria LLM
    (np. spam emoji albo powtarzajace sie zdanie). Sprawdza czy jakis
    fragment dlugosci min_len powtarza sie min_repeats razy w tekscie.
    Sprawdza tylko poczatek tekstu (petla zwykle zaczyna sie szybko),
    zeby nie bylo to kosztowne obliczeniowo na dlugich tekstach.

    NAPRAWIONE 09.07.2026 (Dyskusja): progi byly za czule (min_len=15,
    min_repeats=3) - lapaly fałszywe alarmy na naturalnych powtorzeniach
    krotkich zwrotow scenariusza (np. "UJĘCIE: Zbliżenie" powtorzone w 3
    z 15 scen, bo to po prostu 3 kadry ze zblizeniem - normalne w
    scenopisarstwie, nie awaria modelu). Podniesione do min_len=25,
    min_repeats=4 - prawdziwa petla powtorzen (np. model zapetlony w kolko
    powtarzajacy to samo zdanie/akapit) i tak generuje znacznie dluzsze
    i czestsze powtorzenia niz jakikolwiek naturalny zbieg okolicznosci
    w tresci, wiec to nadal lapie realne awarie, tylko bez falszywych
    alarmow na normalnym tekscie."""
    if not text or len(text) < min_len * min_repeats:
        return False
    check_range = min(len(text) - min_len, 300)
    for start in range(0, max(check_range, 1)):
        chunk = text[start:start + min_len]
        if text.count(chunk) >= min_repeats:
            return True
    return False
