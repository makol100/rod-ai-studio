from PIL import Image, ImageOps
import glob, numpy as np, os
pliki = sorted(glob.glob("/root/rod-ai-studio/data/filmy/kuny/kot/k_*.jpg"))
sz = [np.asarray(Image.open(p).convert("L"), dtype=np.float32) for p in pliki]
tlo = np.median(np.stack([a - a.mean() for a in sz]), axis=0)
naj = None
for p, a in zip(pliki, sz):
    d = np.abs((a - a.mean()) - tlo); m = d > 30; n = int(m.sum())
    if 300 < n < 60000:
        ys, xs = np.where(m); cy, cx = int(np.median(ys)), int(np.median(xs))
        g = int(((np.abs(ys-cy)<120)&(np.abs(xs-cx)<120)).sum())
        if naj is None or g > naj[0]: naj = (g, p, cy, cx)
print("najlepsza:", naj[1] if naj else "brak", naj[0] if naj else "")
if naj:
    _, p, cy, cx = naj
    im = Image.open(p).convert("L")
    r = 165
    box = (max(0,cx-r), max(0,cy-r), min(im.width,cx+r), min(im.height,cy+r))
    zblizenie = ImageOps.autocontrast(im.crop(box)).resize((330,330))
    pelna = im.resize((330, int(330*im.height/im.width)))
    plansza = Image.new("L", (670, 340), 20)
    plansza.paste(pelna, (0, int((340-pelna.height)/2)))
    plansza.paste(zblizenie, (338, 5))
    out = "/root/rod-ai-studio/data/filmy/kuny/kot/kot_na_kosiarce.jpg"
    plansza.save(out, quality=46, optimize=True)
    print(os.path.getsize(out), out)
