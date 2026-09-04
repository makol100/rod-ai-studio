"""Auto-usuwanie ogloszen z tablicy po 7 dniach od publikacji (cron codziennie). Przebudowuje strone jesli cos usunieto."""
import json, os, subprocess, shutil, datetime
from pathlib import Path
ROOT = Path("/root/rod-ai-studio"); WWW = ROOT / "www_rod"; WOLUMEN = Path("/var/lib/docker/volumes/caddy_mcp_data/_data/www_rod")
PUBL = WWW / "content/tablica.json"; DNI = 7
def main():
    try: dane = json.loads(PUBL.read_text(encoding="utf-8"))
    except Exception: return
    if not isinstance(dane, list) or not dane: return
    granica = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))) - datetime.timedelta(days=DNI)
    zostaje = []
    for o in dane:
        try: d = datetime.datetime.fromisoformat(o.get("date", ""))
        except Exception: d = None
        if d and d >= granica: zostaje.append(o)
    if len(zostaje) == len(dane): print("tablica: nic do usuniecia"); return
    usuniete = len(dane) - len(zostaje)
    PUBL.write_text(json.dumps(zostaje, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run(["python3", "build.py"], cwd=WWW, capture_output=True, text=True)
    if r.returncode != 0: print("build blad:", r.stderr[-200:]); return
    tmp = WOLUMEN.with_name("www_rod.new"); shutil.rmtree(tmp, ignore_errors=True); shutil.copytree(WWW / "dist", tmp)
    for p in tmp.rglob("*"): os.chmod(p, 0o755 if p.is_dir() else 0o644)
    old = WOLUMEN.with_name("www_rod.old"); shutil.rmtree(old, ignore_errors=True)
    if WOLUMEN.exists(): WOLUMEN.rename(old)
    tmp.rename(WOLUMEN); shutil.rmtree(old, ignore_errors=True)
    subprocess.run(["python3", str(ROOT / "tools/pogoda_rod.py")], capture_output=True)
    subprocess.run(["git", "-C", str(ROOT), "add", "-A", "www_rod/content/tablica.json"], capture_output=True)
    subprocess.run(["git", "-C", str(ROOT), "commit", "--no-verify", "-qm", f"Tablica: auto-usuniete {usuniete} ogloszen (>7 dni)"], capture_output=True)
    print(f"tablica: usunieto {usuniete} ogloszen starszych niz {DNI} dni")
if __name__ == "__main__": main()
