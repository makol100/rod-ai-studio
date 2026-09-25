"""Szukanie zdjec Commons: opis PL kazdego kandydata (VLM) + test 'nic rozpraszajacego' + NATYCHMIAST na Telegram Tomasza (D-0522)."""
import json,subprocess,io,re,urllib.parse,time,base64,urllib.request,os,sys
from PIL import Image
sys.path.insert(0,'/root/rod-ai-studio/tools'); import tg_foto
os.chdir('/root/rod-ai-studio/data/rolki_0zl/commons')
Q=json.load(open(sys.argv[1]))  # {"prefiks":[query, opis_oczekiwany], ...}
TEMAT=sys.argv[2]; log=open(f'/root/rod-ai-studio/data/rolki_0zl/_szukaj_{TEMAT}.log','w',encoding='utf-8')
def get(u): return subprocess.run(['curl','-sL','-m','90','-A','RODWozniki/1.0 (rodwozniki.pl; kontakt rodwozniki@gmail.com)',u],capture_output=True).stdout
def vlm(path,q):
    b=base64.b64encode(open(path,'rb').read()).decode()
    r=urllib.request.Request('http://127.0.0.1:11434/api/generate',data=json.dumps({"model":"qwen2.5vl:7b","stream":False,"prompt":q,"images":[b],"options":{"temperature":0}}).encode(),headers={'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r,timeout=300)).get('response','').strip()
man=json.load(open('manifest_commons.json')); ok=0
for k,(q,opis) in Q.items():
    time.sleep(3)
    if q.startswith('cat:'):
        api="https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle="+urllib.parse.quote('Category:'+q[4:])+"&gcmtype=file&gcmlimit=200&prop=imageinfo&iiprop=url%7Csize%7Cextmetadata%7Cmime&iiurlwidth=1600&format=json"
    else:
        api="https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch="+urllib.parse.quote(q)+"&gsrnamespace=6&gsrlimit=40&prop=imageinfo&iiprop=url%7Csize%7Cextmetadata%7Cmime&iiurlwidth=1600&format=json"
    try: d=json.loads(get(api))
    except Exception: print(k,'API padl',file=log,flush=True); continue
    pages=list(d.get('query',{}).get('pages',{}).values()); n=0; probe=0
    for p in sorted(pages, key=lambda p:-p.get('imageinfo',[{}])[0].get('width',0)):
        ii=p.get('imageinfo',[{}])[0]; w=ii.get('width',0)
        if w<900 or ii.get('mime')!='image/jpeg': continue
        t=p['title'].lower()
        if any(x in t for x in ('painting','drawing','illustration','engraving','microscop','herbarium','specimen','panoram','biedronka','sklep','market')): continue
        WT=os.environ.get('WYMAGANE_W_TYTULE','')
        if WT and not any(w in t for w in WT.split(',')): continue
        md=ii.get('extmetadata',{}); lic=md.get('LicenseShortName',{}).get('value','?'); aut=re.sub(r'<[^>]+>','',md.get('Artist',{}).get('value','?'))[:60]
        if not re.search(r'CC|Public domain|PD|No restrictions',lic,re.I): continue
        data=get(ii.get('thumburl') or ii['url'])
        try: im=Image.open(io.BytesIO(data)); im.load()
        except Exception: continue
        tmp=f'_kand_{k}_{probe}.jpg'; probe+=1; im.convert('RGB').save(tmp,quality=90)
        import oko_genka
        try:
            g=oko_genka.ocen(tmp, opis); o=g.get('co_widac',''); w_='YES' if g.get('werdykt')=='TAK' else 'NO '+g.get('powod','')[:80]
        except Exception as e:
            o='BLAD oka: '+str(e)[:60]; w_='NO'
        ZLE=('nagrob','cmentarz','grób','grob','pomnik','tablic','napis','ludz','osob','mężczy','kobiet','dzieck','samoch','pojazd','budyn','rysun','mikrosk','muze','sklep','reklam','logo','ruin','pracown','człowiek','czlowiek','mundur','dmuchaw')
        if any(z in o.lower() for z in ZLE): w_='NO (czarna lista opisu)'
        if w_.strip().upper().startswith('YES'):
            n+=1; ok+=1; fn=f"{k}_{n:02d}.jpg"; im.convert('RGB').save(fn,quality=92)
            man.append({'plik':fn,'tytul':p['title'],'licencja':lic,'autor':aut,'url':ii.get('descriptionurl'),'rozmiar':im.size,'opis':o[:200]}); print('OK',fn,'|',o[:160],file=log,flush=True)
            try: tg_foto.wyslij(fn, f"[{TEMAT}] {k.split('_')[0]} ({fn}) — {o[:180]} (lic. {lic}). OK / NIE?")
            except Exception as e: print('  TG blad',e,file=log,flush=True)
            json.dump(man,open('manifest_commons.json','w'),ensure_ascii=False,indent=1)
        else: print('  odrzucone:',p['title'][:40],'|',o[:100],file=log,flush=True)
        os.remove(tmp)
        if n>=int(os.environ.get('MAXN','2')) or probe>=int(os.environ.get('MAXP','8')): break
print('KONIEC przyjete',ok,file=log,flush=True)

# WYMAGANE_W_TYTULE obslugiwane
