import sys, json, urllib.request
sys.path.insert(0,'/app')
import fal_client
B='/root/rod-ai-studio/data/awatar/relacja_alejka'
TEKST="Jestem Izabela, wirtualny awatar zarządu. To pierwszy dzień robót — w kolejnych dniach kabel pójdzie dalej. Będziemy informować."
r=fal_client.subscribe('fal-ai/elevenlabs/tts/eleven-v3', arguments={'text':TEKST,'voice':'Charlotte','language_code':'pl','stability':0.4,'similarity_boost':0.75,'speed':1.0,'output_format':'mp3_44100_128'})
json.dump(r,open(f'{B}/_tts_C_resp.json','w'))
url=None
if isinstance(r,dict):
    a=r.get('audio'); url=(a.get('url') if isinstance(a,dict) else a) or r.get('audio_url') or r.get('url')
urllib.request.urlretrieve(url,f'{B}/izabela_C.mp3'); print('OK', url[:60])
