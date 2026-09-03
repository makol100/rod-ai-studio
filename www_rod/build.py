#!/usr/bin/env python3
"""Dependency-free builder for the static ROD website."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
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
    escaped = re.sub(r"\[([^]]+)]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', escaped)
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

    for raw_line in text.splitlines():
        line = raw_line.strip()
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
        '<a class="button" href="/ogloszenia/">Szczegóły</a>'
    )


def announcements_page(items: list[dict]) -> str:
    cards = []
    for item in sorted(items, key=lambda row: row["date"], reverse=True):
        cards.append(
            '<li class="announcement-item">'
            f'<time datetime="{html.escape(item["date"])}">{html.escape(item["display_date"])}</time>'
            f'<h2>{html.escape(item["title"])}</h2>'
            f'<p><strong>{html.escape(item["place"])}</strong></p>'
            f'<p>{html.escape(item["body"])}</p></li>'
        )
    return '<header class="page-hero shell"><p class="eyebrow">Bądź na bieżąco</p><h1>Ogłoszenia</h1></header><section class="page-content"><ul class="announcement-list">' + "".join(cards) + "</ul></section>"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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
    shutil.copy2(ROOT.parent / "data/rolka-prad/do-rolki/00-MAPA-OGRODU.jpg", image_dest / "mapa-ogrodu.jpg")
    shutil.copy2(ROOT.parent / "data/rolka-prad/do-rolki/ZK-z-tablica-ROD.jpg", image_dest / "elektryfikacja.jpg")
    shutil.copy2(ROOT / "static/img/jozef_lompa.jpg", image_dest / "jozef_lompa.jpg")

    layout = (ROOT / "templates/page.html").read_text(encoding="utf-8")
    home = (ROOT / "templates/home.html").read_text(encoding="utf-8")
    featured = next((item for item in announcements if item.get("featured")), announcements[0])
    home_body = render(home, {"featured_announcement": announcement_html(featured)})
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
            content=page_content(meta["title"], markdown(body)),
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


if __name__ == "__main__":
    raise SystemExit(main())
