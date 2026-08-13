from PIL import Image, ImageOps
import glob, os, numpy as np
G = "/root/rod-ai-studio/data/filmy/kuny"
def najlepszy(pref, kat):
    pliki = sorted(glob.glob(f"{kat}/{pref}_*.jpg"))
    if len(pliki) < 3: return None
    sz = [np.asarray(Image.open(p).convert("L"), dtype=np.float32) for p in pliki]
    sz = [a - a.mean() for a in sz]
    naj = None
    for i in range(1, len(pliki)):
        d = np.abs(sz[i]-sz[i-1]); m = d > 26; n = int(m.sum())
        if 250 < n < 45000:
            ys, xs = np.where(m); cy, cx = int(np.median(ys)), int(np.median(xs))
            g = int(((np.abs(ys-cy)<140)&(np.abs(xs-cx)<140)).sum())
            if naj is None or g > naj[0]: naj = (g, pliki[i], cy, cx)
    return naj
zest = [("noc_0125", G+"/gęste"), ("noc_0244", G+"/gęste"), ("noc_0352", G+"/gęste"), ("noc_0438", G+"/gęste")]
plansza = Image.new("L", (500, 500), 0)
for k, (pref, kat) in enumerate(zest):
    n = najlepszy(pref, kat)
    if not n: continue
    _, p, cy, cx = n
    im = Image.open(p).convert("L"); r = 175
    box = (max(0,cx-r), max(0,cy-r), min(im.width,cx+r), min(im.height,cy+r))
    kadr = ImageOps.autocontrast(im.crop(box)).resize((245,245))
    plansza.paste(kadr, ((k%2)*250, (k//2)*250))
out = G+"/plansza_mala.jpg"
plansza.save(out, quality=42, optimize=True)
print(os.path.getsize(out), out)
