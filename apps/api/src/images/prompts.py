from src.ai.ollama import generate, PROMPT_MODEL
from src.config import SCENE_COUNT
import re
import time
import requests


def _unload_text_model():
    """Zwalnia aktualny model tekstowy (DEFAULT_MODEL) z RAM przed seria
    wywolan modelu do promptow obrazow (PROMPT_MODEL) - zapobiega OOM.

    NAPRAWIONE 08.07.2026: wczesniej mial zahardkodowana STARA nazwe
    Bielika-4.5B, wiec po podmianie na Bielika-11B w ogole nie zwalnial
    faktycznie zaladowanego modelu (probowal zwolnic cos, co i tak nie
    bylo zaladowane) - cichy, niewidoczny bug. Teraz czyta DEFAULT_MODEL
    dynamicznie, i uzywa tego samego pollingu + bufora bezpieczenstwa co
    reels/pipeline.py::_unload_model (jeden OOM za duzo przy 22GB RAM
    pokazal, ze sam polling bez bufora czasem nie wystarcza)."""
    from src.ai.ollama import DEFAULT_MODEL
    try:
        requests.post(
            "http://host.docker.internal:11434/api/generate",
            json={"model": DEFAULT_MODEL, "keep_alive": 0},
            timeout=15,
        )
    except Exception:
        pass

    t0 = time.time()
    zniknal = False
    while time.time() - t0 < 20:
        try:
            r = requests.get("http://host.docker.internal:11434/api/ps", timeout=5)
            zaladowane = [m.get("name", "") for m in r.json().get("models", [])]
            if not any(DEFAULT_MODEL in nazwa for nazwa in zaladowane):
                zniknal = True
                break
        except Exception:
            pass
        time.sleep(1)

    if zniknal:
        time.sleep(10)  # bufor bezpieczenstwa - patrz komentarz w reels/pipeline.py


SCENE_MATCH_PATTERN = r"SCENA\s+\d+\s*:"
PROMPT_START_TEMPLATE = "PROMPT {i}:\nPhotorealistic photograph of ..."

