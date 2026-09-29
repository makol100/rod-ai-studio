#!/root/sd_venv/bin/python
"""N0 Ciekawostki wyd.1 — kandydaci SD lokalnie (0 zl), D-0663/D-0664. Nic nie idzie do filmu bez 👍 Tomasza."""
import sys, time, torch
from diffusers import StableDiffusionPipeline, LCMScheduler
torch.set_num_threads(12)
pipe = StableDiffusionPipeline.from_pretrained("/root/modele/sd_dreamshaper8_lcm", torch_dtype=torch.float32,
                                               safety_checker=None, requires_safety_checker=False)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
NEG = "blurry, deformed, text, letters, watermark, signature, logo, lowres, jpeg artifacts, people, person, hands"
P = {
 "ai_N0_1_altana": "photo of a charming polish allotment garden in late summer, small wooden garden shed gazebo painted green, colorful flower beds, dahlias, sunflowers, vegetable patches, apple tree, soft morning light, lush, high detail, 35mm photography",
 "ai_N0_2_lupa": "photo of a vintage magnifying glass lying on a rustic wooden garden table, next to fresh tomatoes, apples, garden trowel and an old notebook, allotment garden blurred in background, golden hour, shallow depth of field, cozy, high detail",
 "ai_N0_3_zlota": "wide photo of allotment gardens at golden hour, rows of small garden plots with little wooden sheds, fruit trees, flowers, green hedges, warm sunset light, peaceful, europe, high detail, 35mm photography",
 "ai_N0_4_furtka": "photo of an open old wooden garden gate leading into a blooming allotment garden, path with flowers on both sides, sunflowers, small shed in background, warm afternoon light, inviting, high detail",
 "ai_N0_5_gora": "aerial drone photo of european allotment gardens, patchwork of small green garden plots, tiny sheds, fruit trees, paths, summer, sunny, high detail",
 "ai_N0_6_kosz": "photo of a wicker basket full of vegetables and flowers, carrots, tomatoes, zucchini, dahlias, standing on grass in an allotment garden, small wooden shed behind, sunny late summer day, high detail, shallow depth of field",
}
wybor = sys.argv[1:] or list(P)
for i, k in enumerate(wybor):
    t = time.time()
    g = torch.Generator().manual_seed(2909 + i)
    img = pipe(P[k], negative_prompt=NEG, num_inference_steps=6, guidance_scale=1.5, width=768, height=512, generator=g).images[0]
    img.save(f"/root/rod-ai-studio/data/ciekawostki/wydanie1/zdjecia/ai/{k}.png")
    print(f"OK {k} {time.time()-t:.0f}s", flush=True)
