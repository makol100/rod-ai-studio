import cv2
import numpy as np
import os
import json
import base64
import urllib.request

video_path = 'data/remont_wc/maska_podglad.mp4'
if not os.path.isfile(video_path):
    print(f"Error: {video_path} not found")
    exit(1)

cap = cv2.VideoCapture(video_path)
frames_to_check = [1, 100, 200, 300, 400]

prompts = {
    1: "In this image (frame 1 of the bathroom renovation), check if the red semi-transparent mask stays exactly above the upper boundary of the green wall tiles. Does it overlap onto the green tiles, or onto the black flush plate, or onto the toilet bowl/door? Answer in Polish with a concise verdict: PASS or FAIL, and a brief explanation.",
    100: "In this image (frame 100 of the bathroom renovation), check if the red semi-transparent mask stays exactly above the upper boundary of the green wall tiles. Does it overlap onto the green tiles, or onto the black flush plate, or onto the toilet bowl/door? Answer in Polish with a concise verdict: PASS or FAIL, and a brief explanation.",
    200: "In this image (frame 200 of the bathroom renovation), check if the red semi-transparent mask stays exactly above the upper boundary of the green wall tiles. Does it overlap onto the green tiles, or onto the black flush plate, or onto the toilet bowl/door? Answer in Polish with a concise verdict: PASS or FAIL, and a brief explanation.",
    300: "In this image (frame 300 of the bathroom renovation), check if the red semi-transparent mask stays exactly above the upper boundary of the green wall tiles. Does it overlap onto the green tiles, or onto the black flush plate, or onto the toilet bowl/door? Answer in Polish with a concise verdict: PASS or FAIL, and a brief explanation.",
    400: "In this image (frame 400 of the bathroom renovation), check if the red semi-transparent mask stays exactly above the upper boundary of the green wall tiles. Does it overlap onto the green tiles, or onto the black flush plate, or onto the toilet bowl/door? Answer in Polish with a concise verdict: PASS or FAIL, and a brief explanation."
}

results = {}

for f_idx in frames_to_check:
    cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
    ret, frame = cap.read()
    if not ret:
        print(f"Failed to read frame {f_idx}")
        continue
    
    # Save frame as temporary image
    tmp_img_path = f"data/remont_wc/verify_frame_{f_idx}.jpg"
    cv2.imwrite(tmp_img_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    
    # Read and encode to b64
    with open(tmp_img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Call Ollama qwen2.5vl:7b
    payload = {
        "model": "qwen2.5vl:7b",
        "prompt": prompts[f_idx],
        "images": [encoded_string],
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }
    
    req_body = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        "http://172.17.0.1:11434/api/generate",
        data=req_body,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            resp_data = json.loads(resp.read().decode('utf-8'))
            results[f_idx] = resp_data.get("response", "").strip()
            print(f"--- Frame {f_idx} ---")
            print(results[f_idx])
    except Exception as e:
        results[f_idx] = f"Error: {e}"
        print(f"Error checking frame {f_idx}: {e}")
        
    # Clean up temp image
    if os.path.exists(tmp_img_path):
        os.remove(tmp_img_path)

cap.release()

# Save verify log
with open('data/remont_wc/verification_log.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
