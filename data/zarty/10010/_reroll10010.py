"""Re-roll 10010: k02,k04,k05,k06 w rezimie statycznym (prompty pracownika + poprawki szefa).
Dane w _klipy_reroll.json. GUARD __main__. Submit tylko przy 4/4 ZIELONYCH preflightach."""
import sys, json, subprocess
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/zarty/10010'
M = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
PF = '/root/rod-ai-studio/tools/preflight.py'
K = json.load(open(f'{B}/_klipy_reroll.json'))

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
        print('WERDYKT: CZERWONY — STOP, zero submitow', flush=True)
        sys.exit(1)
    print('[reroll] 4/4 ZIELONY — submit', flush=True)
    for n, d in K.items():
        u = fal_client.upload_file(f'{B}/kadry/{n}.jpg')
        h = fal_client.submit(M, arguments={'prompt': d['prompt'],
            'first_frame_url': u, 'last_frame_url': u, 'duration': '8s',
            'aspect_ratio': 'auto', 'resolution': '1080p'})
        json.dump({'rid': h.request_id, 'model': M, 'koszt': 0.64},
                  open(f'{B}/gen_state_reroll_{n}.json', 'w'))
        print(f'[reroll] {n} RID: {h.request_id}', flush=True)
    print('WERDYKT: 4/4 ZIELONY — submity poszly ($2.56)', flush=True)

if __name__ == '__main__':
    main()