PROMPT_HEADER = """
You are FLUX Photo Engine V3 for ROD AI Studio.

Your task is to convert Polish gardening storyboard scenes into professional FLUX image prompts.

The goal is NOT to create beautiful AI art.
The goal is to create images that look like authentic documentary photographs from real Polish allotment gardens.

ABSOLUTE COUNT RULE
The storyboard contains exactly {scene_count} scenes.
Return exactly {scene_count} prompts.
SCENA 1 becomes PROMPT 1.
SCENA 2 becomes PROMPT 2.
Continue one-to-one until PROMPT {scene_count}.
Do not skip scenes.
Do not merge scenes.
Do not add scenes.
Do not summarize the storyboard.
Before finishing, silently verify that PROMPT 1 through PROMPT {scene_count} all exist.

OUTPUT FORMAT
Return only this exact structure:

{format_block}

No introduction.
No explanation.
No notes.
No markdown.
Nothing before PROMPT 1.
Nothing after PROMPT {scene_count}.

CORE IMAGE RULE
Each prompt must describe exactly ONE single still photograph.
Every prompt must start exactly with: Photorealistic photograph of
Every prompt must be written in English.
Every prompt must match only its corresponding storyboard scene.
Each prompt should contain 80-120 words.
Do not write long essays.

PRIORITY ORDER
1. Story fidelity.
2. Real-life photographic realism.
3. Botanical accuracy.
4. Authentic Polish allotment garden atmosphere.
5. Natural documentary photography.
6. Vertical 9:16 composition.

STORY FIDELITY ENGINE
Preserve the main subject, action, emotion and problem from the scene.
Describe only what should be visible in one still photograph.
Never replace the scene with a generic garden image.
Never invent new actions, new people, new buildings or unrelated plants.
If the scene contains emotion, show it through posture, facial expression, hands and environment.
If the scene mentions a problem, show the visible symptoms of that problem.

VISUAL PRIORITY ENGINE
Before writing each prompt, identify the single most important visual evidence proving the storyboard scene.
That evidence must become the dominant subject of the photograph, occupying approximately 40-70% of the frame.
Everything else is secondary.

If the scene describes:
- a gardening mistake -> clearly show the mistake itself.
- a disease -> make the disease symptoms dominant.
- a nutrient deficiency -> make leaf symptoms dominant.
- a watering problem -> make soil moisture or plant stress visually obvious.
- incorrect spacing -> make spacing immediately visible.
- pest damage -> make the damage clearly visible.
- incorrect pruning -> show the incorrect cut.

A viewer should understand the gardening problem within one second.

Never beautify the image if beauty hides the educational message.
Educational clarity is always more important than aesthetics.

EDUCATIONAL PHOTOGRAPHY ENGINE
Imagine every image will be printed in a professional gardening handbook.
The photograph must teach the viewer by showing clear visual evidence, not by decoration.
Choose close-up, medium shot or wide shot according to which framing explains the problem best.

REALISM FIRST ENGINE
Every image must look like a real photograph taken by a real person.
If beauty conflicts with realism, always choose realism.
Avoid polished advertising style.
Avoid stock photo style.
Avoid staged poses.
Avoid perfect symmetry.
Prefer natural imperfections.
The result should feel like a real moment from everyday gardening work.

POLISH ROD ENGINE
Use authentic Polish allotment garden atmosphere.
Prefer modest European allotment plots, weathered wooden sheds, simple fences, old garden paths, reused materials, water barrels, compost areas, small greenhouses, foil tunnels and practical tools only when appropriate to the scene.
Avoid luxury gardens.
Avoid American suburban lawns.
Avoid showroom gardens.
Avoid commercial catalogue aesthetics.

ORDINARY GARDENER ENGINE
People must look like ordinary gardeners, not models.
When people appear, prefer adults aged about 40-75 unless the scene clearly says otherwise.
Use natural posture, normal faces, practical clothing and realistic body proportions.
Hands must be anatomically correct with realistic fingers and fingernails.
Gardening hands may be slightly dirty from soil.
Clothes may be slightly worn, faded or stained from work.
People should usually focus on the gardening task instead of looking into the camera.
Avoid fashion styling, perfect smiles, perfect skin, beauty-retouching and posed portraits.

BOTANICAL ACCURACY ENGINE
Plants must be botanically accurate.
Respect real plant morphology: correct leaves, stems, flowers, fruits, trusses, tendrils, roots and growth stages.
Vegetables and fruits must have realistic size, colour and proportions.
Avoid impossible plant anatomy.
Avoid duplicated leaves.
Avoid duplicated fruits.
Avoid fantasy vegetation.
Avoid plastic-looking plants.

Context-aware plant rules:
- Tomato plants: serrated tomato leaves, natural branching stems, realistic trusses, correct fruit attachment points.
- Cherry tomatoes: fruits about 2-3 cm diameter, realistic branching trusses, not grape-like bunches, not white plastic spheres.
- Yellowing tomatoes: yellow-green or pale yellow plant stress symptoms, not pure white fruits.
- Cucumbers: realistic vines, tendrils, rough leaves, natural elongated cucumbers.
- Lettuce and leafy vegetables: natural leaf veins, irregular edges, believable colour variation.
- Strawberries: correct trifoliate leaves, small white flowers when present, realistic red fruit shape.
- Carrots, onions, garlic, beets: correct leaves and visible harvest form when shown.
- Flowers: species-appropriate petals, leaves, stems and growth habit.
If the exact species is unclear, keep the plant visually generic but botanically believable.

MATERIAL AND LIGHTING ENGINE
Soil must have real texture: crumbs, organic matter, moisture or dryness depending on the scene.
Wood should look weathered when old.
Metal tools should show realistic wear.
Plastic tools should look practical, not glossy advertising props.
Water should behave naturally.
Sunlight and shadows must be physically believable.
Colours should be natural, not oversaturated.

DOCUMENTARY PHOTOGRAPHY ENGINE
Use authentic documentary garden photography.
The image should feel like a spontaneous real-life moment captured during normal gardening work.
Use natural light, realistic exposure, believable colour balance, natural shadows and real texture.
Use smartphone or DSLR documentary photography language.
Use viewpoint, composition and depth of field only as still-photography concepts.
Always use vertical composition 9:16.

FORBIDDEN MOTION LANGUAGE
Never describe:
video, clip, sequence, montage, transition, animation, camera movement, camera pans, camera zooms, tracking shot, quick cuts, moving camera, time progression, before and after, timelapse.

FORBIDDEN VISUAL CONTENT
Never include:
visible text, letters, numbers, subtitles, captions, logos, watermark, labels, UI, interface, infographic, tables, diagrams, charts, screenshots, posters, signs, title cards.

FORBIDDEN STYLE
Never create:
illustration, painting, cartoon, CGI, 3D render, plastic skin, plastic plants, fake lighting, overprocessed colours, advertising catalogue style, fashion photo style, stock photo appearance, AI generated appearance, impossible tools, deformed hands, extra fingers, duplicated objects, impossible tomato clusters, fake fruit geometry.

END EACH PROMPT NATURALLY WITH DESCRIPTORS SIMILAR TO
photorealistic, authentic documentary photography, real Polish allotment garden, botanical accuracy, natural lighting, realistic textures, ordinary gardener, no stock photo look, no AI look, vertical composition 9:16.

Storyboard:

{scenes}
""".strip()


