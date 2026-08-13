# -*- coding: utf-8 -*-
"""FIX NAPISOW 10009: podzial fraz po INTERPUNKCJI (nie co 4 slowa na slepo),
zero nachodzenia linii. Reszta (grading, klipy) bez zmian - skladam z gr_*.mp4."""
import sys, json, subprocess, re
sys.path.insert(0, '/app')
from pathlib import Path
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

KONIEC_FRAZY = re.compile(r'[.!?…,]["\u201d\u201e]?$')

def frazy(kanon, slowa, trim):
    sl = [w for w in slowa if w[1] < trim - 0.05]
    if not sl:
        return []
    kw = kanon.split()
    if len(kw) == len(sl):
        pary = [[kw[i], sl[i][1], min(sl[i][2], trim - 0.10)] for i in range(len(kw))]
    else:
        t0, t1 = sl[0][1], min(sl[-1][2], trim - 0.10)
        dl = [len(w) for w in kw]; suma = sum(dl); pary = []; t = t0
        for w, d in zip(kw, dl):
            dt = (t1 - t0) * d / suma
            pary.append([w, round(t, 2), round(t + dt, 2)]); t += dt
    # 1) tnij po interpunkcji lub gdy fraza urosla do 6 slow
    grupy = []; buf = None
    for w, a, b in pary:
        if buf is None:
            buf = [w, a, b, 1]
        else:
            buf[0] += ' ' + w; buf[2] = b; buf[3] += 1
        if KONIEC_FRAZY.search(w) or buf[3] >= 6:
            grupy.append(buf); buf = None
    if buf:
        grupy.append(buf)
    # 2) doklej ogarki (1 slowo) do sasiada
    scalone = []
    for g in grupy:
        if scalone and (g[3] == 1 or scalone[-1][3] == 1) and scalone[-1][3] + g[3] <= 7:
            p = scalone[-1]
            p[0] += ' ' + g[0]; p[2] = g[2]; p[3] += g[3]
        else:
            scalone.append(g)
    return [(g[0], g[1], g[2]) for g in scalone]

linie = [(0.40, trimy[0]-0.30, bialy, 'Prawdziwy czarny rynek istnieje tylko na działkach...')]
off = 0.0
for k, t in zip(KOL, trimy):
    if k in KW:
        kolor, kanon = KW[k]
        fr = frazy(kanon, SLOWA[k], t)
        for i, (txt, a, b) in enumerate(fr):
            nast = off + fr[i+1][1] - 0.05 if i + 1 < len(fr) else off + t - 0.05
            koniec = min(off + b + 0.20, nast, off + t - 0.05)
            linie.append((off + a, koniec, kolor, txt))
    off += t

tresc = ''.join(f'Dialogue: 0,{czas(a)},{czas(b)},Default,,0,0,0,,{{\\c{kol}}}{t}\n'
                for a, b, kol, t in linie)
(B/'napisy9.ass').write_text(ASS_HEADER + tresc, encoding='utf-8')
print(f'linii ASS: {len(linie)}', flush=True)
for a, b, kol, t in linie:
    print(f'  {a:6.2f}-{b:6.2f}  {t}', flush=True)

def ff(*a):
    r = subprocess.run(['ffmpeg','-y','-v','error',*a], capture_output=True, text=True)
    if r.returncode != 0:
        print('FFMPEG BLAD:', r.stderr[-400:], flush=True); sys.exit(1)

ff('-i', str(B/'sklejka.mp4'), '-vf', f"ass={B/'napisy9.ass'}",
   '-c:v','libx264','-preset','fast','-crf','19','-c:a','copy', str(B/'z_napisami.mp4'))
start_k06 = round(sum(trimy[:-1]), 2)
ff('-i', str(B/'z_napisami.mp4'), '-i', str(B8/'hit.wav'),
   '-filter_complex', f'[1:a]adelay={int(start_k06*1000)}|{int(start_k06*1000)},volume=0.9[w];[0:a][w]amix=inputs=2:duration=first:normalize=0[a]',
   '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac', str(B/'z_werblem.mp4'))
(B/'concat_final.txt').write_text('\n'.join(f"file '{B/f}'" for f in
    ('intro_a.mp4','z_werblem.mp4','outro_a.mp4','plansza_ai.mp4')))
ff('-f','concat','-safe','0','-i', str(B/'concat_final.txt'),
   '-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-ar','48000', str(B/'final_v3.mp4'))
print('FINAL v3 OK', flush=True)
