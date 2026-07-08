"""
Naprawa istniejacej rolki na podstawie zgloszenia uzytkownika (funkcja "NAPRAW" w panelu).

Dwuetapowy przeplyw, zeby nie placic za fal.ai bez przegladu:
  1) sprawdz_zmiany(folder, skarga) -> model przepisuje CALY scenariusz (PROMPT_MODEL - obecnie qwen3:14b,
     za darmo, lokalnie), kod diffuje stary vs nowy scena-po-scenie.
  2) zastosuj_zmiany(folder, ...) -> scala stary+nowy wg zaakceptowanych numerow scen,
     i SURGICZNIE regeneruje TYLKO to co faktycznie zaakceptowano:
       - obraz (fal.ai FLUX, kosztowe) tylko dla zaakceptowanych scen ze zmiana UJECIA
       - audio (edge-tts, darmowe) + napisy (fal.ai Whisper, kosztowe) tylko dla
         zaakceptowanych scen ze zmiana LEKTORA
     Reszta plikow (obrazy/audio/napisy niezmienionych scen) zostaje NIETKNIETA.
"""
from pathlib import Path
import subprocess

from src.ai.ollama import generate, PROMPT_MODEL
from src.scenes.generator import _normalize, parse_scenes
from src.images.prompts import generate_image_prompts
from src.images.generator import generate_images
from src.ai.image_backend import generate_image
from src.audio.generator import EDGE_TTS_BIN, EDGE_TTS_VOICE, _TTS_ENV
from src.images.prompts import _unload_text_model
from src.subtitles.generator import transcribe_scene, build_ass
from src.video.renderer import render_video
from src.audio.music import add_background_music


def znajdz_folder(base: str, reel_id: str):
    cands = [reel_id]
    if reel_id.isdigit():
        cands.append(reel_id.zfill(6))
    for c in cands:
        d = Path(base) / c
        if d.is_dir():
            return d
    return None


def sprawdz_zmiany(folder: Path, skarga: str) -> dict:
    stary_tekst = (folder / "scenes.txt").read_text(encoding="utf-8")

    prompt = f'''Oto scenariusz rolki (SCENA / UJĘCIE / LEKTOR) i uwaga uzytkownika o bledzie - uwaga moze juz zawierac poprawna wartosc, ktora nalezy uzyc dokladnie.

SCENARIUSZ:
{stary_tekst}

UWAGA UZYTKOWNIKA: {skarga}

Zadanie: znajdz WSZYSTKIE miejsca ktorych dotyczy uwaga i popraw je. Przepisz CALY scenariusz od SCENA 1 do ostatniej sceny, w DOKLADNIE takim samym formacie jak wyzej (SCENA N: / UJĘCIE: / LEKTOR:), z ta sama liczba scen co w oryginale. Sceny ktorych uwaga NIE dotyczy zostaw BEZ ZMIAN, litera w litere - nie "ulepszaj" niczego innego poza tym, o co poprosil uzytkownik.

Nie pisz nic przed SCENA 1 ani po ostatniej scenie. Nie dodawaj wstepu ani podsumowania.'''

    _unload_text_model()  # zwolnij Bielika z RAM (7.6GB VPS, oba modele naraz sie nie miesza)
    # gemma3:4b: w testach dużo bardziej wiarygodny niż Bielik-Q8_0 przy "przepisz prawie bez zmian"
    # (Bielik gubił/wymyslal litery nawet przy temp=0; gemma3:4b powtarzalnie poprawny 2x z rzedu)
    nowy_tekst = _normalize(generate(prompt, model=PROMPT_MODEL, temperature=0.1))  # lepszy niz gemma3:4b: lapie WSZYSTKIE wystapienia literowki, nie tylko pierwsze

    stare = {s["scena"]: s for s in parse_scenes(stary_tekst)}
    nowe = {s["scena"]: s for s in parse_scenes(nowy_tekst)}

    ostrzezenie = None
    if len(stare) != len(nowe):
        ostrzezenie = f"Liczba scen sie zmienila ({len(stare)} -> {len(nowe)}) - sprawdz uwaznie przed zastosowaniem."

    zmiany = []
    for n in sorted(stare):
        a = stare[n]
        b = nowe.get(n)
        if b is None:
            zmiany.append({
                "scena": n, "zmiana_obrazu": False, "zmiana_audio": False, "brak_w_nowym": True,
                "stare_ujecie": a["ujecie"], "nowe_ujecie": a["ujecie"],
                "stary_lektor": a["lektor"], "nowy_lektor": a["lektor"],
            })
            continue
        zm_uj = a["ujecie"].strip() != b["ujecie"].strip()
        zm_lek = a["lektor"].strip() != b["lektor"].strip()
        zmiany.append({
            "scena": n, "zmiana_obrazu": zm_uj, "zmiana_audio": zm_lek,
            "stare_ujecie": a["ujecie"], "nowe_ujecie": b["ujecie"],
            "stary_lektor": a["lektor"], "nowy_lektor": b["lektor"],
        })

    return {
        "nowy_scenariusz": nowy_tekst,
        "zmiany": zmiany,
        "ostrzezenie": ostrzezenie,
        "liczba_zmienionych": sum(1 for z in zmiany if z["zmiana_obrazu"] or z["zmiana_audio"]),
    }


