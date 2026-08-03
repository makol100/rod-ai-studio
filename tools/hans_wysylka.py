import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def wyslij_do_tomasza(raport: dict[str, Any]) -> bool:
    """Wysyła raport na Telegram do Tomasza, jeśli jest ALERT, stosując limit."""
    if raport.get("poziom") != "ALERT":
        return False

    czesci = ["⚠️ HANS WYKRYŁ POMINIĘCIA KLAUDKA"]
    bledy = raport.get("bledy_wejscia", [])
    if bledy:
        czesci.append("\n❌ BŁĘDY WEJŚCIA:")
        for b in bledy:
            czesci.append(f"- {b}")
            
    przemilczane = raport.get("przemilczane", [])
    if przemilczane:
        czesci.append("\n🤐 PRZEMILCZANE PRZEZ KLAUDKA:")
        for p in przemilczane:
            plik_nazwa = Path(p.get("plik", "nieznany")).name
            czesci.append(f"[{p.get('marker')}] {plik_nazwa}:{p.get('linia', '?')}")
            czesci.append(f"„{p.get('cytat', '')}”")
            
    tresc = "\n".join(czesci)

    token = id_czatu = ""
    try:
        with open("/home/hermes/.hermes/.env", encoding="utf-8", errors="replace") as f:
            for linia in f:
                klucz, _, wartosc = linia.strip().partition("=")
                wartosc = wartosc.strip().strip('"').strip("'")
                if klucz == "HANS_BOT_TOKEN":
                    token = wartosc
                elif klucz == "HANS_CHAT_ID":
                    id_czatu = wartosc
    except OSError as e:
        print(f"[hans] Nie udało się odczytać konfiguracji: {e}")
        return False

    if not token or not id_czatu:
        print("[hans] Brak HANS_BOT_TOKEN lub HANS_CHAT_ID w konfiguracji.")
        return False

    plik_limitu = Path(".scratch/hans/limit.jsonl")
    teraz_ts = datetime.now(timezone.utc).timestamp()
    
    try:
        plik_limitu.parent.mkdir(parents=True, exist_ok=True)
        if plik_limitu.exists():
            linie = plik_limitu.read_text(encoding="utf-8").splitlines()
            wyslane_w_godzinie = 0
            for linia in reversed(linie):
                if not linia.strip():
                    continue
                try:
                    wpis = json.loads(linia)
                    if teraz_ts - wpis.get("ts", 0) <= 3600:
                        if wpis.get("sukces") or wpis.get("wstrzymane"):
                            wyslane_w_godzinie += 1
                    else:
                        break
                except (json.JSONDecodeError, ValueError):
                    continue
            
            if wyslane_w_godzinie >= 3:
                print("[hans] Limit wysyłek (3/h) przekroczony. Raport wstrzymany.")
                with plik_limitu.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({"ts": teraz_ts, "wstrzymane": True}) + "\n")
                return False
    except OSError as e:
        print(f"[hans] Błąd obsługi pliku limitu: {e}")

    dane = urllib.parse.urlencode({
        "chat_id": id_czatu,
        "text": tresc[:4000],
        "disable_web_page_preview": "true",
    }).encode()
    adres = f"https://api.telegram.org/bot{token}/sendMessage"
    
    ok = False
    powod = ""
    try:
        req = urllib.request.Request(adres, data=dane)
        with urllib.request.urlopen(req, timeout=15) as o:
            odp = json.loads(o.read().decode("utf-8"))
        ok = bool(odp.get("ok"))
        if not ok:
            powod = f"Błąd API: {odp.get('description')}"
    except urllib.error.HTTPError as e:
        powod = f"HTTP {e.code}: {e.read()[:200].decode(errors='replace')}"
    except Exception as e:
        powod = f"{type(e).__name__}: {str(e)[:150]}"

    if not ok:
        print(f"[hans] Nie udało się wysłać na Telegram: {powod}")
        
    try:
        with plik_limitu.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": teraz_ts, "sukces": ok, "powod": powod}) + "\n")
    except OSError:
        pass

    return ok
