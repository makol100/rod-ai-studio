# ANALIZA 10 REPOZYTORIÓW AI (28.07.2026)
Zlecenie Tomasza: ocena przydatności dla ekosystemu (fabryka VPS, załoga AI, Henik, HA Dom/Działka, telefon).
Metoda: weryfikacja sieciowa każdego repo (Klaudek, web_search — nazwy z transkrypcji były przekręcone), narada Zenek (codex) + Genek (Gemini API), synteza Klaudka. Pełne głosy: /tmp/zenek_10repo.txt, /tmp/genek_10repo.txt (ulotne), brief: /root/brief_10_repo.md.

## WERDYKTY (Z=Zenek, G=Genek, K=Klaudek-synteza)
1. **earendil-works/pi** (Mario Zechner) — agent toolkit, unified LLM API 15+ prov., minimalizm. Z:WDROŻYĆ(prototyp) G:WDROŻYĆ K:**OBSERWOWAĆ** — mamy działającą załogę (CC+Codex+Gemini+Hermes); Pi = rezerwowy harness / nauka, nie wymieniamy działającego.
2. **ruvnet/RuView** — WiFi CSI sensing, 74.9k★, MIT, integracja HA (MQTT), wymaga ESP32-S3. Krytyka Cybernews 03.2026: "PoC / AI slop". Z:OBSERWOWAĆ G:ODRZUCIĆ K:**OBSERWOWAĆ Z DYSTANSEM** — zero wydatków; ewentualna ciekawostka dla HA Działka (obecność bez kamer) dopiero gdy technologia dojrzeje i się uwiarygodni.
3. **oblien/openship** — self-hosted PaaS, 4 mies., v0.1.11, bugi. Z:ODRZUCIĆ G:ODRZUCIĆ K:**ODRZUCIĆ** — dubluje ręcznego Dockera, dokłada ryzyko produkcji.
4. **tirth8205/code-review-graph** — graf kodu Tree-sitter, MCP, redukcja kontekstu 10-15x. Z:OBSERWOWAĆ G:OBSERWOWAĆ K:**OBSERWOWAĆ** — nasze repo za małe, zysk marginalny; wrócić gdy repo urośnie.
5. **ayghri/i-have-adhd** — skill: odpowiedź pierwsza, kroki numerowane, debug-spiral (3 nieudane iteracje = STOP, nazwij założenie). Z:WDROŻYĆ G:WDROŻYĆ K:**WDROŻYĆ** — zero kosztu, idealne pod pracę Tomasza z telefonu i przeciw spiralom debugowania.
6. **stablyai/orca** — ADE flot agentów, desktop+mobile+VPS, 13-16k★, YC. Z:OBSERWOWAĆ G:OBSERWOWAĆ K:**OBSERWOWAĆ** — apka mobilna kusząca (Tomasz-telefon), ale CX32 za słaby na flotę, ryzyko zmian w działającym stanowisku.
7. **diegosouzapw/OmniRoute** — MIT gateway 290+ prov./500+ modeli, quota-fallback, kompresja RTK+Caveman 15-95%. Z:OBSERWOWAĆ G:OBSERWOWAĆ K:**OBSERWOWAĆ = PLAN AWARYJNY** — zanotować jako fallback gdy Gemini/DeepSeek padnie lub limity zabolą; nie wpinać teraz (dodatkowa warstwa = trudniejsza diagnostyka, kompresja może psuć bramki).
8. **mattpocock/skills** — 176k★, 40+ skilli SKILL.md (/diagnose, /caveman -75% tokenów, /triage, /to-spec, /tdd). Z:WDROŻYĆ G:WDROŻYĆ K:**WDROŻYĆ WYBRANE** — /diagnose (debug hipotezami = nasza zasada fakt-vs-hipoteza), /caveman (oszczędność tokenów), /triage. Przenośne CC+Codex.
9. **koala73/worldmonitor** — OSINT dashboard, 65k★, AGPL. Z:ODRZUCIĆ G:ODRZUCIĆ K:**ODRZUCIĆ** — poza domeną; jedyna wartość: wzorzec "AI digest do Telegrama" (znamy).
10. **bojieli/ai-agent-book** (Li Bojie) — podręcznik "AI Agents in Depth", 10 rozdz., Apache 2.0, kod Python per rozdział, 6.7k★/tydzień. Z:OBSERWOWAĆ G:OBSERWOWAĆ K:**BIBLIOTECZKA** — źródło wzorców przy rozbudowie Henika (pamięć, narzędzia, lekcje); czytać rozdziałami przy projektowaniu, nie komponent produkcyjny.

## TOP-2 KONSENSUS ZAŁOGI
1. mattpocock/skills (wybrane skille) 2. ayghri/i-have-adhd
Oba: koszt 0 zł (git clone), ryzyko ~0 (pliki markdown, nie dotykają produkcji), natychmiastowa wartość dla stanowiska Klaudek+Zenek.
WDROŻENIE CZEKA NA ZGODĘ TOMASZA (zasada: zmiany stanowiska za zgodą).
