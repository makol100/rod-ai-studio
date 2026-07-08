

## ZAMKNIĘTE (08.07.2026, 11:15) — okno NAPRAW w panelu + krytyczna naprawa /reels
Funkcja NAPRAW kompletna: backend (`naprawa.py`, 2 endpointy) + okno w panelu.

**Panel (`panel.html`):** w rozwinietej karcie kazdej rolki - przycisk "🔧 Zglos problem" odslania textarea + "Sprawdz". Po sprawdzeniu: lista scen ktore by sie zmienily (checkbox domyslnie zaznaczony, badge 🖼️obraz/🔊audio, stary vs nowy tekst), przycisk "Zastosuj zaznaczone" z licznikiem aktualizowanym na biezaco. Klik Zastosuj -> `confirm()` z liczba obrazow do wygenerowania (koszt fal.ai) -> `/napraw-zastosuj` -> `loadReels()` odswieza liste. Stan (nowy_scenariusz + zmiany) trzymany w `naprawState` Map w JS, keyed po reel_id.

**KRYTYCZNE ODKRYCIE PO DRODZE:** `/reels` czytal z tabeli SQL `reels`, ktora wypelnia TYLKO stary `generate_text()` (sam tekst, bez wideo) - prawdziwe rolki z pelnym pipelinem (jak 000059) zyja jako foldery `data/reels/NNNNNN/` i NIGDY nie trafialy do tej tabeli. Efekt: `/reels` zawsze zwracal pusta liste, panel nigdy nie pokazywal zadnej karty rolki, wiec cala funkcja NAPRAW bylaby niedostepna mimo poprawnego backendu. Naprawione: `/reels` (w `topics.py`) teraz skanuje `data/reels/` bezposrednio (`_scan_reels_from_disk()`), status="gotowa" jesli istnieje plik wideo (final_napisy_muzyka.mp4/final_with_music.mp4/final.mp4), tytul z pierwszej linii article.md lub pierwszego LEKTOR jako fallback. Zweryfikowane: 20 prawdziwych rolek teraz widocznych, poprawnie posortowane malejaco po ID.

Stara tabela SQL `reels`/`save_reel()`/`list_reels()` w `db/database.py` NIETKNIETE - zostawione dla `generate_text()` (osobna, prostsza funkcja tytul+tekst+hashtagi bez wideo), gdyby ktos jej jeszcze uzywal.

**Zweryfikowane:** JS syntax (`node --check`) czysty, `/reels` zwraca realne dane, cala sciezka Sprawdz+Zastosuj przetestowana wczesniej przez curl na poziomie backendu. Nie przetestowane: klikniecie w prawdziwej przegladarce/telefonie od poczatku do konca (Tomasz powinien sprobowac sam przy okazji).

**FABRYKA ROLEK - stan modeli (patrz tez sekcja wyzej):** Bielik (artykuly/sceny/lektor/tytuly/hashtagi) + llama3.1:8b (NAPRAW + prompty obrazow FLUX). Dwa modele, nie trzy.
