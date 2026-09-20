#!/usr/bin/env python3
"""Render plakatu A4 z HTML -> PDF (druk) + PNG (FB/strona), Chromium przez Playwright.
Uzycie: python3 renderuj.py wylaczenie_sieci_30-11-2026.html [nazwa_wyjsciowa]
Assety (logo_rod.png, znak_elektryk.svg) musza lezec obok pliku HTML.

PNG robimy screenshotem przy viewporcie dokladnie A4 (794x1123 px @96dpi)
i deviceScaleFactor=2.6 -> ok. 2064x2920 px (~250 dpi). Na VPS nie ma pdftoppm.
"""
import sys, os, pathlib
from playwright.sync_api import sync_playwright

src = pathlib.Path(sys.argv[1]).resolve()
baza = sys.argv[2] if len(sys.argv) > 2 else src.stem
kat = src.parent
pdf = kat / f"{baza}.pdf"
png = kat / f"{baza}.png"

A4_W, A4_H = 794, 1123  # 210x297 mm przy 96 dpi

with sync_playwright() as pw:
    b = pw.chromium.launch()
    p = b.new_page(viewport={"width": A4_W, "height": A4_H}, device_scale_factor=2.6)
    p.goto(src.as_uri(), wait_until="networkidle")
    p.wait_for_timeout(1500)
    p.pdf(path=str(pdf), format="A4", print_background=True, scale=1, page_ranges="1")
    p.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": A4_W, "height": A4_H})
    b.close()

print("PDF:", pdf, os.path.getsize(pdf), "B")
print("PNG:", png, os.path.getsize(png), "B")
