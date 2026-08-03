#!/usr/bin/env python3
"""Wycięcie postaci z tła (rembg birefnet-portrait) + rekonstrukcja tła studia.
Użycie: python3 tools/wytnij_izabele.py --source obraz.png --output wynik.png
Domyślnie: source=/root/rod-ai-studio/assets/izabela/IZABELA_CANON.png, output=/tmp/iza_dobra.png
"""
import argparse
from pathlib import Path
import numpy as np


def wytnij(source_path, output_path):
    from PIL import Image
    from rembg import remove, new_session

    src_pil = Image.open(source_path).convert("RGB")
    rgb_u8 = np.asarray(src_pil)
    rgb = rgb_u8.astype(np.float32)
    a_u8 = np.asarray(remove(
        src_pil,
        session=new_session("birefnet-portrait"),
        only_mask=True,
        post_process_mask=False,
    ).convert("L"))
    a = a_u8.astype(np.float32) / 255.0
    h, w = a.shape

    # Fit the smooth original studio background from high-confidence background pixels.
    yy, xx = np.mgrid[0:h, 0:w]
    sample = (a < 2/255) & ((xx % 12) == 0) & ((yy % 12) == 0)
    xn = (xx[sample] / (w - 1) * 2 - 1).astype(np.float64)
    yn = (yy[sample] / (h - 1) * 2 - 1).astype(np.float64)
    X = np.column_stack([
        np.ones_like(xn), xn, yn, xn*xn, xn*yn, yn*yn,
        xn**3, xn*xn*yn, xn*yn*yn, yn**3,
    ])
    xall = (xx / (w - 1) * 2 - 1).astype(np.float64)
    yall = (yy / (h - 1) * 2 - 1).astype(np.float64)
    terms = [
        np.ones_like(xall), xall, yall, xall*xall, xall*yall, yall*yall,
        xall**3, xall*xall*yall, xall*yall*yall, yall**3,
    ]
    bg = np.empty_like(rgb)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(X, rgb[sample, c], rcond=None)
        bg[..., c] = sum(k*t for k, t in zip(coef, terms))

    # Remove the old background contribution only from partial-alpha pixels.
    af = np.maximum(a[..., None], 0.08)
    clean = np.clip((rgb - (1-a[..., None])*bg) / af, 0, 255)
    partial = (a > 0) & (a < 1)
    out_rgb = rgb.copy()
    out_rgb[partial] = clean[partial]
    out_rgb[a == 0] = 0
    rgba = np.dstack([out_rgb.round().astype(np.uint8), a_u8])
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(output_path, optimize=True)
    print(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wycięcie postaci z tła (rembg + odtwarzanie tła)")
    parser.add_argument("--source", default="/root/rod-ai-studio/assets/izabela/IZABELA_CANON.png",
                        help="Obraz źródłowy")
    parser.add_argument("--output", default="/tmp/iza_dobra.png",
                        help="Ścieżka wyjściowa PNG")
    args = parser.parse_args()
    wytnij(args.source, args.output)
