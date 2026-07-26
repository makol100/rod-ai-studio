"""Batch 10010: 5 klipow (k01,k02 nieme; k03,k05 Tomek; k06 puenta Jozka).
Dane w _klipy_batch.json (lekcja: dane poza skryptem z efektami).
GUARD __main__ OBOWIAZKOWY. Submit tylko przy komplecie ZIELONYCH preflightow."""
import sys, json, subprocess
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/zarty/10010'
M = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
PF = '/root/rod-ai-studio/tools/preflight.py'
K = json.load(open(f'{B}/_klipy_batch.json'))

def preflight(n, d):
    kadr = f'{B}/kadry/{n}.jpg'
    cmd = ['/app/venv/bin/python', PF, '--odcinek', '10010', '--mowca', d['mowca'],
           '--kadr-start', kadr, '--kadr-koniec', kadr, '--prompt', d['prompt'],
           '--koszt', '0.64', '--limit', '12.0']
    if d.get('niemy'):
        cmd += ['--bez-dialogu']
    else:
        cmd += ['--kwestia', d['kwestia']]
    r = subprocess.run(cmd, capture_output=True, text=True)
    ok = 'ZIELONY' in r.stdout
    print(f'[pf] {n} ({d["mowca"]}): {"ZIELONY" if ok else "CZERWONY"}', flush=True)
    if not ok:
        for l in r.stdout.splitlines():
            if l.startswith(('FAIL', 'FLAG')):
                print('   ', l, flush=True)
    return ok

def main():
    wyniki = {n: preflight(n, d) for n, d in K.items()}
    if not all(wyniki.values()):
        print('[batch] STOP — nie wszystkie zielone, ZERO submitow', flush=True)
        sys.exit(1)
    print('[batch] 5/5 ZIELONY — submit', flush=True)
    for n, d in K.items():
        u = fal_client.upload_file(f'{B}/kadry/{n}.jpg')
        h = fal_client.submit(M, arguments={'prompt': d['prompt'],
            'first_frame_url': u, 'last_frame_url': u, 'duration': '8s',
            'aspect_ratio': 'auto', 'resolution': '1080p'})
        json.dump({'rid': h.request_id, 'model': M, 'koszt': 0.64},
                  open(f'{B}/gen_state_batch_{n}.json', 'w'))
        print(f'[batch] {n} RID: {h.request_id}', flush=True)
    print('[batch] KONIEC SUBMITOW', flush=True)

if __name__ == '__main__':
    main()
