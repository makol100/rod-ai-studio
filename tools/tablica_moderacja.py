"""Moderacja tablicy ogloszen — BEZ fastapi (uzywane przez ucho Hansa gdy Tomasz klika TAK/NIE).
obsluz_callback(data) -> komunikat. Wspoldzieli pliki z apps/api/src/tablica_rod.py."""
import json, os, subprocess, shutil, datetime
from pathlib import Path
ROOT = Path("/root/rod-ai-studio"); WWW = ROOT / "www_rod"; WOLUMEN = Path("/var/lib/docker/volumes/caddy_mcp_data/_data/www_rod")
OCZEK = ROOT / "data/tablica/oczekujace.json"; PUBL = WWW / "content/tablica.json"
def _wczytaj(p, d):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return d
def _zbuduj():
    r = subprocess.run(["python3", "build.py"], cwd=WWW, capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(r.stderr[-300:])
    tmp = WOLUMEN.with_name("www_rod.new"); shutil.rmtree(tmp, ignore_errors=True); shutil.copytree(WWW / "dist", tmp)
    for p in tmp.rglob("*"): os.chmod(p, 0o755 if p.is_dir() else 0o644)
    old = WOLUMEN.with_name("www_rod.old"); shutil.rmtree(old, ignore_errors=True)
    if WOLUMEN.exists(): WOLUMEN.rename(old)
    tmp.rename(WOLUMEN); shutil.rmtree(old, ignore_errors=True)
    subprocess.run(["python3", str(ROOT / "tools/pogoda_rod.py")], capture_output=True)
def obsluz_callback(data: str) -> str:
    akcja, _, oid = data.partition(":")
    ocz = _wczytaj(OCZEK, []); cel = next((x for x in ocz if x["id"] == oid), None)
    if not cel: return "To ogłoszenie już obsłużone."
    ocz = [x for x in ocz if x["id"] != oid]
    OCZEK.write_text(json.dumps(ocz, ensure_ascii=False, indent=1), encoding="utf-8"); os.chmod(OCZEK, 0o600)
    if akcja == "tab_nie":
        return f"❌ Odrzucone: {cel['tytul']}"
    dane = _wczytaj(PUBL, []); teraz = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
    dane.insert(0, {"id": cel["id"], "kategoria": cel["kategoria"], "tytul": cel["tytul"], "tresc": cel["tresc"],
                    "kontakt": cel.get("kontakt", ""), "imie": cel.get("imie", ""), "dzialka": cel.get("dzialka", ""),
                    "date": teraz.isoformat(timespec="minutes"), "display_date": teraz.strftime("%d.%m.%Y")})
    dane = dane[:60]; PUBL.write_text(json.dumps(dane, ensure_ascii=False, indent=1), encoding="utf-8")
    try:
        _zbuduj()
        subprocess.run(["git", "-C", str(ROOT), "add", "-A", "www_rod/content/tablica.json"], capture_output=True)
        subprocess.run(["git", "-C", str(ROOT), "commit", "--no-verify", "-qm", f"Tablica: zatwierdzone ({cel['tytul'][:40]})"], capture_output=True)
    except Exception as e: return f"Zatwierdzone, ale blad publikacji: {str(e)[:150]}"
    return f"✅ Opublikowane na tablicy: {cel['tytul']}"
if __name__ == "__main__":
    import sys; print(obsluz_callback(sys.argv[1]) if len(sys.argv) > 1 else "podaj data")
