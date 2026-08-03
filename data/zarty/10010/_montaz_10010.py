# -*- coding: utf-8 -*-
"""Montaz 10010 'Kiedy zlapiesz zlodzieja jablek' wg ARCHITEKTURA KOMIZMU v1.1."""
import subprocess, sys
sys.path.insert(0, '/app')
from pathlib import Path
from src.zarty_produkcja import ASS_HEADER, KOLORY_ASS

B = Path('/root/rod-ai-studio/data/zarty/10010')
T = B / 'montaz_tmp'; T.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 24
VIDEO = ['-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r',str(FPS),'-s',f'{W}x{H}']
AUDIO = ['-c:a','aac','-b:a','192k','-ar','48000','-ac','2']

def run(args):
    r = subprocess.run(['ffmpeg','-y','-loglevel','error']+args, capture_output=True, text=True)
    if r.returncode != 0:
        print('FFMPEG FAIL:', ' '.join(map(str,args))[:300], '\n', r.stderr[-600:]); sys.exit(1)

# ===== SFX =====
run(['-i',str(B/'klip_k01.mp4'),'-ss','1.0','-t','1.0','-vn','-af','volume=-19dB','-ar','48000','-ac','2',str(T/'amb1.wav')])
run(['-stream_loop','9','-i',str(T/'amb1.wav'),'-t','8',str(T/'amb45.wav')])
run(['-f','lavfi','-i','anoisesrc=c=white:r=48000:d=0.09','-af','highpass=f=900,lowpass=f=4200,afade=t=in:d=0.005,afade=t=out:st=0.03:d=0.06,volume=6dB','-ac','2',str(T/'trzask.wav')])
run(['-f','lavfi','-i','anoisesrc=c=pink:r=48000:d=0.22','-af','bandpass=f=1600:w=500,vibrato=f=11:d=0.6,afade=t=in:d=0.02,afade=t=out:st=0.12:d=0.10,volume=2dB','-ac','2',str(T/'skrzyp.wav')])
run(['-i',str(B/'sfx_boom.mp3'),'-ar','48000','-ac','2',str(T/'boom.wav')])
run(['-i',str(B/'pisk_A.wav'),'-ss','2.20','-t','1.00','-af','silenceremove=start_periods=1:start_threshold=-38dB,areverse,silenceremove=start_periods=1:start_threshold=-38dB,areverse,alimiter=limit=0.95','-ac','2',str(T/'pisk.wav')])
run(['-i',str(B/'glos_Ef.wav'),'-t','5.70','-af','aecho=0.55:0.28:42:0.22,alimiter=limit=0.95','-ac','2','-ar','48000',str(T/'jozek.wav')])

def dur(p):
    r = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],capture_output=True,text=True)
    return float(r.stdout.strip())
D_PISK = dur(T/'pisk.wav'); D_JOZ = dur(T/'jozek.wav')
print(f'pisk={D_PISK:.2f}s jozek={D_JOZ:.2f}s')

def part(name, d, inputs, outopts):
    run(inputs + outopts + ['-t',f'{d:.3f}']+VIDEO+AUDIO+[str(T/name)])

KADR = str(B/'kadry'/'k04.jpg')
def zoomvf(d, z0, z1, jitter=0.0):
    fr = int(d*FPS)+1
    jx = f"+({jitter})*sin(on*2.1)" if jitter>0 else ""
    return f"zoompan=z='{z0}+({z1}-{z0})*on/{fr}':d={fr}:x='iw/2-(iw/zoom/2){jx}':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}"

def still(name, d, z0, z1, jitter=0.0, extra_a=None):
    ins = ['-loop','1','-t',f'{d+0.15:.2f}','-i',KADR] + (extra_a if extra_a else ['-i',str(T/'amb45.wav')])
    part(name, d, ins, ['-vf', zoomvf(d,z0,z1,jitter), '-map','0:v','-map','1:a'])

