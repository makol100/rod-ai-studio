
## 27.08.2026 — fail2ban + Caddy access log (S3, wdrozone i przetestowane zywym banem)
1. fail2ban datepattern WYCINA dopasowany prefix z linii ZANIM failregex zobaczy linie.
   Failregex musi pasowac do linii PO wycieciu daty (u nas: zaczyna sie od ',"logger":...').
   Objaw pomylki: fail2ban-regex 0 matched mimo poprawnego regexa na cala linie.
2. Caddy pisze ts z ZMIENNA liczba cyfr ulamka (6 albo 7+). Wzorzec {EPOCH} fail2ban lyka
   maks 6 cyfr ulamka — przy 7 zostaje resztka '.X' na poczatku linii po wycieciu.
   Failregex tolerancyjny: ^(?:\.\d+)?,"logger":... — pokrywa oba przypadki.
3. Access log per host: dyrektywa `log` W BLOKU SITE (nie global options) — loguje tylko ten
   host, nie rusza logowania pozostalych site'ow (kanal MCP bezpieczny).
4. Zla proba hasla musi byc ROZROZNIALNA w logu zanim fail2ban ma co liczyc:
   matcher @zle_klucz { query k=* / not query k=DOBRE } + handle respond 401.
5. Test bana z IP samego VPS: po zbanowaniu VPS nie dogada sie sam ze soba po publicznym
   adresie — natychmiast `fail2ban-client set JAIL unbanip IP` po tescie.
