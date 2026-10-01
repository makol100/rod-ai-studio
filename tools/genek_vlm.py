import urllib.request
import json
import base64
import os

images = [
    "data/reels/prad_rolka/ai/straszak1.jpg",
    "data/reels/prad_rolka/ai/straszak2.jpg",
    "data/reels/prad_rolka/ai/straszak3.jpg",
    "data/reels/prad_rolka/ai/straszak4.jpg"
]
out_file = "data/reels/prad_rolka/ai/opisy.txt"

with open(out_file, "w", encoding="utf-8") as f_out:
    for img_path in images:
        if not os.path.exists(img_path):
            continue
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        payload = {
            "model": "qwen2.5vl:7b",
            "prompt": "Opisz krótko, co przedstawia ten obraz (czy to 1. ciemna altana ze świeczką, 2. lodówka bez światła z zepsutym jedzeniem, 3. zimna altana i czajnik, czy 4. ciemna alejka i jedna oświetlona altana). Wymień tylko jedną z tych czterech opcji.",
            "images": [encoded_string],
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }
        try:
            req = urllib.request.Request("http://localhost:11434/api/generate", data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode('utf-8'))
            desc = result.get("response", "").strip()
            f_out.write(f"--- {os.path.basename(img_path)} ---\n{desc}\n\n")
            print(f"Described {img_path}")
        except Exception as e:
            print(f"Error {img_path}: {e}")
            f_out.write(f"--- {os.path.basename(img_path)} ---\nBlad VLM: {e}\n\n")
