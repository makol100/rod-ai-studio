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
alarm = any(a for _, _, a in wyn)
lin = "\n".join(f"{'⚠️' if a else '✅'} {n}: {b if not isinstance(b, float) else f'{b:.2f} USD'}" for n, b, a in wyn)
print(lin)
if alarm or "--zawsze" in sys.argv:
    import hans_ucho as h
    tok, czat = h._wczytaj_token_hansa()
    urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage", data=json.dumps({"chat_id": czat, "text": ("⚠️ SALDA ZAŁOGI — doładuj:\n" if alarm else "Salda załogi:\n") + lin}).encode(), headers={"Content-Type": "application/json"}), timeout=20)
