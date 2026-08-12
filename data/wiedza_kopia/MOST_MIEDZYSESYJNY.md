# MOST MIEDZYSESYJNY CLAUDE CODE — ZWERYFIKOWANY 12.08.2026
Cross-session messaging: sesje Claude Code pisza do siebie bezposrednio (ListAgents + SendMessage).
Wymaga Claude Code >= 2.1.224; na VPS zaktualizowano 2.1.220 -> 2.1.228.

## DOWOD (test na VPS, obie strony)
- Sesja "nadawca" -> SendMessage -> "odbiorca [520a14]": msg_id d9c009fd-78a2-46df-8cdc-9b2fc98a0474, tresc "TEST MOSTU MIEDZYSESYJNEGO OK — kod LOMPA-1234".
- "odbiorca" ODEBRAL (karta, uds /tmp/cc-socks/...), odeslal potwierdzenie z kodem: msg_id b25e7c69-c45d-4cba-b563-f56f0ac2aa53, success:true.
- "nadawca" ODEBRAL zwrotke z kodem LOMPA-1234. Pelna petla potwierdzona.

## HACZYK ADRESOWANIA (wazne)
Gola nazwa (np. "odbiorca") NIE dziala. Adresowac refem z ListAgents: "odbiorca [520a14]".

## WLASCIWOSCI BEZPIECZENSTWA (z dokow, zgodne z testem)
- Przechodzi TYLKO tekst-podsumowanie; nigdy historia, pliki, uprawnienia.
- Wiadomosc nie moze zatwierdzic uprawnien, zmienic configu ani wykonac polecenia; odbiorca widzi normalny prompt uprawnien.
- Ochrona przed petla: rate-limit, drop identycznych powtorek, sufit 50 nieprzeczytanych.
- Gniazdo per-sesja (unix socket, tylko ten sam user OS); CLAUDE_CODE_MESSAGING_SOCKET dla hooków/skryptow.

## POSWIADCZENIA — WAZNA LEKCJA (rotacja refresh tokena)
Dwie KOPIE tych samych creds Claude (root + openclaw) rozjezdzaja sie: jedna odswieza -> refresh drugiej martwy ("OAuth session expired and could not be refreshed").
FIX na stale: /root/.claude/.credentials.json to SYMLINK do /home/openclaw/.claude/.credentials.json — jeden wspolny plik, obaj zawsze aktualni.

## STATUS
Zweryfikowane narzedzie, NIE wdrozone produkcyjnie. Potencjal: lancuch scenariusz->kontrola->produkcja bez Klaudka jako listonosza; sesja-monitor + sesja-wykonawca. Przed wdrozeniem: projekt uzycia + audyt Zenka.
DEKRET 12.08: "Robimy tak zeby nic nie spierdolic" — wdrozenie TYLKO etapami: (1) projekt pilota -> (2) opinie zalogi -> (3) pilot W CIENIU obok produkcji -> (4) audyt Zenka -> (5) dopiero produkcja. Zero dotykania dzialajacej fabryki do etapu 5.
