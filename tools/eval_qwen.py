import urllib.request
import json
import base64
import os

img_path = "data/remont_wc/k3_test_krok2.png"
with open(img_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

payload = {
    "model": "qwen2.5vl:7b",
    "prompt": "Look at this image from a toilet renovation. Please answer: \n1. Is the wall above the tiles smooth and white? (sciana biala?)\n2. Is there a white wall-hung toilet bowl mounted on the gray tiles under the black flush button? (miska na plytkach?)\n3. Are the door and tiles identical to the original unfinished bathroom? Or did the edit add a white plate/board behind the toilet bowl? (drzwi/plytki jak w oryginale? czy dolozylo biala plyte za miska?)",
    "images": [encoded_string],
    "stream": False,
    "options": {
        "temperature": 0.1
    }
}
req = urllib.request.Request("http://localhost:11434/api/generate", data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode('utf-8'))
    print("Qwen Response:")
    print(result.get("response", "").strip())
except Exception as e:
    print("Error:", e)
