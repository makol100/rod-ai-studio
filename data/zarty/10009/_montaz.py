# -*- coding: utf-8 -*-
"""Montaz 10009 Dzialkowy czarny rynek: trimy wg mowy, ASS, sklejka, werbel,
brand z 10008. Wzorzec: 10008/montaz.py + lancuch plikow sklejka->final."""
import sys, json, subprocess
sys.path.insert(0, '/app')
from pathlib import Path
from src.zarty_produkcja import ASS_HEADER, KOLORY_ASS

B = Path('/root/rod-ai-studio/data/zarty/10009')
B8 = Path('/root/rod-ai-studio/data/zarty/10008')
KOL = ['k01','k02','k03a','k03b','k04a','k04b','k04c','k05','k06']
KONCE = json.load(open(B/'_konce.json'))

trimy = []
for k in KOL:
    zapas = 0.5 if k == 'k01' else (0.35 if k == 'k04b' else 0.45)
    trimy.append(min(8.0, round(float(KONCE[k]) + zapas, 2)))
(B/'trimy.txt').write_text(' '.join(map(str, trimy)))

kb = KOLORY_ASS['BOHATER']; kj = KOLORY_ASS['JANUSZ']; bialy = '&HFFFFFF&'
KW = {
 'k02': (kj, 'JANUSZ: Pssst... Masz towar? Pytam o te sadzonki pomidorów z czarnego rynku, te co szwagier z Holandii przywiózł.'),
 'k03a': (kb, 'TOMEK: Mam. Odmiana „Czarny Książę". Słodkie jak miód, odporne na zarazę ziemniaczaną.'),
 'k03b': (kb, 'TOMEK: Ale co masz dla mnie w zamian? Miała być czysta, naturalna waluta.'),
 'k04a': (kj, 'JANUSZ: Prosto od rolnika spod Grójca. Trzyletni, przekompostowany obornik koński.'),
 'k04b': (kj, 'JANUSZ: Żadnej chemii, sam czysty azot. Twoje ogórki po tym wystrzelą w kosmos.'),
 'k04c': (kj, 'JANUSZ: Bierz, zanim prezes zauważy, bo oficjalnie w tym tygodniu jest zakaz wwożenia gabarytów na alejki.'),
 'k05': (kb, 'TOMEK: Dobry towar. Umowa stoi. Tylko nikomu ani słowa, zwłaszcza tej sąsiadce z naprzeciwka.'),
 'k06': (kj, 'JANUSZ: Grażyna? Ona sypie sztuczny nawóz z marketu, amatorka... Nie zna życia. Do następnego, młody.'),
}

def czas(s):
    return f'{int(s//3600)}:{int(s%3600//60):02d}:{s%60:05.2f}'

linie = [(0.40, trimy[0]-0.30, bialy, 'Prawdziwy czarny rynek istnieje tylko na działkach...')]
off = 0.0
for k, t in zip(KOL, trimy):
    if k in KW:
        kolor, txt = KW[k]
        linie.append((off + 0.10, off + t - 0.05, kolor, txt))
    off += t

tresc = ''.join(f'Dialogue: 0,{czas(a)},{czas(b)},Default,,0,0,0,,{{\\c{kol}}}{t}\n'
                for a, b, kol, t in linie)
(B/'napisy9.ass').write_text(ASS_HEADER + tresc, encoding='utf-8')
print('trimy:', trimy, '| suma:', round(sum(trimy),1), 's | linii ASS:', len(linie), flush=True)

def ff(*args):
    r = subprocess.run(['ffmpeg','-y','-v','error',*args], capture_output=True, text=True)
    if r.returncode != 0:
        print('FFMPEG BLAD:', r.stderr[-500:], flush=True); sys.exit(1)

# 1. trim + normalizacja + concat
czesci = []
for k, t in zip(KOL, trimy):
    o = B/f'trim_{k}.mp4'
    ff('-i', str(B/f'klip_{k}.mp4'), '-t', str(t),
       '-vf','scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=24',
       '-r','24','-c:v','libx264','-preset','fast','-crf','19',
       '-c:a','aac','-ar','48000','-ac','2', str(o))
    czesci.append(o)
(B/'concat.txt').write_text('\n'.join(f"file '{c}'" for c in czesci))
ff('-f','concat','-safe','0','-i', str(B/'concat.txt'), '-c','copy', str(B/'sklejka.mp4'))
print('sklejka OK', flush=True)

# 2. napisy
ff('-i', str(B/'sklejka.mp4'), '-vf', f"ass={B/'napisy9.ass'}",
   '-c:v','libx264','-preset','fast','-crf','19','-c:a','copy', str(B/'z_napisami.mp4'))
print('napisy OK', flush=True)

# 3. werbel na puencie (poczatek k06)
start_k06 = round(sum(trimy[:-1]), 2)
ff('-i', str(B/'z_napisami.mp4'), '-i', str(B8/'hit.wav'),
   '-filter_complex', f'[1:a]adelay={int(start_k06*1000)}|{int(start_k06*1000)},volume=0.9[w];[0:a][w]amix=inputs=2:duration=first:normalize=0[a]',
   '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac', str(B/'z_werblem.mp4'))
print('werbel OK @', start_k06, flush=True)

# 4. brand: intro + korpus + outro + plansza AI (kopiowane z 10008 — wspolny brand serii)
for f in ('intro_a.mp4','outro_a.mp4','plansza_ai.mp4'):
    if not (B/f).exists():
        subprocess.run(['cp', str(B8/f), str(B/f)], check=True)
(B/'concat_final.txt').write_text('\n'.join(f"file '{B/f}'" for f in
    ('intro_a.mp4','z_werblem.mp4','outro_a.mp4','plansza_ai.mp4')))
ff('-f','concat','-safe','0','-i', str(B/'concat_final.txt'),
   '-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-ar','48000', str(B/'final.mp4'))
print('FINAL OK', flush=True)