def _scena_do_tekstu(n: int, ujecie: str, lektor: str) -> str:
    return f"SCENA {n}:\nUJĘCIE: {ujecie}\nLEKTOR: {lektor}\n"


def zastosuj_zmiany(folder: Path, stary_tekst: str, nowy_tekst: str, zaakceptowane: set) -> dict:
    stare = {s["scena"]: s for s in parse_scenes(stary_tekst)}
    nowe = {s["scena"]: s for s in parse_scenes(nowy_tekst)}

    merged = {}
    do_obrazu = []
    do_audio = []
    for n in sorted(stare):
        a = stare[n]
        b = nowe.get(n, a)
        if n in zaakceptowane:
            merged[n] = b
            if a["ujecie"].strip() != b["ujecie"].strip():
                do_obrazu.append(n)
            if a["lektor"].strip() != b["lektor"].strip():
                do_audio.append(n)
        else:
            merged[n] = a

    merged_tekst = "".join(_scena_do_tekstu(n, merged[n]["ujecie"], merged[n]["lektor"]) for n in sorted(merged))
    (folder / "scenes.txt").write_text(merged_tekst, encoding="utf-8")

    wynik = {"do_obrazu": do_obrazu, "do_audio": do_audio,
             "obrazy_ok": [], "obrazy_blad": [], "audio_ok": [], "audio_blad": []}

    if do_obrazu:
        nowe_prompty = generate_image_prompts(merged_tekst)  # llama3.1:8b, darmowe (lokalny ollama, nie fal.ai)
        (folder / "prompts.txt").write_text(nowe_prompty, encoding="utf-8")
        images_meta = generate_images(folder)  # tylko parsuje prompts.txt, darmowe
        for img in images_meta:
            if img["index"] in do_obrazu:
                res = generate_image(img["prompt"], Path(img["output"]))  # KOSZTOWNE (fal.ai)
                if res.get("status") == "ok":
                    wynik["obrazy_ok"].append(img["index"])
                else:
                    wynik["obrazy_blad"].append({"scena": img["index"], "blad": res.get("error")})

    audio_dir = folder / "audio"
    subs_dir = folder / "subs"
    audio_dir.mkdir(parents=True, exist_ok=True)
    subs_dir.mkdir(parents=True, exist_ok=True)
    for n in do_audio:
        text = merged[n]["lektor"].strip('"').strip("*").replace("*", "").strip()
        wav = audio_dir / f"{n:02d}.wav"
        mp3_tmp = audio_dir / f"{n:02d}.mp3"
        try:
            subprocess.run([EDGE_TTS_BIN, "--voice", EDGE_TTS_VOICE, "--text", text,
                             "--write-media", str(mp3_tmp)], check=True, env=_TTS_ENV)  # darmowe
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp3_tmp), str(wav)], check=True)
            mp3_tmp.unlink(missing_ok=True)
            segments = transcribe_scene(wav)  # KOSZTOWNE (fal.ai Whisper) - tylko ta 1 scena
            if segments:
                build_ass(segments, subs_dir / f"{n:02d}.ass")
            wynik["audio_ok"].append(n)
        except Exception as e:
            wynik["audio_blad"].append({"scena": n, "blad": str(e)})

    video = render_video(folder)  # darmowe (ffmpeg)
    wynik["video"] = video
    if isinstance(video, dict) and video.get("status") == "ok":
        video_path = Path(video["output"])
        music_output = video_path.with_name("final_with_music.mp4")
        music_result = add_background_music(video_path, music_output)  # darmowe
        wynik["music"] = music_result
        wynik["video_final"] = music_result.get("output") if music_result.get("status") == "ok" else video["output"]

    return wynik
