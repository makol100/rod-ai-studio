#!/usr/bin/env python3
"""Kto oglada kamery ROD: dziennik /kamery/auth (user, kamera, IP, czas) + go2rtc (widzowie teraz). Uzycie: kto_oglada.py [godzin wstecz]"""
import json, sys, datetime, urllib.request, collections
LOG='/root/rod-ai-studio/data/kamery_dostepy.jsonl'
godz=float(sys.argv[1]) if len(sys.argv)>1 else 24
od=datetime.datetime.now().timestamp()-godz*3600
sesje=collections.OrderedDict()
try:
    for l in open(LOG,encoding='utf-8'):
        try: d=json.loads(l)
        except Exception: continue
        if d.get('ts',0)<od or '/api/ws' not in d.get('uri',''): continue
        k=(d.get('user','?'), d['uri'].split('src=')[-1], d.get('ip','?'), datetime.datetime.fromtimestamp(d['ts'],datetime.timezone(datetime.timedelta(hours=2))).strftime('%d.%m %H:%M'))
        sesje[k]=sesje.get(k,0)+1
except FileNotFoundError: print('brak dziennika')
print(f'=== ostatnie {godz:g} h: kto / kamera / IP / kiedy / polaczen ===')
for (user,kam,ip,t),n in list(sesje.items())[-40:]: print(f'{user:10s} {kam:17s} {ip:16s} {t}  x{n}')
d=json.load(urllib.request.urlopen('http://127.0.0.1:1984/api/streams',timeout=10))
print('=== TERAZ ===')
for k,v in d.items():
    cons=v.get('consumers') or []
    print(f'{k}: {len(cons)} widzow', ' | '.join((c.get('remote_addr') or '')+' '+(c.get('user_agent') or '')[:30] for c in cons))
