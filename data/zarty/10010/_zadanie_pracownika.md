# ZADANIE DLA PRACOWNIKA — prompty Veo w REŻIMIE STATYCZNYM (odcinek 10010)

Rola: pracownik w pętli dwumodelowej. Budujesz, nie decydujesz. Niczego nie zapisujesz na dysk, nie wykonujesz poleceń zmieniających stan — czytasz pliki i zwracasz wynik na stdout. Odpowiadasz po polsku (same prompty po angielsku, jak w oryginałach).

## Przeczytaj najpierw (w całości)
1. data/zarty/10010/KANON.md — scenariusz źródłowy; kwestie dialogowe są ŚWIĘTE, verbatim co do znaku
2. data/zarty/10010/_klipy_batch.json — obecne prompty k01/k02/k03/k05/k06 (k02, k05, k06 przepisujesz)
3. wiedza/PRZEKAZANIE_2026-07-26_10010.md — sekcja DIAGNOZA: jak i dlaczego obecne prompty poległy
4. (opcjonalnie) data/zarty/10010/raporty/ — jeśli chcesz zobaczyć stary prompt k04, szukaj w raportach preflight

## Sedno problemu
Klipy generuje Veo 3.1 FLF (first-last-frame): model dostaje TYLKO pierwszą i ostatnią klatkę, środek klipu jest wolny. Każdy dynamiczny czasownik w prompcie ("legs JERK violently", "fist TIGHTENS", "twitch") to zaproszenie do akrobatyki w środku — dziś tak rozpadły się sceny (ścisk znikał, postać łaziła po drzewie, bohater podciągał własne spodnie). Reżim, który DZIAŁAŁ w odcinkach 10008/10009: postać trzyma dokładną pozę z kadru przez cały klip, rusza się tylko twarz przy mówieniu.

## Twarde zasady przepisania (wszystkie obowiązkowe)
1. Baza każdego promptu: postać "holds the exact pose/grip/framing from the first frame for the entire clip". Poza i chwyt DOMINUJĄ nad wszystkim.
2. ZERO czasowników dynamicznych i ruchu ciała: jerk, tighten, twitch, shake, whiten, struggle, kick, thrash, rush, violently, suddenly itp. Szarpanie nóg, atak, ściskanie w ruchu — WYRZUCIĆ; dźwięk ataku dogra montaż (SFX), nie opisuj go.
3. Maksymalnie JEDNA mikroakcja na klip, wyłącznie gdy konieczna dla sensu sceny.
4. W klipach z kwestią rusza się WYŁĄCZNIE twarz/usta mówiącego. Reszta ciała i wszystko w kadrze zamrożone.
5. Kwestie po polsku, VERBATIM z KANON.md, z polskimi znakami, w cudzysłowie. DOKŁADNIE JEDNA para cudzysłowów w całym prompcie — opisy głosu i dźwięków bez cudzysłowów.
6. Z oryginałów zachować co do tokenu: opis tożsamości postaci ("A man of about fifty... THE SAME MAN with THE SAME FACE for the entire clip, his facial features never change"), bloki opisu głosu, "speaking fluent native Polish with a natural Polish accent", "No captions, no subtitles, no on-screen text", scenografię nocnego sadu.
7. Jeden mówca na klip.

## Specyfikacja klipów do napisania
- **k02** (niemy): Tomek stoi pod jabłonią, ręka w górze, pięść zaciśnięta między dwiema nogawkami zwisającymi z korony; osoba w koronie CAŁKOWICIE niewidoczna. Nikt nie mówi. Chwyt i poza trzymane przez cały klip — bez ruchu nogawek, bez szarpania.
- **k04** (mówca: BOHATER + głos z korony): ta sama poza chwytu co k02. Tomek patrzy w górę i mówi kwestię z kanonu sceny 4: "Gadaj, pókim dobry, ktoś ty?!" (przez zaciśnięte zęby, wściekły, powolny, groźny — zwykły niski męski głos). Z ukrytej korony słychać krótki wysoki pisk bólu (opisz bez cudzysłowu, bez ruchu nogawek).
- **k05** — DWA WARIANTY:
  - **k05a** (do obecnego kadru, w którym gumowiec wisi w powietrzu): ekstremalne zbliżenie wściekłej twarzy Tomka, kwestia "No gadaj draniu, ktoś ty?!" (krzyk, maksymalna wściekłość); JEDYNA mikroakcja: pojedynczy gumowiec spada pionowo w dół przez kadr, raz, i znika — nic poza tym się nie rusza.
  - **k05b** (do ewentualnego kadru po edycji, gumowiec już na ziemi): to samo zbliżenie i kwestia, ZERO mikroakcji.
- **k06** (mówca: JOZEK z offu): poza jak k02 — Tomek osłupiały (brwi w górę, oczy szeroko, usta lekko otwarte), NIE MÓWI. Z ukrytej korony pada kwestia "To ja... Józek... niemowa ze wsi!" głosem niezwykle piskliwym, nienaturalnie wysokim, zduszonym, łamiącym się, jak wyciśnięty z resztek sił. Nogawki NIERUCHOME (żadnego "final twitch").

## Format wyniku (dokładnie tak)
1. Blok ```json``` — struktura identyczna jak _klipy_batch.json, klucze: k02, k04, k05a, k05b, k06 (pola: mowca, niemy/kwestia, prompt).
2. Sekcja "## RYZYKA" — wypunktuj każde miejsce, gdzie mimo przepisania widzisz ryzyko ruchu w środku klipu, konflikt z FLF albo z zasadami wyżej.
