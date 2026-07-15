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
# add_background_music juz niepotrzebny tutaj - render_video wmiksowuje muzyke sam (Dyskusja 09.07.2026)


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

    video = render_video(folder)  # darmowe (ffmpeg), muzyka juz wmiksowana w jednym przebiegu
    wynik["video"] = video
    if isinstance(video, dict) and video.get("status") == "ok":
        wynik["video_final"] = video["output"]
        if video.get("music"):
            wynik["music"] = {"status": "ok", "music": video["music"]}

    return wynik


def audytuj_checkpoint(artykul: str, scenariusz: str) -> dict:
    """Automatyczna weryfikacja checkpointu (Dyskusja 09.07.2026): qwen3:14b
    porownuje artykul ze scenariuszem, wypisuje wady (odjechanie od tematu,
    bledy rzeczowe, powtorzenia) i proponuje poprawiony scenariusz w tym
    samym wywolaniu. Darmowe (lokalny model), wiec mozna sprawdzac za
    kazdym razem przed kliknieciem OK.

    Uzywa PROMPT_MODEL (qwen3:14b) zamiast DEFAULT_MODEL (Bielik), bo to ten
    sam model co przy funkcji NAPRAW - sprawdzony jako wiarygodny przy
    zadaniu 'przepisz scenariusz zachowujac format' (patrz sprawdz_zmiany()
    wyzej: Bielik gubil/wymyslal litery przy temp=0, qwen3 nie).
    """
    prompt = f'''Ponizej jest artykul zrodlowy oraz wygenerowany na jego podstawie scenariusz rolki wideo (format SCENA N: / UJECIE: / LEKTOR:).

Sprawdz CZY scenariusz FAKTYCZNIE trzyma sie tematu artykulu - czy UJECIA i LEKTOR pasuja tresciowo do tego, o czym jest artykul, czy nie ma bledow rzeczowych, czy tresc nie "odjechala" w zupelnie inny temat.

ARTYKUL:
{artykul}

SCENARIUSZ:
{scenariusz}

Odpowiedz WYLACZNIE w dokladnie takim formacie, bez zadnego komentarza przed ani po:

PROBLEMY:
- (krotki opis problemu, po polsku. Jesli scenariusz trzyma sie tematu i nie ma bledow, napisz dokladnie: "Brak problemow - scenariusz trzyma sie tematu artykulu.")

PROPOZYCJA_SCENARIUSZA:
(Jesli sa problemy: przepisz CALY scenariusz od SCENA 1 do ostatniej sceny, naprawiajac WYLACZNIE wskazane problemy tak, zeby scenariusz pasowal do artykulu, w DOKLADNIE takim samym formacie SCENA N: / UJECIE: / LEKTOR:, z ta sama liczba scen co oryginal. Jesli scenariusz jest juz dobry, przepisz go bez zmian, litera w litere.)'''

    # ZMIANA 14.07.2026 (decyzja Tomasza): audyt robi Claude Fable 5 przez
    # Anthropic API zamiast lokalnego qwen3:14b. Powod: Qwen sprawdzal tylko
    # "czy trzyma sie artykulu", a Bielik psuje rzeczy, ktorych Qwen nie widzi
    # (dawki z kosmosu, doniczki zamiast dzialki, cyfry w lektorze, napisy
    # w ujeciach...). Fable 5 dostaje pelna liste grzechow Bielika i NAPRAWIA
    # kazdy z nich. Platne (klucz Tomasza, grosze/audyt); fallback: Qwen.
    import os as _os
    import requests as _req
    _api_key = _os.environ.get("ANTHROPIC_API_KEY")
    odpowiedz = None
    if _api_key:
        _system = (
            "Jesteś redaktorem-audytorem scenariuszy krótkich rolek (9:16) dla polskiego "
            "ogrodu działkowego ROD. Scenariusz napisał lokalny model Bielik — Twoim zadaniem "
            "jest znaleźć i NAPRAWIĆ jego typowe błędy. Sprawdzasz scenariusz przeciwko "
            "artykułowi źródłowemu ORAZ przeciwko tej liście znanych grzechów Bielika:\n"
            "1. AKCJA POZA DZIAŁKĄ: kuchnia, parapet, doniczki, mieszkanie — akcja MUSI dziać "
            "się na działce (grządki, altana, alejki), chyba że temat wprost mówi inaczej.\n"
            "2. WYMYŚLONE DAWKI I PROPORCJE: Bielik zmyśla liczby (np. 'kostka mydła na litr' "
            "zamiast dwóch łyżek wiórków). Każdą dawkę/proporcję weryfikuj z rzetelną wiedzą "
            "ogrodniczą; niebezpieczne popraw.\n"
            "3. FAŁSZYWA PRZYRODA: błędne objawy chorób (mączniak prawdziwy = BIAŁY nalot na "
            "wierzchu liści), zmyślone zachowania zwierząt (turkuć NIE skacze), rośliny "
            "zachowujące się wbrew biologii.\n"
            "4. CYFRY W LEKTORZE: liczby w liniach LEKTOR muszą być SŁOWNIE z poprawną polską "
            "gramatyką ('dziesięć minut', 'co trzy dni', 'jeden do dziewięciu') — NIGDY '10 "
            "minut', '3 dni', '10x', '1:9'. Lektor TTS czyta cyfry bezsensownie.\n"
            "5. URWANE ZDANIA LEKTORA: np. kończące się 'albo...' — dokończ sensownie.\n"
            "6. ABSURDY SPRZĘTOWE: rzeczy, których nikt nie ma na działce (wentylator ogrodowy "
            "dmuchający w grządki) — zamień na realne praktyki (rozstaw, przerzedzanie).\n"
            "7. LEKTOR/NARRATOR W UJĘCIU: opisy typu 'lektor patrzy w kamerę' — generator "
            "obrazów namaluje z tego przypadkowego człowieka. Usuwaj.\n"
            "8. NAPISY W UJĘCIACH: żadnych 'z napisem X', etykiet, kalendarzy z datą — "
            "generator obrazów psuje polskie napisy. Kadry bez tekstu do namalowania.\n"
            "9. POWTÓRZENIA: to samo zdanie/fraza wielokrotnie.\n"
            "10. HACZYK I PĘTLA: scena pierwsza ma zatrzymywać konkretem (nie 'czy wiesz, "
            "że...'), ostatnia ma domykać pętlę do pierwszej + jedno CTA.\n"
            "Zachowaj format SCENA N: / UJĘCIE: / LEKTOR: i liczbę scen. Zdania lektora "
            "krótkie, na jeden wydech, naturalna polszczyzna. Zmieniaj TYLKO to, co jest "
            "błędem z listy lub niezgodnością z artykułem — resztę przepisuj litera w literę."
        )
        try:
            _r = _req.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": _api_key, "anthropic-version": "2023-06-01",
                         "content-type": "application/json"},
                json={"model": "claude-fable-5", "max_tokens": 8192,
                      "system": _system,
                      "messages": [{"role": "user", "content": prompt}]},
                timeout=120)
            _r.raise_for_status()
            odpowiedz = "".join(b.get("text", "") for b in _r.json().get("content", []))
        except Exception as _e:
            odpowiedz = None  # fallback nizej

    if not odpowiedz:
        _unload_text_model()  # zwolnij Bielika z RAM przed qwen3:14b (7.6GB VPS)
        odpowiedz = generate(prompt, model=PROMPT_MODEL, temperature=0.2, max_tokens=4096)

    marker = "PROPOZYCJA_SCENARIUSZA:"
    if marker in odpowiedz:
        czesc_problemy, czesc_propozycja = odpowiedz.split(marker, 1)
    else:
        czesc_problemy, czesc_propozycja = odpowiedz, ""

    czesc_problemy = czesc_problemy.replace("PROBLEMY:", "", 1).strip()
    problemy = [l.strip(" -") for l in czesc_problemy.splitlines() if l.strip().startswith("-")]
    if not problemy and czesc_problemy:
        problemy = [czesc_problemy]

    propozycja = _normalize(czesc_propozycja.strip())

    brak_problemow = len(problemy) == 1 and "brak problemow" in problemy[0].lower()

    # Diff scena-po-scenie (Dyskusja 09.07.2026) - ten sam mechanizm co w
    # sprawdz_zmiany() powyzej: pokazuje DOKLADNIE co model zmienil, zamiast
    # kazac Tomaszowi porownywac dwa dlugie bloki tekstu na oko.
    zmiany = []
    if propozycja and not brak_problemow:
        stare = {s["scena"]: s for s in parse_scenes(scenariusz)}
        nowe = {s["scena"]: s for s in parse_scenes(propozycja)}
        for n in sorted(stare):
            a = stare[n]
            b = nowe.get(n)
            if b is None:
                continue
            zm_uj = a["ujecie"].strip() != b["ujecie"].strip()
            zm_lek = a["lektor"].strip() != b["lektor"].strip()
            if zm_uj or zm_lek:
                zmiany.append({
                    "scena": n, "zmiana_obrazu": zm_uj, "zmiana_audio": zm_lek,
                    "stare_ujecie": a["ujecie"], "nowe_ujecie": b["ujecie"],
                    "stary_lektor": a["lektor"], "nowy_lektor": b["lektor"],
                })

    return {
        "problemy": problemy,
        "propozycja_scenariusza": propozycja,
        "brak_problemow": brak_problemow,
        "zmiany": zmiany,
    }
