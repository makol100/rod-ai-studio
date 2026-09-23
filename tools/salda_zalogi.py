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
# Codex (Zenek) — limit subskrypcji: ostatnia sesja z bledem 'usage limit' w ciagu 24 h
try:
    import glob, os, time
    fs = sorted(glob.glob(os.path.expanduser("~/.codex/sessions/*/*/*/*.jsonl")), key=os.path.getmtime)[-5:]
    lim = any("usage limit" in open(f, errors="ignore").read().lower() and time.time() - os.path.getmtime(f) < 86400 for f in fs)
    wyn.append(("Codex (Zenek)", "LIMIT SUBSKRYPCJI — chatgpt.com/codex/settings/usage" if lim else "OK", lim))
except Exception: wyn.append(("Codex (Zenek)", "?", False))
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
