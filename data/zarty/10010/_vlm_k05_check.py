import json, base64, urllib.request, subprocess, sys
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",
 "/root/rod-ai-studio/data/zarty/10010/kadry/k05.jpg","-vf","scale=768:-1","/tmp/k05_n.jpg"], check=True)
img = base64.b64encode(open('/tmp/k05_n.jpg','rb').read()).decode()
def ask(q):
    p = json.dumps({"model":"qwen2.5vl:7b","stream":False,"prompt":q,"images":[img]}).encode()
    r = urllib.request.urlopen(urllib.request.Request("http://172.17.0.1:11434/api/generate", p, {"Content-Type":"application/json"}), timeout=120)
    return json.loads(r.read())["response"].strip()
otw = ask("Opisz dokładnie co widzisz na tym obrazie. Po polsku.")
but = ask("Czy na obrazie widać jakikolwiek but, gumowiec lub kalosz? Odpowiedz jednym słowem: TAK albo NIE.")
twarz = ask("Czy twarz mężczyzny wygląda naturalnie, bez zniekształceń i artefaktów? Odpowiedz jednym słowem: TAK albo NIE.")
print("OPIS OTWARTY:", otw)
print("BUT W KADRZE:", but)
print("TWARZ NATURALNA:", twarz)
ok = but.upper().startswith("NIE") and twarz.upper().startswith("TAK")
print("WERDYKT:", "PASS — gumowiec usunięty, twarz czysta" if ok else "FAIL — sprawdź opis wyżej")
sys.exit(0 if ok else 1)
