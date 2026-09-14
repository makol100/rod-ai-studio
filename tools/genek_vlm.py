import json, os, sys
from google.genai import Client
from google.genai.types import Part

K=""
for p in ("/root/.gemini/.env","/root/rod-ai-studio/.env"):
    try:
        for l in open(p):
            if l.startswith("GEMINI_API_KEY="): K=l.split("=",1)[1].strip().strip('"\''); break
    except FileNotFoundError: pass
    if K: break

c = Client(api_key=K)
img_path = "data/izabela/relacja2/izabela_stoi_v2.png"
with open(img_path, "rb") as f:
    img_data = f.read()
    
img_part = Part.from_bytes(data=img_data, mime_type="image/png")

prompt = "Opisz krótko tę postać i tło. Czy to kobieta z blond włosami w jasnej marynarce (ecru linen blazer)? Czy tło to zagrabiona ziemia, bez żadnej koparki w kadrze?"

resp = c.models.generate_content(
    model="gemini-2.5-flash",
    contents=[img_part, prompt]
)
print(resp.text)
