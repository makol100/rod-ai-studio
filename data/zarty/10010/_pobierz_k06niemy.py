"""Pobranie 4 klipow re-rollu po RID (gen_state_k06niemy_*.json) -> klip_kXX_niemy.mp4 (+faststart podglad na panel)."""
import sys, json, glob, subprocess
sys.path.insert(0, '/app')
import fal_client, requests

B = '/root/rod-ai-studio/data/zarty/10010'
P = '/root/rod-ai-studio/data/n150files'
gotowe, czekamy = [], []
for g in sorted(glob.glob(f'{B}/gen_state_k06niemy_*.json')):
    n = g.split('k06niemy_')[1].split('.')[0]
    s = json.load(open(g))
    st = type(fal_client.status(s['model'], s['rid'])).__name__
    if 'Completed' not in st:
        czekamy.append(f'{n}:{st}')
        continue
    res = fal_client.result(s['model'], s['rid'])
    url = res['video']['url']
    out = f'{B}/klip_{n}_niemy.mp4'
    r = requests.get(url, timeout=180); r.raise_for_status()
    open(out, 'wb').write(r.content)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out,'-c','copy',
                    '-movflags','+faststart', f'{P}/10010_klip_{n}_niemy.mp4'], check=True)
    gotowe.append(n)
    print(f'[dl] {n} OK ({len(r.content)} B) + podglad na panelu', flush=True)
print(f'GOTOWE: {gotowe} | CZEKAMY: {czekamy}', flush=True)
