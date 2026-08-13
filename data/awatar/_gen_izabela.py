import sys, json, urllib.request, os
import fal_client

B = '/root/rod-ai-studio/data/awatar'
M = 'fal-ai/nano-banana-pro'

# PROMPT ZLOZONY Z GLOSOW ZALOGI (30.07.2026):
#   Zenek — specyfikacja tozsamosci, wiek 53 opisany konstrukcyjnie, lista slow zakazanych
#   Henio — cechy anatomiczne, przeplyw z wycinaniem tla, kolory ubioru pod tlo
#   Klaudek (research) — slowo "Slavic" ciagnie ku glamour: opisywac ANATOMIE, nie etykiete;
#                        miekkie boczne swiatlo ODMLADZA; niedoskonalosci podnosza realizm; 85 mm
# Decyzja Tomasza: "Ma byc piekna kobieta o slowianskich rysach. Polka. Po piecdziesiatce."
# Tlo do WYCIECIA (jasna szarosc, nie zielen — zielona poswiata na siwiejacych wlosach jest nie do cofniecia).

PROMPT = """Photorealistic vertical 9:16 three-quarter portrait of one fictional woman named Izabela,
a Polish woman aged 53, photographed as a calm, credible local community reporter.

IDENTITY — preserve these exact traits in every future image:
Softly oval face, slightly wider at the cheeks, with a natural jawline.
High, elegantly defined cheekbones that catch the light and give the face structure.
Large, well-set, gently almond-shaped grey-green eyes with a clear direct gaze and dark lashes.
Straight, finely shaped nose with a naturally rounded tip.
Well-shaped medium lips with a defined cupid's bow, natural colour, no augmentation.
Balanced, harmonious facial proportions — a genuinely beautiful woman, with only slight natural asymmetry.
Fair, neutral-to-cool complexion with a subtle natural flush, uneven tone and small pigmentation marks.
Ash dark-blonde to light-brown hair with scattered natural silver strands throughout,
shoulder-length softly layered bob, slight side part, a few natural flyaway hairs.
Well-groomed cool-brown eyebrows of medium density, natural shape, not laminated.
She is a strikingly beautiful woman whose beauty comes from bone structure, clear eyes and poise —
not from makeup, retouching or youth. Elegant and dignified. The kind of face people trust and remember.

VISIBLE AGE 53 — must read as genuinely early fifties, never as a young woman with artificially grey hair:
Fine-to-moderate crow's feet visible at rest, subtle under-eye lines and slight under-eye hollowing,
faint horizontal forehead lines, a light glabellar line, moderate natural nasolabial folds,
slight loss of cheek volume, softly defined jawline, clearly visible age-appropriate skin laxity on the neck
with distinct horizontal neck lines and softening under the chin, visible pores, peach fuzz, fine uneven pigmentation,
natural minor facial asymmetry.

EXPRESSION AND POSE:
Calm, attentive and composed, with clear warmth and a subtle smile in the eyes only.
Lips relaxed and closed with the faintest hint of a soft smile at the corners — alive, not blank.
Direct eye contact with the camera. Natural upright posture, relaxed shoulders.
Three-quarter framing from mid-torso upward. Hands not visible.

WARDROBE:
Simple matte solid petrol-teal blouse, colour approximately #356A70, modest soft neckline.
No blazer, no uniform, no pattern, no visible brand, no jewellery except very small plain stud earrings.

COMPOSITION:
Vertical 1080x1920. The entire upper 16 percent of the image must remain empty background,
with the top of her hair clearly below that reserved area. Her face and body stay in the lower 84 percent.
Eye-level camera, natural portrait perspective, 85 mm portrait-lens look.

LIGHTING AND TEXTURE:
Soft directional key light from camera-left at about 40 degrees, sculpting the cheekbone and jaw
with a gentle shadow, plus soft fill on the shadow side. Loop lighting. Clear catchlights in both eyes.
The light must flatter the face and give it depth, while keeping every age marker fully visible.
Real human skin with visible pores, peach fuzz and small natural imperfections.
No beauty retouching, no skin smoothing, no digital makeup, no plastic skin, no rim-light halo.

BACKGROUND FOR LATER EXTRACTION:
Perfectly uniform flat light warm-grey background, colour #D4CFC8, evenly lit,
with no gradient, texture, props, horizon, floor line or cast shadow.
Clean, sharp hair edges suitable for background removal.

One woman only. No text, no logo, no captions, no background objects.
She must not look like a fashion model, celebrity, politician, executive, government official,
news anchor, gardener or allotment holder."""

print(f"ZNAKOW PROMPTU: {len(PROMPT)}", flush=True)
try:
    r = fal_client.subscribe(M, arguments={
        'prompt': PROMPT,
        'aspect_ratio': '9:16',
        'resolution': '2K',
        'num_images': 1,
    })
    json.dump(r, open(f'{B}/_izabela_v2_resp.json', 'w'))
    url = None
    if isinstance(r, dict):
        im = r.get('images') or []
        if im and isinstance(im[0], dict):
            url = im[0].get('url')
        url = url or r.get('image', {}).get('url') if isinstance(r.get('image'), dict) else url
    if url:
        urllib.request.urlretrieve(url, f'{B}/izabela_v2.png')
        print(f"OK -> {B}/izabela_v2.png", flush=True)
    else:
        print(f"BRAK URL: {json.dumps(r)[:400]}", flush=True)
except Exception as e:
    print(f"BLAD: {str(e)[:400]}", flush=True)
