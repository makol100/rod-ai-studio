"""Pobranie klipu wstepu k00 po RID (gen_state_wstep_k00.json) -> klip_k00.mp4 + faststart podglad na panel."""
import sys, json, subprocess
sys.path.insert(0, '/app')
import fal_client, requests
B = '/root/rod-ai-studio/data/zarty/10010'
P = '/root/rod-ai-studio/data/n150files'
s = json.load(open(f'{B}/gen_state_wstep_k00.json'))
st = type(fal_client.status(s['model'], s['rid'])).__name__
print(f'status: {st}', flush=True)
if 'Completed' not in st:
    sys.exit(2)
res = fal_client.result(s['model'], s['rid'])
url = res['video']['url']
out = f'{B}/klip_k00.mp4'
r = requests.get(url, timeout=180); r.raise_for_status()
open(out, 'wb').write(r.content)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out,'-c','copy',
                '-movflags','+faststart', f'{P}/10010_klip_k00.mp4'], check=True)
print(f'[dl] k00 OK ({len(r.content)} B) + podglad na panelu', flush=True)
