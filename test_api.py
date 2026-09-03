import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    try:
        models = genai.list_models()
        for m in models:
            print(m.name)
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No GEMINI_API_KEY found.")
