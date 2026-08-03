import fal_client, requests, sys
SRC = "/root/rod-ai-studio/data/zarty/10010/kadry/k05_gumowiec_w_powietrzu.jpg"
OUT = "/root/rod-ai-studio/data/zarty/10010/kadry/k05.jpg"
PROMPT = ("CHANGE ONLY: completely remove the rubber boot hanging in the branches "
 "behind the man - the spot where it was shows only dark leaves and branches, "
 "as if the boot was never there. PRESERVE everything else exactly as in the "
 "original image: the man's face, furious expression, open mouth, beard, flat cap, "
 "clothing, pose, framing, the moonlit night orchard, fog, lighting, colors and "
 "composition. CONSTRAINTS: do not add any new objects, do not change the man in "
 "any way, photorealistic, same night lighting.")
ref = fal_client.upload_file(SRC)
res = fal_client.run("fal-ai/nano-banana-pro/edit",
    arguments={"prompt": PROMPT, "image_urls": [ref],
               "aspect_ratio": "9:16", "resolution": "2K", "safety_tolerance": 6},
    timeout=180, start_timeout=90)
r = requests.get(res["images"][0]["url"], timeout=120); r.raise_for_status()
open(OUT, "wb").write(r.content)
print(f"EDYCJA OK, {len(r.content)} B -> k05.jpg")
