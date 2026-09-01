# -*- coding: utf-8 -*-
"""Publikacja dowolnego pliku mp4 na FB Reels strony ROD — upload BINARNY (panel jest za loginem, file_url nie dziala).
Wywolanie: python3 tools/publikuj_prezenter.py <plik.mp4> <opis.txt>"""
import sys, os, json, time, urllib.request, urllib.parse, urllib.error
plik=sys.argv[1]; opis=open(sys.argv[2],encoding='utf-8').read().strip()
tok_path='/root/rod-ai-studio/data/.secrets/fb_page_token'
if not os.path.isfile(tok_path): tok_path='/root/rod-ai-studio/fb_page_token'
tok=open(tok_path,encoding='utf-8').read().strip(); assert tok.startswith('EAA'),'token FB nieprawidlowy'
PAGE_ID='1174205105781401'; V='v21.0'
def graph_post(path, params):
    params=dict(params); params['access_token']=tok
    req=urllib.request.Request(f'https://graph.facebook.com/{V}/{path}', data=urllib.parse.urlencode(params).encode(), method='POST')
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        try: eb=json.loads(e.read().decode())
        except Exception: eb={}
        print(f'FB_ERROR ({e.code}):', (eb.get('error') or {}).get('message','blad')); sys.exit(3)
size=os.path.getsize(plik); print('plik:',plik,size,'B')
start=graph_post(f'{PAGE_ID}/video_reels', {'upload_phase':'start'})
video_id=start.get('video_id'); upload_url=start.get('upload_url'); assert video_id and upload_url
print('video_id:',video_id)
data=open(plik,'rb').read()
req=urllib.request.Request(upload_url, data=data, headers={'Authorization':'OAuth '+tok,'offset':'0','file_size':str(size),'Content-Type':'application/octet-stream'}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=600) as r: print('upload:', r.read().decode()[:200])
except urllib.error.HTTPError as e:
    print(f'UPLOAD_ERROR ({e.code}):', e.read().decode()[:300]); sys.exit(4)
fin=graph_post(f'{PAGE_ID}/video_reels', {'upload_phase':'finish','video_id':video_id,'video_state':'PUBLISHED','description':opis})
print('finish:', json.dumps(fin)[:200])
# status
for i in range(12):
    time.sleep(10)
    q=urllib.parse.urlencode({'fields':'status','access_token':tok})
    try:
        with urllib.request.urlopen(f'https://graph.facebook.com/{V}/{video_id}?{q}', timeout=30) as r: st=json.load(r).get('status',{})
    except Exception as ex: st={'err':str(ex)[:80]}
    print('status:', json.dumps(st)[:220])
    if st.get('video_status') in ('ready','published') or st.get('publishing_phase',{}).get('status')=='complete': break
os.makedirs(os.path.dirname(plik), exist_ok=True)
open(os.path.join(os.path.dirname(plik),'opublikowano.txt'),'a',encoding='utf-8').write(time.strftime('%Y-%m-%d %H:%M')+' | FB Reel video_id='+str(video_id)+' | '+os.path.basename(plik)+'\n')
print('OPUBLIKOWANO:', f'https://www.facebook.com/reel/{video_id}')
