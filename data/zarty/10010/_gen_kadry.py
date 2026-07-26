"""Kadry odcinka 10010 (6 szt.) — nano-banana-pro/edit, referencja bohater_noc.jpg.
Zgoda Tomasza 26.07 ("Pasuje."), 6 x $0.15 = $0.90.
GUARD __main__ OBOWIAZKOWY (lekcja 10009: import wykonal submity za $5.12)."""
import sys, time
from pathlib import Path
import requests, fal_client

K = Path("/root/rod-ai-studio/assets/zarty/karty")
OUT = Path("/root/rod-ai-studio/data/zarty/10010/kadry")

NOC = ("Dark Polish allotment orchard at night, old apple tree, moonlight through "
       "the branches, light ground fog, deep shadows, cinematic moody lighting. "
       "Photorealistic, natural documentary photography, vertical 9:16 composition. "
       "No captions, no subtitles, no text anywhere. ")
TOMEK = ("The man from the reference image - identity lock: exactly the same eyes, "
         "nose, jawline and facial proportions - about fifty years old, long hair "
         "tied in a ponytail, full salt-and-pepper beard, wearing a flat cap and a "
         "dark work jacket. ")
NOGI = ("High up in the tree crown two legs dangle down from the branches - only "
        "trouser legs and rubber boots are visible, the person is completely hidden "
        "in the leaves, no face, no torso, no silhouette. ")

KADRY = {
 "k01": NOC + "Wide shot. " + TOMEK + "He crouches hidden in the bushes below the "
   "apple tree, looking up into the crown with intense angry focus. Comedic "
   "stakeout mood.",
 "k02": NOC + "Low angle shot from below the tree. " + NOGI + TOMEK + "He lunges "
   "forward and reaches up with one hand between the dangling legs, gripping "
   "firmly. Motion blur on his arm, dynamic comedic action.",
 "k03": NOC + "Close-up portrait. " + TOMEK + "He shouts angrily upwards into the "
   "tree crown, mouth open mid-shout, face clearly visible and lit by moonlight.",
 "k04": NOC + "Medium shot from the side. " + NOGI + "Those dangling legs are "
   "stiffening and trembling. " + TOMEK + "Below them he speaks through clenched "
   "teeth, his raised arm disappearing up among the branches. His face and mouth "
   "clearly visible.",
 "k05": NOC + "Extreme close-up. " + TOMEK + "His face is furious, veins on his "
   "forehead, jaw clenched hard, eyes burning with rage, mouth open shouting. "
   "A single rubber boot is falling through the air behind him, out of focus.",
 "k06": NOC + "Medium shot. " + NOGI + "Those dangling legs now hang limp and "
   "motionless. " + TOMEK + "Standing below, he stares up into the crown with a "
   "stunned, dumbfounded expression, mouth slightly open in disbelief, arm still "
   "raised into the branches.",
}

def main():
    ref = fal_client.upload_file(str(K / "bohater_noc.jpg"))
    print("[kadry] referencja nocna OK", flush=True)
    bledy = 0
    for nazwa, prompt in KADRY.items():
        out = OUT / f"{nazwa}.jpg"
        if out.exists():
            print(f"[kadry] {nazwa} istnieje, pomijam", flush=True)
            continue
        try:
            res = fal_client.run("fal-ai/nano-banana-pro/edit",
                arguments={"prompt": prompt, "image_urls": [ref],
                           "aspect_ratio": "9:16", "resolution": "2K",
                           "safety_tolerance": 6},
                timeout=180, start_timeout=90)
            r = requests.get(res["images"][0]["url"], timeout=120)
            r.raise_for_status()
            out.write_bytes(r.content)
            print(f"[kadry] {nazwa} OK ({len(r.content)} B)", flush=True)
        except Exception as e:
            bledy += 1
            print(f"[kadry] {nazwa} BLAD: {str(e)[:140]}", flush=True)
        time.sleep(2)
    print(f"[kadry] KONIEC, bledy: {bledy}", flush=True)
    sys.exit(1 if bledy else 0)

if __name__ == '__main__':
    main()
