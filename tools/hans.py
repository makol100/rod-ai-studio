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


def main() -> int:
    """Udostępnia tę samą kontrolę z terminala i drukuje pełny raport z cytatami."""
    parser = argparse.ArgumentParser(description="Sprawdź, co z głosów pominięto w meldunku.")
    parser.add_argument("--narada", required=True, help="Katalog z głosami *.txt")
    parser.add_argument("--meldunek", required=True, help="Plik meldunku Klaudka")
    argumenty = parser.parse_args()
    print(json.dumps(sprawdz_narade(argumenty.narada, argumenty.meldunek), ensure_ascii=False, indent=2))
    # Hans zgłasza po fakcie i nie blokuje, dlatego także ALERT kończy się kodem zero.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
