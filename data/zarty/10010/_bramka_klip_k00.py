"""BRAMKA KLIPU k00 (wstep-szept) wg narady finalnej: whisper verbatim+pauza, RMS szeptu vs k03,
tozsamosc klatek vs kadr k00 (+noc pomocniczo), usta w 4 fazach (VLM), MAD kalibrowany na k03. FAIL=STOP."""
import json, base64, re, subprocess, sys, urllib.request, unicodedata
sys.path.insert(0, '/app')
import numpy as np
import cv2

B = '/root/rod-ai-studio/data/zarty/10010'
KLIP = f'{B}/klip_k00.mp4'
KADR = f'{B}/kadry/k00.jpg'
NOC = '/root/rod-ai-studio/assets/zarty/karty/bohater_noc.jpg'
W2 = 'Złodziej jabłek grasuje. Dzisiaj... koniec tej zabawy.'
fails = 0

def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    return re.sub(r'[^a-z0-9ąćęłńóśźż ]', '', s.replace('ł', 'ł')).replace('  ', ' ').strip()

def test(nazwa, ok, info=''):
    global fails
    fails += 0 if ok else 1
    print(f"  {'OK  ' if ok else 'FAIL'} | {nazwa}" + (f' | {info}' if info else ''), flush=True)

# ===== 1. AUDIO + WHISPER =====
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', KLIP, '-vn', '-ac', '1',
                '-ar', '16000', f'{B}/k00_a.wav'], check=True)
from faster_whisper import WhisperModel
m = WhisperModel('medium', device='cpu', compute_type='int8')
segs, _ = m.transcribe(f'{B}/k00_a.wav', language='pl', vad_filter=True, word_timestamps=True)
ws = [w for s in segs for w in s.words]
print('WHISPER:', ' '.join(f"[{w.word.strip()} {w.start:.2f}-{w.end:.2f}]" for w in ws), flush=True)
trans = ' '.join(w.word.strip() for w in ws)
test('whisper: kwestia VERBATIM W2', norm(trans) == norm(W2), f'uslyszal: "{trans}"')

pauza_ok, pauza_val = False, -1.0
idx_dz = [i for i, w in enumerate(ws) if norm(w.word) == 'dzisiaj']
if idx_dz and idx_dz[0] + 1 < len(ws):
    i = idx_dz[0]
    pauza_val = ws[i + 1].start - ws[i].end
    pauza_ok = 0.5 <= pauza_val <= 1.0
test('pauza po "Dzisiaj" 0.6-0.8s (tol. 0.5-1.0)', pauza_ok, f'zmierzono {pauza_val:.2f}s')

# ===== 2. SZEPT: RMS mowy k00 vs krzyczane pytanie k03 =====
def rms_db(wav, t0, t1):
    r = subprocess.run(['ffmpeg', '-loglevel', 'info', '-ss', str(t0), '-to', str(t1),
                        '-i', wav, '-af', 'astats=measure_overall=RMS_level:measure_perchannel=none',
                        '-f', 'null', '-'], capture_output=True, text=True)
    m2 = re.search(r'RMS level dB:\s*(-?[\d.]+)', r.stderr)
    return float(m2.group(1)) if m2 else None

t0, t1 = (ws[0].start, ws[-1].end) if ws else (0, 6)
rms_k00 = rms_db(f'{B}/k00_a.wav', t0, t1)
rms_k03 = rms_db(f'{B}/k03_a.wav', 0.4, 2.8)
roznica = (rms_k03 - rms_k00) if (rms_k00 is not None and rms_k03 is not None) else -99
test('szept: RMS >=3dB cichszy niz pytanie k03', roznica >= 3.0,
     f'k00={rms_k00} dB, k03={rms_k03} dB, roznica {roznica:.1f} dB')

# ===== 3. TOZSAMOSC: klatki co 1s vs kadr k00 (glowny) + noc (pomocniczo) =====
from insightface.app import FaceAnalysis
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

def emb_img(img):
    f = app.get(img)
    return f[0].normed_embedding if f else None

e_kadr = emb_img(cv2.imread(KADR))
e_noc = emb_img(cv2.imread(NOC))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', KLIP, '-vf', 'fps=1',
                '/tmp/k00f_%02d.jpg'], check=True)
import glob
cos_k, cos_n, brak = [], [], 0
for f in sorted(glob.glob('/tmp/k00f_*.jpg')):
    e = emb_img(cv2.imread(f))
    if e is None:
        brak += 1
        continue
    cos_k.append(float(np.dot(e, e_kadr)))
    cos_n.append(float(np.dot(e, e_noc)))
