import sys, json, hashlib
import fal_client
B = '/root/rod-ai-studio/data/wiadomosci/0001-teren'
KARTA = '/root/rod-ai-studio/data/awatar/karta_stanislaw_CANON.png'
SHA_KANON = '3fb0473388cbc022dd9a43c0d24b6086c65557716699e9dc58dc51d69aec8de0'
sha = hashlib.sha256(open(KARTA,'rb').read()).hexdigest()
assert sha == SHA_KANON, f'KARTA NIEZGODNA Z KANONEM! {sha}'
print('karta SHA OK (kanon)')
M = 'fal-ai/kling-video/ai-avatar/v2/standard'
PROMPT = ("Calm natural presentation, head mostly still, maintaining continuous "
          "direct eye contact with the camera lens, natural blinking, subtle facial movement.")
iu = fal_client.upload_file(KARTA)
au = fal_client.upload_file(f'{B}/work/stanislaw_0001.mp3')
print('upload OK', flush=True)
h = fal_client.submit(M, arguments={'image_url': iu, 'audio_url': au, 'prompt': PROMPT})
json.dump({'rid': h.request_id, 'model': M, 'koszt_est': 3.20, 'audio_s': 57.0},
          open(f'{B}/_kling_0001_state.json', 'w'))
print('SUBMIT 0001 OK rid:', h.request_id[-12:])
