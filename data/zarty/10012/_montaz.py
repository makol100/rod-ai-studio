# -*- coding: utf-8 -*-
"""Montaz 10012 Rezystancja Izolacji: trimy wg mowy, ASS, sklejka, huk korkow
na koncu k05, brand z 10008. Wzorzec: 10009/_montaz.py."""
import sys, json, subprocess
from pathlib import Path

B = Path('/root/rod-ai-studio/data/zarty/10012')
B8 = Path('/root/rod-ai-studio/data/zarty/10008')
S = json.load(open(B/'_stale.json'))
ASS_HEADER, KOLORY_ASS = S['ASS_HEADER'], S['KOLORY_ASS']
KOL = ['k01','k02','k03','k04','k05']
KONCE = json.load(open(B/'_konce.json'))

trimy = []
for k in KOL:
    if k in ('k01','k02','k05'):
        trimy.append(8.0)
    else:
        trimy.append(min(8.0, round(float(KONCE[k]) + 0.45, 2)))
(B/'trimy.txt').write_text(' '.join(map(str, trimy)))

kb = KOLORY_ASS['BOHATER']; kj = KOLORY_ASS['JANUSZ']; bialy = '&HFFFFFF&'
KW = {
 'k02': (kb, 'TOMEK: Janusz, badałeś ty kiedyś ciągłość przewodu ochronnego i rezystancję izolacji na tym kablu YKY?'),
 'k03': (kb, 'TOMEK: Przecież tu ci zaraz różnicówkę wywali w kosmos.'),
 'k04': (kj, 'JANUSZ: Panie, to ma prąd przewodzić, a nie mieć jakąś... rezystancję. Od 30 lat działa!'),
}

def czas(s):
    return f'{int(s//3600)}:{int(s%3600//60):02d}:{s%60:05.2f}'

linie = [(0.40, trimy[0]-0.30, bialy, 'Rezystancja izolacji...')]
off = 0.0
for k, t in zip(KOL, trimy):
    if k in KW:
        kolor, txt = KW[k]
        linie.append((off + 0.10, off + t - 0.05, kolor, txt))
    off += t

tresc = ''.join(f'Dialogue: 0,{czas(a)},{czas(b)},Default,,0,0,0,,{{\\c{kol}}}{t}\n'
                for a, b, kol, t in linie)
(B/'napisy12.ass').write_text(ASS_HEADER + tresc, encoding='utf-8')
print('trimy:', trimy, '| suma:', round(sum(trimy),1), 's | linii ASS:', len(linie), flush=True)

def ff(*args):
    r = subprocess.run(['ffmpeg','-y','-v','error',*args], capture_output=True, text=True)
    if r.returncode != 0:
        print('FFMPEG BLAD:', r.stderr[-500:], flush=True); sys.exit(1)

czesci = []
for k, t in zip(KOL, trimy):
    o = B/f'trim_{k}.mp4'
    ff('-i', str(B/f'{k}.mp4'), '-t', str(t),
       '-vf','scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=24',
       '-r','24','-c:v','libx264','-preset','fast','-crf','19',
       '-c:a','aac','-ar','48000','-ac','2', str(o))
    czesci.append(o)
(B/'concat.txt').write_text('\n'.join(f"file '{c}'" for c in czesci))
ff('-f','concat','-safe','0','-i', str(B/'concat.txt'), '-c','copy', str(B/'sklejka.mp4'))
print('sklejka OK', flush=True)

ff('-i', str(B/'sklejka.mp4'), '-vf', f"ass={B/'napisy12.ass'}",
   '-c:v','libx264','-preset','fast','-crf','19','-c:a','copy', str(B/'z_napisami.mp4'))
print('napisy OK', flush=True)

start_huk = round(sum(trimy) - 0.30, 2)
ff('-i', str(B/'z_napisami.mp4'), '-i', str(B/'huk.wav'),
   '-filter_complex', f'[1:a]adelay={int(start_huk*1000)}|{int(start_huk*1000)},volume=0.9[w];[0:a][w]amix=inputs=2:duration=first:normalize=0[a]',
   '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac', str(B/'z_hukiem.mp4'))
print('huk OK @', start_huk, flush=True)

for f in ('intro_a.mp4','outro_a.mp4','plansza_ai.mp4'):
    if not (B/f).exists():
        subprocess.run(['cp', str(B8/f), str(B/f)], check=True)
(B/'concat_final.txt').write_text('\n'.join(f"file '{B/f}'" for f in
    ('intro_a.mp4','z_hukiem.mp4','outro_a.mp4','plansza_ai.mp4')))
ff('-f','concat','-safe','0','-i', str(B/'concat_final.txt'),
   '-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-ar','48000', str(B/'final.mp4'))
print('FINAL OK', flush=True)
