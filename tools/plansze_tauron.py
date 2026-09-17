#!/usr/bin/env python3
"""Plansze dwoch wydan Tauron (D-0363..D-0368): styl intro C + zrzut ekranu apki w ramce telefonu.
Logo i font jako data URI (lekcja 16.09). Render playwright 1080x1920. 0 USD.
Uzycie: python3 tools/plansze_tauron.py [W1|W2|all]"""
import base64, sys
from pathlib import Path

WY = Path("/root/rod-ai-studio/data/wiadomosci/tauron_apki/plansze")
ZR = Path("/root/rod-ai-studio/data/wiadomosci/tauron_apki/zrzuty")
LOGO = "data:image/png;base64," + base64.b64encode(Path("/root/rod-ai-studio/assets/branding/rod_logo_kolo.png").read_bytes()).decode()
FONT = "data:font/woff2;base64," + base64.b64encode(Path("/root/rod-ai-studio/www_rod/static/fonts/fraunces-pl.woff2").read_bytes()).decode()

def img(nazwa):
    p = ZR / nazwa
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()

# (id, kicker, nr, tytul, zrzuty[list], linie tekstu[list], wyroznienie)
PLANSZE = {
 "W1": [
  ("W1_01", "MÓJ TAURON", "1", "ZAINSTALUJ", ["play_mojtauron.png"], ["Sklep Play · App Store", "wpisz: Mój TAURON"], "ZAINSTALUJ — DARMOWA"),
  ("W1_02", "MÓJ TAURON", "2", "WEŹ UMOWĘ", [], ["NUMER EWIDENCYJNY — z umowy", "(na fakturze: numer płatnika)", "+ Twój PESEL"], "NUMER Z UMOWY · PESEL"),
  ("W1_03", "MÓJ TAURON", "3", "ZAREJESTRUJ SIĘ", ["www_mojtauron_logowanie.png"], ["Serwis: Mój TAURON / eBOK", "Klient indywidualny"], "ZAREJESTRUJ SIĘ"),
  ("W1_04", "MÓJ TAURON", "4", "WPISZ DANE", [], ["PESEL · NUMER Z UMOWY → Dalej", "E-MAIL (dwa razy)", "HASŁO (dwa razy)"], "ZGODY → ZATWIERDŹ"),
  ("W1_05", "MÓJ TAURON", "5", "AKTYWUJ KONTO", [], ["Na e-mail przyjdzie", "LINK AKTYWACYJNY", "— kliknij w niego"], "KONTO GOTOWE"),
  ("W1_06", "MÓJ TAURON", "6", "ZALOGUJ SIĘ", ["mojtauron_android_01.png"], ["e-mail + hasło", "ustaw PIN — 4 cyfry"], "WCHODZISZ JEDNYM RUCHEM"),
  ("W1_07", "MÓJ TAURON", "", "CO MASZ W APLIKACJI", ["mojtauron_android_03.png", "mojtauron_android_07.png", "mojtauron_android_04.png"], ["UMOWA · FAKTURY", "PŁATNOŚĆ JEDNYM KLIKNIĘCIEM · CZAT"], "PYTAJ W ZARZĄDZIE — POMOŻEMY"),
  ("W1_08", "MÓJ TAURON", "", "PEŁNA INSTRUKCJA", [], ["Krok po kroku na naszej stronie"], "rodwozniki.pl/dla-dzialkowcow/"),
 ],
 "W2": [
  ("W2_01", "eLICZNIK", "1", "ZAINSTALUJ", ["play_elicznik.png"], ["Sklep Play · App Store", "wpisz: TAURON eLicznik"], "INNA APLIKACJA NIŻ MÓJ TAURON"),
  ("W2_02", "eLICZNIK", "2", "PRZYGOTUJ UMOWĘ", [], ["Twój E-MAIL", "NUMER PPE — 18 cyfr,", "z umowy (punkt poboru energii)"], "E-MAIL · NUMER PPE Z UMOWY"),
  ("W2_03", "eLICZNIK", "3", "ZAREJESTRUJ SIĘ", ["www_elicznik_logowanie.png"], ["Serwis: eLicznik", "e-mail · hasło · dane z umowy"], "ZAREJESTRUJ SIĘ"),
  ("W2_04", "eLICZNIK", "4", "AKTYWUJ I ZALOGUJ", [], ["LINK AKTYWACYJNY na e-mail", "→ Zaloguj się"], "1 KONTO = 1 UMOWA"),
  ("W2_05", "eLICZNIK", "!", "NIE WIDZISZ LICZNIKA?", [], ["Tauron musi najpierw", "włączyć zdalny odczyt"], "ZGŁOŚ W ZARZĄDZIE"),
  ("W2_06", "eLICZNIK", "", "CO WIDZISZ", ["elicznik_android_01.png"], ["STAN LICZNIKA", "ZUŻYCIE"], "EKRAN STARTOWY"),
  ("W2_07", "eLICZNIK", "", "ZUŻYCIE", ["elicznik_android_06.png", "elicznik_android_07.png"], ["dzień · miesiąc · rok", "godzina po godzinie · porównania"], "ZAKŁADKA ZUŻYCIE"),
  ("W2_08", "eLICZNIK", "", "STRAŻNIK", ["elicznik_android_04.png"], ["powiadomi, gdy zużyjesz", "więcej niż planowałeś"], "USTAW CEL"),
  ("W2_09", "eLICZNIK", "", "PEŁNA INSTRUKCJA", [], ["Krok po kroku na naszej stronie"], "rodwozniki.pl/dla-dzialkowcow/"),
 ],
}

