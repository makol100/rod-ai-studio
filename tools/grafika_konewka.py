#!/usr/bin/env python3
"""Własna ilustracja wektorowa (0 zł, D-0422 'Grafikę nie zdjęcia'): konewka, pomidory, płotek, słońce — styl płaski,
paleta strony ROD. Zwraca SVG 300x500 (3:5) jako string; --png zapisuje podgląd."""
import sys

def svg(w=300, h=500):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
<defs><linearGradient id="niebo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef6f0"/><stop offset="1" stop-color="#d9ecdd"/></linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#niebo)"/>
<!-- slonce -->
<g stroke="#f2c14e" stroke-width="6" stroke-linecap="round" opacity="0.9">
<line x1="232" y1="22" x2="232" y2="40"/><line x1="232" y1="132" x2="232" y2="150"/><line x1="168" y1="86" x2="186" y2="86"/><line x1="278" y1="86" x2="296" y2="86"/>
<line x1="187" y1="41" x2="200" y2="54"/><line x1="264" y1="118" x2="277" y2="131"/><line x1="187" y1="131" x2="200" y2="118"/><line x1="264" y1="54" x2="277" y2="41"/></g>
<circle cx="232" cy="86" r="34" fill="#f6cf5c"/>
<!-- wzgorza -->
<ellipse cx="90" cy="470" rx="230" ry="110" fill="#9ccf98"/>
<ellipse cx="270" cy="500" rx="220" ry="95" fill="#7fbb7c"/>
<!-- plotek -->
<g fill="#c8925c" stroke="#8a5a2e" stroke-width="3" stroke-linejoin="round">
<rect x="18" y="290" width="264" height="12" rx="3"/><rect x="18" y="334" width="264" height="12" rx="3"/>
<polygon points="34,268 58,268 58,362 34,362"/><polygon points="34,268 46,252 58,268"/>
<polygon points="82,262 106,262 106,362 82,362"/><polygon points="82,262 94,246 106,262"/>
<polygon points="194,262 218,262 218,362 194,362"/><polygon points="194,262 206,246 218,262"/>
<polygon points="242,268 266,268 266,362 242,362"/><polygon points="242,268 254,252 266,268"/></g>
<!-- krzak pomidora -->
<g stroke="#2e7d4f" stroke-width="7" stroke-linecap="round" fill="none">
<path d="M150 372 C150 330 150 290 150 232"/><path d="M150 320 C126 300 118 282 112 262"/><path d="M150 300 C176 284 186 268 190 248"/><path d="M150 260 C130 244 124 232 122 214"/></g>
<g fill="#4a9a5a"><ellipse cx="108" cy="258" rx="20" ry="11" transform="rotate(-35 108 258)"/><ellipse cx="194" cy="244" rx="20" ry="11" transform="rotate(35 194 244)"/>
<ellipse cx="120" cy="212" rx="18" ry="10" transform="rotate(-30 120 212)"/><ellipse cx="164" cy="222" rx="18" ry="10" transform="rotate(25 164 222)"/></g>
<g fill="#e2503c" stroke="#b83a2a" stroke-width="2"><circle cx="128" cy="292" r="17"/><circle cx="176" cy="276" r="15"/><circle cx="150" cy="248" r="14"/></g>
<g fill="#2e7d4f"><path d="M128 275 l-8 -8 l6 1 l-1 -7 l5 5 l2 -7 l3 7 l5 -5 l-1 7 l6 -1 z"/><path d="M176 261 l-7 -7 l5 1 l-1 -6 l4 4 l2 -6 l3 6 l4 -4 l-1 6 l5 -1 z"/><path d="M150 234 l-7 -7 l5 1 l-1 -6 l4 4 l2 -6 l3 6 l4 -4 l-1 6 l5 -1 z"/></g>
<!-- konewka -->
<g>
<path d="M60 372 h82 a12 12 0 0 1 12 12 v66 a12 12 0 0 1 -12 12 h-82 a12 12 0 0 1 -12 -12 v-66 a12 12 0 0 1 12 -12 z" fill="#2e7d4f" stroke="#1f5b38" stroke-width="3"/>
<rect x="48" y="392" width="106" height="10" fill="#1f5b38" opacity="0.5"/>
<path d="M76 372 C60 336 96 330 110 358 C122 336 156 340 142 372" fill="none" stroke="#1f5b38" stroke-width="9" stroke-linecap="round"/>
<path d="M150 410 L212 372 L226 386 L160 430 Z" fill="#2e7d4f" stroke="#1f5b38" stroke-width="3" stroke-linejoin="round"/>
<circle cx="222" cy="378" r="16" fill="#5aa572" stroke="#1f5b38" stroke-width="3"/>
<g fill="#1f5b38"><circle cx="216" cy="372" r="2.2"/><circle cx="224" cy="370" r="2.2"/><circle cx="230" cy="378" r="2.2"/><circle cx="220" cy="382" r="2.2"/><circle cx="228" cy="386" r="2.2"/></g>
<g fill="#6fb3e0"><ellipse cx="246" cy="360" rx="4" ry="7" transform="rotate(-30 246 360)"/><ellipse cx="258" cy="346" rx="4" ry="7" transform="rotate(-30 258 346)"/><ellipse cx="262" cy="372" rx="4" ry="7" transform="rotate(-30 262 372)"/><ellipse cx="274" cy="356" rx="4" ry="7" transform="rotate(-30 274 356)"/></g>
</g>
<!-- marchewki -->
<g><path d="M232 452 l10 40 l10 -40 z" fill="#f08a3c"/><path d="M262 456 l9 36 l9 -36 z" fill="#f08a3c"/>
<g stroke="#3f8a4d" stroke-width="4" stroke-linecap="round" fill="none"><path d="M242 452 v-16"/><path d="M242 452 l-8 -12"/><path d="M242 452 l8 -12"/><path d="M271 456 v-14"/><path d="M271 456 l-7 -11"/><path d="M271 456 l7 -11"/></g></g>
</svg>'''

if __name__ == "__main__":
    s = svg()
    if "--png" in sys.argv:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 300, "height": 500}, device_scale_factor=2)
            pg.set_content(f"<html><body style='margin:0'>{s}</body></html>"); pg.screenshot(path="/root/rod-ai-studio/data/kartka_qr/grafiki/g2_konewka.png"); b.close()
        print("png: data/kartka_qr/grafiki/g2_konewka.png")
    else:
        print(s)
