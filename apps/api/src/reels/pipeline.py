from pathlib import Path
import traceback

from src.ai.ollama import generate, has_repetition_loop
from src.scenes.generator import generate_scenes, generate_scenes_en, validate_scenario, parse_scenes, _normalize
from src.images.prompts import generate_image_prompts, generate_image_prompts_czysty
from src.images.generator import generate_images
from src.ai.image_backend import generate_image
from src.video.renderer import render_video
from src.reels import create_reel_folder, save_text
from src.audio.generator import generate_audio
from src.subtitles.generator import make_subtitles


_LIVE_LOG_PATH = Path("/root/rod-ai-studio/data/live.log")
_LIVE_LOG_MAX_LINES = 2000  # przycina plik zeby nie rosl w nieskonczonosc


def _log(msg: str):
    # widoczne na żywo w: docker logs -f fabryka-api ORAZ w panelu (okno "Na zywo",
    # Dyskusja 09.07.2026 - "jak w Termius"). Zapis do pliku jest best-effort,
    # nigdy nie ma wywalic pipeline'u jesli dysk/uprawnienia zawioda.
    import datetime
    print(f"[reel] {msg}", flush=True)
    try:
        linia = f"{datetime.datetime.now().strftime('%H:%M:%S')} {msg}\n"
        with open(_LIVE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(linia)
        # przytnij co jakis czas, zeby plik nie rosl w nieskonczonosc (tanie: co ~50 linii)
        if hash(msg) % 50 == 0:
            tekst = _LIVE_LOG_PATH.read_text(encoding="utf-8")
            wszystkie = tekst.splitlines(keepends=True)
            if len(wszystkie) > _LIVE_LOG_MAX_LINES:
                _LIVE_LOG_PATH.write_text("".join(wszystkie[-_LIVE_LOG_MAX_LINES:]), encoding="utf-8")
    except Exception:
        pass


def _notify_telegram(folder: Path, result: dict):
    """Powiadomienie Telegram o gotowej rolce (Dyskusja 09.07.2026).
    Wola webhook HA Dom (automation.fabryka_rolek_powiadomienie_o_gotowej_rolce),
    ktora wysyla telegram_bot.send_video na chat Tomasza. Wideo publicznie
    dostepne przez port 8000 (firewall VPS ma otwarty dpt:8000 dla fabryka-api).
    Nigdy nie ma wywalic pipeline'u - failure tylko logowany."""
    import requests
    try:
        reel_id = folder.name
        video_url = f"http://157-90-155-155.sslip.io:8000/reels/{reel_id}/video"
        caption = f"\U0001F3AC Rolka {reel_id} gotowa!\n{video_url}"
        requests.post(
            "https://kzdoj77rzm29x15ipkor8zo2jnh884rs.ui.nabu.casa/api/webhook/fabryka_rolka_gotowa",
            json={"video_url": video_url, "caption": caption},
            timeout=15,
        )
        _log(f"powiadomienie Telegram wyslane ({reel_id})")
    except Exception as e:
        _log(f"OSTRZEZENIE: powiadomienie Telegram nie wyslane: {e}")


def _stop_requested(folder: Path) -> bool:
    """Sprawdza czy user kliknal 'Przerwij' w panelu (Dyskusja 09.07.2026).
    Kooperacyjna flaga plikowa - nie zabija watku na sile (bezpieczniej dla
    pol-wykonanych zapisow na dysku), tylko sprawdzana w bezpiecznych
    punktach (miedzy obrazami/audio/etc), zeby przerwac PRZED kolejnym
    kosztownym wywolaniem fal.ai."""
    return (folder / "STOP.flag").exists()


def _przygotuj_prompty_na_checkpoint(folder: Path, scenariusz: str, tryb_jezykowy: str) -> str:
    """Generuje prompty obrazow PRZED checkpointem, zeby Tomasz mogl je
    zobaczyc i ocenic PRZED kosztownym krokiem (fal.ai) - nie tylko sam
    scenariusz UJECIE/LEKTOR (Dyskusja 09.07.2026). Darmowe (lokalny model),
    wiec bezpiecznie generowac zawsze, nawet jesli user potem nie zatwierdzi.

    Zapisuje do folder/prompts.txt - _produce_media/_produce_media_en_pl
    przy zatwierdzeniu SPRAWDZA czy ten plik juz istnieje i jesli tak,
    NIE generuje ponownie (oszczedza czas), chyba ze scenariusz zostal
    zmieniony w miedzyczasie (wtedy trzeba wywolac ta funkcje ponownie -
    patrz reel_checkpoint_zapisz w topics.py, ktore wlasnie to robi)."""
    from src.ai.ollama import PROMPT_MODEL, DEFAULT_MODEL
    if tryb_jezykowy in ("en_pl", "czysty"):
        prompty = generate_image_prompts_czysty(scenariusz)
    elif tryb_jezykowy == "czysty_bielik":
        # NAPRAWIONE (rolka 000081): musi isc przez _czysty (bez sekcji
        # "kalarepa/koper" z SINGLE_SCENE_HEADER), inaczej Bielik dostaje
        # szablon narzucajacy "to ma byc ogrod" i albo odmawia dla scen
        # niezwiazanych z ogrodem, albo sam wymysla warzywa ignorujac scene.
        prompty = generate_image_prompts_czysty(scenariusz, model=DEFAULT_MODEL, jezyk="pl")
    else:
        prompty = generate_image_prompts(scenariusz)
    save_text(folder, "prompts.txt", prompty)
    return prompty


def _notify_telegram_checkpoint(folder: Path, ostrzezenia: list = None):
    """Powiadomienie Telegram gdy rolka dojdzie do checkpointu (Dyskusja
    09.07.2026 - Tomasz nie chce siedziec i pilnowac panelu, chce dostac
    powiadomienie). Osobny webhook/automatyzacja od tej dla gotowej rolki,
    bo tu wysylamy TEKST (jeszcze nie ma wideo), nie send_video."""
    import requests
    try:
        reel_id = folder.name
        link = "http://157-90-155-155.sslip.io:8000/panel"
        if ostrzezenia:
            ostrzezenie_txt = "\n⚠️ Automatyczny detektor zglosil uwage - sprawdz uwaznie przed zatwierdzeniem."
        else:
            ostrzezenie_txt = ""
        wiadomosc = f"🧐 Rolka {reel_id} czeka na weryfikacje scenariusza (checkpoint).{ostrzezenie_txt}\n{link}"
        requests.post(
            "https://kzdoj77rzm29x15ipkor8zo2jnh884rs.ui.nabu.casa/api/webhook/fabryka_checkpoint_gotowy",
            json={"wiadomosc": wiadomosc},
            timeout=15,
        )
        _log(f"powiadomienie Telegram (checkpoint) wyslane ({reel_id})")
    except Exception as e:
        _log(f"OSTRZEZENIE: powiadomienie Telegram (checkpoint) nie wyslane: {e}")


def _write_status(folder: Path, etap: str, extra: dict = None, kolejnosc: str = None):
    """Zapisuje PRAWDZIWY aktualny etap do status.json w folderze rolki.
    Uzywane przez panel do prawdziwego paska postepu (nie symulacji).
    Ustalone w Dyskusji 08.07.2026 - zasada 'weryfikacja nie halucynacja'.

    kolejnosc (dodane 09.07.2026): "pl" albo "en" - mowi panelowi KTORY
    zestaw/kolejnosc etapow pokazac na pasku postepu. Powod: sciezka "pl"
    generuje audio PRZED obrazami, a sciezka "en_pl"/"czysty" (CZYSTA DROGA)
    generuje obrazy, POTEM tlumaczenie, POTEM dopiero audio - odwrotna
    kolejnosc + dodatkowy etap ktorego "pl" w ogole nie ma. Jeden statyczny
    pasek dla obu sciezek klamal o tym co sie realnie dzieje."""
    import json, datetime
    try:
        data = {"etap": etap, "extra": extra or {}, "ts": datetime.datetime.now().isoformat()}
        if kolejnosc:
            data["kolejnosc"] = kolejnosc
        (folder / "status.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass  # status.json to tylko UI-owy bonus, nigdy nie ma wywalic pipeline'u


def _produce_media(folder: Path, scenes: str, result: dict, prompt_model: str = None, silnik_obrazow: str = None) -> dict:
    """
    Druga połowa pipeline'u: gotowy scenariusz -> audio -> prompty -> obrazy -> wideo.
    Współdzielona przez generate_reel (pełny bieg) i render_from_scenes (z gotowego skryptu).
    Odporna: błąd jednego obrazu nie zabija reszty; render sam pomija brakujące klatki.

    prompt_model -- opcjonalnie nadpisuje model uzywany do promptow obrazow
    (domyslnie Qwen). Dodane dla 'Czysta Droga Bielik' (Dyskusja 09.07.2026),
    gdzie Tomasz chce Bielika na kazdym kroku tekstowym, zero Qwena/Gemmy.
    """
    save_text(folder, "scenes.txt", scenes)
    result["scenes_file"] = str(folder / "scenes.txt")

    _write_status(folder, "lektor", kolejnosc="pl")
    _log("audio (edge-tts)…")
    audio = generate_audio(folder, scenes)
    result["audio_count"] = len(audio)

    _write_status(folder, "obrazy", {"i": 0, "total": 0, "faza": "prompty"}, kolejnosc="pl")
    istniejace_prompty = folder / "prompts.txt"
    if istniejace_prompty.is_file():
        # Prompty juz wygenerowane na checkpoincie (Dyskusja 09.07.2026) -
        # nie licz drugi raz, oszczedza czas i unika niespojnosci.
        _log("prompty obrazow: uzywam gotowych z checkpointu…")
        image_prompts = istniejace_prompty.read_text(encoding="utf-8")
    else:
        _log("prompty obrazow…" + (" (Bielik)" if prompt_model else ""))
        if prompt_model:
            # prompt_model ustawiony = to Czysta Droga Bielik - NAPRAWIONE
            # (rolka 000081), musi isc przez wersje _czysty, bez sekcji
            # "kalarepa/koper" ktora skazi kazdy niezwiazany z ogrodem temat.
            image_prompts = generate_image_prompts_czysty(
                scenes,
                on_progress=lambda i, t: _write_status(folder, "obrazy", {"i": i, "total": t, "faza": "prompty"}, kolejnosc="pl"),
                model=prompt_model,
                jezyk="pl"
            )
        else:
            image_prompts = generate_image_prompts(
                scenes,
                on_progress=lambda i, t: _write_status(folder, "obrazy", {"i": i, "total": t, "faza": "prompty"}, kolejnosc="pl")
            )
        save_text(folder, "prompts.txt", image_prompts)
    result["prompts_file"] = str(folder / "prompts.txt")

    images = generate_images(folder)
    total = len(images)
    _log(f"obrazy fal.ai: {total} szt…")

    konteksty_gemini = {}
    if silnik_obrazow == "nano_banana_pro":
        from src.images.prompts import zbuduj_konteksty_gemini
        konteksty_gemini = zbuduj_konteksty_gemini(scenes, image_prompts)

    ok = 0
    failed = []
    for img in images:
        if _stop_requested(folder):
            _log(f"PRZERWANO przez uzytkownika (po {ok}/{total} obrazach).")
            (folder / "STOP.flag").unlink(missing_ok=True)
            result["status"] = "przerwano"
            _write_status(folder, "przerwano", {"i": ok, "total": total}, kolejnosc="pl")
            return result
        idx = img.get("index")
        try:
            if silnik_obrazow == "nano_banana_pro":
                prompt_do_wyslania = konteksty_gemini.get(idx, img["prompt"])
                res = generate_image(prompt_do_wyslania, Path(img["output"]), silnik="fal-ai/nano-banana-pro")
            else:
                res = generate_image(img["prompt"], Path(img["output"]))
            if res.get("status") == "ok":
                ok += 1
                _write_status(folder, "obrazy", {"i": idx, "total": total, "faza": "render"}, kolejnosc="pl")
                info_ref = " (Nano Banana Pro)" if silnik_obrazow == "nano_banana_pro" else ""
                _log(f"    obraz {idx}/{total} OK{info_ref}")
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

    _write_status(folder, "napisy", kolejnosc="pl")
    _log("napisy (whisper)…")
    subs_res = make_subtitles(folder)
    result["subs_count"] = subs_res.get("count", 0)

    _write_status(folder, "render", kolejnosc="pl")
    _log("renderuje wideo…")
    video = render_video(folder)
    result["video"] = video

    # NAPRAWIONE 09.07.2026 (Dyskusja z Tomaszem, opcja B) - muzyka jest teraz
    # wmiksowana WEWNATRZ render_video() w JEDNYM przebiegu ffmpeg (sidechain
    # ducking pod lektorem), nie osobnym krokiem. final.mp4 (bez muzyki) juz
    # w ogole nie powstaje jako osobny plik - koniec z dublowaniem 474MB na
    # dysku. Ten blok tylko odnotowuje ze muzyka byla juz uwzgledniona.
    if video.get("status") == "ok" and video.get("music"):
        _log(f"muzyka wmiksowana w jednym przebiegu: {video['music']}")
        result["music"] = {"status": "ok", "music": video["music"]}
    if isinstance(video, dict) and video.get("status") == "ok":
        result["video_file"] = video.get("output")
        _write_status(folder, "gotowe", {"video": video.get('output')}, kolejnosc="pl")
        _log(f"GOTOWE: {video.get('output')} (obrazy {ok}/{total})")
        _notify_telegram(folder, result)
    else:
        result["status"] = "partial"
        _write_status(folder, "blad", {"detail": str(video)}, kolejnosc="pl")
        _log(f"Render zwrocil blad: {video}")

    return result


def przetlumacz_scenariusz_podglad_pl(scenes_en: str) -> str:
    """Tlumaczenie CALEGO scenariusza (UJECIE + LEKTOR) na polski, WYLACZNIE
    do podgladu na checkpoincie (Dyskusja 09.07.2026 - Tomasz nie zna
    angielskiego na tyle by wygodnie weryfikowac scenariusz, chce porownac
    polski z angielskim przed zatwierdzeniem). NIC NIE ZAPISUJE na dysku,
    to tylko tekst zwracany do panelu.

    Neutralny prompt (BEZ zalozenia 'film o ogrodnictwie' - patrz komentarz
    w _translate_lektor_to_pl ponizej, ktora ma ten problem dla docelowego
    tlumaczenia lektora; tu unikamy tego swiadomie, bo CZYSTA DROGA moze
    byc o czymkolwiek)."""
    from src.ai.ollama import PROMPT_MODEL
    scenes = parse_scenes(scenes_en)
    if not scenes:
        return scenes_en

    _unload_model(PROMPT_MODEL)

    tekst_en = "\n\n".join(
        f"SCENA {s['scena']}:\nUJECIE: {s['ujecie']}\nLEKTOR: {s['lektor']}"
        for s in scenes
    )
    prompt_tlumacz = (
        "Ponizej jest scenariusz filmu po angielsku, w formacie SCENA N: / "
        "UJECIE: / LEKTOR:. Przetlumacz KAZDE pole UJECIE i LEKTOR na naturalny "
        "polski, zachowujac DOKLADNIE ta sama liczbe scen, numeracje i format. "
        "Nie dodawaj wlasnej interpretacji tematu - tlumacz wiernie to, co jest "
        "napisane, nic wiecej. Odpowiedz WYLACZNIE w formacie SCENA N: / UJECIE: / "
        "LEKTOR:, bez zadnego komentarza przed ani po:\n\n" + tekst_en
    )
    tlumaczenie = generate(prompt_tlumacz, temperature=0.2)
    return _normalize(tlumaczenie)


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

    # NAPRAWIONE 09.07.2026: prompt wczesniej zakladal na sztywno "film o
    # ogrodnictwie" - dobre dla Zapowiedzi (ROD), ale falszywe zalozenie dla
    # CZYSTEJ DROGI, ktora moze byc o czymkolwiek (ta sama funkcja obsluguje
    # OBIE sciezki, bo obie ida przez _produce_media_en_pl). Neutralny opis
    # "narrator krotkiego filmu" dziala dobrze dla tlumaczenia niezaleznie
    # od tematu - to zadanie tlumaczeniowe, nie kreatywne.
    lista = "\n".join(f"{s['scena']}. {s['lektor']}" for s in scenes)
    prompt_tlumacz = (
        "Ponizej jest ponumerowana lista zdan po angielsku - to tekst narratora "
        "(lektora) krotkiego filmu. Przetlumacz KAZDE zdanie na naturalny, cieply "
        "polski, wiernie oddajac tresc oryginalu. Zachowaj TA SAMA numeracje i "
        "kolejnosc, jedno zdanie na linie. Zachowaj nazwy wlasne i skroty "
        "techniczne dokladnie jak w oryginale. Odpowiedz WYLACZNIE po polsku, "
        "bez zadnych komentarzy - tylko ponumerowana lista tlumaczen:\n\n"
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


def _produce_media_en_pl(folder: Path, scenes_en: str, result: dict, silnik_obrazow: str = None) -> dict:
    save_text(folder, "scenes_en.txt", scenes_en)
    result["scenes_file"] = str(folder / "scenes_en.txt")

    _write_status(folder, "obrazy", {"i": 0, "total": 0, "faza": "prompty"}, kolejnosc="en")
    istniejace_prompty = folder / "prompts.txt"
    if istniejace_prompty.is_file():
        _log("prompty obrazow: uzywam gotowych z checkpointu…")
        image_prompts = istniejace_prompty.read_text(encoding="utf-8")
    else:
        _log("prompty obrazow (EN, czysty prompt bez konkurencyjnych przykladow)…")
        image_prompts = generate_image_prompts_czysty(
            scenes_en,
            on_progress=lambda i, t: _write_status(folder, "obrazy", {"i": i, "total": t, "faza": "prompty"}, kolejnosc="en")
        )
        save_text(folder, "prompts.txt", image_prompts)
    result["prompts_file"] = str(folder / "prompts.txt")

    images = generate_images(folder)
    total = len(images)
    _log(f"obrazy fal.ai: {total} szt…")

    konteksty_gemini = {}
    if silnik_obrazow == "nano_banana_pro":
        from src.images.prompts import zbuduj_konteksty_gemini
        konteksty_gemini = zbuduj_konteksty_gemini(scenes_en, image_prompts)

    ok = 0
    failed = []
    for img in images:
        if _stop_requested(folder):
            _log(f"PRZERWANO przez uzytkownika (po {ok}/{total} obrazach).")
            (folder / "STOP.flag").unlink(missing_ok=True)
            result["status"] = "przerwano"
            _write_status(folder, "przerwano", {"i": ok, "total": total}, kolejnosc="en")
            return result
        idx = img.get("index")
        try:
            if silnik_obrazow == "nano_banana_pro":
                prompt_do_wyslania = konteksty_gemini.get(idx, img["prompt"])
                res = generate_image(prompt_do_wyslania, Path(img["output"]), silnik="fal-ai/nano-banana-pro")
            else:
                res = generate_image(img["prompt"], Path(img["output"]))
            if res.get("status") == "ok":
                ok += 1
                _write_status(folder, "obrazy", {"i": idx, "total": total, "faza": "render"}, kolejnosc="en")
                info_ref = " (Nano Banana Pro)" if silnik_obrazow == "nano_banana_pro" else ""
                _log(f"    obraz {idx}/{total} OK{info_ref}")
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
        _write_status(folder, "blad", {"detail": "brak obrazow"}, kolejnosc="en")
        _log("PRZERWANE: brak obrazow, render pominiety.")
        return result

    _write_status(folder, "tlumaczenie", kolejnosc="en")
    _log("tlumaczenie lektora na polski (Bielik)…")
    scenes_pl = _translate_lektor_to_pl(scenes_en)
    save_text(folder, "scenes.txt", scenes_pl)

    _write_status(folder, "lektor", kolejnosc="en")
    _log("audio (edge-tts)…")
    audio = generate_audio(folder, scenes_pl)
    result["audio_count"] = len(audio)

    _write_status(folder, "napisy", kolejnosc="en")
    _log("napisy (whisper)…")
    subs_res = make_subtitles(folder)
    result["subs_count"] = subs_res.get("count", 0)

    _write_status(folder, "render", kolejnosc="en")
    _log("renderuje wideo…")
    video = render_video(folder)
    result["video"] = video

    if video.get("status") == "ok" and video.get("music"):
        _log(f"muzyka wmiksowana w jednym przebiegu: {video['music']}")
        result["music"] = {"status": "ok", "music": video["music"]}
    if isinstance(video, dict) and video.get("status") == "ok":
        result["video_file"] = video.get("output")
        _write_status(folder, "gotowe", {"video": video.get('output')}, kolejnosc="en")
        _log(f"GOTOWE: {video.get('output')} (obrazy {ok}/{total})")
        _notify_telegram(folder, result)
    else:
        result["status"] = "partial"
        _write_status(folder, "blad", {"detail": str(video)}, kolejnosc="en")
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
    polsku - dla zwyklych tematow z bazy, dziala dobrze, NIE ruszac), "en_pl"
    (osobna, wewnetrzna sciezka dla gotowych zapowiedzi serii - Llama po
    angielsku, tlumaczenie Bielikiem), albo "czysty" = CZYSTA DROGA (Dyskusja
    09.07.2026): niezalezna sciezka dla WLASNEGO promptu Tomasza - Qwen3:14B
    pisze artykul i scenariusz po angielsku z neutralnym szablonem (zero
    narzuconego tematu/stylu), checkpoint do weryfikacji, potem obrazy,
    tlumaczenie Bielikiem, lektor, napisy, render.
    """
    if folder is None:
        folder = create_reel_folder()
    _log(f"START (pelny) folder={folder} tryb={tryb} tryb_jezykowy={tryb_jezykowy}")
    # NAPRAWIONE 10.07.2026 (Dyskusja) - surowy prompt Tomasza (to co wpisal
    # w polu "Temat rolki") wczesniej NIGDY nie byl zapisywany na dysku, znikal
    # bezpowrotnie po jednorazowym uzyciu do wywolania modelu (Bielik/Qwen/Llama
    # sa bezstanowe - kazde wywolanie to osobne zapytanie, model niczego nie
    # "pamieta" po fakcie). Rolka 000085 - Tomasz chcial zobaczyc oryginalny
    # prompt, nie dalo sie go odtworzyc zadna droga. Od teraz zapisany zawsze.
    try:
        (folder / "prompt_oryginalny.txt").write_text(prompt, encoding="utf-8")
    except Exception:
        pass
    # Znacznik trybu na dysku (Dyskusja 09.07.2026) - potrzebny bo od "czysty_bielik"
    # w gore mamy WIECEJ NIZ DWIE sciezki zapisujace do tego samego scenes.txt
    # (zwykla "pl" z baza tematow, i "czysty_bielik" z wlasnym promptem Tomasza).
    # Samo istnienie pliku scenes.txt/scenes_en.txt juz nie wystarcza zeby
    # rozroznic KTORYM modelem trzeba wznowic prompty obrazow po checkpoincie.
    try:
        (folder / "tryb_jezykowy.txt").write_text(tryb_jezykowy, encoding="utf-8")
    except Exception:
        pass
    kolejnosc_start = "en" if tryb_jezykowy in ("en_pl", "czysty") else "pl"
    _write_status(folder, "sceny", kolejnosc=kolejnosc_start)
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
                _write_status(folder, "zatrzymano_walidacja", {"problemy": problemy}, kolejnosc="en")
                return result

            if ostrzezenia:
                import json
                (folder / "WARNING.json").write_text(
                    json.dumps({"ostrzezenia": ostrzezenia}, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
                result["warning"] = True
                result["warning_details"] = ostrzezenia

            # Prompty obrazow PRZED checkpointem (Dyskusja 09.07.2026) - darmowe,
            # Tomasz ma je zobaczyc PRZED kosztownym krokiem.
            _log("prompty obrazow (podglad na checkpoint)…")
            _przygotuj_prompty_na_checkpoint(folder, scenes_en, tryb_jezykowy)

            # CHECKPOINT (Dyskusja 09.07.2026) - patrz komentarz w sciezce PL nizej.
            _write_status(folder, "checkpoint", {"warning": bool(ostrzezenia)}, kolejnosc="en")
            result["status"] = "checkpoint"
            result["etap"] = "checkpoint"
            _log("CHECKPOINT (en_pl): scenariusz gotowy, czekam na weryfikacje w panelu")
            _notify_telegram_checkpoint(folder, ostrzezenia)
            return result

        # CZYSTA DROGA (Dyskusja 09.07.2026): niezalezna sciezka, WLASNY prompt
        # Tomasza, zero szablonow tematycznych. Qwen3:14B pisze artykul i
        # scenariusz PO ANGIELSKU (neutralny PROMPT_TEMPLATE_CZYSTY_EN, bez
        # zadnego narzuconego stylu/tematu). Checkpoint pokazuje ten angielski
        # scenariusz do weryfikacji. Po akceptacji: obrazy z angielskiego
        # UJECIA, POTEM Bielik tlumaczy LEKTOR na polski, POTEM audio z
        # przetlumaczonego tekstu, napisy, render - to _produce_media_en_pl
        # (kod wspoldzielony technicznie, koncepcyjnie to zupelnie osobna sciezka).
        if tryb_jezykowy == "czysty":
            from src.ai.ollama import PROMPT_MODEL
            from src.scenes.generator import generate_scenes_czysty_en
            _log("artykul (CZYSTA DROGA, Qwen3:14B)…")
            article_en = generate(prompt, model=PROMPT_MODEL)
            save_text(folder, "article.md", article_en)
            result["article_file"] = str(folder / "article.md")
            if has_repetition_loop(article_en):
                _log("OSTRZEZENIE: wykryto petle powtorzen w artykule!")
                ostrzezenia.append({"etap": "artykul", "fragment": article_en[:150]})

            _log("sceny (CZYSTA DROGA, Qwen3:14B, po angielsku, bez szablonu tematycznego)…")
            scenes_en = generate_scenes_czysty_en(article_en, scene_count, model=PROMPT_MODEL)
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
                _write_status(folder, "zatrzymano_walidacja", {"problemy": problemy}, kolejnosc="en")
                return result

            if ostrzezenia:
                import json
                (folder / "WARNING.json").write_text(
                    json.dumps({"ostrzezenia": ostrzezenia}, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
                result["warning"] = True
                result["warning_details"] = ostrzezenia

            # Prompty obrazow PRZED checkpointem (Dyskusja 09.07.2026).
            _log("prompty obrazow (podglad na checkpoint)…")
            _przygotuj_prompty_na_checkpoint(folder, scenes_en, tryb_jezykowy)

            # CHECKPOINT - 1. weryfikacja, PRZED obrazami (koszt fal.ai).
            _write_status(folder, "checkpoint", {"warning": bool(ostrzezenia)}, kolejnosc="en")
            result["status"] = "checkpoint"
            result["etap"] = "checkpoint"
            _log("CHECKPOINT (CZYSTA DROGA): scenariusz gotowy, czekam na weryfikacje w panelu")
            _notify_telegram_checkpoint(folder, ostrzezenia)
            return result

        # CZYSTA DROGA BIELIK (Dyskusja 09.07.2026, na zadanie Tomasza):
        # jak "czysty", ale ZERO Qwena/Gemmy - Bielik robi WSZYSTKO (artykul,
        # scenariusz, prompty obrazow), CALOSC po polsku, ZERO tlumaczenia
        # (bo nigdy nie przechodzi przez angielski, wiec nie ma czego
        # tlumaczyc z powrotem). Powod usuniecia tlumaczenia: zwykla
        # sciezka "pl" juz dowodzi ze prompty obrazow dzialaja dobrze
        # wprost z polskiego UJECIA - angielski detour w "czysty"/"en_pl"
        # byl niepotrzebny tutaj i to on powodowal mieszanie jezykow
        # (rolka 000080 - UJECIE po polsku, LEKTOR po angielsku w tym
        # samym scenariuszu). Ta sciezka idzie przez _produce_media
        # (dokladnie jak zwykla "pl"), tylko z prompt_model=DEFAULT_MODEL
        # zamiast domyslnego Qwena.
        if tryb_jezykowy == "czysty_bielik":
            from src.ai.ollama import DEFAULT_MODEL
            from src.scenes.generator import generate_scenes_czysty
            _log("artykul (CZYSTA DROGA BIELIK, po polsku)…")
            article = generate(prompt)  # domyslny model = Bielik (DEFAULT_MODEL)
            save_text(folder, "article.md", article)
            result["article_file"] = str(folder / "article.md")
            if has_repetition_loop(article):
                _log("OSTRZEZENIE: wykryto petle powtorzen w artykule!")
                ostrzezenia.append({"etap": "artykul", "fragment": article[:150]})

            _log("sceny (CZYSTA DROGA BIELIK, po polsku, bez szablonu tematycznego)…")
            scenes = generate_scenes_czysty(article, scene_count, model=DEFAULT_MODEL)
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
                _write_status(folder, "zatrzymano_walidacja", {"problemy": problemy}, kolejnosc="pl")
                return result

            if ostrzezenia:
                import json
                (folder / "WARNING.json").write_text(
                    json.dumps({"ostrzezenia": ostrzezenia}, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
                result["warning"] = True
                result["warning_details"] = ostrzezenia

            # Prompty obrazow PRZED checkpointem (Dyskusja 09.07.2026), Bielikiem.
            _log("prompty obrazow (podglad na checkpoint, Bielik)…")
            _przygotuj_prompty_na_checkpoint(folder, scenes, tryb_jezykowy)

            _write_status(folder, "checkpoint", {"warning": bool(ostrzezenia)}, kolejnosc="pl")
            result["status"] = "checkpoint"
            result["etap"] = "checkpoint"
            _log("CHECKPOINT (CZYSTA DROGA BIELIK): scenariusz gotowy, czekam na weryfikacje w panelu")
            _notify_telegram_checkpoint(folder, ostrzezenia)
            return result

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
            _write_status(folder, "zatrzymano_walidacja", {"problemy": problemy}, kolejnosc="pl")
            return result

        if ostrzezenia:
            import json
            (folder / "WARNING.json").write_text(
                json.dumps({"ostrzezenia": ostrzezenia}, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            result["warning"] = True
            result["warning_details"] = ostrzezenia

        # CHECKPOINT (Dyskusja 09.07.2026): po incydencie z rolka 000068 (scenariusz
        # kompletnie odjechal od tematu artykulu, wykryte przez has_repetition_loop,
        # ale pipeline lecial dalej i zaczal placic za fal.ai) - PAUZA jest teraz
        # TWARDA i DOMYSLNA. Produkcja obrazow/wideo NIE rusza automatycznie -
        # czeka na recznej akceptacji z panelu (/reel-checkpoint/{id}/zatwierdz).
        # Prompty obrazow PRZED checkpointem (Dyskusja 09.07.2026).
        _log("prompty obrazow (podglad na checkpoint)…")
        _przygotuj_prompty_na_checkpoint(folder, scenes, tryb_jezykowy)

        _write_status(folder, "checkpoint", {"warning": bool(ostrzezenia)}, kolejnosc="pl")
        result["status"] = "checkpoint"
        result["etap"] = "checkpoint"
        _log("CHECKPOINT: scenariusz gotowy, czekam na weryfikacje w panelu (nie generuje obrazow automatycznie)")
        _notify_telegram_checkpoint(folder, ostrzezenia)
        return result

    except Exception as e:
        _log(f"BLAD KRYTYCZNY: {e}")
        result["status"] = "error"
        result["error"] = str(e)
        result["trace"] = traceback.format_exc().splitlines()[-3:]
        _write_status(folder, "blad", {"detail": str(e)}, kolejnosc=kolejnosc_start)
        return result


def wznow_po_checkpoincie(folder: Path, scenariusz: str = None, tryb_jezykowy: str = "pl", silnik_obrazow: str = None):
    """Wznawia produkcje mediow (audio/obrazy/render) PO recznej akceptacji
    scenariusza na checkpoincie (Dyskusja 09.07.2026 - 'weryfikacja nie
    halucynacja', wersja 2: pauza rowniez PRZED kosztem fal.ai, nie tylko
    przy naprawie gotowej rolki).

    scenariusz -- jesli podany (np. recznie poprawiony w panelu), NADPISUJE
    zapisany na dysku scenes.txt/scenes_en.txt przed wznowieniem. Jesli
    None, uzywa tego co juz lezy na dysku (czyli zwykle zatwierdzenie bez zmian).
    """
    # Odczyt PRAWDZIWEGO trybu ze znacznika na dysku (Dyskusja 09.07.2026) -
    # dokladniejszy niz zgadywanie z nazw plikow (scenes.txt vs scenes_en.txt),
    # bo od "czysty_bielik" mamy DWIE sciezki zapisujace do scenes.txt.
    # Parametr tryb_jezykowy zostaje jako fallback dla starszych rolek bez znacznika.
    try:
        tryb_ze_znacznika = (folder / "tryb_jezykowy.txt").read_text(encoding="utf-8").strip()
        if tryb_ze_znacznika:
            tryb_jezykowy = tryb_ze_znacznika
    except Exception:
        pass

    result = {"status": "ok", "folder": str(folder), "mode": "wznowienie_po_checkpoincie", "tryb_jezykowy": tryb_jezykowy}
    kolejnosc_wzn = "en" if tryb_jezykowy in ("en_pl", "czysty") else "pl"
    if _stop_requested(folder):
        _log(f"WZNOWIENIE ODRZUCONE - rolka {folder.name} oznaczona STOP, nie ruszam produkcji.")
        result["status"] = "przerwano"
        _write_status(folder, "przerwano", {"powod": "STOP uzytkownika"}, kolejnosc=kolejnosc_wzn)
        return result
    try:
        if tryb_jezykowy in ("en_pl", "czysty"):
            if scenariusz:
                save_text(folder, "scenes_en.txt", scenariusz)
                tekst = scenariusz
            else:
                tekst = (folder / "scenes_en.txt").read_text(encoding="utf-8")
            _log(f"WZNOWIENIE ({tryb_jezykowy}) po checkpoincie, folder={folder}")
            return _produce_media_en_pl(folder, tekst, result, silnik_obrazow=silnik_obrazow)
        else:
            if scenariusz:
                save_text(folder, "scenes.txt", scenariusz)
                tekst = scenariusz
            else:
                tekst = (folder / "scenes.txt").read_text(encoding="utf-8")
            prompt_model = None
            if tryb_jezykowy == "czysty_bielik":
                from src.ai.ollama import DEFAULT_MODEL
                prompt_model = DEFAULT_MODEL
            _log(f"WZNOWIENIE ({tryb_jezykowy}) po checkpoincie, folder={folder}")
            return _produce_media(folder, tekst, result, prompt_model=prompt_model, silnik_obrazow=silnik_obrazow)
    except Exception as e:
        _log(f"BLAD KRYTYCZNY (wznowienie po checkpoincie): {e}")
        result["status"] = "error"
        result["error"] = str(e)
        _write_status(folder, "blad", {"detail": str(e)}, kolejnosc=kolejnosc_wzn)
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
