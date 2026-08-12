# TELEPORT FABRYKI — stan po sesji 12.08.2026 (wieczor)
Czytaj najpierw: wiedza/DECYZJE_OPENCLAW.md (dekrety dnia), wiedza/PRZEGLAD_WARSZTATU_2026-08-12.md, wiedza/MOST_MIEDZYSESYJNY.md + PILOT_MOST_PLAN.md.

## CO ZYJE (zweryfikowane dzis)
1. MOLTY/OpenClaw: gateway systemd (user openclaw, loopback+token), Telegram @Rodmoltybot (allowlist TYLKO Tomasz 8339659505), domyslny mozg anthropic/claude-sonnet-5 (Max; dekret "Claude ma robic robote"), fallbacki gpt-5.5->haiku->ollama/qwen (ctx 32k), heartbeat 30m na lokalnym. PORANNY RAPORT cron 7:00 Europe/Vienna (id e64dacf3-...): pogoda ROD=TYLKO Wozniki, Walding OSOBNO prywatnie, porada ogrodnicza. Subskrypcje spiete: Codex OAuth (profil openai:tomasz...), Claude Max (claude-cli reuse). UWAGA: /root/.claude/.credentials.json = SYMLINK do /home/openclaw/.claude/ (rotacja refresh tokena!). Otwarte: sandbox off (plugin podman/codex za murem "trusted" tej wersji; kompensacja deny-web+approvals), re-audyt Zenka po zmianach.
2. MOST MIEDZYSESYJNY Claude Code (2.1.228): ZWERYFIKOWANY + pilot PASS fazy 0-3 (pisarz<->kontroler, worktree, test negatywny). Adresowac REFEM z ListAgents. Faza 4 (kill-test): rozbieznosc zalogi, decyzja Tomasza OTWARTA. Nastepny krok: projekt produkcyjnego ogniwa (propozycja: kontrola scenariusza) + audyt Zenka.
3. WYSZUKIWARKI: kazdy swoja (Zenek searxng:8888, Henio ddg, wspolny firecrawl do poglebiania) — tools/szukaj_web.py; zasady wiedza/WYSZUKIWARKI.md.
4. HENIO: kanoniczny launcher /home/hermes/uruchom_zadanie.py + zadania w /tmp/zadania_henio/ (NIE surowe hermes -z!). Ma: wlasny FAL_KEY w ~/.hermes/.env, fal_client+whisper+torch w venv, wlasne /home/hermes/narzedzia/veo_henio.py (bramka --zaplac; --sprawdz-klucz naprawiony, KOD 200), FIRECRAWL w module web agenta.
5. GENEK: Gemini doladowane ("Google oplacone") — zyje. genek.py: +--skip-trust; kanony ZAWSZE przez --material; wiedza/BANK_PROMPTOW.md utworzony. OTWARTE: Droga 1 (CLI z dyskiem) nadal "zaden model nie odpowiedzial" — debug w kolejce Zenka.
6. OBRAZY: imagen-4.0-fast MARTWY (404 nowi uzytkownicy); kanon gemini-3.1-flash-image $0.067 POTWIERDZONY (tools/zenek_obraz.py, obraz.png dowod).
7. SCENARIUSZ KUNY: scenariusze/kuny_scenariusz_final.md + kuny_material_zweryfikowany.md (v2, zespolowo; obie kuny LOWNE, odlow=kolo lowieckie). Zanety: opcje w rozmowie, decyzja Tomasza NIEPODJETA.

## W TOKU
- ZENEK A+B (klient obrazow + pipeline 16:9 + pipeline Wiadomosci): buduje (setki KB logu /tmp/zenek_ab.txt, raport .scratch/zenek_ab_raport.md). Jego .git RO w sandboxie -> po oddaniu KLAUDEK commituje na branch zenek-warsztat. Potem kontrola zalogi + zgoda Tomasza na platny test odcinka Izabeli. Torch: NIE instalowac — droga przez kontener (patrz PRZEGLAD).

## ZASADY DNIA (dekrety 12.08)
"Robimy tak zeby nic nie spierdolic" (most: etapy, pilot w cieniu, audyt). "Wszystko" (A-D warsztat). "Dzialamy" (E fal Henia). Kazdy czlonek zalogi ma SWOJE narzedzia.
