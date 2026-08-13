# -*- coding: utf-8 -*-
"""NAPRAWA 10009 (darmowa, bez fal):
(1) NAPISY FRAZOWE zsynchronizowane z mowa (timingi slow z Whispera, TEKST
    kanonu podstawiony) zamiast jednego bloku wiszacego caly klip.
(2) GRADING: wyrownanie temperatury barwowej i jasnosci wszystkich klipow
    do wspolnego punktu (zmierzch), zeby ciecia nie skakaly."""
import sys, json, subprocess
sys.path.insert(0, '/app')
from pathlib import Path
import cv2, numpy as np
from src.zarty_produkcja import ASS_HEADER, KOLORY_ASS

B = Path('/root/rod-ai-studio/data/zarty/10009')
B8 = Path('/root/rod-ai-studio/data/zarty/10008')
KOL = ['k01','k02','k03a','k03b','k04a','k04b','k04c','k05','k06']
KONCE = json.load(open(B/'_konce.json'))
SLOWA = json.load(open(B/'_slowa.json'))

trimy = []
for k in KOL:
    zapas = 0.5 if k == 'k01' else (0.35 if k == 'k04b' else 0.45)
    trimy.append(min(8.0, round(float(KONCE[k]) + zapas, 2)))

kb = KOLORY_ASS['BOHATER']; kj = KOLORY_ASS['JANUSZ']; bialy = '&HFFFFFF&'
KW = {
 'k02': (kj, 'Pssst... Masz towar? Pytam o te sadzonki pomidorów z czarnego rynku, te co szwagier z Holandii przywiózł.'),
 'k03a': (kb, 'Mam. Odmiana „Czarny Książę". Słodkie jak miód, odporne na zarazę ziemniaczaną.'),
 'k03b': (kb, 'Ale co masz dla mnie w zamian? Miała być czysta, naturalna waluta.'),
 'k04a': (kj, 'Prosto od rolnika spod Grójca. Trzyletni, przekompostowany obornik koński.'),
 'k04b': (kj, 'Żadnej chemii, sam czysty azot. Twoje ogórki po tym wystrzelą w kosmos.'),
 'k04c': (kj, 'Bierz, zanim prezes zauważy, bo oficjalnie w tym tygodniu jest zakaz wwożenia gabarytów na alejki.'),
 'k05': (kb, 'Dobry towar. Umowa stoi. Tylko nikomu ani słowa, zwłaszcza tej sąsiadce z naprzeciwka.'),
 'k06': (kj, 'Grażyna? Ona sypie sztuczny nawóz z marketu, amatorka... Nie zna życia. Do następnego, młody.'),
}

def czas(s):
    s = max(s, 0)
    return f'{int(s//3600)}:{int(s%3600//60):02d}:{s%60:05.2f}'

def frazy(kanon, slowa, trim):
    """Slowa kanonu na osi czasu mowy; grupy <=4 slowa / <=2.2s."""
    sl = [w for w in slowa if w[1] < trim - 0.05]
    if not sl:
        return []
    t0, t1 = sl[0][1], min(sl[-1][2], trim - 0.10)
    kw = kanon.split()
    if len(kw) == len(sl):
        pary = [(kw[i], sl[i][1], min(sl[i][2], trim - 0.10)) for i in range(len(kw))]
    else:  # proporcjonalnie wg dlugosci slow
        dl = [len(w) for w in kw]; suma = sum(dl); pary = []; t = t0
        for w, d in zip(kw, dl):
            dt = (t1 - t0) * d / suma
            pary.append((w, round(t, 2), round(t + dt, 2))); t += dt
    grupy = []; buf = []
    for w, a, b in pary:
        if not buf:
            buf = [w, a, b]; continue
        if len(buf[0].split()) >= 4 or (b - buf[1]) > 2.2:
            grupy.append(tuple(buf)); buf = [w, a, b]
        else:
            buf[0] += ' ' + w; buf[2] = b
    if buf:
        grupy.append(tuple(buf))
    return grupy

