#!/usr/bin/env python3
"""Osobny bot Telegram Belzebuba @BelzebubV2_bot (25.09.2026, D-0608/D-0610: „Zrób mi okno w telegramie dla Belzebuba
żeby nie musiał wpisywać /bzb", „Dla mnie i Wiki"). Kazda wiadomosc = pytanie do Belzebuba 2.1 (tools/belzebub_agent.py).
Historia i archiwum wspolne z /bzb (ta sama pamiec): Tomasz -> /root/rozmowy_belzebub, Wikus -> /root/rozmowy_belzebub/wikus.
Rozmowy Wikusi kopiowane do Tomasza botem Hansa (D-0234). Bez limitow dlugosci (D-0606)."""
import json, time, threading, datetime, sys, urllib.request, urllib.parse
from pathlib import Path
sys.path.insert(0, "/root/rod-ai-studio/tools")
import importlib, belzebub_agent as bzb
LUDZIE = {8339659505: "tomasz", 8260509563: "wikus"}
ARCH = {"tomasz": Path("/root/rozmowy_belzebub"), "wikus": Path("/root/rozmowy_belzebub/wikus")}
def _env(n):
    for l in open("/root/.sekrety/wartosci.env", encoding="utf-8"):
        if l.startswith(n + "="): return l.split("=", 1)[1].strip().strip("\"'").strip("<>")
    return ""
TOK = _env("BELZEBUB_BOT_TOKEN"); KLUCZ = _env("BELZEBUB_KEY")
def api(tok, metoda, **p):
    r = urllib.request.Request(f"https://api.telegram.org/bot{tok}/{metoda}", data=urllib.parse.urlencode(p).encode())
    with urllib.request.urlopen(r, timeout=70) as o: return json.load(o)
def wyslij(tok, czat, tekst):
    for i in range(0, max(len(tekst), 1), 3500):
        try: api(tok, "sendMessage", chat_id=czat, text=tekst[i:i+3500] or "…")
        except Exception as e: print("send blad", e, flush=True)
        time.sleep(0.4)
def historia(kto):
    zeb = []
    for pl in sorted(ARCH[kto].glob("2*.md")):
        try: t = pl.read_text(encoding="utf-8")
        except OSError: continue
        if "## PYTANIE TOMASZA" in t and "## ODPOWIEDZ BELZEBUBA" in t:
            cz = t.split("## ODPOWIEDZ BELZEBUBA", 1)
            zeb += [{"role": "user", "content": cz[0].split("## PYTANIE TOMASZA", 1)[-1].strip()}, {"role": "assistant", "content": cz[1].strip()}]
    return zeb
def archiwizuj(kto, q, a):
    k = ARCH[kto]; k.mkdir(mode=0o700, parents=True, exist_ok=True)
    s = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); p = k / f"{s}.md"
    p.write_text(f"# Belzebub — wymiana {s} (bot @BelzebubV2_bot)\n\n## PYTANIE TOMASZA\n\n{q}\n\n## ODPOWIEDZ BELZEBUBA\n\n{a}\n", encoding="utf-8"); p.chmod(0o600)
    with (k / "SPIS.md").open("a", encoding="utf-8") as f: f.write(f"- {s}.md — {q[:90]}\n")
def obsluz(czat, kto, q):
    stop = threading.Event()
    def pisze():
        while not stop.is_set():
            try: api(TOK, "sendChatAction", chat_id=czat, action="typing")
            except Exception: pass
            stop.wait(4)
    threading.Thread(target=pisze, daemon=True).start()
    try:
        importlib.reload(bzb); a, slad = bzb.odpowiedz(q, historia(kto), KLUCZ)
        if slad: a += "\n\n" + slad
    except Exception as e: a = f"Belzebub: błąd {str(e)[:300]}"
    finally: stop.set()
    wyslij(TOK, czat, a)
    try: archiwizuj(kto, q, a)
    except Exception as e: print("archiwum blad", e, flush=True)
    if kto != "tomasz":
        try:
            sys.path.insert(0, "/root/rod-ai-studio/tools"); import hans_ucho
            ht, hc = hans_ucho._wczytaj_token_hansa()
            wyslij(ht, hc, f"[Wikuś -> Belzebub]\nPYTANIE: {q}\n\nODPOWIEDZ:\n{a}")
        except Exception as e: print("kopia blad", e, flush=True)
def main():
    off = 0; print("belzebub_bot start", flush=True)
    while True:
        try: d = api(TOK, "getUpdates", offset=off, timeout=50)
        except Exception as e: print("poll blad", e, flush=True); time.sleep(5); continue
        for u in d.get("result", []):
            off = u["update_id"] + 1; m = u.get("message") or {}
            uid = (m.get("from") or {}).get("id"); czat = (m.get("chat") or {}).get("id"); q = (m.get("text") or m.get("caption") or "").strip()
            if uid not in LUDZIE:
                if czat: wyslij(TOK, czat, "Brak dostępu.")
                print("obcy", uid, flush=True); continue
            if not q: wyslij(TOK, czat, "Na razie rozumiem tylko tekst."); continue
            if q == "/start": wyslij(TOK, czat, "Belzebub słucha. Pisz normalnie — bez /bzb."); continue
            threading.Thread(target=obsluz, args=(czat, LUDZIE[uid], q), daemon=True).start()
if __name__ == "__main__": main()
