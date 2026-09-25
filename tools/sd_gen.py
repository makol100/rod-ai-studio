#!/root/sd_venv/bin/python
"""Stable Diffusion na CPU VPS (25.09.2026, D-0618: „Stable Diffusion na naszym serwerze instaluj. Generowanie zdjęć daj belzebubowi przez diffusiona").
Model: Lykon/dreamshaper-8 (SD 1.5, licencja CreativeML OpenRAIL-M) + LCM-LoRA (latent-consistency/lcm-lora-sdv1-5) -> 6 krokow.
Bez safety checkera. Uzycie: sd_gen.py "prompt" wyjscie.png [szer] [wys]"""
import sys, time, torch
from diffusers import StableDiffusionPipeline, LCMScheduler
torch.set_num_threads(12)
t0 = time.time()
# lokalna kopia z wtopiona LCM-LoRA, fp16 na dysku (2 GB) — /root/modele/sd_dreamshaper8_lcm; liczy w fp32 na CPU
pipe = StableDiffusionPipeline.from_pretrained("/root/modele/sd_dreamshaper8_lcm", torch_dtype=torch.float32, safety_checker=None, requires_safety_checker=False)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
t1 = time.time()
w = int(sys.argv[3]) if len(sys.argv) > 3 else 512; h = int(sys.argv[4]) if len(sys.argv) > 4 else 768
img = pipe(sys.argv[1], negative_prompt="blurry, deformed, bad anatomy, extra fingers, text, watermark, lowres, jpeg artifacts",
           num_inference_steps=6, guidance_scale=1.5, width=w, height=h).images[0]
img.save(sys.argv[2]); print(f"OK {sys.argv[2]} ladowanie {t1-t0:.0f}s generowanie {time.time()-t1:.0f}s", flush=True)
