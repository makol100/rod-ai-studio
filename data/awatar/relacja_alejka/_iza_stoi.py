import sys, json, urllib.request
sys.path.insert(0,'/app')
import fal_client
B='/root/rod-ai-studio/data/awatar/relacja_alejka'
PROMPT=("Photorealistic vertical 9:16 photo. The exact same woman as in the first image - identical face and features, about 50 years old, "
 "shoulder-length ash-blonde hair, cream linen blazer over a black top - now STANDING upright outdoors in the garden alley from the second image: "
 "a grassy allotment path in Poland with a freshly dug trench, piles of soil and a small yellow mini excavator behind her, hedges and fruit trees on both sides, "
 "soft overcast daylight. Medium shot framed from the hips up, she stands facing the camera with a calm, friendly, professional expression, "
 "arms relaxed at her sides with both hands visible, weight evenly on both feet. No table, no desk, no chair, no railing, nothing in front of her. "
 "Natural skin texture, realistic lighting matching the background. No text, no captions, no logos, no watermark.")
refs=[fal_client.upload_file('/root/rod-ai-studio/assets/izabela/IZABELA_CANON_v2.png'), fal_client.upload_file('/root/rod-ai-studio/data/roboty/2026-09-07/web/07-alejka.jpg')]
r=fal_client.subscribe('fal-ai/nano-banana-pro/edit', arguments={'prompt':PROMPT,'image_urls':refs,'aspect_ratio':'9:16','num_images':1,'output_format':'jpeg'})
json.dump(r,open(f'{B}/_iza_stoi_resp.json','w'))
url=r['images'][0]['url']; urllib.request.urlretrieve(url,f'{B}/izabela_stoi_v1.jpg'); print('OK', url[:70])
