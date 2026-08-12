# DECYZJA TOMASZA (2026-08-12): OpenClaw WDROZYC — pilotaz proaktywnosci 24/7
Dekret: "Google oplacone. OpenClaw wdrozyc" (po jednomyslnej naradzie zalogi: Zenek B, Henio B, Klaudek B).

## WARUNKI PILOTAZU (z narady, obowiazuja w konfiguracji runtime, nie w promptach)
1. Start: TYLKO odczyt i meldunki. Zero publikacji, zero zmian produkcyjnych.
2. Kazdy krok kosztujacy pieniadze lub publikujacy = bramka zgody Tomasza na Telegramie.
3. Heartbeat na darmowym modelu (Ollama lokalnie), mocne modele tylko do realnej pracy.
4. Modele lokalne: okno kontekstu min. 64k (ustawic recznie).

## STOS ZERO NOWYCH KOSZTOW (rekomendacja Zenka, zrodla w /tmp/zenek_darmo.txt)
cron/n8n zegar -> Codex OAuth (ChatGPT Plus) -> Claude Max -> Groq free -> Ollama lokalnie (zmierzone: qwen2.5vl:7b ~19 tok/s CPU; Bielik-11B na dysku).
Gemini: kredyty doladowane 2026-08-12 ("Google oplacone") — Genek wraca do obrazow/filmow.

## PIERWSZE ZADANIE PILOTAZOWE
Poranny raport na Telegram: stan HA Dom/Dzialka + research pod nastepny film.

## STATUS WDROZENIA (2026-08-12) — czesc Klaudka ZAKONCZONA, werdykt Zenka: POTWIERDZAM
- OpenClaw 2026.7.1-2, user openclaw (bez roota, bez grupy docker), gateway jako usluga systemd (user, linger), nasluch TYLKO loopback 127.0.0.1:18789.
- Auth: token (test funkcjonalny: zly token = unauthorized 1008, dobry = dziala). Prawa: ~/.openclaw 700, openclaw.json 600.
- Model: lokalna ollama/qwen2.5vl:7b (zero chmury, zero kosztow). Deny [group:web, browser] dla malego modelu. Sandbox mode=all backend=podman (ROOTLESS, test przeszedl). Exec-policy: allowlist + ask=on-miss + askFallback=deny. Kanaly: zero. Heartbeat: 30m.
- Audyt: 0 critical. Warn trusted_proxies NIEISTOTNY przy local-only (werdykt Zenka; Genek zglosil votum separatum, Henio niedostepny w sesji audytu).
- Dowody: .scratch/openclaw_dowody/ (dowody.txt, dowody2.txt, werdykty).

## NASTEPNE KROKI (wymagaja Tomasza)
1. Codex OAuth (ChatGPT Plus) jako glowny mozg — logowanie Tomasza.
2. Claude Max jako drugi backend — logowanie Tomasza.
3. Kanal Telegram — nowy bot (BotFather) i token od Tomasza.
4. Potem: pierwsze zadanie pilotazowe (poranny raport HA + research) przez openclaw cron/heartbeat, z bramka approvals.

## STATUS 12.08.2026 po poludniu — SUBSKRYPCJE I KANAL SPIETE (testy zywe)
- Telegram: bot @Rodmoltybot, allowlist TYLKO Tomasz (8339659505) + ownerAllowFrom; dwustronna komunikacja PRZETESTOWANA.
- Codex OAuth (ChatGPT Plus): profil openai OAuth zarejestrowany (flow tmux + callback URL od Tomasza); test "SUBSKRYPCJA-DZIALA" na openai/gpt-5.5 PRZESZEDL.
- Claude Max: profil anthropic:claude-cli (reuse loginu Claude Code; creds skopiowane do usera openclaw); test "MAX-DZIALA" na anthropic/claude-haiku-4-5 PRZESZEDL. Aliasy: opus, sonnet.
- Lokalny mozg: ollama/qwen2.5vl:7b default, contextWindow 32768 (fix stopReason=length), maxTokens 1024.
- Fallbacki: openai/gpt-5.5 -> anthropic/claude-haiku-4-5. Plugin stock codex-supervisor enabled.
- OTWARTE: (1) sandbox nadal off (plugin podman za murem "trusted" tej wersji; kompensacja: deny web dla malego modelu + exec-policy ask/deny + allowlist kanalu), (2) re-audyt Zenka rundy 2, (3) pierwsze zadanie pilotazowe: poranny raport (cron), (4) ewentualna aktualizacja OpenClaw dla trusted plugins.
KOREKTA TOMASZA 12.08: 'Rod to tylko Wozniki' — poranny raport: pogoda WYLACZNIE Wozniki (bez Walding).
DOPRECYZOWANIE 12.08: pogoda Walding moze byc w briefingu, ale ODDZIELNIE od ROD ('nie lacz Austrii z ROD') — Wozniki = pogoda ROD, Walding = prywatna sekcja.
DEKRET 12.08 ("Wszystko" po przegladzie warsztatu): A) wlasny klient Gemini Image dla Zenka (redundancja; bramka: kazda generacja wymaga jawnej flagi kosztowej, bez niej tylko darmowa walidacja auth), B) Zenek skleja pipeline 16:9 + pipeline Wiadomosci (bez platnych generacji w budowie), C) naprawa launchera Henia, D) odczyt kanonow dla Genka + wiedza/BANK_PROMPTOW.md.
DEKRET E 12.08 ("Dzialamy"): wlasny klucz fal.ai dla Henia (osobny klucz, srodowisko FAL_KEY w jego .env) + fal_client i whisper w jego venv (0 zl) + wlasne tools Henia do Veo (submit TYLKO z jawna flaga kosztowa). Weryfikacja klucza bez kosztu: 401 vs 404 na queue.fal.run.
E WYKONANE 12.08: klucz fal Henia w jego .env (600), weryfikacja darmowa OK (200 vs 401), fal_client+whisper zainstalowane (exit=0), veo_henio.py zbudowany PRZEZ HENIA (bramka --zaplac dziala: dry-run $0.64 zatrzymany; --sprawdz-klucz 405 -> poprawka u Henia).
ZGODA TOMASZA 12.08 ("Daje"): dwa testy klienta obrazow Zenka — imagen-4.0-fast ~$0.02 + gemini-3.1-flash-image ~$0.067 (razem ~$0.09). Koszt infrastrukturalny (walidacja klienta), nie odcinkowy.