test('tozsamosc: twarz wykrywalna na klatkach', brak <= 2, f'brak twarzy na {brak} klatkach')
test('tozsamosc vs KADR k00: min cos >= 0.35', bool(cos_k) and min(cos_k) >= 0.35,
     f'min={min(cos_k):.3f} mean={np.mean(cos_k):.3f}' if cos_k else 'brak pomiaru')
if cos_n:
    print(f'  INFO | pomocniczo vs bohater_noc: min={min(cos_n):.3f} mean={np.mean(cos_n):.3f}', flush=True)

# ===== 4. USTA W 4 FAZACH (VLM) wg timestampow =====
def ask(img64, q):
    p = json.dumps({"model": "qwen2.5vl:7b", "stream": False, "prompt": q, "images": [img64]}).encode()
    r = urllib.request.urlopen(urllib.request.Request("http://172.17.0.1:11434/api/generate",
        p, {"Content-Type": "application/json"}), timeout=180)
    return json.loads(r.read())["response"].strip()

def klatka64(t):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', KLIP,
                    '-frames:v', '1', '-vf', 'scale=768:-1', '/tmp/k00_faza.jpg'], check=True)
    return base64.b64encode(open('/tmp/k00_faza.jpg', 'rb').read()).decode()

if pauza_val > 0 and idx_dz:
    i = idx_dz[0]
    fazy = [
        ('A artykulacja fr.1', (ws[0].start + ws[i].end) / 2,
         'Czy usta mężczyzny są otwarte lub w trakcie mówienia?', True),
        ('B pauza — usta domkniete', ws[i].end + pauza_val / 2,
         'Czy usta mężczyzny są całkowicie zamknięte?', True),
        ('C artykulacja fr.2', (ws[i + 1].start + ws[-1].end) / 2,
         'Czy usta mężczyzny są otwarte lub w trakcie mówienia?', True),
        ('D po kwestii — efekt karpia', min(ws[-1].end + 0.5, 7.8),
         'Czy usta mężczyzny są zamknięte?', True),
    ]
    for nazwa, t, q, chce in fazy:
        o = ask(klatka64(t), q + ' Odpowiedz jednym słowem: TAK albo NIE.')
        test(f'usta {nazwa} (t={t:.2f}s)', o.upper().startswith('TAK') == chce, f'VLM: {o[:24]}')
else:
    test('usta: fazy wg timestampow', False, 'brak pauzy — nie wyznaczono faz')

print('OPIS klatki pauzy (B):', ask(klatka64(ws[idx_dz[0]].end + pauza_val / 2) if (pauza_val > 0 and idx_dz) else klatka64(4.0),
      'Opisz dokładnie twarz i usta mężczyzny na tym obrazie. Po polsku.')[:300], flush=True)

# ===== 5. MAD kalibrowany: ruch k00 vs zdrowy k03 (podobny plan) =====
def mad_ruchu(video, t_od=3.0, t_do=5.0):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t_od), '-to', str(t_do),
                    '-i', video, '-vf', 'fps=2,scale=192:-1,format=gray', '/tmp/mad_%02d.png'], check=True)
    fr = [cv2.imread(f, 0).astype(np.float32) for f in sorted(glob.glob('/tmp/mad_*.png'))]
    subprocess.run('rm -f /tmp/mad_*.png', shell=True)
    if len(fr) < 2:
        return None
    return float(np.mean([np.abs(fr[i + 1] - fr[i]).mean() for i in range(len(fr) - 1)]))

mad_k00 = mad_ruchu(KLIP)
mad_k03 = mad_ruchu(f'{B}/klip_k03.mp4')
if mad_k03:
    ok_mad = mad_k00 is not None and 0.3 * mad_k03 <= mad_k00 <= 3.0 * mad_k03
    test('MAD srodka w widelkach [0.3x, 3x] zdrowego k03', ok_mad,
         f'k00={mad_k00:.2f} vs k03={mad_k03:.2f}')
else:
    print(f'  INFO | MAD k00={mad_k00} (brak kalibratora k03 — pomiar bez werdyktu)', flush=True)

print(f"WERDYKT: {'PASS — klip k00 przyjety do montazu' if fails == 0 else str(fails) + ' FAIL — STOP, decyzja Tomasza'}", flush=True)
sys.exit(1 if fails else 0)
