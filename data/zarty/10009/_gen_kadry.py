"""Kadry odcinka 10009 (9 szt.) — nano-banana-pro/edit, refy z domeny zmierzch.
Zgoda Tomasza 25.07 ("Przygotowanie"), ~$1.35. Zapis: data/zarty/10009/kadry/"""
import sys, time
from pathlib import Path
import requests, fal_client

K = Path("/root/rod-ai-studio/assets/zarty/karty")
OUT = Path("/root/rod-ai-studio/data/zarty/10009/kadry")

SW = ("Golden hour, low warm sun just before dusk in a lush Polish allotment "
      "garden, next to a simple garden fence, long soft shadows, warm "
      "orange-amber light. Photorealistic, natural documentary photography, "
      "vertical 9:16 composition. No captions, no text anywhere. ")
TOMEK = ("The man from reference image {n} - identity lock: exactly the same "
         "eyes, nose, jawline and facial proportions - long ponytail, full "
         "salt-and-pepper beard, wearing a dark casual jacket over a black "
         "t-shirt. ")
JANUSZ = ("The tall thin man in his mid-sixties from reference image {n} - "
          "identity lock: exactly the same eyes, nose, jawline and facial "
          "proportions - grey mustache, wearing dark sunglasses and a grey "
          "hoodie with the hood pulled over his head like an amateur gangster. ")

KADRY = {
 "k01": (["bohater_zmierzch.jpg", "janusz_zmierzch.jpg"],
   SW + "Wide shot, two men by the fence. " + TOMEK.format(n=1) +
   "He stands by the fence glancing nervously left and right. " + JANUSZ.format(n=2) +
   "He is just approaching him along the fence. Comedic conspiratorial mood."),
 "k02": (["janusz_zmierzch.jpg"],
   SW + "Medium close-up. " + JANUSZ.format(n=1) +
   "He leans over the fence in a conspiratorial whispering pose, hand half "
   "covering his mouth, looking around. His mouth area is clearly visible."),
 "k03a": (["bohater_zmierzch.jpg"],
   SW + "Medium shot. " + TOMEK.format(n=1) +
   "He is secretly pulling a small flower pot with a young tomato seedling "
   "from inside his jacket, hunched, conspiratorial. Face and mouth clearly visible."),
 "k03b": (["bohater_zmierzch.jpg"],
   SW + "Medium close-up. " + TOMEK.format(n=1) +
   "He holds a small flower pot with a young tomato seedling at chest height "
   "and gives a questioning, bargaining look. Face and mouth clearly visible."),
 "k04a": (["janusz_zmierzch.jpg"],
   SW + "Medium shot. " + JANUSZ.format(n=1) +
   "He proudly reveals a small plastic bucket with a lid from behind his back, "
   "presenting it like contraband. Face and mouth clearly visible."),
 "k04b": (["janusz_zmierzch.jpg"],
   SW + "Close shot. " + JANUSZ.format(n=1) +
   "He slightly lifts the lid of the small bucket and grimaces with delight "
   "at the smell, comedic overacting. Face and mouth clearly visible."),
 "k04c": (["janusz_zmierzch.jpg"],
   SW + "Medium shot. " + JANUSZ.format(n=1) +
   "He leans in urgently holding the closed bucket with both hands, glancing "
   "over his shoulder as if the president might see them. Mouth clearly visible."),
 "k05": (["bohater_zmierzch.jpg", "janusz_zmierzch.jpg"],
   SW + "Medium shot, two men at the fence mid-exchange. " + TOMEK.format(n=1) +
   "He is taking the small bucket with one hand while handing over the flower "
   "pot with the tomato seedling with the other; his face and mouth clearly "
   "visible, he is the one about to speak. " + JANUSZ.format(n=2) +
   "He receives the pot, seen slightly from the side."),
 "k06": (["janusz_zmierzch.jpg"],
   SW + "Medium shot. " + JANUSZ.format(n=1) +
   "He tucks the small flower pot under his hoodie with a proud smirk, half "
   "turned on his heel as if about to vanish behind the bushes. Face and mouth "
   "clearly visible."),
}

def main():
    urls = {}
    bledy = 0
    for nazwa, (refy, prompt) in KADRY.items():
        out = OUT / f"{nazwa}.jpg"
        if out.exists():
            print(f"[kadry] {nazwa} istnieje, pomijam", flush=True)
            continue
        try:
            iu = []
            for r in refy:
                if r not in urls:
                    urls[r] = fal_client.upload_file(str(K / r))
                iu.append(urls[r])
            res = fal_client.run("fal-ai/nano-banana-pro/edit",
                arguments={"prompt": prompt, "image_urls": iu,
                           "aspect_ratio": "9:16", "resolution": "2K",
                           "safety_tolerance": 6},
                timeout=180, start_timeout=90)
            r = requests.get(res["images"][0]["url"], timeout=120)
            r.raise_for_status()
            out.write_bytes(r.content)
            print(f"[kadry] {nazwa} OK ({len(r.content)} B)", flush=True)
        except Exception as e:
            bledy += 1
            print(f"[kadry] {nazwa} BLAD: {e}", flush=True)
        time.sleep(2)
    print(f"[kadry] KONIEC, bledy: {bledy}", flush=True)
    sys.exit(1 if bledy else 0)

main()
