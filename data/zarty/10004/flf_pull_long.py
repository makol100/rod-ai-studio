# -*- coding: utf-8 -*-
import sys, time, json, subprocess, datetime
sys.path.insert(0, '/app')
import fal_client
BAZA = '/root/rod-ai-studio/data/zarty/10004'
def log(t):
    with open(f'{BAZA}/log.txt', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now():%H:%M:%S} {t}\n")
st = json.load(open(f'{BAZA}/flf_state_02.json'))
rid, M = st['rid'], st['model']
t0 = time.time()
while time.time() - t0 < 1500:
    s = type(fal_client.status(M, rid)).__name__
    if s == 'Completed':
        res = fal_client.result(M, rid)
        subprocess.run(['curl', '-sL', '-o', f'{BAZA}/klip_02.mp4', res['video']['url']], check=True)
        m = json.load(open(f'{BAZA}/meta.json'))
        m['koszt_wydany'] = round(float(m.get('koszt_wydany', 0) or 0) + 1.20, 2)
        json.dump(m, open(f'{BAZA}/meta.json', 'w'), ensure_ascii=False, indent=1)
        log(f"K2 v5 POBRANY przez watchdog ({int(time.time()-t0)}s czekania)")
        break
    if s not in ('Queued', 'InProgress'):
        log(f"K2 v5 watchdog: status {s} — STOP"); break
    time.sleep(20)
else:
    log("K2 v5 watchdog: 25 min minelo, job wciaz w fal — rid zostaje")
