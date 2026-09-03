"""Kadry 10012 'Rezystancja Izolacji' (5 szt.) — nano-banana-pro/edit, refy dzienne _baza.
Zgoda: dekret 27.08 'Wszyscy do dziela' (D-0171). ~$0.75. Zapis: data/zarty/10012/kadry/"""
import sys, time
from pathlib import Path
import requests, fal_client

K = Path("/root/rod-ai-studio/assets/zarty/karty")
OUT = Path("/root/rod-ai-studio/data/zarty/10012/kadry"); OUT.mkdir(exist_ok=True)

SW = ("Bright sunny summer day in a lush Polish allotment garden, next to a "
      "rickety old lawnmower by a wooden garden shed, vivid natural daylight. "
      "Photorealistic, natural documentary photography, vertical 9:16 "
      "composition. No captions, no text anywhere. ")
TOMEK = ("The man from reference image {n} - identity lock: exactly the same "
         "eyes, nose, jawline and facial proportions - long ponytail, full "
         "salt-and-pepper beard, wearing a black t-shirt. A rugged professional "
         "industrial multimeter hangs on a strap around his neck: bright yellow "
         "rubberized protective holster, dark grey front panel, large digital "
         "LCD screen, big rotary range selector dial, test lead sockets - "
         "high-end electrician equipment, plain, no logo, no text on it. ")
JANUSZ = ("The tall thin man in his mid-sixties from reference image {n} - "
          "identity lock: exactly the same eyes, nose, jawline and facial "
          "proportions - grey mustache, reading glasses on a cord, wearing a "
          "beige multi-pocket vest. ")

KADRY = {
 "k01": (["janusz_baza.jpg"],
   SW + "Wide shot showing the whole scene. " + JANUSZ.format(n=1) +
   "He crouches beside the rickety old lawnmower, both hands on a frayed, "
   "cracked old extension cord half-wrapped in grey electrical tape, mid-wrap. "
   "Hands visible but not in close-up. Visible cracks on the cord."),
 "k02": (["bohater_baza.jpg"],
   SW + "Medium shot. " + TOMEK.format(n=1) +
   "He has just stepped into frame and looks down at the taped cord with "
   "grave, exaggerated professional seriousness. Face and mouth clearly visible."),
 "k03": (["bohater_baza.jpg"],
   SW + "Medium shot. " + TOMEK.format(n=1) +
   "He points with concern toward the old lawnmower, lecturing pose. "
   "Face and mouth clearly visible."),
 "k04": (["janusz_baza.jpg"],
   SW + "Medium close-up. " + JANUSZ.format(n=1) +
   "He stands upright holding the taped extension cord, staring at someone "
   "off-frame as if they were speaking a foreign language, head slightly "
   "turned over his shoulder, dismissive squint. Face and mouth clearly visible."),
 "k05": (["janusz_baza.jpg"],
   SW + "Full wide shot, whole body visible. " + JANUSZ.format(n=1) +
   "He confidently plugs the taped extension cord into an outdoor power "
   "socket mounted on a wooden post beside the lawnmower, arm extended, "
   "seen from the side."),
}

def main():
    urls = {}; bledy = 0
    for nazwa, (refy, prompt) in KADRY.items():
        out = OUT / f"{nazwa}.jpg"
        if out.exists():
            print(f"[kadry] {nazwa} istnieje, pomijam", flush=True); continue
        try:
            iu = []
            for r in refy:
                if r not in urls: urls[r] = fal_client.upload_file(str(K / r))
                iu.append(urls[r])
            res = fal_client.run("fal-ai/nano-banana-pro/edit",
                arguments={"prompt": prompt, "image_urls": iu,
                           "aspect_ratio": "9:16", "resolution": "2K",
                           "safety_tolerance": 6},
                timeout=180, start_timeout=90)
            r = requests.get(res["images"][0]["url"], timeout=120)
            r.raise_for_status(); out.write_bytes(r.content)
            print(f"[kadry] {nazwa} OK ({len(r.content)} B)", flush=True)
        except Exception as e:
            bledy += 1; print(f"[kadry] {nazwa} BLAD: {e}", flush=True)
        time.sleep(2)
    print(f"[kadry] KONIEC, bledy: {bledy}", flush=True)
    sys.exit(1 if bledy else 0)

if __name__ == "__main__":
    main()
