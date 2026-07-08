

## POPRAWKA (08.07.2026, 13:25) — prawdziwa przyczyna "brak rolek" znaleziona
Dzisiejsza wczesniejsza "naprawa" /reels (skanowanie dysku) byla NIEPELNA - poprawilem backend, ale nie sprawdzilem czy frontend poprawnie odpakowuje odpowiedz. `/reels` zwraca `{"status":"ok","reels":[...]}`, a `loadReels()` robilo `let reels = await api('/reels'); if(!Array.isArray(reels)) reels=[];` - poniewaz CALY obiekt {status,reels} nigdy nie jest tablica, ZAWSZE ladowalo na reels=[], niezaleznie od realnych danych w srodku. Bug istnial od rana (od zbudowania panelu), moja poranna "naprawa" backendu tego nie ujawnila bo testowalem tylko surowym curlem, nie symulujac dokladnej logiki JS.

Naprawione: `loadReels()` teraz poprawnie odpakowuje `.reels` z odpowiedzi (obsluguje tez demo-mode ktory zwraca gola tablice). Zweryfikowane przez node -e symulujacy DOKLADNIE logike przegladarki (nie tylko surowy endpoint) - 20 rolek poprawnie wyodrebnionych.

**LEKCJA na przyszlosc:** przy debugowaniu "X nie dziala w panelu" nie wystarczy sprawdzic czy backend endpoint zwraca dobre dane (curl) - trzeba tez zweryfikowac, czy JS PO STRONIE KLIENTA poprawnie ja konsumuje/odpakowuje. To dwa oddzielne miejsca gdzie bug moze siedziec.
