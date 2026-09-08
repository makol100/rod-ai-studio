#!/usr/bin/env python3
"""Codzienne posty FB 'Ogrodnik ROD' (teksty: powitanie 6:30 + porada 9:00 + ostrzezenia IMGW) -> rodwozniki.pl.
Cron co 30 min. Pobiera przez Graph API, zapisuje www_rod/content/fb_posty.json (max 30), buduje strone gdy nowe."""
import subprocess, json, os, subprocess, shutil, urllib.request, urllib.parse, datetime, re
from pathlib import Path
ROOT = Path("/root/rod-ai-studio"); WWW = ROOT / "www_rod"; WOLUMEN = Path("/var/lib/docker/volumes/caddy_mcp_data/_data/www_rod")
PLIK = WWW / "content/fb_posty.json"; PAGE = "1174205105781401"; V = "v21.0"
OGL_SLOWA = ("ogłaszamy", "ogłoszenie", "komunikat zarząd", "informujemy", "zapraszamy na", "walne zebranie")
def klasyfikuj(tytul: str, msg: str, godzina: int) -> str:
    if "Dzień dobry" in tytul or godzina < 8: return "powitanie"
    if "OSTRZEŻENIE" in msg.upper(): return "ostrzezenie"
    if any(w in msg.lower() for w in OGL_SLOWA): return "ogloszenie"
    return "porada"


HUMOR_SLOWA = ("tomek i janusz", "janusz", "odcinek", "nowa seria startuje")
def _idy_z_folderow(wzor):
    import glob as _g
    idy=set()
    for f in _g.glob(f"/root/rod-ai-studio/data/zarty/{wzor}/opublikowano*"):
        for lin in open(f, encoding="utf-8", errors="ignore"):
            if "video_id=" in lin: idy.add(lin.split("video_id=")[1].split()[0].split("|")[0].strip())
    return idy
