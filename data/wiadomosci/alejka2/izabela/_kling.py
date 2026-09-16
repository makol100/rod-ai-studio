import sys, json, time, urllib.request
sys.path.insert(0, '/app')
import fal_client
# Kling AI Avatar v2 standard — Izabela w kadrze (D-0355). Wzorzec: relacja_alejka/_kling_C2.py (08.09, transkrypt idealny).
# Uzycie: python <skrypt> <I1|I7>
B = '/root/rod-ai-studio/data/wiadomosci/alejka2/izabela'
n = sys.argv[1]
M = 'fal-ai/kling-video/ai-avatar/v2/standard'
PROMPT = ("Calm natural presentation, head mostly still, maintaining continuous direct eye contact with the camera lens, "
          "natural blinking, subtle facial movement, gentle breeze in the hair, background stays static.")
iu = fal_client.upload_file('/root/rod-ai-studio/data/awatar/relacja_alejka/izabela_stoi_v1.jpg')
au = fal_client.upload_file(f'{B}/izabela_{n}.mp3')
h = fal_client.submit(M, arguments={'image_url': iu, 'audio_url': au, 'prompt': PROMPT})
json.dump({'rid': h.request_id, 'model': M}, open(f'{B}/_kling_{n}_state.json', 'w')); print('SUBMIT', n, h.request_id[-12:], flush=True)
for i in range(150):
    time.sleep(10)
    try:
        st = fal_client.status(M, h.request_id, with_logs=False)
        if 'Completed' in type(st).__name__:
            r = fal_client.result(M, h.request_id); json.dump(r, open(f'{B}/_kling_{n}_resp.json', 'w'))
            url = r.get('video', {}).get('url') if isinstance(r.get('video'), dict) else r.get('video_url') or r.get('url')
            urllib.request.urlretrieve(url, f'{B}/izabela_{n}.mp4'); print('OK', n, flush=True); break
    except Exception as e: print('status:', str(e)[:80], flush=True)
else: print('TIMEOUT', n)
