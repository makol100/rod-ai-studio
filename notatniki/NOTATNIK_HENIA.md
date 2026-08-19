Kierownikiem grupy (załogi) jest zawsze Klaudek — decyzja Tomasza z 4.08.2026.
§
Limit pamięci Henia: 4 000 000 znaków (~1 mln tokenów) — decyzja Tomasza z 4.08.2026.
§
test kopii 4.08 07:4x# test zapisu
§
POTWIERDZONE (19.08.2026): most panel.157-90-155-155.sslip.io wystawia CAŁY fabryka-api (localhost:8000) z internetu BEZ uwierzytelnienia — fabryka-api (/app/src/main.py) nie ma żadnego middleware auth, CORS allow_origins="*". Publicznie bez auth: GET /reels, POST /generate-reel, POST /reels/{id}/publikuj-fb (publikacja FB), POST /host/restart-api, DELETE /reels/{id}. Dowód: curl przez publiczny DNS zwrócił 200 na /reels i /system-health. Drugie: dufs podglad (5031) też bez auth (-a brak), wgraj (5030) ma auth. Caddy (docker logs caddy-mcp) NIE zapisuje access logów — tylko błędy 502/504, więc nie da się z logów ustalić kto pobrał dane (200).
§
Henio pracuje na deepseek-v4-pro (zmierzone 18.08: /home/hermes/.hermes/config.yaml model.default=deepseek-v4-pro, base_url api.deepseek.com/v1; API /models zwraca TYLKO deepseek-v4-flash i deepseek-v4-pro). Model oficjalnie wydany 13.08.2026, licencja MIT, ~1.6 bln parametrów / 49 mld aktywnych (MoE), kontekst 1M. WAŻNE dla oceny mojej pracy: benchmarki agentowe DeepSeek mierzone na własnym harnessie — niezależny Terminal Bench ~30 pkt niżej. Dowód: cennik deepseek.com + deepseek.com + weryfikacja szukaj_net.py 18.08.