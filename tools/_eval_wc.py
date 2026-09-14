import subprocess
from google import genai
client = genai.Client()

def eval_img(path):
    f = client.files.upload(file=path)
    res = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=[f, "Opisz krótko obraz. 1. Czy nad płytkami jest biała gładka ściana? 2. Czy jest biały podwieszany sufit? 3. Czy pod czarnym przyciskiem wisi biała miska toaletowa na płytkach? 4. Czy drzwi i podłoga są nienaruszone względem standardowej łazienki w remoncie?"]
    )
    print(res.text)

eval_img("data/remont_wc/k3_test_krok2.png")
