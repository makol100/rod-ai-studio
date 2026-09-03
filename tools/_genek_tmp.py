import json, base64, urllib.request, sys
D = "/root/rod-ai-studio/data/zarty/10012/kadry/"
def vlm(sciezka):
    b64 = base64.b64encode(open(sciezka, 'rb').read()).decode()
    body = json.dumps({"model": "qwen2.5vl:7b", "stream": False,
        "prompt": "Describe exactly what you see in this image.",
        "images": [b64]}).encode()
    req = urllib.request.Request("http://172.17.0.1:11434/api/generate", data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=180).read())["response"]
for k in ["k01", "k02", "k03", "k04", "k05"]:
    print(f"--- {k} ---")
    print(vlm(D + k + ".jpg"))
