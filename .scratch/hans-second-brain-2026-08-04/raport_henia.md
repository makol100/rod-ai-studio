# MELDUNEK HENIA — zaległość dzienników i second brain

Data pomiaru: 04.08.2026. Autor: **Henio**.

## POTWIERDZONE

### 1. Zbiór do badania

Polecenie mówi o 18 plikach, lecz bieżący pomiar rekurencyjny plików Markdown
i ich czasu modyfikacji daje **61 plików ogółem i 20 starszych niż 7 dni**. Nie potrafię
odtworzyć z dysku, które dwie pozycje nie należały do wcześniejszej osiemnastki,
więc kontroluję wszystkie 20. To chroni przed wybiórczym pominięciem.

### 2. Werdykt dla 20 plików

Legenda: **STABILNY** = wiek nie jest wadą; zapis nadal pełni swoją rolę.
**MARTWY/SUPERSEDED** = nie wolno czytać jako bieżącego stanu, choć pozostaje
wartościowym śladem historycznym. **MIESZANY** = część nadal działa, część opisuje
nieobowiązujący stan; wymaga późniejszej decyzji Tomasza, nie cichego przepisania.

| plik | werdykt | cytat ze starego pliku | stan faktyczny na dysku |
|---|---|---|---|
| `wiedza/ARCHITEKTURA.md` | **MARTWY jako opis „jak jest teraz”** | l.1: „ARCHITEKTURA — jak jest teraz”; l.16: „Nano Banana Pro = Gemini 3 Pro Image przez fal.ai”; l.62: „bohaterowie: HENIEK + HALINKA” | `wiedza/GENEROWANIE_OBRAZU.md:9` ustala kanon `gemini-3.1-flash-image`; `apps/api/src/zarty_produkcja.py:27-31` ma tylko opisy/głosy `BOHATER` i `JANUSZ`. |
| `wiedza/STYL.md` | **MIESZANY** | l.4-8: haczyk/mięso/zamknięcie i format `SCENA/UJĘCIE/LEKTOR`; l.40: „puenta Mieczysława” | Format rolki foto nadal jest parsowany w kodzie, ale `apps/api/src/zarty_produkcja.py:29-31` ma tylko `BOHATER` i `JANUSZ`; Mieczysław nie jest bieżącą obsadą modułu produkcyjnego. |
| `wiedza/PROCEDURY.md` | **MIESZANY** | l.7: `generate_image(... silnik="fal-ai/nano-banana-pro")`; l.47-48: start obejmuje TELEPORT, koniec zapisuje TELEPORT | Część teleportowa odpowiada przywróconemu `tools/teleport.py`; silnik obrazu przeczy kanonowi `wiedza/GENEROWANIE_OBRAZU.md:9,30`, gdzie Gemini jest drogą główną, fal.ai awaryjną. |
| `wiedza/DROGA_ROLKA_HUMOR.md` | **MIESZANY** | l.12: „Silnik: fal-ai/veo3.1/lite”; l.40: limit „6 USD”; l.49: każdy odcinek ma `wiedza/DECYZJE_NNNN.md` | Ten sam plik l.29 podnosi limit do $12, więc l.40 jest wewnętrznie stare. Bieżące decyzje odcinków leżą w `wiedza/archiwum/`, a aktywna obsada na dysku to duet z `apps/api/src/zarty_produkcja.py:27-31`. Produkcja jest obecnie zatrzymana przez `wiedza/SLOWA_TOMASZA.md:59-70`. |
| `wiedza/PROMPTY_WZORCE.md` | **STABILNY** | l.8: zapis przez `tools/kanarek.py --zapis-bank`; l.38-40: zwycięzca 10008 po PASS | `tools/kanarek.py` istnieje i nadal zawiera obsługę wzorca/banku; `data/zarty/10008/opublikowano.txt` istnieje. Brak świeżej daty nie dowodzi śmierci banku. |
| `wiedza/DECYZJE_SERIA_HUMOR.md` | **STABILNY, append-only** | l.159-166: po czystce zostali tylko `BOHATER` i `JANUSZ`; l.168: publikacja tylko na osobną komendę | `apps/api/src/zarty_produkcja.py:18,27-31,183` ma właśnie ten duet; pliki `assets/zarty/karty/bohater_baza.jpg` i `janusz_baza.jpg` istnieją. |
| `wiedza/AKTYWA_SERII.md` | **STABILNY rejestr kosztów, z jedną jawną flagą** | l.9-11: biblioteka duetu i suma $0.75; l.17: `bohater_noc.jpg JEST ZDRYFOWANY` | Wszystkie wymienione bazy/arkusze/noce nadal istnieją w `assets/zarty/karty/`, w tym jawnie oznaczony `bohater_noc_v1_zdryfowany.jpg`. Brak nowego kosztu nie wymaga dotknięcia księgi. |
| `wiedza/archiwum/ARCHIWUM_DROGA_HUMOR_v1.md` | **MARTWY/SUPERSEDED, poprawnie odłożony** | l.1: „DROGA ROLKA HUMOR”; l.38: Mieczysław/Brian | Nazwa i położenie mówią `ARCHIWUM`; `wiedza/DROGA_ROLKA_HUMOR.md:15-16` wprost mówi, że v1 została zastąpiona. Nie jest bieżącą procedurą. |
| `wiedza/archiwum/DECYZJE_10004.md` | **STABILNY ślad historyczny** | l.20-24: „LUKA HISTORYCZNA… odcinek stoi zamrożony” | `data/zarty/10004/final.mp4` oraz warianty nadal istnieją. Plik nie udaje procedury ogólnej; zachowuje nierozstrzygniętą historię odcinka. |
| `wiedza/archiwum/DECYZJE_10005_slimak.md` | **STABILNY ślad zamknięcia** | l.52-59: „UKOŃCZONY… bez publikacji… ZAMKNIĘTE (na dysku)” | `data/zarty/10005/final.mp4` istnieje, a brak `opublikowano.txt` jest zgodny z „bez publikacji”. |
| `wiedza/archiwum/DECYZJE_10006_afera.md` | **STABILNY ślad historyczny** | l.84-86: Tomasz publikuje ręcznie, auto-publikacja odłożona | `data/zarty/10006/final.mp4` istnieje. Czy Tomasz faktycznie opublikował ręcznie: **NIE WIEM** — na dysku nie ma `opublikowano.txt`. |
| `wiedza/archiwum/DECYZJE_10007_jablko.md` | **STABILNY ślad historyczny** | l.154-158: publikacja przyjęta jako obowiązująca | `data/zarty/10007/final.mp4` istnieje. Bieżącego stanu Facebooka nie sprawdzałem; z samego dysku **NIE WIEM**, czy reel nadal wisi. |
| `wiedza/archiwum/DECYZJE_10008_kontrola.md` | **STABILNY ślad zamknięcia** | l.20: „ZAMKNIETE, OPUBLIKOWANE” | `data/zarty/10008/final.mp4` i `data/zarty/10008/opublikowano.txt` istnieją; zwycięski prompt jest w `wiedza/PROMPTY_WZORCE.md:38-40`. |
| `wiedza/archiwum/DECYZJE_000098.md` | **STABILNY ślad zamknięcia** | l.12: „OPUBLIKOWANA… ZAMKNIĘTE” | `data/reels/000098/video/final_with_music.mp4` istnieje (11 791 764 bajty w pomiarze `ls -l`). Stanu posta na FB dziś: **NIE WIEM**. |
| `wiedza/archiwum/KANON_10009.md` | **STABILNY artefakt odcinka** | l.2-4: źródło Tomasz, kwestie verbatim, czasy nie są kanonem | `data/zarty/10009/KANON.md`, `final.mp4` i `opublikowano.txt` istnieją. Plik jest kanonem zamkniętego odcinka, nie opisem bieżącej infrastruktury. |
| `wiedza/archiwum/DECYZJE_10009.md` | **STABILNY ślad zamknięcia** | l.26: „OPUBLIKOWANE… ODCINEK ZAMKNIĘTY” | `data/zarty/10009/final.mp4`, `final_v1_odrzucony.mp4`, `final_v5.mp4` i `opublikowano.txt` istnieją, zgodnie z opisem wersji i zachowania odrzutu. |
| `wiedza/archiwum/PRZEKAZANIE_2026-07-26_10010.md` | **MARTWY jako bieżące przekazanie, STABILNY jako historia** | l.1-2: „PRZEKAZANIE OKNA… przeczytać… zanim ruszysz”; l.62-63: LOCK `PRZEKAZANY` | `wiedza/archiwum/DECYZJE_10010.md:84` zamyka odcinek jako opublikowany; `data/zarty/10010/final.mp4` i `opublikowano.txt` istnieją. Nie wolno użyć starego „czeka” jako aktualnego stanu. |
| `wiedza/archiwum/DECYZJE_10010.md` | **STABILNY ślad zamknięcia** | l.84: „OPUBLIKOWANO… ODCINEK 10010 DOMKNIĘTY” | `data/zarty/10010/final.mp4`, `opis_fb.txt` i `opublikowano.txt` istnieją. |
| `wiedza/archiwum/BIBLIA_STANISLAWA.md` | **MARTWY/SUPERSEDED jako kanon, poprawnie zarchiwizowany** | l.1-2: „DRAFT… CZEKA NA DECYZJE TOMASZA” | `wiedza/STANISLAW_CANON_1.0.md:1-3` mówi „Zatwierdzona” i nazywa draft archiwum procesu. Czytanie draftu jako nadal oczekującego byłoby błędem. |
| `wiedza/archiwum/PORADNIK_17_CLAUDE_CODE.md` | **STABILNY materiał referencyjny** | l.29-35: audit trail, weryfikacja i kontrola człowieka | To poradnik, nie migawka stanu usługi. Bieżące `tools/hans.py`, `tools/audyt_meldunku.py` i `tools/kontrola_krzyzowa.py` istnieją i realizują opisany wzorzec kontroli. Wiek sam nie obala poradnika. |

