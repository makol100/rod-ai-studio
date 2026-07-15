# -*- coding: utf-8 -*-
"""
FABRYKA ŻARTÓW — produkcja (Droga B).
kadr referencyjny (NB Pro) -> klipy Veo 3.1 Fast i2v (fal.ai, 8s, 9:16, bez audio)
-> dialogi edge-tts (HENIEK=Marek, HALINKA=Zofia) -> napisy ASS -> ffmpeg concat.
Wszystko per żart w data/zarty/NNNN/. Wołane W TLE z /zart-checkpoint/{id}/zatwierdz.
"""
import json
import re
import subprocess
import time
from pathlib import Path

# 4 postacie z 2 polskich glosow edge-tts: modulacja pitch/rate robi charaktery.
GLOSY_TTS = {  # relikt edge-tts, dialogi robi Veo
    "MIECZYSŁAW": {"voice": "pl-PL-MarekNeural", "rate": "-12%", "pitch": "-14Hz"},  # wolny, niski, wazki
    "TOMASZ":     {"voice": "pl-PL-MarekNeural", "rate": "+16%", "pitch": "+18Hz"},  # nerwowy cwaniak
    "HELENA":     {"voice": "pl-PL-ZofiaNeural", "rate": "+2%",  "pitch": "-2Hz"},   # cieplo, spokojnie
    "JACUŚ":      {"voice": "pl-PL-MarekNeural", "rate": "+8%",  "pitch": "+30Hz"},  # mlody dorosly
    "JÓZEK":      {"voice": "pl-PL-MarekNeural", "rate": "+12%", "pitch": "+45Hz"},  # przestraszony niemowa
}
KOLORY_ASS = {"MIECZYSŁAW": "&H00D7FF&", "HELENA": "&HFFD7A0&",
              "TOMASZ": "&H7AD77A&", "JACUŚ": "&HF0A0F0&", "JÓZEK": "&H55CCFF&"}  # BGR
VEO_MODEL = "fal-ai/veo3.1/fast"  # text-to-video!
# ZMIANA 15.07: i2v z ludzmi na obrazie = twarda blokada content policy Google
# (potwierdzone testami + forum Google). Postacie opisujemy SLOWAMI w kazdym klipie.
OPIS_POSTACI = {
    "MIECZYSŁAW": "starszy pan w kaszkiecie i kamizelce ogrodowej, siwy krotki zarost, spokojne madre oczy",
    "HELENA": "starsza pani z siwym kokiem, kwiecista sukienka i fartuch",
    "TOMASZ": "mezczyzna okolo piecdziesiatki w hawajskiej koszuli i czapce z daszkiem, lekko zaokraglony",
    "JACUŚ": "mlody dorosly mezczyzna z piegami i odstajacymi uszami, luzna koszulka",
}


# === NATYWNE AUDIO VEO (wzorzec z zatwierdzonego testu #9999) ===
OPISY_POSTACI = {
    "MIECZYSŁAW": "MIECZYSLAW, a calm Polish gardener around 70 years old, short grey "
                  "stubble, grey flat cap, olive gardening vest, wise squinting eyes",
    "HELENA": "HELENA, his wife around 65, warm face, grey hair in a bun, floral dress "
              "with a kitchen apron",
    "TOMASZ": "TOMASZ, the neighbour around 50, slightly round, crooked baseball cap, "
              "open Hawaiian shirt, wide uncertain smile",
    "JACUŚ": "JACUS, a young man around 25, slim, protruding ears, freckles, loose t-shirt",
    "JÓZEK": "JOZEK, a skinny scared villager around 40, tousled hair, oversized old brown jacket, wide frightened eyes",
}
GLOSY_VEO = {
    "MIECZYSŁAW": "slowly in Polish with a wise quiet elderly voice",
    "HELENA": "in Polish with a warm motherly voice",
    "TOMASZ": "in Polish with an enthusiastic slightly nervous voice",
    "JACUŚ": "in Polish with a young casual voice",
    "JÓZEK": "in Polish with a thin panicked stuttering voice",
}
STYL_KLIPU = ("Cinematic realistic footage, warm golden summer light. Vertical 9:16. "
              "Natural ambient sounds. No subtitles, no text overlay.")
# Miejsce akcji MUSI byc opisane w scenie (OBRAZ), nie w stylu — inaczej
# styl wymusza plener i sceny wnetrza laduja na podworku (lekcja: klip 2 pilota).


def _postacie_w_klipie(k):
    tekst = (k.get("ruch", "") + " " + k.get("obraz", "") + " " + k.get("mowi", "")
             + " " + k.get("kwestia", "")).upper()
    t = tekst.replace("Ł", "L").replace("Ś", "S")
    return [im for im in OPISY_POSTACI
            if im.replace("Ł", "L").replace("Ś", "S") in t]



