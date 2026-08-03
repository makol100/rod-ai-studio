#!/usr/bin/env python3
"""Hans: mechaniczna pamięć o markerach pominiętych w meldunku narady."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# Stała lista zapobiega uznaniowemu wybieraniu przez Hansa, czego ma pilnować.
MARKERY = (
    "BRAK SLADU",
    "OBALONE",
    "NIE MA TEGO W PLIKU",
    "TRYB AWARYJNY",
    "NIE WIEM",
    "GLOS NIEODEBRANY",
    "NIEODEBRANY",
    "STOP",
)

DZIENNIK = Path(".scratch/hans/dziennik.jsonl")
# 3.08: LIMIT_PATH wskazywal ZAWSZE ten sam plik, wiec wynik testow zalezal od tego, ile wysylek
# Hans zanotowal w ostatniej godzinie — raz przechodzily, raz nie (Zenek mierzyl FAIL, Klaudek OK,
# obaj mieli racje w swoim oknie czasowym). Pod testami licznik idzie do osobnego pliku,
# wiec stan produkcyjny nigdy na nie nie wplywa.
LIMIT_PATH = (Path(tempfile.gettempdir()) / "_hans_limit_testowy.jsonl"
              if "unittest" in sys.modules
              else Path(".scratch/hans/limit.jsonl"))
LIMIT_GODZINA = 3  # twardy limit wiadomosci na godzine (dekret Genka)

KONFIGI_HANS = (
    "/home/hermes/.hermes/.env",
    "/home/hermes/.hermes/hermes-agent/.env",
)

# Hans nie rozstrzyga, czy wynik jest ważny. Uruchamia kontrolę tylko wtedy, gdy
# autor meldunku sam przedstawia go jako zakończony.
SLOWA_WYKONANIA = re.compile(
    r"\b(?:zrobion\w*|uruchomion\w*|gotow\w*|zapisan\w*)\b",
    re.IGNORECASE,
)
SCIEZKA_W_TEKSCIE = re.compile(
    r"(?<![\w:/.-])(?:/tmp/[^\s'\"`<>]+|(?:\.?\.?/)?(?:tools|data)/[^\s'\"`<>]+)"
)
POMINIETO = re.compile(r"\bPOMINIETO\s*:\s*\S+", re.IGNORECASE)


def _czas_epoch(poczatek_tury: datetime | float | int) -> float:
    """Normalizuje jawnie podany początek tury do czasu POSIX."""
    if isinstance(poczatek_tury, datetime):
        return poczatek_tury.timestamp()
    return float(poczatek_tury)


def _sciezki_z_meldunku(meldunek: str) -> list[str]:
    """Wyciąga wspierane ścieżki i odcina typową interpunkcję zdania."""
    wynik: list[str] = []
    for trafienie in SCIEZKA_W_TEKSCIE.finditer(meldunek):
        sciezka = trafienie.group(0).rstrip(".,;:!?)]}")
        if sciezka and sciezka not in wynik:
            wynik.append(sciezka)
    return wynik


def sprawdz_stan_plikow(
    meldunek: str,
    poczatek_tury: datetime | float | int,
    katalog_bazowy: str | Path | None = None,
) -> dict[str, Any]:
    """Sprawdza twardy stan ścieżek z meldunku o zakończonej pracy.

    Świadome pominięcie musi być wypowiedziane jako ``POMINIETO: powod``.
    Funkcja nie zapisuje dziennika: zwracany raport jest śladem pojedynczej kontroli.
    """
    sciezki = _sciezki_z_meldunku(meldunek)
    wykonanie_zadeklarowane = bool(SLOWA_WYKONANIA.search(meldunek))
    pominieto = bool(POMINIETO.search(meldunek))
    bazowy = Path.cwd() if katalog_bazowy is None else Path(katalog_bazowy)
    start = _czas_epoch(poczatek_tury)
    stany: list[dict[str, Any]] = []
    rozbieznosci: list[dict[str, Any]] = []

    if wykonanie_zadeklarowane:
        for tekst_sciezki in sciezki:
            podana = Path(tekst_sciezki)
            sciezka = podana if podana.is_absolute() else bazowy / podana
            istnieje = sciezka.exists()
            rozmiar = sciezka.stat().st_size if istnieje else None
            mtime = sciezka.stat().st_mtime if istnieje else None
            niepusty = (
                any(sciezka.iterdir()) if istnieje and sciezka.is_dir() else bool(rozmiar)
            )
            stan = {
                "sciezka": tekst_sciezki,
                "istnieje": istnieje,
                "rozmiar": rozmiar,
                "mtime": mtime,
                "niepusty": niepusty,
                "swiezy": bool(mtime is not None and mtime >= start),
            }
            stany.append(stan)

            powod: str | None = None
            komunikat: str | None = None
            if not istnieje:
                powod = "nie_istnieje"
                komunikat = f"STOP. Plik {tekst_sciezki} nie istnieje na dysku."
            elif not niepusty:
                powod = "pusty"
                komunikat = f"STOP. Plik {tekst_sciezki} jest pusty na dysku."
            elif mtime is not None and mtime < start:
                powod = "nie_drgnał"
                komunikat = (
                    f"STOP. Plik {tekst_sciezki} nie drgnal na dysku. "
                    "Zglaszasz wynik bez weryfikacji."
                )
            if powod is not None:
                rozbieznosci.append({**stan, "powod": powod, "komunikat": komunikat})

    niewyjasnione = [] if pominieto else rozbieznosci
    return {
        "poziom": "ALERT" if niewyjasnione else "OK",
        "wykonanie_zadeklarowane": wykonanie_zadeklarowane,
        "pominieto_wyjasnione": pominieto,
        "sciezki": sciezki,
        "stany": stany,
        "rozbieznosci": niewyjasnione,
    }


def _czy_sciezka_zadeklarowana(sciezka_str: str, tekst_meldunku: str) -> bool:
    """Sprawdza, czy dana ścieżka została zadeklarowana jako wykonana/uruchomiona."""
    slowa_wykonania_patterns = [
        r"zrobion\w*", r"gotow\w*", r"uruchomion\w*", r"zapisan\w*",
        r"utworzon\w*", r"naprawion\w*", r"wysłan\w*", r"wyslan\w*"
    ]
    slowa_reg = re.compile(r"\b(?:" + "|".join(slowa_wykonania_patterns) + r")\b", re.IGNORECASE)
    
    if not slowa_reg.search(tekst_meldunku):
        return False
        
    linie = tekst_meldunku.splitlines()
    for i, linia in enumerate(linie):
        if sciezka_str in linia:
            if slowa_reg.search(linia):
                return True
            for j in range(max(0, i-3), i):
                if slowa_reg.search(linie[j]):
                    return True
                    
    zdania = re.split(r'[.!?]+', tekst_meldunku)
    for zdanie in zdania:
        if sciezka_str in zdanie:
            if slowa_reg.search(zdanie):
                return True
                
    return False


def _czy_pominieta(sciezka_str: str, tekst_meldunku: str, sciezki: list[str]) -> bool:
    """Sprawdza, czy dana ścieżka została oznaczona jako pominięta."""
    pominieto_reg = re.compile(r"\bPOMINIETO\s*:", re.IGNORECASE)
    if not pominieto_reg.search(tekst_meldunku):
        return False
        
    if len(sciezki) == 1:
        return True
        
    linie = tekst_meldunku.splitlines()
    for linia in linie:
        if sciezka_str in linia and pominieto_reg.search(linia):
            return True
            
    zdania = re.split(r'[.!?]+', tekst_meldunku)
    for zdanie in zdania:
        if sciezka_str in zdanie and pominieto_reg.search(zdanie):
            return True
            
    nazwa_pliku = Path(sciezka_str).name
    for linia in linie:
        if pominieto_reg.search(linia) and (sciezka_str in linia or nazwa_pliku in linia):
            return True
            
    return False


def weryfikuj_stan_plikow(
    tekst_meldunku: str,
    czas_startu_tury: datetime | float | int,
) -> list[str]:
    """Weryfikuje, czy zadeklarowane jako gotowe ścieżki drgnęły na dysku."""
    sciezki = _sciezki_z_meldunku(tekst_meldunku)
    start = _czas_epoch(czas_startu_tury)
    bazowy = Path.cwd()
    wynik_nie_drgnely: list[str] = []

    for tekst_sciezki in sciezki:
        if not _czy_sciezka_zadeklarowana(tekst_sciezki, tekst_meldunku):
            continue

        if _czy_pominieta(tekst_sciezki, tekst_meldunku, sciezki):
            continue

        podana = Path(tekst_sciezki)
        sciezka = podana if podana.is_absolute() else bazowy / podana
        istnieje = sciezka.exists()
        
        nie_drgnal = False
        if not istnieje:
            nie_drgnal = True
        else:
            rozmiar = sciezka.stat().st_size
            mtime = sciezka.stat().st_mtime
            niepusty = any(sciezka.iterdir()) if sciezka.is_dir() else bool(rozmiar)
            
            if not niepusty:
                nie_drgnal = True
            elif mtime is not None and mtime < start:
                nie_drgnal = True

        if nie_drgnal:
            wynik_nie_drgnely.append(tekst_sciezki)

    return wynik_nie_drgnely


def _wczytaj_tekst(sciezka: Path) -> tuple[str, str | None]:
    """Czyta tekst bez przerywania audytu; błąd wejścia ma trafić do raportu."""
    try:
        return sciezka.read_text(encoding="utf-8"), None
    except OSError as blad:
        return "", f"Nie można odczytać pliku {sciezka}: {blad}"
    except UnicodeError as blad:
        return "", f"Plik {sciezka} nie jest poprawnym UTF-8: {blad}"


def _cytat(plik: Path, numer_linii: int, linia: str) -> dict[str, Any]:
    """Zachowuje dosłowny fragment i miejsce, aby alarm miał sprawdzalny ślad."""
    return {
        "plik": str(plik),
        "linia": numer_linii,
        "cytat": linia.strip(),
    }


def _dopisz_do_dziennika(wynik: dict[str, Any]) -> str | None:
    """Dopisuje jeden rekord JSONL; nigdy nie nadpisuje wcześniejszej historii."""
    try:
        DZIENNIK.parent.mkdir(parents=True, exist_ok=True)
        with DZIENNIK.open("a", encoding="utf-8") as uchwyt:
            uchwyt.write(json.dumps(wynik, ensure_ascii=False, sort_keys=True) + "\n")
        return None
    except (OSError, TypeError, ValueError) as blad:
        # Awaria pamięci nie może ukryć wyniku samej kontroli.
        return f"Nie można dopisać dziennika {DZIENNIK}: {blad}"


def sprawdz_narade(katalog_narady: str | Path, plik_meldunku: str | Path) -> dict[str, Any]:
    """Porównuje markery z głosów z meldunkiem i zwraca raport bez blokowania pracy."""
    katalog = Path(katalog_narady)
    meldunek_path = Path(plik_meldunku)
    bledy_wejscia: list[str] = []
    znalezione: list[dict[str, Any]] = []

    # Brak katalogu jest faktem do zameldowania, nie wyjątkiem kończącym kontrolę.
    if not katalog.is_dir():
        bledy_wejscia.append(f"Brak katalogu narady: {katalog}")
        pliki_glosow: list[Path] = []
    else:
        pliki_glosow = sorted(sciezka for sciezka in katalog.glob("*.txt") if sciezka.is_file())

    for plik in pliki_glosow:
        tekst, blad = _wczytaj_tekst(plik)
        if blad:
            bledy_wejscia.append(blad)
            continue
        # Numer linii i cytat pozwalają Tomaszowi sprawdzić dokładnie przemilczany fragment.
        for numer_linii, linia in enumerate(tekst.splitlines(), start=1):
            linia_duzymi = linia.upper()
            for marker in MARKERY:
                if marker in linia_duzymi:
                    znalezione.append({"marker": marker, **_cytat(plik, numer_linii, linia)})

    if not meldunek_path.is_file():
        meldunek = ""
        bledy_wejscia.append(f"Brak pliku meldunku: {meldunek_path}")
    else:
        meldunek, blad = _wczytaj_tekst(meldunek_path)
        if blad:
            bledy_wejscia.append(blad)

    meldunek_duzymi = meldunek.upper()
    # Każde wystąpienie zachowuje własny cytat, nawet gdy ten sam marker pada w kilku głosach.
    przemilczane = [wpis for wpis in znalezione if wpis["marker"] not in meldunek_duzymi]
    poziom = "ALERT" if bledy_wejscia or przemilczane else "OK"

    wynik: dict[str, Any] = {
        "czas_utc": datetime.now(timezone.utc).isoformat(),
        "katalog_narady": str(katalog),
        "plik_meldunku": str(meldunek_path),
        "pliki_glosow": [str(plik) for plik in pliki_glosow],
        "znalezione_markery": znalezione,
        "przemilczane": przemilczane,
        # Alias zachowuje kontrakt uzgodnionego projektu: lista rozbieżności.
        "rozbieznosci": przemilczane,
        "bledy_wejscia": bledy_wejscia,
        "poziom": poziom,
    }
    blad_dziennika = _dopisz_do_dziennika(wynik)
    if blad_dziennika:
        wynik["bledy_wejscia"].append(blad_dziennika)
        wynik["poziom"] = "ALERT"
    return wynik


def _wczytaj_token_hansa() -> tuple:
    """Zwraca (token, chat_id) dla bota Hansa z plikow .env. Wzor: tools/dzwonek.py."""
    token = czat = ""
    for sciezka in KONFIGI_HANS:
        try:
            with open(sciezka, encoding="utf-8", errors="replace") as f:
                for linia in f:
                    klucz, _, wartosc = linia.strip().partition("=")
                    wartosc = wartosc.strip().strip('"').strip("'")
                    if klucz == "HANS_BOT_TOKEN" and wartosc and not token:
                        token = wartosc
                    elif klucz == "HANS_CHAT_ID" and wartosc and not czat:
                        czat = wartosc
        except OSError:
            continue
    return token, czat


def _sprawdz_limit() -> tuple:
    """Zwraca (ile_w_oknie_godzinnym, czy_zablokowane).

    Czyta LIMIT_PATH (append-only JSONL), liczy wpisy z ostatniej godziny.
    Maks LIMIT_GODZINA wiadomosci na godzine (dekret Genka).
    """
    godzina_temu = datetime.now(timezone.utc).timestamp() - 3600
    licznik = 0
    if LIMIT_PATH.is_file():
        try:
            for linia in LIMIT_PATH.read_text(encoding="utf-8").splitlines():
                if not linia.strip():
                    continue
                try:
                    wpis = json.loads(linia)
                    if wpis.get("czas", 0) >= godzina_temu and wpis.get("wyslane") is True:
                        licznik += 1
                except json.JSONDecodeError:
                    continue
        except OSError:
            pass
    zablokowane = licznik >= LIMIT_GODZINA
    return licznik, zablokowane


def _dopisz_limit(wynik: bool, powod: str = "") -> str | None:
    """Dopisuje rekord do LIMIT_PATH (append-only). Zwraca None lub komunikat bledu."""
    wpis = {
        "czas": datetime.now(timezone.utc).timestamp(),
        "czas_iso": datetime.now(timezone.utc).isoformat(),
        "wyslane": wynik,
        "powod": powod,
    }
    try:
        LIMIT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LIMIT_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(wpis, ensure_ascii=False, sort_keys=True) + "\n")
        return None
    except (OSError, TypeError, ValueError) as blad:
        return f"Nie mozna dopisac limitu {LIMIT_PATH}: {blad}"


def _zbuduj_tresc(raport: dict) -> str | None:
    """Buduje zwiezla wiadomosc z raportu Hansa. Zwraca None gdy nie ma czego zglaszac."""
    poziom = raport.get("poziom", "OK")
    przemilczane = raport.get("przemilczane", [])
    bledy = raport.get("bledy_wejscia", [])

    if poziom == "OK" and not przemilczane and not bledy:
        return None  # nic do zgloszenia — cisza znaczy "czysto"

    linie = ["🤖 HANS — KONTROLA NARADY"]

    if bledy:
        linie.append(f"Bledy wejscia: {len(bledy)}")
        for b in bledy[:5]:
            linie.append(f"  • {b[:200]}")

    if przemilczane:
        linie.append(f"Przemilczane markery: {len(przemilczane)}")
        for p in przemilczane[:10]:
            marker = p.get("marker", "?")
            plik = p.get("plik", "?").split("/")[-1] if p.get("plik") else "?"
            cytat = p.get("cytat", "")[:300]
            linie.append(f"  [{marker}] {plik} linia {p.get('linia', '?')}: \"{cytat}\"")

    if poziom == "OK" and (bledy or przemilczane):
        linie.append("Poziom: OK (bledy/przemilczane sa, ale nie ALERT)")

    if not przemilczane and not bledy:
        return None

    return "\n".join(linie)


def _pod_testami() -> bool:
    """Twarda blokada wysylki podczas testow.

    3.08: mimo podmiany na atrape JEDEN przypadek testowy siegnal do prawdziwego Telegrama —
    w dzienniku limitu wyladowal wpis "message_id=3" (atrapa zwraca 99/100), czyli Tomasz
    dostal na telefon smieci z testu. Ta blokada dziala NIEZALEZNIE od jakosci atrap:
    jesli w pamieci jest unittest albo ustawiono HANS_BEZ_WYSYLKI, prawdziwa wysylka nie nastapi.
    """
    if os.environ.get("HANS_BEZ_WYSYLKI") == "1":
        return True
    if "unittest" not in sys.modules:
        return False
    # Jestesmy pod testami. Blokujemy TYLKO wtedy, gdy wysylka NIE jest podmieniona atrapa —
    # czyli gdy urlopen to prawdziwa funkcja biblioteki. Test z poprawna atrapa ma dzialac dalej.
    return type(urllib.request.urlopen).__name__ == "function"


def wyslij_do_tomasza(raport: dict) -> bool:
    """Wysyla raport Hansa na Telegram, jesli jest co zglaszac.

    Czyta HANS_BOT_TOKEN i HANS_CHAT_ID z /home/hermes/.hermes/.env.
    Wysyla TYLKO gdy raport zawiera cokolwiek do zgloszenia.
    Limit: maks 3 wiadomosci na godzine (dekret Genka).
    Awaria wysylki NIE MOZE zepsuc narady ani kontroli Hansa — zwraca False.

    Zwraca True gdy wyslano, False gdy nie wyslano (lub nie bylo co wysylac).
    """
    # Sprawdz czy jest CO wyslac
    tresc = _zbuduj_tresc(raport)
    if not tresc:
        return False  # cisza znaczy "czysto" — nic do zgloszenia

    # Sprawdz limit godzinny
    licznik, zablokowane = _sprawdz_limit()
    if zablokowane:
        msg = f"Hans wstrzymal wysylke — limit {LIMIT_GODZINA}/h przekroczony ({licznik} w ostatniej godzinie)"
        print(f"[hans] {msg}")
        _dopisz_limit(False, msg)
        return False

    # Wczytaj token i chat_id
    token, czat = _wczytaj_token_hansa()
    if not token or not czat:
        msg = "brak HANS_BOT_TOKEN lub HANS_CHAT_ID w konfiguracji"
        print(f"[hans] {msg}")
        _dopisz_limit(False, msg)
        return False

    # Wyslij na Telegram
    naglowek = "🤖 HANS — RAPORT\n\n"
    dane = urllib.parse.urlencode({
        "chat_id": czat,
        "text": (naglowek + tresc)[:4000],
        "disable_web_page_preview": "true",
    }).encode()
    adres = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        if _pod_testami():
            print("[hans] BLOKADA: wykryto tryb testowy — prawdziwa wysylka wstrzymana")
            return False
        with urllib.request.urlopen(urllib.request.Request(adres, data=dane), timeout=25) as o:
            odp = json.load(o)
        ok = bool(odp.get("ok"))
        msg_id = odp.get("result", {}).get("message_id", "?")
        if ok:
            print(f"[hans] wyslane na Telegram — message_id={msg_id}")
            _dopisz_limit(True, f"message_id={msg_id}")
            return True
        else:
            msg = f"Telegram zwrocil ok=False: {odp.get('description', 'brak opisu')[:200]}"
            print(f"[hans] {msg}")
            _dopisz_limit(False, msg)
            return False
    except urllib.error.HTTPError as e:
        msg = f"HTTP {e.code}: {e.read()[:200].decode(errors='replace')}"
        print(f"[hans] NIE WYSLANE: {msg}")
        _dopisz_limit(False, msg)
        return False
    except Exception as e:
        msg = f"{type(e).__name__}: {str(e)[:150]}"
        print(f"[hans] NIE WYSLANE: {msg}")
        _dopisz_limit(False, msg)
        return False


# ═══════════════════════════════════════════════════════════════════════════
# NOWE FUNKCJE — HENIO, 04.08.2026 (dekret Tomasza: Hans należy do Henia)
# ═══════════════════════════════════════════════════════════════════════════

def _magiczne_slowa_kodu(sciezka: Path) -> set[str]:
    """Zbiera nazwy, identyfikatory i stałe z pliku kodu Python."""
    if not sciezka.suffix == ".py":
        return set()
    try:
        tekst = sciezka.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    slowa: set[str] = set()
    for token in re.findall(r"[A-Z_]{4,}|[a-z_]{6,}", tekst):
        slowa.add(token.lower())
    # Dodajemy nazwy modułów i klas
    for token in re.findall(r"(?:def|class)\s+(\w+)", tekst):
        slowa.add(token.lower())
    return slowa


def _magiczne_slowa_wiedzy(sciezka: Path) -> set[str]:
    """Zbiera słowa kluczowe z pliku wiedzy."""
    if not sciezka.suffix == ".md":
        return set()
    try:
        tekst = sciezka.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    slowa: set[str] = set()
    for token in re.findall(r"[a-z_]{5,}", tekst):
        slowa.add(token)
    # Dodajemy ścieżki plików wymienione w wiedzy
    for trafienie in SCIEZKA_W_TEKSCIE.finditer(tekst):
        slowa.add(trafienie.group(0).lower())
    return slowa


def sprawdz_niedokonczone_slady(katalog_bazowy: str | Path | None = None) -> dict[str, Any]:
    """Wykrywa kod zmieniony bez aktualizacji wiedzy (i odwrotnie).

    Wzorzec Klaudka: zmienia tools/xyz.py, nie aktualizuje wiedza/XYZ.md.
    Skutek dla Henia: czyta nieaktualną wiedzę i podejmuje błędne decyzje.

    Zwraca raport z listą plików, które zmieniły się BEZ powiązanych zmian
    w drugim katalogu. Nie blokuje niczego — tylko melduje.
    """
    bazowy = Path.cwd() if katalog_bazowy is None else Path(katalog_bazowy)
    tools_dir = bazowy / "tools"
    wiedza_dir = bazowy / "wiedza"

    kod_slowa: dict[str, set[str]] = {}
    wiedza_slowa: dict[str, set[str]] = {}

    # Zbieramy słowa z plików kodu (pomijamy testy)
    if tools_dir.is_dir():
        for plik in tools_dir.glob("*.py"):
            if "test" in plik.name.lower():
                continue
            slowa = _magiczne_slowa_kodu(plik)
            if slowa:
                kod_slowa[plik.name] = slowa

    # Zbieramy słowa z plików wiedzy
    if wiedza_dir.is_dir():
        for plik in wiedza_dir.rglob("*.md"):
            slowa = _magiczne_slowa_wiedzy(plik)
            if slowa:
                rel = str(plik.relative_to(wiedza_dir))
                wiedza_slowa[rel] = slowa

    osierocone_kod: list[dict[str, Any]] = []
    osierocone_wiedza: list[dict[str, Any]] = []

    # Każdy plik kodu powinien mieć swój odpowiednik w wiedzy
    for nazwa, slowa_kodu in kod_slowa.items():
        rdzen = Path(nazwa).stem.lower()
        znaleziono = False
        for sciezka_w, slowa_w in wiedza_slowa.items():
            # Sprawdzamy, czy plik wiedzy wspomina o tym pliku kodu
            if nazwa.lower() in slowa_w or rdzen in slowa_w:
                znaleziono = True
                break
            # Albo czy słowa z kodu są w wiedzy
            wspolne = slowa_kodu & slowa_w
            if len(wspolne) >= 3:
                znaleziono = True
                break
        if not znaleziono:
            osierocone_kod.append({
                "plik": f"tools/{nazwa}",
                "problem": "brak_powiazania_w_wiedzy",
                "komunikat": (
                    f"Plik kodu tools/{nazwa} nie ma powiązania w wiedza/. "
                    "Po zmianie kodu Klaudek musi zaktualizować dokumentację."
                ),
            })

    # Każdy plik wiedzy o narzędziach powinien mieć swój odpowiednik w kodzie
    for sciezka_w, slowa_w in wiedza_slowa.items():
        # Interesują nas tylko pliki wiedzy, które opisują narzędzia/procedury
        if not any(s in sciezka_w.lower() for s in (
            "tools", "narzedzi", "procedur", "hans", "genek", "klaudek",
            "zenek", "henio", "decyzje", "styl", "droga", "architekt",
            "kontrol", "bramk", "strazn", "generow",
        )):
            continue
        rdzen_w = Path(sciezka_w).stem.lower()
        znaleziono = False
        for nazwa, slowa_k in kod_slowa.items():
            rdzen_k = Path(nazwa).stem.lower()
            if rdzen_k in slowa_w or rdzen_w in slowa_k:
                znaleziono = True
                break
            wspolne = slowa_k & slowa_w
            if len(wspolne) >= 3:
                znaleziono = True
                break
        if not znaleziono:
            osierocone_wiedza.append({
                "plik": f"wiedza/{sciezka_w}",
                "problem": "brak_powiazania_w_kodzie",
                "komunikat": (
                    f"Plik wiedzy wiedza/{sciezka_w} opisuje procedurę/narzędzie, "
                    "ale nie znaleziono odpowiadającego pliku kodu w tools/. "
                    "Być może opis jest nieaktualny."
                ),
            })

    alerty = osierocone_kod + osierocone_wiedza
    return {
        "czas_utc": datetime.now(timezone.utc).isoformat(),
        "katalog": str(bazowy),
        "pliki_kodu": len(kod_slowa),
        "pliki_wiedzy": len(wiedza_slowa),
        "osierocone_kod": osierocone_kod,
        "osierocone_wiedza": osierocone_wiedza,
        "poziom": "ALERT" if alerty else "OK",
        "rozbieznosci": alerty,
    }


def sprawdz_srodowisko_henia() -> dict[str, Any]:
    """Sprawdza, czy środowisko Henia jest prawidłowo skonfigurowane.

    Wykrywa:
    - nieaktualny alias modelu (FLASH zamiast PRO)
    - limit pamięci poniżej normy
    - brak uprawnień zapisu do repo
    - nieaktualną kartę środowiska

    Problem udokumentowany w TECZKI/HENIO.md: pracowałem na FLASH zamiast PRO
    przez tydzień, bo nikt nie sprawdził konfiguracji. Ta funkcja to wykrywa.
    """
    rozbieznosci: list[dict[str, Any]] = []
    stan: dict[str, Any] = {}

    # 1. Sprawdź model
    config_paths = [
        Path("/home/hermes/.hermes/config.yaml"),
        Path.home() / ".hermes" / "config.yaml",
    ]
    model_ok = False
    for cfg in config_paths:
        try:
            tekst = cfg.read_text(encoding="utf-8", errors="replace")
            stan["config_path"] = str(cfg)
            # Szukamy aliasu modelu
            if "deepseek" in tekst.lower():
                if "pro" in tekst.lower() or "v4-pro" in tekst.lower():
                    model_ok = True
                    stan["model"] = "deepseek-v4-pro (OK)"
                elif "flash" in tekst.lower():
                    stan["model"] = "deepseek-v4-flash (UWAGA: słabszy model!)"
                    rozbieznosci.append({
                        "problem": "model_flash",
                        "komunikat": (
                            "HENIO UŻYWA FLASH ZAMIAST PRO. "
                            "Dekret Tomasza 01.08: 'Bo już jest dobry, a będzie lepszy'. "
                            f"Sprawdź alias w {cfg}."
                        ),
                    })
                else:
                    stan["model"] = "nieznany wariant deepseek"
            else:
                stan["model"] = "nieznany (brak deepseek w config.yaml)"
            break
        except OSError:
            continue
    if not model_ok and "model" not in stan:
        stan["model"] = "NIE SPRAWDZONO — brak config.yaml"
        rozbieznosci.append({
            "problem": "brak_configu",
            "komunikat": "Nie można odczytać config.yaml — nie wiadomo, na jakim modelu działa Henio.",
        })

    # 2. Sprawdź uprawnienia do repo
    repo = Path("/root/rod-ai-studio")
    if repo.is_dir():
        # Append-only: dekret Tomasza zabrania usuwania, więc próba zapisu
        # zostaje w dzienniku zamiast tworzyć i kasować plik tymczasowy.
        test_plik = repo / ".scratch" / "hans" / "proby_zapisu_henia.jsonl"
        try:
            test_plik.parent.mkdir(parents=True, exist_ok=True)
            with test_plik.open("a", encoding="utf-8") as uchwyt:
                uchwyt.write(json.dumps({
                    "czas_utc": datetime.now(timezone.utc).isoformat(),
                    "proba": "zapis_do_repo",
                }, ensure_ascii=False) + "\n")
            stan["zapis_do_repo"] = True
        except OSError as e:
            stan["zapis_do_repo"] = False
            rozbieznosci.append({
                "problem": "brak_zapisu",
                "komunikat": f"HENIO NIE MOŻE ZAPISAĆ DO REPO: {e}. Sprawdź ACL/uprawnienia.",
            })
    else:
        stan["zapis_do_repo"] = "NIE SPRAWDZONO — brak katalogu repo"

    # 3. Sprawdź limit pamięci
    pamiec_path = Path("/sys/fs/cgroup/memory.current")
    pamiec_max = Path("/sys/fs/cgroup/memory.max")
    if pamiec_path.exists():
        try:
            biezaca = int(pamiec_path.read_text().strip())
            stan["pamiec_biezaca_bajty"] = biezaca
            stan["pamiec_biezaca_mb"] = round(biezaca / 1024 / 1024, 1)
            if pamiec_max.exists():
                maks_raw = pamiec_max.read_text().strip()
                if maks_raw != "max":
                    maks = int(maks_raw)
                    stan["pamiec_limit_mb"] = round(maks / 1024 / 1024, 1)
                    if biezaca > maks * 0.8:
                        rozbieznosci.append({
                            "problem": "pamiec_blisko_limitu",
                            "komunikat": (
                                f"HENIO: pamięć {stan['pamiec_biezaca_mb']} MB "
                                f"z {stan['pamiec_limit_mb']} MB (>{round(biezaca/maks*100)}%). "
                                "Ogranicza to kontekst i zdolność analityczną."
                            ),
                        })
        except (ValueError, OSError):
            pass
    else:
        stan["pamiec"] = "NIE SPRAWDZONO — brak cgroup"

    return {
        "czas_utc": datetime.now(timezone.utc).isoformat(),
        "stan": stan,
        "rozbieznosci": rozbieznosci,
        "poziom": "ALERT" if rozbieznosci else "OK",
    }


def sprawdz_narade_z_glosami(
    katalog_narady: str | Path,
    plik_meldunku: str | Path,
) -> dict[str, Any]:
    """Rozszerzona wersja sprawdz_narade — dodatkowo wykrywa pominięte głosy.

    Oprócz markerów sprawdza też, czy każdy plik głosu ma swojego autora
    wymienionego w meldunku Klaudka. Jeśli nie — głos został pominięty.
    """
    wynik = sprawdz_narade(katalog_narady, plik_meldunku)

    # Dodajemy sprawdzenie pominiętych głosów
    katalog = Path(katalog_narady)
    meldunek_path = Path(plik_meldunku)
    meldunek = ""
    if meldunek_path.is_file():
        try:
            meldunek = meldunek_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass

    pominiete_glosy: list[dict[str, Any]] = []
    if katalog.is_dir():
        for plik in sorted(katalog.glob("*.txt")):
            autor = plik.stem.lower()  # np. "zenek", "henio", "genek", "klaudek"
            # Sprawdź, czy autor jest wymieniony w meldunku.
            # Polskie imiona odmieniają się (Zenek→Zenka, Henio→Henia),
            # więc używamy prefiksu 3 znaków zamiast pełnego dopasowania.
            prefiks = autor[:3] if len(autor) >= 3 else autor
            if prefiks not in meldunek.lower() and autor not in meldunek.lower():
                pominiete_glosy.append({
                    "autor": plik.stem,
                    "plik": str(plik),
                    "problem": "glos_pominiety",
                    "komunikat": (
                        f"Głos {plik.stem} ({plik.name}) NIE został wymieniony "
                        "w meldunku Klaudka. Czy Klaudek go uwzględnił?"
                    ),
                })

    if pominiete_glosy:
        wynik["pominiete_glosy"] = pominiete_glosy
        # Dodajemy do rozbieżności
        wynik["rozbieznosci"] = wynik.get("rozbieznosci", []) + pominiete_glosy
        if wynik["poziom"] == "OK":
            wynik["poziom"] = "ALERT"

    return wynik


def main() -> int:
    """Udostępnia tę samą kontrolę z terminala i drukuje pełny raport z cytatami."""
    parser = argparse.ArgumentParser(description="Hans — kontrola Klaudka i ochrona Henia.")
    parser.add_argument("--narada", help="Katalog z głosami *.txt")
    parser.add_argument("--meldunek", help="Plik meldunku Klaudka")
    parser.add_argument("--z-glosami", action="store_true",
                        help="Rozszerzona narada: wykrywaj też pominięte głosy")
    parser.add_argument("--niedokonczone-slady", action="store_true",
                        help="Wykryj kod bez powiązanej wiedzy (wzorzec Klaudka)")
    parser.add_argument("--srodowisko-henia", action="store_true",
                        help="Sprawdź, czy środowisko Henia jest prawidłowe")
    parser.add_argument("--repo", default=None,
                        help="Katalog repo (domyślnie: bieżący)")
    argumenty = parser.parse_args()

    if argumenty.niedokonczone_slady:
        wynik = sprawdz_niedokonczone_slady(argumenty.repo)
        print(json.dumps(wynik, ensure_ascii=False, indent=2))
        return 0

    if argumenty.srodowisko_henia:
        wynik = sprawdz_srodowisko_henia()
        print(json.dumps(wynik, ensure_ascii=False, indent=2))
        return 0

    if argumenty.narada and argumenty.meldunek:
        if argumenty.z_glosami:
            wynik = sprawdz_narade_z_glosami(argumenty.narada, argumenty.meldunek)
        else:
            wynik = sprawdz_narade(argumenty.narada, argumenty.meldunek)
        print(json.dumps(wynik, ensure_ascii=False, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
