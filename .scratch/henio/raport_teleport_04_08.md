# RAPORT HENIA — ZADANIE 1: ROZSZERZENIE NARZĘDZI O MONITORING TELEPORTÓW

Data: 04.08.2026 02:25 CEST

## STAN ZASTANY

Monitoring zaległości dzienników JEST JUŻ WBUDOWANY w `tools/hans.py`. Został dodany
podczas budowy Hansa (2-3.08.2026) przez całą załogę. Oto co jest:

### Funkcje (działające, przetestowane):

1. **`sprawdz_zaleglosc_dziennikow()`** (linie 279-323) — sprawdza wiek obu teleportów.
   - Próg: `PROG_ZALEGLOSCI_DZIENNIKA_DNI = 1.0` (jedna doba)
   - Zwraca raport JSON z poziomem OK/ALERT, listą dzienników i rozbieżnościami.

2. **`_dolacz_kontrole_dziennikow()`** (linie 326-330) — automatycznie dołącza kontrolę
   dzienników do KAŻDEGO wyniku Hansa. Oznacza to: każde uruchomienie `hans.py --narada`,
   `--niedokonczone-slady` czy `--srodowisko-henia` MA W SOBIE kontrolę teleportów.

3. **CLI: `--dzienniki`** (linia 884) — dedykowany przełącznik do sprawdzania samych dzienników.

### Test: 32/32 OK (w tym testy_kontroli_dziennikow)

## PRÓG — UZASADNIENIE

**Próg: 1.0 dnia (24 godziny)**

Uzasadnienie (z komentarza w kodzie, linie 42-45):
> "Doba daje prowadzącemu całą sesję na domknięcie wpisu, ale nie pozwala, aby drugie
> okno przez kilka dni uznawało stary stan za bieżący."

Dlaczego NIE krócej (np. 12h):
- Teleport jest dziennikiem PRZEBIEGU, nie logiem minutowym. Sesja może trwać kilka godzin.
- Sesja kończy się wpisem — wymaganie wpisu co 12h karałoby za długą sesję.

Dlaczego NIE dłużej (np. 3 dni):
- Klaudek zaniedbał teleport na 8,4 dnia i to wystarczyło, żeby nowe okno dostało stan
  sprzed tygodnia. 3 dni to już poważna luka.
- 1 dzień to ZAWSZE maksymalnie 1 sesja opóźnienia — nowe okno następnego dnia ma
  stan maksymalnie 1 dzień wstecz.

**Podtrzymuję 1.0 dnia jako właściwy próg.**

## CO DZIAŁA AUTOMATYCZNIE

Każde wywołanie Hansa (cokolwiek robi) automatycznie sprawdza teleporty przez
`_dolacz_kontrole_dziennikow`. To znaczy: zaległość NIE MOŻE być niewidzialna —
każdy raport Hansa ją zawiera.

Przykład (właśnie zmierzone):
```
python3 tools/hans.py --niedokonczone-slady
→ w wyniku jest "kontrola_dziennikow": { "poziom": "OK", "dni_bez_wpisu": 0.009 }
```

## CO JEST POZA HANSEM (teleport.py)

`tools/teleport.py --sprawdz` pozostaje NIETKNIĘTY jako kanoniczne narzędzie teleportu.
Hans nie zastępuje go — dodaje własną, niezależną kontrolę.

Zmierzony wynik:
```
fabryka          bez wpisu: 0.0 dnia
Home Assistant   bez wpisu: 0.0 dnia
```

## WNIOSEK

**Narzędzia Henia już pilnują zaległości dzienników.** Nie trzeba nic dodawać —
funkcjonalność jest wbudowana, przetestowana (32/32 testów OK) i automatycznie
dołączana do każdego raportu Hansa. Próg 1.0 dnia jest uzasadniony i skuteczny.

Podpis: HENIO
