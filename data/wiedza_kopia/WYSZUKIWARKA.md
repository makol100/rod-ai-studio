# NIEZALEZNA WYSZUKIWARKA ZALOGI - SearXNG na VPS
Dekret Tomasza: "Heniek i Zenek powinni miec swoja niezaleznosc we wyszukiwaniu. Przez Klaudka wyniki moga byc takie same jakby on szukal. Wszyscy oprocz Genka maja wlasna wyszukiwarke."

## ZASADA
- KAZDY (Klaudek, Zenek, Henio) szuka w internecie SAM przez wlasna wyszukiwarke - NIE przez Klaudka, NIE przez Gemini.
- GENEK zostaje do obrazow/filmow (Gemini wizja).
- Wyszukiwarka: SearXNG (wlasna instancja Docker na VPS, 127.0.0.1:8888) - metawyszukiwarka Google/Bing/DuckDuckGo, JSON, bez kluczy i limitow.

## JAK SZUKAC (kazdy sam)
python3 tools/szukaj_www.py "zapytanie"
-> surowe wyniki z internetu (tytul, URL, opis). Wlasne zapytania = wlasne wyniki.

## STARY most_web.py (przez Klaudka) - PORZUCONY
Dawal te same wyniki co Klaudek (brak niezaleznosci). Zastapiony przez szukaj_www.py (SearXNG). most_web zostaje tylko awaryjnie.

## Infrastruktura
Kontener docker "searxng" (searxng/searxng), restart unless-stopped, port lokalny 8888, config /root/searxng/settings.yml (JSON on).
