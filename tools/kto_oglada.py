#!/usr/bin/env python3
"""Kto oglada kamery ROD: dziennik Caddy (uzytkownik, kamera, IP, czas) + go2rtc (widzowie teraz). Uzycie: kto_oglada.py [godzin wstecz]"""
import json, sys, datetime, urllib.request, collections
LOG='/var/lib/docker/volumes/caddy_mcp_data/_data/kamery_access.log'
godz=float(sys.argv[1]) if len(sys.argv)>1 else 24
od=datetime.datetime.now().timestamp()-godz*3600
sesje=collections.OrderedDict()
try:
    for l in open(LOG,encoding='utf-8'):
        try: d=json.loads(l)
        except Exception: continue
        if d.get('ts',0)<od: continue
        r=d.get('request',{}); uri=r.get('uri','')
        if '/api/ws' not in uri and '/api/frame.jpeg' not in uri: continue
        user=d.get('user_id') or '?'; kam=uri.split('src=')[-1] if 'src=' in uri else '?'
        ip=r.get('client_ip') or r.get('remote_ip','?'); t=datetime.datetime.fromtimestamp(d['ts']).strftime('%d.%m %H:%M')
        k=(user,kam,ip,t); sesje[k]=sesje.get(k,0)+1
except FileNotFoundError: print('brak dziennika')
print(f'=== ostatnie {godz:g} h: kto / kamera / IP / kiedy / polaczen ===')
for (user,kam,ip,t),n in list(sesje.items())[-40:]: print(f'{user:10s} {kam:17s} {ip:16s} {t}  x{n}')
d=json.load(urllib.request.urlopen('http://127.0.0.1:1984/api/streams',timeout=10))
print('=== TERAZ ===')
for k,v in d.items():
    cons=v.get('consumers') or []
    print(f'{k}: {len(cons)} widzow', ' | '.join((c.get('remote_addr') or '')+' '+(c.get('user_agent') or '')[:30] for c in cons))
