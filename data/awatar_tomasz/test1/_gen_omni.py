import base64, json, os, sys, time, re
from google.genai import Client
K=""
for p in ("/root/.gemini/.env","/root/rod-ai-studio/.env"):
    try:
        for l in open(p):
            if l.startswith("GEMINI_API_KEY="): K=l.split("=",1)[1].strip().strip('"\''); break
    except FileNotFoundError: pass
    if K: break
assert K, "brak klucza"
img=base64.b64encode(open("ref_tomasz_720.jpg","rb").read()).decode()
PROMPT=("Use the man from <IMAGE_REF_0> as the main character. Keep his exact face: the same eyes, eyebrows, nose, "
 "lips, skin tone, age and facial proportions, so he is clearly recognizable. Change ONLY these three things: "
 "(1) his hair is short and neatly trimmed, (2) his face is completely clean-shaven, no beard and no mustache, "
 "(3) he wears a clean white button-up shirt with the top button undone, no tie. "
 "Setting: a sunny family allotment garden in Poland - vegetable beds, fruit trees, a small wooden garden shed, "
 "lush greenery softly blurred in the background, warm afternoon light. Medium close-up, vertical 9:16, single continuous shot, "
 "he stands facing the camera with a calm, friendly, confident expression, subtle natural head movements and blinks. "
 "He speaks in Polish with a native Polish accent, warm tone, lips in sync: \"Dzień dobry, tu Tomasz. Witam na naszym ogrodzie.\" "
 "Natural ambient garden sounds: birdsong, light breeze. No subtitles, no captions, no on-screen text, no logos.")
c=Client(api_key=K)
t0=time.time()
body=dict(model="gemini-omni-1.1-flash",
    input=[{"type":"text","text":PROMPT},{"type":"image","data":img,"mime_type":"image/jpeg"}],
    response_format={"type":"video","resolution":"720p","aspect_ratio":"9:16","duration":sys.argv[1] if len(sys.argv)>1 else "8s","delivery":"inline"},
    generation_config={"video_config":{"task":"reference_to_video"}})
try:
    r=c.interactions.create(**body, timeout=900)
except Exception as e:
    print("BLAD:",type(e).__name__, str(e)[:1500]); sys.exit(1)
dt=time.time()-t0
d=r.model_dump() if hasattr(r,"model_dump") else json.loads(json.dumps(r,default=str))
# wytnij base64 do pliku
def walk(o,path="",out=[]):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="data" and isinstance(v,str) and len(v)>10000:
                out.append((path,v)); o[k]=f"<{len(v)} b64 chars>"
            else: walk(v,path+"/"+k,out)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]",out)
    return out
blobs=walk(d)
n=0
for p,b in blobs:
    n+=1; raw=base64.b64decode(b); open(f"omni_test1_{n}.mp4","wb").write(raw); print("ZAPIS",f"omni_test1_{n}.mp4",len(raw),"B z",p)
json.dump(d,open("omni_test1_response.json","w"),indent=1,ensure_ascii=False,default=str)
print("czas %.0fs | id=%s | status=%s | usage=%s"%(dt,d.get("id"),d.get("status"),json.dumps(d.get("usage"))[:300]))
