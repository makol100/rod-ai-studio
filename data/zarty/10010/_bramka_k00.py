"""BRAMKA KADRU k00 (wstep): VLM otwarty opis + sedno wg checklisty Zenka + tozsamosc insightface vs bohater_noc.jpg. FAIL=STOP."""
import json, base64, urllib.request, subprocess, sys
import numpy as np
B = '/root/rod-ai-studio/data/zarty/10010'
REF = '/root/rod-ai-studio/assets/zarty/karty/bohater_noc.jpg'

def ask(img, q):
    p = json.dumps({"model":"qwen2.5vl:7b","stream":False,"prompt":q,"images":[img]}).encode()
    r = urllib.request.urlopen(urllib.request.Request("http://172.17.0.1:11434/api/generate", p, {"Content-Type":"application/json"}), timeout=180)
    return json.loads(r.read())["response"].strip()

subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{B}/kadry/k00.jpg","-vf","scale=768:-1","/tmp/k00s.jpg"], check=True)
img = base64.b64encode(open("/tmp/k00s.jpg","rb").read()).decode()
print("===== k00 — OTWARTY OPIS: =====")
print(ask(img, "Opisz dokładnie co widzisz na tym obrazie. Po polsku.")[:500], flush=True)

SEDNO = [
 ("Czy na obrazie jest dokładnie jeden mężczyzna, kucający lub skradający się nocą w sadzie?", True),
 ("Czy jego oczy i usta są wyraźnie widoczne i oświetlone?", True),
 ("Czy w jego czapce lub przy głowie tkwi mała gałązka?", True),
 ("Czy górna część obrazu to ciemna, pusta przestrzeń bez twarzy i bez tekstu?", True),
 ("Czy widać drugą osobę albo jej twarz?", False),
 ("Czy dłonie i ciało wyglądają anatomicznie naturalnie?", True),
]
fails = 0
for q, chce_tak in SEDNO:
    o = ask(img, q + " Odpowiedz jednym słowem: TAK albo NIE.")
    zgoda = o.upper().startswith("TAK") == chce_tak
    fails += 0 if zgoda else 1
    print(f"  SEDNO: {q} -> {o[:24]} {'OK' if zgoda else 'SPRZECZNOŚĆ'}", flush=True)

from insightface.app import FaceAnalysis
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640,640))
import cv2
def emb(p):
    f = app.get(cv2.imread(p))
    return f[0].normed_embedding if f else None
e1, e2 = emb(f"{B}/kadry/k00.jpg"), emb(REF)
if e1 is None or e2 is None:
    print("  TOZSAMOSC: brak twarzy do pomiaru — FAIL", flush=True); fails += 1
else:
    cos = float(np.dot(e1, e2))
    ok = cos >= 0.35
    fails += 0 if ok else 1
    print(f"  TOZSAMOSC vs bohater_noc: cos={cos:.3f} (prog 0.35) {'OK' if ok else 'FAIL'}", flush=True)
print(f"WERDYKT: {'PASS — kadr k00 do Veo' if fails==0 else str(fails)+' FAIL — STOP, decyzja Tomasza'}", flush=True)
sys.exit(1 if fails else 0)
