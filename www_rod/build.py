#!/usr/bin/env python3
"""Dependency-free builder for the static ROD website."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
CONTENT = ROOT / "content"


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def parse_page(path: Path) -> tuple[dict[str, str], str]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise ValueError(f"{path}: brak front matter")
    _, head, body = raw.split("---\n", 2)
    meta: dict[str, str] = {}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    for required in ("title", "description", "slug"):
        if not meta.get(required):
            raise ValueError(f"{path}: brak pola {required}")
    return meta, body.strip()


def inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\[([^]]+)]\(((?:https?://|mailto:|/)[^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def markdown(text: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline(' '.join(paragraph))}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    raw_html = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == ":::html":
            flush_paragraph(); close_list(); raw_html = True; continue
        if line == ":::" and raw_html:
            raw_html = False; continue
        if raw_html:
            output.append(raw_line); continue
        if not line:
            flush_paragraph()
            close_list()
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            continue
        item = re.match(r"^([-*]|\d+\.)\s+(.+)$", line)
        if item:
            flush_paragraph()
            wanted = "ol" if item.group(1)[0].isdigit() else "ul"
            if list_type != wanted:
                close_list()
                list_type = wanted
                output.append(f"<{wanted}>")
            output.append(f"<li>{inline(item.group(2))}</li>")
            continue
        if line.endswith("  "):
            paragraph.append(line[:-2] + "<br>")
        else:
            paragraph.append(line)
    flush_paragraph()
    close_list()
    return "\n".join(output)


def render(template: str, values: dict[str, str]) -> str:
    result = template
    for key, value in values.items():
        result = result.replace("{{" + key + "}}", value)
    leftovers = re.findall(r"{{[^}]+}}", result)
    if leftovers:
        raise ValueError(f"nieuzupełnione pola szablonu: {leftovers}")
    return result


def page_content(title: str, body: str) -> str:
    body = re.sub(r"^<h1>.*?</h1>\s*", "", body, count=1, flags=re.S)
    return (
        '<header class="page-hero shell"><p class="eyebrow">ROD Woźniki</p>'
        f"<h1>{html.escape(title)}</h1></header>"
        f'<article class="page-content">{body}</article>'
    )


def announcement_html(item: dict) -> str:
    return (
        f'<div><h2 id="pilne-tytul">{html.escape(item["title"])}</h2>'
        f'<p>{html.escape(item["display_date"])} · {html.escape(item["place"])}</p></div>'
        '<a class="button" href="/ogloszenia/">Szczegóły' + (' i film' if item.get("video_fb") else '') + '</a>'
    )


def ostatnie_ogloszenia_html(items: list[dict]) -> str:
    rows = []
    for item in sorted(items, key=lambda row: row["date"], reverse=True)[:3]:
        rows.append(f'<li><time datetime="{html.escape(item["date"])}">{html.escape(item["display_date"])}</time><a href="/ogloszenia/#{html.escape(item["id"])}">{html.escape(item["title"])}</a></li>')
    return '<ul class="ogl-lista">' + "".join(rows) + '</ul>'


def announcements_page(items: list[dict]) -> str:
    cards = []
    for item in sorted(items, key=lambda row: row["date"], reverse=True):
        cards.append(
            '<li class="announcement-item" id="' + html.escape(item["id"]) + '">'
            f'<time datetime="{html.escape(item["date"])}">{html.escape(item["display_date"])}</time>'
            f'<h2>{html.escape(item["title"])}</h2>'
            f'<p><strong>{html.escape(item["place"])}</strong></p>'
            f'<p>{html.escape(item["body"])}</p>'
            + (f'<img class="ogl-foto" src="/static/img/{html.escape(item["image"])}" alt="" loading="lazy">' if item.get("image") else "")
            + (
                _ogl_film_html(item)
                if item.get("video_fb") else ""
            )
            + '</li>'
        )
    return '<header class="page-hero shell"><p class="eyebrow">Bądź na bieżąco</p><h1>Ogłoszenia</h1></header><section class="page-content"><ul class="announcement-list">' + "".join(cards) + "</ul></section>"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


KATEGORIE_TABLICA = {"sprzedam": "Sprzedam", "oddam": "Oddam za darmo", "kupie": "Kupię", "pomoc": "Szukam pomocy", "zguby": "Zguby i znaleziska", "inne": "Inne"}


def _fb_tresc_bez_tytulu(it) -> str:
    """Tytul to pierwsza linia tresci — nie pokazywac jej drugi raz."""
    tresc = it.get("tresc", "")
    tytul = it.get("tytul", "")
    if tytul and tresc.startswith(tytul):
        tresc = tresc[len(tytul):].lstrip("\n ")
    return tresc


def _ogl_film_html(item) -> str:
    """Film z ogłoszenia: D-0315 — gra w oknie na stronie z własnego mp4, nie na Facebooku."""
    import re as _re
    fb = item.get("video_fb", "")
    m = _re.search(r"(\d{12,})", fb)
    mini = "/static/img/" + html.escape(item.get("video_img", "ogloszenie_sezon.jpg"))
    lokalny = (ROOT / "static" / "wideo" / f"{m.group(1)}.mp4") if m else None
    if lokalny and lokalny.is_file():
        return (f'<a class="fb-wideo" href="/static/wideo/{m.group(1)}.mp4" data-wideo="/static/wideo/{m.group(1)}.mp4" data-mini="{mini}" aria-label="Obejrzyj film">'
                f'<img src="{mini}" width="720" height="1280" alt="Kadr z filmu z ogłoszeniem" loading="lazy">'
                '<span class="play" aria-hidden="true">▶</span><span class="fb-podpis">Obejrzyj film</span></a>')
    return (f'<a class="fb-wideo" href="{html.escape(fb)}" rel="noopener" aria-label="Obejrzyj film">'
            f'<img src="{mini}" width="720" height="1280" alt="Kadr z filmu z ogłoszeniem" loading="lazy">'
            '<span class="play" aria-hidden="true">▶</span><span class="fb-podpis">Obejrzyj film</span></a>')


def wideo_html(kategoria: str) -> str:
    try:
        items = [x for x in load_json(CONTENT / "wideo.json") if x.get("kategoria") == kategoria]
    except Exception:
        items = []
    if not items:
        return '<p class="muted">Wkrótce pojawią się tu nagrania.</p>'
    karty = []
    for it in items[:12]:
        mini = f'<img src="{html.escape(it.get("miniaturka",""))}" alt="" loading="lazy">' if it.get("miniaturka") else ""
        wid = it.get("wideo") or ""
        atr = f' data-wideo="{html.escape(wid)}" data-mini="{html.escape(it.get("miniaturka",""))}"' if wid else ' rel="noopener"'
        dopisek = "" if wid else " · Facebook"
        karty.append(f'<a class="wideo-karta" href="{html.escape(wid or it["link"])}"{atr}>'
                     f'<span class="wideo-mini">{mini}<span class="wideo-play" aria-hidden="true">▶</span></span>'
                     f'<span class="wideo-tyt">{html.escape(it["tytul"])}</span>'
                     f'<span class="wideo-data">{html.escape(it.get("display_date",""))}{dopisek}</span></a>')
    return '<div class="wideo-lista">' + "".join(karty) + '</div>'


def fb_posty_html() -> str:
    try:
        items = load_json(CONTENT / "fb_posty.json")
    except Exception:
        items = []
    if not isinstance(items, list) or not items:
        return '<p class="muted">Wpisy pojawią się wkrótce.</p>'
    ETYK = {"powitanie": "Dzień dobry", "porada": "Porada dnia", "ostrzezenie": "Ostrzeżenie", "ogloszenie": "Ogłoszenie"}
    rows = []
    for it in items:
        tresc = html.escape(_fb_tresc_bez_tytulu(it)).replace("\n", "<br>")
        rows.append(f'<article class="fb-wpis fb-{it.get("typ","porada")}"><div class="fb-head"><span class="ogl-kat">{ETYK.get(it.get("typ"),"Wpis")}</span><time>{html.escape(it.get("display_date",""))} · {html.escape(it.get("godz",""))}</time></div>'
                    f'<h3>{html.escape(it["tytul"])}</h3><div class="fb-tresc">{tresc}</div><a class="text-link" href="{html.escape(it["link"])}" rel="noopener">Zobacz na Facebooku <span aria-hidden="true">→</span></a></article>')
    return '<div class="fb-lista">' + "".join(rows) + '</div>'


def fb_posty_skrot() -> str:
    try:
        items = load_json(CONTENT / "fb_posty.json")
    except Exception:
        items = []
    if not isinstance(items, list) or not items:
        return '<p class="muted">Codzienne wpisy Ogrodnika ROD.</p>'
    it = items[0]
    return f'<p class="fb-skrot-tyt">{html.escape(it["tytul"])}</p><p class="fb-skrot-tresc">{html.escape(_fb_tresc_bez_tytulu(it)[:140])}…</p>'


def porady_miesiaca_html() -> str:
    import datetime as _dt
    try:
        p = load_json(CONTENT / "porady_miesiace.json")
    except Exception:
        return ""
    m = str(_dt.date.today().month)
    MIES = ["", "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]
    lista = p.get(m, [])
    if not lista:
        return ""
    return f'<p class="card-label">Co robić teraz — {MIES[int(m)]}</p><ul class="porady-lista">' + "".join(f"<li>{html.escape(x)}</li>" for x in lista) + "</ul>"


def tablica_skrot() -> str:
    try:
        items = load_json(CONTENT / "tablica.json")
    except Exception:
        items = []
    if not isinstance(items, list) or not items:
        return '<p class="muted">Jeszcze nie ma ogłoszeń — dodaj pierwsze na tablicy.</p>'
    rows = []
    for it in items[:3]:
        kat = KATEGORIE_TABLICA.get(it.get("kategoria", "inne"), "Inne")
        rows.append(f'<li><span class="ogl-kat ogl-kat-{html.escape(it.get("kategoria","inne"))}">{kat}</span> {html.escape(it["tytul"])}</li>')
    return '<ul class="tablica-skrot">' + "".join(rows) + '</ul>'


def tablica_html() -> str:
    try:
        items = load_json(CONTENT / "tablica.json")
    except Exception:
        items = []
    if not isinstance(items, list) or not items:
        return '<p class="muted">Na razie brak ogłoszeń. Bądź pierwszy — wyślij swoje powyżej.</p>'
    rows = []
    for it in items:
        kat = KATEGORIE_TABLICA.get(it.get("kategoria", "inne"), "Inne")
        kontakt = f'<p class="ogl-kontakt">Kontakt: {html.escape(it["kontakt"])}</p>' if it.get("kontakt") else ""
        podpis = " · ".join(x for x in [html.escape(it.get("imie", "")), ("działka " + html.escape(it["dzialka"])) if it.get("dzialka") else ""] if x)
        rows.append(
            f'<li class="ogl-tab"><div class="ogl-tab-head"><span class="ogl-kat ogl-kat-{html.escape(it.get("kategoria","inne"))}">{kat}</span>'
            f'<time>{html.escape(it.get("display_date",""))}</time></div>'
            f'<h3>{html.escape(it["tytul"])}</h3><p>{html.escape(it["tresc"])}</p>{kontakt}'
            + (f'<p class="ogl-od">{podpis}</p>' if podpis else "") + '</li>')
    return '<ul class="ogl-tablica">' + "".join(rows) + '</ul>'


def build() -> list[Path]:
    site = load_json(CONTENT / "site.json")
    announcements = load_json(CONTENT / "announcements.json")
    if not isinstance(announcements, list) or not announcements:
        raise ValueError("announcements.json: wymagana niepusta lista")

    DIST.mkdir(parents=True, exist_ok=True)
    static_dest = DIST / "static"
    shutil.copytree(ROOT / "static", static_dest, dirs_exist_ok=True)
    image_dest = static_dest / "img"
    image_dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT.parent / "assets/branding/rod_logo_kolo.png", image_dest / "logo.png")
    shutil.copy2(ROOT.parent / "data/rolka-prad/mapy-16x9/MAPA-OGRODU-16x9.jpg", image_dest / "mapa-ogrodu.jpg")
    shutil.copy2(ROOT.parent / "data/rolka-prad/do-rolki/ZK-z-tablica-ROD.jpg", image_dest / "elektryfikacja.jpg")
    shutil.copy2(ROOT / "static/img/jozef_lompa.jpg", image_dest / "jozef_lompa.jpg")
    shutil.copy2(ROOT / "static/img/a14.svg", image_dest / "a14.svg")

    layout = (ROOT / "templates/page.html").read_text(encoding="utf-8")
    home = (ROOT / "templates/home.html").read_text(encoding="utf-8")
    # Karta na stronie glownej: "Najblizsze wydarzenie" tylko gdy termin przed nami; po imprezie -> "Ostatnie wydarzenie"
    from datetime import datetime as _dt, timedelta as _td, timezone as _tz
    _teraz = _dt.now(_tz.utc)
    def _kiedy(item):
        try: return _dt.fromisoformat(item["date"])
        except Exception: return _teraz
    _przyszle = [a for a in announcements if _kiedy(a) >= _teraz - _td(hours=6)]
    if _przyszle:
        featured = next((a for a in _przyszle if a.get("featured")), min(_przyszle, key=_kiedy))
        featured_kicker = "Najbliższe wydarzenie"
    else:
        featured = max(announcements, key=_kiedy)
        featured_kicker = "Ostatnie wydarzenie"
    home_body = render(home, {"featured_announcement": announcement_html(featured), "featured_kicker": featured_kicker, "ostatnie_ogloszenia": ostatnie_ogloszenia_html(announcements), "tablica_skrot": tablica_skrot(), "fb_skrot": fb_posty_skrot(), "porady_miesiaca": porady_miesiaca_html()})
    generated: list[Path] = []

    def make_page(path: Path, *, title: str, description: str, canonical: str, content: str, body_class: str = "") -> None:
        write(path, render(layout, {
            "title": html.escape(title, quote=True),
            "description": html.escape(description, quote=True),
            "canonical": html.escape(canonical, quote=True),
            "content": content,
            "body_class": body_class,
        }))
        generated.append(path)

    make_page(
        DIST / "index.html",
        title=site["short_name"],
        description="Ogłoszenia, informacje dla działkowców, kamery, pogoda i aktualności ROD Woźniki.",
        canonical=site["url"] + "/",
        content=home_body,
        body_class="home",
    )
    make_page(
        DIST / "ogloszenia/index.html",
        title="Ogłoszenia",
        description="Aktualne ogłoszenia zarządu ROD im. Józefa Lompy w Woźnikach.",
        canonical=site["url"] + "/ogloszenia/",
        content=announcements_page(announcements),
    )

    for path in sorted((CONTENT / "pages").glob("*.md")):
        meta, body = parse_page(path)
        make_page(
            DIST / meta["slug"] / "index.html",
            title=meta["title"],
            description=meta["description"],
            canonical=f'{site["url"]}/{meta["slug"]}/',
            content=page_content(meta["title"], markdown(body).replace("{{tablica_ogloszen}}", tablica_html()).replace("{{fb_posty}}", fb_posty_html()).replace("{{wideo_rolki}}", wideo_html("rolki")).replace("{{wideo_wiadomosci}}", wideo_html("wiadomosci")).replace("{{wideo_humor}}", wideo_html("humor"))),
        )

    paths = ["/", "/ogloszenia/"] + [f"/{parse_page(path)[0]['slug']}/" for path in sorted((CONTENT / "pages").glob("*.md"))]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(
        f"  <url><loc>{site['url']}{path}</loc><lastmod>{site['updated']}</lastmod></url>" for path in paths
    ) + "\n</urlset>\n"
    write(DIST / "sitemap.xml", sitemap)
    write(DIST / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {site['url']}/sitemap.xml\n")
    write(DIST / "404.html", render(layout, {
        "title": "Nie znaleziono strony",
        "description": "Ta strona nie istnieje.",
        "canonical": site["url"] + "/404.html",
        "content": '<header class="page-hero shell"><p class="eyebrow">Błąd 404</p><h1>Ta alejka prowadzi donikąd.</h1></header><section class="page-content"><p><a class="button button-primary" href="/">Wróć na stronę główną</a></p></section>',
        "body_class": "error-page",
    }))
    generated.extend([DIST / "sitemap.xml", DIST / "robots.txt", DIST / "404.html"])
    return generated


def validate_sources() -> list[str]:
    errors: list[str] = []
    try:
        site = load_json(CONTENT / "site.json")
        announcements = load_json(CONTENT / "announcements.json")
    except (OSError, json.JSONDecodeError) as exc:
        return [str(exc)]
    for key in ("name", "short_name", "address", "plots", "url", "updated"):
        if key not in site:
            errors.append(f"site.json: brak {key}")
    if not isinstance(announcements, list):
        errors.append("announcements.json: korzeń nie jest listą")
    for page in (CONTENT / "pages").glob("*.md"):
        try:
            parse_page(page)
        except ValueError as exc:
            errors.append(str(exc))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="sprawdź źródła bez budowania")
    args = parser.parse_args()
    errors = validate_sources()
    if errors:
        print("BŁĘDY:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    if args.check:
        print("OK: źródła JSON/Markdown poprawne")
        return 0
    generated = build()
    print(f"OK: zbudowano {len(generated)} plików stron i SEO w {DIST}")
    return 0


# CACHE_BUST (03.09): po kazdym buildzie podmien ?v= na skrot CSS+JS, zeby telefony nie trzymaly starych plikow
def _cache_bust():
    import hashlib, re as _re
    dist = ROOT / "dist"
    v = hashlib.md5((dist / "static/styles.css").read_bytes() + (dist / "static/app.js").read_bytes()).hexdigest()[:8]
    for html in dist.rglob("*.html"):
        s = html.read_text(encoding="utf-8")
        s = _re.sub(r'/static/styles(?:\.[0-9a-f]{8})?\.css(\?v=\w+)?', "/static/styles." + v + ".css", s)
        s = _re.sub(r'/static/app(?:\.[0-9a-f]{8})?\.js(\?v=\w+)?', "/static/app." + v + ".js", s)
        html.write_text(s, encoding="utf-8")
    import shutil as _sh
    for _old in list((dist / "static").glob("styles.*.css")) + list((dist / "static").glob("app.*.js")):  # stare wersje z hashem
        if v not in _old.name: _old.unlink()
    _sh.copy2(dist / "static/styles.css", dist / ("static/styles." + v + ".css"))
    _sh.copy2(dist / "static/app.js", dist / ("static/app." + v + ".js"))
    print("cache-bust v=" + v)


if __name__ == "__main__":
    _rc = main()
    _cache_bust()
    raise SystemExit(_rc)