# ===== CZESCI =====
part('p00.mp4', 0.45, ['-i',str(B.parent/'10008'/'intro_a.mp4')], ['-vf',f'scale={W}:{H}'])
part('p0w.mp4', 6.73, ['-ss','0.05','-i',str(B/'klip_k00.mp4')], ['-vf',f'scale={W}:{H}'])
part('p01.mp4', 0.55, ['-ss','6.90','-i',str(B/'klip_k01.mp4')], ['-vf',f'scale={W}:{H}'])
# p02 shake + trzask, szelest ustaje
run(['-ss','7.50','-t','0.40','-i',str(B/'klip_k01.mp4'),'-vf',f"crop=1000:1780:'40+30*sin(n*2.7)':'70+24*cos(n*3.3)',scale={W}:{H}",'-an']+VIDEO+[str(T/'p02v.mp4')])
run(['-i',str(T/'p02v.mp4'),'-i',str(B/'klip_k01.mp4'),'-i',str(T/'trzask.wav'),'-filter_complex',"[1:a]atrim=7.50:7.90,asetpts=PTS-STARTPTS,afade=t=out:st=0.10:d=0.25[amb];[2:a]adelay=60|60[tr];[amb][tr]amix=inputs=2:normalize=0[a]",'-map','0:v','-map','[a]','-t','0.35']+VIDEO+AUDIO+[str(T/'p02.mp4')])
# p03 atak 1.1s JEDNA czesc: zoompan 0.5 + k02 0.6, BOOM pelny od klatki 1
run(['-loop','1','-t','0.65','-i',KADR,'-vf',zoomvf(0.50,1.00,1.28),'-an']+VIDEO+['-t','0.50',str(T/'p03v1.mp4')])
run(['-ss','2.00','-t','0.65','-i',str(B/'klip_k02_reroll.mp4'),'-vf',f'scale={W}:{H}','-an']+VIDEO+['-t','0.60',str(T/'p03v2.mp4')])
run(['-i',str(T/'p03v1.mp4'),'-i',str(T/'p03v2.mp4'),'-i',str(T/'boom.wav'),'-i',str(T/'amb45.wav'),'-filter_complex',"[0:v][1:v]concat=n=2:v=1[v];[3:a]atrim=0:1.10,volume=0.6[c];[c][2:a]amix=inputs=2:normalize=0[a]",'-map','[v]','-map','[a]','-t','1.10']+VIDEO+AUDIO+[str(T/'p03.mp4')])
# p04 pyt1: k03 0-2.82 + 0.30 ciszy; punch-in cieciem od 1.90
run(['-t','1.90','-i',str(B/'klip_k03.mp4'),'-vf',f'scale={W}:{H}','-an']+VIDEO+[str(T/'p04a.mp4')])
run(['-ss','1.90','-t','1.25','-i',str(B/'klip_k03.mp4'),'-vf',f'crop=iw*0.94:ih*0.94,scale={W}:{H}','-an']+VIDEO+[str(T/'p04b.mp4')])
run(['-i',str(T/'p04a.mp4'),'-i',str(T/'p04b.mp4'),'-i',str(B/'klip_k03.mp4'),'-i',str(T/'amb45.wav'),'-filter_complex',"[0:v][1:v]concat=n=2:v=1[v];[2:a]atrim=0:2.82,asetpts=PTS-STARTPTS[q];[3:a]atrim=0:0.30,asetpts=PTS-STARTPTS[c];[q][c]concat=n=2:v=0:a=1[a]",'-map','[v]','-map','[a]','-t','3.12']+VIDEO+AUDIO+[str(T/'p04.mp4')])
# p05 czekanie 0.55s
still('p05.mp4', 0.55, 1.02, 1.045)
# p06 pyt2: k04_reroll 4.22s; punch-in cieciem od 3.10
run(['-t','3.10','-i',str(B/'klip_k04_reroll.mp4'),'-vf',f'scale={W}:{H}','-an']+VIDEO+[str(T/'p06a.mp4')])
run(['-ss','3.10','-t','1.20','-i',str(B/'klip_k04_reroll.mp4'),'-vf',f'crop=iw*0.90:ih*0.90,scale={W}:{H}','-an']+VIDEO+[str(T/'p06b.mp4')])
run(['-i',str(T/'p06a.mp4'),'-i',str(T/'p06b.mp4'),'-i',str(B/'klip_k04_reroll.mp4'),'-filter_complex',"[0:v][1:v]concat=n=2:v=1[v];[2:a]atrim=0:4.22,asetpts=PTS-STARTPTS[a]",'-map','[v]','-map','[a]','-t','4.22']+VIDEO+AUDIO+[str(T/'p06.mp4')])
# p07 'Jozek...'
d7 = round(0.15 + D_PISK + 0.15, 2)
run(['-i',str(T/'pisk.wav'),'-i',str(T/'amb45.wav'),'-filter_complex',f"[0:a]adelay=150|150[p];[1:a]atrim=0:{d7}[c];[c][p]amix=inputs=2:normalize=0[a]",'-map','[a]',str(T/'a07.wav')])
still('p07.mp4', d7, 1.24, 1.26, extra_a=['-i',str(T/'a07.wav')])
# p08 pyt3 nad Ken Burns + drzenie
run(['-ss','0.05','-t','3.75','-i',str(B/'klip_k05_reroll.mp4'),'-vn','-af','asetpts=PTS-STARTPTS','-ar','48000','-ac','2',str(T/'a08.wav')])
still('p08.mp4', 3.75, 1.00, 1.18, jitter=4.0, extra_a=['-i',str(T/'a08.wav')])
# p09 scisniecie
run(['-i',str(T/'skrzyp.wav'),'-i',str(T/'amb45.wav'),'-filter_complex',"[1:a]atrim=0:0.45[c];[c][0:a]amix=inputs=2:normalize=0[a]",'-map','[a]',str(T/'a09.wav')])
still('p09.mp4', 0.45, 1.42, 1.46, extra_a=['-i',str(T/'a09.wav')])
# p10 puenta
d10 = round(0.12 + D_JOZ + 0.10, 2)
run(['-i',str(T/'jozek.wav'),'-i',str(T/'amb45.wav'),'-filter_complex',f"[0:a]adelay=120|120[j];[1:a]atrim=0:{d10}[c];[c][j]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]",'-map','[a]',str(T/'a10.wav')])
run(['-i',str(B/'klip_k06_niemy.mp4'),'-i',str(T/'a10.wav'),'-vf',f'scale={W}:{H}','-map','0:v','-map','1:a','-t',f'{d10:.2f}']+VIDEO+AUDIO+[str(T/'p10.mp4')])
# p11 outro pelne (oznaczenie AI czytelne)
part('p11.mp4', 3.00, ['-i',str(B.parent/'10008'/'outro_a.mp4')], ['-vf',f'scale={W}:{H}'])

