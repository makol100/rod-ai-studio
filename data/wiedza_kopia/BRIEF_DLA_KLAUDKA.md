1. PRODUKCJA: WOLNA — stop zdjety (D-0039) | wygenerowano 2026-08-07 14:01:30 CEST
2. OSTATNIA DECYZJA: D-0068 | 2026-08-07 | Zawsze zapisuj do teleportu i sie nie pytaj — po znaczacej pracy dopisuj wpis do TELEPORT_fabryka.md aut…
3. JAK PISZESZ: odpowiedź PIERWSZA, kroki numerowane, na końcu JEDNA rzecz do zrobienia, stan powtarzany co turę (krok 3 z 5), konkretne liczby zamiast ogólników. Bez pokrycia — NIE WIEM. Pełne: wiedza/JAK_PISZEMY.md
4. TO JEST SKRÓT. Reszta na dysku, dociągaj sam gdy trzeba: pełny dziennik TELEPORT_fabryka.md · wszystkie decyzje `python3 tools/decyzje.py --lista` · nauki wiedza/NAUKI.md · kanon Izabeli wiedza/IZABELA_KANON_0.1.md · teczki wiedza/TECZKI/ · rozmowy /mnt/transcripts/journal.txt
5. PRAWA RĘKA: HENIO | su - hermes -c 'cd /root/rod-ai-studio && timeout 400 hermes -z "zadanie"'
6. HANS: Henia, nie Klaudka (D-0050)
7. TELEPORTY: fabryka 0.0 dnia, Home Assistant 1.2 dnia
8. /root/.claude/CLAUDE.md: 3.3 dnia bez zmian
9. !! DO ZROBIENIA PRZEZ TOMASZA: WYMIANA KLUCZY API (FAL_KEY + ANTHROPIC_API_KEY) — wyswietlone w czacie 10.07, nadal jawnym tekstem w docker-compose.yml. Tomasz 4.08: "dzis wieczorem albo jutro rano".
10. GENEK: oszczędzany — tylko oczy/uszy/grafika (D-0005: Gienka oszczedzac ze wzgledu na oczy i uszy i generowanie grafik.)
11. KIEROWNIK: Klaudek, rozstrzygnięte 4.08 (D-0002)

# STAN (graf krotkotrwaly)

```mermaid
graph TD
  n001["n001 | zrobione | Router Sosnowca przenumerowany 192.168.0.1 -> 192.168.50.1, trasa Tailscale 192.168.50.0/24 zatwierdzona i dziala"]
  n002["n002 | zrobione | Transkrypcje YouTube przez oczy_uszy.py (Gemini fileUri omija blokade botow na VPS)"]
  n003["n003 | zrobione | STAN zbudowany: pamiec_stan.py rdzen + wariant3 + luka1 (--zrodlo-most), commit 3383d06"]
  n004["n004 | w_toku | Wdrozenie STAN do protokolu startu + pamieci Klaudka"]
  n003 --> n004
  classDef zrobione fill:#d8f3dc,stroke:#2d6a4f
  classDef w_toku fill:#fff3bf,stroke:#e67700
  classDef bloker fill:#ffe3e3,stroke:#c92a2a
  class n001,n002,n003 zrobione
  class n004 w_toku
```
