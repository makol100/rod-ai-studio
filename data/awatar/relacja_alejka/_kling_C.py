import sys, json, time, urllib.request
sys.path.insert(0,'/app')
import fal_client
B='/root/rod-ai-studio/data/awatar/relacja_alejka'
M='fal-ai/kling-video/ai-avatar/v2/standard'
PROMPT=("Calm natural presentation, head mostly still, maintaining continuous direct eye contact with the camera lens, "
        "natural blinking, subtle facial movement, gentle breeze in the hair, background stays static.")
iu=fal_client.upload_file(f'{B}/izabela_w_alejce.jpg'); au=fal_client.upload_file(f'{B}/izabela_C.mp3')
h=fal_client.submit(M, arguments={'image_url':iu,'audio_url':au,'prompt':PROMPT})
json.dump({'rid':h.request_id,'model':M},open(f'{B}/_kling_C_state.json','w')); print('SUBMIT rid', h.request_id[-12:], flush=True)
for i in range(120):
    time.sleep(10)
    try:
        st=fal_client.status(M, h.request_id, with_logs=False)
        if 'Completed' in type(st).__name__:
            r=fal_client.result(M, h.request_id); json.dump(r,open(f'{B}/_kling_C_resp.json','w'))
            url=r.get('video',{}).get('url') if isinstance(r.get('video'),dict) else r.get('video_url') or r.get('url')
            urllib.request.urlretrieve(url, f'{B}/izabela_C.mp4'); print('OK', url[:70]); break
    except Exception as e: print('status:', str(e)[:80], flush=True)
else: print('TIMEOUT')
