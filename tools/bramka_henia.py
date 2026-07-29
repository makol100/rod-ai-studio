#!/usr/bin/env python3
"""bramka_henia.py — mechaniczna bramka dowodowa na odpowiedzi dyzurnego.

Powstala 29.07.2026 na wniosek CALEJ czworki (Klaudek, Zenek, Genek, Henio — zbieznie):
"nie kolejny apel w podreczniku, lecz automatyczna bramka dowodowa".

Zasada: bramka NIE OCENIA sensu. Sprawdza mechanicznie, czy to, co odpowiedz PRZYPISUJE ZRODLU,
faktycznie w tym zrodle wystepuje. Zero modelu, zero opinii — grep i liczby.

Uzycie:
    python3 tools/bramka_henia.py --odpowiedz /tmp/henio_out.txt --zrodlo plik1.txt,plik2.md
    python3 tools/bramka_henia.py --odpowiedz /tmp/o.txt --zrodlo dane.txt --prog 0

Co sprawdza:
1. CYTATY — kazdy fragment w cudzyslowie ("..." albo „...") musi wystapic w zrodle.
2. NAZWY WLASNE — slowa CamelCase / z cyframi w srodku / ALLCAPS (typowe nazwy repo, produktow,
   plikow, modeli) musza wystapic w zrodle.
3. LICZBY z jednostka lub procentem — musza wystapic w zrodle.

Werdykt:
    PRZEPUSCIC — wszystko, co przypisano zrodlu, w zrodle jest.
    BLOKADA    — cokolwiek przypisanego zrodlu w nim NIE wystepuje (exit 2).

Fail-closed: brak zrodla, puste zrodlo albo pusta odpowiedz = BLOKADA.
"""
import argparse
import os
import re
import sys
import unicodedata

# slowa, ktore wygladaja jak nazwa wlasna, ale sa polskim/angielskim slowem zwyklym
POMIJANE = {
    "NIE", "WIEM", "TAK", "OK", "URL", "API", "ID", "MB", "GB", "KB", "TB", "CPU", "RAM",
    "PDF", "JSON", "YAML", "HTML", "HTTP", "HTTPS", "SSH", "VPS", "AI", "TTS", "PL", "EN",
    "POTWIERDZONE", "HIPOTEZA", "HIPOTEZY", "SLAD", "ŚLAD", "DOWOD", "DOWÓD", "BRAK",
    "UWAGA", "WERDYKT", "WNIOSEK", "KROK", "PUNKT", "TEST", "STAN", "LICZBY",
}


def plaski(s: str) -> str:
    s = s.replace("ł", "l").replace("Ł", "L")
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()


def wczytaj_zrodla(lista: str) -> tuple:
    tresci, braki = [], []
    for sciezka in [s.strip() for s in lista.split(",") if s.strip()]:
        if os.path.isfile(sciezka):
            with open(sciezka, encoding="utf-8", errors="replace") as f:
                tresci.append(f.read())
        else:
            braki.append(sciezka)
    return "\n".join(tresci), braki


NEGACJE = ("0 razy", "0 wystapien", "0 wystąpień", "zero razy", "nie ma w", "nie wystepuje",
           "nie występuje", "brak w zrodle", "brak w źródle", "nie znalaz", "0 trafien", "0 trafień")


def zgloszona_jako_nieobecna(token: str, odpowiedz: str) -> bool:
    """Token, o ktorym odpowiedz WPROST mowi ze go nie ma, nie jest twierdzeniem o zrodle."""
    for linia in odpowiedz.split("\n"):
        if token in linia and any(n in plaski(linia) for n in [plaski(x) for x in NEGACJE]):
            return True
    return False


SCIEZKA_LUB_POLECENIE = re.compile(
    r"^-|/|\.(md|py|txt|json|yaml|yml|sh|jpg|png|mp4|log)$|^(grep|ls|cat|wc|sed|awk|python3?|curl|git|tail|head|find|chmod|sudo|docker)$",
    re.IGNORECASE)


