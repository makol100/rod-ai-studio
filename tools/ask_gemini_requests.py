import os
import requests
import base64
import json
import re

env = open('.env').read() if os.path.exists('.env') else ''
key = [line.split('=')[1] for line in env.split('\n') if line.startswith('GEMINI_API_KEY=')]
if not key and 'GEMINI_API_KEY' in os.environ:
    key = [os.environ['GEMINI_API_KEY']]
key = key[0].strip(' "\'')

for i in range(1, 6):
    img_path = f'data/remont_wc/kadry/k{i}.jpg'
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [
                {"text": "Is there a black flush button in this image? If yes, provide its bounding box as a [ymin, xmin, ymax, xmax] list (from 0 to 1000). If no, just say 'brak'."},
                {"inline_data": {"mime_type": "image/jpeg", "data": encoded_string}}
            ]
        }]
    }
    response = requests.post(url, headers=headers, json=data)
    try:
        print(f"k{i}.jpg:", response.json()['candidates'][0]['content']['parts'][0]['text'].strip())
    except Exception as e:
        print(f"k{i}.jpg Error:", response.json())
