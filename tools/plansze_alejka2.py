#!/usr/bin/env python3
"""Plansze wydania „Alejka Północna — ciąg dalszy" (D-0351/D-0354), styl intro C.
Render HTML -> PNG 1080x1920 przez playwright. 0 USD.
Użycie: python3 tools/plansze_alejka2.py [--telegram]
"""
import sys
import urllib.request
from pathlib import Path

WY = Path("/root/rod-ai-studio/data/wiadomosci/alejka2/plansze")
import base64 as _b64
# D-0357: logo i font jako data URI — file:// w set_content NIE laduje sie (v1/v2 bez logo)
LOGO = "data:image/png;base64," + _b64.b64encode(Path("/root/rod-ai-studio/assets/branding/rod_logo_kolo.png").read_bytes()).decode()
FONT = "data:font/woff2;base64," + _b64.b64encode(Path("/root/rod-ai-studio/www_rod/static/fonts/fraunces-pl.woff2").read_bytes()).decode()

# (numer, tytuł, objaśnienie/druga linia, wyróżnienie)
PLANSZE = [
    ("1", "KABLE W ZIEMI", "Położone i zasypane.<br>Do 2 tygodni gleba i kabel muszą się uleżeć.", ""),
    ("2", "PODŁĄCZENIE", "Kable łączymy z zabezpieczonymi miejscami licznikowymi — każde przypisane do swojej działki.", ""),
    ("3", "TWÓJ ELEKTRYK", "Zabezpiecza nowy kabel u Ciebie na działce i daje PROTOKÓŁ.", "DO SZAFKI TYLKO UPRAWNIONY ELEKTRYK"),
    ("4", "ZARZĄD → KDT", "Z protokołem do Tomasza Maksysia. Dostajesz KARTĘ DANYCH TECHNICZNYCH.", "KDT = LEGITYMACJA TWOJEJ DZIAŁKI DLA PRĄDU"),
    ("5", "UMOWA Z TAURONEM", "Z kartą KDT podpisujesz umowę na prąd — jak na telefon.", "LUBLINIEC, UL. KLONOWA 1"),
    ("6", "LICZNIK", "Tauron montuje licznik. Zgłoś to Tomaszowi Maksysiowi.", "PRZEPIĘCIE · STARY LICZNIK · OSTATNI STAN"),
    ("!", "ZA LICZNIKIEM", "Kabel, szafka i instalacja za licznikiem są po Twojej stronie.", "TYLKO UPRAWNIONY ELEKTRYK"),
    ("!", "AWARIA?", "Sieć, złącze albo licznik — dzwoń.", "991"),
    ("", "PEŁNA INSTRUKCJA", "Wszystko krok po kroku na naszej stronie.", "rodwozniki.pl/dla-dzialkowcow/"),
    ("", "PRZYGOTOWAŁ", "Wydanie przygotował", "TOMASZ MAKSYŚ"),
]

