import re
from pathlib import Path
from datetime import datetime
import subprocess
import shutil
from fastapi import APIRouter, Body, HTTPException

from src.ai.ollama import generate
from src.db.database import save_reel, list_reels
from src.scenes.generator import generate_scenes
from src.images.prompts import generate_image_prompts
from src.reels.pipeline import generate_reel, render_from_scenes

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

        wyniki.append({
            "id": int(d.name),
            "title": title or ("Rolka #" + d.name),
            "prompt": title,
            "text": "",
            "hashtags": "",
            "status": "gotowa" if has_video else "w trakcie",
            "created_at": created,
            "warning": warning,
        })

    wyniki.sort(key=lambda r: r["id"], reverse=True)
    return wyniki[:limit]


@router.get("/reels")
def get_reels():
    return {
        "status": "ok",
        "reels": _scan_reels_from_disk()
    }


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
    KONCOWE = {"gotowe", "blad", "zatrzymano_walidacja"}
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
        wiek = time.time() - sp.stat().st_mtime
        if wiek > PROG_MAX_WIEK_S:
            continue  # zbyt stare, prawdopodobnie porzucone po crashu
        if najnowsza is None or sp.stat().st_mtime > najnowsza[1]:
            najnowsza = (d.name, sp.stat().st_mtime, dane)

    if najnowsza is None:
        return {"aktywna": None}
    reel_id, _, dane = najnowsza
    return {"aktywna": reel_id, "status": dane}


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


@router.post("/napraw-sprawdz")
def napraw_sprawdz_endpoint(data: dict = Body(...)):
    from fastapi import HTTPException
    from src.naprawa import znajdz_folder, sprawdz_zmiany
    folder = znajdz_folder("/root/rod-ai-studio/data/reels", str(data["reel_id"]))
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    if not (folder / "scenes.txt").is_file():
        raise HTTPException(status_code=404, detail="Brak scenes.txt dla tej rolki")
    return sprawdz_zmiany(folder, data["skarga"])


@router.post("/napraw-zastosuj")
def napraw_zastosuj_endpoint(data: dict = Body(...)):
    from fastapi import HTTPException
    from src.naprawa import znajdz_folder, zastosuj_zmiany
    folder = znajdz_folder("/root/rod-ai-studio/data/reels", str(data["reel_id"]))
    if folder is None:
        raise HTTPException(status_code=404, detail="Rolka nie znaleziona")
    stary_tekst = (folder / "scenes.txt").read_text(encoding="utf-8")
    nowy_tekst = data["nowy_scenariusz"]
    zaakceptowane = set(int(x) for x in data.get("zaakceptowane_sceny", []))
    return zastosuj_zmiany(folder, stary_tekst, nowy_tekst, zaakceptowane)


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
