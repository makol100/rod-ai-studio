# EGO LITE — ROZPOZNANIE (5.08.2026). WATEK ODLOZONY, NIE ODRZUCONY.

Tomasz podal 5.08 haslo „ego lite" i wskazal GitHub. **Nic nie instalowano.**

## CO TO JEST

**`github.com/citrolabs/ego-lite`** — 8647 gwiazdek, 411 forkow, licencja MIT, JavaScript.
Zalozone **16.04.2026**, ostatnia zmiana **5.08.2026** (bardzo aktywne).
Strona: `https://lite.ego.app`

> *„The fastest browser for AI agents to run browser automation, built for sharing
> your logged-in browser state with your AI"*

**Przegladarka, w ktorej czlowiek i agenci AI pracuja ROWNOLEGLE.** Agenci wykonuja zadania
we wlasnych „Spaces", uzytkownik korzysta ze swojej karty jak zwykle.

**Czym rozni sie od reszty (ich wlasne slowa):** narzedzia typu `browser-use`
i `agent-browser` to frameworki, ktore potrzebuja OSOBNEJ przegladarki do sterowania
i **logowania sie w nich nie przenosza**. Ego lite **dzieli zalogowana sesje**.

## DLACZEGO TO NAS DOTYCZY — REALNE BLOKADY Z 5.08

Tego dnia stanelismy DWA RAZY na tej samej scianie: **czynnosc wymaga zalogowanej przegladarki,
do ktorej Klaudek nie siega.**
1. **Tailscale: 2 trasy czekaja na zatwierdzenie** — trzeba kliknac w `login.tailscale.com`.
   Bez tego urzadzenia w sieci mieszkania na Wybickiego sa nieosiagalne.
2. **Tuya: kod QR** — Tomasz nie moze go zeskanowac TYM SAMYM telefonem, ktory go wyswietla.
   Przez to czujniki bezpieczenstwa byly martwe.

Doszlaby do tego publikacja na Facebooku i zarzadzanie Nabu Casa.

## DLACZEGO ODPADA DZIS — ZMIERZONE

> README, linia 30: *„ego lite runs on macOS today. Windows and Linux are on the roadmap."*

**TYLKO macOS.** Nasz serwer to Linux, komputer Tomasza to Windows (`desktop-tot1520`),
pracuje glownie z telefonu. **Zadna z tych drog nie jest obslugiwana.**

## CZEGO NIE WOLNO PRZEOCZYC, GDY DOJDZIE WINDOWS

1. **BEZPIECZENSTWO.** To narzedzie **dzieli z agentem CALA zalogowana sesje przegladarki** —
   bank, poczta, media spolecznosciowe. To jest jednoczesnie jego sila i jego ryzyko.
   Przed uzyciem rozstrzygnac, na ktorym profilu przegladarki ma dzialac i do czego NIE ma dostepu.
2. **WIEK.** Projekt ma **4 miesiace** (kwiecien 2026) mimo 8647 gwiazdek. Mlode oprogramowanie
   przy dostepie do zalogowanych sesji = ostroznie.
3. **SPRAWDZIC ZRODLO PONOWNIE.** Lekcja z ClawMema tego samego dnia: pakiet o tej samej nazwie
   na PyPI byl INNYM projektem z martwym repozytorium. Przed instalacja potwierdzic,
   ze to `citrolabs/ego-lite`.

## STAN: ODLOZONE. Wrocic, gdy pojawi sie wersja na Windows.