def _log(folder: Path, msg: str):
    with open(folder / "log.txt", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")


def _meta(folder: Path, **zmiany):
    p = folder / "meta.json"
    m = json.loads(p.read_text(encoding="utf-8"))
    m.update(zmiany)
    p.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    return m


def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"cmd fail: {' '.join(cmd[:6])}...: {r.stderr[-400:]}")


def _dlugosc(plik: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(plik)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


# ---------------------------------------------------------------- KADR (GLOBALNY)
# Decyzja Tomasza 15.07: "Postacie raz wygenerowane na zawsze" — jeden kadr
# referencyjny dla CAŁEJ serii, w assets, generowany osobnym endpointem
# po akceptacji Tomasza. Produkcja żartu NIGDY nie generuje kadru sama.
KADR_GLOBALNY = Path("/root/rod-ai-studio/assets/zarty/postacie.jpg")


def zrob_kadr_globalny(styl: str, wymus: bool = False) -> Path:
    from src.ai.image_backend import generate_image
    KADR_GLOBALNY.parent.mkdir(parents=True, exist_ok=True)
    if wymus and KADR_GLOBALNY.is_file():
        KADR_GLOBALNY.rename(KADR_GLOBALNY.with_suffix(f".bak-{int(time.time())}.jpg"))
    if not KADR_GLOBALNY.is_file():
        generate_image(styl, KADR_GLOBALNY, silnik="fal-ai/nano-banana-pro")
    return KADR_GLOBALNY


# ---------------------------------------------------------------- KLIPY VEO
def _opis_dla_klipu(tekst: str) -> str:
    """Sklada opisy postaci wystepujacych w klipie (wykrywanie po imionach)."""
    czesci = []
    for imie, opis in OPIS_POSTACI.items():
        if imie.replace("Ł", "L").replace("Ś", "S") in tekst.upper().replace("Ł", "L").replace("Ś", "S"):
            czesci.append(f"{imie} to {opis}")
    return ". ".join(czesci)


def zrob_klipy(folder: Path, klipy: list, kadr=None):
    import fal_client
    for k in klipy:
        out = folder / f"klip_{k['nr']:02d}.mp4"
        if out.is_file():
            _log(folder, f"klip {k['nr']} już jest — pomijam")
            continue
        _log(folder, f"klip {k['nr']}/{len(klipy)} Veo t2v+audio…")
        kto = _postacie_w_klipie(k)
        opisy = ("In frame: " + "; ".join(OPISY_POSTACI[i] for i in kto) + ". ") if kto else ""
        mowi = k.get("mowi", "")
        kwestia = k.get("kwestia", "")
        glos = GLOSY_VEO.get(mowi, "in Polish with a natural voice")
        dialog = (f'{mowi.capitalize()} says {glos}: "{kwestia}" ') if kwestia else ""
        prompt = f"{opisy}Scene: {k['ruch']} {dialog}{STYL_KLIPU}"
        args = {"prompt": prompt, "aspect_ratio": "9:16", "duration": "8s",
                "resolution": "1080p", "generate_audio": True, "auto_fix": True}
        try:
            res = fal_client.run(VEO_MODEL, arguments=args)
        except Exception as e:
            if "content_policy" in str(e):
                raise RuntimeError(f"klip {k['nr']}: Veo odrzucil tresc — popraw OBRAZ/KWESTIE klipu {k['nr']} i zatwierdz ponownie")
            raise
        url = res["video"]["url"]
        _run(["curl", "-sL", "-o", str(out), url])
        if not out.is_file() or out.stat().st_size < 50000:
            raise RuntimeError(f"klip {k['nr']}: pobieranie nieudane")
        _log(folder, f"klip {k['nr']} OK ({out.stat().st_size//1024} KB)")

def _kwestie(dialog: str) -> list:
    """'HENIEK (krzywiąc usta): "tekst" / HALINKA: "tekst"' -> [(kto, tekst), ...]"""
    out = []
    for m in re.finditer(r'(MIECZYS[ŁL]AW|HELENA|TOMASZ|JACU[ŚS]|J[ÓO]ZEK)[^:\n"]{0,80}:\s*[*_\s]*"([^"]+)"', dialog):
        kto = m.group(1).replace("MIECZYSLAW", "MIECZYSŁAW").replace("JACUS", "JACUŚ").replace("JOZEK", "JÓZEK")
        tekst = re.sub(r"\([^)]*\)", "", m.group(2)).strip()  # didaskalia out
        if tekst:
            out.append((kto, tekst))
    return out


def zrob_dialogi(folder: Path, klipy: list):
    import asyncio
    import edge_tts

    async def _tts(tekst, cfg, out):
        await edge_tts.Communicate(tekst, cfg["voice"], rate=cfg["rate"],
                                   pitch=cfg["pitch"]).save(str(out))

    for k in klipy:
        kwestie = _kwestie(k["dialog"])
        k["kwestie"] = []
        czesci = []
        for i, (kto, tekst) in enumerate(kwestie):
            w = folder / f"kw_{k['nr']:02d}_{i}.mp3"
            asyncio.run(_tts(tekst, GLOSY[kto], w))
            d = _dlugosc(w)
            k["kwestie"].append({"kto": kto, "tekst": tekst, "dl": d})
            czesci.append(w)
        # sklejka kwestii klipu z pauza 0.45s
        dialog_wav = folder / f"dialog_{k['nr']:02d}.wav"
        if czesci:
            filtr = "".join(f"[{i}:a]" for i in range(len(czesci)))
            cmd = ["ffmpeg", "-y", "-v", "error"]
            for w in czesci:
                cmd += ["-i", str(w)]
            if len(czesci) == 1:
                cmd += ["-ar", "44100", str(dialog_wav)]
            else:
                cmd += ["-filter_complex",
                        "".join(f"[{i}:a]apad=pad_dur=0.45[p{i}];" for i in range(len(czesci) - 1))
                        + "".join(f"[p{i}]" for i in range(len(czesci) - 1))
                        + f"[{len(czesci)-1}:a]concat=n={len(czesci)}:v=0:a=1[out]",
                        "-map", "[out]", "-ar", "44100", str(dialog_wav)]
            _run(cmd)
        _log(folder, f"dialog {k['nr']}: {len(kwestie)} kwestii, {round(_dlugosc(dialog_wav),1)}s")


# ---------------------------------------------------------------- NAPISY
def _ass_czas(t: float) -> str:
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"



# Naglowek ASS: duze czytelne napisy na 9:16 (1080x1920), u dolu, obrys dla czytelnosci
ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,64,&H00FFFFFF,&H00FFFFFF,&H00101010,&H88000000,-1,0,0,0,100,100,0,0,1,4,2,2,60,60,220,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def zrob_napisy(folder: Path, klipy: list):
    for k in klipy:
        d = _dlugosc(folder / f"klip_{k['nr']:02d}.mp4")
        kolor = KOLORY_ASS.get(k.get("mowi", ""), "&H00FFFFFF")
        ass = folder / f"napisy_{k['nr']:02d}.ass"
        tekst = k.get("kwestia", "")
        ass.write_text(ASS_HEADER + (
            f"Dialogue: 0,{_ass_czas(0.4)},{_ass_czas(max(d-0.2, 1))},Default,,0,0,0,,"
            f"{{\\c{kolor}}}{k.get('mowi','')}: {tekst}\n"), encoding="utf-8")
    _log(folder, "napisy: kwestie na caly klip (duze, bez Whisper)")

def zloz(folder: Path, klipy: list) -> Path:
    party = []
    for k in klipy:
        klip = folder / f"klip_{k['nr']:02d}.mp4"
        ass = folder / f"napisy_{k['nr']:02d}.ass"
        part = folder / f"part_{k['nr']:02d}.mp4"
        vf = f"ass={ass}" if ass.is_file() else "null"
        _run(["ffmpeg", "-y", "-v", "error", "-i", str(klip), "-vf", vf,
              "-c:v", "libx264", "-preset", "medium", "-crf", "21",
              "-c:a", "aac", "-pix_fmt", "yuv420p", str(part)])
        party.append(part)
        _log(folder, f"part {k['nr']} zlozony")
    lista = folder / "concat.txt"
    lista.write_text("".join(f"file '{p}'\n" for p in party), encoding="utf-8")
    final = folder / "final.mp4"
    _run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
          "-c", "copy", str(final)])
    _log(folder, f"FINAL: {final} ({final.stat().st_size//1024} KB)")
    return final

