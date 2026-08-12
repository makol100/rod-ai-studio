#!/usr/bin/env python3
"""most_web.py — szukanie w internecie PRZEZ KLAUDKA (web_search Anthropic, NIE Gemini).
Zenek i Henio uzywaja tego zamiast Gemini do szukania w sieci.
Uzycie: python3 tools/most_web.py "zapytanie"
Dziala gdy Klaudek obsluguje kolejke (jest aktywny w sesji z Tomaszem)."""
import sys, os, time, uuid
IN="/tmp/most_web/in"; OUT="/tmp/most_web/out"
os.makedirs(IN, exist_ok=True); os.makedirs(OUT, exist_ok=True)
if len(sys.argv)<2:
    print('Uzycie: most_web.py "zapytanie"'); sys.exit(1)
q=" ".join(sys.argv[1:])
qid=uuid.uuid4().hex[:10]
open(f"{IN}/{qid}.query","w").write(q)
sys.stderr.write(f"[most_web] {qid} w kolejce do Klaudka: {q}\n"); sys.stderr.flush()
timeout=int(os.environ.get("MOST_TIMEOUT","600"))
res=f"{OUT}/{qid}.result"
for _ in range(timeout):
    if os.path.exists(res):
        print(open(res, encoding="utf-8").read())
        for p in (res, f"{IN}/{qid}.query"):
            try: os.remove(p)
            except: pass
        sys.exit(0)
    time.sleep(1)
sys.stderr.write(f"[most_web] TIMEOUT {timeout}s — Klaudek nie odebral {qid}. Dziala tylko gdy Klaudek jest aktywny.\n")
sys.exit(2)
