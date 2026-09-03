import sys, re, json, urllib.request, time, os
sys.path.insert(0,'/app'); import fal_client
B='/root/rod-ai-studio/data/rolki_info/tauron_kdt'; L=B+'/izabela'
t=open(B+'/SCENARIUSZ_v1.md',encoding='utf-8').read()
kw={m.group(1):m.group(2) for m in re.finditer(r'^I(\d): (.*)$',t,re.M)}
img=fal_client.upload_file('/root/rod-ai-studio/assets/izabela/STUDIO_IZABELI_CANON_v3.png')
PROMPT=("A calm, credible TV presenter speaking directly to the camera in a small studio. Natural breathing, subtle head movements, "
 "slight shoulder and torso motion, eyebrows and cheeks moving with speech, occasional natural blinks, lips in sync with the Polish speech. "
 "Hands resting on the desk. Background, logo, desk and caption remain completely unchanged.")
for i,txt in kw.items():
    mp3=f'{L}/I{i}.mp3'
    if not os.path.exists(mp3):
        r=fal_client.subscribe('fal-ai/elevenlabs/tts/eleven-v3', arguments={'text':txt,'voice':'Charlotte','language_code':'pl','stability':0.4,'similarity_boost':0.75,'speed':1.0,'output_format':'mp3_44100_128'})
        a=r.get('audio'); urllib.request.urlretrieve(a.get('url') if isinstance(a,dict) else a, mp3)
    d=json.loads(os.popen(f'ffprobe -v error -show_entries format=duration -of json {mp3}').read())['format']['duration']
    print(f'I{i} TTS {float(d):.1f}s', flush=True)
    out=f'{L}/I{i}.mp4'
    if os.path.exists(out): continue
    au=fal_client.upload_file(mp3); t0=time.time()
    try:
        r=fal_client.subscribe('fal-ai/bytedance/omnihuman/v1.5', arguments={'image_url':img,'audio_url':au,'prompt':PROMPT,'resolution':'1080p','turbo_mode':False})
        v=r.get('video'); urllib.request.urlretrieve(v.get('url') if isinstance(v,dict) else v, out)
        print(f'I{i} OMNIHUMAN OK {time.time()-t0:.0f}s {os.path.getsize(out)} B', flush=True)
    except Exception as e:
        print(f'I{i} OMNIHUMAN BLAD {type(e).__name__}: {str(e)[:200]}', flush=True)
print('IZABELA_KONIEC', flush=True)