def z_zadania(element: str, zadanie_plaskie: str) -> bool:
    """Cytat albo nazwa, ktora pochodzi z TRESCI ZADANIA, nie jest twierdzeniem o zrodle."""
    return bool(zadanie_plaskie) and plaski(element) in zadanie_plaskie


def wyciagnij(odpowiedz: str) -> dict:
    cytaty = re.findall(r'"([^"\n]{8,120})"', odpowiedz)
    cytaty += re.findall(r'„([^"\n]{8,120})"', odpowiedz)
    cytaty += re.findall(r'\*\*"([^"\n]{8,120})"\*\*', odpowiedz)

    nazwy = set()
    for token in re.findall(r"\b[A-Za-z][A-Za-z0-9\-_.]{2,}\b", odpowiedz):
        if token.upper() in POMIJANE:
            continue
        camel = re.search(r"[a-z][A-Z]", token)
        zcyfra = re.search(r"[A-Za-z]\d|\d[A-Za-z]", token)
        allcaps = token.isupper() and len(token) > 3 and any(c.isdigit() for c in token)
        myslnik = "-" in token and any(c.isupper() for c in token)
        if SCIEZKA_LUB_POLECENIE.search(token):
            continue
        if camel or zcyfra or allcaps or myslnik:
            if not zgloszona_jako_nieobecna(token, odpowiedz):
                nazwy.add(token)

    liczby = set(re.findall(r"\b\d[\d\s.,]{0,12}\s?(?:%|MB|GB|KB|s|ms|USD|zl|zł)\b", odpowiedz))
    return {"cytaty": [c.strip() for c in cytaty], "nazwy": sorted(nazwy), "liczby": sorted(liczby)}


WZORZEC_TECHNICZNY = re.compile(r"^[\w./\-]+\.(md|py|txt|json|yaml|yml|sh|jpg|png|mp4|log)$|^[\(\[].*[|].*[\)\]]$|^-{1,2}\w")


def techniczny(element: str) -> bool:
    """Sciezka pliku, flaga polecenia albo wzorzec wyszukiwania — to narzedzie, nie cytat ze zrodla."""
    e = element.strip().strip("`\"'")
    return bool(WZORZEC_TECHNICZNY.match(e))


def sprawdz(element: str, zrodlo_plaskie: str) -> bool:
    return plaski(element) in zrodlo_plaskie


