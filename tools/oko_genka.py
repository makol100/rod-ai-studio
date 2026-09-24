#!/usr/bin/env python3
"""OKO GENKA (24.09.2026, po nagrobkach i nie-tulipanach): Gemini ocenia zdjecie PRZED wyslaniem Tomaszowi.
Uzycie: oko_genka.py <plik.jpg> "<czego oczekujemy, po polsku>"  -> JSON {"werdykt":"TAK|NIE","co_widac":"...","powod":"..."}"""
import sys, json, base64, urllib.request, os
def klucz():
    for l in open('/root/.gemini/.env'):
        if l.startswith('GEMINI_API_KEY='): return l.split('=',1)[1].strip().strip('"').strip("'")
    return os.environ.get('GEMINI_API_KEY')
def ocen(plik, oczekiwane, model='gemini-2.5-flash'):
    b64=base64.b64encode(open(plik,'rb').read()).decode()
    prompt=("Jestes surowym kontrolerem zdjec do polskiej rolki ogrodniczej na Facebooku. Najpierw opisz DOSLOWNIE co jest na zdjeciu (obiekt, GATUNEK rosliny jesli rozpoznajesz, miejsce, ludzie, napisy, budynki, groby, pomniki). "
            f"Potem oceń: czy zdjecie pokazuje DOKLADNIE to: <<{oczekiwane}>>? Badz bezlitosny: inny gatunek kwiatu, dziki gatunek zamiast ogrodowego, cmentarz, nagrobek, napis, czlowiek, rysunek, eksponat, zle ujecie = NIE. "
            'Odpowiedz WYLACZNIE JSON: {"werdykt":"TAK"|"NIE","co_widac":"...","powod":"..."}')
    body=json.dumps({"contents":[{"parts":[{"text":prompt},{"inline_data":{"mime_type":"image/jpeg","data":b64}}]}],"generationConfig":{"temperature":0,"responseMimeType":"application/json"}}).encode()
    r=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={klucz()}",data=body,headers={'Content-Type':'application/json'})
    t=json.load(urllib.request.urlopen(r,timeout=90))['candidates'][0]['content']['parts'][0]['text']
    return json.loads(t)
if __name__=='__main__':
    print(json.dumps(ocen(sys.argv[1],sys.argv[2]),ensure_ascii=False))
