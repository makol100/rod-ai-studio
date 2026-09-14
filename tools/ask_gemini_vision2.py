from google import genai
from google.genai import types
import os

client = genai.Client()

def analyze_image(img_path):
    try:
        sample_file = client.files.upload(file=img_path)
        prompt = "Look at this image. Can you find the black button of the toilet flush (spłuczka)? If it is visible, return its coordinates as [ymin, xmin, ymax, xmax] relative to 1000. If it's not visible, just answer 'brak'. Do not write anything else."
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[sample_file, prompt]
        )
        print(f"{img_path}: {response.text.strip()}")
    except Exception as e:
        print(f"Error for {img_path}: {e}")

if __name__ == "__main__":
    for i in range(1, 6):
        analyze_image(f"data/remont_wc/kadry/k{i}.jpg")
