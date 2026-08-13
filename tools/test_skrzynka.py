#!/usr/bin/env python3
"""Petla testowa skrzynki na Telegramie (13.08).

Kazdy przypadek pochodzi z realnej wpadki albo z realnego wymagania Tomasza:
 T1  sekret zapisuje sie do pliku POZA repozytorium
 T2  ten sam klucz jest PODMIENIANY, nie dublowany
 T3  odpowiedz bota NIGDY nie zawiera wartosci sekretu
 T4  lista sekretow pokazuje SAME NAZWY
 T5  bledne uzycie /sekret jest odrzucane
 T6  filtr przepuszcza zaslepki <...> i [...] (falszywy alarm z 10:15)
 T7  filtr odrzuca prawdziwe przypisanie hasla i naglowek Authorization
 T8  filtr czyta KATALOG sekretow (IsADirectoryError ginelo cicho w except OSError)
 T9  filtr odrzuca tekst zawierajacy realna wartosc z pliku sekretow
Uruchomienie: python3 tools/test_skrzynka.py   (kod 0 = zielono)
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

KATALOG = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KATALOG)

import filtr_sekretow as fs  # noqa: E402
import hans_ucho as hu  # noqa: E402

bledy: list[str] = []


def sprawdz(nazwa: str, warunek: bool, szczegol: str = "") -> None:
    if warunek:
        print(f"  ZIELONY  {nazwa}")
    else:
        print(f"  CZERWONY {nazwa} {szczegol}")
        bledy.append(nazwa)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # --- sekrety: zapis, podmiana, brak wycieku wartosci ---
        hu.PLIK_SEKRETOW = tmp / "wartosci.env"
        WARTOSC = "tajna_wartosc_do_testu_1"
        ok, komunikat = hu._zapisz_sekret(f"KAMERA_ROD={WARTOSC}")
        tresc = hu.PLIK_SEKRETOW.read_text(encoding="utf-8")
        sprawdz("T1 sekret zapisany do pliku", ok and f"KAMERA_ROD={WARTOSC}" in tresc)
        sprawdz("T1b plik ma prawa 600", oct(hu.PLIK_SEKRETOW.stat().st_mode)[-3:] == "600",
                oct(hu.PLIK_SEKRETOW.stat().st_mode)[-3:])
        sprawdz("T3 odpowiedz bez wartosci", WARTOSC not in komunikat, komunikat)

        hu._zapisz_sekret("KAMERA_ROD=inna_wartosc_2")
        tresc = hu.PLIK_SEKRETOW.read_text(encoding="utf-8")
        sprawdz("T2 klucz podmieniony, nie zdublowany",
                tresc.count("KAMERA_ROD=") == 1 and WARTOSC not in tresc)

        hu.PLIKI_SEKRETOW_TEST = None  # znacznik, ze nie ruszamy prawdziwych plikow
        lista = hu._lista_sekretow()
        sprawdz("T4 lista bez wartosci",
                "inna_wartosc_2" not in lista and WARTOSC not in lista)

        ok2, _ = hu._zapisz_sekret("bezrownosci")
        sprawdz("T5 bledne uzycie odrzucone", ok2 is False)

        # --- filtr: zaslepki kontra prawdziwe sekrety ---
        sprawdz("T6 zaslepka <wartosc> przepuszczona",
                fs.czysto("opis testu: haslo: <wartosc> i token = [twoj_token]"))
        sprawdz("T7a prawdziwe haslo odrzucone",
                not fs.czysto("haslo: Zaq12wsx!Xyz"))
        sprawdz("T7b naglowek Authorization odrzucony",
                not fs.czysto("Authorization: Bearer abcdefgh12345678"))
        sprawdz("T7c zwykle zdanie o hasle przepuszczone",
                fs.czysto("Haslo MQTT lezy jawnym tekstem w publicznym repo — to opis usterki."))

        # --- filtr: katalog sekretow (blad z 13.08) ---
        katalog = tmp / "sekrety_katalog"
        katalog.mkdir()
        (katalog / "README").write_text("# instrukcja, zero wartosci\n", encoding="utf-8")
        (katalog / "kamery").write_text("SuperTajneHaslo987\n", encoding="utf-8")
        stare = fs.PLIKI_SEKRETOW
        fs.PLIKI_SEKRETOW = (str(katalog),)
        try:
            wartosci = fs._wartosci_znane()
            sprawdz("T8 filtr wchodzi do katalogu sekretow",
                    "SuperTajneHaslo987" in wartosci, f"wczytano {len(wartosci)}")
            sprawdz("T9 tekst z realna wartoscia odrzucony",
                    not fs.czysto("gdzies w tekscie SuperTajneHaslo987 poszlo w swiat"))
        finally:
            fs.PLIKI_SEKRETOW = stare

        # --- T10/T11: kasowanie wiadomosci z sekretem MUSI byc sprawdzane (uwaga Zenka) ---
        oryginal = hu._skasuj_wiadomosc
        try:
            hu._skasuj_wiadomosc = lambda *a, **k: True
            udane = hu._obsluz_sekret("NVR_ROD=jakas_wartosc_9", "token", "1", 55)
            sprawdz("T10 udane kasowanie zameldowane", "skasowana z czatu" in udane, udane)
            sprawdz("T10b bez wartosci w odpowiedzi", "jakas_wartosc_9" not in udane)

            hu._skasuj_wiadomosc = lambda *a, **k: False
            nieudane = hu._obsluz_sekret("NVR_ROD=jakas_wartosc_9", "token", "1", 55)
            sprawdz("T11 NIEUDANE kasowanie ostrzega Tomasza",
                    "NIE UDALO SIE" in nieudane and "RECZNIE" in nieudane, nieudane)
            sprawdz("T11b bez wartosci w ostrzezeniu", "jakas_wartosc_9" not in nieudane)

            brak_id = hu._obsluz_sekret("NVR_ROD=jakas_wartosc_9", "token", "1", None)
            sprawdz("T12 brak numeru wiadomosci tez ostrzega", "RECZNIE" in brak_id, brak_id)
        finally:
            hu._skasuj_wiadomosc = oryginal

    # --- T17-T19: braki wskazane przez Zenka w bramce 13.08 ---
    with tempfile.TemporaryDirectory() as tmp2:
        tmp2 = Path(tmp2)
        hu.PLIK_SEKRETOW = tmp2 / "wartosci.env"
        odpowiedzi = []
        oryg_odp, oryg_kas = hu._odpowiedz, hu._skasuj_wiadomosc
        hu._odpowiedz = lambda tok, czat, tekst: odpowiedzi.append(tekst)
        hu._skasuj_wiadomosc = lambda *a, **k: True
        try:
            # DWIE komendy /sekret w JEDNEJ wiadomosci — realna wpadka z 13.08,
            # gdzie drugi klucz zapisal sie jako "/sekret KAMERY_PASS"
            hu._obsluz_komende("/sekret KLUCZ_A=wartosc_pierwsza\n/sekret KLUCZ_B=wartosc_druga",
                               "token", "1", 77)
            tresc = hu.PLIK_SEKRETOW.read_text(encoding="utf-8")
            klucze = [l.partition("=")[0] for l in tresc.splitlines() if l.strip()]
            sprawdz("T17 dwa /sekret w jednej wiadomosci -> dwa czyste klucze",
                    klucze == ["KLUCZ_A", "KLUCZ_B"], str(klucze))
            sprawdz("T17b zaden klucz nie zawiera '/sekret'",
                    not any("/sekret" in k or " " in k for k in klucze), str(klucze))
            sprawdz("T17c odpowiedz bota bez wartosci",
                    all("wartosc_pierwsza" not in o and "wartosc_druga" not in o for o in odpowiedzi))
        finally:
            hu._odpowiedz, hu._skasuj_wiadomosc = oryg_odp, oryg_kas

        # ZAPIS ZALACZNIKA — podstawiamy siec, zeby nie ruszac Telegrama
        class FalszywaOdp:
            def __init__(self, dane=None, js=None):
                self.content = dane or b""
                self._js = js or {}
            def json(self):
                return self._js
        oryg_get = hu.requests.get
        hu.SKRZYNKA = tmp2 / "skrzynka"
        try:
            hu.requests.get = lambda url, **k: (
                FalszywaOdp(js={"result": {"file_path": "photos/x.jpg"}})
                if "getFile" in url else FalszywaOdp(dane=b"\xff\xd8\xff" + b"0" * 500))
            for pole, wiad, opis in [
                ("photo", {"photo": [{"file_id": "abc", "file_size": 100}]}, "zdjecie"),
                ("document", {"document": {"file_id": "def", "file_name": "raport.pdf"}}, "plik"),
                ("voice", {"voice": {"file_id": "ghi"}}, "glosowka"),
            ]:
                wynik = hu._pobierz_zalacznik(wiad, "token")
                sprawdz(f"T18 {opis} pobrane i zapisane",
                        bool(wynik) and "ZAPISANY" in wynik, str(wynik)[:60])
            pliki = list((tmp2 / "skrzynka" / "pliki").glob("*"))
            sprawdz("T18b trzy pliki faktycznie leza na dysku", len(pliki) == 3, str(len(pliki)))
            sprawdz("T19 zwykly tekst NIE jest brany za zalacznik",
                    hu._pobierz_zalacznik({"text": "dzien dobry"}, "token") is None)
        finally:
            hu.requests.get = oryg_get

    # --- T13-T16: dobor zalogi w bramce ukonczenia (uwaga Zenka z bramki 13.08) ---
    sys.path.insert(0, KATALOG)
    import zrobione
    sprawdz("T13 dowody kodowe: bez Genka",
            zrobione.dobierz_zaloge("tools/hans_ucho.py,dowod.txt") == ["zenek", "henio"],
            str(zrobione.dobierz_zaloge("tools/hans_ucho.py,dowod.txt")))
    sprawdz("T14 dowod z obrazem: Genek dolacza",
            zrobione.dobierz_zaloge("klatka.jpg,raport.txt") == ["zenek", "henio", "genek"])
    sprawdz("T15 dowod z wideo: Genek dolacza",
            zrobione.dobierz_zaloge("kandydat.MP4") == ["zenek", "henio", "genek"])
    sprawdz("T16 wymuszenie flaga: Genek dolacza mimo dowodow tekstowych",
            zrobione.dobierz_zaloge("a.txt", z_genkiem=True) == ["zenek", "henio", "genek"])

    print()
    if bledy:
        print(f"PETLA CZERWONA — {len(bledy)} przypadkow: {', '.join(bledy)}")
        return 1
    print("PETLA ZIELONA — wszystkie przypadki przeszly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
