import sys, json, os, subprocess
import fal_client
B = '/root/rod-ai-studio/data/wiadomosci/0001-teren'
st = json.load(open(f'{B}/_kling_0001_state.json'))
if os.path.exists(f'{B}/work/stanislaw_0001_raw.mp4'):
    print('JUZ POBRANY'); sys.exit(0)
s = fal_client.status(st['model'], st['rid'])
n = type(s).__name__
if n != 'Completed':
    print('STATUS:', n); sys.exit(0)
res = fal_client.result(st['model'], st['rid'])
json.dump(res, open(f'{B}/_kling_0001_resp.json', 'w'))
url = (res.get('video') or {}).get('url')
if not url:
    print('BRAK URL:', json.dumps(res)[:250]); sys.exit(1)
subprocess.run(['curl', '-sL', '-o', f'{B}/work/stanislaw_0001_raw.mp4', url], check=True)
print('POBRANY')
