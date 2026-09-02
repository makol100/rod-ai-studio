#!/usr/bin/env python3
"""Ucho Hansa: dopisuje wiadomosci Tomasza z Telegrama do jego slow."""

from __future__ import annotations

import os
import subprocess
import sys
import time
import json
import argparse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import filtr_sekretow  # noqa: E402

KONFIGI_HANS = (
    "/home/hermes/.hermes/.env",
    "/home/hermes/.hermes/hermes-agent/.env",
)
STREFA_TOMASZA = ZoneInfo("Europe/Vienna")


def _wczytaj_token_hansa() -> tuple[str, str]:
    """Zwraca (token, chat_id) dla bota Hansa z plikow .env. Wzor: tools/hans.py."""
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


def _pobierz_slowa_path() -> Path:
    # 13.08: bylo wiedza/SLOWA_TOMASZA.md — plik SLEDZONY przez gita w PUBLICZNYM repo
    # makol100/rod-ai-studio. Po wylaczeniu filtra to byla droga hasla prosto na GitHuba.
    return Path(os.environ.get("HANS_SLOWA_PATH", "/root/skrzynka/slowa.md"))



REPO = os.environ.get("HANS_REPO", "/root/rod-ai-studio")  # 4.08: brakowalo tej stalej — moj blad
AWARIE_PATH = os.path.join(REPO, ".scratch", "hans", "ucho_awarie.jsonl")
LICZNIK_PATH = os.path.join(REPO, ".scratch", "hans", "ucho_licznik.json")
PROG_ALARMU = 3  # trzy kolejne nieudane cykle = alarm; przy odpytaniu co 60 s to ok. 3 minuty ciszy

# UWAGA (zmierzone 4.08 07:56): Telegram pozwala tylko na JEDEN nasluch getUpdates naraz.
# Uruchomienie tego narzedzia RECZNIE, gdy chodzi usluga hans-ucho.service, daje blad
# "409 Client Error: Conflict" — czyli FALSZYWA awarie. Przed recznym testem:
#   systemctl stop hans-ucho.service   ... test ...   systemctl start hans-ucho.service


def _zapisz_awarie(powod: str) -> None:
    """Awaria ucha NIE MOZE byc cicha — to kanal, ktorym Tomasz omija pamiec Klaudka.

    Zapisuje kazda awarie (dopisywanie, nigdy nadpisywanie) i liczy KOLEJNE niepowodzenia.
    Po PROG_ALARMU uderza alarmem DRUGIM botem (dzwonek Henia) — bo wlasny kanal Hansa
    jest wlasnie tym, co nie dziala. Alarm wysylany RAZ na serie, zeby nie zasypac Tomasza.
    """
    os.makedirs(os.path.dirname(AWARIE_PATH), exist_ok=True)
    try:
        with open(AWARIE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({"czas": time.time(), "powod": powod}, ensure_ascii=False) + "\n")
    except OSError:
        pass

    stan = {"kolejne": 0, "alarm_wyslany": False}
    try:
        with open(LICZNIK_PATH, encoding="utf-8") as f:
            stan = json.load(f)
    except (OSError, ValueError):
        pass
    stan["kolejne"] = int(stan.get("kolejne", 0)) + 1

    if stan["kolejne"] >= PROG_ALARMU and not stan.get("alarm_wyslany"):
        try:
            subprocess.run(
                ["python3", os.path.join(REPO, "tools", "dzwonek.py"),
                 f"UCHO HANSA NIE DZIALA od {stan['kolejne']} cykli. Powod: {powod[:150]}\n"
                 f"Twoje wiadomosci do @HansFabrykaRolek_bot NIE SA ZAPISYWANE.",
                 "--tytul", "AWARIA UCHA HANSA"],
                capture_output=True, timeout=60)
            stan["alarm_wyslany"] = True
        except (OSError, subprocess.SubprocessError):
            pass
    try:
        with open(LICZNIK_PATH, "w", encoding="utf-8") as f:
            json.dump(stan, f)
    except OSError:
        pass


def _wyczysc_awarie() -> None:
    """Udany cykl zeruje licznik — zeby kolejna seria znow wywolala alarm."""
    try:
        with open(LICZNIK_PATH, encoding="utf-8") as f:
            stan = json.load(f)
        if stan.get("kolejne", 0) or stan.get("alarm_wyslany"):
            with open(LICZNIK_PATH, "w", encoding="utf-8") as f:
                json.dump({"kolejne": 0, "alarm_wyslany": False}, f)
    except (OSError, ValueError):
        pass


def _pobierz_offset_path() -> Path:
    return Path(os.environ.get("HANS_OFFSET_PATH", ".scratch/hans/ucho_offset.json"))


def _wczytaj_offset(sciezka: Path) -> int:
    try:
        if not sciezka.exists():
            return -1
        dane = json.loads(sciezka.read_text(encoding="utf-8"))
        return int(dane.get("offset", -1))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return -1


