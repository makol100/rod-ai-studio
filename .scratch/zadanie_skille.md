# ZADANIE KONTROLNE: ktore skille z filmu GitHub Trending #124 przydadza sie fabryce

WAZNE DLA ZENKA (Codex): NIE URUCHAMIAJ zadnych narzedzi, NIE odpalaj zaloga.py, NIE tworz plikow. Napisz SAMA OCENE tekstem, koniec. Poprzednio wpadles w rekurencje zaloga.py — tego nie powtarzaj.

Kazdy (Zenek, Henio) podpisany glos + werdykt per kandydat. Rozbieznosc zostaje. Decyduje Tomasz.

## KONTEKST FABRYKI
rod-ai-studio generuje AI rolki wideo (prezenterka Izabela, "Wiadomosci Dzialkowe"), publikuje na Facebooku ROD Wozniki. Srodowisko: Claude Code na VPS, skille w /root/.claude/skills/. Teksty (skrypty lektora, posty FB) sa generowane przez modele AI.
WAZNE: mamy juz WLASNE narzedzie tools/oczy_uszy.py — Gemini oglada YouTube/wideo przez fileUri (omija blokade botow na VPS), tryb transkrypcja/opis. Dzis zadzialalo od reki na filmie 18:50. To jest nasz odpowiednik "ogladania wideo".

## KANDYDACI DO OCENY (przesiane z 24 repo — tylko te, ktore moga nas dotyczyc)
1. **fogsight** (~3000 gwiazdek) — agent + silnik animacji napedzany LLM. Wpisujesz koncept/kilka slow -> generuje kompletna animacje krotka z narracja i "kinowymi" wizualami; mozna doprecyzowywac przez interfejs jezykowy. Lokalnie albo web fogsight.ai. PYTANIE: czy to alternatywa/uzupelnienie naszego pipeline'u rolek (inny styl: animacja generowana z tekstu), czy nie pasuje do formatu "Izabela + wiadomosci"?
2. **claude-video** (~14000 gwiazdek) — skill /watch: Claude oglada wideo (yt-dlp -> klatki -> Whisper fallback). PYTANIE: daje cokolwiek PONAD nasze oczy_uszy.py? (nasze omija blokade YouTube, ktora /watch dostaje na VPS; ale /watch dodaje KLATKI/obraz, nie tylko audio). Wpinac obok oczy_uszy, czy zbedne bo mamy swoje?
3. **im-not-ai** (~5000 gwiazdek) — skill usuwajacy "AI tell" z tekstu (oryginalnie KOREANSKI: translationese, mechaniczne rownolegle struktury, frazy typu "podsumowujac", "to ma istotne implikacje"), bez zmiany tresci. PYTANIE: warto zaadaptowac KONCEPT na POLSKI dla naszych skryptow rolek i postow FB (zeby nie brzmialy jak AI)? Czy sam koreanski skill jest bezuzyteczny, a wartoscia jest tylko idea?

## PYTANIA ROZSTRZYGALNE (per kandydat: TAK/NIE + jak)
- fogsight: wpinac do testu pod rolki, czy odrzucic (nie nasz format)?
- claude-video: wpinac obok oczy_uszy.py (dla klatek/obrazu), czy zbedne?
- im-not-ai: adaptowac koncept "anty-AI-tell" na polski jako nasz skill kontroli tekstu, czy pominac?
- Czy w 24 repo jest COKOLWIEK, co przeoczylem, a moglo by sie przydac fabryce/HA/pamieci?

## RESZTA 21 REPO (odsiane — uzasadnienie): ida-pro-mcp (reverse engineering), MariaDB (baza; HA i tak jej uzywa, nie skill), server-survival (gra), Dalfox (skaner XSS), DevOps-Projects (nauka), elFinder (web file manager), awesome-newsletters (lista), claude-bug-bounty (bug bounty), BewlyCat (Bilibili), NilAway (Go), KACTL (competitive prog), vite-vue3-lowcode (H5), nixos-hardware (NixOS), Docker Toolbox (deprecated), nomacs (viewer), jichangtuijian (proxy CN), Tracker (Laravel), tailslayer (C++ DRAM), susi_android (asystent), cccl (CUDA). Jesli ktoras zle odsiana — zglos.

Zasada 27.07: domyslnie najnizszy koszt. Zasada 17.07: uczyc sie z cudzych bledow (issues).
