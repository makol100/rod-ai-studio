#!/usr/bin/env python3
"""Plansze rolki „Przegląd z ogrodów działkowych" (D-0398..D-0411), styl intro C + zdjęcie w ramce. Render HTML→PNG 1080x1920 (playwright, 0 zł).
Użycie: python3 tools/plansze_pzd_news3.py"""
import base64, json
from pathlib import Path
Z = Path("/root/rod-ai-studio/data/wiadomosci/pzd_news3/zdjecia")
WY = Path("/root/rod-ai-studio/data/wiadomosci/pzd_news3/plansze"); WY.mkdir(parents=True, exist_ok=True)
LOGO = "data:image/png;base64," + base64.b64encode(Path("/root/rod-ai-studio/assets/branding/rod_logo_kolo.png").read_bytes()).decode()
FONT = "data:font/woff2;base64," + base64.b64encode(Path("/root/rod-ai-studio/www_rod/static/fonts/fraunces-pl.woff2").read_bytes()).decode()
ALEJKA = Path("/root/rod-ai-studio/www_rod/static/img/gal/alejka")

def img(p):
    p = Path(p)
    if not p.exists(): return ""
    from PIL import Image; import io
    im = Image.open(p).convert("RGB"); im.thumbnail((1400, 1400)); b = io.BytesIO(); im.save(b, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

# (klucz_kwestii, nr, tytuł, zdjęcie, podpis zdjęcia, linie tekstu[], wyróżnienie)
P = [
 ("N0", "", "PRZEGLĄD Z OGRODÓW DZIAŁKOWYCH", Z/"wyb_N0_rod.jpg", "fot. Adrian Grycuk, Wikimedia Commons, CC BY 3.0 pl — ROD Spartański", ["wydanie 3 · 29 września 2026", "najpierw Śląsk, potem kraj"], "9 TEMATÓW"),
 ("N1a", "1", "OPŁATY ZA GRUNT U PREZYDENTA", Z/"wyb_N1a_palac.jpg", "fot. Omenaga, Wikimedia Commons, CC BY-SA 4.0 — Pałac Prezydencki", ["Sławomir Barwiak, Okręg Śląski PZD", "spotkanie z szefem Kancelarii Prezydenta"], "PISMO DO PREZYDENTA"),
 ("N1b", "1", "OPŁATY ZA GRUNT U PREZYDENTA", Z/"wyb_N1b_prezydent.jpg", "slaski-ozpzd.pl, 28.09.2026", ["skala problemu i postulaty ochrony działkowców", "dalsze dokumenty — przez posła Marka Wesołego"], "DOTYCZY TEŻ WOŹNIK"),
 ("N2", "2", "GLIWICE POMAGAJĄ OGRODOM", Z/"wyb_N2_gliwice.jpg", "slaski-ozpzd.pl, 28.09.2026 — ROD „Szarotka”", ["1,54 mln zł na 42 ogrody w 2026 r.", "Szarotka: 40 tys. zł dotacji na salę"], "GMINA, KTÓRA POMAGA"),
 ("N3", "3", "KATOWICE: ALEJKA PRZEPADŁA", Z/"wyb_N3_katowice.jpg", "fot. Mike Peel, Wikimedia Commons, CC BY-SA 4.0 — Katowice", ["budżet obywatelski · ROD Kościuszki", "1 112 głosów · 475 000 zł", "w puli Śródmieścia zabrakło miejsca"], "SZKODA"),
 ("N4", "4", "120 LAT OGRODU „PROMIEŃ”", Z/"wyb_N4_promien.jpg", "pzd.pl, 24.09.2026", ["Ruda Śląska — Orzegów", "założony w 1906 roku"], "JEDEN Z NAJSTARSZYCH W POLSCE"),
 ("N5", "5", "BYTOM: DNI DZIAŁKOWCA", Z/"wyb_N5_bytom.jpg", "slaski-ozpzd.pl, 28.09.2026 — ROD „Pod Wierzbami”", ["ogród założony w 1944 roku", "nagrody: „Segregujesz – wygrywasz”"], "32 OGRODY W BYTOMIU"),
 ("N6a", "6", "OPŁATY ZA GRUNT — PRZYKŁADY", Z/"wyb_N6a_lubon.jpg", "gazeta-lubon.pl, 24.09.2026", ["ROD „Nad Wartą”, Luboń", "21 072,94 zł rocznie za cały ogród"], "OK. 160 ZŁ NA DZIAŁKĘ"),
 ("N6b", "6", "OPŁATY ZA GRUNT — PRZYKŁADY", Z/"wyb_N6b_namyslow.jpg", "pzd.pl, 24.09.2026 — stanowisko z Namysłowa", ["Wieliczka: ok. 900 zł na działkę", "duże miasta: nawet 3 000 zł rocznie", "Namysłów: stanowisko przeciw opłatom"], "ZAPOWIEDZI PORZUCANIA DZIAŁEK"),
 ("N7", "7", "LUBLIN: WYPOWIEDZENIA DŁUŻNIKOM", Z/"wyb_N7_lublin.jpg", "Wikimedia Commons, domena publiczna — Lublin", ["ROD „Bystrzyca”", "60 osób z zaległościami za ten rok", "17 także za poprzedni"], "OPŁATY PŁAĆMY W TERMINIE"),
 ("N8", "8", "OPIEKUN DZIAŁKI", Z/"wyb_N8_rod.jpg", "fot. Rakoon, Wikimedia Commons, CC BY 3.0", ["choroba, wyjazd — opiekun za zgodą zarządu", "najwyżej na 2 lata", "odpowiada działkowiec · nie zastąpi na walnym"], "§ 79 REGULAMINU ROD"),
 ("N9", "9", "NYSA CHCE NOWEGO OGRODU", Z/"wyb_N9_nysa.jpg", "fot. Krzysztof Popławski, Wikimedia Commons, CC BY 4.0", ["Związek u burmistrza Nysy", "teren pod nowy ogród działkowy"], "CHĘTNYCH PRZYBYWA"),
 ("NK", "", "TO WSZYSTKO NA DZIŚ", Z/"wyb_NK_alejka.jpg", "nasza alejka — ROD im. Józefa Lompy w Woźnikach", ["zaglądajcie na rodwozniki.pl", "Wiadomości z ogrodu — wydanie 3"], "DO USŁYSZENIA"),
]

HTML = """<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Fraunces ROD";src:url("{font}") format("woff2");font-weight:400 800}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;background:#fffdf6;overflow:hidden}}
body{{font-family:"Fraunces ROD",serif;color:#172019;position:relative}}
.logo{{position:absolute;left:50%;top:70px;width:130px;height:130px;transform:translateX(-50%)}}
.kicker{{position:absolute;left:0;right:0;top:215px;text-align:center;font-size:30px;letter-spacing:.18em;color:#2e7d4f;font-weight:600}}
.nr{{position:absolute;left:70px;top:290px;width:130px;height:130px;border-radius:50%;background:#1f5a37;color:#fffdf6;font-size:84px;font-weight:800;line-height:130px;text-align:center}}
.nr.puste{{display:none}}
.tytul{{position:absolute;left:{tyt_left}px;right:60px;top:290px;height:130px;display:flex;align-items:center;font-size:{tyt_size}px;font-weight:800;color:#1f5a37;line-height:1.05;{tyt_align}}}
.foto{{position:absolute;left:60px;right:60px;top:450px;height:{foto_h}px;border-radius:30px;overflow:hidden;background:#e8efe9;border:6px solid #1f5a37}}
.foto img{{width:100%;height:100%;object-fit:cover;display:block}}
.foto.puste{{display:none}}
.podpis{{position:absolute;left:60px;right:60px;top:{podpis_top}px;font-size:24px;color:#59635b;text-align:center;letter-spacing:.02em}}
.dol{{position:absolute;left:60px;right:60px;top:{dol_top}px;bottom:130px;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:28px}}
.linie{{text-align:center;font-size:{linie_size}px;line-height:1.28;font-weight:500}}
.linie div{{margin-bottom:6px}}
.wyr{{text-align:center;font-size:{wyr_size}px;font-weight:800;color:#fffdf6;background:#2e7d4f;padding:26px 36px;border-radius:26px;line-height:1.2;letter-spacing:.02em;width:100%}}
.wyr:empty{{display:none}}
.stopka{{position:absolute;left:0;right:0;bottom:60px;text-align:center;font-size:28px;color:#59635b;letter-spacing:.08em}}
</style></head><body>
<img class="logo" src="{logo}"><div class="kicker">WIADOMOŚCI Z OGRODU</div>
<div class="nr {nr_klasa}">{nr}</div><div class="tytul"><span>{tytul}</span></div>
<div class="foto {foto_klasa}"><img src="{foto}"></div><div class="podpis">{podpis}</div>
<div class="dol"><div class="linie">{linie}</div><div class="wyr">{wyr}</div></div>
<div class="stopka">ROD IM. JÓZEFA LOMPY W WOŹNIKACH · rodwozniki.pl</div></body></html>"""

def render():
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for klucz, nr, tytul, foto, podpis, linie, wyr in P:
            f = img(foto) if foto else ""
            ma_nr = bool(nr); ma_foto = bool(f)
            foto_h = 700 if ma_foto else 0
            html = HTML.format(font=FONT, logo=LOGO, nr=nr, nr_klasa="" if ma_nr else "puste",
                tytul=tytul, tyt_left=230 if ma_nr else 60, tyt_align="" if ma_nr else "justify-content:center;text-align:center",
                tyt_size=64 if len(tytul) <= 18 else (52 if len(tytul) <= 28 else 44),
                foto=f, foto_klasa="" if ma_foto else "puste", foto_h=foto_h,
                podpis=podpis if ma_foto else "", podpis_top=450+foto_h+14,
                linie="".join(f"<div>{l}</div>" for l in linie), dol_top=(450+foto_h+70) if ma_foto else 700,
                linie_size=44 if sum(len(l) for l in linie) < 80 else 38,
                wyr=wyr, wyr_size=52 if len(wyr) <= 22 else 40)
            pg.set_content(html); pg.evaluate("document.fonts.ready.then(()=>window._f=1)"); pg.wait_for_function("window._f===1"); pg.wait_for_timeout(300)
            geo = pg.evaluate("""() => { const g = s => { const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [Math.round(r.top),Math.round(r.bottom),Math.round(r.height)]; };
                return {tytul:g('.tytul span'), foto:g('.foto'), podpis:g('.podpis'), linie:g('.linie'), wyr:g('.wyr'), stopka:g('.stopka'), tytul_box:g('.tytul')}; }""")
            wady = []
            if geo['tytul'] and geo['tytul_box'] and geo['tytul'][2] > geo['tytul_box'][2] + 2: wady.append('tytul wyzszy niz ramka')
            if geo['wyr'] and geo['stopka'] and geo['wyr'][1] > geo['stopka'][0] - 10: wady.append(f"wyr nachodzi na stopke ({geo['wyr'][1]} > {geo['stopka'][0]-10})")
            if geo['linie'] and geo['wyr'] and geo['linie'][1] > geo['wyr'][0]: wady.append('linie nachodza na wyr')
            if geo['wyr'] and geo['wyr'][1] > 1920: wady.append('wyr poza plansza')
            fn = WY / f"{klucz}.png"; pg.screenshot(path=str(fn)); out[klucz] = str(fn)
            print(klucz, "->", fn.name, "foto" if ma_foto else "BEZ FOTO", "| linie", geo['linie'], "wyr", geo['wyr'], "stopka", geo['stopka'], "| WADY:" if wady else "| OK", ", ".join(wady))
        b.close()
    json.dump(out, open(WY/"_plansze.json", "w"), indent=1)
    return out

if __name__ == "__main__":
    render()
