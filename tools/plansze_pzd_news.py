#!/usr/bin/env python3
"""Plansze rolki „Przegląd z ogrodów działkowych" (D-0398..D-0411), styl intro C + zdjęcie w ramce. Render HTML→PNG 1080x1920 (playwright, 0 zł).
Użycie: python3 tools/plansze_pzd_news.py"""
import base64, json
from pathlib import Path
Z = Path("/root/rod-ai-studio/data/wiadomosci/pzd_news/zdjecia")
WY = Path("/root/rod-ai-studio/data/wiadomosci/pzd_news/plansze"); WY.mkdir(parents=True, exist_ok=True)
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
 ("N0", "", "PRZEGLĄD Z OGRODÓW DZIAŁKOWYCH", Z/"kdd_01.jpg", "fot. pzd.pl — Krajowe Dni Działkowca 2026", ["7 tematów · wrzesień 2026", "w tym 2 o naszym ogrodzie"], ""),
 ("NRa", "1", "NASZ OKRĘG", Z/"wiki_katowice.jpg", "fot. Wikimedia Commons — Katowice", ["Okręg Częstochowski PZD", "→ Okręg Śląski w Katowicach"], "OD 1 STYCZNIA 2027"),
 ("NRb", "1", "NASZ OKRĘG", Z/"wiki_czestochowa.jpg", "fot. Wikimedia Commons — Częstochowa", ["Częstochowa zostaje REJONEM", "sprawy nadal na miejscu"], "DO KOŃCA ROKU BEZ ZMIAN"),
 ("N1a", "2", "30 000 zł DLA NASZEGO OGRODU", Z/"komunikat_dotacja_zrzut.png", "komunikat Krajowego Zarządu PZD, 13.08.2026", ["ROD im. Józefa Lompy w Woźnikach", "nowa instalacja elektryczna"], "30 000 ZŁ"),
 ("N1b", "2", "PRĄD W ALEJKACH", ALEJKA/"d1_03.jpg", "fot. ROD Woźniki — roboty w górnej alejce", ["Związek rozdał w sierpniu", "1 631 750 zł ogrodom w Polsce"], "MY JESTEŚMY NA LIŚCIE"),
 ("N2a", "3", "OPŁATY ZA GRUNT", Z/"commons_sejm_03.jpg", "fot. A. Barabasz, Wikimedia Commons, CC BY-SA 4.0", ["użytkowanie wieczyste gruntów ogrodów", "w przepisach brak stawki dla ROD"], "GMINA MOŻE NALICZYĆ 3 %"),
 ("N2b", "3", "OPŁATY ZA GRUNT", Z/"wiki_wieliczka.jpg", "fot. Wikimedia Commons — Wieliczka", ["Wieliczka: ok. 900 zł rocznie na działkę", "Ruda Śląska: ok. 8 razy więcej"], "NASZ GRUNT: UŻYTKOWANIE WIECZYSTE"),
 ("N2c", "3", "OPŁATY ZA GRUNT", Z/"commons_sejm_01.jpg", "fot. Kszapsza, Wikimedia Commons, CC BY-SA 4.0", ["PZD chce stawki 0,1 %", "rząd: „ustawy nie zmieniamy”", "prezesi naszego okręgu — stanowisko 27.08"], "BĘDZIE PETYCJA — PODPISZEMY"),
 ("N3a", "4", "STUDNIE I ABISYNKI", Z/"commons_pompa_reczna_01.jpg", "fot. Christian David, Wikimedia Commons, CC BY-SA 4.0", ["abolicja od 18.08.2026", "wniosek do Wód Polskich do 31.12.2027"], "BEZ OPŁATY I BEZ KARY"),
 ("N3b", "4", "STUDNIE I ABISYNKI", Z/"studnie_01.jpg", "pismo Prezesa PZD do ministerstwa — pzd.pl", ["ministerstwo i Wody Polskie mówią różnie", "Związek zapytał — czekamy na odpowiedź"], "NIE PŁAĆ NIKOMU ZA LEGALIZACJĘ"),
 ("N4", "5", "ZAKAZ SPALANIA", Z/"commons_ognisko_liscie_01.jpg", "fot. Jorge Royan, Wikimedia Commons, CC BY-SA 3.0", ["§ 68 pkt 5 Regulaminu ROD", "liście i gałęzie — na kompost"], "MANDAT DO 500 ZŁ"),
 ("N5a", "6", "BEZPIECZEŃSTWO NA JESIEŃ", Z/"irys_01.jpg", "fot. ROD „Irys” Ruda Śląska / rudaslaska.com.pl", ["Ruda Śląska: 3 altany w jedną noc", "zarząd nie wyklucza podpalenia"], "ZAMYKAJ ALTANĘ · ZABIERZ NARZĘDZIA"),
 ("N5b", "6", "BEZPIECZEŃSTWO NA JESIEŃ", Z/"wiki_butla_gazowa.jpg", "fot. Wikimedia Commons", ["Gdańsk: wypadek z gazem, dwie ofiary", "przed zimą sprawdź butle, węże, kuchenkę"], "COŚ PODEJRZANEGO? DZWOŃ 112"),
 ("N6a", "7", "DOBRE WIEŚCI ZE ŚLĄSKA", Z/"najp_dzialka_ozd_01.jpg", "fot. pzd.pl — laureaci konkursów krajowych 2026", ["Piekary Śląskie — I miejsce", "Najpiękniejsza Działka Roku 2026", "Łaziska Górne — III miejsce, Najlepszy ROD"], "GRATULUJEMY"),
 ("N6b", "7", "45 LAT PZD", Z/"kdd_02.jpg", "fot. pzd.pl — Krajowe Dni Działkowca, Ojrzanów 11.09.2026", ["Związek świętował 45 lat", "ponad 250 działkowców z całej Polski"], "DO ZOBACZENIA W OGRODZIE"),
 ("OUTRO", "", "PRZYGOTOWAŁ", "", "", ["Głos to awatar AI Tomasza Maksysia", "wygenerowany za jego zgodą"], "TOMASZ MAKSYŚ"),
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
