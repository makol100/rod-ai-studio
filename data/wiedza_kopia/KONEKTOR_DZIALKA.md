# KONEKTOR HA DZIAŁKA — NAPRAWIONY 29.07.2026

Problem: konektor w aplikacji Tomasza nie odpowiadał. Adres to `homeassistant-1.tail0109d4.ts.net`,
czyli nazwa wewnątrz Tailnetu — **aplikacja Tomasza jest poza Tailnetem, więc fizycznie tam nie dotrze**.
Z VPS działało (VPS jest w Tailnecie), dlatego przez cały czas chodziliśmy obejściem przez mostek.

Nabu Casa odpada — **Działka ma tylko Tailscale** (słowo Tomasza, 29.07).

## ROZWIĄZANIE (projekt Henia, wdrożone i sprawdzone)

VPS jest w Tailnecie i ma publiczny adres — więc robi za most. Ale **nie wystawiamy całego Home Assistanta**.
Wpis w `/root/claude-vps-mcp/Caddyfile`:

    dzialka.157-90-155-155.sslip.io {
        @mcp path /api/webhook/mcp_<hash>*
        handle @mcp {
            reverse_proxy 100.115.112.5:8123 {
                header_up -X-Forwarded-For
                header_up -X-Forwarded-Proto
                header_up -X-Forwarded-Host
                header_up Host {upstream_hostport}
            }
        }
        handle { respond "Nie ma tu nic." 404 }
    }

Nowy adres konektora: `https://dzialka.157-90-155-155.sslip.io/api/webhook/mcp_<ten sam hash>`

## DWIE RZECZY, KTÓRE TRZEBA BYŁO ZROBIĆ DOBRZE

1. **Ograniczenie ścieżki.** Bez `@mcp path` byłby publicznie wystawiony cały frontend HA ze stroną
   logowania. Zmierzone po wdrożeniu: strona główna **404**, `/api/` **404**, `/config` **404**.
   Odpowiada wyłącznie ścieżka webhooka.
2. **Zdjęcie nagłówków proxy.** Pierwsze podejście dawało **400 Bad Request** — Home Assistant odrzuca
   ruch z nieznanego proxy. Alternatywą było dopisanie `trusted_proxies` w configuration.yaml Działki,
   ale to znaczy edycję i restart instancji 600 km stąd. Zamiast tego Caddy zdejmuje nagłówki
   `X-Forwarded-*` i podstawia Host — HA widzi połączenie jak zwykłe z tailnetu. **Zero zmian na Działce.**

## POMIAR PO WDROŻENIU
- webhook przez nowy adres: **HTTP 200 w 0.24 s**
- bezpośrednio z VPS: HTTP 200 (bez zmian)
- reszta HA z internetu: 404

## CO ZOSTAŁO DLA TOMASZA
Podmienić adres w konektorze „HA DZIAŁKA" w aplikacji na `dzialka.157-90-155-155.sslip.io`.
Hash webhooka bez zmian.
