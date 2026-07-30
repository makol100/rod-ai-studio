import sys, json
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/awatar'
M = 'fal-ai/kling-video/ai-avatar/v2/pro'
PROMPT = ("A dignified 70-year-old Polish news presenter with a warm, steady gaze. "
 "He performs slow, deliberate head tilts and subtle nodding to emphasize key words. "
 "Minimal, organic facial expressions with natural blinking. His hands remain mostly "
 "stationary on the table near a tea glass and a notebook, making only very rare, tiny, "
 "controlled gestures. The movement is calm, professional, and avoids any broad or fast "
 "motions, maintaining a 'talking head' news anchor composure.")

iu = fal_client.upload_file(f'{B}/karta_stanislaw_v1.jpg')
au = fal_client.upload_file(f'{B}/powitanie_daniel.mp3')
print('upload OK', flush=True)
h = fal_client.submit(M, arguments={'image_url': iu, 'audio_url': au, 'prompt': PROMPT})
json.dump({'rid': h.request_id, 'model': M, 'koszt': 4.64},
          open(f'{B}/_avatar_pro_state.json', 'w'))
print('SUBMIT OK rid:', h.request_id[-12:])
