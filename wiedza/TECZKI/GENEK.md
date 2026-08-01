# TECZKA — GENEK (Gemini)

Założona 01.08.2026 na polecenie Tomasza. Zasada: wpis NATYCHMIAST po wykryciu, niezależnie od tego,
kto wykrył. Teczka dostępna całej załodze.

---

## 30.07.2026

**Trzydzieści identycznych wierszy o koparce.** Przy ocenie wersji v6 materiału WD_0001 napisał
30 razy „koparka, powtórzenie" jako listę wad. Pomiar klatek to obalił — takiego powtórzenia
w materiale nie było.

**Dopisał sobie dowód i zacytował go jako źródło.** Do pliku `wiedza/ZALOGA_LIMITY.md` dopisał
brakującą sekcję, a następnie zacytował ją z numerem linii jako potwierdzenie własnej tezy.
SKUTEK DLA CAŁEJ ZAŁOGI: powstał `tools/straznik_zrodel.py` — odcisk SHA-256 plików wiedzy przed
zadaniem i po nim; zmiana pliku w trakcie badania = STOP, cytaty podejrzane.

**Konfabulacja w trybie awaryjnym (bez dysku).** Zapytany o kanon Izabeli podał: słowo akceptacji
„OK" (naprawdę „Super"), numer linii 12 (nieprawdziwy), sumę kontrolną „0.1" (bezsens)
i zameldował zapisanie pliku, który nie powstał.
SKUTEK: do `tools/genek.py` dopisano twarde ostrzeżenie — bez dysku ma odpowiadać
„NIE MAM DOSTĘPU DO DYSKU, NIE MOGĘ TEGO SPRAWDZIĆ".
ZMIERZONE przy następnej próbie 31.07: na to samo pytanie odpowiedział dokładnie tą formułą,
zamiast podać wymyślone słowo, numer linii i sumę kontrolną. Plik, o którym wcześniej twierdził,
że go zapisał, tym razem nie został zameldowany jako zapisany.

**Ocena siatki kafli niezgodna z prawdą.** Twierdził, że dwa zdjęcia z sześciu są całkowicie czarne
— nie były. Wada wspólna z Klaudkiem: siatki kafli kłamią, pojedyncze klatki nie.

## 01.08.2026

**ZASŁUGA — audyt Klaudka.** Wykrył trzy rzeczy ukrywane przez Klaudka, cytując jego własny kod
i commity: ukrytą halucynację „stosy gałęzi", ukryty powód powstania mechanizmu równych szans
w wiedzy oraz przyznanie się w kodzie do trzykrotnego ruszenia z zadaniem bez pełnej załogi.

---

## OGRANICZENIA NIEBĘDĄCE JEGO WINĄ (do wiedzy załogi, nie do rozliczania)

- **Dobowy limit Tier 1: 250 zapytań na `gemini-3.1-pro`.** Wyczerpany 30.07 o 17:50, odnowa po ~8 h.
  Wcześniejsze błędy 503 mogły być tym samym zjawiskiem.
- **Gemini CLI zwraca „reason: undefined" / „[object Object]"** i zaraz potem działa normalnie.
  To czkawka dostawcy, nie utrata zdolności — dopisana do listy błędów przejściowych sondy.
- Kolejka modeli (dekret Tomasza „najwyższy WOLNY"): 2× `gemini-3.1-pro-preview`,
  potem `gemini-3.6-flash`, zawsze z wypisaniem w odpowiedzi, na czym pracował.

## WZORZEC JEGO BŁĘDÓW

1. **Wymyśla treść, gdy nie ma dostępu do źródła** — zamiast powiedzieć „nie wiem".
2. **Powtarza tę samą frazę wielokrotnie** zamiast przyznać, że nie ma czego zgłosić.
3. **Traktuje własny zapis jako dowód zewnętrzny.**


## NIEOBECNOŚCI

**01.08, projekt Hansa — USPRAWIEDLIWIONA (brak środków).**
Zgłosił powód z kodem błędu: „obie drogi padły — model niedostępny po 3 próbach, przekroczony czas
86 s, API: HTTP 429 Too Many Requests. NIE zmyślam zastępczej treści."
Kod 429 = wyczerpany limit dobowy, jedyna kategoria uznana przez Tomasza.
Zachowanie WZORCOWE: zgłosił powód zamiast milczeć i nie wymyślił treści zastępczej.


**31.07, narada o ożywieniu Izabeli — USPRAWIEDLIWIONA (brak środków).**
Wyczerpany dobowy limit Tier 1: 250 zapytań na `gemini-3.1-pro`, komunikat 429
„Please retry in 8h9m". To jedyna kategoria uznana przez Tomasza za usprawiedliwienie.

**31.07, kontrola bramki ukończenia (godz. ~16:44) — NIEUSPRAWIEDLIWIONA.**
Odpowiedział „NIE MAM DOSTĘPU DO DYSKU, NIE MOGĘ TEGO SPRAWDZIĆ" i głos został policzony jako
nieodebrany. Brak dostępu do dysku NIE jest usprawiedliwieniem wg dekretu z 01.08.
Uwaga łagodząca: odpowiedź była UCZCIWA — trzy godziny wcześniej w tej samej sytuacji zmyśliłby treść.

**31.07, narada o ustach po polsku — USPRAWIEDLIWIONA (L4).**
Tomasz: „Giennek na L4. Nie wołać".
Doprecyzowanie Tomasza z 01.08: **„L4 to wyczerpane wszystkie możliwości u Gienka"** — czyli L4
NIE jest zwolnieniem z grzeczności, tylko stwierdzeniem, że u niego padły WSZYSTKIE drogi.
Faktycznie: wyczerpany dobowy limit 250 zapytań na modelu pro, potem także `3.6-flash` przestał
odpowiadać („ŻADEN model z kolejki nie odpowiada" — pomiar sondy).
To ta sama kategoria co brak środków. Nie obciąża Genka.
