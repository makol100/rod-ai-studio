# ŚRODOWISKO: HENIO

Silnik: Hermes Agent v0.19.0 + DeepSeek V4 Flash (kontekst 128K), osobne konto Tomasza.
Gdzie żyje: user `hermes` na VPS, gateway Telegram @HermesDyzurny_Bot (słucha tylko ID 8339659505).
Działa 24/7. Koszt zadania: grosze.

## Dostęp (zmierzony 29.07)
Odczyt ✅ zapis ✅ internet ✅ obraz ✅ polecenia ✅ — zapis i kasowanie w całym repo BEZ sudo (ACL),
sudo NOPASSWD, grupa docker (fabryka-api, caddy-mcp, n8n), własny klucz Gemini w `~/.gemini/.env`.

## Czego silnik NIE potrafi i czym to obchodzi
| brak | polecenie zastępcze |
|---|---|
| brak `web_search` / `web_fetch`; Google odbija curla jako bota | `python3 tools/szukaj_net.py "pytanie"` — zwraca odpowiedź z adresami źródeł |
| model nie przyjmuje obrazów (`vision_analyze` → błąd 400) | `python3 tools/oczy_uszy.py plik.jpg --pytanie "..."` — działa też na wideo i YouTube |

## Ścieżki jego okna
- kopia wiedzy: `/home/hermes/fabryka/data/wiedza_kopia/` (+ `archiwum/` z oboma teleportami)
- log fabryki: `/var/log/fabryka-api.log`
- jego patrole: `~/.hermes/scripts/` — zasoby co 30 min, fabryka co godzinę, meldunek 7:00

## Runbook dyżuru
`/home/hermes/PODRECZNIK_DYZURNEGO.md` — checklist zmiany, progi alarmowe, wzorce w logach, eskalacja.
To instrukcja OPERACYJNA roli dyżurnego, nie regulamin osoby.