linie = [(0.40, trimy[0]-0.30, bialy, 'Prawdziwy czarny rynek istnieje tylko na działkach...')]
off = 0.0
for k, t in zip(KOL, trimy):
    if k in KW:
        kolor, kanon = KW[k]
        for txt, a, b in frazy(kanon, SLOWA[k], t):
            linie.append((off + a, off + min(b + 0.15, t), kolor, txt))
    off += t

tresc = ''.join(f'Dialogue: 0,{czas(a)},{czas(b)},Default,,0,0,0,,{{\\c{kol}}}{t}\n'
                for a, b, kol, t in linie)
(B/'napisy9.ass').write_text(ASS_HEADER + tresc, encoding='utf-8')
print('linii ASS:', len(linie), '(bylo 9 blokow)', flush=True)

# --- GRADING: pomiar i wyrownanie ---
def pomiar(p):
    cap = cv2.VideoCapture(str(p)); cap.set(cv2.CAP_PROP_POS_FRAMES, 24)
    ok, img = cap.read(); cap.release()
    b, g, r = [float(np.mean(img[:, :, i])) for i in range(3)]
    y = float(np.mean(cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:, :, 2]))
    return b, g, r, y

P = {k: pomiar(B/f'klip_{k}.mp4') for k in KOL}
tb = float(np.median([p[0] for p in P.values()]))
tg = float(np.median([p[1] for p in P.values()]))
tr = float(np.median([p[2] for p in P.values()]))
ty = float(np.median([p[3] for p in P.values()]))
print(f'cel: B={tb:.1f} G={tg:.1f} R={tr:.1f} Y={ty:.1f}', flush=True)

def ff(*a):
    r = subprocess.run(['ffmpeg','-y','-v','error',*a], capture_output=True, text=True)
    if r.returncode != 0:
        print('FFMPEG BLAD:', r.stderr[-400:], flush=True); sys.exit(1)

czesci = []
for k, t in zip(KOL, trimy):
    b, g, r, y = P[k]
    kb_, kg_, kr_ = [min(max(tb/b, 0.85), 1.18), min(max(tg/g, 0.85), 1.18), min(max(tr/r, 0.85), 1.18)]
    jasn = min(max((ty - y) / 255.0, -0.06), 0.06)
    o = B/f'gr_{k}.mp4'
    ff('-i', str(B/f'klip_{k}.mp4'), '-t', str(t),
       '-vf', (f'colorchannelmixer={kr_:.3f}:0:0:0:0:{kg_:.3f}:0:0:0:0:{kb_:.3f}:0,'
               f'eq=brightness={jasn:.3f}:saturation=1.02,'
               'scale=1080:1920:force_original_aspect_ratio=decrease,'
               'pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=24'),
       '-r','24','-c:v','libx264','-preset','fast','-crf','19',
       '-c:a','aac','-ar','48000','-ac','2', str(o))
    print(f'  grade {k}: R×{kr_:.2f} G×{kg_:.2f} B×{kb_:.2f} jasn{jasn:+.3f}', flush=True)
    czesci.append(o)

(B/'concat.txt').write_text('\n'.join(f"file '{c}'" for c in czesci))
ff('-f','concat','-safe','0','-i', str(B/'concat.txt'), '-c','copy', str(B/'sklejka.mp4'))
ff('-i', str(B/'sklejka.mp4'), '-vf', f"ass={B/'napisy9.ass'}",
   '-c:v','libx264','-preset','fast','-crf','19','-c:a','copy', str(B/'z_napisami.mp4'))
start_k06 = round(sum(trimy[:-1]), 2)
ff('-i', str(B/'z_napisami.mp4'), '-i', str(B8/'hit.wav'),
   '-filter_complex', f'[1:a]adelay={int(start_k06*1000)}|{int(start_k06*1000)},volume=0.9[w];[0:a][w]amix=inputs=2:duration=first:normalize=0[a]',
   '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac', str(B/'z_werblem.mp4'))
(B/'concat_final.txt').write_text('\n'.join(f"file '{B/f}'" for f in
    ('intro_a.mp4','z_werblem.mp4','outro_a.mp4','plansza_ai.mp4')))
ff('-f','concat','-safe','0','-i', str(B/'concat_final.txt'),
   '-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-ar','48000', str(B/'final_v2.mp4'))
print('FINAL v2 OK', flush=True)
