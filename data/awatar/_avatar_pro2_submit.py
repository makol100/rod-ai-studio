import sys, json
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/awatar'
M = 'fal-ai/kling-video/ai-avatar/v2/pro'
# prompt Zenka z narady wzroku — krotki, eye contact, do poprawionej karty v2
PROMPT = ("Calm natural presentation, head mostly still, maintaining continuous "
          "direct eye contact with the camera lens, natural blinking, subtle facial movement.")

iu = fal_client.upload_file(f'{B}/karta_stanislaw_v2.jpg')
au = fal_client.upload_file(f'{B}/powitanie_daniel.mp3')
print('upload OK', flush=True)
h = fal_client.submit(M, arguments={'image_url': iu, 'audio_url': au, 'prompt': PROMPT})
json.dump({'rid': h.request_id, 'model': M, 'koszt': 4.64},
          open(f'{B}/_avatar_pro2_state.json', 'w'))
print('SUBMIT v3 OK rid:', h.request_id[-12:])
