import urllib.request, json, time, sys, base64

k = open('/root/rod-ai-studio/data/.secrets/fal_key').read().strip()
H = {'Authorization': 'Key ' + k, 'Content-Type': 'application/json'}

def bal():
    return json.load(urllib.request.urlopen(urllib.request.Request('https://rest.alpha.fal.ai/billing/user_balance', headers=H), timeout=20))

def to_data_uri(path, mime):
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

przed = bal()
print('saldo PRZED:', przed, flush=True)

video_url = to_data_uri("data/remont_wc/t2_org.mp4", "video/mp4")
mask_video_url = to_data_uri("data/remont_wc/t2_mask.mp4", "video/mp4")
first_frame_url = to_data_uri("data/remont_wc/k3_test_krok2_544x960.png", "image/png")

payload = {
    "video_url": video_url,
    "mask_video_url": mask_video_url,
    "first_frame_url": first_frame_url,
    "prompt": "Small bathroom renovation, finished: smooth matte white painted wall above the tiles, perfectly flat white suspended plasterboard ceiling with two small recessed LED spotlights, a modern white rimless wall-hung ceramic toilet bowl with white seat mounted on the tiled wall under the black flush plate. Photorealistic, natural lighting, clean surfaces.",
    "negative_prompt": "letterboxing, borders, black bars, bright colors, overexposed, blurred details, subtitles, text, watermark, sink, mirror, window, plants, extra objects, worst quality, low quality",
    "num_frames": 33,
    "frames_per_second": 16,
    "resolution": "480p",
    "aspect_ratio": "9:16",
    "num_inference_steps": 30,
    "guidance_scale": 5,
    "shift": 5,
    "seed": 4242,
    "enable_safety_checker": False,
    "match_input_num_frames": False,
    "match_input_frames_per_second": False
}

try:
    req = urllib.request.Request('https://queue.fal.run/fal-ai/wan-vace-14b/inpainting', data=json.dumps(payload).encode(), headers=H)
    r = json.load(urllib.request.urlopen(req, timeout=60))
except urllib.error.HTTPError as e:
    print('HTTP', e.code, e.read().decode()[:500], flush=True)
    sys.exit(1)

rid = r['request_id']
print('request_id:', rid, flush=True)
su = f'https://queue.fal.run/fal-ai/wan-vace-14b/requests/{rid}/status'
ru = f'https://queue.fal.run/fal-ai/wan-vace-14b/requests/{rid}'

for i in range(120):
    time.sleep(10)
    s = json.load(urllib.request.urlopen(urllib.request.Request(su, headers=H), timeout=30))
    print(i, s.get('status'), flush=True)
    if s.get('status') in ('COMPLETED', 'FAILED'): break

res = json.load(urllib.request.urlopen(urllib.request.Request(ru, headers=H), timeout=60))
vu = (res.get('video') or {}).get('url')
print('wynik:', vu if vu else json.dumps(res)[:400], flush=True)

if vu:
    open('/root/rod-ai-studio/data/remont_wc/t2_wynik.mp4', 'wb').write(urllib.request.urlopen(vu, timeout=120).read())
    print('ZAPISANO t2_wynik.mp4', flush=True)

po = bal()
print('saldo PO:', po, '| KOSZT:', round(przed - po, 4), 'USD', flush=True)
