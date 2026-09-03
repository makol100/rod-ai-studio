import json
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
konce = {}
for n in ["k02", "k03", "k04"]:
    segs, _ = m.transcribe(f"/root/rod-ai-studio/data/zarty/10012/{n}.mp4", language="pl")
    segs = list(segs)
    konce[n] = round(max(s.end for s in segs), 2) if segs else 8.0
    print(n, "koniec mowy:", konce[n], "| segmenty:", [(round(s.start,1), round(s.end,1)) for s in segs], flush=True)
konce["k01"] = 8.0; konce["k05"] = 8.0
json.dump(konce, open("/root/rod-ai-studio/data/zarty/10012/_konce.json", "w"))
print("zapisane _konce.json", flush=True)
