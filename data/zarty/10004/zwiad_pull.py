# -*- coding: utf-8 -*-
import sys, time, json, subprocess
sys.path.insert(0, '/app')
import fal_client
BAZA = '/root/rod-ai-studio/data/zarty/10004'
rid = json.load(open(f'{BAZA}/zwiad_state.json'))['request_id']
M = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
t0 = time.time()
while time.time() - t0 < 100:
    st = type(fal_client.status(M, rid)).__name__
    print(f'{time.time()-t0:5.1f}s {st}', flush=True)
    if st == 'Completed':
        res = fal_client.result(M, rid)
        url = res['video']['url']
        subprocess.run(['curl', '-sL', '-o', f'{BAZA}/zwiad_02.mp4', url], check=True)
        print('POBRANY', flush=True)
        m = json.load(open(f'{BAZA}/meta.json'))
        m['koszt_wydany'] = round(float(m.get('koszt_wydany', 0) or 0) + 0.40, 2)
        json.dump(m, open(f'{BAZA}/meta.json', 'w'), ensure_ascii=False, indent=1)
        break
    time.sleep(8)
