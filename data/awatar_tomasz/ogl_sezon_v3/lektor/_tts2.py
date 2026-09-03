import sys, json, urllib.request
sys.path.insert(0,'/app'); import fal_client
nr,voice,speed,st=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4])
kw=json.load(open('/root/rod-ai-studio/data/awatar_tomasz/ogl_sezon_v3/kwestie.json'))
t=kw[nr]
r=fal_client.subscribe('fal-ai/elevenlabs/tts/multilingual-v2', arguments={'text':t,'voice':voice,'language_code':'pl','stability':st,'similarity_boost':0.8,'speed':speed,'output_format':'mp3_44100_128'})
a=r.get('audio'); url=a.get('url') if isinstance(a,dict) else a
out=f'/root/rod-ai-studio/data/awatar_tomasz/ogl_sezon_v3/lektor/kw{nr}_{voice}_m2_s{speed}_st{st}.mp3'
urllib.request.urlretrieve(url,out); print('OK',out)
