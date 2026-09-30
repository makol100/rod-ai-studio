#!/usr/bin/env python3
"""Codzienna kontrola sald zalogi (DeepSeek=Henio, fal.ai=Kling/TTS/obrazy, Google=Genek) -> alarm na Telegram gdy nisko lub 429/402."""
import json, re, sys, urllib.request
sys.path.insert(0, "/root/rod-ai-studio/tools")
PROG = {"deepseek": 3.0, "fal": 5.0}
wyn = []
# DeepSeek (Henio)
try:
    k = re.search(r"sk-[a-f0-9]{32}", open("/home/hermes/.hermes/config.yaml").read()).group(0)
    r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.deepseek.com/user/balance", headers={"Authorization": "Bearer " + k}), timeout=20))
    b = float(r["balance_infos"][0]["total_balance"]); wyn.append(("DeepSeek (Henio)", b, b < PROG["deepseek"]))
except Exception as e: wyn.append(("DeepSeek (Henio)", None, True))
# fal.ai
try:
    k = open("/root/rod-ai-studio/data/.secrets/fal_key").read().strip()
    b = float(json.load(urllib.request.urlopen(urllib.request.Request("https://rest.alpha.fal.ai/billing/user_balance", headers={"Authorization": "Key " + k}), timeout=20)))
    wyn.append(("fal.ai (Kling/TTS/obrazy)", b, b < PROG["fal"]))
except Exception: wyn.append(("fal.ai", None, True))
# Google (Genek) — brak API salda; test wywolania
try:
    k = [l.split("=", 1)[1].strip().strip('"') for p in ("/root/.gemini/.env", "/root/.sekrety/wartosci.env") for l in open(p) if l.startswith("GEMINI_API_KEY=")][0]
    urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={k}", data=json.dumps({"contents": [{"parts": [{"text": "OK"}]}]}).encode(), headers={"Content-Type": "application/json"}), timeout=30)
    wyn.append(("Google (Genek)", "OK", False))
except urllib.error.HTTPError as e:
    wyn.append(("Google (Genek)", f"HTTP {e.code}" + (" — kredyty wyczerpane" if "depleted" in e.read().decode() else ""), True))
except Exception: wyn.append(("Google (Genek)", "błąd", True))
# Codex (Zenek) — limit subskrypcji AKTYWNY TERAZ (30.09.2026: stara wersja alarmowala 24 h po bledzie, choc limit 5 h juz minal)
# Blad Codexa: "You've hit your usage limit ... try again at 11:04 AM" (czas UTC, jak zegar VPS). Alarm tylko gdy ta godzina jeszcze nie minela.
try:
    import glob, os, time, datetime as _dt
    fs = sorted(glob.glob(os.path.expanduser("~/.codex/sessions/*/*/*/*.jsonl")), key=os.path.getmtime)[-8:]
    lim, do_kiedy = False, ""
    for f in reversed(fs):
        tx = open(f, errors="ignore").read()
        if "usage limit" not in tx.lower(): continue
        mt = _dt.datetime.fromtimestamp(os.path.getmtime(f), _dt.timezone.utc)
        m = re.findall(r"try again at ([^.\\\"]{3,40}?(?:AM|PM))", tx)
        koniec = None
        if m:
            g = re.search(r"(\d{1,2}):(\d{2}) ?(AM|PM)", m[-1])
            if g:
                h = int(g.group(1)) % 12 + (12 if g.group(3) == "PM" else 0)
                koniec = mt.replace(hour=h, minute=int(g.group(2)), second=0, microsecond=0)
                if koniec < mt: koniec += _dt.timedelta(days=1)
                dm = re.search(r"([A-Z][a-z]{2}) (\d{1,2})(?:st|nd|rd|th)?,", m[-1])   # limit tygodniowy: "Oct 5th, 2:30 PM"
                if dm:
                    try:
                        mies = _dt.datetime.strptime(dm.group(1), "%b").month
                        koniec = koniec.replace(month=mies, day=int(dm.group(2)))
                        if koniec < mt: koniec = koniec.replace(year=koniec.year + 1)
                    except ValueError: pass
        if koniec is None: koniec = mt + _dt.timedelta(hours=6)   # brak godziny w komunikacie -> okno 5 h z zapasem
        teraz = _dt.datetime.now(_dt.timezone.utc)
        lim = teraz < koniec
        do_kiedy = (koniec + _dt.timedelta(hours=2)).strftime("%d.%m %H:%M")   # czas polski (CEST)
        break
    wyn.append(("Codex (Zenek)", f"LIMIT SUBSKRYPCJI do {do_kiedy} — chatgpt.com/codex/settings/usage" if lim else "OK", lim))
except Exception as e: wyn.append(("Codex (Zenek)", f"? ({e})", False))
# /tmp (tmpfs w RAM) — >6 GB = ryzyko OOM dla Bielika (23.09.2026)
try:
    import shutil as _sh
    u = _sh.disk_usage("/tmp").used / 1e9; wyn.append(("/tmp (RAM)", f"{u:.1f} GB", u > 6.0))
except Exception: pass
# Ollama (po incydencie 08.2026): obce modele lub obce IP w logu = alarm
try:
    import subprocess as _sp
    mods = [m["name"] for m in json.load(urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=10))["models"]]
    KANON = {"SpeakLeash/bielik-11b-v3.0-instruct:Q8_0", "qwen3:14b", "qwen2.5vl:7b", "glm-5.2:cloud", "kimi-k2.7-code:cloud"}
    obce = [m for m in mods if m not in KANON]
    lg = _sp.run(["journalctl", "-u", "ollama", "--since", "24 hours ago", "--no-pager"], capture_output=True, text=True).stdout
    ip = sorted({l.split("|")[3].strip() for l in lg.splitlines() if "[GIN]" in l and l.count("|") >= 4} - {"127.0.0.1"})
    ip = [i for i in ip if not (i.startswith("172.") or i.startswith("100.") or i.startswith("10."))]
    wyn.append(("Ollama obce modele/IP", (f"MODELE: {obce} " if obce else "") + (f"IP: {ip}" if ip else "") or "OK", bool(obce or ip)))
except Exception as e: wyn.append(("Ollama", "?", False))
alarm = any(a for _, _, a in wyn)
lin = "\n".join(f"{'⚠️' if a else '✅'} {n}: {b if not isinstance(b, float) else f'{b:.2f} USD'}" for n, b, a in wyn)
print(lin)
if alarm or "--zawsze" in sys.argv:
    import hans_ucho as h
    tok, czat = h._wczytaj_token_hansa()
    urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage", data=json.dumps({"chat_id": czat, "text": ("⚠️ SALDA ZAŁOGI — doładuj:\n" if alarm else "Salda załogi:\n") + lin}).encode(), headers={"Content-Type": "application/json"}), timeout=20)
