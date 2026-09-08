import base64, json, os, sys, time
from google.genai import Client
K=""
for p in ("/root/.gemini/.env","/root/rod-ai-studio/.env"):
    try:
        for l in open(p):
            if l.startswith("GEMINI_API_KEY="): K=l.split("=",1)[1].strip().strip('"\''); break
    except FileNotFoundError: pass
    if K: break
assert K
ref=base64.b64encode(open("ref_tomasz_720.jpg","rb").read()).decode()
tlo=base64.b64encode(open("tlo_alejka_720.jpg","rb").read()).decode()
KWESTIA="Dzień dobry, tu Tomasz. Zaczęliśmy kłaść kabel w górnej alejce — prace ruszyły. Spójrzcie na mapę."
PROMPT=("Use the man from <IMAGE_REF_0> as the main character. Keep his exact face: the same eyes, eyebrows, nose, "
 "lips, skin tone, age and facial proportions, so he is clearly recognizable. Change ONLY these three things: "
 "(1) his hair is short and neatly trimmed, (2) his face is completely clean-shaven, no beard and no mustache, "
 "(3) he wears a clean white button-up shirt with the top button undone, no tie. "
 "Setting: he stands in the exact garden alley shown in <IMAGE_REF_1> - a grassy allotment path in Poland with a freshly dug trench, "
 "piles of soil and a small yellow mini excavator behind him, hedges and fruit trees on both sides, soft overcast daylight; "
 "the background is that real photo scene, slightly out of focus. Medium close-up, vertical 9:16, single continuous shot, "
 "he stands facing the camera with a calm, friendly, confident expression, subtle natural head movements and blinks, "
 "a small gesture pointing to his side at the end. "
 "He speaks in Polish with a native Polish accent, warm clear tone, lips in sync: \""+KWESTIA+"\" "
 "Natural ambient garden sounds: birdsong, light breeze, distant excavator hum. No subtitles, no captions, no on-screen text, no logos.")
dur=sys.argv[1] if len(sys.argv)>1 else "12s"
c=Client(api_key=K); t0=time.time()
body=dict(model="gemini-omni-1.1-flash",
    input=[{"type":"text","text":PROMPT},{"type":"image","data":ref,"mime_type":"image/jpeg"},{"type":"image","data":tlo,"mime_type":"image/jpeg"}],
    response_format={"type":"video","resolution":"720p","aspect_ratio":"9:16","duration":dur,"delivery":"inline"},
    generation_config={"video_config":{"task":"reference_to_video"}})
try: r=c.interactions.create(**body, timeout=900)
except Exception as e: print("BLAD:",type(e).__name__,str(e)[:1500]); sys.exit(1)
d=r.model_dump() if hasattr(r,"model_dump") else json.loads(json.dumps(r,default=str))
def walk(o,path="",out=[]):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="data" and isinstance(v,str) and len(v)>10000: out.append((path,v)); o[k]=f"<{len(v)} b64>"
            else: walk(v,path+"/"+k,out)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]",out)
    return out
n=0
for p,b in walk(d):
    n+=1; raw=base64.b64decode(b); open(f"omni_A_{n}.mp4","wb").write(raw); print("ZAPIS",f"omni_A_{n}.mp4",len(raw),"B")
json.dump(d,open("omni_A_response.json","w"),indent=1,ensure_ascii=False,default=str)
print("czas %.0fs | id=%s | status=%s | usage=%s"%(time.time()-t0,d.get("id"),d.get("status"),json.dumps(d.get("usage"))[:300]))
