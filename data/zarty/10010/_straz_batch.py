import subprocess, json
B = '/root/rod-ai-studio/data/zarty/10010'
KAN = '/root/rod-ai-studio/tools/kanarek.py'
W = '/root/rod-ai-studio/assets/zarty/karty'
K = json.load(open(f'{B}/_klipy_batch.json'))
for n, d in K.items():
    cmd = ['/app/venv/bin/python', KAN, '--odcinek', '10010',
           '--klip', f'{B}/klip_{n}.mp4', '--mowca', d['mowca'],
           '--kwestia', d.get('kwestia',''), '--kadr', f'{B}/kadry/{n}.jpg',
           '--prompt', d['prompt'], '--typ', 'noc', '--domena', 'noc',
           '--wzorzec', f'BOHATER={W}/bohater_noc.jpg']
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(f"===== {n} ({d['mowca']}{', niemy' if d.get('niemy') else ''}) =====", flush=True)
    for l in r.stdout.splitlines():
        if l.startswith(('[', 'WERDYKT', '  *')):
            print(l, flush=True)
print("KONIEC STRAZNIKA 5 KLIPOW", flush=True)
