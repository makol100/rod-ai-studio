import subprocess, json
B = '/root/rod-ai-studio/data/zarty/10009'
KAN = '/root/rod-ai-studio/tools/kanarek.py'
W = '/root/rod-ai-studio/assets/zarty/karty'
K = json.load(open(f'{B}/_klipy_meta.json'))
for n, d in K.items():
    cmd = ['/app/venv/bin/python', KAN, '--odcinek', '10009',
           '--klip', f'{B}/klip_{n}.mp4', '--mowca', d['mowca'],
           '--kwestia', d.get('kwestia',''), '--kadr', f'{B}/kadry/{n}.jpg',
           '--prompt', d['prompt'], '--domena', 'zmierzch']
    for w in d['wzorce']:
        cmd += ['--wzorzec', w]
    r = subprocess.run(cmd, capture_output=True, text=True)
    werdykt = [l for l in r.stdout.splitlines() if 'WERDYKT' in l or l.startswith('[')]
    print(f"===== {n} =====", flush=True)
    for l in werdykt:
        print(l, flush=True)
print("KONIEC STRAZNIKA", flush=True)
