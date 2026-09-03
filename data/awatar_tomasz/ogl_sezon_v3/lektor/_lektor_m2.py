import subprocess, os, re
B='/root/rod-ai-studio/data/awatar_tomasz/ogl_sezon_v3'; L=B+'/lektor'
okna=[('omni_seg2_A4.mp4',0.0,10.0,'1',1.1),('omni_seg2_A4.mp4',10.0,8.1,'2',1.05),('omni_seg3_C.mp4',0.0,9.9,'3',1.1),
      ('omni_seg6_B2.mp4',0.0,10.0,'4',1.1),('omni_seg6_B2.mp4',10.0,10.0,'5',1.2),('omni_seg6_B2.mp4',20.0,10.0,'6',1.0)]
def run(c): return subprocess.run(c,shell=True,capture_output=True,text=True)
def dur(f): return float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {f}').stdout.strip() or 0)
for plik,st,dl,kw,sp in okna:
    mp3=None
    for sp_try in (sp, sp+0.1, 1.2):
        r=run(f'docker exec fabryka-api /app/venv/bin/python {L}/_tts2.py {kw} Daniel {sp_try} 0.5'); m=re.search(r'OK (\S+)',r.stdout)
        if not m: print('TTS BLAD',kw,r.stderr[-120:],flush=True); continue
        d=dur(m.group(1)); print(f'kw{kw} speed{sp_try}: {d:.2f}s / okno {dl}',flush=True)
        if d<=dl-0.25: mp3=m.group(1); break
        mp3=m.group(1)
    d=dur(mp3); tempo=min(1.06,max(1.0,d/(dl-0.25)))
    run(f'ffmpeg -v error -y -i {mp3} -filter:a "atempo={tempo:.3f},apad=whole_dur={dl}" -t {dl} -ar 44100 -ac 1 {L}/kw{kw}_fitm2.wav')
    if not os.path.exists(f'{L}/frag{kw}.mp4'): run(f'ffmpeg -v error -y -ss {st} -i {B}/{plik} -t {dl} -an -c:v libx264 -crf 18 {L}/frag{kw}.mp4')
    r=run(f'docker exec fabryka-api /app/venv/bin/python {L}/_lipsync.py {L}/frag{kw}.mp4 {L}/kw{kw}_fitm2.wav {L}/lip{kw}_m2.mp4')
    print(f'KW{kw}: tts {d:.2f}s tempo {tempo:.2f} | lipsync {"OK" if os.path.exists(f"{L}/lip{kw}_m2.mp4") else "BLAD "+r.stderr[-100:]}',flush=True)
print('SEGMENTY GOTOWE',flush=True)
