import sys, json, urllib.request
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/awatar'
vu = fal_client.upload_file(f'{B}/baza_stanislaw_40s.mp4')
au = fal_client.upload_file(f'{B}/powitanie_daniel.mp3')
print('upload OK', flush=True)
r = fal_client.subscribe('fal-ai/latentsync', arguments={'video_url': vu, 'audio_url': au})
json.dump(r, open(f'{B}/_lipsync_resp.json', 'w'))
v = r.get('video')
url = v.get('url') if isinstance(v, dict) else v or r.get('url')
if url:
    urllib.request.urlretrieve(url, f'{B}/stanislaw_lipsync_raw.mp4')
    print('OK: stanislaw_lipsync_raw.mp4')
else:
    print('BRAK URL:', json.dumps(r)[:300])
