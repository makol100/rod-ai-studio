import sys, json
sys.path.insert(0, '/app')
import fal_client
B = '/root/rod-ai-studio/data/wiadomosci/0001-teren'
M = 'fal-ai/kling-video/ai-avatar/v2/standard'
PROMPT = ("Calm natural presentation, head mostly still, maintaining continuous "
          "direct eye contact with the camera lens, natural blinking, subtle facial movement.")
iu = fal_client.upload_file('/root/rod-ai-studio/data/awatar/karta_stanislaw_CANON.png')
au = fal_client.upload_file(f'{B}/wd0001_daniel.mp3')
print('upload OK', flush=True)
h = fal_client.submit(M, arguments={'image_url': iu, 'audio_url': au, 'prompt': PROMPT})
json.dump({'rid': h.request_id, 'model': M, 'koszt_szac': 3.07}, open(f'{B}/_avatar_0001_state.json', 'w'))
print('SUBMIT 0001 OK rid:', h.request_id[-12:])
