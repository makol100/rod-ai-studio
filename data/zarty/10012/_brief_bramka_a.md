# ZLECENIE WYKONAWCZE: BRAMKA A na kadrach 10012 "Rezystancja Izolacji"
Zlecenie kontrolne z podzialem rol (regula: autor nie sprawdza sam siebie):
- ZENEK: WYKONAJ bramke A (kod ponizej), zapisz wyniki do data/zarty/10012/_bramka_a_wyniki.txt
- GENEK: NIEZALEZNIE zweryfikuj wyniki Zenka (wlasny przelot sim po min. 2 kadrach albo kontrola logiki+liczb); rozstrzygnij PASS/FAIL per kadr
- HENIO: audyt zgodnosci z regulami serii (VLM pytanie OTWARTE "describe what you see" — pytania naprowadzajace NIE sa weryfikacja; 1 referencja z domeny swiatla; progi sim>=0.35, det>=0.6; twarze=1 na kadr)
Kazdy pisze SWOJ glos do swojego katalogu (plik <imie>.txt), podpisany.

## FAKTY (zmierzone w tej sesji)
- Kadry: data/zarty/10012/kadry/{k01..k05}.jpg (nano-banana-pro 2K 9:16, wygenerowane 12:57-13:00)
- Obsada per kadr: k01=JANUSZ, k02=BOHATER, k03=BOHATER, k04=JANUSZ, k05=JANUSZ
- Karty referencyjne (1 ref, domena DZIENNA): assets/zarty/karty/janusz_baza.jpg, assets/zarty/karty/bohater_baza.jpg
- Srodowisko: cv2+insightface TYLKO w kontenerze: docker exec fabryka-api /app/venv/bin/python ...  (mounty 1:1: data/, assets/, tools/ te same sciezki)
- Ollama VLM Z KONTENERA: http://172.17.0.1:11434 (NIE 127.0.0.1!), model qwen2.5vl:7b
- Szkic startowy (do poprawy adres ollamy): data/zarty/10012/_bramka_a.py — wzorzec twarzy z tools/preflight.py linie 92-109 (buffalo_l, CPU, det_size 640)
- Werdykt per kadr: PASS gdy twarze==1 AND sim>=0.35 AND VLM opisuje scene zgodna z planem (k01 starszy pan kuca przy kosiarce z kablem w tasmie; k02 mezczyzna kucyk+broda+miernik patrzy powaznie; k03 ten sam wskazuje; k04 starszy zblizenie przez ramie; k05 starszy wklada wtyczke do gniazdka na slupku, cala sylwetka) AND zero tekstu/logo w obrazie
## ZAKAZY TWARDE
- ZERO wywolan fal / submitow / wydatkow (obowiazuje D-0175). Bramka A jest w 100% lokalna i darmowa.
- NIE ruszac: kadry/*.jpg, LOCK, KANON.md. Wolno pisac: _bramka_a.py (poprawki), _bramka_a_wyniki.txt, wlasne glosy.