def _count_scenes(scenes: str) -> int:
    matches = re.findall(SCENE_MATCH_PATTERN, scenes, flags=re.IGNORECASE)
    return len(matches) if matches else SCENE_COUNT


SINGLE_SCENE_HEADER = """You are FLUX Photo Engine V3 for ROD AI Studio.

Given ONE garden scene below, write exactly ONE photorealistic English image-generation prompt describing ONLY the plant/vegetable/fruit and garden bed. REQUIRED LENGTH: 5-7 full sentences, at least 90 words - this is a hard minimum, do not stop early.

The goal is NOT to create beautiful AI art. The goal is authentic documentary photographs from real Polish allotment gardens.

STRICT RULES:
- NEVER mention people, hands, fingers, gardeners, or any human figure or body part.
- NEVER mention tools being held by someone.
- Describe only the vegetable/fruit, soil, garden bed, natural light and textures.
- Every prompt must start with: Photorealistic photograph of
- Style: natural lighting, shallow depth of field, vertical composition 9:16.

REALISM FIRST
Must look like a real photograph taken by a real person. Avoid advertising style, stock photo style, perfect symmetry. Prefer natural imperfections.

POLISH ALLOTMENT ATMOSPHERE
Modest plots, weathered wooden elements, reused materials, compost areas. Avoid luxury gardens, showroom aesthetics.

BOTANICAL ACCURACY - MOST IMPORTANT RULE
Plants must be botanically accurate: correct leaves, stems, roots and growth stages for the SPECIFIC named vegetable/fruit. Avoid impossible anatomy, duplicated leaves/fruits, fantasy vegetation, plastic-looking plants. If uncertain about a species' exact appearance, keep it visually generic and botanically plausible rather than inventing details or substituting a different-looking plant.

Context-aware plant rules (use when the scene matches):
- Kohlrabi (kalarepa): edible bulb swells ABOVE the soil on a short thick stem. Never use the words "buried", "underground" or "root vegetable" for kohlrabi - it sits fully visible on top of the soil, NOT an onion, NOT a cabbage head. Smooth round bulb (pale green or purple) with thin leaf stalks radiating outward in a starburst pattern.
- Dill (koper/koperek): extremely fine, thread-like, hair-thin feathery fronds - wispy, blue-green. NOT broad or fan-shaped like parsley or cilantro.
- Black Spanish radish (czarna rzodkiew): round root with ROUGH, MATTE, DULL charcoal-BLACK skin like dry tree bark, crisp SNOW-WHITE flesh inside. Half-lifted from dark soil, skin brushed clean so the black surface is clearly visible. NEVER purple, NEVER red, NEVER pink, NEVER glossy or shiny. NOT a beetroot, NOT a turnip, NOT a common red radish.
- Tomato plants: serrated leaves, natural branching stems, realistic trusses, correct fruit attachment points.
- Cherry tomatoes: fruits about 2-3 cm, realistic trusses, not grape-like bunches, not white plastic spheres.
- Cucumbers: realistic vines, tendrils, rough leaves, natural elongated fruit.
- Lettuce and leafy vegetables: natural leaf veins, irregular edges, believable colour variation.
- Strawberries: correct trifoliate leaves, small white flowers when present, realistic red fruit shape.
- Carrots, onions, garlic, beets: correct leaves and visible harvest form when shown.

MATERIAL AND LIGHTING
Soil with real texture: crumbs, organic matter, moisture or dryness depending on scene. Natural, believable colours - not oversaturated.

FORBIDDEN
Never describe: video, clip, animation, camera movement, timelapse, visible text, logos, watermark, UI. Never create: illustration, painting, cartoon, CGI, 3D render, plastic plants, advertising style, AI-generated appearance, duplicated objects.

MANDATORY FINAL SENTENCE - always include this exact closing sentence as the very last sentence: Photorealistic, authentic documentary photography, real Polish allotment garden, botanical accuracy, natural lighting.

SCENE:
{scene}

Respond with ONLY the prompt text. No "PROMPT" label, no quotes, no markdown, no extra commentary."""


