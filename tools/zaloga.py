#!/usr/bin/env python3
"""zaloga.py — jedno polecenie, cala czworka pracuje rownolegle.

Powstalo 29.07.2026, bo Tomasz musial trzeci raz tego samego dnia przypominac:
"Dlaczego pracujecie we dwojke? Mieliscie pracowac zawsze wszyscy".
Regula byla zapisana w pamieci, w START.md, w AGENTS.md i w podreczniku — i mimo to Klaudek
zrobil pomiar z samym Heniem. Wniosek: regula w dokumencie nie wystarcza. Wolanie calej zalogi
musi byc LATWIEJSZE niz praca solo. To narzedzie robi z tego jedno polecenie.

Uzycie:
    python3 tools/zaloga.py --zadanie /tmp/zadanie.md
    python3 tools/zaloga.py --zadanie /tmp/z.md --material plik1.md,plik2.txt
    python3 tools/zaloga.py --zadanie /tmp/z.md --kto zenek,genek        # gdy ktos juz odpowiedzial
    python3 tools/zaloga.py --zadanie /tmp/z.md --katalog /tmp/narada7   # gdzie zapisac glosy

Kazdy dostaje TO SAMO zadanie i ten sam material. Nikt nie widzi cudzej odpowiedzi przed napisaniem
wlasnej — glosy powstaja niezaleznie, dokladnie tak jak chcial Tomasz.
Material dokladany jest do zlecenia Genka, bo on jako jedyny nie ma dostepu do dysku.

Wynik: pliki <katalog>/<imie>.txt oraz zbiorcze podsumowanie na wyjsciu.
Awaria jednego wykonawcy NIE jest zgoda — w podsumowaniu stoi wtedy "GLOS NIEODEBRANY".
"""
import argparse
import json
import os
import subprocess
import sys
import threading
import urllib.request

REPO = "/root/rod-ai-studio"
STOPKA = ("\n\nPodpisz sie swoim imieniem. Jesli czegos nie da sie ustalic z materialu — napisz NIE WIEM. "
          "Nie uzgadniaj odpowiedzi z nikim, to ma byc TWOJ glos."
          "\n\nTO JEST BADANIE, NIE ZAPIS (dekret Tomasza 30.07: 'Zadanie to zadanie, badanie to badanie. "
          "Decyzje zawsze podejmuje JA'). NIE zmieniaj, nie dopisuj i nie tworz ZADNEGO pliku w repo. "
          "Jesli czegos w pliku NIE MA — napisz 'NIE MA TEGO W PLIKU'. Nie wolno dopisac brakujacej tresci, "
          "a potem zacytowac jej jako dowodu; to sie stalo 30.07 i jest wykrywane automatycznie. "
          "Decyzji nie zapisuje nikt z zalogi — zapisuje je Tomasz przez Klaudka, po swojej decyzji.")


def sprawdz_rowne_szanse() -> tuple:
    """Przed KAZDYM zadaniem: czy cala zaloga ma komplet zdolnosci.
    Powod (Tomasz, 29.07): "Dlaczego ja musze bez przerwy powtarzac, ze wy wszyscy macie miec rowne
    szanse. Jezeli komus cos padlo, to moze naprawiac, jak zaczynacie cokolwiek robic."
    Regula w dokumencie tego nie zalatwila — Klaudek trzy razy ruszyl z zadaniem, majac Zenka bez sieci
    i Genka bez dysku. Teraz sprawdzenie odpala sie SAMO, przed rozeslaniem zadania."""
    sonda = os.path.join(REPO, "tools", "sonda_zdolnosci.py")
    if not os.path.isfile(sonda):
        return True, "brak sondy — nie sprawdzono"
    try:
        w = subprocess.run([sys.executable, sonda], cwd=REPO, capture_output=True, text=True, timeout=600)
    except Exception as e:
        return True, f"sonda nie dokonczyla ({e})"
    if w.returncode == 0:
        return True, "wszyscy maja komplet zdolnosci"
    # 30.07: telefon Tomasza NIE jest zdolnoscia zalogi — to jego urzadzenie, ktore bywa uspione.
    # Bramka blokowala narade nad TEKSTEM, bo Fold byl poza siecia. Peryferium informuje, nie blokuje.
    braki = [l for l in w.stdout.split("\n") if "STRACONE" in l]
    tylko_telefon = braki and all("telefon." in l for l in braki)
    if tylko_telefon:
        return True, ("wszyscy z zalogi maja komplet zdolnosci; niedostepne peryferium: "
                      + "; ".join(l.split("|")[0].strip() for l in braki))
    return False, w.stdout.strip()


