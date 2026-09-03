"""Tablica ogloszen dzialkowcow rodwozniki.pl (dekret Tomasza 03.09, wariant A):
dzialkowiec wysyla ogloszenie przez formularz -> zapis jako 'oczekuje' -> Tomasz dostaje na Telegram z przyciskami TAK/NIE ->
po TAK ogloszenie trafia na strone (build), po NIE kasowane. Kategorie: sprzedam/oddam/kupie/pomoc/zguby/inne."""
import json, os, time, re, subprocess, shutil, datetime, uuid, urllib.request, urllib.parse
from pathlib import Path
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse
router = APIRouter()
ROOT = Path("/root/rod-ai-studio"); WWW = ROOT / "www_rod"; WOLUMEN = Path("/var/lib/docker/volumes/caddy_mcp_data/_data/www_rod")
OCZEK = ROOT / "data/tablica/oczekujace.json"; PUBL = WWW / "content/tablica.json"
OCZEK.parent.mkdir(parents=True, exist_ok=True)
KATEGORIE = {"sprzedam": "Sprzedam", "oddam": "Oddam za darmo", "kupie": "Kupię", "pomoc": "Szukam pomocy", "zguby": "Zguby i znaleziska", "inne": "Inne"}
def _hans():
    tok = czat = None
    for l in open("/root/rod-ai-studio/data/.secrets/hans.env", encoding="utf-8"):
        k, _, v = l.strip().partition("=")
        if k == "HANS_BOT_TOKEN": tok = v.strip()
        if k == "HANS_CHAT_ID": czat = v.strip()
    return tok, czat
def _wczytaj(p, d):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return d
def _zapisz(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8"); os.chmod(p, 0o600)
def _powiadom_tomasza(o):
    tok, czat = _hans()
    kat = KATEGORIE.get(o["kategoria"], o["kategoria"])
    txt = (f"📌 NOWE OGŁOSZENIE NA TABLICĘ (do zatwierdzenia)\n\n[{kat}] {o['tytul']}\n{o['tresc']}\n\n"
           f"Kontakt: {o.get('kontakt','—')}\nOd: {o.get('imie','—')} (działka {o.get('dzialka','—')})")
    klaw = {"inline_keyboard": [[{"text": "✅ Zatwierdź", "callback_data": f"tab_ok:{o['id']}"},
                                 {"text": "❌ Odrzuć", "callback_data": f"tab_nie:{o['id']}"}]]}
    try:
        urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage",
            data=json.dumps({"chat_id": czat, "text": txt[:3900], "reply_markup": klaw}).encode(),
            headers={"Content-Type": "application/json"}), timeout=20)
    except Exception as e: print("tablica: powiadomienie nie poszlo:", e)
def _zbuduj():
    r = subprocess.run(["python3", "build.py"], cwd=WWW, capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(r.stderr[-300:])
    tmp = WOLUMEN.with_name("www_rod.new"); shutil.rmtree(tmp, ignore_errors=True); shutil.copytree(WWW / "dist", tmp)
    for p in tmp.rglob("*"): os.chmod(p, 0o755 if p.is_dir() else 0o644)
    old = WOLUMEN.with_name("www_rod.old"); shutil.rmtree(old, ignore_errors=True)
    if WOLUMEN.exists(): WOLUMEN.rename(old)
    tmp.rename(WOLUMEN); shutil.rmtree(old, ignore_errors=True)
    subprocess.run(["python3", str(ROOT / "tools/pogoda_rod.py")], capture_output=True)
@router.post("/tablica/wyslij")
def tablica_wyslij(req: Request, kategoria: str = Form(""), tytul: str = Form(""), tresc: str = Form(""),
                   kontakt: str = Form(""), imie: str = Form(""), dzialka: str = Form(""), zgoda: str = Form(""), www: str = Form("")):
    if www:  # honeypot (bot)
        return RedirectResponse("/tablica/?ok=1", status_code=303)
    tytul = tytul.strip()[:100]; tresc = tresc.strip()[:600]; kategoria = kategoria if kategoria in KATEGORIE else "inne"
    if not tytul or not tresc or zgoda != "tak":
        return RedirectResponse("/tablica/?blad=1", status_code=303)
    o = {"id": uuid.uuid4().hex[:10], "kategoria": kategoria, "tytul": tytul, "tresc": tresc,
         "kontakt": kontakt.strip()[:80], "imie": imie.strip()[:50], "dzialka": dzialka.strip()[:20],
         "ts": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).isoformat(timespec="minutes")}
    ocz = _wczytaj(OCZEK, []); ocz.append(o); _zapisz(OCZEK, ocz)
    _powiadom_tomasza(o)
    return RedirectResponse("/tablica/?ok=1", status_code=303)
def obsluz_callback(data: str) -> str:
    """Wywolywane z ucha bota Hansa gdy Tomasz klika Tak/Nie. Zwraca komunikat zwrotny."""
    akcja, _, oid = data.partition(":")
    ocz = _wczytaj(OCZEK, []); cel = next((x for x in ocz if x["id"] == oid), None)
    if not cel: return "To ogłoszenie już obsłużone."
    ocz = [x for x in ocz if x["id"] != oid]; _zapisz(OCZEK, ocz)
    if akcja == "tab_nie":
        return f"❌ Odrzucone: {cel['tytul']}"
    # zatwierdz -> dopisz do tablica.json (publiczna) + build
    dane = _wczytaj(PUBL, []); teraz = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
    dane.insert(0, {"id": cel["id"], "kategoria": cel["kategoria"], "tytul": cel["tytul"], "tresc": cel["tresc"],
                    "kontakt": cel.get("kontakt", ""), "imie": cel.get("imie", ""), "dzialka": cel.get("dzialka", ""),
                    "date": teraz.isoformat(timespec="minutes"), "display_date": teraz.strftime("%d.%m.%Y")})
    dane = dane[:60]; PUBL.write_text(json.dumps(dane, ensure_ascii=False, indent=1), encoding="utf-8")
    try:
        _zbuduj()
        subprocess.run(["git", "-C", str(ROOT), "add", "-A", "www_rod/content/tablica.json"], capture_output=True)
        subprocess.run(["git", "-C", str(ROOT), "commit", "--no-verify", "-qm", f"Tablica: zatwierdzone ogloszenie ({cel['tytul'][:40]})"], capture_output=True)
    except Exception as e: return f"Zatwierdzone, ale blad publikacji: {str(e)[:150]}"
    return f"✅ Opublikowane na tablicy: {cel['tytul']}"
