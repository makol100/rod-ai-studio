# ŚRODOWISKO: ZENEK

Silnik: Codex CLI (abonament ChatGPT Plus, GPT-5.6 Sol). Uruchamiany na żądanie, nie działa ciągle.

## Dostęp (zmierzony 29.07 — sprawdzał sam)
Odczyt ✅ zapis ✅ internet ✅ obraz ✅ polecenia ✅ — komplet, bez braków.

## Jak go wołać
    cd /root/rod-ai-studio && codex exec "zadanie"
- uruchamiać Z KATALOGU repo (z `/root` żąda trusted dir albo `--skip-git-repo-check`)
- BEZ `--model gpt-5` — na koncie Plus ta flaga jest niewspierana, używać modelu domyślnego
- długie zadania w tle: `nohup ... > /tmp/plik &`, odbiór osobnym wywołaniem (mostek MCP tnie po 120 s)

## Uwaga o pomiarach
Jego sesja chodzi w piaskownicy `bwrap` z własnymi namespace'ami. Widzi tam inne numery użytkowników
(uid 4294967295 zamiast 1000) i nie widzi hostowego systemd ani cgroup. Przy pytaniach o uprawnienia
systemu jego pomiar bywa mylący — rozstrzyga sprawdzenie na hoście.
