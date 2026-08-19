#!/usr/bin/env python3
"""straznik_komend.py — PreToolUse hook Claude Code: blokuje katastrofalne komendy.

POWOD (17.08.2026): narada Zenka i Henia nad filmem Szewczyka. Metoda z paczki
davidondrej/skills (hooks/deny-dangerous.sh) — jedyna pozycja z filmu, ktorej NIE
mamy u siebie. Bierzemy METODE, nie cudzy kod: 48 skilli z obcego repo na VPS
z poswiadczeniami (kamery, NVR, Telegram, Gemini) to za duza powierzchnia ataku.

CZYM SIE ROZNIMY OD ORYGINALU (obie wady wskazane przez zaloge):
1. ORYGINAL: fail-OPEN — brak jq / brak pliku wzorcow / nieodczytana komenda = PRZEPUSC.
   U NAS: fail-CLOSED — czego nie umiem odczytac, tego nie przepuszczam. Na VPS
   z poswiadczeniami blad ma isc w strone bezpieczenstwa. (jq na tym VPS NIE MA
   w ogole — sprawdzone 17.08 — wiec zero zaleznosci zewnetrznych: czysty Python.)
2. ORYGINAL: wzorce macOS-centryczne (diskutil, brew, security, keychain) — u nas
   Linux, wiec martwe. U NAS: wzorce pod Linux + NASZE sciezki (skrytka, repo, klucze).

CZYM TO NIE JEST (uczciwie, za autorem oryginalu):
To PAS BEZPIECZENSTWA przeciw wypadkowi, NIE piaskownica przeciw zlosliwemu agentowi.
Komenda ukryta (np. python -c z shutil.rmtree) przejdzie. Regex nie zastapi izolacji.

KONTRAKT Claude Code: na stdin JSON z tool_input.command; wyjscie 2 = BLOKADA
(powod na stderr trafia do modelu), wyjscie 0 = przepusc.

Test: python3 tools/test_straznik.py
"""
import json
import re
import sys

# Kazdy wzorzec: (regex, po co to blokujemy). Regex liczy sie na CALEJ komendzie.
WZORCE = [
    # --- kasowanie systemu i katalogow domowych
    (r"\brm\s+(-[a-zA-Z]*\s+)*-?[a-zA-Z]*[rR][a-zA-Z]*[fF]|\brm\s+(-[a-zA-Z]*\s+)*-?[a-zA-Z]*[fF][a-zA-Z]*[rR]",
     "rm -rf — kasowanie rekurencyjne bez pytania"),
    (r"\brm\b[^|;&]*\s(/|~|\$HOME|/root|/etc|/var|/usr|/boot)(\s|/\*|$)",
     "rm na katalogu systemowym albo domowym"),
    (r":\(\)\s*\{\s*:\|:&\s*\}\s*;\s*:", "bomba fork — zawiesza maszyne"),
    # --- niszczenie dyskow
    (r"\bmkfs(\.\w+)?\b", "mkfs — formatowanie systemu plikow"),
    (r"\bdd\b[^|;&]*\bof=\s*/dev/(sd|nvme|vd|hd)", "dd na surowy dysk — nadpisuje nosnik"),
    (r"\b(shred|wipefs)\b[^|;&]*/dev/", "shred/wipefs na urzadzeniu blokowym"),
    (r">\s*/dev/(sd|nvme|vd|hd)\w+", "przekierowanie na surowy dysk"),
    # --- pobierz-i-uruchom (najczestsza droga wejscia zlosliwego kodu)
    (r"\b(curl|wget)\b[^|]*\|\s*(sudo\s+)?(ba|z|k|)sh\b", "curl/wget | sh — uruchamianie kodu prosto z sieci"),
    (r"\b(curl|wget)\b[^|]*\|\s*(sudo\s+)?(python|perl|ruby|node)\b", "pobranie i uruchomienie skryptu z sieci"),
    # --- nasze sekrety i tozsamosc maszyny
    (r"/root/\.sekrety", "dotyka skrytki z poswiadczeniami"),
    (r"\.ssh/(id_\w+|authorized_keys)\b(?![^|;&]*\bssh-keygen -l)", "dotyka kluczy SSH"),
    (r"\b(cat|cp|scp|curl|tar|base64)\b[^|;&]*\.(env|pem|key)\b", "wynosi plik z poswiadczeniami"),
    (r"tailscale\s+(logout|down|set\s+--exit-node=\S)",
     "tailscale logout/down/exit-node — 17.08 to odcielo fabryke od swiata (D-0098)"),
    # --- niszczenie historii pracy
    (r"\bgit\s+push\b[^|;&]*(--force(?!-with-lease)|-f)\b",
     "git push --force — nadpisuje historie zdalna"),
    (r"\bgit\s+reset\s+--hard\b[^|;&]*\b(origin/|HEAD~)", "git reset --hard na cudzy stan"),
    (r"\bgit\s+(clean\s+-[a-zA-Z]*[xX]?[a-zA-Z]*d|reflog\s+expire|gc\s+--prune=now)",
     "kasowanie niezacommitowanej pracy albo refloga"),
    (r"\brm\b[^|;&]*\.git(\s|/|$)", "kasowanie repozytorium git"),
    # --- system
    (r"\b(shutdown|halt|poweroff)\b", "wylaczenie maszyny"),
    (r"\bchmod\s+(-R\s+)?777\s+(/|/etc|/root|/var)(\s|$)", "chmod 777 na katalogu systemowym"),
    (r"\bchown\b[^|;&]*\s+(/|/etc|/root)(\s|$)", "chown na katalogu systemowym"),
    (r"\b(userdel|groupdel)\b", "kasowanie konta uzytkownika"),
    (r"\bdocker\s+(system\s+prune\s+-[a-zA-Z]*a|volume\s+rm)", "kasowanie danych kontenerow"),
    (r"\btruncate\s+-s\s*0\b", "zerowanie pliku w miejscu"),
]

