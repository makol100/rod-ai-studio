import google.generativeai as genai
import os
import sys

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

def analyze_image(img_path):
    try:
        sample_file = genai.upload_file(path=img_path)
        prompt = "Zwróć współrzędne [ymin, xmin, ymax, xmax] dla czarnego przycisku spłuczki na tym zdjęciu w postaci bounding box. Jeśli przycisku spłuczki nie ma na zdjęciu, napisz 'brak'. Opisz też króciutko, gdzie on jest."
        response = model.generate_content([sample_file, prompt])
        print(f"{img_path}: {response.text}")
    except Exception as e:
        print(f"Error for {img_path}: {e}")

if __name__ == "__main__":
    for i in range(1, 6):
        analyze_image(f"data/remont_wc/kadry/k{i}.jpg")
