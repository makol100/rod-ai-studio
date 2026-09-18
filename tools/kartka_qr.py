#!/usr/bin/env python3
"""Kartka z kodem QR do rodwozniki.pl (D-0419, 18.09.2026, 0 zł) — jeden projekt A6, trzy skale:
  kartka A6 (arkusz A4 = 4 kartki 2x2 z liniami ciecia), plakat A4, plakat A3.
Wyjscie: data/kartka_qr/ (PDF do druku + PNG 300 dpi do kontroli). Uzycie: python3 tools/kartka_qr.py
"""
import base64, io, json, sys
from pathlib import Path
import segno

ROOT = Path("/root/rod-ai-studio")
WY = ROOT / "data/kartka_qr"; WY.mkdir(parents=True, exist_ok=True)
ADRES = "https://rodwozniki.pl"
def _jpg(p):
    return "data:image/jpeg;base64," + base64.b64encode(Path(p).read_bytes()).decode()
# D-0421 (18.09 „Dodaj parę grafik związanych z tematem" / „Zobacz co mamy na fb"): grafiki z naszych zasobów, 0 zł —
# lewa: ilustracja tablicy ogłoszeń z FB 04.09 (kadr bez napisów wg oka Genka), prawa: alejka ogrodu (gal/alejka/d4_03)
G1 = _jpg(ROOT / "data/kartka_qr/grafiki/g1_tablica.jpg")
# D-0422 (08:29 „Grafikę nie zdjęcia głąbie"): zdjęcie alejki wypada — prawa strona = własna ilustracja wektorowa (tools/grafika_konewka.py)
sys.path.insert(0, str(ROOT / "tools")); import grafika_konewka
G2 = grafika_konewka.svg()
LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "assets/branding/rod_logo_kolo.png").read_bytes()).decode()
FONT = "data:font/woff2;base64," + base64.b64encode((ROOT / "www_rod/static/fonts/fraunces-pl.woff2").read_bytes()).decode()

def qr_svg():
    """QR jako wektor (inline SVG) — poziom H (30 %), czarny na bialym, strefa ciszy 4 moduly (glosy Henia/Zenka/Genka 18.09)."""
    q = segno.make(ADRES, error="h", boost_error=False)
    svg = q.svg_inline(scale=10, border=4, dark="#000000", light="#ffffff", svgclass=None, lineclass=None, omitsize=True)
    return svg, q.designator, q.symbol_size(scale=1, border=4)[0]

QR, QR_WERSJA, QR_MODULY = qr_svg()

# Tresc (v1 Klaudka — do poprawki po glosach zalogi). ZAKAZ slowa "prezes".
T = dict(
    nazwa="ROD im. Józefa Lompy",
    miejsce="Woźniki · od 1948 roku",
    naglowek="Nasz ogród w Twoim telefonie",
    adres="rodwozniki.pl",
    linie=["Ogłoszenia i komunikaty zarządu", "Tablica ogłoszeń działkowców", "Pogoda dla Woźnik na 8 dni",
           "Kamery — co teraz dzieje się w ogrodzie", "Dokumenty, regulamin, filmy i poradniki"],
    jak_tytul="Jak otworzyć?",
    jak="Włącz aparat w telefonie i skieruj go na kod. Dotknij napisu (linku), który pojawi się na ekranie. "
        "Nie skanujesz? Wpisz w przeglądarce: rodwozniki.pl",
    stopka="ROD im. Józefa Lompy · ul. Młyńska 40c, Woźniki · rodwozniki@gmail.com",
)