def czytaj_material(lista: str) -> str:
    if not lista:
        return ""
    kawalki = []
    for s in [x.strip() for x in lista.split(",") if x.strip()]:
        p = s if os.path.isabs(s) else os.path.join(REPO, s)
        if os.path.isfile(p):
            with open(p, encoding="utf-8", errors="replace") as f:
                kawalki.append(f"--- {s} ---\n{f.read()[:25000]}")
        else:
            kawalki.append(f"--- {s} --- PLIK NIE ISTNIEJE")
    return "\n\n".join(kawalki)


def zenek(zadanie: str, _material: str, wynik: dict) -> None:
    try:
        w = subprocess.run(["codex", "exec", zadanie + STOPKA], cwd=REPO,
                           capture_output=True, text=True, timeout=600)
        out = w.stdout
        # 30.07: obcinanie do 3000 znakow ucielo Zenkowi punkty 1-5 w debacie o wygladzie Izabeli —
        # zostala sama koncowka, zaczynajaca sie w polowie zdania. Limit podniesiony i liczony od KONCA
        # ostatniej wypowiedzi, a nie od konca calego logu.
        czesci = out.split("\ncodex\n")
        tresc = czesci[-1].strip() if len(czesci) > 1 else out
        # odetnij stopke licznika tokenow, jesli jest
        for znacznik in ("\ntokens used", "\nTokens used"):
            if znacznik in tresc:
                tresc = tresc.split(znacznik)[0].strip()
        wynik["zenek"] = tresc[-24000:] if len(tresc) > 24000 else tresc
    except Exception as e:
        wynik["zenek"] = f"GLOS NIEODEBRANY ({e})"


def genek(zadanie: str, material: str, wynik: dict) -> None:
    """Genek przez tools/genek.py — ma WLASNY dostep do dysku (CLI), material tylko na wypadek awarii."""
    sciezka = "/tmp/_zaloga_zadanie_genek.txt"
    try:
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write(zadanie + STOPKA)
        polecenie = [sys.executable, os.path.join(REPO, "tools", "genek.py"), "--plik", sciezka, "--limit", "260"]
        if material:
            mat = "/tmp/_zaloga_material_genek.txt"
            with open(mat, "w", encoding="utf-8") as f:
                f.write(material)
            polecenie += ["--material", mat]
        w = subprocess.run(polecenie, cwd=REPO, capture_output=True, text=True, timeout=900)
        tresc = (w.stdout or w.stderr).strip()
        # 29.07: bramka sprawdza zdolnosci PRZED startem, ale CLI Genka moze paść w TRAKCIE (limit czasu).
        # Wtedy leci tryb awaryjny — bez dysku, czyli NIEROWNE SZANSE. Tomasz to wylapal.
        # Jedna proba ponowna z dluzszym limitem; jesli dalej awaryjnie — to NIE jest rownowazny glos.
        if "TRYB AWARYJNY" in tresc.upper():
            polecenie_dl = [x if x != "260" else "600" for x in polecenie]
            try:
                w2 = subprocess.run(polecenie_dl, cwd=REPO, capture_output=True, text=True, timeout=1200)
                tresc2 = (w2.stdout or w2.stderr).strip()
                if tresc2 and "TRYB AWARYJNY" not in tresc2.upper():
                    tresc = tresc2
                else:
                    tresc = ("GLOS NIEODEBRANY (dwukrotnie tryb awaryjny — Genek nie mial dostepu do dysku, "
                             "czyli NIE mial rownych szans; ponizej jego odpowiedz bez dostepu, do wgladu)\n\n" + tresc2 or tresc)
            except Exception as e:
                tresc = f"GLOS NIEODEBRANY (ponowna proba padla: {e})\n\n{tresc}"
        wynik["genek"] = tresc or "GLOS NIEODEBRANY (pusta odpowiedz)"
    except Exception as e:
        wynik["genek"] = f"GLOS NIEODEBRANY ({e})"


def henio(zadanie: str, _material: str, wynik: dict) -> None:
    sciezka = "/tmp/_zaloga_zadanie_henio.txt"
    try:
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write(zadanie + STOPKA)
        os.chmod(sciezka, 0o644)
        w = subprocess.run(
            ["su", "-", "hermes", "-c", f'hermes -z "$(cat {sciezka})"'],
            capture_output=True, text=True, timeout=600)
        wynik["henio"] = (w.stdout or w.stderr).strip() or "GLOS NIEODEBRANY (pusta odpowiedz)"
    except Exception as e:
        wynik["henio"] = f"GLOS NIEODEBRANY ({e})"


WYKONAWCY = {"zenek": zenek, "genek": genek, "henio": henio}


