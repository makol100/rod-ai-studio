import sys, json, subprocess, difflib, re, unicodedata
plik=sys.argv[1]; segs=sys.argv[2].split(',')
kw=json.load(open(__import__("os").environ.get("KWESTIE","kwestie.json"))); oczek=' '.join(kw[s] for s in segs)
subprocess.run(['ffmpeg','-v','error','-y','-i',plik,'-vn','-ac','1','-ar','16000','_tmp.wav'],check=True)
code='''
from faster_whisper import WhisperModel
m=WhisperModel('medium', device='cpu', compute_type='int8')
segs,_=m.transcribe('/root/rod-ai-studio/data/awatar_tomasz/ogl_sezon_v3/_tmp.wav', language='pl', word_timestamps=True, beam_size=5)
import json
out=[]; words=[]
for s in segs:
    out.append((round(s.start,1),round(s.end,1),s.text.strip()))
    for w in (s.words or []): words.append((round(w.start,1), w.word.strip(), round(w.probability,2)))
print(json.dumps({'segs':out,'words':words},ensure_ascii=False))
'''
out=subprocess.run(['docker','exec','fabryka-api','/app/venv/bin/python','-c',code],capture_output=True,text=True).stdout.strip().splitlines()[-1]
J=json.loads(out); tr=J['segs']; words=J['words']
import subprocess as sp
dur=float(sp.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',plik],capture_output=True,text=True).stdout.strip())
tr=[x for x in tr if x[0] < dur-0.3]
usl=' '.join(t for _,_,t in tr)
def norm(s):
    s=s.lower().replace('5 września','piątego września').replace('godzina 17','godzina siedemnasta').replace('2026 roku','dwa tysiące dwudziestego szóstego roku').replace('rod ','rod ')
    return re.findall(r"[a-ząćęłńóśźż0-9]+", s)
a,b=norm(oczek),norm(usl)
sm=difflib.SequenceMatcher(a=a,b=b); prob=[]
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal': continue
    prob.append(f"{tag.upper()} oczek='{' '.join(a[i1:i2])}' usl='{' '.join(b[j1:j2])}'")
print("TRANSKRYPT:"); [print('  %5.1f-%5.1f %s'%(s,e,t)) for s,e,t in tr]
slabe=[(t,w,p) for t,w,p in words if p<0.5 and len(w.strip('.,!?'))>1]
dup=[(words[i][0],words[i][1]) for i in range(1,len(words)) if words[i][1].strip('.,!?').lower()==words[i-1][1].strip('.,!?').lower() and len(words[i][1].strip('.,!?'))>2]
for t,w,p in slabe: prob.append(f"SLABE SLOWO @{t}s '{w}' p={p}")
for t,w in dup: prob.append(f"DUPLIKAT SLOWA @{t}s '{w}'")
print("WERDYKT MOWY:", "CZYSTO" if not prob else "PROBLEMY:"); [print("  -",p) for p in prob]
