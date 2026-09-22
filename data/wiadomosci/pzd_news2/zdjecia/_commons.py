import json,subprocess,io,re,urllib.parse
from PIL import Image
def get(u):
    return subprocess.run(['curl','-sL','-m','90','-A','RODWozniki/1.0 (rodwozniki.pl)',u],capture_output=True).stdout
Q={'oplaty':'Polish zloty banknotes coins','ministerstwo':'Ministerstwo Rozwoju i Technologii budynek Warszawa','dzik':'wild boar Sus scrofa Poland','dziki_miasto':'dziki w mieście Warszawa','pozar':'fire brigade night fire OSP','smietnik':'kontener na śmieci ogród','wodociag':'water pipe trench installation','brama':'automatic gate remote garden','ruda_slaska':'Ruda Śląska panorama','siedlce':'Siedlce ratusz','szklarnia':'greenhouse autumn garden','jesien_ogrod':'autumn garden leaves rake','kompost':'compost heap leaves','klimat':'city park trees climate','warszawa_ogrody':'rodzinny ogród działkowy Warszawa'}
man=[]
for k,q in Q.items():
    api="https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch="+urllib.parse.quote(q)+"&gsrnamespace=6&gsrlimit=15&prop=imageinfo&iiprop=url%7Csize%7Cextmetadata%7Cmime&iiurlwidth=1600&format=json"
    raw=get(api)
    try: d=json.loads(raw)
    except Exception as e: print(k,'API padl',raw[:100]); continue
    pages=list(d.get('query',{}).get('pages',{}).values())
    n=0
    for p in sorted(pages, key=lambda p:-p.get('imageinfo',[{}])[0].get('width',0)):
        ii=p.get('imageinfo',[{}])[0]; w=ii.get('width',0); mime=ii.get('mime','')
        if w<1200 or mime!='image/jpeg': continue
        md=ii.get('extmetadata',{}); lic=md.get('LicenseShortName',{}).get('value','?'); aut=re.sub(r'<[^>]+>','',md.get('Artist',{}).get('value','?'))[:60]
        if not re.search(r'CC|Public domain|PD|No restrictions',lic,re.I): continue
        data=get(ii.get('thumburl') or ii['url'])
        try: im=Image.open(io.BytesIO(data)); im.load()
        except Exception as e: continue
        n+=1; fn=f"commons_{k}_{n:02d}.jpg"; im.convert('RGB').save(fn,quality=92)
        man.append({'plik':fn,'tytul':p['title'],'licencja':lic,'autor':aut,'url':ii.get('descriptionurl'),'rozmiar':im.size}); print(fn,im.size,lic,'|',aut,'|',p['title'][:70])
        if n>=3: break
    if n==0: print(k,'NIC (stron:',len(pages),')')
json.dump(man,open('manifest_commons.json','w'),ensure_ascii=False,indent=1); print('razem',len(man))
