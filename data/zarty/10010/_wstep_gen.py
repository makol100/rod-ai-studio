"""Kadr k00 (wstep-szept) — nano-banana-pro/edit, ref bohater_noc.jpg, $0.15. Zgoda Tomasza 26.07 ("Ruszac!"). GUARD __main__."""
import sys
from pathlib import Path
import requests, fal_client

K = Path("/root/rod-ai-studio/assets/zarty/karty")
OUT = Path("/root/rod-ai-studio/data/zarty/10010/kadry")
NOC = ("Dark Polish allotment orchard at night, old apple trees, moonlight through "
       "the branches, light ground fog, deep shadows, cinematic moody lighting. "
       "Photorealistic, natural documentary photography, vertical 9:16 composition. "
       "No captions, no subtitles, no text anywhere. ")
TOMEK = ("The man from the reference image - identity lock: exactly the same eyes, "
         "nose, jawline and facial proportions - about fifty years old, long hair "
         "tied in a ponytail, full salt-and-pepper beard, wearing a flat cap and a "
         "dark work jacket. ")
PROMPT = (NOC + "Medium close shot from slightly below eye level, front three-quarter "
  "facial angle. " + TOMEK + "He crouches low, sneaking between the apple trees as if "
  "conducting a covert military operation, leaning slightly toward the camera with "
  "intense conspiratorial focus, mock-thriller deadly seriousness. A small apple-tree "
  "twig is tucked absurdly into the side of his flat cap as improvised camouflage. "
  "His face sits in the middle-lower portion of the frame, occupying about 35-40 "
  "percent; both eyes and both lip contours remain clearly visible below the "
  "moustache despite the beard and night lighting. Leave clean dark negative space "
  "in the upper third of the frame for a meme-style title overlay, away from his "
  "eyes and mouth. A few red apples visible on the branches. One person only, "
  "natural anatomy, realistic hands.")

def main():
    ref = fal_client.upload_file(str(K / "bohater_noc.jpg"))
    res = fal_client.run("fal-ai/nano-banana-pro/edit",
        arguments={"prompt": PROMPT, "image_urls": [ref],
                   "aspect_ratio": "9:16", "resolution": "2K", "safety_tolerance": 6},
        timeout=180, start_timeout=90)
    r = requests.get(res["images"][0]["url"], timeout=120); r.raise_for_status()
    (OUT / "k00.jpg").write_bytes(r.content)
    print(f"[k00] OK ({len(r.content)} B)", flush=True)

if __name__ == '__main__':
    main()
