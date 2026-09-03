from __future__ import annotations

import importlib.util
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("rod_build", ROOT / "build.py")
BUILD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BUILD)


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.images_without_alt: list[str] = []
        self.remote_assets: list[str] = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if tag == "img" and "alt" not in values:
            self.images_without_alt.append(values.get("src", "?"))
        if tag == "script" and values.get("src", "").startswith(("http://", "https://")):
            self.remote_assets.append(values["src"])
        if tag == "link" and values.get("rel") == "stylesheet" and values.get("href", "").startswith(("http://", "https://")):
            self.remote_assets.append(values["href"])


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_dist = BUILD.DIST
        BUILD.DIST = Path(self.temp.name) / "dist"
        BUILD.build()

    def tearDown(self):
        BUILD.DIST = self.old_dist
        self.temp.cleanup()

    def test_expected_outputs(self):
        for relative in ("index.html", "ogloszenia/index.html", "dla-dzialkowcow/index.html", "sitemap.xml", "robots.txt", "static/app.js", "static/styles.css"):
            self.assertTrue((BUILD.DIST / relative).is_file(), relative)

    def test_html_has_metadata_and_accessible_images(self):
        for page in BUILD.DIST.rglob("*.html"):
            text = page.read_text(encoding="utf-8")
            self.assertIn('<meta name="description"', text, page)
            self.assertIn('property="og:title"', text, page)
            self.assertIn('rel="canonical"', text, page)
            parser = AuditParser()
            parser.feed(text)
            self.assertEqual([], parser.images_without_alt, page)

    def test_internal_links_resolve(self):
        for page in BUILD.DIST.rglob("*.html"):
            parser = AuditParser()
            parser.feed(page.read_text(encoding="utf-8"))
            for href in parser.links:
                parsed = urlparse(href)
                if parsed.scheme or href.startswith(("mailto:", "tel:", "#")):
                    continue
                relative = parsed.path.lstrip("/")
                target = BUILD.DIST / relative
                if parsed.path.endswith("/") or not target.suffix:
                    target = target / "index.html"
                self.assertTrue(target.exists(), f"{page}: {href}")

    def test_no_remote_scripts_or_styles(self):
        for page in BUILD.DIST.rglob("*.html"):
            parser = AuditParser()
            parser.feed(page.read_text(encoding="utf-8"))
            self.assertEqual([], parser.remote_assets, page)

    def test_sources_validate(self):
        self.assertEqual([], BUILD.validate_sources())


if __name__ == "__main__":
    unittest.main()