# ===== CONCAT =====
parts = ['p00.mp4','p0w.mp4','p01.mp4','p02.mp4','p03.mp4','p04.mp4','p05.mp4','p06.mp4','p07.mp4','p08.mp4','p09.mp4','p10.mp4','p11.mp4']
(T/'lista.txt').write_text(''.join(f"file '{T/p}'\n" for p in parts))
run(['-f','concat','-safe','0','-i',str(T/'lista.txt'),'-c','copy',str(T/'sklejka.mp4')])

# ===== NAPISY =====
offs, t = {}, 0.0
for p in parts:
    offs[p] = t; t += dur(T/p)
print('TOTAL:', round(t,2), 's | offsety:', {k: round(v,2) for k,v in offs.items()})
kb = KOLORY_ASS['BOHATER']; kj = '&H0AD9FF&'
def cz(s): return f'{int(s//3600)}:{int(s%3600//60):02d}:{s%60:05.2f}'
L = []
o=offs['p0w.mp4']
L.append((o+0.20, o+2.64, '&HFFFFFF&', '{\\an8\\fad(200,150)}Kiedy złapiesz złodzieja jabłek... 🍎'))
L.append((o+0.25, o+2.64, kb, 'TOMEK (szeptem): Złodziej jabłek grasuje.'))
L.append((o+3.52, o+6.58, kb, 'Dzisiaj... koniec tej zabawy.'))
o=offs['p04.mp4']; L.append((o+0.08, o+2.82, kb, 'TOMEK: Gadaj, ktoś ty?!'))
o=offs['p06.mp4']; L.append((o+0.02, o+2.76, kb, 'TOMEK: Gadaj, pókim dobry...')); L.append((o+3.18, o+4.22, kb, '...ktoś ty?!'))
o=offs['p07.mp4']; L.append((o+0.15, o+0.15+D_PISK, kj, 'JÓZEK: Józek...!'))
o=offs['p08.mp4']; L.append((o+0.09, o+2.19, kb, 'TOMEK: No gadaj, draniu!')); L.append((o+2.69, o+3.63, kb, 'Ktoś ty?!'))
o=offs['p10.mp4']+0.12; L.append((o+0.00, o+1.12, kj, 'JÓZEK: To ja...')); L.append((o+2.40, o+2.88, kj, 'Józek...')); L.append((o+4.46, o+5.62, kj, 'niemowa ze wsi!'))
tresc = ''.join(f'Dialogue: 0,{cz(a)},{cz(b)},Default,,0,0,0,,{{\\c{k}}}{txt}\n' for a,b,k,txt in L)
(B/'napisy10.ass').write_text(ASS_HEADER + tresc, encoding='utf-8')

# ===== FINAL =====
run(['-i',str(T/'sklejka.mp4'),'-vf',f"ass={B/'napisy10.ass'}",'-c:a','copy','-movflags','+faststart',str(B/'final.mp4')])
va = subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,duration','-of','csv=p=0',str(B/'final.mp4')],capture_output=True,text=True).stdout
print('FINAL streams:', va.replace('\n',' '), '| plik:', (B/'final.mp4').stat().st_size//1024, 'KB')