def _zapisz_offset(offset: int, sciezka: Path) -> None:
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    tymczasowy = sciezka.with_suffix(sciezka.suffix + ".tmp")
    tymczasowy.write_text(
        json.dumps({"offset": offset}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    tymczasowy.replace(sciezka)


def _dopisz_doslownie(tekst: str, epoch: int | float, sciezka: Path) -> None:
    chwila = datetime.fromtimestamp(epoch, STREFA_TOMASZA)
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    with sciezka.open("a", encoding="utf-8") as plik:
        plik.write(f"\n## {chwila:%d.%m.%Y %H:%M:%S} (Europe/Vienna) — Telegram\n\n")
        plik.write(tekst)
        plik.write("\n")
    os.chmod(sciezka, 0o600)  # 13.08: plik powstawal z prawami 644 — moj blad


def _odpowiedz(token: str, czat: str, tekst: str) -> None:
    """Krotka odpowiedz bota. Nigdy nie zawiera tresci sekretu."""
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": czat, "text": tekst[:3500]},
            timeout=30,
        )
    except Exception:  # noqa: BLE001
        pass


SKRZYNKA = Path("/root/skrzynka")          # 700, POZA repozytorium (repo jest publiczne!)
PLIK_SEKRETOW = Path("/root/.sekrety/wartosci.env")  # 600, POZA repozytorium (katalog .sekrety juz istnial)


def _skasuj_wiadomosc(token: str, czat: str, msg_id: int) -> bool:
    """Kasuje wiadomosc Tomasza z Telegrama — zeby sekret nie zostal w historii czatu."""
    try:
        odp = requests.post(
            f"https://api.telegram.org/bot{token}/deleteMessage",
            data={"chat_id": czat, "message_id": msg_id}, timeout=30,
        ).json()
        return bool(odp.get("ok"))
    except Exception:  # noqa: BLE001
        return False


def _zapisz_sekret(linia: str) -> tuple[bool, str]:
    """KLUCZ=WARTOSC albo KLUCZ WARTOSC -> /root/.sekrety (600). Wartosci NIGDY nie zwracamy."""
    tresc = linia.strip()
    if "=" in tresc:
        klucz, _, wartosc = tresc.partition("=")
    else:
        klucz, _, wartosc = tresc.partition(" ")
    klucz = klucz.strip().upper().replace(" ", "_")
    wartosc = wartosc.strip().strip('"').strip("'")
    if not klucz or not wartosc:
        return False, "Podaj w postaci: /sekret KLUCZ=WARTOSC"
    if not all(z.isalnum() or z == "_" for z in klucz):
        return False, "Nazwa klucza tylko litery, cyfry i podkreslnik."

    try:
        stare = PLIK_SEKRETOW.read_text(encoding="utf-8") if PLIK_SEKRETOW.exists() else ""
    except OSError as blad:
        return False, f"Nie moge odczytac pliku sekretow: {type(blad).__name__}"

    linie, podmieniony = [], False
    for l in stare.splitlines():
        if l.strip() and not l.lstrip().startswith("#") and l.partition("=")[0].strip() == klucz:
            linie.append(f"{klucz}={wartosc}")
            podmieniony = True
        else:
            linie.append(l)
    if not podmieniony:
        linie.append(f"{klucz}={wartosc}")

    try:
        tymczasowy = PLIK_SEKRETOW.with_suffix(".tmp")
        tymczasowy.write_text("\n".join(linie).strip() + "\n", encoding="utf-8")
        os.chmod(tymczasowy, 0o600)
        tymczasowy.replace(PLIK_SEKRETOW)
        os.chmod(PLIK_SEKRETOW, 0o600)
    except OSError as blad:
        return False, f"Nie moge zapisac: {type(blad).__name__}"

    czynnosc = "PODMIENIONY" if podmieniony else "ZAPISANY"
    return True, f"{czynnosc} sekret {klucz} ({len(wartosc)} znakow). Wartosci nie drukuje nigdzie."


def _lista_sekretow() -> str:
    """TYLKO nazwy kluczy. Nigdy wartosci."""
    nazwy = []
    for sciezka in (PLIK_SEKRETOW, Path("/root/.hilook_cred")):
        try:
            for l in sciezka.read_text(encoding="utf-8").splitlines():
                l = l.strip()
                if l and not l.startswith("#"):
                    nazwy.append(f"{l.partition('=')[0].strip()}  ({sciezka.name})")
        except OSError:
            continue
    return "Zapisane klucze (same nazwy):\n" + ("\n".join(nazwy) if nazwy else "(pusto)")


def _zapisz_dane(tekst: str) -> str:
    SKRZYNKA.mkdir(parents=True, exist_ok=True)
    plik = SKRZYNKA / "dane.md"
    chwila = datetime.now(STREFA_TOMASZA)
    with plik.open("a", encoding="utf-8") as f:
        f.write(f"\n## {chwila:%d.%m.%Y %H:%M:%S} — Telegram\n\n{tekst}\n")
    os.chmod(plik, 0o600)
    return f"ZAPISANE do skrzynki ({len(tekst)} znakow). Lezy poza repozytorium."


def _pobierz_zalacznik(wiadomosc: dict, token: str) -> str | None:
    """Zdjecie albo plik z Telegrama -> /root/skrzynka/pliki. Zwraca komunikat albo None."""
    file_id = nazwa = None
    # 13.08: bylo TYLKO document i photo — glosowka, wideo czy naklejka przepadaly po cichu.
    domyslne = {
        "document": "plik", "voice": "glosowka.ogg", "audio": "audio.mp3",
        "video": "wideo.mp4", "video_note": "kolko.mp4", "animation": "animacja.mp4",
        "sticker": "naklejka.webp",
    }
    for pole, domyslna_nazwa in domyslne.items():
        obiekt = wiadomosc.get(pole)
        if isinstance(obiekt, dict) and obiekt.get("file_id"):
            file_id = obiekt["file_id"]
            nazwa = obiekt.get("file_name") or domyslna_nazwa
            break
    if not file_id and isinstance(wiadomosc.get("photo"), list) and wiadomosc["photo"]:
        najwieksze = max(wiadomosc["photo"], key=lambda p: p.get("file_size", 0))
        file_id = najwieksze.get("file_id")
        nazwa = "zdjecie.jpg"
    if not file_id:
        return None

    try:
        info = requests.get(f"https://api.telegram.org/bot{token}/getFile",
                            params={"file_id": file_id}, timeout=30).json()
        sciezka_zdalna = info["result"]["file_path"]
        dane = requests.get(
            f"https://api.telegram.org/file/bot{token}/{sciezka_zdalna}", timeout=120
        ).content
    except Exception as blad:  # noqa: BLE001
        return f"NIE POBRALEM zalacznika: {type(blad).__name__}"

    SKRZYNKA.joinpath("pliki").mkdir(parents=True, exist_ok=True)
    bezpieczna = "".join(z for z in nazwa if z.isalnum() or z in "._-") or "plik"
    chwila = datetime.now(STREFA_TOMASZA)
    cel = SKRZYNKA / "pliki" / f"{chwila:%Y%m%d_%H%M%S}_{bezpieczna}"
    try:
        cel.write_bytes(dane)
        os.chmod(cel, 0o600)
    except OSError as blad:
        return f"NIE ZAPISALEM zalacznika: {type(blad).__name__}"
    komunikat = f"ZAPISANY plik: {cel.name} ({len(dane)} bajtow). Lezy w /root/skrzynka/pliki."

    # 17.08.2026: ciasteczka YouTube rozpoznajemy PO TRESCI i przenosimy do skrytki,
    # zeby tools/film.py mial je od reki. Powod: Tomasz przyslal je kiedys i przepadly,
    # bo nikt ich nie zapisal — przeszukanie 497 sesji i calej historii gita nic nie dalo.
    # NIGDY nie drukujemy zawartosci ani nazw ciasteczek — to dostep do konta Google.
    try:
        poczatek = dane[:200].decode("utf-8", errors="ignore")
        if "Netscape HTTP Cookie" in poczatek or "# HTTP Cookie File" in poczatek:
            tresc = dane.decode("utf-8", errors="ignore")
            if "youtube.com" in tresc or "google.com" in tresc:
                skrytka = Path("/root/.sekrety")
                skrytka.mkdir(parents=True, exist_ok=True)
                os.chmod(skrytka, 0o700)
                docelowy = skrytka / "youtube_cookies.txt"
                docelowy.write_bytes(dane)
                os.chmod(docelowy, 0o600)
                cel.unlink(missing_ok=True)  # nie zostawiamy kopii w skrzynce
                wpisow = sum(1 for l in tresc.splitlines()
                             if l.strip() and not l.startswith("#"))
                komunikat = (f"ROZPOZNANE CIASTECZKA YouTube — {wpisow} wpisow. "
                             "Zapisane do skrytki (600, poza repozytorium), kopia ze "
                             "skrzynki usunieta. Tresci nie drukuje. "
                             "Teraz dziala: python3 tools/film.py <link>")
    except Exception:  # noqa: BLE001
        pass  # rozpoznanie jest dodatkiem — nigdy nie moze zepsuc zapisu zalacznika

    return komunikat


def _obsluz_sekret(tekst: str, token: str, czat: str, msg_id: int | None) -> str:
    """Zapis sekretu i kasowanie wiadomosci — z KONTROLA WYNIKU kasowania.

    Uwaga Zenka z bramki 13.08: kasowanie bylo wolane bez sprawdzenia wyniku, wiec przy
    nieudanym deleteMessage sekret zostawalby w historii czatu, a Tomasz nie wiedzialby o tym.
    """
    ok, komunikat = _zapisz_sekret(tekst)
    if not ok:
        return komunikat
    if msg_id is None:
        return komunikat + "\nUWAGA: nie znam numeru wiadomosci — SKASUJ JA RECZNIE z czatu."
    if _skasuj_wiadomosc(token, czat, int(msg_id)):
        return komunikat + "\nTwoja wiadomosc skasowana z czatu Telegrama."
    return (komunikat + "\nUWAGA: NIE UDALO SIE skasowac Twojej wiadomosci z Telegrama "
            "(bot moze kasowac tylko wiadomosci mlodsze niz 48 h i musi miec prawo do kasowania). "
            "SKASUJ JA RECZNIE — sekret nadal wisi w historii czatu.")


def _obsluz_komende(tekst: str, token: str, czat: str, msg_id: int | None = None) -> bool:
    """Komendy Tomasza. Zwraca True, jesli wiadomosc byla komenda (nie zapisujemy jej do slow)."""
    komenda = tekst.strip().split()[0].lower().split("@")[0] if tekst.strip() else ""
    if komenda not in ("/pakiet", "/wznow", "/pomoc", "/start", "/help",
                       "/sekret", "/sekrety", "/dane", "/henio", "/bzb"):
        return False

    reszta = tekst.strip()[len(komenda):].strip()

    # 25.08 DROGA DO HENIA PRZEZ TELEGRAM (dekret Tomasza: "zrobisz mi droge przez
    # telegram do tego modelu"). Ustalenia z narady: Qwen 3.8 27B na naszym VPS NIE
    # ruszy (dense 27B, 2-3 tok/s na CPU, Q4 nie miesci sie w 17 GB) — ale Henio
    # (DeepSeek v4 pro) NIE ODMAWIA ostrego humoru, sprawdzone pomiarem. Wiec droga
    # prowadzi do Henia, nie do Qwena. Zmiana adresata = zmiana jednej linii nizej.
    # 25.08 BELZEBUB — pisarz-doradca bez mechanizmu odmawiania (imie nadal Tomasz).
    # Osobny uzytkownik systemowy: BEZ sudo, BEZ dockera, BEZ dostepu do /root/.sekrety
    # i do repo — zgodnie ze stanowiskiem Zenka ("tak dla piatego pracownika, nie dla
    # piatego roota") i Henia, oba niezalezne. Prompt injection przez tresc z sieci jest
    # udokumentowany (NIST) i dotyczy takze modeli Z zabezpieczeniami — model po ablacji
    # nie ma hamulca w ogole. Belzebub PROPONUJE, wykonuje Henio albo Klaudek.
    if komenda == "/bzb":
        # 25.08: /sekret zapisuje do zbiorczego wartosci.env, nie do osobnego pliku
        def _klucz_bzb() -> str:
            for sc in ("/root/.sekrety/belzebub.key", "/root/.sekrety/wartosci.env"):
                try:
                    t = Path(sc).read_text(encoding="utf-8")
                except OSError:
                    continue
                if sc.endswith(".key") and t.strip():
                    return t.strip()
                # 25.08: bierzemy OSTATNI wpis (Tomasz przyslal klucz dwa razy —
                # pierwszy raz z nawiasami <> z mojej instrukcji) i czyscimy nawiasy
                znaleziony = ""
                for lin in t.splitlines():
                    if lin.strip().upper().startswith(("BELZEBUB", "FEATHERLESS")):
                        znaleziony = lin.split("=", 1)[-1].strip().strip('"\'').strip("<>")
                if znaleziony:
                    return znaleziony
            return ""
        _kbzb = _klucz_bzb()
        if not _kbzb:
            _odpowiedz(token, czat,
                       "Belzebub nie ma jeszcze klucza.\n\n"
                       "1. featherless.ai/register (email + haslo min. 8 znakow)\n"
                       "2. plan Developer (od $50 kredytow/mies, karta przez Stripe)\n"
                       "3. Account -> API Keys -> utworz klucz\n"
                       "4. przyslij: /sekret BELZEBUB_KEY=<klucz>")
            return True
        if not reszta:
            _odpowiedz(token, czat, "Napisz: /bzb <polecenie>")
            return True
        _odpowiedz(token, czat, "Belzebub dostal. Pracuje...")
        try:
            # 25.08: powloka Hermesa wymaga kontekstu 64K, a ten model ma 32K —
            # obejscie przez context_length nie dziala ("Cannot compress further").
            # Tomasz wybral rolę PISARZA ("no to pisarz"), wiec narzedzia systemowe
            # nie sa potrzebne. Idziemy PROSTO do API (sprawdzone: model odpowiedzial
            # po polsku o dzialkowcu i kunach).
            import json as _js, urllib.request as _ur
            # 25.08 dekret Tomasza: "dac pamiec co z nim pisze", limit "32k tokenow MAX".
            # Budujemy historie z archiwum /root/rozmowy_belzebub od NAJNOWSZEJ wymiany,
            # doklejajac az do bezpiecznego progu. Model ma 32K ctx; rezerwujemy miejsce
            # na nowa odpowiedz (1500 tok) + bufor. ~4 znaki/token => prog 22000 tokenow
            # historii = ~88000 znakow. Nowe pytanie zawsze na koncu.
            _hist = []
            try:
                _kat = Path("/root/rozmowy_belzebub")
                _pliki = sorted(_kat.glob("2*.md"), reverse=True)  # najnowsze pierwsze
                _budzet_znakow = 88000  # ~22K tokenow historii, zapas do 32K
                _zebrane = []
                for _pl in _pliki:
                    try:
                        _tekst = _pl.read_text(encoding="utf-8")
                    except OSError:
                        continue
                    # rozbij na pytanie i odpowiedz po naglowkach
                    _q = _a = ""
                    if "## PYTANIE TOMASZA" in _tekst and "## ODPOWIEDZ BELZEBUBA" in _tekst:
                        _cz = _tekst.split("## ODPOWIEDZ BELZEBUBA", 1)
                        _q = _cz[0].split("## PYTANIE TOMASZA", 1)[-1].strip()
                        _a = _cz[1].strip()
                    if not _q:
                        continue
                    _dlugosc = len(_q) + len(_a)
                    if sum(len(x["content"]) for x in _zebrane) + _dlugosc > _budzet_znakow:
                        break  # 32K sufit — nie przekraczamy
                    # wstawiamy na POCZATEK (bo idziemy od najnowszej wstecz)
                    _zebrane.insert(0, {"role": "assistant", "content": _a})
                    _zebrane.insert(0, {"role": "user", "content": _q})
                _hist = _zebrane
            except Exception:  # noqa: BLE001
                _hist = []  # brak pamieci nie moze zablokowac odpowiedzi
            # 02.09 BELZEBUB 2.0 (dekret Tomasza: mocniejszy model bez kontroli, pelny dostep
            # do sieci): petla narzedziowa w tools/belzebub_agent.py — model SAM szuka
            # (SearXNG bez safesearch) i CZYTA cale strony, do 6 rund; linki nieodwiedzone
            # sa oznaczane. Model: huihui-ai/Huihui-Qwen3.8-27B-abliterated (D-0214/D-0215).
            import sys as _sys
            if "/root/rod-ai-studio/tools" not in _sys.path:
                _sys.path.insert(0, "/root/rod-ai-studio/tools")
            import importlib as _il
            import belzebub_agent as _bzb
            _il.reload(_bzb)
            odp, _slad = _bzb.odpowiedz(reszta, _hist, _kbzb)
            if _slad:
                odp = odp + "\n\n" + _slad
            # 25.08 dekret Tomasza: "To zrob taki folder z pytaniami i odpowiedziami"
            # Kazda wymiana /bzb ladu­je na dysku — Tomasz i Henio moga wrocic do tresci.
            try:
                import datetime as _dt
                _kat = Path("/root/rozmowy_belzebub")
                _kat.mkdir(mode=0o700, exist_ok=True)
                _stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
                _plik = _kat / f"{_stamp}.md"
                _plik.write_text(
                    f"# Belzebub — wymiana {_stamp}\n\n"
                    f"## PYTANIE TOMASZA\n\n{reszta}\n\n"
                    f"## ODPOWIEDZ BELZEBUBA\n\n{odp}\n",
                    encoding="utf-8")
                _plik.chmod(0o600)
                with (_kat / "SPIS.md").open("a", encoding="utf-8") as _s:
                    _s.write(f"- {_stamp}.md — {reszta[:90]}\n")
            except Exception:  # noqa: BLE001
                pass  # archiwum nie moze zablokowac odpowiedzi do Tomasza
            for i2 in range(0, min(len(odp), 12000), 3800):
                _odpowiedz(token, czat, odp[i2:i2+3800])
        except Exception as exc:  # noqa: BLE001
            _odpowiedz(token, czat, f"Belzebub nie odpowiedzial: {exc}")
        return True

    if komenda == "/henio":
        if not reszta:
            _odpowiedz(token, czat,
                       "Napisz: /henio <polecenie>\n\n"
                       "Henio ma pelny dostep do VPS (sudo, docker, repo).\n"
                       "Odpowiedz potrafi zajac kilka minut przy dluzszej robocie.")
            return True
        _odpowiedz(token, czat, "Henio dostal. Pracuje...")
        try:
            import secrets as _sec, shlex as _shl, subprocess as _sub, json as _js, os as _os
            zad = f"/tmp/_henio_tg_{_sec.token_hex(6)}.txt"
            Path(zad).write_text(reszta, encoding="utf-8")
            _os.chmod(zad, 0o644)
            uzycie = f"/tmp/_henio_tg_usage_{_sec.token_hex(6)}.json"
            w = _sub.run(
                ["su", "-", "hermes", "-c",
                 f"HERMES_VERIFY_ON_STOP=0 hermes --usage-file {_shl.quote(uzycie)} "
                 f'-z "$(cat {zad})"'],
                capture_output=True, text=True, timeout=1800)
            koncowa = (w.stdout or w.stderr).strip()
            # pelna tura z bazy sesji (D-0123): -z zwraca tylko ostatnia wypowiedz
            try:
                sid = str(_js.loads(Path(uzycie).read_text()).get("session_id") or "").strip()
                e = _sub.run(["su", "-", "hermes", "-c",
                              f"hermes sessions export - --format jsonl --session-id {_shl.quote(sid)}"],
                             capture_output=True, text=True, timeout=120)
                czesci = [m["content"].strip() for m in _js.loads(e.stdout).get("messages", [])
                          if m.get("role") == "assistant"
                          and isinstance(m.get("content"), str) and m["content"].strip()]
                if koncowa and koncowa not in czesci:
                    czesci.append(koncowa)
                odp = "\n\n".join(czesci) or koncowa
            except Exception:
                odp = koncowa
            for plik in (zad, uzycie):
                try: _os.unlink(plik)
                except OSError: pass
            odp = odp or "Henio nie odpowiedzial."
            # Telegram tnie po 4096 znakow
            for i in range(0, min(len(odp), 12000), 3800):
                _odpowiedz(token, czat, odp[i:i+3800])
        except Exception as exc:  # noqa: BLE001
            _odpowiedz(token, czat, f"Henio nie odpowiedzial: {exc}")
        return True

    if komenda == "/sekret":
        # 13.08: Tomasz wyslal DWIE komendy w jednej wiadomosci — klucz wyszedl jako
        # "/sekret KAMERY_PASS". Kazda linia jest teraz osobnym sekretem.
        linie = [l.strip() for l in tekst.strip().splitlines() if l.strip()]
        komunikaty = []
        for i, linia in enumerate(linie):
            if linia.lower().startswith("/sekret"):
                linia = linia[len("/sekret"):].strip()
            if not linia:
                continue
            if i == 0:
                komunikaty.append(_obsluz_sekret(linia, token, czat, msg_id))
            else:
                komunikaty.append(_zapisz_sekret(linia)[1])
        _odpowiedz(token, czat, "\n".join(komunikaty) or "Nic nie podales.")
        return True

    if komenda == "/sekrety":
        _odpowiedz(token, czat, _lista_sekretow())
        return True

    if komenda == "/dane":
        if not reszta:
            _odpowiedz(token, czat, "Nic nie podales. Uzycie: /dane <tresc>")
        else:
            _odpowiedz(token, czat, _zapisz_dane(reszta))
        return True

    if komenda in ("/pomoc", "/start", "/help"):
        _odpowiedz(token, czat,
                   "/henio <polecenie> — wysyla zadanie do Henia (ma pelny dostep do VPS)\nHans — ratunek kontekstu.\n"
                   "/pakiet  — przyslij PAKIET WZNOWIENIA jako plik .txt "
                   "(wklejasz go do nowego okna czatu po blokadzie)\n"
                   "/wznow   — to samo co /pakiet\n"
                   "/sekret KLUCZ=WARTOSC — zapis hasla/tokenu do /root/.sekrety (600, "
                   "POZA repozytorium). Bot kasuje Twoja wiadomosc z czatu i NIGDY nie "
                   "drukuje wartosci.\n"
                   "/sekrety — lista SAMYCH NAZW zapisanych kluczy\n"
                   "/dane <tresc> — zapis danych roboczych do /root/skrzynka (poza repo)\n"
                   "zdjecie albo plik — pobiera sie do /root/skrzynka/pliki\n\n"
                   "Kazda INNA wiadomosc idzie do /root/skrzynka/slowa.md — katalog 700, "
                   "plik 600, POZA repozytorium (od 13.08). Nic stamtad nie trafia na GitHuba. "
                   "Poswiadczenia i tak wysylaj przez /sekret — ich tresc jest maskowana "
                   "w dzienniku diagnostycznym, zwykle wiadomosci nie.")
        return True

    _odpowiedz(token, czat, "Skladam pakiet wznowienia...")
    try:
        wynik = subprocess.run(
            ["python3", os.path.join(REPO, "tools", "pakiet_wznowienia.py"), "--wyslij", "--cicho"],
            cwd=REPO, capture_output=True, text=True, timeout=180,
        )
    except (OSError, subprocess.SubprocessError) as blad:
        _odpowiedz(token, czat, f"PAKIET NIE POWSTAL: {type(blad).__name__}")
        return True
    if wynik.returncode != 0:
        powod = (wynik.stderr or "").strip()[:600] or f"kod {wynik.returncode}"
        powod = powod.replace("PAKIET NIE POWSTAL — ", "").replace(
            "PAKIET NIE POWSTAL —", "").strip()
        _odpowiedz(token, czat, f"PAKIET NIE POWSTAL (fail-closed):\n{powod}")
    return True


def _zamaskuj_wrazliwe(aktualizacja: dict) -> dict:
    """Kopia aktualizacji z zamaskowana trescia komend wrazliwych (19.08).

    Diagnostyka ma pokazywac KSZTALT tego, co przysyla Telegram — nie tresc sekretow.
    Maskujemy: /sekret, /dane, oraz teksty wygladajace na poswiadczenia. Reszta bez zmian.
    """
    import copy as _copy
    import re as _re
    try:
        kopia = _copy.deepcopy(aktualizacja)
    except Exception:  # noqa: BLE001
        return {"update_id": aktualizacja.get("update_id"), "_uwaga": "nie udalo sie skopiowac"}

    wzorce_wrazliwe = _re.compile(
        r"^\s*/(sekret|dane)\b|sk-[A-Za-z0-9_-]{8,}|AIza[A-Za-z0-9_-]{10,}|"
        r"(haslo|password|token|api[_-]?key)\s*[:=]",
        _re.IGNORECASE,
    )
    for klucz in ("message", "edited_message", "channel_post"):
        wiad = kopia.get(klucz)
        if not isinstance(wiad, dict):
            continue
        tekst = wiad.get("text") or wiad.get("caption")
        if isinstance(tekst, str) and wzorce_wrazliwe.search(tekst):
            komenda = tekst.split()[0] if tekst.split() else "?"
            zamiennik = f"<ZAMASKOWANE {len(tekst)} znakow, komenda: {komenda[:20]}>"
            if "text" in wiad:
                wiad["text"] = zamiennik
            if "caption" in wiad:
                wiad["caption"] = zamiennik
    return kopia


# 02.09.2026 DEKRET Tomasza: "Udostepnilem Hans_bot mojej Wiktorii. Masz Jej go nie zablokowac!"
# Dozwoleni nadawcy = Tomasz (HANS_CHAT_ID) + lista w /root/skrzynka/dozwolone_ids.json.
# Nadawca o imieniu Wiktoria (Telegram first_name) jest wpuszczany automatycznie i dopisywany do listy;
# inni nieznani NIE sa obslugiwani, Tomasz dostaje o nich powiadomienie (ID + imie).
_DOZWOLENI_PLIK = Path("/root/skrzynka/dozwolone_ids.json")
def _dozwoleni() -> dict:
    try:
        return json.loads(_DOZWOLENI_PLIK.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}
def _dodaj_dozwolonego(id_: str, imie: str) -> None:
    d = _dozwoleni(); d[str(id_)] = imie
    _DOZWOLENI_PLIK.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    _DOZWOLENI_PLIK.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    _DOZWOLENI_PLIK.chmod(0o600)
def _kto(id_czatu: str, id_nadawcy: str, nadawca: dict, chat_id: str, token: str) -> str | None:
    """Zwraca 'tomasz', imie dozwolonego, albo None (nieznany — nie obslugujemy)."""
    if id_czatu == str(chat_id) or id_nadawcy == str(chat_id):
        return "tomasz"
    d = _dozwoleni()
    if id_nadawcy in d:
        return d[id_nadawcy]
    imie = (nadawca.get("first_name") or "").strip()
    # 02.09 Tomasz: "Wikus tak mam ja na telegramie" — imie w Telegramie to Wikus, nie Wiktoria
    _im = imie.lower().replace("ś", "s")
    if _im and any(w in _im for w in ("wiktoria", "wikus", "wika", "wiki")):
        _dodaj_dozwolonego(id_nadawcy, imie or "Wiktoria")
        try:
            _odpowiedz(token, chat_id, f"Hans: Wiktoria ({imie}, id {id_nadawcy}) napisala pierwszy raz — wpuszczona na Twoj dekret z 02.09.")
        except Exception:  # noqa: BLE001
            pass
        return imie or "Wiktoria"
    try:
        _odpowiedz(token, chat_id, f"Hans: NIEZNANY nadawca {imie or '?'} (id {id_nadawcy}) napisal do bota — NIE obsluzone. Jesli to ktos Twoj, dopisz do /root/skrzynka/dozwolone_ids.json.")
    except Exception:  # noqa: BLE001
        pass
    return None

def uruchom_ucho(token: str | None = None, chat_id: str | None = None) -> bool:
    """Główna funkcja odpytująca Telegram i zapisująca słowa Tomasza."""
    # 1. Uzgodnienie danych uwierzytelniających
    env_token, env_chat_id = _wczytaj_token_hansa()
    token = token or os.environ.get("HANS_BOT_TOKEN") or env_token
    chat_id = chat_id or os.environ.get("HANS_CHAT_ID") or env_chat_id

    if not token or not chat_id:
        print("Hans ucho: brak tokenu lub chat_id.", file=sys.stderr)
        return False

    slowa_path = _pobierz_slowa_path()
    offset_path = _pobierz_offset_path()

    offset = _wczytaj_offset(offset_path)

    # 2. Odpytanie Telegram getUpdates przy użyciu requests
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {"offset": offset + 1, "timeout": 20}
    try:
        res = requests.get(url, params=params, timeout=45)
        res.raise_for_status()
        dane = res.json()
    except Exception as e:
        # 4.08: TU BYLO "return True" — awaria byla meldowana jako SUKCES. Wykryl Zenek w audycie:
        # "hans_ucho uznaje awarie Telegrama za sukces, wiec moze bez konca nie odbierac slow
        # Tomasza, a usluga nadal wyglada na dzialajaca". To bylo ciche milczenie tego samego
        # mechanizmu, ktory mial zerwac zaleznosc od pamieci Klaudka.
        _zapisz_awarie(f"polaczenie/odpowiedz: {e}")
        print(f"Hans ucho: AWARIA polaczenia z Telegramem: {e}", file=sys.stderr)
        return False

    if not dane.get("ok") or not isinstance(dane.get("result"), list):
        _zapisz_awarie(f"wadliwa odpowiedz: {str(dane)[:200]}")
        print(f"Hans ucho: AWARIA — Telegram zwrocil blad lub zly format: {dane}", file=sys.stderr)
        return False

    wyniki = dane["result"]
    dopisane = 0
    ostatni_offset = offset

    for aktualizacja in sorted(wyniki, key=lambda x: int(x.get("update_id", -1))):
        up_id = int(aktualizacja.get("update_id", -1))
        if up_id <= offset:
            continue

        try:  # 13.08 diagnostyka: co Telegram NAPRAWDE przysyla
            # 19.08 NAPRAWA (znalazl Zenek przy kontroli napraw): CALA surowa aktualizacja
            # ladowala tu ZANIM kod rozpoznal /sekret — czyli haslo wyslane ta komenda
            # zostawialo slad w pliku diagnostycznym. Teraz tresc komend wrazliwych
            # jest maskowana PRZED zapisem; struktura zostaje, bo po to ta diagnostyka jest.
            do_zapisu = _zamaskuj_wrazliwe(aktualizacja)
            Path("/root/skrzynka").mkdir(parents=True, exist_ok=True)
            with open("/root/skrzynka/surowe_aktualizacje.jsonl", "a", encoding="utf-8") as _d:
                _d.write(json.dumps(do_zapisu, ensure_ascii=False) + "\n")
            os.chmod("/root/skrzynka/surowe_aktualizacje.jsonl", 0o600)
        except OSError:
            pass

        wiadomosc = aktualizacja.get("message")
        if not isinstance(wiadomosc, dict):
            wiadomosc = aktualizacja.get("edited_message")

        if isinstance(wiadomosc, dict):
            czat = wiadomosc.get("chat", {})
            nadawca = wiadomosc.get("from", {})
            id_czatu = str(czat.get("id"))
            id_nadawcy = str(nadawca.get("id"))

            tekst = wiadomosc.get("text")
            if tekst is None:
                tekst = wiadomosc.get("caption")

            kto = _kto(id_czatu, id_nadawcy, nadawca, str(chat_id), token)
            # Przechwytujemy wiadomości od Tomasza i dozwolonych (Wiktoria, dekret 02.09)
            if kto:
                # 13.08 BLAD KLAUDKA: _pobierz_zalacznik istniala, ale NIE BYLA WOLANA.
                # Skutek: zdjecie/plik od Tomasza przesuwalo offset i przepadalo bez sladu.
                komunikat_zalacznika = _pobierz_zalacznik(wiadomosc, token)
                if komunikat_zalacznika:
                    if isinstance(tekst, str) and tekst.strip():
                        _zapisz_dane(f"(podpis do pliku) {tekst.strip()}")
                        komunikat_zalacznika += " Podpis zapisany do skrzynki."
                    _odpowiedz(token, id_czatu, komunikat_zalacznika)
                    print(f"Hans ucho: {komunikat_zalacznika}")
                    ostatni_offset = up_id
                    _zapisz_offset(ostatni_offset, offset_path)
                    continue

            if kto and isinstance(tekst, str):
                # 13.08: komendy nie ida do SLOWA_TOMASZA.md
                if _obsluz_komende(tekst, token, id_czatu, wiadomosc.get("message_id")):
                    ostatni_offset = up_id
                    _zapisz_offset(ostatni_offset, offset_path)
                    continue
                # 13.08 POLECENIE TOMASZA: "Wylacz te zabezpieczenie, tylko ja z tego pisze".
                # Filtr na WEJSCIU jest wylaczony — kazdy tekst przechodzi.
                # W zamian slowa NIE ida juz do publicznego repo, tylko do /root/skrzynka
                # (700), wiec nawet haslo wyslane pomylkowo nie trafia na GitHuba.
                if kto == "tomasz":
                    _dopisz_doslownie(tekst, wiadomosc.get("date", time.time()), slowa_path)
                else:
                    # slowa innych osob — OSOBNY plik, nigdy do SLOWA_TOMASZA (to nie dekrety)
                    _dopisz_doslownie(f"[{kto}] {tekst}", wiadomosc.get("date", time.time()), Path("/root/skrzynka/SLOWA_INNYCH.md"))
                dopisane += 1

            elif kto:
                # 13.08: wiadomosc od Tomasza, ktorej NIE UMIEM odebrac, nie moze zniknac
                # po cichu — dokladnie to stalo sie o 10:58 i 11:02.
                pola = sorted(k for k in wiadomosc
                              if k not in ("message_id", "from", "chat", "date"))
                _odpowiedz(token, id_czatu,
                           "NIE UMIEM TEGO ODEBRAC — wiadomosc nie zostala zapisana.\n"
                           f"Rodzaj: {', '.join(pola) or 'nieznany'}\n"
                           "Napisz to tekstem albo wyslij jako plik/zdjecie.")
                print(f"Hans ucho: NIEROZPOZNANA wiadomosc, pola: {pola}")

        ostatni_offset = up_id
        _zapisz_offset(ostatni_offset, offset_path)

    if dopisane > 0 or wyniki:
        print(f"Hans ucho: odebrano {len(wyniki)} wpisów, dopisano {dopisane} nowych słów Tomasza.")
    _wyczysc_awarie()  # udany cykl kasuje licznik kolejnych awarii
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    tryb = parser.add_mutually_exclusive_group(required=True)
    tryb.add_argument("--raz", action="store_true", help="jedno odpytanie Telegrama")
    tryb.add_argument("--petla", type=float, metavar="N", help="odpytuj co N sekund")
    args = parser.parse_args()

    if args.petla is not None and args.petla <= 0:
        parser.error("N dla --petla musi być większe od zera")

    if args.raz:
        uruchom_ucho()
        return 0

    try:
        while True:
            uruchom_ucho()
            time.sleep(args.petla)
    except KeyboardInterrupt:
        print("Hans ucho: zatrzymane.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
