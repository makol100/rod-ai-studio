"""Bramka A na kadrach 10012: twarze, tozsamosc i otwarty opis VLM."""
import base64
import json
import urllib.request

import cv2, numpy as np
from insightface.app import FaceAnalysis

K = "/root/rod-ai-studio/assets/zarty/karty/"
D = "/root/rod-ai-studio/data/zarty/10012/kadry/"
PLAN = {"k01": "JANUSZ", "k02": "BOHATER", "k03": "BOHATER", "k04": "JANUSZ", "k05": "JANUSZ"}
KARTY = {"JANUSZ": K+"janusz_baza.jpg", "BOHATER": K+"bohater_baza.jpg"}
DET_THRESHOLD = 0.6
SIM_THRESHOLD = 0.35
VLM_URL = "http://172.17.0.1:11434/api/generate"
VLM_MODEL = "qwen2.5vl:7b"
VLM_PROMPT = "describe what you see"

app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=-1, det_size=(640, 640))
wz = {}
for n, p in KARTY.items():
    im = cv2.imread(p)
    if im is None:
        raise RuntimeError(f"Nie mozna odczytac karty: {p}")
    wszystkie = app.get(im)
    twarze = [x for x in wszystkie if x.det_score >= DET_THRESHOLD]
    if len(twarze) != 1:
        raise RuntimeError(
            f"Karta {n}: oczekiwano 1 twarzy det>={DET_THRESHOLD}, jest {len(twarze)}"
        )
    wz[n] = twarze[0].normed_embedding
    print(
        f"REFERENCJA {n} plik:{p} twarze:{len(twarze)} "
        f"det:{float(twarze[0].det_score):.6f}",
        flush=True,
    )

def vlm(sciezka):
    with open(sciezka, "rb") as obraz:
        b64 = base64.b64encode(obraz.read()).decode()
    body = json.dumps({"model": VLM_MODEL, "stream": False,
        "prompt": VLM_PROMPT,
        "images": [b64]}).encode()
    req = urllib.request.Request(VLM_URL, data=body,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as odpowiedz:
        payload = json.loads(odpowiedz.read())
    return payload["response"]

print(
    f"KONFIG model:{VLM_MODEL} url:{VLM_URL} prompt:{VLM_PROMPT!r} "
    f"det>={DET_THRESHOLD} sim>={SIM_THRESHOLD} oczekiwane_twarze:1",
    flush=True,
)

for k, postac in PLAN.items():
    sciezka = D + k + ".jpg"
    im = cv2.imread(sciezka)
    if im is None:
        raise RuntimeError(f"Nie mozna odczytac kadru: {sciezka}")
    h, w = im.shape[:2]
    wszystkie = app.get(im)
    tw = [t for t in wszystkie if t.det_score >= DET_THRESHOLD]
    dets = [round(float(t.det_score), 6) for t in tw]
    sims_raw = [float(np.dot(t.normed_embedding, wz[postac])) for t in tw]
    sims = [round(s, 6) for s in sims_raw]
    prop_ok = abs(w / h - 9 / 16) < 0.02
    toz_ok = any(s >= SIM_THRESHOLD for s in sims_raw)
    licz_ok = len(tw) == 1
    print(
        f"=== {k} [{postac}] plik:{sciezka} {w}x{h} "
        f"prop:{'OK' if prop_ok else 'FAIL'} twarze:{len(tw)} "
        f"liczba:{'OK' if licz_ok else 'FAIL'} det:{dets} sim:{sims} "
        f"tozsamosc:{'OK' if toz_ok else 'FAIL'}",
        flush=True,
    )
    print(f"VLM_PROMPT {k}: {VLM_PROMPT}", flush=True)
    print(f"VLM_RESPONSE_BEGIN {k}", flush=True)
    print(vlm(sciezka), flush=True)
    print(f"VLM_RESPONSE_END {k}", flush=True)
