import re
import json
from pathlib import Path
from datetime import datetime
import subprocess
import shutil
from fastapi import APIRouter, Body, HTTPException, UploadFile, File

from src.ai.ollama import generate
from src.db.database import save_reel, list_reels
from src.scenes.generator import generate_scenes
from src.images.prompts import generate_image_prompts
from src.reels.pipeline import generate_reel, render_from_scenes, wznow_po_checkpoincie
from src.naprawa import znajdz_folder, audytuj_checkpoint

router = APIRouter()


@router.get("/topics")
def get_topics():
    return {
        "status": "ok",
        "topics": [
            "5 ciekawostek o...",
            "3 błędy, które popełnia każdy",
            "Czy wiedziałeś, że...?",
            "Największy mit na temat...",
            "TOP 10 faktów"
        ]
    }


def clean_hashtags(raw: str):
    tags = re.findall(r"#[A-Za-zÀ-ž0-9_]+", raw)
    out = []
    for tag in tags:
        if tag.lower() not in [x.lower() for x in out]:
            out.append(tag)
    return " ".join(out[:10])


@router.post("/generate")
def generate_text(data: dict = Body(...)):
    prompt = data["prompt"]

    text = generate(prompt)

    title_prompt = (
        "Wygeneruj krótki, chwytliwy tytuł do rolki na podstawie tego tekstu. "
        "Zwróć tylko sam tytuł, bez cudzysłowów i bez dodatkowego komentarza:\n\n"
        + text
    )
    title = generate(title_prompt).strip()

    hashtags_prompt = (
        "Jesteś generatorem hashtagów Instagrama.\n"
        "Wygeneruj dokładnie 10 trafnych hashtagów.\n"
        "Odpowiedz WYŁĄCZNIE hashtagami.\n"
        "Każdy hashtag musi zaczynać się od #.\n"
        "Oddziel je pojedynczą spacją.\n"
        "Nie dodawaj żadnych zdań, komentarzy ani wyjaśnień.\n\n"
        + text
    )
    hashtags = clean_hashtags(generate(hashtags_prompt))

    save_reel(prompt, title, text, hashtags)

    return {
        "status": "ok",
        "title": title,
        "text": text,
        "hashtags": hashtags,
        "saved": True
    }


REELS_DIR = Path("/root/rod-ai-studio/data/reels")


