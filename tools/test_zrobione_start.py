#!/usr/bin/env python3
"""test_zrobione_start.py — czy bramka wykrywa nieudany start zalogi i przekazuje --mimo-braku.

POWSTAL 19.08.2026, bo Zenek slusznie odrzucil zgloszenie: jako dowodu uzylem
tools/test_bramki.py, ktory testuje CO INNEGO (tools/bramka_henia.py). Test musi
sprawdzac dokladnie to, co sie twierdzi — inaczej jest tylko dekoracja.

Sprawdza dwie naprawy z 19.08:
  1. pytaj_zaloge() przekazuje --mimo-braku do zaloga.py.
     Bez tego zaloga konczy kodem 2 (sonda zdolnosci sprawdza takze Genka, ktory jest
     WYLACZONY decyzja Tomasza) i kontrola NIGDY nie startuje. Objaw przed naprawa:
     bramka pokazywala "GLOS NIEODEBRANY" dla obu, choc nikt ich nie pytal.
  2. niezerowy returncode zalogi = SPRZECIW, z komunikatem "KONTROLA NIE WYSTARTOWALA".

Uruchomienie: python3 tools/test_zrobione_start.py   (kod 0 = zielone)
"""
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import zrobione  # noqa: E402

bledy = []
zrodlo = inspect.getsource(zrobione.pytaj_zaloge)

# --- 1. --mimo-braku faktycznie w wywolaniu zaloga.py ---
if "--mimo-braku" not in zrodlo:
    bledy.append("pytaj_zaloge NIE przekazuje --mimo-braku — kontrola nie wystartuje (kod 2)")
else:
    # musi byc w TEJ SAMEJ liscie argumentow co zaloga.py, nie w komentarzu obok
    # UWAGA: "zaloga.py" pada tez w opisie funkcji — szukamy WYWOLANIA, czyli
    # ostatniego wystapienia, i sprawdzamy, czy flaga jest w tej samej liscie argumentow.
    i_zaloga = zrodlo.rfind('"zaloga.py"')
    i_flaga = zrodlo.rfind("--mimo-braku")
    if i_zaloga == -1 or i_flaga == -1 or not (0 < i_flaga - i_zaloga < 400):
        bledy.append("--mimo-braku nie jest w wywolaniu zaloga.py (odleglosc poza zakresem)")

# --- 2. niezerowy returncode ustawia sprzeciw ---
if "w.returncode != 0" not in zrodlo:
    bledy.append("brak sprawdzenia returncode zalogi — nieudany start przechodzi niezauwazony")
else:
    i_rc = zrodlo.find("w.returncode != 0")
    ogon = zrodlo[i_rc:i_rc + 500]
    if "sprzeciw = True" not in ogon:
        bledy.append("returncode != 0 NIE ustawia sprzeciwu")
    if "NIE WYSTARTOWALA" not in ogon:
        bledy.append("brak czytelnego komunikatu o nieudanym starcie")

# --- 3. nieodebrany glos nadal blokuje (naprawa z rana, nie moge jej cofnac) ---
if 'if "NIEODEBRANY" in " ".join(glosy):' not in zrodlo:
    bledy.append("cofnieto naprawe: NIEODEBRANY znow nie blokuje bezwarunkowo")

# --- 4. uruchom_test zwraca 3 wartosci na KAZDEJ sciezce (bez tego bramka sie wywala) ---
for arg, opis in (("/tmp/na_pewno_nie_ma_takiego_pliku_19_08.py", "plik nie istnieje"),
                  ("tools/test_straznik.py", "plik istnieje")):
    w = zrobione.uruchom_test(arg)
    if not isinstance(w, tuple) or len(w) != 3:
        bledy.append(f"uruchom_test({opis}) zwrocil {len(w) if isinstance(w, tuple) else '?'} wartosci zamiast 3")

# --- 5. test podany jako CALE POLECENIE ma byc odrzucony jako nieistniejacy ---
# (19.08: podawalem "python3 tools/test_straznik.py" i bramka szukala pliku o tej nazwie)
zielony, opis, _ = zrobione.uruchom_test("python3 tools/test_straznik.py")
if zielony:
    bledy.append("cale polecenie zamiast sciezki zostalo uznane za zielony test")

if bledy:
    print(f"CZERWONE — {len(bledy)}:")
    for b in bledy:
        print(f"  - {b}")
    sys.exit(1)
print("PETLA ZIELONA — 5 sprawdzen: --mimo-braku w wywolaniu, returncode=sprzeciw, "
      "komunikat o starcie, NIEODEBRANY blokuje, uruchom_test zwraca 3 wartosci")
