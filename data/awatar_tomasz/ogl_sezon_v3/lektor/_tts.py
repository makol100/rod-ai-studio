import sys, json, urllib.request
sys.path.insert(0,'/app'); import fal_client
nr=sys.argv[1]; voice=sys.argv[2] if len(sys.argv)>2 else 'Daniel'; speed=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
kw=json.load(open('/root/rod-ai-studio/data/awatar_tomasz/ogl_sezon_v3/kwestie.json'))
teksty={'1':"Dzień dobry, tu Tomasz. Zakończenie sezonu działkowego ROD Woźniki! Sezon dobiega końca, plony zebrane, grządki zasłużyły na odpoczynek.",
        '2':"A my na porządną biesiadę! Sobota, piątego września dwa tysiące dwudziestego szóstego roku, godzina siedemnasta."}
t=teksty.get(nr, kw[nr])
r=fal_client.subscribe('fal-ai/elevenlabs/tts/eleven-v3', arguments={'text':t,'voice':voice,'language_code':'pl','stability':float(sys.argv[4]) if len(sys.argv)>4 else 0.6,'similarity_boost':0.8,'speed':speed,'output_format':'mp3_44100_128'})
a=r.get('audio'); url=a.get('url') if isinstance(a,dict) else a
out=f'/root/rod-ai-studio/data/awatar_tomasz/ogl_sezon_v3/lektor/kw{nr}_{voice}_s{speed}_st{sys.argv[4] if len(sys.argv)>4 else 0.6}.mp3'
urllib.request.urlretrieve(url,out); print('OK',out)
