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
        importlib.reload(bzb); a, slad = bzb.odpowiedz(q, historia(kto), KLUCZ, obraz_cb=sd_callback(czat, kto))
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

# 25.09 D-0612: "obraz: ..." -> Belzebub pisze prompt EN -> Zenek (Codex image_gen, 0 zl) -> zdjecie do czatu
import subprocess, uuid, os
def prompt_en(opis, sd=False):
    instr = ("You write prompts for Stable Diffusion 1.5. Output ONLY one English prompt: comma-separated descriptive tags, max 55 words, most important subject first, then setting, lighting, style (e.g. photorealistic, detailed, 35mm photo). No quotes, no comments. /no_think" if sd else
             "You write prompts for an image generator. Output ONLY one English prompt (60-120 words): subject, setting, composition, lighting, style, camera. No quotes, no comments. /no_think")
    body = {"model": bzb.MODEL_DOMYSLNY, "max_tokens": 3000, "temperature": 0.7, "messages": [
        {"role": "system", "content": instr},
        {"role": "user", "content": opis}]}
    d = bzb._api(body, KLUCZ)
    t = ((d.get("choices") or [{}])[0].get("message", {}).get("content") or "").strip()
    import re as _re
    return _re.sub(r"(?s)<think>.*?</think>", "", t).strip() or opis
def wyslij_zdjecie(czat, plik, podpis):
    b = uuid.uuid4().hex
    dane = (f"--{b}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{czat}\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{podpis[:1000]}\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"obraz.png\"\r\nContent-Type: image/png\r\n\r\n").encode() + open(plik, "rb").read() + f"\r\n--{b}--\r\n".encode()
    r = urllib.request.Request(f"https://api.telegram.org/bot{TOK}/sendPhoto", data=dane, headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(r, timeout=120) as o: return json.load(o)
def sd_callback(czat, kto):
    """25.09 D-0624 („Po co obraz?"): Belzebub SAM wola generuj_obraz w rozmowie — bez komendy."""
    def cb(pr):
        try: wyslij(TOK, czat, "🎨 Maluję (Stable Diffusion)…")
        except Exception: pass
        os.makedirs("/tmp/bzb_img", exist_ok=True); cel = f"/tmp/bzb_img/bzb_sd_{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
        with SD_LOCK:
            r = subprocess.run(["timeout", "400", "/root/rod-ai-studio/tools/sd_gen.py", pr, cel], stdin=subprocess.DEVNULL, capture_output=True, text=True, env={**os.environ, "HF_HUB_OFFLINE": "1"})
        if not os.path.isfile(cel): return "BŁĄD: Stable Diffusion nie wygenerował obrazu: " + (r.stderr or r.stdout)[-200:]
        wyslij_zdjecie(czat, cel, "[Stable Diffusion] Prompt: " + pr)
        try: archiwizuj(kto, "[obraz]", f"[OBRAZ {cel}]\nPrompt: {pr}")
        except Exception: pass
        return "OK — obraz wygenerowany i już wysłany rozmówcy."
    return cb
SD_LOCK = threading.Lock()   # jeden obraz SD naraz (RAM: SD ~6 GB + Bielik ~12 GB)
def obraz(czat, kto, opis):
    # 25.09 D-0618: „Generowanie zdjęć daj belzebubowi przez diffusiona"; D-0622: „Usuń belzebubowi generowanie zdjęc u zenka" — TYLKO Stable Diffusion na VPS
    wyslij(TOK, czat, "Belzebub układa prompt, Stable Diffusion maluje na naszym serwerze… (1–3 min)")
    try:
        pr = prompt_en(opis, sd=True)
        os.makedirs("/tmp/bzb_img", exist_ok=True); cel = f"/tmp/bzb_img/bzb_sd_{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
        with SD_LOCK:
            r = subprocess.run(["timeout", "400", "/root/rod-ai-studio/tools/sd_gen.py", pr, cel], stdin=subprocess.DEVNULL, capture_output=True, text=True, env={**os.environ, "HF_HUB_OFFLINE": "1"})
        if not os.path.isfile(cel):
            wyslij(TOK, czat, "Stable Diffusion nie wygenerował obrazu: " + (r.stderr or r.stdout)[-300:] + "\nPrompt:\n" + pr); return
        wyslij_zdjecie(czat, cel, "[Stable Diffusion] Prompt: " + pr)
        archiwizuj(kto, "obraz: " + opis, f"[OBRAZ {cel}]\nPrompt: {pr}")
        if kto != "tomasz":
            import hans_ucho; ht, hc = hans_ucho._wczytaj_token_hansa(); wyslij(ht, hc, f"[Wikuś -> Belzebub] obraz: {opis}\nPrompt: {pr}")
    except Exception as e:
        wyslij(TOK, czat, f"Błąd obrazu: {str(e)[:300]}")

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
            if q == "/start": wyslij(TOK, czat, "Belzebub słucha. Pisz normalnie — bez /bzb. Chcesz zdjęcie — po prostu poproś, Belzebub sam je namaluje (Stable Diffusion na naszym serwerze)."); continue
            threading.Thread(target=obsluz, args=(czat, LUDZIE[uid], q), daemon=True).start()
if __name__ == "__main__": main()
