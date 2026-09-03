import subprocess, json, os, time
B='/root/rod-ai-studio/data/awatar_tomasz/ogl_sezon_v3'; L=B+'/lektor'; V='Daniel'; SPEED=1.1
while subprocess.run('pgrep -f _lektor_calosc.py',shell=True,capture_output=True).returncode==0: time.sleep(10)
okna=[('omni_seg2_A4.mp4',0.0,10.0,'1'),('omni_seg2_A4.mp4',10.0,8.1,'2'),('omni_seg3_C.mp4',0.0,9.9,'3'),
      ('omni_seg6_B2.mp4',0.0,10.0,'4'),('omni_seg6_B2.mp4',10.0,10.0,'5'),('omni_seg6_B2.mp4',20.0,10.0,'6')]
def run(c): return subprocess.run(c,shell=True,capture_output=True,text=True)
# TTS ze speed 1.1
tts=open(f'{L}/_tts.py').read().replace("'speed':1.0","'speed':SPEED").replace("import sys, json, urllib.request","import sys, json, urllib.request\nSPEED=float(sys.argv[3]) if len(sys.argv)>3 else 1.0").replace("kw{nr}_{voice}.mp3","kw{nr}_{voice}_s{SPEED}.mp3")
open(f'{L}/_tts2.py','w').write(tts)
for plik,st,dl,kw in okna:
    r=run(f'docker exec fabryka-api /app/venv/bin/python {L}/_tts2.py {kw} {V} {SPEED}'); a=f'{L}/kw{kw}_{V}_s{SPEED}.mp3'
    d=float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {a}').stdout.strip())
    cel=d+0.35                       # dlugosc docelowa fragmentu = audio + pauza
    f=max(1.0, cel/dl)               # spowolnienie wideo (>=1)
    run(f'ffmpeg -v error -y -i {a} -filter:a "apad=whole_dur={cel:.2f}" -t {cel:.2f} -ar 44100 -ac 1 {L}/kw{kw}_fit2.wav')
    run(f'ffmpeg -v error -y -ss {st} -i {B}/{plik} -t {dl} -an -filter:v "setpts={f:.4f}*PTS" -r 24 -c:v libx264 -crf 18 {L}/frag{kw}_v2.mp4')
    r=run(f'docker exec fabryka-api /app/venv/bin/python {L}/_lipsync.py {L}/frag{kw}_v2.mp4 {L}/kw{kw}_fit2.wav {L}/lip{kw}_v2.mp4')
    print(f'KW{kw}: tts {d:.1f}s okno {dl}s -> wideo x{f:.2f} wolniej | {r.stdout.strip()[-30:]} {r.stderr[-100:]}', flush=True)
print('V2 SEGMENTY GOTOWE', flush=True)
