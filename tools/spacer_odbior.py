#!/usr/bin/env python3
"""Odbiór sfer 360 z Folda PO 5G (apka MCP przez Tailscale, bez WiFi/ADB) i nazwanie numerami punktów.
Użycie: python3 tools/spacer_odbior.py --od 42 [--po "2026-09-04 18:00"] [--sucho]
Kroki: lista Pictures/My360s (lokalizacja SAF dodana 04.09) → tylko pliki nowsze niż --po → sortowanie po czasie →
p{od}, p{od+1}… → android_share_file_via_web → curl (3 próby, kontrola rozmiaru) → oryginał data/spacer_oryginaly/pNN.jpg
→ web 4096x2048 q85 → www_rod/static/spacer/pNN.jpg. Nic nie kasuje na telefonie. Zmierzone 04.09: ~1,5 MB/s, 14,7 MB w 9,7 s."""
import argparse, subprocess, json, datetime, sys, re
from pathlib import Path
LOK = 'com.android.externalstorage.documents/primary:Pictures/My360s'
ROOT = Path('/root/rod-ai-studio'); ORYG = ROOT / 'data/spacer_oryginaly'; WEB = ROOT / 'www_rod/static/spacer'

def tel(narzedzie, arg):
    out = subprocess.run(['/root/tel.sh', 'tools/call', json.dumps({'name': narzedzie, 'arguments': arg})], capture_output=True, text=True, timeout=120).stdout
    r = json.loads(out); t = r['result']['content'][0]['text']
    if r['result'].get('isError'): raise RuntimeError(t[:200])
    return t

ap = argparse.ArgumentParser(); ap.add_argument('--od', type=int, required=True); ap.add_argument('--po', default=None)
ap.add_argument('--sucho', action='store_true'); A = ap.parse_args()
t = tel('android_list_files', {'location_id': LOK, 'path': ''}); d = json.loads(t[t.find('{'):])
pliki = [f for f in d['files'] if not f['is_directory'] and f['name'].lower().endswith(('.jpg', '.jpeg'))]
if A.po:
    prog = datetime.datetime.strptime(A.po, '%Y-%m-%d %H:%M').timestamp() * 1000
    pliki = [f for f in pliki if (f['last_modified'] or 0) >= prog]
pliki.sort(key=lambda f: f['last_modified'] or 0)
print(f'plików do odbioru: {len(pliki)}')
for i, f in enumerate(pliki):
    print(f"  p{A.od + i:02d} <- {f['name']} ({f['size'] // 1_000_000} MB, {datetime.datetime.fromtimestamp((f['last_modified'] or 0) / 1000):%d.%m %H:%M:%S})")
if A.sucho: sys.exit(0)
ORYG.mkdir(parents=True, exist_ok=True); WEB.mkdir(parents=True, exist_ok=True)
from PIL import Image
for i, f in enumerate(pliki):
    nr = A.od + i; cel = ORYG / f'p{nr:02d}.jpg'
    ok = False
    for proba in range(3):
        try:
            s = tel('android_share_file_via_web', {'location_id': LOK, 'path': f['name']})
            url = re.search(r'(http://\S+/s/\S+?)(?=\s)', s).group(1)
            r = subprocess.run(['curl', '-s', '-m', '600', '-o', str(cel), url], timeout=620)
            if cel.is_file() and cel.stat().st_size == f['size']: ok = True; break
        except Exception as e: print(f'  próba {proba + 1} p{nr:02d}: {str(e)[:80]}')
    if not ok: print(f'  BŁĄD p{nr:02d} — nie pobrano całości'); continue
    im = Image.open(cel); w, h = im.size
    if abs(w / h - 2) > 0.02: print(f'  UWAGA p{nr:02d}: proporcje {w}x{h} nie 2:1')
    im.convert('RGB').resize((4096, 2048), Image.LANCZOS).save(WEB / f'p{nr:02d}.jpg', quality=85, optimize=True)
    print(f'  OK p{nr:02d}: {w}x{h}, oryginał {f["size"] // 1_000_000} MB, web {(WEB / f"p{nr:02d}.jpg").stat().st_size // 1000} KB')
