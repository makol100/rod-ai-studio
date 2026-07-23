from src.ai.ollama import generate

def generate_image_prompts(scenes: str):
    prompt = f"""
Jesteś profesjonalnym prompt engineerem.

Na podstawie scen przygotuj jeden prompt do wygenerowania obrazu dla każdej sceny.

Każdy prompt w osobnej linii.
Bez numeracji.
Bez komentarzy.
Po angielsku.

Sceny:

{scenes}
"""
    return generate(prompt).strip().splitlines()
