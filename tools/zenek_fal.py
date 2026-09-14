import os
import json
import requests
import time

with open('data/.secrets/fal_key', 'r') as f:
    fal_key = f.read().strip()

headers = {
    'Authorization': f'Key {fal_key}',
    'Content-Type': 'application/json'
}

def check_balance():
    # Fal API doesn't have a direct "balance" endpoint publicly documented in standard REST sometimes, 
    # but let's try the usual /v1/user/balance or similar, or skip if not strictly possible.
    # Actually, we can use the /users/current endpoint maybe? 
    pass

# We will use Fal Client if available, otherwise fallback to requests.
try:
    import fal_client
    os.environ['FAL_KEY'] = fal_key
    print("Uploading test_org.mp4...")
    video_url = fal_client.upload_file("data/remont_wc/test_org.mp4")
    print("Uploading test_mask.mp4...")
    mask_video_url = fal_client.upload_file("data/remont_wc/test_mask.mp4")
    
    print(f"video_url: {video_url}")
    print(f"mask_video_url: {mask_video_url}")
    
    prompt = "smooth finished matte white painted wall flush with the tiles, flat white suspended plasterboard ceiling with two recessed LED spotlights, modern white rimless wall-hung ceramic toilet bowl with white seat mounted on the tiled wall under the black flush plate, photorealistic, same lighting"
    negative = "text, watermark, extra objects, sink, mirror, window"
    
    args = {
        "video_url": video_url,
        "mask_video_url": mask_video_url,
        "prompt": prompt,
        "negative_prompt": negative,
        "video_strength": 1.0,
        "seed": 42,
        "enable_prompt_expansion": False
    }
    
    print("Calling fal-ai/ltx-video/inpaint (or ltx-2.3-quality/inpaint)...")
    # Actually the model name is fal-ai/ltx-video/inpaint or similar. Let's check exact name.
    # The prompt says: fal-ai/ltx-2.3-quality/inpaint
    # Let's try that. If it fails, maybe fal-ai/ltx-video/inpaint
    
    try:
        result = fal_client.subscribe(
            "fal-ai/ltx-2.3-quality/inpaint",
            arguments=args
        )
    except Exception as e:
        print("Failed with ltx-2.3-quality/inpaint, trying ltx-video/inpaint", e)
        result = fal_client.subscribe(
            "fal-ai/ltx-video/inpaint",
            arguments=args
        )
    
    print("Result:", result)
    
    if 'video' in result:
        out_url = result['video']['url']
        print(f"Downloading result from {out_url}...")
        r = requests.get(out_url)
        with open('data/remont_wc/test_ltx.mp4', 'wb') as f:
            f.write(r.content)
        print("Saved to data/remont_wc/test_ltx.mp4")

except Exception as e:
    print(f"Error: {e}")

