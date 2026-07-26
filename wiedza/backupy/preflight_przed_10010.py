#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PREFLIGHT — bramka "1000% pewne w Veo" (DROGA 2.5+, decyzja Tomasza 17.07).
Sprawdza WSZYSTKO przed submitem; bez zielonego werdyktu submit jest ZAKAZANY.
Użycie:
/app/venv/bin/python tools/preflight.py --odcinek 10005 --mowca JANUSZ \
  --kwestia "..." --kadr-start X.jpg --kadr-koniec Y.jpg --prompt "..." [--koszt 0.64]
Kontrole: kwestia VERBATIM w kanonie DECYZJI • blok głosu mówcy z GLOSY_VEO
w prompcie • "native Polish" • "no captions" • dokładnie JEDEN mówca (jedna para
cudzysłowów dialogowych) • słowa-miny (flaga) • kadry: istnieją, proporcja ~9:16,
twarz mówcy obecna (insightface vs biblioteka) • budżet odcinka.
"""
import argparse, json, re, sys, unicodedata
sys.path.insert(0, '/app')
from pathlib import Path

MINY = ['kill', 'attack', 'weapon', 'gun', 'knife', 'blood', 'terrified', 'terror',
        'eliminat', 'violence', 'coerc', 'child', 'minor', 'niemowa', 'inwazj']
BIBLIO = {'BOHATER': '/root/rod-ai-studio/assets/zarty/karty/bohater_baza.jpg',
          'JANUSZ':  '/root/rod-ai-studio/assets/zarty/karty/janusz_baza.jpg'}

def norm(t):
    t = unicodedata.normalize('NFC', t).lower()
    t = re.sub(r'\s+', ' ', t)  # łamania linii kanonu → spacja (bug: sklejanie słów)
    return re.sub(r'[^a-ząćęłńóśźż ]', '', t)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--odcinek', required=True)
    ap.add_argument('--mowca', required=True)
    ap.add_argument('--kwestia', default='')
    ap.add_argument('--bez-dialogu', action='store_true')
    ap.add_argument('--kadr-start', required=True)
    ap.add_argument('--kadr-koniec', required=True)
    ap.add_argument('--prompt', required=True)
    ap.add_argument('--koszt', type=float, default=0.64)
    ap.add_argument('--limit', type=float, default=6.0)
    a = ap.parse_args()
    R, flagi = [], []

    def test(nazwa, ok, detal=''):
        R.append(ok); print(('PASS' if ok else 'FAIL'), '|', nazwa, '|', str(detal)[:100])

    if not a.bez_dialogu and not a.kwestia:
        print('FAIL | podaj --kwestia albo --bez-dialogu'); sys.exit(1)
    # 1. Kwestia VERBATIM w kanonie (DECYZJE odcinka)
    kanon_p = Path(f'/root/rod-ai-studio/data/zarty/{a.odcinek}/KANON.md')
    if not kanon_p.exists():  # fallback: uruchomienie na hoście
        kanon_p = next(Path('/root/rod-ai-studio/wiedza').glob(f'DECYZJE_{a.odcinek}*.md'),
                       kanon_p)
    kanon = kanon_p.read_text() if kanon_p.exists() else ''
    test('kanon: plik DECYZJI odcinka istnieje', bool(kanon), kanon_p.name)
    if not a.bez_dialogu:
        test('kanon: kwestia VERBATIM w kanonie', norm(a.kwestia) in norm(kanon))

    # 2. Prompt: kwestia w cudzysłowie, głos, native Polish, no captions
    from src.zarty_produkcja import GLOSY_VEO
    glos = GLOSY_VEO.get(a.mowca, '')
    if not a.bez_dialogu:
        test('głos: mówca ma zdefiniowany głos w GLOSY_VEO', bool(glos), a.mowca)
    if not a.bez_dialogu:
        test('prompt: kwestia obecna w prompcie', norm(a.kwestia)[:40] in norm(a.prompt))
    if not a.bez_dialogu:
        test('prompt: blok głosu mówcy obecny', glos.lower() in a.prompt.lower())
    if not a.bez_dialogu:
        test('prompt: native Polish accent', 'native polish' in a.prompt.lower())
    test('prompt: no captions', 'no captions' in a.prompt.lower())

    # 3. Dokładnie JEDEN mówca (jedna para cudzysłowów dialogowych)
    cyt = re.findall(r'"([^"]{3,})"', a.prompt)
    if a.bez_dialogu:
        test('dialog: klip niemy — zero kwestii w cudzysłowie', len(cyt) == 0, f'znaleziono {len(cyt)}')
    else:
        test('dialog: dokładnie jedna kwestia w cudzysłowie', len(cyt) == 1, f'znaleziono {len(cyt)}')

    # 4. Słowa-miny (FLAGA, nie bloker)
    trafienia = [m for m in MINY if m in a.prompt.lower()]
    if trafienia:
        flagi.append(f'słowa-miny w prompcie: {trafienia} — przepisz / homofon / safety=6')
        print('FLAG |', flagi[-1])

    # 5. Kadry: istnienie, proporcja, twarz mówcy
    try:
        import cv2, numpy as np
        from insightface.app import FaceAnalysis
        app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        app.prepare(ctx_id=-1, det_size=(640, 640))
        wz = app.get(cv2.imread(BIBLIO[a.mowca]))
        wz = [t for t in wz if t.det_score >= 0.6][0].normed_embedding
        for rola, sciezka in [('start', a.kadr_start), ('koniec', a.kadr_koniec)]:
            p = Path(sciezka)
            test(f'kadr {rola}: istnieje', p.exists(), p.name)
            if not p.exists():
                continue
            im = cv2.imread(str(p)); h, w = im.shape[:2]
            test(f'kadr {rola}: proporcja ~9:16', abs(w / h - 9 / 16) < 0.02, f'{w}x{h}')
            tw = [t for t in app.get(im) if t.det_score >= 0.6]
            sims = [float(np.dot(t.normed_embedding, wz)) for t in tw]
            test(f'kadr {rola}: twarz mówcy obecna (sim≥0.35)', any(s >= 0.35 for s in sims),
                 [round(s, 2) for s in sims] or 'brak twarzy')
    except Exception as e:
        test('kadry: analiza twarzy działa', False, repr(e)[:90])

    # 6. Konto fal aktywne (sonda blokady salda — darmowy token-probe)
    import os, urllib.request
    req = urllib.request.Request(
        'https://rest.fal.ai/storage/auth/token?storage_type=fal-cdn-v3',
        data=b'{}', method='POST',
        headers={'Authorization': 'Key ' + os.environ.get('FAL_KEY', ''),
                 'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req, timeout=10)
        test('saldo: konto fal aktywne', True)
    except urllib.error.HTTPError as e:
        tresc = e.read().decode()[:120]
        test('saldo: konto fal aktywne', False, tresc)

    # 7. Budżet odcinka
    meta_p = Path(f'/root/rod-ai-studio/data/zarty/{a.odcinek}/meta.json')
    wydane = json.load(open(meta_p)).get('koszt_wydany', 0.0) if meta_p.exists() else 0.0
    test('budżet: koszt klipu mieści się w limicie', wydane + a.koszt <= a.limit,
         f'{wydane} + {a.koszt} <= {a.limit}')

    fail = R.count(False)
    print(f'=== PREFLIGHT: {len(R)} kontroli, FAIL: {fail}, FLAG: {len(flagi)} ===')
    print('WERDYKT:', 'ZIELONY — submit dozwolony' if fail == 0 else 'CZERWONY — submit ZAKAZANY')
    sys.exit(1 if fail else 0)

if __name__ == '__main__':
    main()