def produkuj(folder: Path, styl_bohaterow: str):
    """Pełna produkcja żartu — wołać W WĄTKU. Stany w meta.json."""
    from src.zarty import _parsuj
    try:
        _meta(folder, stan="produkcja", start_produkcji=time.time())
        klipy = _parsuj((folder / "scenariusz.txt").read_text(encoding="utf-8"))
        if not klipy:
            raise RuntimeError("scenariusz nie parsuje się na klipy")
        _meta(folder, stan="klipy_veo")
        zrob_klipy(folder, klipy)
        _meta(folder, stan="dialogi")
        zrob_napisy(folder, klipy)
        _meta(folder, stan="render")
        final = zloz(folder, klipy)
        _meta(folder, stan="gotowy", final=str(final))
        # telegram tym samym webhookiem co rolki
        try:
            import requests
            url = f"https://panel.157-90-155-155.sslip.io/zarty/{folder.name}/video"
            requests.post("https://kzdoj77rzm29x15ipkor8zo2jnh884rs.ui.nabu.casa/api/webhook/fabryka_rolka_gotowa",
                          json={"video_url": url, "caption": f"\U0001F3AD Żart {folder.name} — WERSJA ROBOCZA (bez montażu i planszy). Gotowa wersja przyjdzie po montażu.\n{url}"},
                          timeout=15)
            _log(folder, "telegram wyslany")
        except Exception as e:
            _log(folder, f"telegram nieudany: {e}")
    except Exception as e:
        _meta(folder, stan="blad", blad=str(e)[:300])
        _log(folder, f"BLAD PRODUKCJI: {e}")