def sprawdz_sume(odpowiedz: str) -> list:
    """Sprawdza arytmetyke TYLKO w tabeli markdown: wiersze skladnikow vs wiersz SUMA.
    Powod (29.07): Henio poprawnie wyciagnal 7 pozycji strat, ale zsumowal je zle
    (zadeklarowal 18.76 przy skladnikach dajacych 21.26). Pierwsza wersja tego sprawdzenia
    liczyla wszystkie kwoty w dokumencie (takze te w cytatach) i dawala bzdury — zawezona do tabeli."""
    problemy = []
    skladniki, sumy = [], []
    for linia in odpowiedz.split("\n"):
        if not linia.strip().startswith("|"):
            continue
        kwoty = [float(x.replace(",", ".")) for x in re.findall(r"\$\s?(\d+[.,]\d{2})\b", linia)]
        if not kwoty:
            continue
        czy_suma = re.search(r"\b(SUMA|RAZEM|LACZNIE|ŁĄCZNIE)\b", linia, re.IGNORECASE)
        czy_pominac = "*" in linia and not czy_suma
        if czy_suma:
            sumy.extend(kwoty)
        elif not czy_pominac:
            skladniki.extend(kwoty)
    if not sumy or len(skladniki) < 2:
        return problemy
    razem = round(sum(skladniki), 2)
    for deklarowana in sorted(set(sumy)):
        if abs(deklarowana - razem) > 0.02:
            problemy.append(
                f"SUMA W TABELI SIE NIE ZGADZA: zadeklarowano {deklarowana:.2f}, "
                f"{len(skladniki)} skladnikow daje {razem:.2f} (roznica {abs(deklarowana - razem):.2f})")
    return problemy


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--odpowiedz", required=True)
    p.add_argument("--zrodlo", required=True, help="pliki zrodlowe po przecinku")
    p.add_argument("--prog", type=int, default=0, help="ile brakow wolno przepuscic (domyslnie 0)")
    p.add_argument("--zadanie", default="", help="plik z trescia zadania — cytaty z niego nie sa twierdzeniami o zrodle")
    a = p.parse_args()

    if not os.path.isfile(a.odpowiedz):
        print(f"BLOKADA: brak pliku z odpowiedzia ({a.odpowiedz})")
        return 2
    with open(a.odpowiedz, encoding="utf-8", errors="replace") as f:
        odpowiedz = f.read()
    if not odpowiedz.strip():
        print("BLOKADA: odpowiedz jest pusta")
        return 2

    zrodlo, braki_plikow = wczytaj_zrodla(a.zrodlo)
    if braki_plikow:
        print(f"BLOKADA: nie ma plikow zrodlowych: {', '.join(braki_plikow)}")
        return 2
    if not zrodlo.strip():
        print("BLOKADA: zrodlo jest puste — nie ma czego porownac")
        return 2

    zp = plaski(zrodlo)
    zadanie_plaskie = ""
    if a.zadanie and os.path.isfile(a.zadanie):
        with open(a.zadanie, encoding="utf-8", errors="replace") as f:
            zadanie_plaskie = plaski(f.read())
    el = wyciagnij(odpowiedz)
    pominiete = {"z zadania": [], "techniczne": []}
    for rodzaj in ("cytaty", "nazwy", "liczby"):
        zostaje = []
        for e in el[rodzaj]:
            if techniczny(e):
                pominiete["techniczne"].append(e)
            elif z_zadania(e, zadanie_plaskie):
                pominiete["z zadania"].append(e)
            else:
                zostaje.append(e)
        el[rodzaj] = zostaje
    braki = {"cytaty": [], "nazwy": [], "liczby": []}
    ile = {"cytaty": 0, "nazwy": 0, "liczby": 0}

    for rodzaj in ("cytaty", "nazwy", "liczby"):
        for e in el[rodzaj]:
            ile[rodzaj] += 1
            if not sprawdz(e, zp):
                braki[rodzaj].append(e)

    print(f"ODPOWIEDZ: {a.odpowiedz} ({len(odpowiedz)} znakow)")
    print(f"ZRODLO:    {a.zrodlo} ({len(zrodlo)} znakow)\n")
    for rodzaj, etykieta in (("cytaty", "CYTATY"), ("nazwy", "NAZWY WLASNE"), ("liczby", "LICZBY")):
        sprawdzone = ile[rodzaj]
        zle = braki[rodzaj]
        print(f"{etykieta}: sprawdzono {sprawdzone}, BRAK W ZRODLE: {len(zle)}")
        for e in zle[:15]:
            print(f"    !!! NIE MA W ZRODLE: {e}")
        if len(zle) > 15:
            print(f"    ... i jeszcze {len(zle) - 15}")

    problemy_sumy = sprawdz_sume(odpowiedz)
    if problemy_sumy:
        print("ARYTMETYKA:")
        for x in problemy_sumy:
            print(f"    !!! {x}")
    else:
        print("ARYTMETYKA: sumy zgodne albo brak sumy do sprawdzenia")

    ile_pominietych = sum(len(v) for v in pominiete.values())
    if ile_pominietych:
        print(f"\nPOMINIETE PRZY SPRAWDZANIU ({ile_pominietych}) — NIE zweryfikowane, obejrzyj sam:")
        for powod, lista in pominiete.items():
            for e in lista[:8]:
                print(f"    ~ [{powod}] {e[:90]}")
            if len(lista) > 8:
                print(f"    ~ [{powod}] ... i jeszcze {len(lista) - 8}")

    razem = sum(len(v) for v in braki.values()) + len(problemy_sumy)
    print()
    if razem > a.prog:
        print(f"WERDYKT: BLOKADA — {razem} rzeczy przypisanych zrodlu, ktorych w nim NIE MA.")
        print("Odpowiedz NIE IDZIE dalej. Popraw albo napisz NIE WIEM.")
        return 2
    print("WERDYKT: PRZEPUSCIC — wszystko, co przypisano zrodlu, w zrodle wystepuje.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
