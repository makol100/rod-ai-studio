import base64, json, os, sys, time
from google.genai import Client
seg=sys.argv[1]; prev=sys.argv[2] if len(sys.argv)>2 and sys.argv[2]!="-" else None
dur=sys.argv[3] if len(sys.argv)>3 else "10s"
K=""
for p in ("/root/.gemini/.env","/root/rod-ai-studio/.env"):
    try:
        for l in open(p):
            if l.startswith("GEMINI_API_KEY="): K=l.split("=",1)[1].strip().strip('"\''); break
    except FileNotFoundError: pass
    if K: break
kw=json.load(open(os.environ.get("KWESTIE","kwestie.json")))[seg]
WYGLAD=("Use the man from <IMAGE_REF_0> as the main character. Keep his exact face: the same eyes, eyebrows, nose, lips, skin tone, "
 "age and facial proportions, clearly recognizable. Change ONLY: short neatly trimmed hair, completely clean-shaven face (no beard, no mustache), "
 "a clean white button-up shirt with the top button undone, no tie. Setting: a sunny family allotment garden in Poland - vegetable beds, "
 "fruit trees, a small wooden garden shed, lush greenery softly blurred in the background, warm afternoon light. Medium close-up, vertical 9:16, "
 "single continuous static shot, he stands facing the camera with a calm, friendly, confident expression, subtle natural head movements and blinks. ")
if prev:
    prompt=("Extend this video: continue the exact same continuous shot without any cut - the same man, the same face, the same voice and tone, "
            "the same framing, lighting and garden background. He keeps looking at the camera and continues speaking in Polish with a native Polish accent, "
            f"lips in sync. He says the line EXACTLY ONCE in one calm continuous breath, clearly and fluently, never repeating any word or phrase, then, after the last word, he smiles warmly and gives a small nod without saying anything more: \"{kw}\" "+(" After the last word he gives a small welcoming nod and keeps a warm, inviting smile at the camera until the end." if seg=="6" else "")+" Natural ambient garden sounds continue. No subtitles, no captions, no on-screen text, no logos.")
    inp=[{"type":"text","text":prompt}]
    vc={"task":"extend"}
else:
    prompt=(WYGLAD+f"He speaks in Polish with a native Polish accent, warm tone, lips in sync: \"{kw}\" "
            "Natural ambient garden sounds: birdsong, light breeze. No subtitles, no captions, no on-screen text, no logos.")
    img=base64.b64encode(open("/root/rod-ai-studio/data/awatar_tomasz/test1/ref_tomasz_720.jpg","rb").read()).decode()
    inp=[{"type":"text","text":prompt},{"type":"image","data":img,"mime_type":"image/jpeg"}]
    iref=os.environ.get("IREF")
    if iref:
        ib=base64.b64encode(open(iref,"rb").read()).decode()
        inp[0]["text"]=prompt.replace("Use the man from <IMAGE_REF_0> as the main character.","Use the man from <IMAGE_REF_0> as the main character. <IMAGE_REF_1> is a still from the previous scene of the same video: keep the same hairstyle, the same white shirt, the same camera framing, lighting and garden background as in <IMAGE_REF_1>.")
        inp.append({"type":"image","data":ib,"mime_type":"image/jpeg"})
    vc={"task":"reference_to_video"}
body=dict(model="gemini-omni-1.1-flash", input=inp,
    response_format={"type":"video","resolution":"720p","aspect_ratio":"9:16","duration":dur,"delivery":"inline"},
)
if prev: body["previous_interaction_id"]=prev
else: body["generation_config"]={"video_config":vc}
c=Client(api_key=K); t0=time.time()
try: r=c.interactions.create(**body, timeout=900)
except Exception as e: print("BLAD:",type(e).__name__,str(e)[:1200]); sys.exit(1)
d=r.model_dump()
blob=None
def walk(o):
    global blob
    if isinstance(o,dict):
        for k,v in list(o.items()):
            if k=="data" and isinstance(v,str) and len(v)>10000:
                if blob is None: blob=v
                o[k]=f"<{len(v)} b64>"
            else: walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(d)
out=f"omni_seg{seg}{os.environ.get('SUFIKS','')}.mp4"
if blob: open(out,"wb").write(base64.b64decode(blob))
json.dump(d,open(f"omni_seg{seg}_resp.json","w"),indent=1,ensure_ascii=False,default=str)
u=d.get("usage") or {}
vt=sum(x.get("tokens",0) for x in u.get("output_tokens_by_modality",[]) if x.get("modality")=="video")
print(f"SEG {seg} | {time.time()-t0:.0f}s | id={d.get('id')} | status={d.get('status')} | video_tok={vt} (~${vt*17.5/1e6:.2f}) | plik={out} {os.path.getsize(out) if blob else 0} B")
