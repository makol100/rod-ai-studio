import glob, os
import numpy as np
from PIL import Image
OUT = "/root/rod-ai-studio/data/filmy/kuny/wyciete_drzewo"
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(OUT + "/*.jpg"): os.remove(f)

for pref in ["drzewo_05_2209","drzewo_06_0300","drzewo_09_2150","drzewo_11_0040"]:
    pliki = sorted(glob.glob(f"/root/rod-ai-studio/data/filmy/kuny/gęste_drzewo/{pref}_*.jpg"))
    if len(pliki) < 3: continue
    kand = []
    prev = None; prev_p = None
    for p in pliki:
        a = np.asarray(Image.open(p).convert("L"), dtype=np.float32)
        a = a - a.mean()                      # wyrownanie jasnosci (IR wl/wyl)
        if prev is not None:
            d = np.abs(a - prev)
            maska = d > 26
            n = int(maska.sum())
            if 250 < n < 45000:               # LOKALNA zmiana = zwierze, nie caly kadr
                ys, xs = np.where(maska)
                # najgestsze skupisko
                cy, cx = int(np.median(ys)), int(np.median(xs))
                blisko = (np.abs(ys-cy) < 140) & (np.abs(xs-cx) < 140)
                gestosc = int(blisko.sum())
                kand.append((gestosc, n, p, cy, cx))
        prev = a; prev_p = p
    kand.sort(key=lambda x: -x[0])
    for i, (g, n, p, cy, cx) in enumerate(kand[:3]):
        im = Image.open(p)
        r = 190
        box = (max(0,cx-r), max(0,cy-r), min(im.width,cx+r), min(im.height,cy+r))
        im.crop(box).resize((768,768)).save(f"{OUT}/{pref}_z{i+1}.jpg", quality=93)
        print(f"{pref}: {os.path.basename(p)} skupisko={g}px zmiana={n}px srodek=({cx},{cy})")
