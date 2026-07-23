# -*- coding: utf-8 -*-
"""Publikacja ZARTU (serii Tomek+Janusz) na FB Reels — dedykowana, ze sciezka data/zarty/.
Kopia sprawdzonej logiki reels z topics.py, poprawiona sciezka + endpoint podgladu zartu.
Wywolanie: /app/venv/bin/python publikuj_zart.py <zid> <opis_path>"""
import sys, os, json, time
import urllib.request, urllib.parse, urllib.error

zid = sys.argv[1]
opis = open(sys.argv[2], encoding='utf-8').read().strip() if len(sys.argv) > 2 else ''

tok_path = '/root/rod-ai-studio/data/.secrets/fb_page_token'
if not os.path.isfile(tok_path):
    tok_path = '/root/rod-ai-studio/fb_page_token'
tok = open(tok_path, encoding='utf-8').read().strip()
assert tok.startswith('EAA'), 'token FB nieprawidlowy'

PAGE_ID = '1174205105781401'
V = 'v21.0'
folder = f'/root/rod-ai-studio/data/zarty/{zid}'
assert os.path.isfile(f'{folder}/final.mp4'), 'brak final.mp4'

# podglad przez nasz endpoint zartow (serwuje z dysku VPS)
video_url = f'https://panel.157-90-155-155.sslip.io/zarty/{zid}/video'

def graph_post(path, params):
    params = dict(params); params['access_token'] = tok
    url = f'https://graph.facebook.com/{V}/{path}'
    req = urllib.request.Request(url, data=urllib.parse.urlencode(params).encode(), method='POST')
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try: eb = json.loads(e.read().decode())
        except Exception: eb = {}
        msg = (eb.get('error') or {}).get('message', 'blad')
        print(f'FB_ERROR ({e.code}): {msg}'); sys.exit(3)

print('faza start...')
start = graph_post(f'{PAGE_ID}/video_reels', {'upload_phase': 'start'})
video_id = start.get('video_id'); upload_url = start.get('upload_url')
assert video_id and upload_url, 'brak video_id/upload_url'
print('video_id:', video_id)

print('faza upload (file_url)...')
up_req = urllib.request.Request(
    upload_url, data=b'',
    headers={'Authorization': 'OAuth ' + tok, 'file_url': video_url}, method='POST')
try:
    with urllib.request.urlopen(up_req, timeout=180) as r:
        r.read()
except urllib.error.HTTPError as e:
    print(f'UPLOAD_ERROR ({e.code}):', e.read().decode()[:180]); sys.exit(4)
print('upload OK')

print('faza finish (PUBLISHED)...')
fin = graph_post(f'{PAGE_ID}/video_reels', {
    'upload_phase': 'finish', 'video_id': video_id,
    'video_state': 'PUBLISHED', 'description': opis})
open(f'{folder}/opublikowano.txt', 'w', encoding='utf-8').write(
    time.strftime('%Y-%m-%d %H:%M') + ' | FB Reel video_id=' + str(video_id))
print('OPUBLIKOWANO:', f'https://www.facebook.com/reel/{video_id}')
print('finish:', json.dumps(fin)[:120])
