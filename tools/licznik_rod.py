#!/usr/bin/env python3
"""Licznik odwiedzin rodwozniki.pl (dekret 03.09): z logu Caddy, bez cookies. Liczy odslony stron HTML i unikalnych gosci (skrot IP+dzien). Wynik: licznik.json w dist i wolumenie."""
import json, os, time, datetime, hashlib, re
LOG='/var/lib/docker/volumes/caddy_mcp_data/_data/rodwozniki_access.log'
STAN='/root/rod-ai-studio/data/licznik_rod.json'
OUTS=('/root/rod-ai-studio/www_rod/dist/licznik.json','/var/lib/docker/volumes/caddy_mcp_data/_data/www_rod/licznik.json')
BOTY=re.compile(r'bot|crawl|spider|slurp|facebookexternalhit|preview|monitor|curl|python-requests|headless',re.I)
st=json.load(open(STAN)) if os.path.exists(STAN) else {"pozycja":0,"odslony":0,"goscie":0,"dni":{},"start":"2026-09-03"}
if not os.path.exists(LOG): raise SystemExit("brak logu")
size=os.path.getsize(LOG)
if size<st["pozycja"]: st["pozycja"]=0   # log zrotowany
with open(LOG,'rb') as f:
    f.seek(st["pozycja"]); dane=f.read(); st["pozycja"]=f.tell()
for l in dane.decode('utf-8','ignore').splitlines():
    try: d=json.loads(l)
    except Exception: continue
    r=d.get('request',{}); uri=r.get('uri','')
    if d.get('status')!=200 or r.get('method')!='GET': continue
    if '/static/' in uri or uri.endswith(('.json','.xml','.txt','.png','.jpg','.svg','.css','.js','.ico')): continue
    ua=(r.get('headers',{}).get('User-Agent') or [''])[0]
    if BOTY.search(ua): continue
    dzien=datetime.datetime.fromtimestamp(d['ts'],datetime.timezone(datetime.timedelta(hours=2))).strftime('%Y-%m-%d')
    ip=r.get('client_ip') or r.get('remote_ip','')
    klucz=hashlib.sha256(f"{ip}|{dzien}".encode()).hexdigest()[:16]
    dz=st["dni"].setdefault(dzien,{"odslony":0,"goscie":[]})
    dz["odslony"]+=1; st["odslony"]+=1
    if klucz not in dz["goscie"]: dz["goscie"].append(klucz); st["goscie"]+=1
# nie trzymaj skrotow starszych niz 2 dni
dzis=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).strftime('%Y-%m-%d')
for k in list(st["dni"]):
    if k<dzis and isinstance(st["dni"][k].get("goscie"),list): st["dni"][k]["goscie"]=len(st["dni"][k]["goscie"])
json.dump(st,open(STAN,'w'),ensure_ascii=False)
d=st["dni"].get(dzis,{"odslony":0,"goscie":[]}); g=d["goscie"] if isinstance(d["goscie"],int) else len(d["goscie"])
out={"dzis_goscie":g,"dzis_odslony":d["odslony"],"lacznie_goscie":st["goscie"],"lacznie_odslony":st["odslony"],"od":st["start"]}
for p in OUTS:
    try: open(p+'.tmp','w').write(json.dumps(out)); os.chmod(p+'.tmp',0o644); os.replace(p+'.tmp',p)
    except Exception as e: print('zapis',p,e)
print('licznik:', out)