WIAD_SLOWA = ("ogłoszenie", "ogłaszamy", "zarząd", "zakończenie sezonu", "wiadomości działkowe", "komunikat")
def pobierz_wideo(tok):
    """Rolki i wiadomosci wideo ze strony FB -> www_rod/content/wideo.json. Zwraca True gdy plik sie zmienil."""
    q = urllib.parse.urlencode({"fields": "id,description,created_time,permalink_url,picture,length,thumbnails{uri,is_preferred}", "limit": 25, "access_token": tok})
    d = json.load(urllib.request.urlopen(f"https://graph.facebook.com/{V}/{PAGE}/videos?{q}", timeout=30))
    wyn = []
    humor_idy = _idy_z_folderow("[0-9]*"); wiad_idy = _idy_z_folderow("awatar*")
    for v in d.get("data", []):
        opis = (v.get("description") or "").strip()
        dl = v.get("length") or 0
        if dl > 150: continue  # dlugie filmy zyja na YouTube, sekcja statyczna
        ct = datetime.datetime.fromisoformat(v["created_time"].replace("+0000", "+00:00")).astimezone(datetime.timezone(datetime.timedelta(hours=2)))
        tytul = next((re.sub(r"#\w+", "", l).strip() for l in opis.splitlines() if l.strip()), "Rolka ROD")[:110]
        if v["id"] in wiad_idy or any(w in opis.lower() for w in WIAD_SLOWA):
            kat = "wiadomosci"
        elif v["id"] in humor_idy or any(w in opis.lower() for w in HUMOR_SLOWA):
            kat = "humor"
        else:
            kat = "rolki"
        link = v.get("permalink_url") or f"/reel/{v['id']}/"
        if link.startswith("/"): link = "https://www.facebook.com" + link  # Graph zwraca sciezki wzgledne
        # miniaturka: najlepszy kadr z thumbnails (picture bywa smieciem ~700 B), cache lokalny bo URL-e fbcdn wygasaja
        thumbs = (v.get("thumbnails") or {}).get("data") or []
        turl = next((t["uri"] for t in thumbs if t.get("is_preferred")), thumbs[0]["uri"] if thumbs else v.get("picture", ""))
        mini = ""
        if turl:
            kat_mini = WWW / "static/wideo"; kat_mini.mkdir(parents=True, exist_ok=True)
            cel = kat_mini / f"{v['id']}.jpg"
            if not cel.is_file() or cel.stat().st_size < 5000:
                try:
                    dane_m = urllib.request.urlopen(urllib.request.Request(turl, headers={"User-Agent": "Mozilla/5.0"}), timeout=20).read()
                    if len(dane_m) > 5000: cel.write_bytes(dane_m)
                except Exception as e: print("miniaturka", v["id"], "blad:", e)
            # czarna miniaturka z FB (rolka jeszcze w obrobce) -> wlasna klatka z lokalnego mp4, gdy jest
            try:
                if cel.is_file():
                    from PIL import Image as _Im, ImageStat as _St
                    if _St.Stat(_Im.open(cel).convert("L")).mean[0] < 8:
                        _mp4 = WWW / f"static/wideo/{v['id']}.mp4"
                        if _mp4.is_file():
                            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "4", "-i", str(_mp4), "-frames:v", "1", "-vf", "scale=720:-2", "-q:v", "3", str(cel)], capture_output=True)
                        else: cel.unlink()
            except Exception as e: print("miniaturka-czarna", v["id"], e)
            if cel.is_file() and cel.stat().st_size >= 5000: mini = f"/static/wideo/{v['id']}.jpg"
        # wlasny plik mp4 (dekret D-0314: filmy graja w oknie na stronie, nie na FB)
        mp4 = WWW / f"static/wideo/{v['id']}.mp4"
        if not mp4.is_file():
            try:
                qs = urllib.parse.urlencode({"fields": "source", "access_token": tok})
                zr = json.load(urllib.request.urlopen(f"https://graph.facebook.com/{V}/{v['id']}?{qs}", timeout=30)).get("source")
                if zr:
                    rq = urllib.request.Request(zr, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(rq, timeout=180) as rr, open(mp4, "wb") as fo:
                        shutil.copyfileobj(rr, fo)
            except Exception as e: print("mp4", v["id"], "blad pobierania:", e)
        wid = f"/static/wideo/{v['id']}.mp4" if mp4.is_file() and mp4.stat().st_size > 200_000 else ""
        wyn.append({"id": v["id"], "tytul": tytul, "kategoria": kat, "link": link, "wideo": wid,
                    "miniaturka": mini, "date": ct.isoformat(timespec="minutes"), "display_date": ct.strftime("%d.%m.%Y")})
    wyn.sort(key=lambda x: x["date"], reverse=True)
    plik = WWW / "content/wideo.json"
    nowy = json.dumps(wyn, ensure_ascii=False, indent=1)
    stary = plik.read_text(encoding="utf-8") if plik.exists() else ""
    if nowy == stary: return False
    plik.write_text(nowy, encoding="utf-8")
    return True

def main():
    tok = (ROOT / "data/.secrets/fb_page_token").read_text().strip()
    q = urllib.parse.urlencode({"fields": "id,created_time,message,status_type,permalink_url", "limit": 40, "access_token": tok})
    d = json.load(urllib.request.urlopen(f"https://graph.facebook.com/{V}/{PAGE}/published_posts?{q}", timeout=30))
    stare = json.loads(PLIK.read_text(encoding="utf-8")) if PLIK.exists() else []
    zmiany = 0
    for x in stare:
        t = klasyfikuj(x.get("tytul",""), x.get("tresc",""), int(x.get("godz","12")[:2] or 12))
        if x.get("typ") != t: x["typ"] = t; zmiany += 1
    najnowszy = max((x["date"] for x in stare), default="")
    znane = {x["id"] for x in stare}
    nowe = []
    for p in d.get("data", []):
        msg = (p.get("message") or "").strip()
        if not msg or p.get("status_type") in ("added_video", "added_photos", "shared_story"): continue  # tylko teksty
        if p["id"] in znane: continue
        ct = datetime.datetime.fromisoformat(p["created_time"].replace("+0000", "+00:00")).astimezone(datetime.timezone(datetime.timedelta(hours=2)))
        # tytul = pierwsza linia bez hasztagow
        if najnowszy and ct.isoformat(timespec="minutes") <= najnowszy: continue  # starsze niz magazyn — juz kiedys ocenione, nie dodawac w kolko
        tytul = next((re.sub(r"#\w+", "", l).strip() for l in msg.splitlines() if l.strip()), "Wpis")[:110]
        typ = klasyfikuj(tytul, msg, ct.hour)
        nowe.append({"id": p["id"], "tytul": tytul, "tresc": msg[:2500], "typ": typ, "link": p.get("permalink_url", f"https://www.facebook.com/{p['id'].replace('_','/posts/')}"),
                     "date": ct.isoformat(timespec="minutes"), "display_date": ct.strftime("%d.%m.%Y"), "godz": ct.strftime("%H:%M")})
    try: wideo_zmiana = pobierz_wideo(tok)
    except Exception as e: wideo_zmiana = False; print("wideo: blad pobierania:", e)
    if not nowe and not zmiany and not wideo_zmiana: print("fb_na_strone: nic nowego"); return
    dane = sorted(nowe + stare, key=lambda x: x["date"], reverse=True)[:30]
    PLIK.write_text(json.dumps(dane, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run(["python3", "build.py"], cwd=WWW, capture_output=True, text=True)
    if r.returncode != 0: print("build blad:", r.stderr[-300:]); return
    tmp = WOLUMEN.with_name("www_rod.new"); shutil.rmtree(tmp, ignore_errors=True); shutil.copytree(WWW / "dist", tmp)
    for p in tmp.rglob("*"): os.chmod(p, 0o755 if p.is_dir() else 0o644)
    old = WOLUMEN.with_name("www_rod.old"); shutil.rmtree(old, ignore_errors=True)
    if WOLUMEN.exists(): WOLUMEN.rename(old)
    tmp.rename(WOLUMEN); shutil.rmtree(old, ignore_errors=True)
    subprocess.run(["python3", str(ROOT / "tools/pogoda_rod.py")], capture_output=True)
    subprocess.run(["python3", str(ROOT / "tools/licznik_rod.py")], capture_output=True)
    subprocess.run(["git", "-C", str(ROOT), "add", "-A", "www_rod/content/fb_posty.json"], capture_output=True)
    subprocess.run(["git", "-C", str(ROOT), "commit", "--no-verify", "-qm", f"Auto: {len(nowe)} postow FB na strone"], capture_output=True)
    print(f"fb_na_strone: nowych {len(nowe)}, przeklasyfikowanych {zmiany}, wideo_zmiana {wideo_zmiana}")
if __name__ == "__main__": main()
