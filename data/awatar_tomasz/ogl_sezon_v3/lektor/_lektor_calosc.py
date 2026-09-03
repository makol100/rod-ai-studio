import subprocess, json, os, sys
B='/root/rod-ai-studio/data/awatar_tomasz/ogl_sezon_v3'; L=B+'/lektor'; V='Daniel'
# okna zrodlowe (720p): (plik, start, dlugosc, kwestia)
import sys
SPEED={'1':1.2,'2':1.0,'3':1.2,'4':1.12,'5':1.12,'6':1.0}
okna=[('omni_seg2_A4.mp4',0.0,10.0,'1'),('omni_seg2_A4.mp4',10.0,8.1,'2'),('omni_seg3_C.mp4',0.0,9.9,'3'),
      ('omni_seg6_B2.mp4',0.0,10.0,'4'),('omni_seg6_B2.mp4',10.0,10.0,'5'),('omni_seg6_B2.mp4',20.0,10.0,'6')]
def run(c): return subprocess.run(c,shell=True,capture_output=True,text=True)
for plik,st,dl,kw in okna:
    sp=SPEED[kw]; mp3=f'{L}/kw{kw}_{V}_s{sp}.mp3'
    if not os.path.exists(mp3):
        r=run(f'docker exec fabryka-api /app/venv/bin/python {L}/_tts.py {kw} {V} {sp}'); print('TTS',kw,sp,r.stdout.strip()[-30:],r.stderr[-100:],flush=True)
    d=float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {mp3}').stdout.strip())
    # audio do okna: jesli dluzsze niz okno-0.4 -> atempo; potem pad cisza do dl
    cel=dl-0.3; tempo=min(1.05, max(1.0, d/cel))
    run(f'ffmpeg -v error -y -i {mp3} -filter:a "atempo={tempo:.3f},apad=whole_dur={dl}" -t {dl} -ar 44100 -ac 1 {L}/kw{kw}_fit.wav')
    run(f'ffmpeg -v error -y -ss {st} -i {B}/{plik} -t {dl} -an -c:v libx264 -crf 18 {L}/frag{kw}.mp4')
    r=run(f'docker exec fabryka-api /app/venv/bin/python {L}/_lipsync.py {L}/frag{kw}.mp4 {L}/kw{kw}_fit.wav {L}/lip{kw}_v2.mp4')
    print(f'KW{kw}: tts {d:.1f}s okno {dl}s tempo {tempo:.2f} | lipsync:', r.stdout.strip()[-60:], r.stderr[-120:], flush=True)
print('SEGMENTY GOTOWE', flush=True)
