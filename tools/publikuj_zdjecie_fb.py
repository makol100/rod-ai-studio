#!/usr/bin/env python3
"""Publikacja POSTU ZE ZDJECIEM na stronie FB ROD Wozniki (Graph API /photos).

Uzycie:
    python3 tools/publikuj_zdjecie_fb.py <url_zdjecia> <plik_z_opisem>
    python3 tools/publikuj_zdjecie_fb.py <url_zdjecia> <plik_z_opisem> --sprawdz

<url_zdjecia> musi byc publicznie dostepny (np. https://rodwozniki.pl/static/...png)
--sprawdz  = tylko pokaz co poszloby na FB, nie publikuj.

Token: data/.secrets/fb_page_token (ten sam co reelsy).
"""
import sys, os, json, urllib.request, urllib.parse, urllib.error, time

PAGE_ID = '1174205105781401'
V = 'v21.0'
ROOT = '/root/rod-ai-studio'

if len(sys.argv) < 3:
    print(__doc__); sys.exit(1)

url_zdjecia = sys.argv[1]
opis = open(sys.argv[2], encoding='utf-8').read().strip()
sucho = '--sprawdz' in sys.argv

if sucho:
    print('--- URL ZDJECIA:', url_zdjecia)
    print('--- OPIS ({} znakow):\n{}'.format(len(opis), opis))
    sys.exit(0)

tok_path = f'{ROOT}/data/.secrets/fb_page_token'
if not os.path.isfile(tok_path):
    tok_path = f'{ROOT}/fb_page_token'
tok = open(tok_path, encoding='utf-8').read().strip()
assert tok.startswith('EAA'), 'token FB nieprawidlowy'

params = {'url': url_zdjecia, 'message': opis, 'published': 'true', 'access_token': tok}
req = urllib.request.Request(f'https://graph.facebook.com/{V}/{PAGE_ID}/photos',
                             data=urllib.parse.urlencode(params).encode(), method='POST')
try:
    with urllib.request.urlopen(req, timeout=90) as r:
        wynik = json.load(r)
except urllib.error.HTTPError as e:
    try: eb = json.loads(e.read().decode())
    except Exception: eb = {}
    print('FB_ERROR ({}): {}'.format(e.code, (eb.get('error') or {}).get('message', 'blad')))
    sys.exit(3)

print('OPUBLIKOWANO:', json.dumps(wynik, ensure_ascii=False))
post_id = wynik.get('post_id') or wynik.get('id')
if post_id:
    print('LINK: https://www.facebook.com/{}'.format(post_id))
    os.makedirs(f'{ROOT}/data/fb_posty', exist_ok=True)
    with open(f'{ROOT}/data/fb_posty/opublikowane.log', 'a', encoding='utf-8') as f:
        f.write('{} | {} | {}\n'.format(time.strftime('%Y-%m-%d %H:%M'), post_id, url_zdjecia))
