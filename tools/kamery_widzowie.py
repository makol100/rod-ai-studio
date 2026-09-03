#!/usr/bin/env python3
"""Co 5 s zapisuje widzowie.json dla strony kamer: ilu oglada (go2rtc) + kto (dziennik /kamery/auth z ostatnich 60 s)."""
import json, time, datetime, urllib.request, os, collections
LOG='/root/rod-ai-studio/data/kamery_dostepy.jsonl'
OUT='/var/lib/docker/volumes/caddy_mcp_data/_data/www_kamery/widzowie.json'
NAZWY={'parking_wjazd':'Wjazd','parking_wejscie':'Wejście','parking_smietnik':'Śmietnik'}
def kto(od):
    who=collections.defaultdict(set)
    try:
        with open(LOG,'rb') as f:
            f.seek(0,2); size=f.tell(); f.seek(max(0,size-200000)); tail=f.read().decode('utf-8','ignore')
        for l in tail.splitlines():
            try: d=json.loads(l)
            except Exception: continue
            if d.get('ts',0)<od or '/api/ws' not in d.get('uri',''): continue
            who[d['uri'].split('src=')[-1]].add(d.get('user') or '?')
    except FileNotFoundError: pass
    return who
while True:
    try:
        d=json.load(urllib.request.urlopen('http://127.0.0.1:1984/api/streams',timeout=5))
        who=kto(time.time()-60); kam=[]; razem=0
        for k,n in NAZWY.items():
            c=max(len((d.get(k) or {}).get('consumers') or []), len(who.get(k,[]))); razem+=c
            kam.append({'kamera':n,'widzow':c,'kto':sorted(who.get(k,[])) if c else []})
        out={'ts':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).strftime('%H:%M'),'razem':razem,'kamery':kam}
        tmp=OUT+'.tmp'; open(tmp,'w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False)); os.chmod(tmp,0o644); os.replace(tmp,OUT)
    except Exception as e:
        try: open(OUT,'w').write(json.dumps({'blad':str(e)[:80]}))
        except Exception: pass
    time.sleep(5)
