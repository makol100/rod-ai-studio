from PIL import Image, ImageOps
import glob, os, numpy as np
out = "/root/rod-ai-studio/data/filmy/kuny/seria"
os.makedirs(out, exist_ok=True)
for f in glob.glob(out+"/*.jpg"): os.remove(f)

def analiza(pref, katalog):
    pliki = sorted(glob.glob(f"{katalog}/{pref}_*.jpg"))
    if len(pliki) < 3: return
    szare = [np.asarray(Image.open(p).convert("L"), dtype=np.float32) for p in pliki]
    szare = [a - a.mean() for a in szare]
    naj = None
    for i in range(1, len(pliki)):
        d = np.abs(szare[i] - szare[i-1]); m = d > 26; n = int(m.sum())
        if 250 < n < 45000:
            ys, xs = np.where(m)
            cy, cx = int(np.median(ys)), int(np.median(xs))
            g = int(((np.abs(ys-cy) < 140) & (np.abs(xs-cx) < 140)).sum())
            if naj is None or g > naj[0]: naj = (g, i, cy, cx)
    if not naj: return
    g, i, cy, cx = naj
    # siatka 2x2 z 4 kolejnych klatek wokol zdarzenia, wyciete i wyostrzone
    idx = [max(0,i-1), i, min(len(pliki)-1,i+1), min(len(pliki)-1,i+2)]
    r = 210
    plansza = Image.new("L", (760, 760))
    for k, j in enumerate(idx):
        im = Image.open(pliki[j]).convert("L")
        box = (max(0,cx-r), max(0,cy-r), min(im.width,cx+r), min(im.height,cy+r))
        kadr = ImageOps.autocontrast(im.crop(box)).resize((375, 375))
        plansza.paste(kadr, ((k%2)*380, (k//2)*380))
    n = f"{out}/{pref}_seria.jpg"
    plansza.save(n, quality=62, optimize=True)
    print(os.path.getsize(n), n)

for p in ["noc_0125","noc_0244","noc_0352","noc_0438"]:
    analiza(p, "/root/rod-ai-studio/data/filmy/kuny/gęste")
for p in ["drzewo_06_0300","drzewo_11_0040"]:
    analiza(p, "/root/rod-ai-studio/data/filmy/kuny/gęste_drzewo")
