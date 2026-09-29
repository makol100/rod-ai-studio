"""Kontrola głosu: Genek (Gemini, oczy_uszy.py) transkrybuje każdą kwestię, porównanie słowo-w-słowo z tekstem."""
import subprocess, re, difflib, sys, json, pathlib
B=pathlib.Path('/root/rod-ai-studio/data/ciekawostki/wydanie1')
kw=[l.rstrip('\n').split('\t',1) for l in open(B/'kwestie_v3.tsv',encoding='utf-8') if '\t' in l]
only=set(sys.argv[1:])
def norm(t): return re.sub(r'[^\wąćęłńóśźż ]','',t.lower().replace('—',' ').replace('-',' ')).split()
wyn={}
for n,t in kw:
    if only and n not in only: continue
    w=B/'glos/final'/f'{n}.wav'
    if not w.exists(): print(n,'BRAK WAV'); continue
    r=subprocess.run(['python3','/root/rod-ai-studio/tools/oczy_uszy.py',str(w),'--co','transkrypcja'],capture_output=True,text=True,timeout=300)
    tr=r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
    a,b=norm(t),norm(tr); s=difflib.SequenceMatcher(None,a,b)
    roz=[(' '.join(a[i1:i2]),' '.join(b[j1:j2])) for op,i1,i2,j1,j2 in s.get_opcodes() if op!='equal']
    wyn[n]={'ratio':round(s.ratio(),3),'transkrypcja':tr,'roznice':roz}
    print(n, round(s.ratio(),3), roz[:6], flush=True)
json.dump(wyn,open(B/'glos/_ucho.json','w'),ensure_ascii=False,indent=1)