SKOMPILOWANE = [(re.compile(w, re.IGNORECASE), p) for w, p in WZORCE]


# Komendy, ktore WYGLADAJA grozne, a sa zwyklym odczytem. Sprawdzane PRZED wzorcami.
BIALA_LISTA = [
    re.compile(r"^\s*ssh-keygen\s+-l\b"),        # odcisk klucza — tylko czyta
    re.compile(r"^\s*ls\s+-l[a-zA-Z]*\s+[^|;&]*\.ssh"),  # listing katalogu kluczy
]


def sprawdz(komenda: str):
    """Zwraca powod blokady albo None. Wydzielone, zeby test mogl wolac wprost."""
    if not isinstance(komenda, str) or not komenda.strip():
        return None
    for wyjatek in BIALA_LISTA:
        if wyjatek.search(komenda):
            return None
    for regex, powod in SKOMPILOWANE:
        if regex.search(komenda):
            return powod
    return None


DZIENNIK = "/root/.straznik_dziennik.jsonl"


def zapisz_slad(komenda: str, decyzja: str) -> None:
    """Slad wywolania — dowod, ze hook faktycznie byl wolany, a nie tylko wpisany w settings."""
    try:
        import datetime
        wpis = {"czas": datetime.datetime.now().isoformat(timespec="seconds"),
                "decyzja": decyzja, "komenda": (komenda or "")[:300]}
        # 19.08: rotacja — bez niej dziennik rosl bez konca (tempo ~139 wpisow/dobe,
        # czyli ~5 MB rocznie). Przy 5 MB przenosimy do .1 i zaczynamy nowy;
        # jedna poprzednia generacja zostaje, starsza jest nadpisywana.
        import os as _os
        try:
            if _os.path.exists(DZIENNIK) and _os.path.getsize(DZIENNIK) > 5 * 1024 * 1024:
                _os.replace(DZIENNIK, DZIENNIK + ".1")
        except OSError:
            pass  # rotacja nigdy nie moze zablokowac zapisu ani pracy
        with open(DZIENNIK, "a", encoding="utf-8") as f:
            f.write(json.dumps(wpis, ensure_ascii=False) + "\n")
    except Exception:
        pass  # dziennik nigdy nie moze zablokowac pracy


