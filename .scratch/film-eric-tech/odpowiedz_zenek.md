## POTWIERDZONE

1. Film omawia artykuł „The new rules of context engineering for Claude 5 models” i przedstawia kontekst jako połączenie promptu, system promptu, skilli, plików CLAUDE.md i pamięci. Pokazuje dwa problemy: kolizje instrukcji oraz przeładowany plik CLAUDE.md ładowany w każdej sesji mimo rzadkiego użycia części reguł. Następnie autor uruchamia `/doctor`, który audytuje jego konfigurację i proponuje wyłączenie nieużywanych lub redundantnych skilli i pluginów oraz skrócenie tekstów.

2. Film nie przedstawia zmiany kompatybilności, przez którą coś w naszym setupie przestanie działać; przedstawia zalecenia optymalizacji kontekstu. Nasze dziewięć skilli w `/root/.claude/skills/` pozostaje zgodne z pokazaną ideą ładowania procedur na żądanie, a ich frontmatter ma łącznie 2686 bajtów, więc materiał nie daje podstaw do stwierdzenia, że dotyczy nas pokazane u Erica obcięcie listy skilli powyżej limitu. Konkretna poprawka jest jednak potrzebna w `/root/rod-ai-studio/`: istnieje `AGENTS.md`, ale nie istnieje projektowy `CLAUDE.md`; oficjalna dokumentacja Claude Code mówi, że Claude Code czyta `CLAUDE.md`, nie `AGENTS.md`, zatem Claude Code nie dostaje automatycznie reguły startu od `wiedza/START.md` zapisanej w pierwszej linii `AGENTS.md`. Należy dodać `/root/rod-ai-studio/CLAUDE.md` z importem `@AGENTS.md` albo dowiązanie do `AGENTS.md`.

3. Autor przesadza już w tytule: materiał nie pokazuje, że nowe reguły „łamą większość setupów”. W filmie pokazuje audyt własnego EricOS, mówi, że nic nie jest kasowane z dysku, a wyłączenia są tylko w ustawieniach, po czym sam wybiera propozycje do zastosowania. Nie przedstawia próby reprezentatywnej ani liczby setupów, które przestały działać.

4. **DZIAŁAĆ** — trzeba teraz dodać projektowy `CLAUDE.md` importujący `AGENTS.md`, bo inaczej Claude Code nie ładuje naszego głównego regulaminu repo; odchudzanie dziewięciu skilli można tylko obserwować.

## HIPOTEZY

Moja opinia: tytuł jest clickbaitowy, natomiast praktyczna rada o usuwaniu kolizji i przenoszeniu rzadkich procedur z zawsze ładowanego kontekstu do skilli jest rozsądna.

## NIE WIEM

Nie wiem na podstawie filmu, czy jakikolwiek z naszych dziewięciu skilli jest faktycznie nieużywany lub redundantny; materiał nie zawiera historii użycia naszego VPS. Nie wiem też, czy autor źródłowego artykułu rzeczywiście dowiódł wyniku „ponad 80%” bez mierzalnej straty, ponieważ film pokazuje to twierdzenie, ale nie metodologię ani dane.

— Zenek