def zapisz_glos(katalog: str, imie: str, tresc: str) -> None:
    """Zapisz glos NATYCHMIAST po odebraniu, nie na koncu narady.
    Powod (Tomasz, 30.07): 'Zawsze na biezaco podawaj, kto co wymysli'.
    Tego samego dnia narada o wygladzie Izabeli zostala UCIETA przez limit czasu po 28 minutach —
    Zenek i Henio dawno odpowiedzieli, ale ich glosy siedzialy w pamieci procesu i przepadly razem
    z nim. Zero na dysku po polgodzinie pracy. Od teraz kazdy glos ladu je na dysku od razu."""
    os.makedirs(katalog, exist_ok=True)
    with open(os.path.join(katalog, f"{imie}.txt"), "w", encoding="utf-8") as f:
        f.write(tresc)
    print(f"[glos zapisany] {imie}.txt ({len(tresc)} znakow) -> {katalog}/", flush=True)


def wspolna_wiedza() -> str:
    """RÓWNE SZANSE W WIEDZY (dekret Tomasza 01.08.2026).

    Bramka rownych szans pilnowala ZDOLNOSCI (dysk, siec, oczy), ale NIKT nie pilnowal WIEDZY.
    Skutek: 01.08 okazalo sie, ze zaloga nie wiedziala o generowaniu obrazu przez Genka, mimo ze
    kanon lezal na dysku od godziny. Tomasz: "To jest najwazniejsze, zeby grupa dzialala
    na rownych szansach".
    Od teraz KAZDY brief dostaje ten sam zestaw: spis wiedzy + najswiezsze decyzje.
    Nikt nie zaczyna zadania slepy.
    """
    czesci = ["=== CO KAZDY Z ZALOGI MA WIEDZIEC (dolaczane automatycznie) ==="]

    # 1) spis plikow wiedzy z pierwsza linia opisu — zeby wiedzieli, CO istnieje i gdzie zajrzec
    kat = os.path.join(REPO, "wiedza")
    if os.path.isdir(kat):
        czesci.append("\nDOSTEPNA WIEDZA (otworz plik, jesli zadanie tego dotyczy):")
        for nazwa in sorted(os.listdir(kat)):
            if not nazwa.endswith(".md"):
                continue
            try:
                with open(os.path.join(kat, nazwa), encoding="utf-8") as f:
                    naglowek = ""
                    for linia in f:
                        linia = linia.strip()
                        if linia and not linia.startswith("#"):
                            naglowek = linia[:110]
                            break
                czesci.append(f"  wiedza/{nazwa} — {naglowek}")
            except OSError:
                czesci.append(f"  wiedza/{nazwa}")

    # 2) najswiezsze decyzje Tomasza — jego slowo przebija kazdy dokument
    czesci.append("\nNAJSWIEZSZE DECYZJE TOMASZA (jego slowo przebija KAZDY dokument):")
    for plik in ("wiedza/DECYZJE_SERIA_HUMOR.md", "wiedza/GENEROWANIE_OBRAZU.md"):
        sc = os.path.join(REPO, plik)
        if os.path.isfile(sc):
            try:
                with open(sc, encoding="utf-8") as f:
                    ogon = [l.rstrip() for l in f.readlines() if l.strip()][-6:]
                czesci.append(f"  --- {plik} (ogon) ---")
                czesci.extend("    " + l[:150] for l in ogon)
            except OSError:
                pass

    # TECZKI — dekret Tomasza 01.08: "Kazdy z grupy ma wglad do teczek innych i tym samym
    # nie walczyc, a pomagac innym." Teczki ida do KAZDEGO briefu, zeby kazdy znal slabe strony
    # kolegow ZANIM zaczna wspolna prace — i mogl je wylapac, zamiast czekac na wpadke.
    kat_t = os.path.join(REPO, "wiedza", "TECZKI")
    if os.path.isdir(kat_t):
        czesci.append("\nTECZKI ZALOGI — czytaj PRZED wspolna praca (sa po to, zeby POMAGAC, nie walczyc):")
        for nazwa in sorted(os.listdir(kat_t)):
            if nazwa.endswith(".md"):
                czesci.append(f"  wiedza/TECZKI/{nazwa}")
        czesci.append("  Wykryty blad dopisujesz NATYCHMIAST — takze wlasny. Kto ukrywa, dostaje drugi wpis.")
        czesci.append("  Nad grupa jest TOMASZ. On ma byc PIERWSZY, ktory wie, co sie dzieje.")

    czesci.append("\nJesli czegos nie ma w tym zestawie, a jest potrzebne — OTWORZ PLIK SAM.")
    czesci.append("=== koniec wspolnej wiedzy ===\n")
    return "\n".join(czesci)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--zadanie", required=True, help="plik z trescia zadania")
    p.add_argument("--material", default="", help="pliki zrodlowe po przecinku (trafiaja do Genka)")
    p.add_argument("--kto", default="zenek,genek,henio")
    p.add_argument("--katalog", default="/tmp/narada")
    p.add_argument("--mimo-braku", action="store_true",
                   help="rusz mimo nierownych szans (swiadoma decyzja, wypisana w meldunku)")
    a = p.parse_args()

    if not os.path.isfile(a.zadanie):
        print(f"BLAD: brak pliku zadania {a.zadanie}")
        return 2
    with open(a.zadanie, encoding="utf-8", errors="replace") as f:
        zadanie = f.read()
    if not zadanie.strip():
        print("BLAD: zadanie jest puste")
        return 2

    # RÓWNE SZANSE W WIEDZY — dekret Tomasza 01.08.2026.
    # Każdy dostaje ten sam zestaw wiedzy razem z zadaniem. Nikt nie zaczyna ślepy.
    zadanie = zadanie + "\n\n" + wspolna_wiedza()

    rowno, opis_sondy = sprawdz_rowne_szanse()
    if not rowno:
        print("=" * 70)
        print("STOP — ZALOGA NIE MA ROWNYCH SZANS. Zadanie NIE zostalo rozeslane.")
        print("=" * 70)
        print(opis_sondy)
        print()
        print("Napraw brak i uruchom ponownie, albo swiadomie dodaj --mimo-braku")
        print("(wtedy brak zostanie wypisany w meldunku, nie zniknie po cichu).")
        if not a.mimo_braku:
            return 2
        print(">>> RUSZAM MIMO BRAKU na wyrazne polecenie. Powyzszy brak obowiazuje w meldunku. <<<")
    else:
        print(f"[rowne szanse] {opis_sondy}\n")

    material = czytaj_material(a.material)
    os.makedirs(a.katalog, exist_ok=True)
    kto = [x.strip() for x in a.kto.split(",") if x.strip() in WYKONAWCY]
    if not kto:
        print("BLAD: nikt do wywolania")
        return 2

    odcisk = "/tmp/_zaloga_odcisk.json"
    subprocess.run([sys.executable, os.path.join(REPO, "tools", "straznik_zrodel.py"),
                    "--zapisz", odcisk, "wiedza", "tools", "AGENTS.md", "CLAUDE.md"],
                   cwd=REPO, capture_output=True, text=True, timeout=180)
    print(f"NARADA: {', '.join(kto)} — kazdy dostaje to samo, nikt nie widzi cudzej odpowiedzi.")
    print("[straznik zrodel] odcisk plikow wziety — badanie nie moze wytworzyc wlasnego dowodu\n")
    wynik: dict = {}

    def _uruchom(imie: str) -> None:
        """Wykonaj i ZAPISZ NATYCHMIAST — nie czekaj na pozostalych."""
        try:
            WYKONAWCY[imie](zadanie, material, wynik)
        finally:
            zapisz_glos(a.katalog, imie, wynik.get(imie, "GLOS NIEODEBRANY (brak wyniku)"))

    watki = [threading.Thread(target=_uruchom, args=(k,)) for k in kto]
    for w in watki:
        w.start()
    for w in watki:
        w.join()

    nieodebrane = 0
    for k in kto:
        tresc = wynik.get(k, "GLOS NIEODEBRANY (brak wyniku)")
        if tresc.startswith("GLOS NIEODEBRANY"):
            nieodebrane += 1
        print("=" * 25, k.upper(), "=" * 25)
        print(tresc, "\n")

    w = subprocess.run([sys.executable, os.path.join(REPO, "tools", "straznik_zrodel.py"),
                        "--porownaj", odcisk], cwd=REPO, capture_output=True, text=True, timeout=180)
    if w.returncode != 0:
        print(w.stdout)
        print("!!! UWAGA: ktos z zalogi RUSZYL PLIKI w trakcie badania. Cytaty z tych plikow sa podejrzane.")
    else:
        print("[straznik zrodel] zrodla nietkniete — cytaty pochodza ze stanu sprzed zadania")

    print(f"GLOSY: {len(kto) - nieodebrane}/{len(kto)} odebrane. Zapisane w {a.katalog}/")
    if nieodebrane:
        print("UWAGA: brak glosu NIE jest zgoda. Wniosek bez pelnego skladu jest niepelny.")
    print("Klaudek dokłada swoj wlasny glos osobno — jest w druzynie, nie nad nia.")
    print("UWAGA: straznik zrodel obejmuje TAKZE prace Klaudka — odcisk brany przed narada i porownany")
    print("po niej obejmuje KAZDA zmiane w wiedza/, tools/, AGENTS.md i CLAUDE.md, niezaleznie od tego,")
    print("kto ja zrobil (luke wskazal Zenek 30.07: 'straznikiem objeci tylko wywolani wykonawcy').")
    return 0


if __name__ == "__main__":
    sys.exit(main())
