#!/usr/bin/env python3
"""Grafika do poradnika: WZORZEC §1 umowy kompleksowej TAURON (formularz KSG-10) — gdzie szukać danych
do aplikacji. Odwzorowanie ukladu z umowy Tomasza (17.09.2026) BEZ jego danych (wartosci wzorcowe/zamaskowane).
Render playwright -> www_rod/static/img/umowa_ksg10_gdzie_szukac.png (D-0374)."""
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path("/root/rod-ai-studio/www_rod/static/img/umowa_ksg10_gdzie_szukac.png")
FONT = "data:font/woff2;base64," + base64.b64encode(Path("/root/rod-ai-studio/www_rod/static/fonts/fraunces-pl.woff2").read_bytes()).decode()

def k(et, wart, kl=""):
    return f'<td class="{kl}"><small>{et}</small><b>{wart}</b></td>'

HTML = f"""<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Fraunces ROD";src:url("{FONT}") format("woff2");font-weight:400 800}}
*{{box-sizing:border-box}} body{{margin:0;background:#fffdf6;width:1400px;font-family:Arial,Helvetica,sans-serif;color:#172019}}
.wrap{{padding:34px 40px 30px}}
h1{{font-family:"Fraunces ROD",serif;font-size:34px;margin:0 0 4px;color:#1f5a37}}
.sub{{font-size:19px;color:#59635b;margin:0 0 18px}}
.ksg{{font-size:15px;color:#59635b;float:right;margin-top:-52px}}
table{{width:100%;border-collapse:collapse;font-size:17px;background:#fff}}
td{{border:1.5px solid #333;padding:7px 10px;vertical-align:top;height:58px}}
td small{{display:block;font-size:13px;color:#444;margin-bottom:3px}}
td b{{font-weight:600;letter-spacing:.02em}}
td.mt{{background:#e9f5ee;outline:4px solid #2e7d4f;outline-offset:-4px}}
td.el{{background:#fbf2d6;outline:4px solid #e5b744;outline-offset:-4px}}
td.pusty b{{color:#8a8f8b;font-weight:400;font-style:italic}}
.leg{{display:flex;gap:26px;margin-top:20px;font-size:19px;align-items:center;flex-wrap:wrap}}
.leg span{{display:inline-flex;align-items:center;gap:10px}}
.leg i{{display:inline-block;width:30px;height:30px;border-radius:6px}}
.leg .a{{background:#e9f5ee;border:4px solid #2e7d4f}} .leg .b{{background:#fbf2d6;border:4px solid #e5b744}}
.stopka{{margin-top:16px;font-size:14px;color:#59635b}}
</style></head><body><div class="wrap">
<h1>Umowa kompleksowa dotycząca energii elektrycznej — § 1</h1>
<p class="sub">Strona 3 umowy z TAURON Sprzedaż (formularz KSG-10). Tak wygląda tabela z Twoimi danymi — zaznaczone pola przepisujesz do aplikacji.</p>
<div class="ksg">KSG-10</div>
<table>
<tr>{k("Nr Umowy:", "K/000XXXXX/0/09/26")}{k("Nr PPE:", "590 XXX XXX XXX XXX XXX &nbsp;(18 cyfr)", "el")}<td></td></tr>
<tr>{k("Imię i nazwisko Klienta:", "IMIĘ NAZWISKO")}{k("Nr Płatnika:", "XXXXXXXX &nbsp;(8 cyfr)", "mt")}{k("Nr ewidencyjny:", "(często puste — to normalne)", "pusty")}</tr>
<tr>{k("PESEL/(Numer paszportu dla obcokrajowca):", "XX*XXXX*X*X &nbsp;(Tauron zasłania część cyfr — w aplikacji wpisz swój pełny PESEL)", "mt")}{k("Data zawarcia umowy:", "DD.MM.2026")}{k("Okres obowiązywania umowy:", "nieoznaczony")}</tr>
<tr>{k("Adres punktu poboru — ulica, nr domu, nr lokalu:", "UL. MŁYŃSKA 40C/[nr działki]")}<td colspan="2"><small>Kod pocztowy i miasto/miejscowość:</small><b>42-289 WOŹNIKI</b></td></tr>
<tr>{k("Adres zamieszkania Klienta:", "Twój adres domowy")}<td colspan="2"><small>Kod pocztowy i miasto/miejscowość:</small><b>…</b></td></tr>
<tr>{k("Adres korespondencyjny Klienta:", "Twój adres do listów")}<td colspan="2"><small>Kod pocztowy i miasto/miejscowość:</small><b>…</b></td></tr>
<tr>{k("Telefon kontaktowy komórkowy:", "XXX XXX XXX")}{k("Adres e-mail:", "twoj@e-mail.pl &nbsp;(ten sam podajesz w eLiczniku)", "el")}{k("Energia elektryczna będzie dostarczana na potrzeby:", "LOKALE NIEMIESZKALNE")}</tr>
<tr>{k("Grupa taryfowa Sprzedawcy:", "np. G12W")}{k("Okres rozliczeniowy Sprzedawcy:", "miesięczny")}{k("Podstawa rozliczeń:", "ODCZYT")}</tr>
<tr>{k("Układ pomiarowy 1F/3F:", "np. 1F")}{k("Zabezpieczenie przedlicznikowe [A]:", "np. 20")}{k("Moc umowna / przyłączeniowa [kW]:", "np. 3,5 / 3,5")}</tr>
<tr><td colspan="3"><small>Sprzedawca:</small><b>TAURON Sprzedaż sp. z o.o., Kraków &nbsp;·&nbsp; Operator Systemu Dystrybucyjnego (§ 2 pkt 3): TAURON Dystrybucja S.A.</b></td></tr>
</table>
<div class="leg"><span><i class="a"></i>do aplikacji <b>Mój TAURON</b>: Nr Płatnika + PESEL</span><span><i class="b"></i>do aplikacji <b>eLicznik</b>: Nr PPE + e-mail</span></div>
<p class="stopka">Wzorzec bez danych osobowych. Umowa przychodzi e-mailem (jeśli potwierdziłeś komunikację elektroniczną) albo pocztą na papierze (na prośbę) — układ jest ten sam. ROD im. Józefa Lompy w Woźnikach · rodwozniki.pl</p>
</div></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1400, "height": 1000}, device_scale_factor=2)
    pg.set_content(HTML); pg.evaluate("document.fonts.ready.then(()=>window._f=1)"); pg.wait_for_function("window._f===1"); pg.wait_for_timeout(200)
    h = pg.evaluate("document.body.scrollHeight"); pg.set_viewport_size({"width": 1400, "height": h})
    pg.screenshot(path=str(OUT), full_page=True); b.close()
print("OK", OUT, OUT.stat().st_size, "B, wys.", h)
