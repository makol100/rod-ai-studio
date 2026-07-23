from pathlib import Path
import threading

ROOT = Path("/root/rod-ai-studio/data/reels")
_LOCK = threading.Lock()  # Dyskusja 09.07.2026: naprawia race condition -


def create_reel_folder():
    """Tworzy nowy, unikalny folder rolki.

    NAPRAWIONE 09.07.2026: bez _LOCK dwa niemal-jednoczesne wywolania (np.
    szybkie podwojne kliknieice 'Generuj' albo dwie karty przegladarki) moglyby
    obie odczytac ta sama liste folderow, obliczyc TEN SAM next_id, i - jesli
    drugi mkdir() zdazyl trafic milisekunde po pierwszym utworzeniu ale przed
    zapisaniem podfolderow - doprowadzic do dwoch rownoleglych watkow
    generate_reel() piszacych do TEGO SAMEGO folderu (dokladnie to zaobserwowane
    w rolce 000077 - dwa pelne przebiegi artykul->scenariusz->checkpoint w
    jednym folderze, drugi ok. 2.5 min po pierwszym). Lock serializuje
    'odczytaj najwyzszy numer -> utworz folder' w jedna atomowa operacje."""
    with _LOCK:
        ROOT.mkdir(parents=True, exist_ok=True)
        ids = [int(p.name) for p in ROOT.iterdir() if p.is_dir() and p.name.isdigit()]
        next_id = max(ids, default=0) + 1
        folder = ROOT / f"{next_id:06d}"
        folder.mkdir()
        (folder/"images").mkdir()
        (folder/"audio").mkdir()
        (folder/"video").mkdir()
        return folder