CSS = """
@font-face{font-family:"Fraunces ROD";src:url("%(font)s") format("woff2");font-weight:400 800}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:"Fraunces ROD",Georgia,serif;color:#172019;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.karta{width:var(--w,calc(var(--s)*105mm));height:var(--h,calc(var(--s)*148mm));padding:calc(var(--s)*6mm);background:#fbf8ef;position:relative;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;text-align:center}
.karta::before{content:"";position:absolute;inset:calc(var(--s)*3mm);border:calc(var(--s)*0.5mm) solid #2e7d4f;border-radius:calc(var(--s)*3mm);pointer-events:none}
.naglowek{display:flex;align-items:center;gap:calc(var(--s)*3mm);width:100%;justify-content:center;margin-top:calc(var(--s)*1mm)}
.naglowek img{width:calc(var(--s)*17mm);height:calc(var(--s)*17mm)}
.naglowek .t{text-align:left}
.naglowek .n{font-weight:700;font-size:calc(var(--s)*4.2mm);line-height:1.15;color:#183a26}
.naglowek .m{font-size:calc(var(--s)*3mm);color:#2e7d4f;margin-top:calc(var(--s)*0.6mm)}
.tytul{font-weight:800;font-size:calc(var(--s)*5.4mm);line-height:1.15;color:#183a26;margin-top:calc(var(--s)*3mm)}
.srodek{margin-top:calc(var(--s)*3mm);display:flex;align-items:center;justify-content:center;gap:calc(var(--s)*2.5mm)}
.foto{width:calc(var(--q)*0.6);height:var(--q);object-fit:cover;border-radius:calc(var(--s)*2mm);border:calc(var(--s)*0.4mm) solid #cfe3d6;display:block;overflow:hidden;flex:none}
.foto svg{width:100%;height:100%;display:block}
.qr{width:var(--q);height:var(--q);background:#fff;border-radius:calc(var(--s)*1.5mm)}
.qr svg{width:100%;height:100%;display:block}
.adres{font-weight:800;font-size:calc(var(--s)*8mm);line-height:1;color:#2e7d4f;margin-top:calc(var(--s)*2.5mm);letter-spacing:calc(var(--s)*-0.1mm)}
.linie{margin-top:calc(var(--s)*2.5mm);font-size:calc(var(--s)*3.2mm);line-height:1.45;text-align:left}
.linie div::before{content:"✔";color:#2e7d4f;font-weight:800;margin-right:calc(var(--s)*1.6mm)}
.jak{margin-top:calc(var(--s)*2.5mm);background:#fff;border:calc(var(--s)*0.35mm) solid #cfe3d6;border-radius:calc(var(--s)*2mm);padding:calc(var(--s)*2mm) calc(var(--s)*3mm);
  font-size:calc(var(--s)*2.8mm);line-height:1.35;width:100%}
.jak b{color:#183a26}
.stopka{margin-top:auto;font-size:calc(var(--s)*2.7mm);color:#4a5a4f;padding-bottom:calc(var(--s)*0.5mm)}
"""

KARTA = """<div class="karta">
<div class="naglowek"><img src="%(logo)s"><div class="t"><div class="n">%(nazwa)s</div><div class="m">%(miejsce)s</div></div></div>
<div class="tytul">%(naglowek)s</div>
<div class="srodek"><img class="foto" src="%(g1)s"><div class="qr">%(qr)s</div><div class="foto">%(g2)s</div></div>
<div class="adres">%(adres)s</div>
<div class="linie">%(linie)s</div>
<div class="jak"><b>%(jak_tytul)s</b> %(jak)s</div>
<div class="stopka">%(stopka)s</div>
</div>"""

def karta_html(s, q_mm, w_mm=None, h_mm=None):
    w_mm = w_mm or 105 * s; h_mm = h_mm or 148 * s
    d = dict(T, logo=LOGO, qr=QR, g1=G1, g2=G2, linie="".join(f"<div>{l}</div>" for l in T["linie"]))
    return f'<html><head><meta charset="utf-8"><style>:root{{--s:{s};--q:{q_mm}mm;--w:{w_mm}mm;--h:{h_mm}mm}}{CSS.replace("%(font)s", FONT)}</style></head><body>{KARTA % d}</body></html>'

def arkusz_html():
    """A4 pionowo: 4 kartki A6 (2x2) + linie ciecia (kreskowane) — kartki po 105x148, arkusz 210x296."""
    d = dict(T, logo=LOGO, qr=QR, g1=G1, g2=G2, linie="".join(f"<div>{l}</div>" for l in T["linie"]))
    k = KARTA % d
    css = CSS.replace("%(font)s", FONT) + """
    @page{size:A4;margin:0}
    .arkusz{width:210mm;height:296mm;display:grid;grid-template-columns:105mm 105mm;grid-template-rows:148mm 148mm;position:relative}
    .arkusz .karta{outline:0.2mm dashed #9aa79f;outline-offset:-0.1mm}
    """
    return f'<html><head><meta charset="utf-8"><style>:root{{--s:1;--q:42mm}}{css}</style></head><body><div class="arkusz">{k}{k}{k}{k}</div></body></html>'

