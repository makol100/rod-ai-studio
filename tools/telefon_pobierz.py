#!/usr/bin/env python3
"""Pobiera z Folda (apka MCP po Tailscale/5G) pliki z lokalizacji SAF nowsze niż podana data.
Użycie: python3 tools/telefon_pobierz.py --lok DCIM --path Camera --od "2026-09-08 00:00" --do KATALOG [--sucho]
Lokalizacje: DCIM, Pictures, My360s."""
import argparse, json, subprocess, datetime, re, sys
from pathlib import Path
LOK={'DCIM':'com.android.externalstorage.documents/primary:DCIM','Pictures':'com.android.externalstorage.documents/primary:Pictures','My360s':'com.android.externalstorage.documents/primary:Pictures/My360s'}
def tel(n,a,timeout=150):
    out=subprocess.run(['/root/tel.sh','tools/call',json.dumps({'name':n,'arguments':a})],capture_output=True,text=True,timeout=timeout).stdout
    r=json.loads(out); t=r['result']['content'][0]['text']
    if r['result'].get('isError'): raise RuntimeError(t[:200])
    return t
ap=argparse.ArgumentParser(); ap.add_argument('--lok',required=True); ap.add_argument('--path',default=''); ap.add_argument('--od',required=True); ap.add_argument('--do',required=True); ap.add_argument('--sucho',action='store_true')
A=ap.parse_args(); lok=LOK[A.lok]; prog=datetime.datetime.strptime(A.od,'%Y-%m-%d %H:%M').timestamp()*1000
pliki=[]; off=0
while True:
    t=tel('android_list_files',{'location_id':lok,'path':A.path,'offset':off,'limit':200}); d=json.loads(t[t.find('{'):])
    f=d['files']; pliki+= [x for x in f if not x['is_directory'] and (x['last_modified'] or 0)>=prog]
    if len(f)<200: break
    off+=200
pliki.sort(key=lambda x:x['last_modified'])
print(f'nowszych niż {A.od}: {len(pliki)}')
for x in pliki: print(' ',x['name'],x['size']//1000,'KB',datetime.datetime.fromtimestamp(x['last_modified']/1000).strftime('%d.%m %H:%M:%S'))
if A.sucho: sys.exit(0)
cel=Path(A.do); cel.mkdir(parents=True,exist_ok=True)
for x in pliki:
    out=cel/x['name']
    if out.is_file() and out.stat().st_size==x['size']: print('  jest',x['name']); continue
    ok=False
    for p in range(3):
        try:
            s=tel('android_share_file_via_web',{'location_id':lok,'path':(A.path+'/' if A.path else '')+x['name']})
            url=re.search(r'(http://\S+/s/\S+?)(?=\s)',s).group(1)
            subprocess.run(['curl','-s','-m','900','-o',str(out),url],timeout=920)
            if out.is_file() and out.stat().st_size==x['size']: ok=True; break
        except Exception as e: print('  próba',p+1,x['name'],str(e)[:80])
    print('  OK' if ok else '  BŁĄD',x['name'],out.stat().st_size//1000 if out.is_file() else 0,'KB')
