"""Odbior batcha 10012 (k01,k02,k03,k05)."""
import sys, json, os
sys.path.insert(0, '/app')
import requests, fal_client
B = '/root/rod-ai-studio/data/zarty/10012'

def main():
    for nr in ['k01','k02','k03','k05']:
        if os.path.exists(f'{B}/{nr}.mp4'):
            print(nr, 'juz jest'); continue
        st = json.load(open(f'{B}/gen_state_{nr}.json'))
        s = fal_client.status(st['model'], st['rid'])
        if type(s).__name__ != 'Completed':
            print(nr, 'jeszcze:', type(s).__name__); continue
        try:
            res = fal_client.result(st['model'], st['rid'])
        except Exception as e:
            print(nr, 'ODRZUCONY:', ('policy' if 'content_policy' in str(e) else str(e)[:120])); continue
        r = requests.get(res['video']['url'], timeout=300); r.raise_for_status()
        open(f'{B}/{nr}.mp4','wb').write(r.content)
        mp = f'{B}/meta.json'
        m = json.load(open(mp)) if os.path.exists(mp) else {}
        m['koszt_wydany'] = round(float(m.get('koszt_wydany',0) or 0) + st['koszt'], 2)
        json.dump(m, open(mp,'w'), ensure_ascii=False, indent=1)
        print(nr, 'POBRANY', os.path.getsize(f'{B}/{nr}.mp4'), 'B')

if __name__ == '__main__':
    main()
