#!/usr/bin/env python3
"""Bot ogloszen ROD (@RodOgloszenia_bot) — dekret Tomasza 03.09: osobne okno w Telegramie dla zarzadu (Tomasz, Dariusz, Robert, Roman).
Wiadomosc tekstowa = ogloszenie (1. linia = tytul, reszta = tresc; opcjonalnie linia 'Kiedy: ...' i 'Gdzie: ...'), zdjecie = ilustracja.
Bot pokazuje podglad; 'tak' publikuje na rodwozniki.pl (announcements.json → build → wolumen Caddy), 'nie' kasuje szkic.
/lista — ostatnie ogloszenia, /usun <id> — usuwa (tylko Tomasz), kontakt (przeslany przez Tomasza) = dopisanie osoby do zarzadu."""
import json, os, re, time, subprocess, shutil, datetime, unicodedata
from pathlib import Path
import requests
SEKRETY = Path("/root/.sekrety/wartosci.env"); SKRZYNKA = Path("/root/skrzynka"); SKRZYNKA.mkdir(mode=0o700, exist_ok=True)
DOZWOLENI = SKRZYNKA / "ogloszenia_zarzad.json"; OFFSET = SKRZYNKA / "ogloszenia_bot.offset"; SZKICE = SKRZYNKA / "ogloszenia_szkice.json"
TOMASZ = "8339659505"; ROOT = Path("/root/rod-ai-studio"); WWW = ROOT / "www_rod"; ANN = WWW / "content/announcements.json"
WOLUMEN = Path("/var/lib/docker/volumes/caddy_mcp_data/_data/www_rod"); ADRES = "https://rodwozniki.pl/ogloszenia/"
def token():
    for l in SEKRETY.read_text(encoding="utf-8").splitlines():
        if l.startswith("OGLOSZENIA_BOT_TOKEN="): return l.split("=", 1)[1].strip().strip('"\'')
    raise SystemExit("brak OGLOSZENIA_BOT_TOKEN")
TOK = token()
def api(m, **kw):
    try: return requests.post(f"https://api.telegram.org/bot{TOK}/{m}", data=kw, timeout=40).json()
    except Exception as e: print("api", m, e); return {}
def powiedz(czat, tekst): api("sendMessage", chat_id=czat, text=tekst[:3900])
def wczytaj(p, d): 
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return d
def zapisz(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8"); os.chmod(p, 0o600)
def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower(); s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:40] or "ogloszenie"
def hans_tomasz(tekst):
    try:
        import sys; sys.path.insert(0, str(ROOT / "tools")); import hans_ucho as h
        t, c = h._wczytaj_token_hansa(); h._odpowiedz(t, c, tekst)
    except Exception as e: print("hans:", e)