def _scan_reels_from_disk(limit=20):
    """
    Prawdziwe rolki (z pelnym pipelinem: sceny/obrazy/audio/wideo) zyja jako
    foldery na dysku data/reels/NNNNNN/, NIE w tabeli SQL 'reels' (ta tabela
    sluzy tylko staremu /generate-text - sam tekst bez wideo). Panel potrzebuje
    tych z dysku, wiec /reels skanuje folder zamiast pytac baze.
    """
    if not REELS_DIR.is_dir():
        return []
    wyniki = []
    for d in REELS_DIR.iterdir():
        if not d.is_dir() or not d.name.isdigit():
            continue
        scenes_path = d / "scenes.txt"
        if not scenes_path.is_file():
            continue

        title = ""
        article_path = d / "article.md"
        if article_path.is_file():
            try:
                linie = article_path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
                if linie:
                    title = linie[0].lstrip("#").strip()[:80]
            except Exception:
                pass
        if not title:
            try:
                txt = scenes_path.read_text(encoding="utf-8", errors="ignore")
                m = re.search(r"LEKTO\w*:\s*\n?\s*(.+)", txt)
                if m:
                    title = m.group(1).strip().strip('"').strip("*")[:80]
            except Exception:
                pass

        video_dir = d / "video"
        has_video = False
        if video_dir.is_dir():
            for cand in ("final_napisy_muzyka.mp4", "final_with_music.mp4", "final.mp4"):
                if (video_dir / cand).is_file():
                    has_video = True
                    break

        try:
            created = datetime.fromtimestamp(scenes_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        except Exception:
            created = ""

        warning = (d / "WARNING.json").is_file()
        opublikowana = (d / "opublikowano.txt").is_file()
        grupy_fb = _wczytaj_grupy_fb(d)

        # NAPRAWIONE 10.07.2026 (Dyskusja) - stary kod patrzyl TYLKO na
        # istnienie wideo, ignorujac status.json calkowicie. Rolka
        # celowo/trwale przerwana przez Tomasza (STOP.flag/"przerwano")
        # pokazywala sie jako "w trakcie" NA ZAWSZE, mylaco sugerujac ze
        # cos sie jeszcze dzieje mimo ze nic juz nigdy sie nie wydarzy.
        status = "gotowa" if has_video else "w trakcie"
        if not has_video:
            try:
                stan = json.loads((d / "status.json").read_text(encoding="utf-8"))
                etap = stan.get("etap", "")
                if etap == "przerwano":
                    status = "przerwana"
                elif etap == "blad":
                    status = "błąd"
                elif etap == "zatrzymano_walidacja":
                    status = "zatrzymana (walidacja)"
                elif etap == "checkpoint":
                    status = "pauza" if (d / "PAUZA.flag").is_file() else "checkpoint"
            except Exception:
                pass

        wyniki.append({
            "id": int(d.name),
            "title": title or ("Rolka #" + d.name),
            "prompt": title,
            "text": "",
            "hashtags": "",
            "status": status,
            "created_at": created,
            "warning": warning,
            "opublikowana": opublikowana,
            "grupy_fb": grupy_fb,
        })

    wyniki.sort(key=lambda r: r["id"], reverse=True)
    return wyniki[:limit]


@router.get("/reels")
def get_reels():
    return {
        "status": "ok",
        "reels": _scan_reels_from_disk()
    }


@router.post("/reels/{reel_id}/opublikowano")
def oznacz_opublikowana(reel_id: str):
    """Oznacza rolke jako opublikowana na Facebooku - prosty znacznik
    plikowy (Dyskusja 09.07.2026, Tomasz publikuje recznie, wklejajac
    wygenerowany opis)."""
    from src.naprawa import znajdz_folder
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    (folder / "opublikowano.txt").write_text(
        datetime.now().strftime("%Y-%m-%d %H:%M"), encoding="utf-8"
    )
    return {"status": "ok", "reel_id": reel_id, "opublikowana": True}


@router.delete("/reels/{reel_id}/opublikowano")
def odznacz_opublikowana(reel_id: str):
    """Cofa oznaczenie 'opublikowana' (np. pomylka)."""
    from src.naprawa import znajdz_folder
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    (folder / "opublikowano.txt").unlink(missing_ok=True)
    return {"status": "ok", "reel_id": reel_id, "opublikowana": False}


GRUPY_FB = {
    "rod": "Rodzinne Ogrody Działkowe",
    "rodcp": "Rodzinne Ogródki Działkowe - Cała Polska",
    "dio": "Działkowicze i Ogrodnicy",
}


def _wczytaj_grupy_fb(folder) -> dict:
    """Odczytuje ktore grupy FB juz zaznaczone jako udostepnione (Dyskusja
    10.07.2026). To wylacznie RECZNE oznaczenie przez Tomasza - Meta
    zablokowala API do Grup w 2024, wiec system NIE MA jak sam wykryc czy
    cos zostalo udostepnione w grupie, to musi zaznaczyc czlowiek."""
    import json
    p = folder / "grupy_fb.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


@router.post("/reels/{reel_id}/grupa/{grupa_id}")
def oznacz_grupe_fb(reel_id: str, grupa_id: str):
    """Zaznacza rolke jako udostepniona w danej grupie FB (recznie przez
    Tomasza, patrz komentarz przy _wczytaj_grupy_fb)."""
    import json
    from src.naprawa import znajdz_folder
    if grupa_id not in GRUPY_FB:
        raise HTTPException(status_code=400, detail=f"Nieznana grupa: {grupa_id}")
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    dane = _wczytaj_grupy_fb(folder)
    dane[grupa_id] = datetime.now().strftime("%Y-%m-%d %H:%M")
    (folder / "grupy_fb.json").write_text(json.dumps(dane, ensure_ascii=False), encoding="utf-8")
    return {"status": "ok", "reel_id": reel_id, "grupy": dane}


@router.delete("/reels/{reel_id}/grupa/{grupa_id}")
def odznacz_grupe_fb(reel_id: str, grupa_id: str):
    """Cofa oznaczenie udostepnienia w danej grupie FB."""
    import json
    from src.naprawa import znajdz_folder
    if grupa_id not in GRUPY_FB:
        raise HTTPException(status_code=400, detail=f"Nieznana grupa: {grupa_id}")
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    dane = _wczytaj_grupy_fb(folder)
    dane.pop(grupa_id, None)
    (folder / "grupy_fb.json").write_text(json.dumps(dane, ensure_ascii=False), encoding="utf-8")
    return {"status": "ok", "reel_id": reel_id, "grupy": dane}


@router.delete("/reels/{reel_id}")
def delete_reel(reel_id: str):
    """Usuwa caly folder rolki z dysku (scenariusz, obrazy, audio, napisy, wideo).
    Nieodwracalne. Numeracja pozostalych rolek sie nie zmienia."""
    from src.naprawa import znajdz_folder
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    shutil.rmtree(folder)
    return {"status": "ok", "deleted": reel_id}


@router.post("/generate-scenes")
def generate_scenes_endpoint(data: dict = Body(...)):
    return {"status": "ok", "scenes": generate_scenes(data["text"], data.get("scene_count"))}


@router.post("/generate-image-prompts")
def generate_image_prompts_endpoint(data: dict = Body(...)):
    return {
        "status": "ok",
        "prompts": generate_image_prompts(data["scenes"])
    }


@router.post("/generate-reel-async")
def generate_reel_async_endpoint(data: dict = Body(...)):
    """Wersja NIEBLOKUJACA /generate-reel - tylko dla panelu (prawdziwy
    pasek postepu). NIGDY nie uzywac z n8n - to zaklada blokujace wywolanie
    i czeka na gotowe wideo przed publikacja na FB. Ustalone w Dyskusji
    08.07.2026, zasada 'weryfikacja nie halucynacja'."""
    import threading
    from src.reels.storage import create_reel_folder
    from src.reels.pipeline import generate_reel

    tryb = "organizm"
    topic_id = data.get("topic_id")
    if topic_id:
        from src.db.database import get_connection
        conn = get_connection()
        row = conn.execute(
            "SELECT t.tryb_override AS ov, c.tryb AS cat_tryb "
            "FROM topics t JOIN categories c ON c.id = t.category_id WHERE t.id = ?",
            (topic_id,)
        ).fetchone()
        conn.close()
        if row:
            tryb = row["ov"] or row["cat_tryb"] or "organizm"

    folder = create_reel_folder()
    reel_id = folder.name
    prompt = data["prompt"]
    scene_count = data.get("scene_count")

    tryb_jezykowy = data.get("tryb_jezykowy", "pl")

    def _uruchom():
        generate_reel(prompt, scene_count, tryb=tryb, folder=folder, tryb_jezykowy=tryb_jezykowy)

    threading.Thread(target=_uruchom, daemon=True).start()
    return {"reel_id": reel_id, "status": "started"}


@router.post("/uwolnij-pamiec")
def uwolnij_pamiec_endpoint():
    """Zwalnia WSZYSTKIE modele aktualnie zaladowane w Ollama (keep_alive=0).
    Przycisk awaryjny w panelu - Tomasz moze to zrobic sam, bez SSH, kiedy
    zobaczy krytyczny RAM na pasku zdrowia. Ustalone 08.07.2026."""
    import requests as req
    zwolnione = []
    try:
        resp = req.get("http://host.docker.internal:11434/api/ps", timeout=5)
        modele = resp.json().get("models", [])
    except Exception as e:
        return {"status": "error", "error": f"Nie mozna polaczyc z Ollama: {e}"}

    for m in modele:
        nazwa = m.get("name")
        if not nazwa:
            continue
        try:
            req.post(
                "http://host.docker.internal:11434/api/generate",
                json={"model": nazwa, "keep_alive": 0},
                timeout=15,
            )
            zwolnione.append(nazwa)
        except Exception as e:
            pass

    return {"status": "ok", "zwolnione": zwolnione, "liczba": len(zwolnione)}


@router.get("/system-health")
def system_health_endpoint():
    """Zywe dane obciazenia VPS - CPU/RAM/dysk. Ustalone 08.07.2026 po
    powtarzajacych sie dzis OOM-killach - Tomasz chce to widziec na biezaco
    w panelu, nie tylko przez SSH."""
    import os, shutil

    meminfo = {}
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    meminfo[parts[0].strip()] = int(parts[1].strip().split()[0])
    except Exception:
        pass
    total_kb = meminfo.get("MemTotal", 0)
    avail_kb = meminfo.get("MemAvailable", 0)
    used_kb = max(total_kb - avail_kb, 0)
    ram_percent = round(100 * used_kb / total_kb, 1) if total_kb else 0

    try:
        load1, load5, load15 = os.getloadavg()
    except Exception:
        load1 = load5 = load15 = 0
    cpu_count = os.cpu_count() or 1
    cpu_percent_approx = min(round(100 * load1 / cpu_count, 1), 100)

    try:
        disk = shutil.disk_usage("/")
        disk_percent = round(100 * disk.used / disk.total, 1)
        disk_used_gb = round(disk.used / 1024 / 1024 / 1024, 1)
        disk_total_gb = round(disk.total / 1024 / 1024 / 1024, 1)
    except Exception:
        disk_percent = disk_used_gb = disk_total_gb = 0

    return {
        "ram_percent": ram_percent,
        "ram_used_gb": round(used_kb / 1024 / 1024, 2),
        "ram_total_gb": round(total_kb / 1024 / 1024, 2),
        "cpu_percent_approx": cpu_percent_approx,
        "cpu_load1": round(load1, 2),
        "cpu_count": cpu_count,
        "disk_percent": disk_percent,
        "disk_used_gb": disk_used_gb,
        "disk_total_gb": disk_total_gb,
    }


@router.get("/aktywne-generowanie")
def aktywne_generowanie_endpoint():
    """Skanuje WSZYSTKIE foldery rolek i znajduje ta, ktora generuje sie
    TERAZ - niezaleznie od tego co ja uruchomilo (przycisk w panelu,
    skrypt testowy, n8n, cokolwiek). Uzywane zeby panel pokazywal realny
    pasek postepu nawet gdy TA sesja przegladarki nie klikala "Generuj".
    Ustalone w Dyskusji 08.07.2026."""
    import json, time
    if not REELS_DIR.is_dir():
        return {"aktywna": None}
    KONCOWE = {"gotowe", "blad", "zatrzymano_walidacja", "przerwano"}  # przerwano dodane 09.07.2026 - bug: STOP nie byl uznawany za koniec
    PROG_MAX_WIEK_S = 20 * 60  # 20 minut - dluzej niz to = uznajemy za porzucone/martwe

    najnowsza = None
    for d in REELS_DIR.iterdir():
        if not d.is_dir() or not d.name.isdigit():
            continue
        sp = d / "status.json"
        if not sp.is_file():
            continue
        try:
            dane = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue
        etap = dane.get("etap")
        if etap in KONCOWE:
            continue
        if etap == "checkpoint" and ((d / "STOP.flag").exists() or (d / "PAUZA.flag").exists()):
            continue  # martwy/wstrzymany checkpoint - user kliknal Totalny STOP albo Pauze,
            # zaden watek go juz nie obsluguje, nie ma co straszyc panelu (Dyskusja 09.07/10.07.2026)
        if etap != "checkpoint":  # checkpoint czeka na czlowieka - nie ma limitu wieku
            wiek = time.time() - sp.stat().st_mtime
            if wiek > PROG_MAX_WIEK_S:
                continue  # zbyt stare, prawdopodobnie porzucone po crashu
        if najnowsza is None or sp.stat().st_mtime > najnowsza[1]:
            najnowsza = (d.name, sp.stat().st_mtime, dane)

    if najnowsza is None:
        return {"aktywna": None}
    reel_id, _, dane = najnowsza
    return {"aktywna": reel_id, "status": dane}


@router.post("/reel-stop/{reel_id}")
def reel_stop(reel_id: str):
    """Przerwij aktywne generowanie (Dyskusja 09.07.2026). Kooperacyjne -
    ustawia plik-flage sprawdzana miedzy obrazami w pipeline.py, wiec
    zatrzymuje sie PRZED kolejnym kosztownym wywolaniem fal.ai, a nie w
    trakcie (nie przerywa polwykonanego zapisu pliku)."""
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    (folder / "STOP.flag").write_text("stop", encoding="utf-8")
    # Totalny STOP (Dyskusja 09.07.2026): oznacza status od razu, bo na
    # checkpoincie nic aktywnie nie leci w petli - sama flaga plikowa
    # nic by nie zatrzymala, dopoki ktos by nie kliknal OK. Nadpisanie
    # statusu blokuje to z gory + jest natychmiast widoczne w panelu.
    import json, datetime
    try:
        (folder / "status.json").write_text(
            json.dumps({"etap": "przerwano", "extra": {"powod": "STOP uzytkownika"}, "ts": datetime.datetime.now().isoformat()}, ensure_ascii=False),
            encoding="utf-8"
        )
    except Exception:
        pass
    return {"status": "ok", "reel_id": folder.name}


@router.post("/reel-checkpoint/{reel_id}/pauza")
def reel_checkpoint_pauza(reel_id: str):
    """Pauza (Dyskusja 10.07.2026, naprawa bledu auto-otwierania okna).
    W odroznieniu od Totalny STOP, NIE zmienia status.json - checkpoint
    zostaje checkpointem, to legalny odwracalny stan czekajacy na czlowieka.
    Jedyna rola: zapisac PAUZA.flag, zeby /aktywne-generowanie przestalo
    zglaszac ta rolke jako 'aktywna' - to byla prawdziwa przyczyna ze okno
    checkpointu wyskakiwalo samo co ok. 15s (heartbeat checkAktywneGenerowanie
    w panelu), bo Pauza nigdy wczesniej nie mowila backendowi nic."""
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    (folder / "PAUZA.flag").write_text("pauza", encoding="utf-8")
    return {"status": "ok", "reel_id": folder.name}


@router.post("/reel-checkpoint/{reel_id}/wznow")
def reel_checkpoint_wznow(reel_id: str):
    """Wznow checkpoint po Pauzie ALBO po Totalnym STOP (Dyskusja 10.07.2026 -
    Tomasz: "Stop to Stop ale odwracalne po przycisnieciu edytuj"). Usuwa obie
    mozliwe flagi + przywraca status.json na checkpoint z poprawna kolejnoscia
    (pl/en) czytana z tryb_jezykowy.txt. Aktywowane WYLACZNIE recznym
    przyciskiem przy rolce na liscie - nigdy automatycznie."""
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    (folder / "STOP.flag").unlink(missing_ok=True)
    (folder / "PAUZA.flag").unlink(missing_ok=True)
    tryb_jezykowy = _odczytaj_tryb_jezykowy(folder)
    kolejnosc = "en" if tryb_jezykowy in ("en_pl", "czysty") else "pl"
    import json, datetime
    (folder / "status.json").write_text(
        json.dumps({"etap": "checkpoint", "extra": {"warning": False}, "ts": datetime.datetime.now().isoformat(), "kolejnosc": kolejnosc}, ensure_ascii=False),
        encoding="utf-8"
    )
    return {"status": "ok", "reel_id": folder.name}


@router.get("/live-log")
def live_log_endpoint(linie: int = 200):
    """Ostatnie linie logu pipeline'u na zywo (Dyskusja 09.07.2026 - 'jak w
    Termius'). To dokladnie ten sam strumien co docker logs -f fabryka-api,
    tylko dostepny z panelu bez SSH."""
    from pathlib import Path as _Path
    log_path = _Path("/root/rod-ai-studio/data/live.log")
    if not log_path.is_file():
        return {"linie": []}
    try:
        tekst = log_path.read_text(encoding="utf-8")
    except Exception:
        return {"linie": []}
    wszystkie = tekst.splitlines()
    return {"linie": wszystkie[-linie:]}


def _odczytaj_tryb_jezykowy(folder):
    """Prawdziwy tryb jezykowy ze znacznika zapisanego przy starcie generowania
    (Dyskusja 09.07.2026) - dokladniejszy niz zgadywanie z obecnosci plikow,
    bo od 'czysty_bielik' mamy wiecej niz dwie sciezki zapisujace do scenes.txt.
    Fallback na stare zgadywanie (po plikach) dla rolek sprzed wprowadzenia znacznika."""
    znacznik = folder / "tryb_jezykowy.txt"
    if znacznik.is_file():
        try:
            wartosc = znacznik.read_text(encoding="utf-8").strip()
            if wartosc:
                return wartosc
        except Exception:
            pass
    scenes_en_p = folder / "scenes_en.txt"
    scenes_pl_p = folder / "scenes.txt"
    return "en_pl" if (scenes_en_p.is_file() and not scenes_pl_p.is_file()) else "pl"


@router.get("/reel-checkpoint/{reel_id}")
def reel_checkpoint_get(reel_id: str):
    """Zwraca artykul + scenariusz do recznej weryfikacji PRZED produkcja
    obrazow/wideo (kosztowna czesc). Dyskusja 09.07.2026 - po incydencie
    z rolka 000068 (scenariusz odjechal od tematu, pipeline lecial dalej
    i zaczal placic za fal.ai zanim ktokolwiek to zobaczyl)."""
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")

    import json
    status_p = folder / "status.json"
    etap = None
    if status_p.is_file():
        try:
            etap = json.loads(status_p.read_text(encoding="utf-8")).get("etap")
        except Exception:
            pass

    article_p = folder / "article.md"
    tryb_jezykowy = _odczytaj_tryb_jezykowy(folder)
    # TYLKO en_pl/czysty (Qwen) czytaja scenes_en.txt. "czysty_bielik" i zwykla
    # "pl" zawsze scenes.txt (po polsku) - NIGDY angielski plik (Dyskusja 09.07.2026).
    scenariusz_p = (folder / "scenes_en.txt") if tryb_jezykowy in ("en_pl", "czysty") else (folder / "scenes.txt")

    warning = None
    warn_p = folder / "WARNING.json"
    if warn_p.is_file():
        try:
            warning = json.loads(warn_p.read_text(encoding="utf-8"))
        except Exception:
            pass

    prompts_p = folder / "prompts.txt"

    przeliczanie = (folder / "przeliczanie.lock").is_file()
    return {
        "przeliczanie": przeliczanie,
        "reel_id": folder.name,
        "etap": etap,
        "tryb_jezykowy": tryb_jezykowy,
        "article": article_p.read_text(encoding="utf-8") if article_p.is_file() else "",
        "scenariusz": scenariusz_p.read_text(encoding="utf-8") if scenariusz_p.is_file() else "",
        "prompty_obrazow": prompts_p.read_text(encoding="utf-8") if prompts_p.is_file() else "",
        "prompty_ts": prompts_p.stat().st_mtime if prompts_p.is_file() else None,
        "warning": warning,
    }


@router.post("/reel-checkpoint/{reel_id}/zapisz")
def reel_checkpoint_zapisz(reel_id: str, data: dict = Body(...)):
    """'Wroc do poprawy scenariusza' - zapisuje recznie poprawiony tekst
    na dysku, ALE NIE rusza produkcji. Checkpoint zostaje otwarty do
    ponownego sprawdzenia."""
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    scenariusz = data.get("scenariusz", "")
    if not scenariusz.strip():
        raise HTTPException(status_code=400, detail="Pusty scenariusz")

    tryb_jezykowy = _odczytaj_tryb_jezykowy(folder)
    target = (folder / "scenes_en.txt") if tryb_jezykowy in ("en_pl", "czysty") else (folder / "scenes.txt")
    target.write_text(scenariusz, encoding="utf-8")

    # Scenariusz sie zmienil - stare prompty obrazow juz nie pasuja.
    # NAPRAWIONE 14.07.2026: przeliczanie w WATKU zamiast synchronicznie -
    # przy 10 scenach Bielikiem trwalo ~10 min i telefon ubijal polaczenie,
    # przez co "Zapisz poprawki" wygladal na zepsuty. Teraz endpoint odpowiada
    # od razu, a flaga przeliczanie.lock mowi frontowi, ze robota trwa.
    import threading
    from src.reels.pipeline import _przygotuj_prompty_na_checkpoint
    lock = folder / "przeliczanie.lock"
    lock.write_text("1", encoding="utf-8")

    def _w_tle():
        try:
            _przygotuj_prompty_na_checkpoint(folder, scenariusz, tryb_jezykowy)
        finally:
            lock.unlink(missing_ok=True)

    threading.Thread(target=_w_tle, daemon=True).start()
    nowe_prompty = None  # przelicza sie w tle; front pyta GET /reel-checkpoint

    # NAPRAWIONE 10.07.2026 (Dyskusja) - Tomasz chcial WYRAZNE potwierdzenie
    # ze prompty faktycznie sie przeliczyly, nie tylko cichy zapis w tle.
    liczba_promptow = nowe_prompty.count("PROMPT ") if nowe_prompty else 0
    prompts_p = folder / "prompts.txt"
    znacznik_czasu = prompts_p.stat().st_mtime if prompts_p.is_file() else None

    return {
        "status": "ok",
        "zapisano": str(target),
        "prompty_obrazow": nowe_prompty,
        "liczba_promptow": liczba_promptow,
        "prompty_ts": znacznik_czasu,
    }


@router.post("/reel-checkpoint/{reel_id}/prompty")
def reel_checkpoint_zapisz_prompty(reel_id: str, data: dict = Body(...)):
    """Zapisuje RECZNIE poprawione przez Tomasza prompty obrazow, bez
    przeliczania na nowo (Dyskusja 10.07.2026) - Tomasz chce moc samemu
    doprecyzowac pojedynczy prompt (np. dodac szczegol ktorego model
    pominal), zamiast tylko podgladac wynik automatycznego przeliczenia."""
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    prompty = data.get("prompty_obrazow", "")
    if not prompty.strip():
        raise HTTPException(status_code=400, detail="Puste prompty")
    (folder / "prompts.txt").write_text(prompty, encoding="utf-8")
    return {"status": "ok", "prompty_ts": (folder / "prompts.txt").stat().st_mtime}


@router.post("/reel-checkpoint/{reel_id}/audytuj")
def reel_checkpoint_audytuj(reel_id: str, data: dict = Body(None)):
    """Automatyczna weryfikacja checkpointu (Dyskusja 09.07.2026) - qwen3:14b
    porownuje artykul ze scenariuszem, wypisuje wady i proponuje poprawiony
    scenariusz. Darmowe (lokalny model). Przyjmuje aktualny (mozliwe ze
    jeszcze niezapisany) tekst scenariusza z panelu, zeby audytowac to co
    Tomasz akurat widzi na ekranie, nie to co ostatnio zapisane na dysku."""
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")

    article_p = folder / "article.md"
    artykul = article_p.read_text(encoding="utf-8") if article_p.is_file() else ""

    scenariusz = (data or {}).get("scenariusz")
    if not scenariusz:
        tryb_jezykowy = _odczytaj_tryb_jezykowy(folder)
        target = (folder / "scenes_en.txt") if tryb_jezykowy in ("en_pl", "czysty") else (folder / "scenes.txt")
        scenariusz = target.read_text(encoding="utf-8") if target.is_file() else ""

    if not artykul or not scenariusz:
        raise HTTPException(status_code=400, detail="Brak artykulu lub scenariusza do audytu")

    return audytuj_checkpoint(artykul, scenariusz)


@router.post("/reel-checkpoint/{reel_id}/tlumacz")
def reel_checkpoint_tlumacz(reel_id: str, data: dict = Body(None)):
    """Podglad tlumaczenia CALEGO scenariusza na polski (Dyskusja 09.07.2026)
    - Tomasz chce porownac polski z angielskim przed zatwierdzeniem,
    zwlaszcza dla CZYSTEJ DROGI gdzie scenariusz jest po angielsku.
    NIC nie zapisuje na dysku - to tylko podglad w panelu. Darmowe (Bielik)."""
    from src.reels.pipeline import przetlumacz_scenariusz_podglad_pl
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")

    scenariusz = (data or {}).get("scenariusz")
    if not scenariusz:
        tryb_jezykowy = _odczytaj_tryb_jezykowy(folder)
        target = (folder / "scenes_en.txt") if tryb_jezykowy in ("en_pl", "czysty") else (folder / "scenes.txt")
        scenariusz = target.read_text(encoding="utf-8") if target.is_file() else ""

    if not scenariusz:
        raise HTTPException(status_code=400, detail="Brak scenariusza do przetlumaczenia")

    tlumaczenie = przetlumacz_scenariusz_podglad_pl(scenariusz)
    return {"scenariusz_pl": tlumaczenie}


@router.post("/reel-checkpoint/{reel_id}/zatwierdz")
def reel_checkpoint_zatwierdz(reel_id: str, data: dict = Body(None)):
    """OK na checkpoincie - odpala produkcje mediow (audio/obrazy/render),
    czyli wlasnie ta kosztowna czesc z fal.ai. Opcjonalnie przyjmuje
    poprawiony scenariusz w tym samym wywolaniu (zeby nie klikac 2x)."""
    import threading
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")

    tryb_jezykowy = _odczytaj_tryb_jezykowy(folder)
    scenariusz = (data or {}).get("scenariusz") or None
    # silnik_obrazow: opcjonalny wybor Tomasza (Dyskusja 09.07.2026) - "nano_banana_pro"
    # zamiast domyslnego FLUX.2 [max], po utracie zaufania do FLUX dla tematow
    # technicznych (rolka 000084, 80% obrazow odrzuconych mimo identycznego promptu).
    silnik_obrazow = (data or {}).get("silnik_obrazow") or None

    def _uruchom():
        wznow_po_checkpoincie(folder, scenariusz=scenariusz, tryb_jezykowy=tryb_jezykowy, silnik_obrazow=silnik_obrazow)

    threading.Thread(target=_uruchom, daemon=True).start()
    return {"status": "started", "reel_id": folder.name}


@router.get("/reel-status/{reel_id}")
def reel_status_endpoint(reel_id: str):
    import json
    base = REELS_DIR
    cands = [reel_id]
    if reel_id.isdigit():
        cands.append(reel_id.zfill(6))
    for c in cands:
        p = base / c / "status.json"
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                pass
    return {"etap": "nieznany"}


@router.post("/generate-reel")
def generate_reel_endpoint(data: dict = Body(...)):
    tryb = "organizm"
    topic_id = data.get("topic_id")
    if topic_id:
        from src.db.database import get_connection
        conn = get_connection()
        row = conn.execute(
            "SELECT t.tryb_override AS ov, c.tryb AS cat_tryb "
            "FROM topics t JOIN categories c ON c.id = t.category_id WHERE t.id = ?",
            (topic_id,)
        ).fetchone()
        conn.close()
        if row:
            tryb = row["ov"] or row["cat_tryb"] or "organizm"
    return generate_reel(data["prompt"], data.get("scene_count"), tryb=tryb, tryb_jezykowy=data.get("tryb_jezykowy", "pl"))

PROMPTS_FILE = Path(__file__).resolve().parent / "images" / "prompts.py"

@router.get("/host/prompts-py")
def host_get_prompts_py():
    return {
        "status": "ok",
        "path": "apps/api/src/images/prompts.py",
        "content": PROMPTS_FILE.read_text(encoding="utf-8")
    }




@router.get("/host/status")
def host_status():
    from pathlib import Path

    prompts = Path("/app/src/images/prompts.py").exists()

    return {
        "host": True,
        "prompts": prompts,
        "write": True,
    }

@router.post("/host/prompts-py")
def host_set_prompts_py(payload: dict = Body(...)):
    content = payload["content"]

    if not content.strip():
        raise HTTPException(status_code=400, detail="Odmowa wdrożenia: plik jest pusty.")

    old_size = PROMPTS_FILE.stat().st_size
    new_size = len(content.encode("utf-8"))

    if old_size > 3000 and new_size < 500:
        raise HTTPException(status_code=400, detail=f"Odmowa wdrożenia: nowy plik ma tylko {new_size} bajtów.")

    shutil.copy2(PROMPTS_FILE, PROMPTS_FILE.with_suffix(".py.bak"))
    PROMPTS_FILE.write_text(content, encoding="utf-8")

    return {
        "status": "ok",
        "path": "apps/api/src/images/prompts.py",
        "bytes": new_size,
        "backup": str(PROMPTS_FILE.with_suffix(".py.bak"))
    }


@router.post("/host/restart-api")
def host_restart_api():
    r = subprocess.run(
        ["docker","restart","fabryka-api"],
        capture_output=True,
        text=True
    )
    return {
        "status":"ok" if r.returncode==0 else "error",
        "stdout":r.stdout,
        "stderr":r.stderr
    }


@router.post("/render-scenes")
def render_scenes_endpoint(data: dict = Body(...)):
    return render_from_scenes(data["scenes"])


@router.get('/random-topic')
def random_topic_endpoint():
    from src.db.database import random_topic
    from fastapi import HTTPException
    t = random_topic()
    if not t:
        raise HTTPException(status_code=404, detail='Brak tematu w oknie sezonowym')
    return t


@router.get('/categories')
def categories_list_endpoint():
    from src.db.database import get_connection
    conn = get_connection()
    rows = conn.execute('SELECT id, nazwa, aktywna FROM categories ORDER BY id').fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post('/categories')
def categories_add_endpoint(data: dict = Body(...)):
    from src.db.database import add_category
    cid = add_category(data['nazwa'])
    return {'id': cid, 'nazwa': data['nazwa']}


@router.get('/topics-db')
def topics_db_list_endpoint(category_id=None):
    from src.db.database import get_connection
    conn = get_connection()
    if category_id is None:
        rows = conn.execute('SELECT id, category_id, tekst, uzyty_razy, ostatnio_uzyty, aktywny, miesiace FROM topics ORDER BY id').fetchall()
    else:
        rows = conn.execute('SELECT id, category_id, tekst, uzyty_razy, ostatnio_uzyty, aktywny, miesiace FROM topics WHERE category_id = ? ORDER BY id', (int(category_id),)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post('/topics-db')
def topics_db_add_endpoint(data: dict = Body(...)):
    from src.db.database import add_topic, get_connection
    tid = add_topic(data['category_id'], data['tekst'])
    mies = data.get('miesiace')
    if mies is not None:
        c = get_connection()
        c.execute('UPDATE topics SET miesiace = ? WHERE id = ?', (mies, tid))
        c.commit()
        c.close()
    return {'id': tid, 'category_id': data['category_id'], 'tekst': data['tekst'], 'miesiace': mies}


@router.get("/reels/{reel_id}/przebieg")
def reel_przebieg(reel_id: str):
    """Zwraca pelny przebieg rolki scena po scenie: UJECIE + LEKTOR + PROMPT
    obrazu (Dyskusja 10.07.2026 - Tomasz chce to widziec po kliknieciu na
    gotowa rolke w panelu, nie tylko sam plik wideo)."""
    from src.naprawa import znajdz_folder
    from src.scenes.generator import parse_scenes
    from src.images.generator import parse_prompts

    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")

    prompt_oryginalny_p = folder / "prompt_oryginalny.txt"
    prompt_oryginalny = prompt_oryginalny_p.read_text(encoding="utf-8") if prompt_oryginalny_p.is_file() else ""

    scenes_p = folder / "scenes.txt"
    scenes_en_p = folder / "scenes_en.txt"
    scenariusz_p = scenes_p if scenes_p.is_file() else scenes_en_p
    scenariusz = scenariusz_p.read_text(encoding="utf-8") if scenariusz_p.is_file() else ""

    prompts_p = folder / "prompts.txt"
    prompty_tekst = prompts_p.read_text(encoding="utf-8") if prompts_p.is_file() else ""

    sceny = parse_scenes(scenariusz) if scenariusz else []
    prompty_lista = parse_prompts(prompty_tekst) if prompty_tekst else []

    wynik = []
    for s in sceny:
        nr = s.get("scena")
        prompt_tej_sceny = prompty_lista[nr - 1] if (nr and 0 < nr <= len(prompty_lista)) else ""
        wynik.append({
            "scena": nr,
            "ujecie": s.get("ujecie", ""),
            "lektor": s.get("lektor", ""),
            "prompt": prompt_tej_sceny,
        })

    return {"reel_id": folder.name, "prompt_oryginalny": prompt_oryginalny, "sceny": wynik}


@router.get("/reels/{reel_id}/video")
def reel_video(reel_id: str):
    import os
    from fastapi import HTTPException
    from fastapi.responses import FileResponse
    base = "/root/rod-ai-studio/data/reels"
    cands = [reel_id]
    if reel_id.isdigit():
        cands.append(reel_id.zfill(6))
    folder = None
    for c in cands:
        d = os.path.join(base, c, "video")
        if os.path.isdir(d):
            folder = d
            break
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    for name in ("final_napisy_muzyka.mp4", "final_with_music.mp4", "final.mp4"):
        p = os.path.join(folder, name)
        if os.path.isfile(p):
            return FileResponse(p, media_type="video/mp4", filename="reel_"+reel_id+".mp4")
    raise HTTPException(status_code=404, detail="Brak finalnego MP4")


@router.get("/reels/{reel_id}/image/{n}")
def reel_image(reel_id: str, n: int):
    from fastapi.responses import FileResponse
    folder = znajdz_folder(str(REELS_DIR), reel_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    p = folder / "images" / f"{n:02d}.jpg"
    if not p.is_file():
        raise HTTPException(status_code=404, detail="Brak obrazu")
    return FileResponse(p, media_type="image/jpeg")


@router.post("/napraw-sprawdz")
def napraw_sprawdz_wycofane(data: dict = Body(None)):
    raise HTTPException(status_code=410, detail="Funkcja wycofana (qwen usuniety) — poprawki scenariuszy robimy w czacie z Claude.")


@router.post("/napraw-zastosuj")
def napraw_zastosuj_wycofane(data: dict = Body(None)):
    raise HTTPException(status_code=410, detail="Funkcja wycofana (qwen usuniety) — poprawki scenariuszy robimy w czacie z Claude.")


@router.get('/zapowiedzi')
def zapowiedzi_list_endpoint():
    from src.db.database import list_zapowiedzi
    return list_zapowiedzi()


@router.post('/zapowiedzi')
def zapowiedzi_add_endpoint(data: dict = Body(...)):
    from src.db.database import add_zapowiedz
    zid = add_zapowiedz(data['tresc_promptu'])
    return {'id': zid, 'tresc_promptu': data['tresc_promptu']}


@router.post('/zapowiedzi/{zapowiedz_id}/uzyj')
def zapowiedzi_uzyj_endpoint(zapowiedz_id: int, data: dict = Body(...)):
    from src.db.database import oznacz_uzyta_zapowiedz
    oznacz_uzyta_zapowiedz(zapowiedz_id, data.get('reel_id'))
    return {'status': 'ok'}


# ==== Publikacja rolki na Facebooka jako Reel (10.07.2026) ====
from fastapi import Body as _FBBody

@router.post("/reels/{reel_id}/publikuj-fb")
def publikuj_fb_reel(reel_id: str, opis: str = _FBBody("", embed=True)):
    import os, json, time, urllib.request, urllib.parse, urllib.error
    from fastapi import HTTPException

    tok_path = "/root/rod-ai-studio/data/.secrets/fb_page_token"
    if not os.path.isfile(tok_path):
        raise HTTPException(status_code=400, detail="Brak tokenu FB na serwerze.")
    tok = open(tok_path, encoding="utf-8").read().strip()
    if not tok.startswith("EAA"):
        raise HTTPException(status_code=400, detail="Token FB wyglada nieprawidlowo.")

    PAGE_ID = "1174205105781401"
    V = "v21.0"
    base_id = reel_id.zfill(6) if reel_id.isdigit() else reel_id
    folder = os.path.join("/root/rod-ai-studio/data/reels", base_id)
    have_video = any(os.path.isfile(os.path.join(folder, "video", n))
                     for n in ("final_napisy_muzyka.mp4", "final_with_music.mp4", "final.mp4"))
    if not have_video:
        raise HTTPException(status_code=404, detail="Rolka nie ma gotowego wideo.")

    video_url = f"https://panel.157-90-155-155.sslip.io/reels/{base_id}/video"

    def graph_post(path, params):
        params = dict(params); params["access_token"] = tok
        url = f"https://graph.facebook.com/{V}/{path}"
        req = urllib.request.Request(url, data=urllib.parse.urlencode(params).encode(), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            try: eb = json.loads(e.read().decode())
            except Exception: eb = {}
            msg = (eb.get("error") or {}).get("message", "blad")
            raise HTTPException(status_code=502, detail=f"FB API ({e.code}): {msg}")
        except Exception as ex:
            raise HTTPException(status_code=502, detail=f"FB API niedostepne ({type(ex).__name__})")

    start = graph_post(f"{PAGE_ID}/video_reels", {"upload_phase": "start"})
    video_id = start.get("video_id"); upload_url = start.get("upload_url")
    if not (video_id and upload_url):
        raise HTTPException(status_code=502, detail="FB nie zwrocil video_id/upload_url.")

    up_req = urllib.request.Request(
        upload_url, data=b"",
        headers={"Authorization": "OAuth " + tok, "file_url": video_url}, method="POST")
    try:
        with urllib.request.urlopen(up_req, timeout=180) as r:
            r.read()
    except urllib.error.HTTPError as e:
        try: eb = e.read().decode()
        except Exception: eb = ""
        raise HTTPException(status_code=502, detail=f"FB upload ({e.code}): {eb[:180]}")
    except Exception as ex:
        raise HTTPException(status_code=502, detail=f"FB upload niedostepny ({type(ex).__name__})")

    fin = graph_post(f"{PAGE_ID}/video_reels", {
        "upload_phase": "finish", "video_id": video_id,
        "video_state": "PUBLISHED", "description": opis or ""})

    try:
        open(os.path.join(folder, "opublikowano.txt"), "w", encoding="utf-8").write(
            time.strftime("%Y-%m-%d %H:%M") + " | FB Reel video_id=" + str(video_id))
    except Exception:
        pass

    return {"ok": True, "video_id": video_id,
            "link": f"https://www.facebook.com/reel/{video_id}", "finish": fin}


# ==== Auto-opis FB: Bielik (darmowy) ====
@router.post("/reels/{reel_id}/generuj-opis-fb")
def generuj_opis_fb(reel_id: str, force: bool = False):
    import os
    from fastapi import HTTPException
    base_id = reel_id.zfill(6) if reel_id.isdigit() else reel_id
    folder = os.path.join("/root/rod-ai-studio/data/reels", base_id)
    cache_path = os.path.join(folder, "opis_fb.txt")
    if not force and os.path.isfile(cache_path):
        cached = open(cache_path, encoding="utf-8").read().strip()
        if cached:
            return {"ok": True, "opis": cached, "cache": True}
    art_path = os.path.join(folder, "article.md")
    if not os.path.isfile(art_path):
        raise HTTPException(status_code=404, detail="Rolka nie ma artykulu (article.md).")
    article = open(art_path, encoding="utf-8").read().strip()[:3000]
    prompt = (
        "Napisz krotki, angazujacy opis posta na Facebooka do rolki wideo dla ROD im. Jozefa Lompy "
        "w Wozniki (ogrod dzialkowy). Odbiorca: zwykly dzialkowiec, czesto po 50-tce.\n"
        "STRUKTURA:\n"
        "- Mocny pierwszy wers (hook) z jednym emoji na poczatku\n"
        "- 3 do 5 konkretnych korzysci lub faktow z tresci, kazdy w osobnej linii z emoji na poczatku\n"
        "- Jedno zdanie podsumowania\n"
        "- Pytanie na koncu zachecajace do komentarzy\n"
        "- Na koncu 3-4 trafne hashtagi po polsku (np. #ogrod #dzialka)\n"
        "Pisz naturalnie po polsku. Odpowiedz WYLACZNIE gotowym opisem posta, bez zadnego komentarza przed ani po.\n\n"
        "TRESC ROLKI:\n" + article
    )
    try:
        from src.ai.ollama import generate
    except Exception:
        from ai.ollama import generate
    opis = (generate(prompt) or "").strip()
    if not opis:
        raise HTTPException(status_code=502, detail="Bielik nie zwrocil opisu.")
    try:
        open(cache_path, "w", encoding="utf-8").write(opis)
    except Exception:
        pass
    return {"ok": True, "opis": opis, "cache": False}


# ==== Popraw opis FB przez Claude (platne, na zadanie) ====
@router.post("/reels/{reel_id}/opis-przez-claude")
def opis_przez_claude(reel_id: str, data: dict = Body(...)):
    import os
    from fastapi import HTTPException
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Brak ANTHROPIC_API_KEY na serwerze.")
    base_id = reel_id.zfill(6) if reel_id.isdigit() else reel_id
    folder = os.path.join("/root/rod-ai-studio/data/reels", base_id)
    obecny = (data.get("opis") or "").strip()
    article = ""
    art_path = os.path.join(folder, "article.md")
    if os.path.isfile(art_path):
        article = open(art_path, encoding="utf-8").read().strip()[:3000]
    system_prompt = (
        "Jestes redaktorem social media dla ROD im. Jozefa Lompy w Wozniki (ogrod dzialkowy). "
        "Napisz DOPRACOWANY, angazujacy opis posta na Facebooka do rolki wideo. Odbiorca: dzialkowicze, "
        "czesto po 50-tce. Zasady algorytmu FB: mocny hook w pierwszym wersie, konkretne korzysci, pytanie "
        "zachecajace do komentarzy, 3-4 trafne hashtagi po polsku. Styl: cieply, konkretny, z emoji. "
        "Odpowiedz WYLACZNIE gotowym opisem posta, bez komentarza przed ani po."
    )
    user_message = ""
    if obecny:
        user_message += "OBECNY OPIS (popraw i podkrec, zachowujac sens):\n" + obecny + "\n\n"
    if article:
        user_message += "TRESC ROLKI (kontekst):\n" + article
    if not user_message.strip():
        raise HTTPException(status_code=400, detail="Brak tresci do opracowania.")
    try:
        resp = req.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": "claude-sonnet-4-6", "max_tokens": 1000, "system": system_prompt,
                  "messages": [{"role": "user", "content": user_message}]},
            timeout=60)
        resp.raise_for_status()
        wynik = resp.json()
        tekst = "".join(b.get("text", "") for b in wynik.get("content", []) if b.get("type") == "text").strip()
        try:
            open(os.path.join(folder, "opis_fb.txt"), "w", encoding="utf-8").write(tekst)
        except Exception:
            pass
        return {"ok": True, "opis": tekst}
    except req.exceptions.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Claude API: {e.response.status_code} - {e.response.text[:200]}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Claude API blad: {e}")