HTML = """<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Fraunces ROD";src:url("{font}") format("woff2");font-weight:400 800}}
*{{margin:0;padding:0}} html,body{{width:1080px;height:1920px;background:#fffdf6;overflow:hidden}}
body{{font-family:"Fraunces ROD",serif;color:#172019;position:relative}}
.logo{{position:absolute;left:50%;top:150px;width:170px;height:170px;transform:translateX(-50%)}}
.kicker{{position:absolute;left:0;right:0;top:360px;text-align:center;font-size:34px;letter-spacing:.18em;color:#2e7d4f;font-weight:600}}
.nr{{position:absolute;left:50%;top:470px;transform:translateX(-50%);width:230px;height:230px;border-radius:50%;
  background:#1f5a37;color:#fffdf6;font-size:150px;font-weight:800;line-height:230px;text-align:center}}
.nr.puste{{display:none}}
.tytul{{position:absolute;left:60px;right:60px;top:{tyt_top}px;text-align:center;font-size:{tyt_size}px;font-weight:800;color:#1f5a37;line-height:1.12}}
.pasek{{position:absolute;left:50%;top:{pasek_top}px;transform:translateX(-50%);width:420px;height:10px;background:#e5b744;border-radius:5px}}
.opis{{position:absolute;left:90px;right:90px;top:{opis_top}px;text-align:center;font-size:56px;line-height:1.35;font-weight:500}}
.wyr{{position:absolute;left:60px;right:60px;top:{wyr_top}px;text-align:center;font-size:{wyr_size}px;font-weight:800;color:#fffdf6;
  background:#2e7d4f;padding:34px 40px;border-radius:26px;line-height:1.2;letter-spacing:.02em}}
.wyr:empty{{display:none}}
.stopka{{position:absolute;left:0;right:0;bottom:90px;text-align:center;font-size:30px;color:#59635b;letter-spacing:.08em}}
</style></head><body>
<img class="logo" src="{logo}"><div class="kicker">WIADOMOŚCI Z OGRODU</div>
<div class="nr {nr_klasa}">{nr}</div>
<div class="tytul">{tytul}</div><div class="pasek"></div>
<div class="opis">{opis}</div><div class="wyr">{wyr}</div>
<div class="stopka">ROD IM. JÓZEFA LOMPY W WOŹNIKACH</div></body></html>"""


def render() -> list[Path]:
    from playwright.sync_api import sync_playwright
    WY.mkdir(parents=True, exist_ok=True)
    pliki = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        for i, (nr, tytul, opis, wyr) in enumerate(PLANSZE, 1):
            ma_nr = bool(nr)
            html = HTML.format(font=FONT, logo=LOGO, nr=nr, nr_klasa="" if ma_nr else "puste",
                               tytul=tytul, opis=opis, wyr=wyr,
                               tyt_top=760 if ma_nr else 560, tyt_size=96 if len(tytul) <= 14 else 80,
                               pasek_top=1000 if ma_nr else 800, opis_top=1060 if ma_nr else 860,
                               wyr_top=1420 if ma_nr else 1220,
                               wyr_size=64 if len(wyr) <= 20 else 46)
            pg.set_content(html)
            pg.evaluate("document.fonts.ready.then(()=>window._f=1)"); pg.wait_for_function("window._f===1")
            pg.wait_for_timeout(400)
            f = WY / f"plansza_{i:02d}.png"
            pg.screenshot(path=str(f))
            pliki.append(f)
        b.close()
    return pliki


def na_telegram(pliki: list[Path]) -> bool:
    import json
    token = chat = ""
    for l in open("/home/hermes/.hermes/.env", encoding="utf-8", errors="replace"):
        k, _, w = l.strip().partition("="); w = w.strip().strip('"').strip("'")
        if k == "HANS_BOT_TOKEN": token = w
        elif k == "HANS_CHAT_ID": chat = w
    granica = "----plansze"
    media = [{"type": "photo", "media": f"attach://p{i}",
              **({"caption": "PLANSZE wydania Alejka Północna cd. (styl intro C, 0 zł) — do akceptacji"} if i == 0 else {})}
             for i in range(len(pliki))]
    cz = (f"--{granica}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat}\r\n"
          f"--{granica}\r\nContent-Disposition: form-data; name=\"media\"\r\n\r\n{json.dumps(media)}\r\n").encode()
    for i, f in enumerate(pliki):
        cz += (f"--{granica}\r\nContent-Disposition: form-data; name=\"p{i}\"; filename=\"{f.name}\"\r\n"
               f"Content-Type: image/png\r\n\r\n").encode() + f.read_bytes() + b"\r\n"
    cz += f"--{granica}--\r\n".encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMediaGroup", data=cz,
                                 headers={"Content-Type": f"multipart/form-data; boundary={granica}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return b'"ok":true' in r.read()


if __name__ == "__main__":
    pliki = render()
    print("plansze:", len(pliki), "->", WY)
    if "--telegram" in sys.argv:
        print("telegram:", "OK" if na_telegram(pliki) else "BLAD")
