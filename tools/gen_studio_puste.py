import base64, json, os, sys, urllib.request, urllib.error

KLUCZ = ""
for l in open("/root/.gemini/.env", encoding="utf-8"):
    if l.startswith("GEMINI_API_KEY="):
        KLUCZ = l.split("=", 1)[1].strip().strip('"').strip("'")

MODEL = "gemini-3.1-flash-image"
WZORZEC = "/root/rod-ai-studio/assets/izabela/STUDIO_IZABELI_CANON_v2.png"
CEL = "/root/rod-ai-studio/data/upload/podglad/TV_STUDIO_PUSTE.png"

with open(WZORZEC, "rb") as f:
    obraz = base64.b64encode(f.read()).decode()

POLECENIE = """Using the reference image as the style guide, produce the SAME television news studio set but COMPLETELY EMPTY.

CRITICAL: NO PERSON. NO PRESENTER. NO HUMAN FIGURE ANYWHERE IN THE IMAGE. The studio must be entirely unoccupied - just the empty set, as if photographed before anyone walked in.

KEEP EXACTLY AS IN THE REFERENCE:
- the deep navy blue colour scheme and the soft gradient lighting
- the vertical illuminated panel lines in the backdrop
- the same lens perspective and the same depth of field
- the horizontal band across the upper part of the frame
- the horizontal band across the lower part of the frame
- overall broadcast-quality look and lighting

REMOVE: the woman, and anything she was holding or sitting behind. Reconstruct the backdrop continuously and naturally where she used to be, so the panels and the gradient run unbroken across the whole frame.

DO NOT render any text, letters, words, captions or logos anywhere - those are added separately afterwards. Leave the bands as clean empty colour blocks.

Photorealistic, sharp, professional broadcast studio lighting, vertical 9:16 portrait, 1080x1920."""

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
