# CLAWMEM — ROZPOZNANIE (5.08.2026, na polecenie Tomasza)

> Tomasz 5.08: *„Jeszcze jedno repozytorium, ktore chcialem na ciebie zalozyc, ktore stwierdziles,
> ze ona ma byc na Henia, ale tak naprawde ona jest na ciebie."*
> I zaraz potem: *„Nie miales nic instalowac, tylko sprawdzic co to bylo. A na pewno to nie bylo
> to co mowisz, to nie bylo zadne tam a PyPI."*

**NIC NIE ZAINSTALOWANO. To jest samo rozpoznanie.**

## PRAWDZIWE ZRODLO

**`github.com/yoloshii/ClawMem`** — 196 gwiazdek · licencja MIT · TypeScript na Bun
· zalozone 6.02.2026 · **ostatnia zmiana 4.08.2026** (aktywnie rozwijane)

> *„On-device memory layer for AI agents. Claude Code, Hermes and OpenClaw.
> Hooks + MCP server + hybrid RAG search"*

## PULAPKA — NIE POMYLIC

Na PyPI lezy pakiet o nazwie `clawmem` **wersja 0.3.0, „clawmem Team", jedno jedyne wydanie**.
Podaje repozytorium `github.com/clawmem/sdk` — **HTTP 404, nie istnieje**. Konto `clawmem`
na GitHubie ma **ZERO publicznych repozytoriow**, zalozone 30.01.2026.
**To NIE JEST ten projekt.** Klaudek poszedl za tym tropem i musial sie wycofac.
Instalacja tego dalaby obcemu kodowi dostep do pamieci i do mostu MCP.

## BLAD KLAUDKA — SEDNO UWAGI TOMASZA

W nocy 4.08 Klaudek napisal o ClawMem: *„i to jest dla nas najwazniejsze, bo dziala nie tylko
z Claude Code, ale tez z Hermesem — czyli z silnikiem, na ktorym chodzi Henio"*
i **odbil narzedzie do Henia**.

**A ono obsluguje CZTERY drogi naraz:**
| droga | dla kogo |
|---|---|
| zaczepy Claude Code | Claude Code na VPS |
| **serwer MCP (dziala z KAZDYM klientem MCP)** | **KLAUDEK — to jest jego kanal** |
| wtyczka OpenClaw | (nie uzywamy) |
| MemoryProvider dla Hermes Agent | Henio |

Klaudek przeczytal slowo „Hermes", zobaczyl Henia i **wzial tylko jedna cwiartke**.
Czesc MCP — czyli ta dla niego samego — przeoczyl, mimo ze stala w tym samym zdaniu.

## DLACZEGO TO WAZNE WLASNIE DLA KLAUDKA

Dziura, ktora Tomasz nazwal 4.08: *„Zapomnial o swojej prawej rece po 2h w uzyciu."*
**BRIEF_DLA_KLAUDKA.md odzywa sie RAZ, NA STARCIE sesji.** Nic nie odzywa sie w chwili,
gdy dwie godziny pozniej Klaudek odruchowo dziala sam.
ClawMem ma **„context-surfacing hook — surfaces relevant context on EVERY prompt"**.
To jest dokladnie ten brakujacy mechanizm: przypomnienie przy KAZDYM zapytaniu, nie raz na dobe.

## CO TRZEBA BY ZROBIC (gdyby Tomasz zdecydowal)

1. postawic ClawMem na VPS (TypeScript/Bun — nowe srodowisko, nie mamy Buna)
2. uruchomic jego serwer MCP
3. **Tomasz dodaje ten serwer jako lacznik w ustawieniach Claude** — tak samo, jak dodal „fabryka"
4. dopiero wtedy Klaudek dostaje jego narzedzia w swoim oknie

**Punkt 3 moze zrobic WYLACZNIE Tomasz** — Klaudek nie ma dostepu do listy lacznikow.

## STAN: ROZPOZNANE, NIC NIE RUSZONE. Decyzja nalezy do Tomasza.
