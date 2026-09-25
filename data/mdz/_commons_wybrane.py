import json,subprocess,urllib.parse,re,io,sys
from PIL import Image
sys.path.insert(0,'/root/rod-ai-studio/tools'); import tg_foto
OUT='/root/rod-ai-studio/data/mdz/foto/'
LISTA=[("C_M1_mieczyk","MIECZYK","File:Orange garden gladiolus.jpg","kwitnace mieczyki"),
 ("C_M1b_mieczyk","MIECZYK","File:AZBG Gladiolus flower.jpg","kwitnace mieczyki"),
 ("C_Z8_zimowit","ZIMOWIT","File:Colchicum autumnale Pilat.jpg","kwitnacy zimowit jesienny"),
 ("C_Z8b_zimowit","ZIMOWIT","File:Colchicum autumnale Piazzo 02.jpg","kwitnacy zimowit jesienny"),
 ("C_Z10_preciki","ZIMOWIT","File:Colchicum autumnale 00.jpg","zimowit — zblizenie, 6 precikow"),
 ("C_Z9_liscie","ZIMOWIT (liscie wiosna)","File:20230503Colchicum autumnale1.jpg","liscie zimowitu wiosna — myla sie z czosnkiem niedzwiedzim")]
def get(u): return subprocess.run(['curl','-sL','-m','90','-A','RODWozniki/1.0 (rodwozniki.pl; kontakt rodwozniki@gmail.com)',u],capture_output=True).stdout
man=[]
for k,rosl,tyt,opis in LISTA:
    d=json.loads(get("https://commons.wikimedia.org/w/api.php?action=query&titles="+urllib.parse.quote(tyt)+"&prop=imageinfo&iiprop=url%7Csize%7Cextmetadata&iiurlwidth=1600&format=json"))
    p=list(d['query']['pages'].values())[0]; ii=p.get('imageinfo',[{}])[0]
    md=ii.get('extmetadata',{}); lic=md.get('LicenseShortName',{}).get('value','?'); aut=re.sub(r'<[^>]+>','',md.get('Artist',{}).get('value','?'))[:60]
    if not re.search(r'CC|Public domain|PD',lic,re.I): print('LICENCJA?',k,lic); continue
    im=Image.open(io.BytesIO(get(ii.get('thumburl') or ii['url']))).convert('RGB'); fn=OUT+k+'.jpg'; im.save(fn,quality=92)
    man.append({'plik':k+'.jpg','tytul':tyt,'licencja':lic,'autor':aut,'url':ii.get('descriptionurl'),'rozmiar':im.size})
    print('OK',k,im.size,lic,aut, 'TG:',tg_foto.wyslij(fn,f"[rolka mieczyki-dalie-zimowit, COMMONS] {rosl} — {opis} ({tyt[5:]}, lic. {lic}, aut. {aut}) — 👍/👎"))
json.dump(man,open(OUT+'manifest_commons.json','w'),ensure_ascii=False,indent=1)
