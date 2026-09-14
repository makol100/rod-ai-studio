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

ref=base64.b64encode(open("assets/izabela/IZABELA_CANON_v2.png","rb").read()).decode()
tlo=base64.b64encode(open("data/roboty/2026-09-14/dzien4_grabienie/11_20260914_180134_zdjecie.jpg","rb").read()).decode()

PROMPT=("Full body shot of the woman from <IMAGE_REF_0>, maintaining her exact face (age 50-55, distinct cheekbones, subtle wrinkles, grey streaks in hair, no makeup) "
 "and her signature formal business attire (ecru linen blazer with visible neckline). She is standing outdoors on the exact finished dirt path from <IMAGE_REF_1> (fully filled trench, raked earth). "
 "Bright natural daylight, professional photography, vertical 9:16, highly detailed, realistic. She is facing the camera with a professional, subtle smile, hands visible, medium shot from the waist up.")

c=Client(api_key=K); t0=time.time()
body=dict(
    model="gemini-3.1-flash-image",
    input=[
        {"type":"text","text":PROMPT},
        {"type":"image","data":ref,"mime_type":"image/png"},
        {"type":"image","data":tlo,"mime_type":"image/jpeg"}
    ],
    response_format={"type":"image","resolution":"1080x1920"},
    generation_config={"image_config":{"task":"reference_to_image"}}
)
try: 
    r=c.interactions.create(**body, timeout=300)
except Exception as e: 
    print("BLAD:",type(e).__name__,str(e)[:1500]); sys.exit(1)

d=r.model_dump() if hasattr(r,"model_dump") else json.loads(json.dumps(r,default=str))

n=0
out_dir="data/izabela/relacja2"
os.makedirs(out_dir, exist_ok=True)
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="data" and isinstance(v,str) and len(v)>10000: 
                global n
                n+=1
                raw=base64.b64decode(v)
                open(f"{out_dir}/izabela_stoi_v2.png","wb").write(raw)
                print("ZAPIS",f"{out_dir}/izabela_stoi_v2.png",len(raw),"B")
            else: walk(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")

walk(d)
json.dump(d,open(f"{out_dir}/izabela_response.json","w"),indent=1,ensure_ascii=False,default=str)
print("czas %.0fs | usage=%s"%(time.time()-t0, json.dumps(d.get("usage"))[:300]))
