#!/usr/bin/env python3
"""GENEK SZUKA (24.09.2026, dekret 'Gienek ma poszukac'): dla kazdego ujecia Genek (Gemini) uklada zapytania -> Commons API -> oko_genka (czy DOKLADNIE to ujecie) -> Telegram. 0 generowania."""
import json,sys,os,re,io,time,subprocess,urllib.request,urllib.parse
from PIL import Image
sys.path.insert(0,'/root/rod-ai-studio/tools'); import oko_genka, tg_foto
KL=oko_genka.klucz(); OUT='/root/rod-ai-studio/data/rolki_0zl/commons/'; LOG=open('/root/rod-ai-studio/data/rolki_0zl/_genek_szuka.log','a',encoding='utf-8')
def gemini(prompt):
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.3,"responseMimeType":"application/json"}}).encode()
    r=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={KL}",data=body,headers={'Content-Type':'application/json'})
    return json.loads(json.load(urllib.request.urlopen(r,timeout=90))['candidates'][0]['content']['parts'][0]['text'])
def get(u): return subprocess.run(['curl','-sL','-m','60','-A','RODWozniki/1.0 (rodwozniki.pl; kontakt rodwozniki@gmail.com)',u],capture_output=True).stdout
def szukaj(prefiks, ujecie, ile=2):
    q=gemini(f'Podaj 5 krotkich ANGIELSKICH zapytan do wyszukiwarki Wikimedia Commons, ktore najlepiej znajda PRAWDZIWE zdjecie: "{ujecie}" (kontekst: polski ogrod dzialkowy, jesien). JSON: {{"q":["..."]}}')['q']
    man=json.load(open(OUT+'manifest_commons.json')); n=0; widziane=set()
    for zap in q:
        api="https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch="+urllib.parse.quote(zap)+"&gsrnamespace=6&gsrlimit=15&prop=imageinfo&iiprop=url%7Csize%7Cextmetadata%7Cmime&iiurlwidth=1400&format=json"
        try: pages=list(json.loads(get(api)).get('query',{}).get('pages',{}).values())
        except Exception: continue
        for p in pages:
            if p['title'] in widziane: continue
            widziane.add(p['title']); ii=p.get('imageinfo',[{}])[0]
            if ii.get('width',0)<900 or ii.get('mime')!='image/jpeg': continue
            md=ii.get('extmetadata',{}); lic=md.get('LicenseShortName',{}).get('value','?')
            if not re.search(r'CC|Public domain|PD|No restrictions',lic,re.I): continue
            try: im=Image.open(io.BytesIO(get(ii.get('thumburl') or ii['url']))); im.load()
            except Exception: continue
            tmp=OUT+f'_kand_{prefiks}.jpg'; im.convert('RGB').save(tmp,quality=90)
            try: g=oko_genka.ocen(tmp, ujecie+' — prawdziwe zdjecie, bez ludzi (dlonie dozwolone), bez napisow, grobow, budynkow')
            except Exception as e: print('oko blad',e,file=LOG,flush=True); continue
            if g.get('werdykt')=='TAK':
                n+=1; fn=f'{prefiks}_{n:02d}.jpg'; os.replace(tmp,OUT+fn)
                man.append({'plik':fn,'tytul':p['title'],'licencja':lic,'url':ii.get('descriptionurl'),'opis':g.get('co_widac','')[:200],'ujecie':ujecie}); json.dump(man,open(OUT+'manifest_commons.json','w'),ensure_ascii=False,indent=1)
                tg_foto.wyslij(OUT+fn, f"[{ujecie}] {g.get('co_widac','')[:250]} — OK / NIE?"); print('OK',fn,'|',ujecie,'|',g.get('co_widac','')[:100],file=LOG,flush=True)
                if n>=ile: return n
            else: os.remove(tmp)
            time.sleep(1)
    print('BRAK/MALO',prefiks,n,'|',ujecie,file=LOG,flush=True); return n
if __name__=='__main__':
    for pref,uj in json.load(open(sys.argv[1])).items(): szukaj(pref,uj,int(os.environ.get('ILE','2')))
    print('KONIEC',file=LOG,flush=True)
