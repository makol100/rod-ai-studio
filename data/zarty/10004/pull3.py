import sys, json, subprocess
sys.path.insert(0, '/app')
import fal_client
B = '/root/rod-ai-studio/data/zarty/10004'
import os
for nr, out in [('01','gen_01.mp4'), ('02a','gen_02a.mp4'), ('02b','gen_02b.mp4')]:
    if os.path.exists(f'{B}/{out}'):
        continue
    st = json.load(open(f'{B}/gen_state_{nr}.json'))
    s = fal_client.status(st['model'], st['rid'])
    if type(s).__name__ != 'Completed':
        print(nr, 'jeszcze:', type(s).__name__); continue
    try:
        res = fal_client.result(st['model'], st['rid'])
    except Exception as e:
        print(nr, 'ODRZUCONY:', ('policy' if 'content_policy' in str(e) else str(e)[:80])); continue
    subprocess.run(['curl','-sL','-o',f'{B}/{out}',res['video']['url']], check=True)
    m = json.load(open(f'{B}/meta.json'))
    m['koszt_wydany'] = round(float(m.get('koszt_wydany',0) or 0) + st['koszt'], 2)
    json.dump(m, open(f'{B}/meta.json','w'), ensure_ascii=False, indent=1)
    print(nr, 'POBRANY')