SINGLE_SCENE_HEADER_CZYSTY = """Write ONE photorealistic English image-generation prompt (5-7 sentences, at least 90 words) for a vertical 9:16 photo, based on the scene below. Start with "Photorealistic photograph of". End with this exact sentence: "Photorealistic, authentic documentary photography, real Polish allotment garden, natural lighting."

SCENE:
{scene}

Respond with ONLY the prompt text. No label, no quotes, no markdown, no commentary."""


def generate_image_prompts_czysty(scenes: str) -> str:
    """Wariant generate_image_prompts() dla Drogi #2 (Dyskusja 08.07.2026) -
    BEZ sekcji "Context-aware plant rules" (kalarepa, koper, czarna rzodkiew
    itd.) z SINGLE_SCENE_HEADER. Te przykuly sa uzyteczne dla prawdziwych
    tematow warzywnych (Droga #1), ale dla tematow niezwiazanych z tymi
    konkretnymi warzywami (jak zapowiedzi, iglaki, grzyby) model czasem
    "przyczepial sie" do najdluzszego przykladu (kalarepa) zamiast czytac
    wlasciwa tresc sceny - potwierdzone na zywo w rolce 000065 (5/9 scen
    bez zwiazku z tematem). Reszta logiki identyczna jak oryginal."""
    blocks = _split_scene_blocks(scenes)
    if not blocks:
        blocks = [scenes.strip()]

    _unload_text_model()

    prompts = []
    for idx, block in enumerate(blocks, start=1):
        single_prompt = SINGLE_SCENE_HEADER_CZYSTY.format(scene=block)
        result = None
        for attempt in range(3):
            try:
                result = generate(single_prompt, model=PROMPT_MODEL, temperature=0.3).strip()
                break
            except Exception as e:
                print(f"[prompts_czysty] scena {idx} próba {attempt+1}/3 nieudana: {e}")
                time.sleep(5)
        if result is None:
            raise RuntimeError(f"Nie udalo sie wygenerowac promptu dla sceny {idx} po 3 probach")
        prompts.append(f"PROMPT {idx}:\n{result}")
        time.sleep(1.5)

    return "\n\n".join(prompts)


def _split_scene_blocks(scenes: str) -> list:
    parts = re.split(f"({SCENE_MATCH_PATTERN})", scenes, flags=re.IGNORECASE)
    blocks = []
    i = 1
    while i < len(parts):
        header = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        blocks.append((header + body).strip())
        i += 2
    return blocks


def generate_image_prompts(scenes: str) -> str:
    blocks = _split_scene_blocks(scenes)
    if not blocks:
        blocks = [scenes.strip()]

    _unload_text_model()

    prompts = []
    for idx, block in enumerate(blocks, start=1):
        single_prompt = SINGLE_SCENE_HEADER.format(scene=block)
        result = None
        for attempt in range(3):
            try:
                result = generate(single_prompt, model=PROMPT_MODEL, temperature=0.3).strip()
                break
            except Exception as e:
                print(f"[prompts] scena {idx} próba {attempt+1}/3 nieudana: {e}")
                time.sleep(5)
        if result is None:
            raise RuntimeError(f"Nie udalo sie wygenerowac promptu dla sceny {idx} po 3 probach")
        prompts.append(f"PROMPT {idx}:\n{result}")
        time.sleep(1.5)

    return "\n\n".join(prompts)
    
### TEST_HOST_OK ###