"""Generacja 8 obrazow rolki 000098 przez fal-ai/nano-banana-pro/edit
z referencja stacja.jpg. Zgoda Tomasza 25.07 ("Generuj"), ~$1.20.
Uruchamiac w kontenerze fabryka-api (venv, FAL_KEY w env)."""
import re, sys, time
from pathlib import Path
import requests
import fal_client

FOLDER = Path("/root/rod-ai-studio/data/reels/000098")
REF = FOLDER / "refs" / "stacja.jpg"
IMG = FOLDER / "images"
IMG.mkdir(exist_ok=True)

DOPISEK = (
    "\n\nWAZNE: jesli w kadrze widac stacje pogodowa, jej czujnik, anemometr, "
    "wiatrowskaz, wyswietlacz LCD albo ekran aplikacji - musi to byc DOKLADNIE "
    "urzadzenie z zalaczonego zdjecia referencyjnego (bialy zestaw 7 w 1): ten sam "
    "ksztalt, kolory i detale. Nie wymyslaj innego modelu stacji. "
    "Zadnych napisow, podpisow ani tekstu na obrazie."
)

def parse_prompts(txt):
    czesci = re.split(r"PROMPT (\d+):", txt)
    out = {}
    for i in range(1, len(czesci), 2):
        out[int(czesci[i])] = czesci[i+1].strip()
    return out

def main():
    prompts = parse_prompts((FOLDER / "prompts.txt").read_text())
    assert len(prompts) == 8, f"oczekiwano 8 promptow, jest {len(prompts)}"
    print("[gen] upload referencji do fal...", flush=True)
    ref_url = fal_client.upload_file(str(REF))
    print(f"[gen] ref OK: {ref_url[:60]}...", flush=True)
    bledy = 0
    for n in range(1, 9):
        out = IMG / f"{n:02d}.jpg"
        if out.exists():
            print(f"[gen] {n}/8 juz istnieje, pomijam", flush=True)
            continue
        print(f"[gen] {n}/8 generuje...", flush=True)
        try:
            result = fal_client.run(
                "fal-ai/nano-banana-pro/edit",
                arguments={
                    "prompt": prompts[n] + DOPISEK,
                    "image_urls": [ref_url],
                    "aspect_ratio": "9:16",
                },
                timeout=180,
                start_timeout=90,
            )
            url = result["images"][0]["url"]
            r = requests.get(url, timeout=120)
            r.raise_for_status()
            out.write_bytes(r.content)
            print(f"[gen] {n}/8 OK ({len(r.content)} B)", flush=True)
        except Exception as e:
            bledy += 1
            print(f"[gen] {n}/8 BLAD: {e}", flush=True)
        time.sleep(2)
    print(f"[gen] KONIEC, bledy: {bledy}", flush=True)
    sys.exit(1 if bledy else 0)

main()