def render():
    from playwright.sync_api import sync_playwright
    wyniki = {"qr": {"adres": ADRES, "wersja": QR_WERSJA, "moduly_z_cisza": QR_MODULY}}
    with sync_playwright() as p:
        b = p.chromium.launch()
        # --- kontrola geometrii + PNG 300 dpi dla A6 ---
        for nazwa, s, w_mm, h_mm, q_mm in [("kartka_A6", 1, 105, 148, 42), ("plakat_A4", 1.8, 210, 297, 110), ("plakat_A3", 2.35, 297, 420, 170)]:
            px_w, px_h = round(w_mm * 96 / 25.4), round(h_mm * 96 / 25.4)
            pg = b.new_page(viewport={"width": px_w, "height": px_h}, device_scale_factor=300 / 96)
            pg.set_content(karta_html(s, q_mm, w_mm, h_mm)); pg.evaluate("document.fonts.ready.then(()=>window._f=1)"); pg.wait_for_function("window._f===1"); pg.wait_for_timeout(200)
            geo = pg.evaluate("""() => { const k=document.querySelector('.karta'); const r=e=>{const b=e.getBoundingClientRect();return {top:b.top,bottom:b.bottom,left:b.left,right:b.right,w:b.width,h:b.height}};
              const K=r(k); const el={}; for (const s of ['.naglowek','.tytul','.qr','.adres','.linie','.jak','.stopka']) el[s]=r(document.querySelector(s));
              return {karta:K, scroll:[k.scrollWidth,k.clientWidth,k.scrollHeight,k.clientHeight], el}; }""")
            wady = []
            if geo["scroll"][2] > geo["scroll"][3] + 1: wady.append(f"tresc wystaje z karty ({geo['scroll'][2]} > {geo['scroll'][3]})")
            K = geo["karta"]; mm = 96 / 25.4
            for nm, e in geo["el"].items():
                if e["bottom"] > K["bottom"] - 5 * mm * s + 0.5 or e["top"] < K["top"] + 5 * mm * s - 0.5: wady.append(f"{nm} poza marginesem 5mm")
                if e["left"] < K["left"] + 5 * mm * s - 0.5 or e["right"] > K["right"] - 5 * mm * s + 0.5: wady.append(f"{nm} poza marginesem bocznym 5mm")
            q = geo["el"][".qr"]; wyniki[nazwa] = {"qr_mm": round(q["w"] / mm / 1, 1), "wady": wady}
            png = WY / f"{nazwa}.png"; pg.screenshot(path=str(png))
            pdf = WY / f"{nazwa}.pdf"; pg.pdf(path=str(pdf), width=f"{w_mm}mm", height=f"{h_mm}mm", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            print(nazwa, "QR", round(q["w"] / mm, 1), "mm", "| WADY:" if wady else "| OK", ", ".join(wady))
            pg.close()
        # --- arkusz A4 z 4 kartkami ---
        pg = b.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=300 / 96)
        pg.set_content(arkusz_html()); pg.evaluate("document.fonts.ready.then(()=>window._f=1)"); pg.wait_for_function("window._f===1"); pg.wait_for_timeout(200)
        n = pg.evaluate("document.querySelectorAll('.karta').length")
        pg.screenshot(path=str(WY / "arkusz_A4_4xA6.png"), full_page=True)
        pg.pdf(path=str(WY / "arkusz_A4_4xA6.pdf"), format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        wyniki["arkusz_A4_4xA6"] = {"kartek": n}
        print("arkusz A4:", n, "kartek")
        b.close()
    json.dump(wyniki, open(WY / "_wyniki.json", "w"), indent=1, ensure_ascii=False)
    return wyniki

def test_dekod():
    """Test rozstrzygalny: PNG 300 dpi -> 100 dpi + rozmycie -> OpenCV QRCodeDetector musi odczytac ADRES."""
    import cv2, numpy as np
    from PIL import Image, ImageFilter
    wyn = {}
    for nazwa in ["kartka_A6", "plakat_A4", "plakat_A3", "arkusz_A4_4xA6"]:
        im = Image.open(WY / f"{nazwa}.png").convert("RGB")
        for dpi in (300, 100, 72):
            im2 = im.resize((max(1, im.width * dpi // 300), max(1, im.height * dpi // 300)), Image.LANCZOS)
            if dpi < 300: im2 = im2.filter(ImageFilter.GaussianBlur(0.8))
            arr = cv2.cvtColor(np.array(im2), cv2.COLOR_RGB2BGR)
            det = cv2.QRCodeDetector()
            if nazwa.startswith("arkusz"):
                # Zenek/Genek (bramka 18.09): multi-detekcja calego arkusza w 72 dpi dawala 0/4 — telefon skanuje JEDNA kartke,
                # wiec arkusz tniemy na 4 cwiartki (jak nozyczkami) i kazda dekodujemy osobno pojedynczym detektorem
                h, w = arr.shape[:2]; n = 0
                for (y0, x0) in [(0, 0), (0, w // 2), (h // 2, 0), (h // 2, w // 2)]:
                    t, _, _ = det.detectAndDecode(arr[y0:y0 + h // 2, x0:x0 + w // 2])
                    n += (t == ADRES)
                wyn[f"{nazwa}@{dpi}dpi"] = {"odczytane": n, "z": 4}
            else:
                t, pts, _ = det.detectAndDecode(arr)
                wyn[f"{nazwa}@{dpi}dpi"] = {"odczyt": t, "ok": t == ADRES}
    for k, v in wyn.items(): print("DEKOD", k, v)
    return wyn

if __name__ == "__main__":
    if "--test" in sys.argv: test_dekod()
    else:
        render(); test_dekod()
