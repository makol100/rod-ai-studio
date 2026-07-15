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

GLOSY = {"HENIEK": "pl-PL-MarekNeural", "HALINKA": "pl-PL-ZofiaNeural"}
KOLORY_ASS = {"HENIEK": "&H00D7FF&", "HALINKA": "&HFFD7A0&"}  # BGR: zloty / blekit
VEO_MODEL = "fal-ai/veo3.1/fast/image-to-video"


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


# ---------------------------------------------------------------- KADR
def zrob_kadr(folder: Path, styl: str) -> Path:
    from src.ai.image_backend import generate_image
    kadr = folder / "kadr.jpg"
    if not kadr.is_file():
        _log(folder, "kadr referencyjny (Nano Banana Pro)…")
        generate_image(styl, kadr, silnik="fal-ai/nano-banana-pro")
        _log(folder, "kadr OK")
    return kadr


# ---------------------------------------------------------------- KLIPY VEO
def zrob_klipy(folder: Path, klipy: list, kadr: Path):
    import fal_client
    img_url = fal_client.upload_file(str(kadr))
    _log(folder, f"kadr wgrany na fal: {img_url[:60]}…")
    for k in klipy:
        out = folder / f"klip_{k['nr']:02d}.mp4"
        if out.is_file():
            _log(folder, f"klip {k['nr']} już jest — pomijam")
            continue
        _log(folder, f"klip {k['nr']}/{len(klipy)} Veo…")
        prompt = (f"{k['ruch']} Postacie i miejsce dokładnie jak na obrazie referencyjnym. "
                  f"Ciepła animacja 3D, letnie światło na polskiej działce.")
        args = {"prompt": prompt, "image_url": img_url, "aspect_ratio": "9:16",
                "duration": "8s", "resolution": "720p", "generate_audio": False}
        try:
            res = fal_client.run(VEO_MODEL, arguments=args)
        except Exception as e:
            _log(folder, f"klip {k['nr']}: pelne argumenty odrzucone ({str(e)[:120]}), probuje minimalnych")
            res = fal_client.run(VEO_MODEL, arguments={"prompt": prompt, "image_url": img_url})
        url = res["video"]["url"]
        _run(["curl", "-sL", "-o", str(out), url])
        if not out.is_file() or out.stat().st_size < 50000:
            raise RuntimeError(f"klip {k['nr']}: pobieranie nieudane")
        _log(folder, f"klip {k['nr']} OK ({out.stat().st_size//1024} KB)")


# ---------------------------------------------------------------- DIALOGI
def _kwestie(dialog: str) -> list:
    """'HENIEK (krzywiąc usta): "tekst" / HALINKA: "tekst"' -> [(kto, tekst), ...]"""
    out = []
    for m in re.finditer(r'(HENIEK|HALINKA)[^:"]*:\s*"([^"]+)"', dialog):
        tekst = re.sub(r"\([^)]*\)", "", m.group(2)).strip()  # didaskalia out
        if tekst:
            out.append((m.group(1), tekst))
    return out


def zrob_dialogi(folder: Path, klipy: list):
    import asyncio
    import edge_tts

    async def _tts(tekst, glos, out):
        await edge_tts.Communicate(tekst, glos, rate="+5%").save(str(out))

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


def zrob_napisy(folder: Path, klipy: list):
    naglowek = """[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV
Style: H,Arial,52,{h},&H000000&,&H80000000&,1,3,1,2,40,40,190
Style: A,Arial,52,{a},&H000000&,&H80000000&,1,3,1,2,40,40,190

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""".format(h=KOLORY_ASS["HENIEK"], a=KOLORY_ASS["HALINKA"])
    for k in klipy:
        linie = []
        t = 0.35  # dialog startuje chwilę po początku klipu
        for kw in k.get("kwestie", []):
            styl = "H" if kw["kto"] == "HENIEK" else "A"
            linie.append(f"Dialogue: 0,{_ass_czas(t)},{_ass_czas(t + kw['dl'])},{styl},,0,0,0,,"
                         f"{kw['kto'].title()}: {kw['tekst']}")
            t += kw["dl"] + 0.45
        (folder / f"napisy_{k['nr']:02d}.ass").write_text(naglowek + "\n".join(linie),
                                                          encoding="utf-8")


# ---------------------------------------------------------------- RENDER
def zloz(folder: Path, klipy: list) -> Path:
    parts = []
    for k in klipy:
        klip = folder / f"klip_{k['nr']:02d}.mp4"
        dialog = folder / f"dialog_{k['nr']:02d}.wav"
        ass = folder / f"napisy_{k['nr']:02d}.ass"
        part = folder / f"part_{k['nr']:02d}.mp4"
        vf = f"scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2"
        if ass.is_file():
            vf += f",subtitles={ass}"
        if dialog.is_file():
            _run(["ffmpeg", "-y", "-v", "error", "-i", str(klip),
                  "-itsoffset", "0.35", "-i", str(dialog),
                  "-vf", vf, "-map", "0:v", "-map", "1:a",
                  "-c:v", "libx264", "-preset", "medium", "-crf", "21",
                  "-c:a", "aac", "-shortest", "-pix_fmt", "yuv420p", str(part)])
        else:
            _run(["ffmpeg", "-y", "-v", "error", "-i", str(klip), "-vf", vf,
                  "-an", "-c:v", "libx264", "-crf", "21", "-pix_fmt", "yuv420p", str(part)])
        parts.append(part)
        _log(folder, f"part {k['nr']} zlozony")

    lista = folder / "concat.txt"
    lista.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
    final = folder / "final.mp4"
    _run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
          "-c:v", "libx264", "-crf", "21", "-c:a", "aac", "-pix_fmt", "yuv420p", str(final)])
    _log(folder, f"FINAL: {final} ({final.stat().st_size//1024} KB)")
    return final


# ---------------------------------------------------------------- CAŁOŚĆ
def produkuj(folder: Path, styl_bohaterow: str):
    """Pełna produkcja żartu — wołać W WĄTKU. Stany w meta.json."""
    from src.zarty import _parsuj
    try:
        _meta(folder, stan="produkcja", start_produkcji=time.time())
        klipy = _parsuj((folder / "scenariusz.txt").read_text(encoding="utf-8"))
        if not klipy:
            raise RuntimeError("scenariusz nie parsuje się na klipy")
        kadr = zrob_kadr(folder, styl_bohaterow)
        _meta(folder, stan="klipy_veo")
        zrob_klipy(folder, klipy, kadr)
        _meta(folder, stan="dialogi")
        zrob_dialogi(folder, klipy)
        zrob_napisy(folder, klipy)
        _meta(folder, stan="render")
        final = zloz(folder, klipy)
        _meta(folder, stan="gotowy", final=str(final))
        # telegram tym samym webhookiem co rolki
        try:
            import requests
            url = f"https://panel.157-90-155-155.sslip.io/zarty/{folder.name}/video"
            requests.post("https://kzdoj77rzm29x15ipkor8zo2jnh884rs.ui.nabu.casa/api/webhook/fabryka_rolka_gotowa",
                          json={"video_url": url, "caption": f"\U0001F3AD Żart {folder.name} gotowy!\n{url}"},
                          timeout=15)
            _log(folder, "telegram wyslany")
        except Exception as e:
            _log(folder, f"telegram nieudany: {e}")
    except Exception as e:
        _meta(folder, stan="blad", blad=str(e)[:300])
        _log(folder, f"BLAD PRODUKCJI: {e}")
