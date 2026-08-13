#!/usr/bin/env python3
"""Test dostepu do kamer i nagrywarki HiLook — DRUKUJE WYLACZNIE KODY HTTP.

Poswiadczenia czytane z /root/.sekrety/wartosci.env i /root/.hilook_cred.
Wartosci nie sa nigdzie wypisywane ani przekazywane w linii polecen.
"""

from __future__ import annotations

import base64
import hashlib
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ZRODLA = ("/root/.sekrety/wartosci.env", "/root/.hilook_cred")
ADRESY = ["192.168.3.110", "192.168.3.111", "192.168.3.112", "192.168.3.113", "192.168.3.114"]
SCIEZKA = "/ISAPI/System/deviceInfo"


def poswiadczenia() -> list[tuple[str, str, str]]:
    """Zwraca [(zrodlo, user, haslo)] — bez drukowania czegokolwiek."""
    wynik = []
    for zr in ZRODLA:
        dane = {}
        try:
            for l in Path(zr).read_text(encoding="utf-8").splitlines():
                l = l.strip()
                if l and not l.startswith("#") and "=" in l:
                    k, _, v = l.partition("=")
                    dane[k.strip().upper()] = v.strip().strip('"').strip("'")
        except OSError:
            continue
        u = dane.get("HILOOK_USER") or dane.get("KAMERY_USER") or dane.get("KAMERY_ROD_USER")
        h = dane.get("HILOOK_PASS") or dane.get("KAMERY_PASS") or dane.get("KAMERY_ROD_PASS")
        if u and h:
            wynik.append((Path(zr).name, u, h))
    return wynik


def digest_naglowek(wyzwanie: str, user: str, haslo: str, metoda: str, uri: str) -> str:
    pola = dict(re.findall(r'(\w+)="([^"]*)"', wyzwanie))
    realm, nonce = pola.get("realm", ""), pola.get("nonce", "")
    qop, opaque = pola.get("qop", ""), pola.get("opaque")
    ha1 = hashlib.md5(f"{user}:{realm}:{haslo}".encode()).hexdigest()
    ha2 = hashlib.md5(f"{metoda}:{uri}".encode()).hexdigest()
    if qop:
        nc, cnonce = "00000001", "abcdef0123456789"
        odp = hashlib.md5(f"{ha1}:{nonce}:{nc}:{cnonce}:auth:{ha2}".encode()).hexdigest()
        naglowek = (f'Digest username="{user}", realm="{realm}", nonce="{nonce}", uri="{uri}", '
                    f'qop=auth, nc={nc}, cnonce="{cnonce}", response="{odp}"')
    else:
        odp = hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode()).hexdigest()
        naglowek = (f'Digest username="{user}", realm="{realm}", nonce="{nonce}", '
                    f'uri="{uri}", response="{odp}"')
    if opaque:
        naglowek += f', opaque="{opaque}"'
    return naglowek


def sprobuj(adres: str, user: str, haslo: str) -> str:
    url = f"http://{adres}{SCIEZKA}"
    # 1. basic
    zad = urllib.request.Request(url)
    zad.add_header("Authorization",
                   "Basic " + base64.b64encode(f"{user}:{haslo}".encode()).decode())
    try:
        with urllib.request.urlopen(zad, timeout=8) as o:
            return f"HTTP {o.status} (basic) — DZIALA"
    except urllib.error.HTTPError as e:
        if e.code != 401:
            return f"HTTP {e.code} (basic)"
        wyzwanie = e.headers.get("WWW-Authenticate", "")
    except Exception as e:  # noqa: BLE001
        return f"brak polaczenia ({type(e).__name__})"

    if "digest" not in wyzwanie.lower():
        return "HTTP 401 (basic, brak digest w wyzwaniu)"

    zad2 = urllib.request.Request(url)
    zad2.add_header("Authorization", digest_naglowek(wyzwanie, user, haslo, "GET", SCIEZKA))
    try:
        with urllib.request.urlopen(zad2, timeout=8) as o:
            return f"HTTP {o.status} (digest) — DZIALA"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code} (digest)"
    except Exception as e:  # noqa: BLE001
        return f"brak polaczenia ({type(e).__name__})"


def main() -> int:
    zestawy = poswiadczenia()
    if not zestawy:
        print("BRAK POSWIADCZEN w skrytce.")
        return 1
    print(f"zestawow poswiadczen: {len(zestawy)}")
    dziala = False
    for zrodlo, u, h in zestawy:
        print(f"\n--- poswiadczenia z {zrodlo} (uzytkownik {len(u)} zn., haslo {len(h)} zn.)")
        for adres in ADRESY:
            wynik = sprobuj(adres, u, h)
            print(f"  {adres:16} {wynik}")
            if "DZIALA" in wynik:
                dziala = True
    return 0 if dziala else 2


if __name__ == "__main__":
    raise SystemExit(main())
