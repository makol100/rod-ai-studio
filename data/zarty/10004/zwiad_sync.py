# -*- coding: utf-8 -*-
import sys, time, json
sys.path.insert(0, '/app')
import fal_client

BAZA = '/root/rod-ai-studio/data/zarty/10004'
kadr = f'{BAZA}/kadr_02.jpg'
stan_f = f'{BAZA}/zwiad_state.json'

url = fal_client.upload_file(kadr)
prompt = ('Tomasz says in Polish with a loud angry determined voice: "Ktoś ty?! Pytam, ktoś ty?!" '
          'He holds the exact pose and grip from the frame for the entire clip, right hand locked '
          'deep in the foliage, speaking through clenched teeth, without gesturing, left arm still. '
          'The branches shake. Continuous single take, natural handheld camera.')
h = fal_client.submit('fal-ai/veo3.1/lite/first-last-frame-to-video', arguments={
    'prompt': prompt, 'first_frame_url': url, 'last_frame_url': url,
    'duration': '8s', 'aspect_ratio': 'auto', 'resolution': '720p'})
rid = h.request_id
json.dump({'request_id': rid, 'start': time.time()}, open(stan_f, 'w'))
print('request_id:', rid, flush=True)

t0 = time.time()
while time.time() - t0 < 88:
    st = fal_client.status('fal-ai/veo3.1/lite/first-last-frame-to-video', rid, with_logs=False)
    nazwa = type(st).__name__
    print(f'{time.time()-t0:5.1f}s {nazwa}', flush=True)
    if nazwa == 'Completed':
        res = fal_client.result('fal-ai/veo3.1/lite/first-last-frame-to-video', rid)
        json.dump({'request_id': rid, 'video_url': res['video']['url']}, open(stan_f, 'w'))
        print('VIDEO:', res['video']['url'], flush=True)
        break
    time.sleep(9)
else:
    print('TIMEOUT-SKRYPTU (job dalej zyje w fal, rid zapisany)', flush=True)
