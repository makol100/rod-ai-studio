import sys, json, urllib.request
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/awatar'
PROMPT = ("Photorealistic portrait, frame from a high-budget documentary about the Polish countryside. "
 "A Polish man aged 65-70 seated at a table inside an allotment-garden summerhouse: noble expressive features, "
 "dense friendly wrinkles around the eyes, short thick neatly combed fully gray hair parted to the right, clean-shaven, "
 "cloudy-blue eyes with the warm gravitas and trustworthy focused gaze of a veteran TV news presenter. "
 "Average slightly slim yet sturdy build, upright dignified posture, head tilted slightly as if attentively listening, "
 "weathered but well-kept hands with long fingers resting near his notes. "
 "He wears a light cream shirt with a very fine, barely visible check pattern and a soft collar, "
 "under a thick cable-knit wool sleeveless sweater vest in muted bottle green; "
 "classic horn-rimmed reading glasses hang on a black cord on his chest; no headwear. "
 "On the table: tea in a transparent glass set in a vintage silver metal holder with a handle, "
 "an open A5 leather notebook densely handwritten, an old-fashioned metal pen, and a Polish gardening magazine. "
 "Interior: light wood paneling, a shelf with thick binders, a few gardening trophy cups, "
 "a neat row of homemade preserve jars on an upper shelf, a small clean window revealing a lush green garden with a rose pergola. "
 "Warm golden-hour sunlight falls from the side window, highlighting the wool texture; homely, safe, quietly erudite atmosphere. "
 "Medium shot, face sharp and highly detailed (character identity reference).")

r = fal_client.run('fal-ai/nano-banana-pro', arguments={
    'prompt': PROMPT, 'aspect_ratio': '9:16', 'resolution': '2K',
    'safety_tolerance': 6}, timeout=180, start_timeout=90)
json.dump(r, open(f'{B}/_karta_stanislaw_resp.json', 'w'))
imgs = r.get('images') or []
url = imgs[0].get('url') if imgs else None
if url:
    urllib.request.urlretrieve(url, f'{B}/karta_stanislaw_v1.jpg')
    print('OK: karta_stanislaw_v1.jpg')
else:
    print('BRAK URL:', json.dumps(r)[:300])
