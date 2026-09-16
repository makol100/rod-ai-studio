import sys, json, urllib.request
sys.path.insert(0,'/app')
import fal_client
# D-0358: Izabela stojaca na GOTOWEJ alejce BEZ LUDZI (tlo = to samo zdjecie co u Tomasza, YOLO: 0 osob). Wzorzec: relacja_alejka/_iza_stoi.py (08.09, przeszlo)
B='/root/rod-ai-studio/data/wiadomosci/alejka2/izabela'
PROMPT=("Photorealistic vertical 9:16 photo. The exact same woman as in the first image - identical face and features, about 50 years old, "
 "shoulder-length ash-blonde hair, cream linen blazer over a black top - STANDING upright outdoors in the garden alley from the second image: "
 "a finished grassy allotment path in Poland, the soil freshly raked flat after a cable was buried, hedges and fruit trees on both sides, "
 "soft overcast daylight. The background is that real photo scene. Absolutely NO other people, NO workers, NO machines, NO excavator anywhere. "
 "Medium shot framed from the hips up, she stands facing the camera with a calm, friendly, professional expression, "
 "arms relaxed at her sides with both hands visible, weight evenly on both feet. No table, no desk, no chair, nothing in front of her. "
 "Natural skin texture, realistic lighting matching the background. No text, no captions, no logos, no watermark.")
refs=[fal_client.upload_file('/root/rod-ai-studio/assets/izabela/IZABELA_CANON_v2.png'), fal_client.upload_file('/root/rod-ai-studio/data/roboty/2026-09-14/dzien4_grabienie/11_20260914_180134_zdjecie.jpg')]
r=fal_client.subscribe('fal-ai/nano-banana-pro/edit', arguments={'prompt':PROMPT,'image_urls':refs,'aspect_ratio':'9:16','num_images':1,'output_format':'jpeg'})
json.dump(r,open(f'{B}/_iza_stoi2_resp.json','w'))
url=r['images'][0]['url']; urllib.request.urlretrieve(url,f'{B}/izabela_stoi_v2.jpg'); print('OK', url[:60])
