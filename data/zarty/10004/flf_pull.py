# -*- coding: utf-8 -*-
import sys, time, json, subprocess
sys.path.insert(0, '/app')
import fal_client
BAZA = '/root/rod-ai-studio/data/zarty/10004'
st = json.load(open(f'{BAZA}/flf_state_02.json'))
rid, M = st['rid'], st['model']
t0 = time.time()
while time.time() - t0 < 95:
    s = type(fal_client.status(M, rid)).__name__
    print(f'{time.time()-t0:5.1f}s {s}', flush=True)
    if s == 'Completed':
        res = fal_client.result(M, rid)
        subprocess.run(['curl', '-sL', '-o', f'{BAZA}/klip_02.mp4', res['video']['url']], check=True)
        m = json.load(open(f'{BAZA}/meta.json'))
        m['koszt_wydany'] = round(float(m.get('koszt_wydany', 0) or 0) + 1.20, 2)
        json.dump(m, open(f'{BAZA}/meta.json', 'w'), ensure_ascii=False, indent=1)
        print('POBRANY, koszt +1.20', flush=True)
        break
    time.sleep(10)
