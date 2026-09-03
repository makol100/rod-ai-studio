import subprocess, json, re, os, sys
B='/root/rod-ai-studio/data/rolki_info/tauron_kdt'; M=B+'/montaz'; BR='/root/rod-ai-studio/data/zarty/10012'
def run(c): r=subprocess.run(c,shell=True,capture_output=True,text=True); return r.stdout+r.stderr
def dur(f): return float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{f}"').strip())
def koniec_mowy(f):
    out=run(f'ffmpeg -v info -y -i "{f}" -vn -af "silencedetect=noise=-38dB:d=0.25" -f null - 2>&1')
    d=dur(f); st=[float(x) for x in re.findall(r'silence_start: ([0-9.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([0-9.]+)',out)]
    # ostatnia cisza siegajaca konca pliku
    if st and (len(en)<len(st) or en[-1]>=d-0.15): return min(d, st[-1]+0.35)
    return d
N="scale=1080:1920:flags=lanczos,fps=24,setsar=1,format=yuv420p"; A="aresample=48000,aformat=channel_layouts=stereo"
# (typ, plik, overlay_img, od, do)
plan=[('v',f'{BR}/intro_a_n.mp4',None,0,0),
 ('i',f'{B}/izabela/I1.mp4',None,0,0),('t',f'{B}/tomasz/T1_OK.mp4',None,0,0),
 ('i',f'{B}/izabela/I2.mp4',None,0,0),('t',f'{B}/tomasz/T2_OK.mp4',f'{M}/p_SZAFKA-gotowa.jpg',3.0,7.0),
 ('i',f'{B}/izabela/I3.mp4',None,0,0),('t',f'{B}/tomasz/T3_OK.mp4',f'{M}/p_granica.jpg',3.2,8.6),
 ('i',f'{B}/izabela/I4.mp4',None,0,0),('t',f'{B}/tomasz/T4_OK.mp4',f'{M}/p_991.jpg',1.5,8.8),
 ('i',f'{B}/izabela/I5.mp4',None,0,0),('t',f'{B}/tomasz/T5_OK.mp4',f'{M}/p_GRAF-kroki.jpg',0.8,6.5),
 ('t',f'{B}/tomasz/T6_OK.mp4',f'{M}/p_STARY-LICZNIK.jpg',0.4,4.2),
 ('i',f'{B}/izabela/I7.mp4',None,0,0),('v',f'{BR}/outro_a_n.mp4',None,0,0),('v',f'{BR}/plansza_ai_n.mp4',None,0,0)]
inputs=[]; fc=[]; idx=0; concat=[]
for typ,plik,ov,a,b in plan:
    if not os.path.exists(plik): print('BRAK',plik); sys.exit(1)
    inputs.append(f'-i "{plik}"'); vi=idx; idx+=1
    kon=koniec_mowy(plik) if typ=='t' else dur(plik)
    if typ=='t' and ov:
        inputs.append(f'-loop 1 -t {kon:.3f} -i "{ov}"'); oi=idx; idx+=1
        fc.append(f'[{vi}:v]trim=0:{kon:.3f},setpts=PTS-STARTPTS,{N}[b{vi}];[{oi}:v]{N}[o{vi}];[b{vi}][o{vi}]overlay=enable=\'between(t,{a},{b})\'[v{vi}]')
    else:
        fc.append(f'[{vi}:v]trim=0:{kon:.3f},setpts=PTS-STARTPTS,{N}[v{vi}]')
    fc.append(f'[{vi}:a]atrim=0:{kon:.3f},asetpts=PTS-STARTPTS,{A}[a{vi}]')
    concat.append(f'[v{vi}][a{vi}]'); print(f'{typ} {os.path.basename(plik)} {kon:.2f}s' + (f' overlay {a}-{b}' if ov else ''))
fc.append(''.join(concat)+f'concat=n={len(concat)}:v=1:a=1[v][a]')
cmd=f'ffmpeg -v error -y {" ".join(inputs)} -filter_complex "{";".join(fc)}" -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 19 -c:a aac -b:a 192k -movflags +faststart {M}/rolka_tauron_v1.mp4'
open(f'{M}/_cmd.sh','w').write(cmd+'\n'); r=run(cmd); print(r[-400:] if r.strip() else 'FFMPEG OK')
print('wynik:', dur(f'{M}/rolka_tauron_v1.mp4'),'s')
