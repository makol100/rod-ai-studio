import sys, json, os, subprocess
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/wiadomosci/0001-teren'
st = json.load(open(f'{B}/_avatar_0001_state.json'))
if os.path.exists(f'{B}/wd0001_avatar_raw.mp4'):
    print('JUZ POBRANY'); sys.exit(0)
s = fal_client.status(st['model'], st['rid'])
n = type(s).__name__
if n != 'Completed':
    print('STATUS:', n); sys.exit(0)
try:
    res = fal_client.result(st['model'], st['rid'])
except Exception as e:
    print('BLAD WYNIKU:', str(e)[:200]); sys.exit(1)
json.dump(res, open(f'{B}/_avatar_0001_resp.json', 'w'))
url = (res.get('video') or {}).get('url')
if not url:
    print('BRAK URL:', json.dumps(res)[:250]); sys.exit(1)
subprocess.run(['curl', '-sL', '-o', f'{B}/wd0001_avatar_raw.mp4', url], check=True)
print('POBRANY: wd0001_avatar_raw.mp4')
