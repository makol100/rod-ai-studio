#!/usr/bin/env python3
"""Plansze „Ciekawostki z ogrodu" wydanie 1 (D-0652) (D-0398..D-0411), styl intro C + zdjęcie w ramce. Render HTML→PNG 1080x1920 (playwright, 0 zł).
Użycie: python3 tools/plansze_pzd_news3.py"""
import base64, json
from pathlib import Path
Z = Path("/root/rod-ai-studio/data/ciekawostki/wydanie1/zdjecia")
WY = Path("/root/rod-ai-studio/data/ciekawostki/wydanie1/plansze"); WY.mkdir(parents=True, exist_ok=True)
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
 ("N0", "", "CIEKAWOSTKI Z OGRODU", Z/"wyb_N0_ai.jpg", "grafika wygenerowana przez AI", ["wydanie 1 · 29 września 2026", "10 rzeczy o działkach, o których mało kto wie"], "NOWY CYKL"),
 ("C1a", "1", "PATRON NASZEGO OGRODU", Z/"wyb_C1a_lompa.jpg", "pomnik J. Lompy w Woźnikach — fot. Tobiasz Janus, Wikimedia Commons, CC BY-SA 4.0", ["Józef Lompa 1797–1863", "zmarł w Woźnikach", "nauczyciel, pisarz, tłumacz · 16 dzieci"], "NASZ PATRON"),
 ("C1b", "1", "PATRON NASZEGO OGRODU", Z/"wyb_C1b_lubsza.jpg", "Lubsza, szkoła Józefa Lompy — fot. Przykuta, Wikimedia Commons, CC BY-SA 3.0", ["ogród warzywny i owocowy z pasieką", "„Wskazówki do stosownej uprawy", "wiejskich warzywnych ogrodów”"], "DZIAŁKOWIEC PRZED DZIAŁKAMI"),
 ("C2", "2", "ŚLĄSK: DZIAŁKI OD GÓRNIKÓW", Z/"wyb_C2_wujek.jpg", "KWK Wujek — fot. Andrzej Otrębski, Wikimedia Commons, CC BY-SA 4.0", ["1905: Chorzów i Toszek", "1906: kopalnia Wujek — 1,7 ha", "dla swoich pracowników"], "PONAD 120 LAT TRADYCJI"),
 ("C3", "3", "SCHREBERGARTEN", Z/"wyb_C3_schreber.jpg", "Moritz Schreber, „Die Gartenlaube” 1883 — domena publiczna", ["zmarł 1861 · plac jego imienia 1865", "najpierw łąka do zabawy dla dzieci", "grządki założył nauczyciel"], "W NIEMCZECH PONAD MILION"),
 ("C4", "4", "DZIAŁKA W WIEDNIU", Z/"wyb_C4_wien.jpg", "Wiedeń, KGV Eschenkogel — Wikimedia Commons, CC0", ["Wiedeń: domek do 50 m² + piwnica", "wolno mieszkać cały rok (wyznaczone strefy)", "u nas: altana do 35 m², mieszkać nie wolno"], "1982–86: TYLKO 20 m²"),
 ("C5", "5", "OLBRZYM Z KIELC", Z/"wyb_C5_kielce.jpg", "wazki.pl — ROD im. Stefana Żeromskiego", ["3 800 działek · 163 ha", "z sąsiednimi ogrodami — jeden z największych w Europie"], "U NAS: 51 DZIAŁEK"),
 ("C6", "6", "CO WOLNO HODOWAĆ", Z/"wyb_C6_kury.jpg", "fot. GATETE Pacifique, Wikimedia Commons, CC BY-SA 4.0", ["kury, króliki, gołębie (§ 58)", "gołębie — za zgodą walnego", "orzech, czereśnia: 5 m od granicy", "na słabej podkładce: 3 m"], "REGULAMIN ROD"),
 ("C7", "7", "ILE KOSZTUJE DZIAŁKA", Z/"wyb_C7_ceny.jpg", "farmer.pl, 24.09.2026", ["143 oferty z 14 miast: 6 200 – 289 000 zł", "najczęściej 65–73 tys. zł", "marzec: 385 tys. zł — Poznań, z domkiem"], "PŁACI SIĘ ZA PRZEJĘCIE, NIE ZA ZIEMIĘ"),
 ("C8", "8", "DZIAŁKA RATOWAŁA PRZED GŁODEM", Z/"wyb_C8_victory.jpg", "plakat USA, Office of War Information — domena publiczna", ["przed wojną: 606 ogrodów, ok. 50 tys. działek", "okupacja: z 300 m² nawet 900 kg ziemniaków"], "OGRODY ZWYCIĘSTWA"),
 ("C9", "9", "DZIAŁKI SĄ STARSZE, NIŻ MYŚLIMY", Z/"wyb_C9_anglia.jpg", "działki w Anglii — fot. Mr Ignavy, geograph.org.uk, CC BY-SA 2.0", ["1732: Birmingham otoczone ogródkami", "1778: Dania — ziemia pod działki", "Anglia dziś: czekanie nawet 9 lat"], "NIE TYLKO U NAS"),
 ("C10", "10", "KTO UPRAWIA DZIAŁKI", Z/"wyb_C10_rod.jpg", "działkowiec przy pracy, Kilonia — fot. Friedrich Magnussen, Wikimedia Commons, CC BY-SA 3.0 de", ["ok. 5 000 ogrodów · ok. 966 tys. działek", "46,9 % działkowców to emeryci i renciści"], "AKTYWNA EMERYTURA"),
 ("OUTRO", "", "PRZYGOTOWAŁ", "", "", ["Głos to awatar AI Tomasza Maksysia", "wygenerowany za jego zgodą"], "TOMASZ MAKSYŚ"),
 ("NK", "", "TO WSZYSTKO NA DZIŚ", Z/"wyb_NK_alejka.jpg", "ROD im. Adama Mickiewicza — fot. Rakoon, Wikimedia Commons, CC0", ["zaglądajcie na rodwozniki.pl", "Ciekawostki z ogrodu — wydanie 1"], "DO USŁYSZENIA"),
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
<img class="logo" src="{logo}"><div class="kicker">CIEKAWOSTKI Z OGRODU</div>
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
            if klucz in ("C6", "C7"):  # 29.09: kwestie C6/C7 podzielone na a/b — ta sama plansza
                import shutil as _sh
                for _s in ("a", "b"): _sh.copy(fn, WY / f"{klucz}{_s}.png")
            print(klucz, "->", fn.name, "foto" if ma_foto else "BEZ FOTO", "| linie", geo['linie'], "wyr", geo['wyr'], "stopka", geo['stopka'], "| WADY:" if wady else "| OK", ", ".join(wady))
        b.close()
    json.dump(out, open(WY/"_plansze.json", "w"), indent=1)
    return out

if __name__ == "__main__":
    render()
