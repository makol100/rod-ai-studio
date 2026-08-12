# MOST WEB — internet dla ZENKA i HENIA PRZEZ KLAUDKA (nie Gemini)
Data: 2026-08-11. Dekret Tomasza: "Zenkowi i Heniowi masz dac dostep do internetu. Przez siebie nie gemini. Genek jest dla obrazow i filmow jak bylo powiedziane."

## ZASADA (obowiazuje)
- ZENEK (codex) i HENIO (hermes) szukaja w internecie PRZEZ KLAUDKA (web_search Anthropic), NIE przez Gemini.
- GENEK zostaje do OBRAZOW i FILMOW (Gemini wizja/generacja) - NIE do web-researchu.
- Powod: Gemini lezy (kredyty 429), zapasowe wyszukiwarki (DuckDuckGo/Brave) blokuja captcha. web_search Klaudka jest niezalezny.

## JAK ZENEK/HENIO SZUKAJA W NECIE
python3 tools/most_web.py "zapytanie"
-> zapisuje zapytanie do /tmp/most_web/in/, czeka na odpowiedz Klaudka w /tmp/most_web/out/, zwraca wynik na stdout.
DZIALA gdy Klaudek jest aktywny w sesji z Tomaszem i obsluguje kolejke. Poza sesja most czeka do timeoutu (domyslnie 180s) - to ograniczenie, bo web_search to narzedzie Klaudka w czacie.

## KLAUDEK - OBSLUGA KOLEJKI
python3 tools/most_kolejka.py            # pokazuje oczekujace zapytania (ID + tresc)
# dla kazdego ID: robi web_search, potem: cat > /tmp/most_web/out/<ID>.result
