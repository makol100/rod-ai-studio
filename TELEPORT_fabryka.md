

## ZAMKNIĘTE (08.07.2026, 12:45) — usuwanie rolek + naprawa diagnostyki
- `DELETE /reels/{reel_id}` (topics.py) - kasuje caly folder rolki z dysku (shutil.rmtree), uzywa `znajdz_folder()` z naprawa.py do obslugi paddingu ID. Nieodwracalne, numeracja pozostalych rolek bez zmian (zwykle usuniecie folderu, zero renumeracji).
- Panel: czerwona/szara ikonka kosza w naglowku KAZDEJ karty rolki (widoczna bez rozwijania) - klik -> `confirm()` z tytulem rolki -> DELETE -> `loadReels()` odswieza liste.
- Naprawiono `/host/status` - sprawdzal martwa sciezke `/app/prompts/prompts.py` (stara struktura sprzed reorganizacji), teraz `/app/src/images/prompts.py`. Diagnostyka "PROMPTS" w panelu bedzie teraz pokazywac true.
- **Uwaga dla przyszlej instancji:** jesli Tomasz zglosi "brak rolek" w panelu mimo ze wiesz ze /reels dziala (sprawdz curlem) - to zwykle stara, niezaladowana na nowo karta w przegladarce. Kaz mu kliknac ikone odswiezania obok "OSTATNIE ROLKI" albo przeladowac strone, zanim zaczniesz szukac buga.