def zbuduj_i_wystaw():
    r = subprocess.run(["python3", "build.py"], cwd=WWW, capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(r.stderr[-300:])
    tmp = WOLUMEN.with_name("www_rod.new"); shutil.rmtree(tmp, ignore_errors=True); shutil.copytree(WWW / "dist", tmp)
    for p in tmp.rglob("*"): os.chmod(p, 0o755 if p.is_dir() else 0o644)
    stare = WOLUMEN.with_name("www_rod.old"); shutil.rmtree(stare, ignore_errors=True)
    if WOLUMEN.exists(): WOLUMEN.rename(stare)
    tmp.rename(WOLUMEN); shutil.rmtree(stare, ignore_errors=True)
    subprocess.run(["python3", str(ROOT / "tools/pogoda_rod.py")], capture_output=True)
def parsuj(tekst):
    linie = [l.strip() for l in tekst.strip().splitlines() if l.strip()]
    tytul = linie[0][:120] if linie else "Ogłoszenie"; kiedy = gdzie = ""; tresc = []
    for l in linie[1:]:
        m = re.match(r"^(kiedy|termin|data)\s*:\s*(.+)$", l, re.I)
        if m: kiedy = m.group(2).strip(); continue
        m = re.match(r"^(gdzie|miejsce)\s*:\s*(.+)$", l, re.I)
        if m: gdzie = m.group(2).strip(); continue
        tresc.append(l)
    return tytul, kiedy, gdzie, " ".join(tresc)
def podglad(sz):
    return (f"PODGLĄD OGŁOSZENIA\n\n{sz['tytul']}\n{('Kiedy: ' + sz['kiedy']) if sz['kiedy'] else ''}\n{('Gdzie: ' + sz['gdzie']) if sz['gdzie'] else ''}\n{sz['tresc']}\n"
            f"{'📷 ze zdjęciem' if sz.get('foto') else ''}\n\nOpublikować na rodwozniki.pl? Odpisz: TAK albo NIE.\n(Możesz też wysłać poprawioną wersję — zastąpi ten szkic.)")
def publikuj(sz, autor):
    dane = wczytaj(ANN, []); teraz = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
    wpis = {"id": f"{teraz.strftime('%Y%m%d-%H%M')}-{slug(sz['tytul'])}", "title": sz["tytul"], "date": teraz.isoformat(timespec="minutes"),
            "display_date": sz["kiedy"] or teraz.strftime("%d.%m.%Y"), "place": sz["gdzie"] or "ROD Woźniki", "body": sz["tresc"] or sz["tytul"], "featured": True, "autor": autor}
    if sz.get("foto"):
        src = Path(sz["foto"]); dst = WWW / "static/img" / f"ogl_{wpis['id']}.jpg"; shutil.copy2(src, dst); wpis["image"] = dst.name
    for d in dane: d["featured"] = False
    dane.insert(0, wpis); ANN.write_text(json.dumps(dane, ensure_ascii=False, indent=2), encoding="utf-8")
    zbuduj_i_wystaw(); subprocess.run(["git", "-C", str(ROOT), "add", "-A", "www_rod/content", "www_rod/static/img"], capture_output=True)
    subprocess.run(["git", "-C", str(ROOT), "commit", "--no-verify", "-qm", f"Ogloszenie z bota: {wpis['title'][:50]} ({autor})"], capture_output=True)
    return wpis
def pobierz_foto(file_id, nazwa):
    info = requests.get(f"https://api.telegram.org/bot{TOK}/getFile", params={"file_id": file_id}, timeout=30).json()
    sciezka = info["result"]["file_path"]; dane = requests.get(f"https://api.telegram.org/file/bot{TOK}/{sciezka}", timeout=60).content
    p = SKRZYNKA / "ogloszenia_foto" / nazwa; p.parent.mkdir(exist_ok=True); p.write_bytes(dane); return str(p)
def kto(msg):
    uid = str(msg.get("from", {}).get("id")); imie = (msg.get("from", {}).get("first_name") or "").strip()
    if uid == TOMASZ: return "Tomasz"
    z = wczytaj(DOZWOLENI, {})
    return z.get(uid)
def main():
    offset = int(OFFSET.read_text()) if OFFSET.exists() else 0
    print("bot ogloszen start, offset", offset, flush=True)
    while True:
        try: r = requests.get(f"https://api.telegram.org/bot{TOK}/getUpdates", params={"offset": offset + 1, "timeout": 50}, timeout=70).json()
        except Exception as e: print("getUpdates", e); time.sleep(5); continue
        for up in r.get("result", []):
            offset = up["update_id"]; OFFSET.write_text(str(offset))
            msg = up.get("message") or up.get("edited_message")
            if not msg: continue
            czat = str(msg["chat"]["id"]); uid = str(msg.get("from", {}).get("id")); imie_tg = (msg.get("from", {}).get("first_name") or "?").strip()
            osoba = kto(msg)
            # Tomasz przesyla kontakt = dopisanie do zarzadu
            if osoba == "Tomasz" and msg.get("contact"):
                c = msg["contact"]; z = wczytaj(DOZWOLENI, {}); z[str(c.get("user_id"))] = (c.get("first_name") or "").strip() or "?"; zapisz(DOZWOLENI, z)
                powiedz(czat, f"Dodany do zarządu: {z[str(c.get('user_id'))]} (id {c.get('user_id')}). Może już wysyłać ogłoszenia."); continue
            if not osoba:
                powiedz(czat, "To bot ogłoszeń zarządu ROD Woźniki. Dostęp nadaje prezes — poproś Tomasza o dodanie."); hans_tomasz(f"Bot ogłoszeń: obcy nadawca {imie_tg} (id {uid}) — prześlij mi jego kontakt w bocie ogłoszeń, żeby go dodać."); continue
            tekst = (msg.get("text") or msg.get("caption") or "").strip(); szkice = wczytaj(SZKICE, {})
            if tekst.lower().startswith("/start"):
                powiedz(czat, f"Cześć {osoba}! Wyślij ogłoszenie zwykłą wiadomością: pierwsza linia to tytuł, dalej treść. Możesz dodać linie 'Kiedy: ...' i 'Gdzie: ...' oraz zdjęcie. Pokażę podgląd i zapytam, czy publikować."); continue
            if tekst.lower().startswith("/lista"):
                dane = wczytaj(ANN, []); powiedz(czat, "Ostatnie ogłoszenia:\n" + "\n".join(f"- {d['id']}: {d['title']}" for d in dane[:10]) + f"\n{ADRES}"); continue
            if tekst.lower().startswith("/usun"):
                if osoba != "Tomasz": powiedz(czat, "Usuwać może tylko prezes."); continue
                cel = tekst.split(maxsplit=1)[1].strip() if len(tekst.split()) > 1 else ""; dane = wczytaj(ANN, []); nowe = [d for d in dane if d["id"] != cel]
                if len(nowe) == len(dane) or not nowe: powiedz(czat, "Nie znalazłem takiego id (albo to ostatnie ogłoszenie — zostaw jedno)."); continue
                ANN.write_text(json.dumps(nowe, ensure_ascii=False, indent=2), encoding="utf-8"); zbuduj_i_wystaw(); powiedz(czat, f"Usunięte: {cel}. Strona odświeżona."); continue
            if tekst.lower() in ("tak", "ok", "publikuj", "publikować") and uid in szkice:
                try:
                    w = publikuj(szkice.pop(uid), osoba); zapisz(SZKICE, szkice)
                    powiedz(czat, f"✅ Opublikowane na rodwozniki.pl:\n{ADRES}\n(id: {w['id']})")
                    if osoba != "Tomasz": hans_tomasz(f"📢 {osoba} opublikował ogłoszenie na rodwozniki.pl: {w['title']}")
                except Exception as e: powiedz(czat, f"Nie udało się opublikować: {str(e)[:200]}"); print("publikuj:", e)
                continue
            if tekst.lower() in ("nie", "anuluj") and uid in szkice:
                szkice.pop(uid); zapisz(SZKICE, szkice); powiedz(czat, "Szkic skasowany."); continue
            foto = None
            if msg.get("photo"):
                try: foto = pobierz_foto(msg["photo"][-1]["file_id"], f"{uid}_{int(time.time())}.jpg")
                except Exception as e: print("foto:", e)
            if not tekst and not foto: powiedz(czat, "Wyślij tekst ogłoszenia (pierwsza linia = tytuł)."); continue
            if not tekst and foto:
                sz = szkice.get(uid);  
                if sz: sz["foto"] = foto; szkice[uid] = sz; zapisz(SZKICE, szkice); powiedz(czat, "Zdjęcie dodane do szkicu.\n\n" + podglad(sz)); continue
                powiedz(czat, "Mam zdjęcie — teraz wyślij tekst ogłoszenia."); szkice[uid] = {"tytul": "", "kiedy": "", "gdzie": "", "tresc": "", "foto": foto}; zapisz(SZKICE, szkice); continue
            tytul, kiedy, gdzie, tresc = parsuj(tekst); sz = {"tytul": tytul, "kiedy": kiedy, "gdzie": gdzie, "tresc": tresc, "foto": foto or (szkice.get(uid) or {}).get("foto")}
            szkice[uid] = sz; zapisz(SZKICE, szkice); powiedz(czat, podglad(sz))
        time.sleep(1)
if __name__ == "__main__": main()
