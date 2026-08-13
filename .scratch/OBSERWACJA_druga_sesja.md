# OBSERWACJA: DRUGA SESJA MCP (ustanowiona 6.08.2026 08:42 CEST)

DECYZJA TOMASZA (6.08): OBSERWOWAC. Nie rotowac tokenu MCP, nie zostawiac slepo. Miec oko.

## CO OBSERWUJEMY
Druga, niezalezna sesja Claude laczaca sie przez MCP fabryki (mcp-fabryka.service) TYM SAMYM tokenem co Klaudek.
6.08 07:56-08:02 CEST dopisala reguly pisania do pelnych 10 (commit d3b02e8), zapisala _zrobione_ok przez `tools/zrobione.py`.
NIE Henio (agent.log czysty), NIE Hans (tylko loguje do most.jsonl), NIE Claude Code (brak sesji jsonl 6.08).
Najprawdopodobniej: dogorywajace ZABLOKOWANE OKNO Tomasza, ktore domknelo zadanie o 08:02 i ucichlo.

## LINIA BAZOWA (stan przy ustanowieniu)
- git HEAD = 2508a13 (commit Klaudka: teleport nadrobiony)
- Ostatni slad DRUGIEJ sesji w most.jsonl: ts 2026-08-06T08:02:48+02:00, komenda `python3 tools/zrobione.py --co "JAK_PISZEMY uzupelnione do 10 regul..."`
- Od 08:02:48 do 08:42 CEST (40 min): w most.jsonl WYLACZNIE komendy Klaudka (tej sesji). Cisza obcej sesji.

## SYGNAL ALARMOWY (jak rozpoznac powrot drugiej sesji)
1. git HEAD != 2508a13 (ani kolejny commit Klaudka) BEZ odpowiadajacej komendy Klaudka = obcy commit.
2. W most.jsonl pojawia sie execute_command / write_file / git w czasie, gdy Klaudek NIE prowadzi rozmowy z Tomaszem.
3. Zapis do wiedza/ albo uruchomienie tools/zrobione.py bez sladu w biezacej sesji Klaudka.
Kazdy z tych sygnalow = druga sesja zyje -> zaalarmowac Tomasza, rozwazyc rotacje tokenu MCP.

## BEZPIECZENSTWO
Token MCP fabryki (mcp-fabryka.service, "full shell access to this VPS") WCIAZ OTWARTY.
Trzeci jawny sekret obok kluczy API (docker-compose.yml) i hasla routera (most.jsonl).
Rotacja odcieta na zyczenie Tomasza 6.08 (odcielaby tez aktywna sesje Klaudka).

## DLA NASTEPNEGO OKNA
Na starcie: `git log --oneline -1` (czy HEAD ruszony bez Klaudka) + sprawdz most.jsonl na komendy spoza sesji Klaudka od 08:02:48.
