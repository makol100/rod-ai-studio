#!/usr/bin/env python3
"""Plansze rolki „Przegląd z ogrodów działkowych" (D-0398..D-0411), styl intro C + zdjęcie w ramce. Render HTML→PNG 1080x1920 (playwright, 0 zł).
Użycie: python3 tools/plansze_pzd_news.py"""
import base64, json
from pathlib import Path
Z = Path("/root/rod-ai-studio/data/wiadomosci/pzd_news2/zdjecia")
WY = Path("/root/rod-ai-studio/data/wiadomosci/pzd_news2/plansze"); WY.mkdir(parents=True, exist_ok=True)
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
 ("N0", "", "PRZEGLĄD Z OGRODÓW DZIAŁKOWYCH", Z/"commons_warszawa_ogrody_01.jpg", "fot. Wikimedia Commons, CC BY-SA 4.0 — ROD Ursynów", ["wydanie 2 · 22 września 2026", "9 tematów z ostatnich dni"], ""),
 ("N1a", "1", "OPŁATY ZA GRUNT — CIĄG DALSZY", Z/"zrzut_oplaty_pzd.png", "stanowisko PZD — pzd.pl, 18.09.2026", ["Związek: stawka 0,1 %", "i ochrona dotychczasowych zwolnień"], "NOWE STANOWISKO PZD"),
 ("N1b", "1", "OPŁATY ZA GRUNT — CIĄG DALSZY", Z/"zrzut_oplaty_farmer.png", "farmer.pl, 21.09.2026", ["kuj.-pomorskie: nawet +1200 zł rocznie na ogród", "~200 zł na działkowca", "ministerstwo: 3 % to przypadki sporadyczne"], "USTAWY NADAL NIE MA"),
 ("N2a", "2", "DZIKI NA DZIAŁKACH", Z/"commons_dzik_01.jpg", "fot. Jerzy Strzelecki, Wikimedia Commons, CC BY-SA 3.0", ["ROD Waszyngtona, Warszawa", "gospodarz doliczył się 15 dzików"], "PRZYSZŁY NASTĘPNE"),
 ("N2b", "2", "DZIKI NA DZIAŁKACH", Z/"commons_dzik_02.jpg", "fot. Jerzy Strzelecki, Wikimedia Commons, CC BY-SA 3.0", ["zachowaj spokój, ustąp drogi", "uwaga na dzieci i psy"], "U NAS LAS JEST BLISKO"),
 ("N3", "3", "POŻAR W OGRODZIE", Z/"zrzut_pozar.png", "walczon.pl, 21.09.2026 — ROD IKAR, Mirosławiec", ["noc 20/21 września — spłonął śmietnik", "gasiła straż, policja bada okoliczności"], "ODPADY Z DALA OD ALTAN"),
 ("N4a", "4", "PIENIĄDZE ZE ZWIĄZKU", Z/"zrzut_dotacje.png", "komunikat Krajowego Zarządu PZD, 18.09.2026", ["wodociągi · elektryfikacja · ogrodzenia", "siedziby · pożyczki"], "378 558 ZŁ DLA OGRODÓW"),
 ("N4b", "4", "PIENIĄDZE ZE ZWIĄZKU", Z/"commons_klimat_01.jpg", "fot. Wikimedia Commons, CC BY 4.0", ["Woźniki: 30 000 zł w sierpniu", "w tej turze nas nie ma"], "KOLEJNE NABORY BĘDĄ"),
 ("N5", "5", "BRAMA NA TELEFON", Z/"zrzut_brama.png", "rodrelaksszczaki.pl, 20.09.2026", ["ROD Relaks, Szczaki k. Piaseczna", "jeden numer na działkę, za darmo", "zapisy trwają, prace ruszyły"], "POMYSŁ DO ROZWAŻENIA U NAS"),
 ("N6", "6", "110 LAT OGRODU", Z/"zrzut_ruda.png", "rudaslaska.com.pl, 21.09.2026", ["ROD im. ks. Jana Dzierżona", "Ruda Śląska — jubileusz 19.09"], "GRATULACJE ZE ŚLĄSKA"),
 ("N7", "7", "SAMORZĄD POMAGA", Z/"commons_siedlce_01.jpg", "fot. Krystian Cieślik, Wikimedia Commons, CC BY-SA 3.0 pl", ["Siedlce → ROD „Złote Piaski”", "2 000 zł na infrastrukturę"], "WARTO PYTAĆ W GMINIE"),
 ("N8a", "8", "CO ROBIĆ TERAZ NA DZIAŁCE", Z/"commons_jesien_ogrod_02.jpg", "fot. Wikimedia Commons, CC BY 2.0", ["sadzimy zimozielone", "siejemy warzywa ozime", "ostatnie nasadzenia drzew i krzewów"], "PAŹDZIERNIKOWY „DZIAŁKOWIEC”"),
 ("N8b", "8", "CO ROBIĆ TERAZ NA DZIAŁCE", Z/"commons_szklarnia_01.jpg", "fot. Wikimedia Commons, CC BY-SA 4.0", ["szklarnia i tunel do zimy", "wieloletnie warzywa i zioła pod okrycie", "liście i gałęzie — na kompost"], "„MÓJ OGRÓDEK” — NOWY NUMER"),
 ("N9", "9", "OGRODY A KLIMAT", Z/"zrzut_klimat.png", "stanowisko PZD — pzd.pl, 18.09.2026", ["ROD w polityce klimatycznej państwa", "argument w sporach o plany gmin"], "KIERUNEK: OCHRONA OGRODÓW"),
 ("NK", "", "TO WSZYSTKO NA DZIŚ", Z/"commons_kompost_01.jpg", "fot. Wikimedia Commons", ["zaglądajcie na rodwozniki.pl", "Wiadomości z ogrodu — wydanie 2"], "DO USŁYSZENIA"),
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