### 3. Zaległość dzienników — wdrożenie addytywne

Dodałem do `tools/hans.py` funkcję `sprawdz_zaleglosc_dziennikow` i CLI
`python3 tools/hans.py --dzienniki`. Próg: **1 doba**. Uzasadnienie: to dokładnie
próg, przy którym istniejący `tools/teleport.py --sprawdz` wypisuje „ZALEGŁOŚĆ”;
doba pozwala domknąć sesję, ale nie pozwala kilku kolejnym oknom przez wiele dni
czytać starego przebiegu jako bieżącego.

Kontrola jest również **dołączana do każdego istniejącego trybu CLI Hansa** pod
osobnym kluczem `kontrola_dziennikow`. Nie zmienia znaczenia dotychczasowego pola
`poziom`, nie blokuje, nie wysyła i nie modyfikuje teleportów. `tools/teleport.py`
pozostał nietknięty. Osobne testy są w `tools/test_hans_dzienniki.py`, ponieważ
istniejący `tools/test_hans.py` ma ACL innego użytkownika i nie dał się bezpiecznie
dopisać.

Wynik uruchomienia po zapisie:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p
  'test_hans*.py' -v`: **47 testów, OK**;
- `python3 tools/hans.py --dzienniki`: oba dzienniki istnieją, mają odpowiednio
  0.011 i 0.011 dnia bez wpisu, poziom `OK`, także po uruchomieniu z `/tmp`;
- porównanie AST `HEAD:tools/hans.py` ze stanem roboczym: **22 funkcje przed,
  24 po, usunięte: []**, dodane tylko `_dolacz_kontrole_dziennikow` i
  `sprawdz_zaleglosc_dziennikow`;
- `git diff --check`: brak komunikatu, kod wyjścia 0.

Kontrola Zenka wykryła po pierwszym teście, że ścieżka teleportu fabryki była
względna i uruchomienie z `/tmp` dawało fałszywy alarm. Poprawiłem ją na ścieżkę
absolutną wyprowadzoną z położenia `tools/hans.py` i dodałem test regresyjny CLI
spoza repo. Zenek potwierdził, że starych funkcji nie usunięto i ich przeznaczenia
nie zmieniono; zaznaczył słusznie, że JSON starych trybów jest rozszerzony o nowy
klucz, więc nie jest bajt-w-bajt identyczny.

## HIPOTEZY

1. Największe ryzyko nie leży w plikach jawnie umieszczonych w `archiwum/`, tylko
   w aktywnych dokumentach zatytułowanych „jak jest teraz”: `ARCHITEKTURA.md`,
   `STYL.md`, `PROCEDURY.md` i `DROGA_ROLKA_HUMOR.md`. Mieszają prawidłowe reguły
   z nieaktualnymi silnikami, obsadą albo limitami.
2. Automatyczna kontrola może wiarygodnie wykrywać tylko część nieistniejącego
   stanu: brak ścieżki, brak symbolu w kodzie, wiek pliku, sprzeczne deklaracje,
   supersedowanie oznaczone w nagłówku oraz rozjazd z maszynowym manifestem.
3. Kontrola semantyczna typu „ta zasada już nie obowiązuje” nie jest w pełni
   automatyzowalna bez kanonicznego rejestru relacji `zastępuje/obowiązuje od/status`.
   LLM lub dopasowanie słów może wskazać kandydatów, ale nie może samo wydać
   decyzji. To byłaby pozorna kontrola.

## NIE WIEM

- NIE WIEM, które dokładnie 18 plików obejmował pomiar z 02:12; bieżący dysk daje 20.
- NIE WIEM z samego dysku, czy zewnętrzne posty Facebook 10006/10007/000098 nadal
  istnieją. Pliki lokalne potwierdzają materiał, nie stan serwisu.
- NIE WIEM, czy Tomasz chce później rozdzielić pliki **MIESZANE** na destylat bieżący
  i historię. To decyzja Tomasza; teraz niczego w tych 20 plikach nie poprawiałem.

**Henio**
