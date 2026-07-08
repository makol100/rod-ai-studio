from pathlib import Path
import traceback

from src.ai.ollama import generate, has_repetition_loop
from src.scenes.generator import generate_scenes, generate_scenes_en, validate_scenario, parse_scenes
from src.images.prompts import generate_image_prompts, generate_image_prompts_czysty
from src.images.generator import generate_images
from src.ai.image_backend import generate_image
from src.video.renderer import render_video
from src.reels import create_reel_folder, save_text
from src.audio.generator import generate_audio
from src.subtitles.generator import make_subtitles


def _log(msg: str):
    # widoczne na żywo w: docker logs -f fabryka-api
    print(f"[reel] {msg}", flush=True)


def _write_status(folder: Path, etap: str, extra: dict = None):
    """Zapisuje PRAWDZIWY aktualny etap do status.json w folderze rolki.
    Uzywane przez panel do prawdziwego paska postepu (nie symulacji).
    Ustalone w Dyskusji 08.07.2026 - zasada 'weryfikacja nie halucynacja'."""
    import json, datetime
    try:
        data = {"etap": etap, "extra": extra or {}, "ts": datetime.datetime.now().isoformat()}
        (folder / "status.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass  # status.json to tylko UI-owy bonus, nigdy nie ma wywalic pipeline'u


def _produce_media(folder: Path, scenes: str, result: dict) -> dict:
    """
    Druga połowa pipeline'u: gotowy scenariusz -> audio -> prompty -> obrazy -> wideo.
    Współdzielona przez generate_reel (pełny bieg) i render_from_scenes (z gotowego skryptu).
    Odporna: błąd jednego obrazu nie zabija reszty; render sam pomija brakujące klatki.
    """
    save_text(folder, "scenes.txt", scenes)
    result["scenes_file"] = str(folder / "scenes.txt")

    _write_status(folder, "lektor")
    _log("audio (edge-tts)…")
    audio = generate_audio(folder, scenes)
    result["audio_count"] = len(audio)

    _write_status(folder, "obrazy", {"i": 0, "total": 0})
    _log("prompty obrazow…")
    image_prompts = generate_image_prompts(scenes)
    save_text(folder, "prompts.txt", image_prompts)
    result["prompts_file"] = str(folder / "prompts.txt")

    images = generate_images(folder)
    total = len(images)
    _log(f"obrazy fal.ai: {total} szt…")

    ok = 0
    failed = []
    for img in images:
        idx = img.get("index")
        try:
            res = generate_image(img["prompt"], Path(img["output"]))
            if res.get("status") == "ok":
                ok += 1
                _write_status(folder, "obrazy", {"i": idx, "total": total})
                _log(f"    obraz {idx}/{total} OK")
            else:
                failed.append(idx)
                _log(f"    obraz {idx}/{total} BLAD: {res.get('error')}")
        except Exception as e:
            failed.append(idx)
            _log(f"    obraz {idx}/{total} WYJATEK: {e}")

    result["images_ok"] = ok
    result["images_failed"] = failed

    if ok == 0:
        result["status"] = "error"
        result["error"] = "Zaden obraz sie nie wygenerowal — render pominiety."
        _log("PRZERWANE: brak obrazow, render pominiety.")
        return result

    _write_status(folder, "napisy")
    _log("napisy (whisper)…")
    subs_res = make_subtitles(folder)
    result["subs_count"] = subs_res.get("count", 0)

    _write_status(folder, "render")
    _log("renderuje wideo…")
    video = render_video(folder)
    result["video"] = video

    if video.get("status") == "ok":
        _write_status(folder, "muzyka")
        _log("muzyka…")
        from src.audio.music import add_background_music
        video_path = Path(video["output"])
        music_output = video_path.with_name("final_with_music.mp4")
        music_result = add_background_music(video_path, music_output)
        result["music"] = music_result
        if music_result.get("status") == "ok":
            video["output"] = music_result["output"]
    if isinstance(video, dict) and video.get("status") == "ok":
        result["video_file"] = video.get("output")
        _write_status(folder, "gotowe", {"video": video.get('output')})
        _log(f"GOTOWE: {video.get('output')} (obrazy {ok}/{total})")
    else:
        result["status"] = "partial"
        _write_status(folder, "blad", {"detail": str(video)})
        _log(f"Render zwrocil blad: {video}")

    return result


def _translate_lektor_to_pl(scenes_en: str) -> str:
    import re as _re
    from src.ai.ollama import PROMPT_MODEL
    scenes = parse_scenes(scenes_en)
    if not scenes:
        return scenes_en

    # KRYTYCZNE: Llama byla wlasnie uzywana do promptow obrazow - trzeba ja
    # zwolnic PRZED zaladowaniem Bielika do tlumaczenia. Przeoczone przy
    # pierwszej wersji, spowodowalo prawdziwy OOM-kill (dmesg potwierdzony,
    # PID 938247) w trakcie testu rolki 000065.
    _unload_model(PROMPT_MODEL)

    lista = "\n".join(f"{s['scena']}. {s['lektor']}" for s in scenes)
    prompt_tlumacz = (
        "Ponizej jest ponumerowana lista zdan po angielsku - to tekst lektora "
        "do filmu o ogrodnictwie. Przetlumacz KAZDE zdanie na naturalny, cieply "
        "polski. Zachowaj TA SAMA numeracje i kolejnosc, jedno zdanie na linie. "
        "Zachowaj nazwy wlasne dokladnie jak w oryginale. Odpowiedz WYLACZNIE "
        "po polsku, bez zadnych komentarzy - tylko ponumerowana lista tlumaczen:\n\n"
        + lista
    )
    tlumaczenie = generate(prompt_tlumacz)
    linie_pl = [l.strip() for l in tlumaczenie.splitlines() if l.strip()]

    wynik = []
    for s in scenes:
        wynik.append(f"SCENA {s['scena']}:")
        wynik.append(f"UJĘCIE: {s['ujecie']}")
        lektor_pl = s['lektor']
        for linia in linie_pl:
            m = _re.match(rf"^{s['scena']}\.\s*(.+)", linia)
            if m:
                lektor_pl = m.group(1).strip()
                break
        wynik.append(f"LEKTOR: {lektor_pl}")
        wynik.append("")
    return "\n".join(wynik).strip()


def _produce_media_en_pl(folder: Path, scenes_en: str, result: dict) -> dict:
    save_text(folder, "scenes_en.txt", scenes_en)
    result["scenes_file"] = str(folder / "scenes_en.txt")

    _write_status(folder, "obrazy", {"i": 0, "total": 0})
    _log("prompty obrazow (EN, czysty prompt bez konkurencyjnych przykladow)…")
    image_prompts = generate_image_prompts_czysty(scenes_en)
    save_text(folder, "prompts.txt", image_prompts)
    result["prompts_file"] = str(folder / "prompts.txt")

    images = generate_images(folder)
    total = len(images)
    _log(f"obrazy fal.ai: {total} szt…")

    ok = 0
    failed = []
    for img in images:
        idx = img.get("index")
        try:
            res = generate_image(img["prompt"], Path(img["output"]))
            if res.get("status") == "ok":
                ok += 1
                _write_status(folder, "obrazy", {"i": idx, "total": total})
                _log(f"    obraz {idx}/{total} OK")
            else:
                failed.append(idx)
                _log(f"    obraz {idx}/{total} BLAD: {res.get('error')}")
        except Exception as e:
            failed.append(idx)
            _log(f"    obraz {idx}/{total} WYJATEK: {e}")

    result["images_ok"] = ok
    result["images_failed"] = failed

    if ok == 0:
        result["status"] = "error"
        result["error"] = "Zaden obraz sie nie wygenerowal — render pominiety."
        _write_status(folder, "blad", {"detail": "brak obrazow"})
        _log("PRZERWANE: brak obrazow, render pominiety.")
        return result

    _write_status(folder, "tlumaczenie")
    _log("tlumaczenie lektora na polski (Bielik)…")
    scenes_pl = _translate_lektor_to_pl(scenes_en)
    save_text(folder, "scenes.txt", scenes_pl)

    _write_status(folder, "lektor")
    _log("audio (edge-tts)…")
    audio = generate_audio(folder, scenes_pl)
    result["audio_count"] = len(audio)

    _write_status(folder, "napisy")
    _log("napisy (whisper)…")
    subs_res = make_subtitles(folder)
    result["subs_count"] = subs_res.get("count", 0)

    _write_status(folder, "render")
    _log("renderuje wideo…")
    video = render_video(folder)
    result["video"] = video

    if video.get("status") == "ok":
        _write_status(folder, "muzyka")
        _log("muzyka…")
        from src.audio.music import add_background_music
        video_path = Path(video["output"])
        music_output = video_path.with_name("final_with_music.mp4")
        music_result = add_background_music(video_path, music_output)
        result["music"] = music_result
        if music_result.get("status") == "ok":
            video["output"] = music_result["output"]
    if isinstance(video, dict) and video.get("status") == "ok":
        result["video_file"] = video.get("output")
        _write_status(folder, "gotowe", {"video": video.get('output')})
        _log(f"GOTOWE: {video.get('output')} (obrazy {ok}/{total})")
    else:
        result["status"] = "partial"
        _write_status(folder, "blad", {"detail": str(video)})
        _log(f"Render zwrocil blad: {video}")

    return result


def _unload_model(model_name: str, max_wait: int = 20, bufor_bezpieczenstwa: int = 10):
    """Zwalnia model i CZEKA az faktycznie zniknie z /api/ps, POTEM CZEKA
    JESZCZE bufor_bezpieczenstwa sekund, zanim pozwoli ladowac nastepny model.

    Powod dodatkowego bufora (Dyskusja 08.07.2026, po powiekszeniu VPS do
    22GB): nawet z pollingiem /api/ps, dwa duze modele (Bielik-11B +
    Qwen3-14B) dalej dawaly OOM-kille - /api/ps najwyrazniej potrafi
    zaraportowac model jako 'zniknal' ZANIM system faktycznie w pelni
    odzyska pamiec na poziomie OS. Bufor to dodatkowy margines na to
    opoznienie, nie tylko poleganie na samym fakcie znikniecia z listy."""
    import requests, time
    try:
        requests.post(
            "http://host.docker.internal:11434/api/generate",
            json={"model": model_name, "keep_alive": 0},
            timeout=15,
        )
    except Exception:
        pass

    t0 = time.time()
    zniknal = False
    while time.time() - t0 < max_wait:
        try:
            r = requests.get("http://host.docker.internal:11434/api/ps", timeout=5)
            zaladowane = [m.get("name", "") for m in r.json().get("models", [])]
            if not any(model_name in nazwa for nazwa in zaladowane):
                zniknal = True
                break
        except Exception:
            pass
        time.sleep(1)

    if not zniknal:
        _log(f"OSTRZEZENIE: {model_name} nie zwolnil sie w {max_wait}s, jade dalej mimo to")
        return

    _log(f"model {model_name} zniknal z /api/ps, dodatkowy bufor {bufor_bezpieczenstwa}s przed zaladowaniem nastepnego…")
    time.sleep(bufor_bezpieczenstwa)


def generate_reel(prompt: str, scene_count=None, tryb: str = "organizm", folder=None, tryb_jezykowy: str = "pl"):
    """Pełny pipeline: prompt -> artykuł -> sceny -> (audio, obrazy, wideo).

    tryb -- "organizm" (domyslnie) albo "sprzet", wybiera wariant promptu
    scenariusza w scenes/generator.py (patrz TELEPORT_fabryka.md).
    folder -- opcjonalnie gotowy, wczesniej utworzony folder (uzywane przez
    /generate-reel-async, zeby caller poznal reel_id NATYCHMIAST). Jesli
    None, tworzy nowy jak dotychczas.
    tryb_jezykowy -- "pl" (domyslnie, Bielik pisze artykul bezposrednio po
    polsku - dla zwyklych tematow z bazy, dziala dobrze, NIE ruszac) albo
    "en_pl" (Llama pisze szkic po angielsku, Bielik tlumaczy+wyglada -
    dla zapowiedzi serii bez sztywnego tematu, patrz Dyskusja 08.07.2026).
    """
    if folder is None:
        folder = create_reel_folder()
    _log(f"START (pelny) folder={folder} tryb={tryb} tryb_jezykowy={tryb_jezykowy}")
    _write_status(folder, "sceny")
    result = {"status": "ok", "folder": str(folder), "mode": "generate_reel", "tryb": tryb, "tryb_jezykowy": tryb_jezykowy}
    ostrzezenia = []
    try:
        if tryb_jezykowy == "en_pl":
            # SCIEZKA v2 (Dyskusja 08.07.2026, plan graficzny Tomasza):
            # Llama robi szkic ORAZ scenariusz PO ANGIELSKU; tlumaczenie na
            # polski przesuniete na PO obrazach (_produce_media_en_pl),
            # tlumaczy tylko LEKTOR, nie cale UJECIE.
            from src.ai.ollama import PROMPT_MODEL, DEFAULT_MODEL
            _log("krok 1: szkic po angielsku (Llama)…")
            _unload_model(DEFAULT_MODEL)
            # Prompt idzie WPROST do Llamy, bez owijki - zapowiedzi dla tej
            # sciezki sa teraz pisane od razu po angielsku (Dyskusja
            # 08.07.2026). Prostsze niz owijanie polskiego tekstu w
            # angielska ramke, i bardziej bezposrednie.
            draft_en = generate(prompt, model=PROMPT_MODEL)
            save_text(folder, "article.md", draft_en)
            result["article_file"] = str(folder / "article.md")
            if has_repetition_loop(draft_en):
                _log("OSTRZEZENIE: wykryto petle powtorzen w szkicu!")
                ostrzezenia.append({"etap": "szkic", "fragment": draft_en[:150]})

            _log("krok 2: scenariusz po angielsku (Llama)…")
            scenes_en = generate_scenes_en(draft_en, scene_count, tryb=tryb)
            if has_repetition_loop(scenes_en):
                _log("OSTRZEZENIE: wykryto petle powtorzen w scenariuszu!")
                ostrzezenia.append({"etap": "scenariusz", "fragment": scenes_en[:150]})

            save_text(folder, "scenes_en.txt", scenes_en)
            problemy = validate_scenario(scenes_en, scene_count)
            if problemy:
                _log(f"ZATRZYMANO PRZED PRODUKCJA MEDIOW: {problemy}")
                import json
                (folder / "WARNING.json").write_text(
                    json.dumps({"ostrzezenia": ostrzezenia, "zatrzymano_walidacja": problemy}, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
                result["status"] = "zatrzymano_walidacja"
                result["warning"] = True
                result["warning_details"] = ostrzezenia
                result["zatrzymano_walidacja"] = problemy
                _write_status(folder, "zatrzymano_walidacja", {"problemy": problemy})
                return result

            if ostrzezenia:
                import json
                (folder / "WARNING.json").write_text(
                    json.dumps({"ostrzezenia": ostrzezenia}, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
                result["warning"] = True
                result["warning_details"] = ostrzezenia

            return _produce_media_en_pl(folder, scenes_en, result)

        # SCIEZKA "pl" (domyslna, NIEZMIENIONA od dzisiejszej konsolidacji modeli)
        _log("artykul…")
        article = generate(prompt)
        save_text(folder, "article.md", article)
        result["article_file"] = str(folder / "article.md")
        if has_repetition_loop(article):
            _log("OSTRZEZENIE: wykryto petle powtorzen w artykule!")
            ostrzezenia.append({"etap": "artykul", "fragment": article[:150]})

        _log("sceny…")
        scenes = generate_scenes(article, scene_count, tryb=tryb)
        if has_repetition_loop(scenes):
            _log("OSTRZEZENIE: wykryto petle powtorzen w scenariuszu!")
            ostrzezenia.append({"etap": "scenariusz", "fragment": scenes[:150]})

        save_text(folder, "scenes.txt", scenes)
        problemy = validate_scenario(scenes, scene_count)
        if problemy:
            _log(f"ZATRZYMANO PRZED PRODUKCJA MEDIOW: {problemy}")
            import json
            (folder / "WARNING.json").write_text(
                json.dumps({"ostrzezenia": ostrzezenia, "zatrzymano_walidacja": problemy}, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            result["status"] = "zatrzymano_walidacja"
            result["warning"] = True
            result["warning_details"] = ostrzezenia
            result["zatrzymano_walidacja"] = problemy
            _write_status(folder, "zatrzymano_walidacja", {"problemy": problemy})
            return result

        if ostrzezenia:
            import json
            (folder / "WARNING.json").write_text(
                json.dumps({"ostrzezenia": ostrzezenia}, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            result["warning"] = True
            result["warning_details"] = ostrzezenia

        return _produce_media(folder, scenes, result)

    except Exception as e:
        _log(f"BLAD KRYTYCZNY: {e}")
        result["status"] = "error"
        result["error"] = str(e)
        result["trace"] = traceback.format_exc().splitlines()[-3:]
        _write_status(folder, "blad", {"detail": str(e)})
        return result


def render_from_scenes(scenes: str):
    """
    Z gotowego, zatwierdzonego scenariusza: -> (audio, obrazy, wideo).
    Pomija generowanie artykułu i scen — renderuje DOKŁADNIE to, co podasz.
    Scenariusz musi być w formacie: SCENA N: / UJĘCIE: / LEKTOR:.
    """
    folder = create_reel_folder()
    _log(f"START (z gotowego skryptu) folder={folder}")
    result = {"status": "ok", "folder": str(folder), "mode": "render_from_scenes"}
    try:
        if not scenes or not scenes.strip():
            result["status"] = "error"
            result["error"] = "Pusty scenariusz."
            _log("PRZERWANE: pusty scenariusz.")
            return result

        return _produce_media(folder, scenes.strip(), result)

    except Exception as e:
        _log(f"BLAD KRYTYCZNY: {e}")
        result["status"] = "error"
        result["error"] = str(e)
        result["trace"] = traceback.format_exc().splitlines()[-3:]
        return result
