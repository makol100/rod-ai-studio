#!/usr/bin/env python3
"""Maska wideo (0 zl): BIALE = wszystko NAD gorna krawedzia plytek (sciana surowa + sufit), CZARNE = plytki/miska/podloga.
Linia plytek mierzona kolumnami na kazdej klatce (plytki = jasne bezowe R>G), luki interpolowane, wygladzenie w czasie (mediana 5 klatek).
Opcjonalnie OR z maska SAM2. Uzycie: maska_plytki.py wejscie.mp4 wyjscie_maska.mp4 [sam.mp4]"""
import sys, subprocess, numpy as np, tempfile, os
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]; sam = sys.argv[3] if len(sys.argv) > 3 else None
tmp = tempfile.mkdtemp(); subprocess.run(['ffmpeg','-v','error','-y','-i',src,f'{tmp}/f%04d.png'],check=True)
files = sorted(f for f in os.listdir(tmp) if f.startswith('f')); N = len(files)
samf = []
if sam:
    st = tempfile.mkdtemp(); subprocess.run(['ffmpeg','-v','error','-y','-i',sam,f'{st}/s%04d.png'],check=True); samf = sorted(os.path.join(st,f) for f in os.listdir(st))
im0 = np.asarray(Image.open(f'{tmp}/{files[0]}').convert('RGB')); H, W, _ = im0.shape
KROK = 8; xs = list(range(KROK//2, W, KROK)); linie = np.full((N, len(xs)), np.nan)
def granica(kol):
    # od gory w dol: pierwszy rzad plytek = jasny bezowy (R>165, R>G+3) poprzedzony ciemniejszym pasem
    for y in range(24, int(H*0.8)):
        r,g,b = kol[y]
        if r > 165 and r > g + 3 and (kol[y-16][0] < r - 22 or kol[y-16][1] > kol[y-16][0] - 2 and kol[y-16][0] < 150): return y
    return np.nan
for i, f in enumerate(files):
    im = np.asarray(Image.open(f'{tmp}/{f}').convert('RGB')).astype(float)
    for j, x in enumerate(xs):
        linie[i, j] = granica(im[:, max(0,x-3):x+4].mean(1))
# interpolacja luk w przestrzeni (po kolumnach) i czasie
for i in range(N):
    row = linie[i]; ok = ~np.isnan(row)
    if ok.sum() >= 3: row[~ok] = np.interp(np.array(xs)[~ok], np.array(xs)[ok], row[ok]); linie[i] = row
for j in range(len(xs)):
    col = linie[:, j]; ok = ~np.isnan(col)
    if ok.sum() >= 2: col[~ok] = np.interp(np.arange(N)[~ok], np.arange(N)[ok], col[ok]); linie[:, j] = col
linie = np.nan_to_num(linie, nan=H*0.25)
# wygladzenie w czasie (mediana 5) i w przestrzeni (srednia 3)
from scipy.ndimage import median_filter, uniform_filter1d
linie = median_filter(linie, size=(5,1)); linie = uniform_filter1d(linie, size=3, axis=1)
out = tempfile.mkdtemp()
for i in range(N):
    m = np.zeros((H, W), np.uint8)
    yl = np.interp(np.arange(W), xs, linie[i])
    for x in range(W): m[:max(0,int(yl[x])-6), x] = 255   # 6 px marginesu nad plytkami
    if samf and i < len(samf):
        s = np.asarray(Image.open(samf[i]).convert('L').resize((W,H))) > 127; m[s] = 255
    Image.fromarray(m).save(f'{out}/m{i:04d}.png')
subprocess.run(['ffmpeg','-v','error','-y','-framerate','16','-i',f'{out}/m%04d.png','-vf','gblur=sigma=2','-c:v','libx264','-crf','12','-pix_fmt','yuv420p',dst],check=True)
print('maska:', dst, N, 'klatek', W, 'x', H)