def main():
    # FAIL-CLOSED: kazdy blad odczytu = blokada. Odwrotnie niz oryginal.
    try:
        surowe = sys.stdin.read()
    except Exception:
        print("STRAZNIK: nie odczytalem wejscia — blokuje (fail-closed).", file=sys.stderr)
        sys.exit(2)

    if not surowe.strip():
        zapisz_slad("(puste wejscie)", "przepusc")
        sys.exit(0)  # brak wejscia = nie ma czego blokowac (hook wolany na sucho)

    try:
        dane = json.loads(surowe)
    except json.JSONDecodeError:
        zapisz_slad("(wejscie nie jest JSON)", "BLOKADA")
        print("STRAZNIK: wejscie nie jest poprawnym JSON — blokuje (fail-closed).", file=sys.stderr)
        sys.exit(2)

    # Cala struktura musi byc slownikiem — inaczej nie umiem jej ocenic.
    if not isinstance(dane, dict):
        zapisz_slad(f"(wejscie typu {type(dane).__name__})", "BLOKADA")
        print(f"STRAZNIK: wejscie nie jest obiektem JSON (typ: {type(dane).__name__}) "
              f"— blokuje (fail-closed).", file=sys.stderr)
        sys.exit(2)

    narzedzie = dane.get("tool_name") or dane.get("tool") or ""
    if not isinstance(narzedzie, str):
        zapisz_slad(f"(tool_name typu {type(narzedzie).__name__})", "BLOKADA")
        print(f"STRAZNIK: tool_name nie jest tekstem (typ: {type(narzedzie).__name__}) "
              f"— blokuje (fail-closed).", file=sys.stderr)
        sys.exit(2)

    wejscie = dane.get("tool_input")
    if wejscie is None:
        wejscie = {}
    if not isinstance(wejscie, dict):
        zapisz_slad(f"(tool_input typu {type(wejscie).__name__})", "BLOKADA")
        print(f"STRAZNIK: tool_input nie jest obiektem (typ: {type(wejscie).__name__}) "
              f"— blokuje (fail-closed).", file=sys.stderr)
        sys.exit(2)
    if narzedzie and narzedzie.lower() not in ("bash", "shell", "run_command"):
        zapisz_slad(f"(narzedzie: {narzedzie})", "przepusc-nie-powloka")
        sys.exit(0)  # nie komenda powloki — nie nasza sprawa

    komenda = wejscie.get("command")
    if komenda is None:
        # Bash bez pola command = nie umiem ocenic -> blokuje
        if narzedzie.lower() in ("bash", "shell", "run_command"):
            zapisz_slad("(brak pola command)", "BLOKADA")
            print("STRAZNIK: brak pola command w tool_input — blokuje (fail-closed).", file=sys.stderr)
            sys.exit(2)
        sys.exit(0)

    # 19.08 NAPRAWA (znalazl Zenek przy audycie Octopa): komenda o typie INNYM NIZ TEKST
    # (lista, slownik, liczba) PRZECHODZILA — bo sprawdz() ma isinstance(komenda, str)
    # i dla nie-tekstu zwracalo None, czyli "czysto". Teraz: czego nie umiem odczytac
    # jako tekst, tego nie przepuszczam.
    if not isinstance(komenda, str):
        zapisz_slad(f"(typ {type(komenda).__name__}) {str(komenda)[:200]}", "BLOKADA")
        print(f"STRAZNIK: pole command nie jest tekstem (typ: {type(komenda).__name__}) "
              f"— blokuje (fail-closed).", file=sys.stderr)
        sys.exit(2)

    powod = sprawdz(komenda)
    zapisz_slad(komenda, "BLOKADA" if powod else "przepusc")
    if powod:
        print(f"STRAZNIK ZABLOKOWAL: {powod}\n"
              f"Komenda: {komenda[:200]}\n"
              f"To pas bezpieczenstwa fabryki (tools/straznik_komend.py). Jesli naprawde tego "
              f"chcesz — powiedz Tomaszowi i zrob to swiadomie, recznie.", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    # Siatka bezpieczenstwa: Claude Code blokuje TYLKO przy kodzie 2. Kazdy nieprzewidziany
    # wyjatek dawalby kod 1 = PRZEPUSZCZENIE. Tego nie chcemy na maszynie z poswiadczeniami.
    try:
        main()
    except SystemExit:
        raise
    except BaseException as e:  # noqa: BLE001
        try:
            zapisz_slad(f"(wyjatek {type(e).__name__})", "BLOKADA")
        except Exception:  # noqa: BLE001
            pass
        print(f"STRAZNIK: nieprzewidziany blad ({type(e).__name__}) — blokuje (fail-closed).",
              file=sys.stderr)
        sys.exit(2)
