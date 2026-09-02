import subprocess, json, os
B='/root/rod-ai-studio/data/awatar_tomasz'
pliki=[('test1/omni_test1_1.mp4','test #1, 8 s'),('ogl_sezon/omni_seg4.mp4','v1 watek 40 s'),('ogl_sezon/omni_seg2_v2.mp4','v2 galaz seg2 (echo)'),('ogl_sezon/omni_seg4_v3.mp4','v2 watek 40 s'),
 ('ogl_sezon_v3/omni_seg3_A2.mp4','v3 A2 30 s'),('ogl_sezon_v3/omni_seg3_A3.mp4','v3 A3 30 s'),('ogl_sezon_v3/omni_seg3_A4.mp4','v3 A4 30 s'),('ogl_sezon_v3/omni_seg3_C.mp4','v3 C 10 s'),
 ('ogl_sezon_v3/omni_seg6_B.mp4','v3 B 30 s'),('ogl_sezon_v3/omni_seg6_B2.mp4','v3 B2 30 s'),('ogl_sezon_v3/omni_seg2_A.mp4','v3 A seg2 (uciete)')]
wyn={}
for p,opis in pliki:
    f=f'{B}/{p}'
    if not os.path.exists(f): print('BRAK',p,flush=True); continue
    subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-vn','-ac','1','-ar','16000',f'{B}/_bank_tmp.wav'],check=True)
    code=f'''
from faster_whisper import WhisperModel
import json
m=WhisperModel('medium', device='cpu', compute_type='int8')
segs,_=m.transcribe('{B}/_bank_tmp.wav', language='pl', word_timestamps=True, beam_size=5)
out=[]
for s in segs:
    ws=[(round(w.start,2),round(w.end,2),w.word.strip(),round(w.probability,2)) for w in (s.words or [])]
    out.append({{'start':round(s.start,2),'end':round(s.end,2),'text':s.text.strip(),'words':ws}})
print(json.dumps(out,ensure_ascii=False))
'''
    r=subprocess.run(['docker','exec','fabryka-api','/app/venv/bin/python','-c',code],capture_output=True,text=True)
    try: segs=json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e: print('BLAD',p,r.stderr[-200:],flush=True); continue
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout.strip())
    segs=[s for s in segs if s['start']<dur-0.3]
    for s in segs:
        ws=s['words']; flags=[]
        for i,w in enumerate(ws):
            if w[3]<0.5 and len(w[2].strip('.,!?'))>2: flags.append(f"slabe '{w[2]}'@{w[0]}")
            if i>0 and w[2].strip('.,!?').lower()==ws[i-1][2].strip('.,!?').lower() and len(w[2].strip('.,!?'))>2: flags.append(f"DUPLIKAT '{w[2]}'@{w[0]}")
        s['flags']=flags
    wyn[p]={'opis':opis,'dur':dur,'segs':segs}
    print('OK',p,len(segs),'zdan',flush=True)
json.dump(wyn,open(f'{B}/bank_kwestii_raw.json','w'),ensure_ascii=False,indent=1)
print('KONIEC',flush=True)
