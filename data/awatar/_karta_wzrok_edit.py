import sys, json, urllib.request
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/awatar'
PROMPT = ("Change only the direction of both pupils so the subject makes natural, symmetrical "
 "eye contact directly with the camera lens. Keep exactly the same identity, facial geometry, "
 "eye shape and size, eyelids, eyebrows, iris color, catchlights, expression, head angle, "
 "skin texture, hair, lighting, clothing, background, framing and resolution. "
 "Do not beautify, retouch, reshape or regenerate the face.")

iu = 'https://v3b.fal.media/files/b/0aa3ed08/pYGkxDnBAF7r-OPZ7arWp_fetRlOJl.png'
r = fal_client.run('fal-ai/nano-banana-pro/edit', arguments={
    'prompt': PROMPT, 'image_urls': [iu], 'aspect_ratio': '9:16',
    'resolution': '2K', 'safety_tolerance': 6}, timeout=180, start_timeout=90)
json.dump(r, open(f'{B}/_karta_v2_resp.json', 'w'))
imgs = r.get('images') or []
url = imgs[0].get('url') if imgs else None
if url:
    urllib.request.urlretrieve(url, f'{B}/karta_stanislaw_v2.jpg')
    print('OK: karta_stanislaw_v2.jpg')
else:
    print('BRAK URL:', json.dumps(r)[:300])
