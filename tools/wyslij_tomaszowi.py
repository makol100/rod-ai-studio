#!/usr/bin/env python3
"""Wyslij Tomaszowi plik na Telegram botem Hansa (sendPhoto / sendDocument / sendVideo).
Uzycie: python3 tools/wyslij_tomaszowi.py PLIK [--podpis "..."] [--jako photo|document|video]  (domyslnie po rozszerzeniu)"""
import argparse, json, mimetypes, subprocess, sys
from pathlib import Path

def sekrety():
    tok = chat = ""
    for linia in open("/home/hermes/.hermes/.env", encoding="utf-8", errors="replace"):
        k, _, w = linia.strip().partition("="); w = w.strip().strip('"').strip("'")
        if k == "HANS_BOT_TOKEN": tok = w
        elif k == "HANS_CHAT_ID": chat = w
    if not (tok and chat): sys.exit("BRAK HANS_BOT_TOKEN/HANS_CHAT_ID")
    return tok, chat

def wyslij(plik, podpis="", jako=None):
    tok, chat = sekrety(); plik = Path(plik)
    if not jako:
        m = mimetypes.guess_type(plik.name)[0] or ""
        jako = "photo" if m.startswith("image/") and plik.stat().st_size < 9_000_000 else ("video" if m.startswith("video/") else "document")
    metoda = {"photo": "sendPhoto", "video": "sendVideo", "document": "sendDocument"}[jako]
    r = subprocess.run(["curl", "-s", "-F", f"chat_id={chat}", "-F", f"caption={podpis}", "-F", f"{jako}=@{plik}",
                        f"https://api.telegram.org/bot{tok}/{metoda}"], capture_output=True, text=True, timeout=180)
    try: d = json.loads(r.stdout)
    except Exception: d = {"ok": False, "raw": r.stdout[:200], "err": r.stderr[:200]}
    if not d.get("ok") and jako == "photo":
        return wyslij(plik, podpis, "document")
    # Henio (bramka 18.09): twardy slad wysylki — message_id z odpowiedzi API do dziennika
    import time
    with open("/root/rod-ai-studio/data/wyslane_tomaszowi.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"czas": time.strftime("%Y-%m-%d %H:%M:%S"), "plik": str(plik), "jako": jako, "ok": bool(d.get("ok")),
                            "message_id": d.get("result", {}).get("message_id"), "podpis": podpis[:120]}, ensure_ascii=False) + "\n")
    return d

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("plik"); a.add_argument("--podpis", default=""); a.add_argument("--jako", choices=["photo", "document", "video"])
    x = a.parse_args(); d = wyslij(x.plik, x.podpis, x.jako)
    print("OK" if d.get("ok") else "BLAD", Path(x.plik).name, d.get("description") or d.get("raw") or "", d.get("result", {}).get("message_id"))
    sys.exit(0 if d.get("ok") else 1)
