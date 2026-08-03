"""STRAZNIK SRODKA KLIPU: klatka z 4s -> VLM otwarte pytanie NAJPIERW, potem sedno sceny. FAIL=STOP."""
import json, base64, urllib.request, subprocess, sys
B = '/root/rod-ai-studio/data/zarty/10010'
K = json.load(open(f'{B}/_klipy_reroll.json'))
SEDNO = {
 'k02': [("Czy mężczyzna trzyma uniesioną pięść między dwiema nogawkami zwisającymi z korony drzewa?", True),
         ("Czy widać drugą osobę albo jej twarz?", False)],
 'k04': [("Czy mężczyzna trzyma uniesioną pięść między dwiema nogawkami zwisającymi z korony drzewa?", True),
         ("Czy widać drugą osobę albo jej twarz?", False)],
 'k05': [("Czy to ekstremalne zbliżenie twarzy krzyczącego mężczyzny?", True),
         ("Czy widać jakikolwiek but, gumowiec lub kalosz?", False)],
 'k06': [("Czy mężczyzna trzyma uniesioną pięść między dwiema nogawkami zwisającymi z korony drzewa?", True),
         ("Czy widać drugą osobę albo jej twarz?", False)],
}
def ask(img, q):
    p = json.dumps({"model":"qwen2.5vl:7b","stream":False,"prompt":q,"images":[img]}).encode()
    r = urllib.request.urlopen(urllib.request.Request("http://172.17.0.1:11434/api/generate", p, {"Content-Type":"application/json"}), timeout=180)
    return json.loads(r.read())["response"].strip()
fails = 0
for n in K:
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss","4","-i",f"{B}/klip_{n}_reroll.mp4",
                    "-frames:v","1","-vf","scale=768:-1",f"/tmp/sr_{n}.jpg"], check=True)
    img = base64.b64encode(open(f"/tmp/sr_{n}.jpg","rb").read()).decode()
    print(f"===== {n} — OTWARTE: =====")
    print(ask(img, "Opisz dokładnie co widzisz na tym obrazie. Po polsku.")[:400], flush=True)
    ok = True
    for q, chce_tak in SEDNO[n]:
        o = ask(img, q + " Odpowiedz jednym słowem: TAK albo NIE.")
        zgoda = o.upper().startswith("TAK") == chce_tak
        ok &= zgoda
        print(f"  SEDNO: {q} -> {o[:20]} {'OK' if zgoda else 'SPRZECZNOŚĆ'}", flush=True)
    print(f"  {n}: {'PASS' if ok else 'FAIL'}", flush=True)
    fails += 0 if ok else 1
print(f"WERDYKT: {'4/4 PASS — środek klipów trzyma sceny' if fails==0 else str(fails)+' FAIL — STOP, decyzja Tomasza'}", flush=True)
sys.exit(1 if fails else 0)
