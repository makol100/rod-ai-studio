"""Odbior kanarka k04 10012."""
import sys, json, os
import requests
sys.path.insert(0, '/app')
import fal_client
B = '/root/rod-ai-studio/data/zarty/10012'

def main():
    if os.path.exists(f'{B}/k04.mp4'):
        print('k04.mp4 juz jest'); return
    st = json.load(open(f'{B}/gen_state_k04.json'))
    s = fal_client.status(st['model'], st['rid'])
    if type(s).__name__ != 'Completed':
        print('jeszcze:', type(s).__name__); return
    try:
        res = fal_client.result(st['model'], st['rid'])
    except Exception as e:
        print('ODRZUCONY:', ('policy' if 'content_policy' in str(e) else str(e)[:120])); return
    r = requests.get(res['video']['url'], timeout=300)
    r.raise_for_status()
    open(f'{B}/k04.mp4','wb').write(r.content)
    mp = f'{B}/meta.json'
    m = json.load(open(mp)) if os.path.exists(mp) else {}
    m['koszt_wydany'] = round(float(m.get('koszt_wydany',0) or 0) + st['koszt'], 2)
    json.dump(m, open(mp,'w'), ensure_ascii=False, indent=1)
    print('k04 POBRANY', os.path.getsize(f'{B}/k04.mp4'), 'B')

if __name__ == '__main__':
    main()
