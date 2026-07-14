# PROCEDURY — jak się robi

## Patch zamiast pełnego renderu (naprawa 1-2 scen)
NIE odpalaj pipeline'u od nowa. Kolejność:
1. Popraw prompt w `data/reels/NNNNNN/prompts.txt` (backup!) i/lub LEKTOR w scenes.txt
2. Jeśli lektor się zmienił: `generate_audio(folder, scenes)` (edge-tts, darmowe, ~30 s)
3. `generate_image(prompt, images/NN.jpg, silnik="fal-ai/nano-banana-pro")` — TYLKO zmienione sceny ($0.15/szt., ZGODA!)
4. `make_subtitles(folder)` (Whisper, bez pytania) → `render_video(folder)` (muzyka wmiksowana w środku)
Wzorzec: /tmp/patch93.py (sesja 14.07). Zero Bielika, zero pełnej rundy fal.ai.

## Odpalanie rolki przez API
POST /generate-reel: {"prompt": TREŚĆ TEMATU (nie instrukcja!), "topic_id": N,
"tryb_jezykowy": "czysty_bielik"}. Timeout klienta po ~25 s = NORMALNE (pipeline w tle);
weryfikuj przez /aktywne-generowanie. Pole tematu = materiał źródłowy po "Tekst:",
Bielik dostaje własny szablon — nie wklejać mu instrukcji formatowania.

## Przed restartem kontenera fabryka-api
1. `/aktywne-generowanie` musi zwracać {"aktywna":null} ALBO etap="checkpoint"
   (checkpoint PRZEŻYWA restart — stan na dysku; mielenie w toku NIE przeżywa!)
2. Zmiany w panel.html NIE wymagają restartu (dysk). Zmiany w *.py — wymagają.
3. Po restarcie: /health + endpoint dotknięty zmianą.
⚠️ Wyniki testów po restarcie potrafią wracać ze STAREGO procesu — testować na świeżo,
najlepiej po pełnym cyklu (docker restart + sleep 22 + curl).

## Transfer plików i długie procesy (MCP)
- Sandbox Claude NIE dosięga VPS (host_not_allowed) — pliki TYLKO przez fabryka:write_file
- `docker exec` bez heredoc (psuje składnię) — skrypty przez `docker cp /tmp/x.py fabryka-api:/tmp/`
- Długie procesy: `setsid nohup ... < /dev/null & disown` na hoście albo
  `docker exec -d` w kontenerze; polling logu zamiast czekania (timeout MCP = 120 s)
- \n w stringach Pythona pisanych przez bash: przez chr(10)/chr(92), heredoc je psuje

## HA Dom / Działka
- Dom: Nabu Casa + MCP; Działka: Tailscale (Funnel włączony!) + MCP
- Zmiany configuration.yaml (klucz rest, shell_command): restart HA wymagany;
  restart przez MCP potrafi zwrócić error, ALE się wykonać — weryfikuj po 90 s
- Telegram: telegram_bot.send_message przez HA Dom (token w HA, NIE kopiować na VPS)
- FB photo post: dwustopniowo Graph API v25.0 (upload published=false → feed
  z attached_media). Token w /config/www/rod/lb_fb_post.py na HA Dom.
  Skrypty z tokenem: TYLKO /tmp kontenera, NIGDY do repo (publiczne!).

## Baza tematów — dogenerowanie
tools/dogeneruj_tematy.py: podgrupy z własnymi miesiącami, few-shot z bazy, dedup po
tytule. Po Bieliku SPRZĄTAĆ: REPLACE('**',''), usunąć bełkot, dezaktywować (aktywny=0,
nie kasować) złe tytuły ("Ujęcie:...") i off-topic. Backup bazy przed operacją.

## Sesja — start i koniec
START: wiedza/INDEX.md → potrzebne destylaty → TELEPORT (ostatnia sesja + zaległości)
KONIEC: wnioski trwałe → wiedza/*, przebieg → TELEPORT, git add -A && commit && push
