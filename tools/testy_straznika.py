#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUITE WZORCOWA (bieg szybki, ~3 min) — DROGA 2.4 pkt 1.
Przypadki WYŁĄCZNIE z realnych plików realnych błędów 16-17.07.
Testuje wykrycia ORAZ brak fałszywych alarmów. Zielony wynik != dowód
(bramka B — oko Tomasza — zostaje zawsze). Każdy nowy błąd = nowy przypadek.
Uruchamianie: /app/venv/bin/python /root/rod-ai-studio/tools/testy_straznika.py
"""
import ast, sys
sys.path.insert(0, '/app')
sys.path.insert(0, '/root/rod-ai-studio/tools')
from pathlib import Path
import straznik as S

B = Path('/root/rod-ai-studio/data/zarty/10004')      # golden: zamrożony odcinek (odczyt legalny)
K = Path('/root/rod-ai-studio/assets/zarty/karty')     # golden: biblioteka postaci
WYNIKI = []

def przypadek(nazwa, ok, detal=''):
    WYNIKI.append(ok)
    print(('PASS' if ok else 'FAIL'), '|', nazwa, '|', str(detal)[:90])

def jest(p, nazwa):
    if not Path(p).exists():
        przypadek(nazwa, True, 'SKIP: brak pliku golden (odnotuj i uzupełnij!)')
        return False
    return True

# 1. LINT KONFIGURACJI — duplikaty kluczy w słownikach produkcji (dowód: kurtka JÓZKA)
zrodlo = open('/app/src/zarty_produkcja.py').read()
dupy = []
for node in ast.walk(ast.parse(zrodlo)):
    if isinstance(node, ast.Dict):
        klucze = [k.value for k in node.keys if isinstance(k, ast.Constant)]
        dupy += [k for k in set(klucze) if klucze.count(k) > 1]
przypadek('lint: zero duplikatów kluczy w słownikach', not dupy, dupy or 'czysto')

# 2. JĘZYK — pozytywny: prawdziwy polski ma przejść (fałszywy alarm = też błąd)
if jest(B/'cut_05.mp4', 'język pl'):
    r = S.straznik_scenariusza(B/'cut_05.mp4', 'U nas na działce to nawet niemowa się w końcu wygada.')
    przypadek('język: cut_05 wykryty jako pl i PASS', r['status'] == 'PASS' and r['detale'].get('język') == 'pl',
              f"{r['status']}/{r['detale'].get('język')}")

# 3. JĘZYK — negatywny: słowacki lektor ma polec (dowód: odrzucony finał v7)
if jest(B/'final_k1.mp4', 'język obcy'):
    r = S.straznik_scenariusza(B/'final_k1.mp4', 'Znowu mi ktoś jabłka podżera! Idę i złapię go za jajca!')
    przypadek('język: final_k1 = obcy język = FAIL', r['status'] == 'FAIL' and r['detale'].get('język_lektora') != 'pl',
              r['detale'].get('język_lektora'))

# 4. SCENARIUSZ — klip z trzema głosami nie może dostać PASS na jednej kwestii (dowód: gen_02b)
if jest(B/'gen_02b.mp4', 'multi-kwestia'):
    r = S.straznik_scenariusza(B/'gen_02b.mp4', 'Ktoś ty? Pytam, kto ty?')
    przypadek('scenariusz: gen_02b (3 głosy) bez PASS', r['status'] != 'PASS', r['detale'].get('zgodność', r['detale']))

# 5. OCR — pozytywny: plansza MA tekst i OCR ma go czytać
if jest(B/'plansza.mp4', 'OCR+'):
    r = S.straznik_napisow(B/'plansza.mp4', tekst_dozwolony=True)
    przypadek('OCR: plansza — tekst wykryty', r['status'] == 'PASS' and r['detale'] != 'brak tekstu na klatkach', '')

# 6. OCR — negatywny: surowa generacja bez doklejonych napisów (fałszywy alarm = błąd)
if jest(B/'final_k3.mp4', 'OCR-'):
    r = S.straznik_napisow(B/'final_k3.mp4')
    przypadek('OCR: surowa generacja czysta', r['status'] == 'PASS', r['detale'] if r['status'] != 'PASS' else '')

# 6b. OCR — szum niskiej pewnosci nie moze oblewac klipu (dowod: "PAPE Yas" na klip_03 10005)
C = Path('/root/rod-ai-studio/data/zarty/10005')
if jest(C/'klip_03.mp4', 'OCR szum'):
    r = S.straznik_napisow(C/'klip_03.mp4')
    przypadek('OCR: klip_03 (szum tekstur) bez falszywego alarmu', r['status'] == 'PASS',
              r['detale'] if r['status'] != 'PASS' else '')

# 6c. TRYB FINAL — montaz z planowana liczba cieć nie moze oblac (dowod: final 10005, 1/7 wykrytych)
if jest(C/'final.mp4', 'final ciecia'):
    r = S.straznik_techniczny(C/'final.mp4', 1080, 1920, freeze_ok=True, ciecia_ok=7)
    przypadek('techniczny --final: niedoszacowanie detektora cieć = WARN nie FAIL', r['status'] != 'FAIL',
              r['detale'].get('problemy'))

# 6d/6e. Z produkcji 10006: pik OCR i graniczna twarz nie oblewaja (falszywe alarmy 17.07)
D = Path('/root/rod-ai-studio/data/zarty/10006')
if jest(D/'klip_09.mp4', 'OCR pik'):
    r = S.straznik_napisow(D/'klip_09.mp4')
    przypadek('OCR: jednoklatkowy pik = WARN nie FAIL', r['status'] != 'FAIL', r['status'])
if jest(D/'klip_12.mp4', 'twarz graniczna'):
    r = S.straznik_tozsamosci(D/'klip_12.mp4',
        {'JANUSZ': '/root/rod-ai-studio/assets/zarty/karty/janusz_baza.jpg'})
    przypadek('tożsamość: graniczna klatka (blur) = WARN nie FAIL', r['status'] != 'FAIL', r['status'])

# 7. REFERENCJE — jedna osoba na bazie, dwie na duecie (dowód: karty-duchy z 2-osobowej referencji)
try:
    import numpy as np
    tb = S._twarze(K/'bohater_baza.jpg'); tj = S._twarze(K/'janusz_baza.jpg'); td = S._twarze(K/'duet_podglad_v1.jpg')
    przypadek('referencje: bazy=1 twarz, duet=2', len(tb) == 1 and len(tj) == 1 and len(td) == 2,
              f'{len(tb)}/{len(tj)}/{len(td)}')
    sep = float(np.dot(tb[0].normed_embedding, tj[0].normed_embedding))
    przypadek('referencje: separacja postaci < 0.30', sep < 0.30, round(sep, 2))
except Exception as e:
    przypadek('referencje: insightface działa', False, repr(e)[:80])

fail = WYNIKI.count(False)
print(f'=== SUITE: {len(WYNIKI)} przypadków, FAIL: {fail} ===')
sys.exit(1 if fail else 0)
