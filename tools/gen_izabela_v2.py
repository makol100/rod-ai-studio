import base64, json, os, sys, urllib.request, urllib.error

KLUCZ = ""
for l in open("/root/.gemini/.env", encoding="utf-8"):
    if l.startswith("GEMINI_API_KEY="):
        KLUCZ = l.split("=", 1)[1].strip().strip('"').strip("'")

MODEL = "gemini-3.1-flash-image"
WZORZEC = "/root/rod-ai-studio/assets/izabela/IZABELA_CANON.png"
CEL = "/root/rod-ai-studio/data/upload/podglad/IZABELA_ECRU_v2.png"

with open(WZORZEC, "rb") as f:
    obraz = base64.b64encode(f.read()).decode()

POLECENIE = """Edit this portrait of the SAME woman. Her FACE, hair, age and skin must stay EXACTLY as in the reference - recognisably the same person. Everything else changes.

THE PROBLEM WITH THE REFERENCE: it looks like a PASSPORT PHOTO - centred, symmetrical, shoulders square to the lens, cropped at the chest, no hands, no depth. This MUST be fixed. The result must look like a candid frame from a live TV news broadcast, NOT like an ID photograph.

REQUIRED - all mandatory, not optional:
- SEATED BEHIND A DESK. A desk edge crosses the lower part of the frame. Essential.
- BOTH HANDS CLEARLY VISIBLE, resting on the desk, one slightly over the other, or holding a few sheets of paper. Hands must be in shot.
- TORSO ROTATED roughly 20-25 degrees to one side; head turned back towards the lens. One shoulder visibly closer to the camera than the other. NO symmetry.
- MEDIUM SHOT from the waist up, so the desk, both arms and both hands fit in frame. Her head must NOT dominate the frame.
- Place her clearly OFF-CENTRE, to one side, leaving open studio space on the opposite side.

OUTFIT: ecru / off-white (#E8DFD0) LINEN BLAZER, open at the front with a visible neckline underneath. Elegant, well-tailored, contemporary. A television news presenter.
BACKGROUND: plain neutral light grey studio backdrop, evenly lit, no text, no logo, no props beyond the desk.
Photorealistic, sharp, professional broadcast lighting, vertical 9:16 portrait."""

dane = json.dumps({
    "contents": [{"parts": [
        {"inline_data": {"mime_type": "image/png", "data": obraz}},
        {"text": POLECENIE},
    ]}],
    "generationConfig": {"responseModalities": ["IMAGE"]},
}).encode()

req = urllib.request.Request(
    "https://generativelanguage.googleapis.com/v1beta/models/" + MODEL + ":generateContent?key=" + KLUCZ,
    data=dane, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req, timeout=300) as o:
        odp = json.load(o)
except urllib.error.HTTPError as e:
    print("BLAD", e.code, e.read()[:400].decode(errors="replace"))
    sys.exit(1)

zapisane = 0
for cz in odp.get("candidates", [{}])[0].get("content", {}).get("parts", []):
    dd = cz.get("inlineData") or cz.get("inline_data")
    if dd and dd.get("data"):
        with open(CEL, "wb") as f:
            f.write(base64.b64decode(dd["data"]))
        print("ZAPISANO " + CEL + " (" + str(os.path.getsize(CEL) // 1024) + " KB)")
        zapisane += 1

if not zapisane:
    print("MODEL NIE ZWROCIL OBRAZU: " + json.dumps(odp)[:400])
