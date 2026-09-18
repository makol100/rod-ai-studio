#!/usr/bin/env python3
"""Test rozstrzygalny dodatków z 18.09.2026 (D-0430, pkt 2/4/6/12/13 narady) na ŻYWEJ stronie rodwozniki.pl.
Zielony = wszystkie warunki spełnione. Sprawdza też, że sekcja POGODY na głównej ZOSTAŁA (Tomasz: „nie kasuj mi tej pogody z główne!")."""
import re, sys, urllib.request
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 test_dodatki"}), timeout=30).read().decode("utf-8", "replace")
B = "https://rodwozniki.pl"
home = get(B + "/"); bledy = []
# pkt 2: pasek Dziś w ROD nad hero, pogoda zostaje
if 'class="dzis-pasek' not in home: bledy.append("brak paska dzis-pasek")
if home.find('class="dzis-pasek') > home.find('class="hero shell"'): bledy.append("dzis-pasek nie jest nad hero")
if 'id="pogoda-tytul">Teraz w ogrodzie' not in home: bledy.append("SEKCJA POGODY ZNIKNĘŁA z głównej")
if 'id="pogoda-dni"' not in home or 'id="pogoda-radar"' not in home: bledy.append("pogoda: brak prognozy 8 dni/radaru")
# pkt 6: stan robót
if 'id="stan-robot"' not in home or home.count('class="stan-wpis') < 3: bledy.append("kącik Stan robót: brak lub <3 wpisów")
for et in ("Zrobione", "Trwa", "Następne"):
    if et not in home: bledy.append(f"stan robót: brak etykiety {et}")
# pkt 4: zarząd
z = get(B + "/zarzad/")
for n in ("Roman Sitko", "Dariusz Żukowski", "Zofia Zachariasz", "Tomasz Maksyś", "Czesław Perek"):
    if n not in z: bledy.append(f"zarząd: brak {n}")
if 'href="/zarzad/"' not in home: bledy.append("menu: brak linku /zarzad/")
# pkt 13: prawda
d = get(B + "/dla-dzialkowcow/")
if "DO POTWIERDZENIA" in d: bledy.append("dla-dzialkowcow: nadal [DO POTWIERDZENIA]")
f = get(B + "/filmy/")
if "klik otwiera nagranie na Facebooku" in f: bledy.append("filmy: stary opis 'klik otwiera Facebook'")
if 'name="as_sitesearch" value="rodwozniki.pl"' not in home: bledy.append("szukajka: brak ograniczenia do rodwozniki.pl")
js_name = re.search(r'/static/(app[.\w]*\.js)', home).group(1); js = get(B + "/static/" + js_name)
if "łącznie ${d.lacznie_goscie} gości" in js: bledy.append("licznik: stara myląca etykieta")
if "bez robotów" not in js: bledy.append("licznik: brak nowej etykiety")
# pkt 12: mobile 18 px / 44 px (w CSS, blok max-width: 640px)
css_name = re.search(r'/static/(styles[.\w]*\.css)', home).group(1); css = get(B + "/static/" + css_name)
blok = css[css.rfind("@media (max-width: 640px)"):]
if "font-size: 18px" not in blok: bledy.append("mobile: brak body 18px")
if "min-height: 44px" not in blok: bledy.append("mobile: brak 44px dla linków menu")
if '"Fraunces ROD"' not in css: bledy.append("Fraunces zniknął")
# nic nie usunięte z głównej: sekcje sprzed zmiany
for s in ("Podziękowania", 'id="na-dzis"', "section-electric", "asystent-tytul", "section-contact", "Ogrodnik ROD", "Tablica ogłoszeń", "Filmy ROD"):
    if s not in home: bledy.append(f"z głównej zniknęło: {s}")
print("BLEDY:", bledy if bledy else "brak"); print("ZIELONY" if not bledy else "CZERWONY"); sys.exit(1 if bledy else 0)
