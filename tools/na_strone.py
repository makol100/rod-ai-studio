#!/usr/bin/env python3
"""Dodaje opublikowany na FB film (Reel) TAKZE na rodwozniki.pl — sekcja 'Z zycia ogrodu' (Filmy FB).
Uzycie: python3 tools/na_strone.py <video_id> <sciezka_wideo> "<opis>"
Robi: miniature z wideo -> www_rod/static/img/fb/, wpis w www_rod/content/fb_filmy.json -> build -> wolumen Caddy.
Idempotentne: ten sam video_id nie duplikuje sie."""
import sys, os, json, subprocess, shutil, datetime, re
ROOT = "/root/rod-ai-studio"; WWW = f"{ROOT}/www_rod"; WOLUMEN = "/var/lib/docker/volumes/caddy_mcp_data/_data/www_rod"
DANE = f"{WWW}/content/fb_filmy.json"
def main():
    if len(sys.argv) < 3:
        print("uzycie: na_strone.py <video_id> <plik_wideo> [opis]"); sys.exit(1)
    vid = sys.argv[1].strip(); plik = sys.argv[2]; opis = (sys.argv[3] if len(sys.argv) > 3 else "").strip()
    if not vid or not os.path.isfile(plik): print("brak video_id lub pliku"); sys.exit(1)
    # tytul = pierwsza linia opisu, bez hasztagow
    tytul = ""
    for l in (opis or "").splitlines():
        l = re.sub(r"#\w+", "", l).strip()
        if l: tytul = l[:90]; break
    tytul = tytul or "Nowy film z ogrodu"
    # miniatura: kadr ~1.5s
    os.makedirs(f"{WWW}/static/img/fb", exist_ok=True)
    thumb = f"fb_{vid}.jpg"; dst = f"{WWW}/static/img/fb/{thumb}"
    if not os.path.isfile(dst):
        subprocess.run(["ffmpeg","-v","error","-y","-ss","1.5","-i",plik,"-vframes","1","-vf","scale=720:-2","-q:v","3",dst], check=False)
    # wpis
    try: dane = json.load(open(DANE, encoding="utf-8"))
    except Exception: dane = []
    if any(d.get("video_id") == vid for d in dane):
        print("juz jest na stronie:", vid); return
    teraz = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
    dane.insert(0, {"video_id": vid, "title": tytul, "opis": opis[:400], "thumb": thumb if os.path.isfile(dst) else "",
                    "link": f"https://www.facebook.com/reel/{vid}", "date": teraz.isoformat(timespec="minutes"), "display_date": teraz.strftime("%d.%m.%Y")})
    dane = dane[:24]  # trzymaj max 24 najnowsze
    json.dump(dane, open(DANE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # build + wystaw
    r = subprocess.run(["python3","build.py"], cwd=WWW, capture_output=True, text=True)
    if r.returncode != 0: print("BUILD BLAD:", r.stderr[-300:]); sys.exit(2)
    tmp = WOLUMEN + ".new"; shutil.rmtree(tmp, ignore_errors=True); shutil.copytree(f"{WWW}/dist", tmp)
    for p in __import__("pathlib").Path(tmp).rglob("*"): os.chmod(p, 0o755 if p.is_dir() else 0o644)
    old = WOLUMEN + ".old"; shutil.rmtree(old, ignore_errors=True)
    if os.path.exists(WOLUMEN): os.rename(WOLUMEN, old)
    os.rename(tmp, WOLUMEN); shutil.rmtree(old, ignore_errors=True)
    subprocess.run(["python3", f"{ROOT}/tools/pogoda_rod.py"], capture_output=True)
    subprocess.run(["git","-C",ROOT,"add","-A","www_rod/content/fb_filmy.json","www_rod/static/img/fb"], capture_output=True)
    subprocess.run(["git","-C",ROOT,"commit","--no-verify","-qm",f"Auto: film z FB na strone ({tytul[:40]})"], capture_output=True)
    print("DODANO NA STRONE:", tytul, "->", f"https://rodwozniki.pl/filmy/")
if __name__ == "__main__": main()
