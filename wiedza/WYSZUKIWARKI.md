# NIEZALEZNE WYSZUKIWARKI ZALOGI (nie przez Klaudka, nie Gemini)
Dekret Tomasza: kazdy agent (oprocz Genka - on do obrazow/filmow) ma WLASNA, niezalezna wyszukiwarke, zeby wyniki sie roznily (przez Klaudka bylyby takie same jak jego).

## Narzedzie
python3 tools/szukaj_web.py "zapytanie" [ile] --backend=<searxng|ddg|firecrawl>

## Backendy (wszystkie DZIALAJA, testowane)
- searxng   - wlasny SearXNG na VPS (localhost:8888), agreguje wiele wyszukiwarek. Darmowy, bez klucza.
- ddg       - DuckDuckGo (biblioteka ddgs). Darmowy, bez klucza.
- firecrawl - Firecrawl API v2 (klucz w .env: FIRECRAWL_API_KEY). Czyta tez tresc stron. 1000 stron/mies free.

## PRZYDZIAL (dla niezaleznosci - rozne zrodla)
- ZENEK  -> --backend=searxng
- HENIO  -> --backend=ddg
- firecrawl -> wspolny, do POGLEBIENIA (czytania tresci znalezionych stron - scrape)
- KLAUDEK ma wlasny web_search (czatu) - niezalezny od powyzszych

## Zasada
Kazdy szuka SAM swoim backendem i przynosi wlasne wyniki. Rozbieznosc miedzy zrodlami = wartosc (widoczna w meldunku, rozstrzyga Tomasz).
Most przez Klaudka (most_web.py) zostaje jako FALLBACK, NIE domyslny.
