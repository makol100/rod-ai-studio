# INCYDENT: włamanie do Ollamy przez otwarte API 11434 (2–18.08.2026) — wykryte i posprzątane 23.09.2026

## Co się stało (dowody: journalctl -u ollama, /api/tags, /api/show)
- Ollama słuchała na 0.0.0.0:11434 bez uwierzytelnienia → skanery internetu weszły przez API.
- Obce IP i akcje: 183.162.105.109 (02.08 create/delete/pull), 136.0.10.220 (03.08 pull), **129.80.12.68 (05.08 pull + DELETE — usunął qwen3:14b + copy/create)**, 156.239.42.225 (06.08 create „verif_sys"), 167.233.197.251 (09.08), 45.86.163.129 (11.08 pull), **199.217.105.247 (12.08 10:29 — 3× create: gpt-4o, claude-3-opus, gpt-4 z tinyllama + system „found our way in… donation to our BTC")**, 101.33.76.181 (12.08), 147.45.69.42 (18.08 /api/chat — używał CPU), 193.29.139.136 (18.08 /v1/models).
- Skutki: cudze modele na dysku (tinyllama + 3 aliasy „okupowe" + verif_sys, ~2,4 GB), obce pulle (transfer/dysk), obce generacje (CPU), **skasowany qwen3:14b** → pipeline foto (prompty obrazów) padał od 05.08 z 404 (dlatego #000097 z 04.09 stoi na checkpoincie, a 23.09 trzy rolki padły).
- 18.08.2026 15:47 override OLLAMA_HOST=127.0.0.1 — od tej chwili ZERO obcych uderzeń (60 dni logów). 23.09: publiczny 11434 = HTTP 000 (zamknięty).

## Co zrobiono 23.09.2026
1. Usunięte obce modele: gpt-4o, claude-3-opus, gpt-4, tinyllama, verif_sys. Zostały: bielik Q8_0, qwen2.5vl:7b, glm-5.2:cloud, kimi-k2.7-code:cloud.
2. iptables: 11434 ACCEPT tylko lo + 172.16.0.0/12 (docker), reszta DROP; zapisane w /etc/iptables/rules.v4.
3. Przywracanie qwen3:14b przez /api/pull (log logs/ollama_pull_qwen3_api.log).
4. Sprawdzone: SSH (hasło tylko z tailnetu, 0 logowań/14 dni), konta, crony, porty, ld.so.preload, procesy, połączenia — czyste. Dysk 95% = nasze pliki (git 9 GB z filmami, duplikat data/ u Henia 14 GB, odrzucone silniki głosu 8 GB, kopie HA 11 GB, modele 18 GB) — po sprzątaniu dockera/cache 87%.

## Zasady od dziś
- Ollama NIGDY na 0.0.0.0. Każda nowa usługa: najpierw 127.0.0.1/Tailscale, potem ewentualnie Caddy z hasłem.
- Cotygodniowa kontrola (salda_zalogi.py): lista modeli Ollamy vs kanon (bielik, qwen3:14b, qwen2.5vl) — obcy model = alarm; obce IP w logu Ollamy = alarm.
- Modele kanoniczne pipeline: DEFAULT_MODEL bielik Q8_0, PROMPT_MODEL qwen3:14b — po każdej awarii 404 sprawdzać /api/tags.
