#!/usr/bin/env python3
"""Odbiór sfer 360 z Folda przez ADB (Tailscale 100.101.116.106:PORT) i nazwanie numerami punktów.
Użycie: python3 tools/spacer_odbior.py --port 46009 --od 47 [--po "2026-09-04 18:00"] [--folder /sdcard/Pictures/My360s]
Kroki: adb connect → lista jpg w folderze (domyślnie szuka folderów 360 w /sdcard) → tylko pliki nowsze niż --po →
sortowanie po czasie → p{od}.jpg, p{od+1}.jpg… → oryginały data/spacer_oryginaly/ → web 4096x2048 q85 → www_rod/static/spacer/.
Nic nie kasuje na telefonie."""
import argparse, subprocess, sys, re, datetime
from pathlib import Path
ADB = '/root/platform-tools/adb'; TEL = '100.101.116.106'
ROOT = Path('/root/rod-ai-studio'); ORYG = ROOT / 'data/spacer_oryginaly'; WEB = ROOT / 'www_rod/static/spacer'
KANDYDACI = ['/sdcard/Pictures/My360s', '/sdcard/DCIM/360PhotoCam', '/sdcard/Pictures/360PhotoCam', '/sdcard/DCIM/Camera', '/sdcard/Pictures']

def adb(*a, timeout=120):
    r = subprocess.run([ADB, '-s', f'{TEL}:{PORT}', *a], capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or '') + (r.stderr or '')

ap = argparse.ArgumentParser()
ap.add_argument('--port', required=True); ap.add_argument('--od', type=int, required=True)
ap.add_argument('--po', default=None, help='tylko pliki nowsze niż (YYYY-MM-DD HH:MM, czas telefonu)')
ap.add_argument('--folder', default=None); ap.add_argument('--sucho', action='store_true', help='tylko lista, bez kopiowania')
A = ap.parse_args(); PORT = A.port
rc, out = subprocess.run([ADB, 'connect', f'{TEL}:{PORT}'], capture_output=True, text=True, timeout=30).returncode, ''
r = subprocess.run([ADB, 'connect', f'{TEL}:{PORT}'], capture_output=True, text=True, timeout=30); print('connect:', (r.stdout + r.stderr).strip())
if 'connected' not in (r.stdout + r.stderr): sys.exit(1)

foldery = [A.folder] if A.folder else KANDYDACI
pliki = []
for f in foldery:
    rc, out = adb('shell', f'ls -l --time-style=+%s "{f}" 2>/dev/null')
    if rc != 0 or not out.strip(): continue
    for lin in out.splitlines():
        m = re.match(r'^-\S+\s+\d+\s+\S+\s+\S+\s+(\d+)\s+(\d+)\s+(.+\.(?:jpg|jpeg|JPG))$', lin.strip())
        if m:
            roz, ts, nazwa = int(m.group(1)), int(m.group(2)), m.group(3)
            if roz > 3_000_000: pliki.append((ts, roz, f + '/' + nazwa))
    if pliki and A.folder is None: print('folder ze sferami:', f); break
if A.po:
    prog = datetime.datetime.strptime(A.po, '%Y-%m-%d %H:%M').timestamp()
    pliki = [p for p in pliki if p[0] >= prog]
pliki.sort()
print(f'plików do odbioru: {len(pliki)}')
for i, (ts, roz, sc) in enumerate(pliki):
    print(f'  p{A.od + i:02d} <- {sc} ({roz // 1_000_000} MB, {datetime.datetime.fromtimestamp(ts):%H:%M:%S})')
if A.sucho: sys.exit(0)
ORYG.mkdir(parents=True, exist_ok=True); WEB.mkdir(parents=True, exist_ok=True)
from PIL import Image
for i, (ts, roz, sc) in enumerate(pliki):
    nr = A.od + i; cel = ORYG / f'p{nr:02d}.jpg'
    for proba in range(3):
        rc, out = adb('pull', sc, str(cel), timeout=600)
        if rc == 0 and cel.is_file() and cel.stat().st_size == roz: break
        print(f'  ponawiam pull p{nr:02d} ({proba + 1})')
    else:
        print(f'  BŁĄD pobrania p{nr:02d}'); continue
    im = Image.open(cel); w, h = im.size
    if abs(w / h - 2) > 0.02: print(f'  UWAGA p{nr:02d}: proporcje {w}x{h} nie 2:1')
    im.convert('RGB').resize((4096, 2048), Image.LANCZOS).save(WEB / f'p{nr:02d}.jpg', quality=85, optimize=True)
    print(f'  OK p{nr:02d}: oryginał {roz // 1_000_000} MB, web {(WEB / f"p{nr:02d}.jpg").stat().st_size // 1000} KB')
