from PIL import Image, ImageOps
import glob, os
out = "/root/rod-ai-studio/data/filmy/kuny/male"
os.makedirs(out, exist_ok=True)
zrodla = sorted(glob.glob("/root/rod-ai-studio/data/filmy/kuny/wyciete/*_z1.jpg")) + \
         sorted(glob.glob("/root/rod-ai-studio/data/filmy/kuny/wyciete_drzewo/*_z1.jpg"))
for p in zrodla:
    im = Image.open(p).convert("L")
    im = ImageOps.autocontrast(im).resize((420, 420))
    n = os.path.join(out, os.path.basename(p).replace(".jpg", "_m.jpg"))
    im.save(n, quality=58, optimize=True)
    print(os.path.getsize(n), n)
