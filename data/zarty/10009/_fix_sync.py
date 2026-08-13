# -*- coding: utf-8 -*-
"""FIX LIP-SYNC 10009 ($0): przyczyna rozjazdu 2.25s = concat materialow o roznym
fps (body 24, intro/outro 30, plansza 25). Normalizujemy brand do parametrow body
(24fps, 1080x1920, aac 48k stereo), potem concat -c copy jak przy sklejce."""
import subprocess, sys, json
from pathlib import Path

B = Path('/root/rod-ai-studio/data/zarty/10009')

def ff(*a):
    r = subprocess.run(['ffmpeg','-y','-v','error',*a], capture_output=True, text=True)
    if r.returncode != 0:
        print('FFMPEG BLAD:', r.stderr[-400:], flush=True); sys.exit(1)

def probe(p, strumien):
    r = subprocess.run(['ffprobe','-v','error','-select_streams', strumien,
        '-show_entries','stream=duration','-of','csv=p=0', str(p)],
        capture_output=True, text=True)
    v = r.stdout.strip().split('\n')[0]
    return float(v) if v and v != 'N/A' else None

# 1. normalizacja brandu do parametrow body
for f in ('intro_a.mp4','outro_a.mp4','plansza_ai.mp4'):
    src = B/f; out = B/f'n_{f}'
    ma_audio = probe(src, 'a:0') is not None
    if ma_audio:
        ff('-i', str(src),
           '-vf','scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=24',
           '-r','24','-c:v','libx264','-preset','fast','-crf','19',
           '-c:a','aac','-ar','48000','-ac','2', str(out))
    else:  # brak audio -> dokladamy cisze, inaczej concat rozjedzie timeline
        ff('-i', str(src), '-f','lavfi','-i','anullsrc=r=48000:cl=stereo',
           '-vf','scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=24',
           '-r','24','-c:v','libx264','-preset','fast','-crf','19',
           '-c:a','aac','-ar','48000','-ac','2','-shortest', str(out))
    print(f'  {f}: audio_wejscie={ma_audio} -> n_{f} '
          f'v={probe(out,"v:0"):.2f}s a={probe(out,"a:0"):.2f}s', flush=True)

# 2. sklejka bez przekodowania (parametry identyczne)
lista = ['n_intro_a.mp4','z_werblem.mp4','n_outro_a.mp4','n_plansza_ai.mp4']
(B/'concat_final.txt').write_text('\n'.join(f"file '{B/f}'" for f in lista))
ff('-f','concat','-safe','0','-i', str(B/'concat_final.txt'), '-c','copy', str(B/'final_v4.mp4'))

# 3. bramka: obraz i dzwiek musza sie zgadzac
v, a = probe(B/'final_v4.mp4','v:0'), probe(B/'final_v4.mp4','a:0')
delta = abs(v - a)
print(f'FINAL v4: wideo {v:.3f}s | audio {a:.3f}s | rozjazd {delta:.3f}s', flush=True)
print('BRAMKA:', 'PASS (<0.05s)' if delta < 0.05 else f'FAIL — nadal rozjazd', flush=True)
sys.exit(0 if delta < 0.05 else 1)
