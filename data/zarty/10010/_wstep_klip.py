"""Klip k00 (wstep-szept) — veo3.1 lite FLF, $0.64. Zgoda Tomasza 26.07 ("Budzet o 0.79$... Ruszac!") — limit force 12.60.
GUARD __main__ OBOWIAZKOWY. Submit tylko przy ZIELONYM preflighcie."""
import sys, json, subprocess
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/zarty/10010'
M = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
PF = '/root/rod-ai-studio/tools/preflight.py'
KWESTIA = 'Z\u0142odziej jab\u0142ek grasuje. Dzisiaj... koniec tej zabawy.'
PROMPT = open(f'{B}/_wstep_klip_prompt.txt', encoding='utf-8').read()

def main():
    kadr = f'{B}/kadry/k00.jpg'
    r = subprocess.run(['/app/venv/bin/python', PF, '--odcinek', '10010',
        '--mowca', 'BOHATER', '--kadr-start', kadr, '--kadr-koniec', kadr,
        '--prompt', PROMPT, '--kwestia', KWESTIA,
        '--koszt', '0.64', '--limit', '12.60'], capture_output=True, text=True)
    ok = 'ZIELONY' in r.stdout
    print(f'[pf] k00 (BOHATER): {"ZIELONY" if ok else "CZERWONY"}', flush=True)
    if not ok:
        for l in r.stdout.splitlines():
            if l.startswith(('FAIL', 'FLAG')):
                print('   ', l, flush=True)
        print('WERDYKT: CZERWONY — STOP, zero submitow', flush=True)
        sys.exit(1)
    u = fal_client.upload_file(kadr)
    h = fal_client.submit(M, arguments={'prompt': PROMPT,
        'first_frame_url': u, 'last_frame_url': u, 'duration': '8s',
        'aspect_ratio': 'auto', 'resolution': '1080p'})
    json.dump({'rid': h.request_id, 'model': M, 'koszt': 0.64},
              open(f'{B}/gen_state_wstep_k00.json', 'w'))
    print(f'[submit] k00 wystrzelony, RID={h.request_id}', flush=True)

if __name__ == '__main__':
    main()
