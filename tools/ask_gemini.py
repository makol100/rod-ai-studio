import google.generativeai as genai
import os
import PIL.Image

# find api key from .env
env = open('.env').read() if os.path.exists('.env') else ''
key = [line.split('=')[1] for line in env.split('\n') if line.startswith('GEMINI_API_KEY=')]
if not key and 'GEMINI_API_KEY' in os.environ:
    key = [os.environ['GEMINI_API_KEY']]

if not key:
    print("No key")
else:
    genai.configure(api_key=key[0])
    model = genai.GenerativeModel('gemini-1.5-pro')
    for i in range(1, 6):
        img_path = f'data/remont_wc/kadry/k{i}.jpg'
        img = PIL.Image.open(img_path)
        prompt = "Return the bounding box [ymin, xmin, ymax, xmax] of the black flush button on the toilet tank in the format: ymin, xmin, ymax, xmax. If there is no black flush button, reply 'brak'."
        response = model.generate_content([img, prompt])
        print(f"k{i}.jpg:", response.text.strip())