HTML = """<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Fraunces ROD";src:url("{font}") format("woff2");font-weight:400 800}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;background:#fffdf6;overflow:hidden}}
body{{font-family:"Fraunces ROD",serif;color:#172019;position:relative}}
.logo{{position:absolute;left:50%;top:60px;width:130px;height:130px;transform:translateX(-50%)}}
.kicker{{position:absolute;left:0;right:0;top:210px;text-align:center;font-size:30px;letter-spacing:.18em;color:#2e7d4f;font-weight:600}}
.naglowek{{position:absolute;left:60px;right:60px;top:270px;display:flex;align-items:center;justify-content:center;gap:28px}}
.nr{{flex:0 0 auto;width:130px;height:130px;border-radius:50%;background:#1f5a37;color:#fffdf6;font-size:84px;font-weight:800;line-height:130px;text-align:center}}
.nr.puste{{display:none}}
.tytul{{font-size:{tyt_size}px;font-weight:800;color:#1f5a37;line-height:1.08;text-align:center}}
.zrzuty{{position:absolute;left:0;right:0;top:440px;height:{zr_h}px;display:flex;justify-content:center;gap:24px}}
.zrzuty img{{height:100%;width:auto;border-radius:34px;border:8px solid #172019;background:#000;box-shadow:0 14px 40px rgba(24,58,38,.25)}}
.pasek{{position:absolute;left:50%;top:{pasek_top}px;transform:translateX(-50%);width:420px;height:10px;background:#e5b744;border-radius:5px}}
.opis{{position:absolute;left:70px;right:70px;top:{opis_top}px;text-align:center;font-size:{opis_size}px;line-height:1.3;font-weight:600}}
.wyr{{position:absolute;left:60px;right:60px;top:{wyr_top}px;text-align:center;font-size:{wyr_size}px;font-weight:800;color:#fffdf6;background:#2e7d4f;padding:30px 36px;border-radius:26px;line-height:1.2}}
.stopka{{position:absolute;left:0;right:0;bottom:70px;text-align:center;font-size:28px;color:#59635b;letter-spacing:.08em}}
</style></head><body>
<img class="logo" src="{logo}"><div class="kicker">PORADNIK · {kicker}</div>
<div class="naglowek"><div class="nr {nr_klasa}">{nr}</div><div class="tytul">{tytul}</div></div>
<div class="zrzuty">{zrzuty}</div><div class="pasek"></div>
<div class="opis">{opis}</div><div class="wyr">{wyr}</div>
<div class="stopka">ROD IM. JÓZEFA LOMPY W WOŹNIKACH</div>
<script>
window.uloz = function(){{
  const q=s=>document.querySelector(s); const zr=q('.zrzuty'), pas=q('.pasek'), op=q('.opis'), wy=q('.wyr'), st=q('.stopka'), ng=q('.naglowek');
  let h = zr.children.length ? {zr_h} : 0;
  for (let i=0;i<40;i++) {{
    zr.style.height = h+'px'; zr.style.top='440px';
    const base = zr.children.length ? 440+h : ng.getBoundingClientRect().bottom;
    pas.style.top = (base+50)+'px'; op.style.top = (base+50+10+40)+'px';
    wy.style.top = (op.getBoundingClientRect().bottom+40)+'px';
    if (wy.getBoundingClientRect().bottom < st.getBoundingClientRect().top-30 || !zr.children.length) return h;
    h -= 30;
  }}
  return h;
}};
</script></body></html>"""


def render(zestawy):
    from playwright.sync_api import sync_playwright
    WY.mkdir(parents=True, exist_ok=True); out = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        for z in zestawy:
            for (pid, kicker, nr, tytul, zr, linie, wyr) in PLANSZE[z]:
                ma_zr = bool(zr)
                zr_h = 1000 if ma_zr else 0
                zrzuty = "".join(f'<img src="{img(n)}">' for n in zr)
                pasek_top = 440 + zr_h + 50
                html = HTML.format(font=FONT, logo=LOGO, kicker=kicker, nr=nr, nr_klasa="" if nr else "puste", tytul=tytul,
                                   tyt_size=84 if len(tytul) <= 14 else 66, zrzuty=zrzuty, zr_h=zr_h, pasek_top=pasek_top,
                                   opis_top=pasek_top + 50, opis_size=48 if ma_zr else 62, opis="<br>".join(linie),
                                   wyr_top=(pasek_top + 50 + (len(linie) * (48 if ma_zr else 62) * 1.3) + 60), wyr_size=52 if len(wyr) <= 22 else 42, wyr=wyr)
                pg.set_content(html); pg.evaluate("document.fonts.ready.then(()=>window._f=1)"); pg.wait_for_function("window._f===1"); pg.wait_for_timeout(300); pg.evaluate("window.uloz()"); pg.wait_for_timeout(100)
                geo = pg.evaluate("""() => { const els=['.logo','.kicker','.naglowek','.zrzuty','.pasek','.opis','.wyr','.stopka'].map(s=>document.querySelector(s)).filter(e=>e&&getComputedStyle(e).display!=='none');
                  const bx=els.map(e=>e.getBoundingClientRect()); const poza=bx.some(b=>b.bottom>1920||b.right>1080||b.left<0); let nach=false;
                  for(let i=0;i<bx.length;i++)for(let j=i+1;j<bx.length;j++){ if(bx[i].height===0||bx[j].height===0) continue; if(!(bx[i].bottom<=bx[j].top||bx[j].bottom<=bx[i].top)) nach=true;} return {poza,nach}; }""")
                f = WY / f"{pid}.png"; pg.screenshot(path=str(f)); out.append(f)
                print(pid, "OK" if not geo["poza"] and not geo["nach"] else f"PROBLEM {geo}")
        b.close()
    return out


if __name__ == "__main__":
    z = sys.argv[1] if len(sys.argv) > 1 else "all"
    render(["W1", "W2"] if z == "all" else [z])
