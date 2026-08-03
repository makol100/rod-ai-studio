#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HANS - OCZY (tools/hans_oczy.py)
Widzi, co się zmieniło w repo od poprzedniego uruchomienia w katalogach wiedza/ i tools/.
Wykrywa wzorzec niedokończonego śladu Klaudka.
"""

import os
import sys
import json
import hashlib
from datetime import datetime

SCIEZKA_OCZY = ".scratch/hans/oczy.jsonl"

def oblicz_stan_plikow() -> dict:
    """Skanuje katalogi wiedza/ i tools/ i oblicza ich aktualny stan."""
    stan = {}
    katalogi = ["wiedza", "tools"]
    for kat in katalogi:
        if not os.path.exists(kat):
            continue
        for root, dirs, files in os.walk(kat):
            # Pomijamy __pycache__ i ukryte katalogi
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
            for file in files:
                if file.startswith(".") or file.endswith(".pyc") or file.endswith("~"):
                    continue
                
                sciezka = os.path.join(root, file)
                # Ujednolicamy ukośniki na systemach unix-podobnych/windows
                sciezka_norm = sciezka.replace("\\", "/")
                
                try:
                    stat = os.stat(sciezka)
                    mtime = stat.st_mtime
                    
                    # Liczenie sumy kontrolnej SHA-256
                    with open(sciezka, "rb") as f:
                        checksum = hashlib.sha256(f.read()).hexdigest()
                        
                    stan[sciezka_norm] = {
                        "mtime": mtime,
                        "checksum": checksum
                    }
                except OSError as e:
                    print(f"Ostrzeżenie przy odczycie pliku {sciezka}: {e}", file=sys.stderr)
                    # Istniejący, ale nieczytelny plik nie może udawać usuniętego.
                    stan[sciezka_norm] = {
                        "mtime": os.path.getmtime(sciezka),
                        "checksum": None,
                        "read_error": str(e),
                    }
    return stan

def wczytaj_poprzedni_stan() -> dict:
    """Odtwarza ostatni znany stan plików z append-only logu oczy.jsonl."""
    stan = {}
    if os.path.exists(SCIEZKA_OCZY):
        try:
            with open(SCIEZKA_OCZY, "r", encoding="utf-8") as f:
                for linia in f:
                    linia = linia.strip()
                    if not linia:
                        continue
                    try:
                        wpis = json.loads(linia)
                        file_path = wpis.get("file")
                        if file_path:
                            status = wpis.get("status")
                            if status == "deleted":
                                if file_path in stan:
                                    del stan[file_path]
                            else:
                                stan[file_path] = {
                                    "mtime": wpis.get("mtime"),
                                    "checksum": wpis.get("checksum")
                                }
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Błąd odczytu poprzedniego stanu z {SCIEZKA_OCZY}: {e}", file=sys.stderr)
    return stan

def zapisz_zmiany(zmiany: list, timestamp: str):
    """Zapisuje zmiany do logu append-only."""
    os.makedirs(os.path.dirname(os.path.abspath(SCIEZKA_OCZY)), exist_ok=True)
    try:
        with open(SCIEZKA_OCZY, "a", encoding="utf-8") as f:
            for zmiana in zmiany:
                wpis = {
                    "timestamp": timestamp,
                    "file": zmiana["file"],
                    "mtime": zmiana["mtime"],
                    "checksum": zmiana["checksum"],
                    "status": zmiana["status"]
                }
                f.write(json.dumps(wpis, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Błąd zapisu zmian do {SCIEZKA_OCZY}: {e}", file=sys.stderr)

def _powiazane(kod: str, wiedza_plik: str) -> bool:
    """Ostrożna heurystyka: dokument musi wskazywać moduł kodu, nie tylko drgnąć."""
    nazwa = os.path.basename(kod)
    rdzen = os.path.splitext(nazwa)[0]
    try:
        with open(wiedza_plik, encoding="utf-8", errors="replace") as f:
            tekst = f.read().lower()
    except OSError:
        return False
    return kod.lower() in tekst or nazwa.lower() in tekst or rdzen.lower() in tekst

def zapisz_podejrzenie(timestamp: str, rodzaj: str, kod: list, wiedza: list):
    """Dopisuje podejrzenie do tego samego append-only dziennika."""
    wpis = {"timestamp": timestamp, "event": "suspicion", "kind": rodzaj,
            "code_files": kod, "knowledge_files": wiedza}
    with open(SCIEZKA_OCZY, "a", encoding="utf-8") as f:
        f.write(json.dumps(wpis, ensure_ascii=False) + "\n")

def czy_plik_kodu(sciezka: str) -> bool:
    """Sprawdza, czy plik jest produkcyjnym plikiem kodu w tools/."""
    if not sciezka.startswith("tools/"):
        return False
    nazwa = os.path.basename(sciezka)
    if not (nazwa.endswith(".py") or nazwa.endswith(".sh")):
        return False
    # Ignorujemy pliki testowe
    if "test" in nazwa.lower():
        return False
    return True

def czy_plik_wiedzy(sciezka: str) -> bool:
    """Sprawdza, czy plik jest plikiem wiedzy w wiedza/."""
    if not sciezka.startswith("wiedza/"):
        return False
    return sciezka.endswith(".md")

def main():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Pobieramy poprzedni i obecny stan
    poprzedni_stan = wczytaj_poprzedni_stan()
    obecny_stan = oblicz_stan_plikow()
    
    # 2. Porównujemy i wykrywamy różnice
    zmiany = []
    
    # Wykrywanie zmodyfikowanych i dodanych
    for plik, dane in obecny_stan.items():
        if plik not in poprzedni_stan:
            zmiany.append({
                "file": plik,
                "mtime": dane["mtime"],
                "checksum": dane["checksum"],
                "status": "added"
            })
        else:
            poprz = poprzedni_stan[plik]
            # Zmiana checksumy lub mtime oznacza modyfikację
            if poprz["checksum"] != dane["checksum"] or poprz["mtime"] != dane["mtime"]:
                zmiany.append({
                    "file": plik,
                    "mtime": dane["mtime"],
                    "checksum": dane["checksum"],
                    "status": "modified"
                })
                
    # Wykrywanie usuniętych
    for plik in poprzedni_stan:
        if plik not in obecny_stan:
            zmiany.append({
                "file": plik,
                "mtime": 0.0,
                "checksum": "",
                "status": "deleted"
            })
            
    # 3. Jeśli są zmiany, zapisujemy je
    if zmiany:
        zapisz_zmiany(zmiany, now_str)
        
    # 4. Wyświetlanie wyników skanowania
    print(f"=== HANS OCZY — SKAN {now_str} ===")
    if not poprzedni_stan:
        print(f"Inicjalizacja: Wykryto {len(zmiany)} plików (utworzono stan początkowy).")
    else:
        if zmiany:
            print(f"Wykryto {len(zmiany)} zmian od poprzedniego uruchomienia:")
            for z in zmiany:
                print(f"  [{z['status'].upper()}] {z['file']}")
        else:
            print("Brak zmian w monitorowanych katalogach od poprzedniego uruchomienia.")
            
    # 5. Analiza wzorca NIEDOKOŃCZONEGO ŚLADU Klaudka
    # Analizujemy wyłącznie zmiany w obecnym uruchomieniu (lub w ogóle jeśli to inicjalizacja,
    # ale przy inicjalizacji podejrzenie nie ma sensu merytorycznego, więc tylko przy kolejnych skanach)
    if poprzedni_stan and zmiany:
        zmieniony_kod = [z["file"] for z in zmiany if czy_plik_kodu(z["file"])]
        zmieniona_wiedza = [z["file"] for z in zmiany if czy_plik_wiedzy(z["file"])]
        powiazania = [(k, w) for k in zmieniony_kod for w in zmieniona_wiedza
                      if _powiazane(k, w)]
        
        if zmieniony_kod and not powiazania:
            zapisz_podejrzenie(now_str, "tools_bez_powiazanej_wiedzy", zmieniony_kod, zmieniona_wiedza)
            print("\n⚠️  [ALARM - PODEJRZENIE] WZORZEC NIEDOKOŃCZONEGO ŚLADU KLAUDKA!")
            print("  Wykryto modyfikację plików kodu w tools/, ale BRAK zmian w wiedzy (wiedza/).")
            print("  Zmienione pliki kodu:")
            for zk in zmieniony_kod:
                print(f"    - {zk}")
            print("  Upewnij się, że odpowiednie zasady i dokumentacja zostały zaktualizowane!")
            
        elif zmieniona_wiedza and not powiazania:
            zapisz_podejrzenie(now_str, "wiedza_bez_powiazanego_kodu", zmieniony_kod, zmieniona_wiedza)
            print("\n⚠️  [ALARM - PODEJRZENIE] WZORZEC NIEDOKOŃCZONEGO ŚLADU KLAUDKA!")
            print("  Wykryto modyfikację plików wiedzy w wiedza/, ale BRAK zmian w kodzie (tools/).")
            print("  Zmienione pliki wiedzy:")
            for zw in zmieniona_wiedza:
                print(f"    - {zw}")
            print("  Upewnij się, że kod odzwierciedla nowe ustalenia lub że zmiana kodu jest planowana!")
        else:
            if zmieniony_kod and zmieniona_wiedza:
                print("\n✅ Spójność zachowana: Zmieniono zarówno kod w tools/, jak i wiedzę w wiedza/.")

if __name__ == "__main__":
    main()
