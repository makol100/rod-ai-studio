import base64, json, os, sys, time
from google.genai import Client
# Omni — Prezenter Tomasz, wydanie Alejka Polnocna cd. (D-0355). Wzorzec: relacja_alejka/_gen_A.py (08.09, PASS).
# Uzycie: python3 _gen_omni.py <nazwa> <duration np. 10s>   (kwestia z KWESTIE[nazwa])
B = "/root/rod-ai-studio/data/wiadomosci/tauron_apki/omni"
import importlib.util as _u; _s=_u.spec_from_file_location("k", B+"/KWESTIE.py"); _m=_u.module_from_spec(_s); _s.loader.exec_module(_m); KWESTIE=_m.KWESTIE
_STARE = {
 "K1": "Dzień dobry, tu Tomasz. Kable w górnej alejce są położone i zasypane. Teraz do dwóch tygodni dajemy czas na uleżenie gleby i kabla.",
 "K2": "Potem podłączymy kable do poszczególnych zabezpieczonych miejsc licznikowych, przypisanych do danej działki.",
 "K4": "Z tym pismem przychodzą Państwo do zarządu, do mnie — Tomasza Maksysia. Wydam kartę danych technicznych, w skrócie ka-de-te.",
}
nazwa = sys.argv[1]; dur = sys.argv[2] if len(sys.argv) > 2 else "10s"
KWESTIA = KWESTIE[nazwa]
K = ""
for p in ("/root/.gemini/.env", "/root/rod-ai-studio/.env"):
    try:
        for l in open(p):
            if l.startswith("GEMINI_API_KEY="): K = l.split("=", 1)[1].strip().strip('"\''); break
    except FileNotFoundError: pass
    if K: break
assert K
ref = base64.b64encode(open(f"{B}/ref_tomasz_720.jpg", "rb").read()).decode()
PROMPT = ("Use the man from <IMAGE_REF_0> as the main character. Keep his exact face: the same eyes, eyebrows, nose, "
 "lips, skin tone, age and facial proportions, so he is clearly recognizable. Change ONLY these three things: "
 "(1) his hair is short and neatly trimmed, (2) his face is completely clean-shaven, no beard and no mustache, "
 "(3) he wears a clean white button-up shirt with the top button undone, no tie. "
 "Setting: a clean, seamless, evenly lit PURE WHITE studio background (#ffffff), like a professional explainer video, nothing else in the frame. "
 "Medium close-up, vertical 9:16, single continuous shot, he stands facing the camera with a calm, friendly, confident expression like a news presenter, "
 "subtle natural head movements and blinks, hands relaxed, no pointing. "
 "He speaks in Polish with a native Polish accent, warm clear tone, unhurried, lips in sync: \"" + KWESTIA + "\" "
 "Natural quiet ambient garden sounds: birdsong, light breeze. No subtitles, no captions, no on-screen text, no logos.")
c = Client(api_key=K); t0 = time.time()
body = dict(model="gemini-omni-1.1-flash",
    input=[{"type": "text", "text": PROMPT}, {"type": "image", "data": ref, "mime_type": "image/jpeg"}],
    response_format={"type": "video", "resolution": "720p", "aspect_ratio": "9:16", "duration": dur, "delivery": "inline"},
    generation_config={"video_config": {"task": "reference_to_video"}})
try: r = c.interactions.create(**body, timeout=900)
except Exception as e: print("BLAD:", type(e).__name__, str(e)[:1500]); sys.exit(1)
d = r.model_dump() if hasattr(r, "model_dump") else json.loads(json.dumps(r, default=str))
def walk(o, path="", out=None):
    out = [] if out is None else out
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "data" and isinstance(v, str) and len(v) > 10000: out.append((path, v)); o[k] = f"<{len(v)} b64>"
            else: walk(v, path + "/" + k, out)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f"{path}[{i}]", out)
    return out
pliki = walk(d)
if pliki:
    raw = base64.b64decode(pliki[0][1]); open(f"{B}/omni_{nazwa}.mp4", "wb").write(raw); print("ZAPIS", f"omni_{nazwa}.mp4", len(raw), "B")
json.dump(d, open(f"{B}/omni_{nazwa}_response.json", "w"), indent=1, ensure_ascii=False, default=str)
print("czas %.0fs | status=%s | usage=%s" % (time.time() - t0, d.get("status"), json.dumps(d.get("usage"))[:200]))
