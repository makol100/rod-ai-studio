from pathlib import Path
import subprocess

from src.config import SCENE_COUNT


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def audio_duration(audio: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return max(float(r.stdout.strip()), 1.0)


def make_clip(image: Path, audio: Path | None, output: Path, duration: float):
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-t", str(duration),
        "-i", str(image),
    ]

    if audio and audio.exists():
        cmd += ["-i", str(audio)]
    else:
        cmd += ["-f", "lavfi", "-t", str(duration), "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]

    cmd += [
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,format=yuv420p",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "18",
    ]

    cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]

    cmd += ["-movflags", "+faststart", str(output)]
    run(cmd)


def concat_parts(parts: list[Path], output: Path):
    n = len(parts)
    cmd = ["ffmpeg", "-y"]
    for p in parts:
        cmd += ["-i", str(p)]

    audio_norm = "".join(
        f"[{i}:a:0]aformat=sample_rates=24000:channel_layouts=mono[a{i}];" for i in range(n)
    )
    concat_inputs = "".join(f"[{i}:v:0][a{i}]" for i in range(n))
    filt = audio_norm + concat_inputs + f"concat=n={n}:v=1:a=1[outv][outa]"

    cmd += [
        "-filter_complex", filt,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(output),
    ]
    run(cmd)


def concat_parts_with_music(parts: list[Path], total_duration: float, output: Path, music_path: Path | None):
    """NAPRAWIONE 09.07.2026 (Dyskusja z Tomaszem) - JEDEN przebieg ffmpeg
    zamiast dwoch. Wczesniej: concat_parts() -> final.mp4 (bez muzyki),
    POTEM osobny przebieg add_background_music() -> final_with_music.mp4,
    zostawiajac OBA pliki na dysku (474MB zbednych duplikatow na wszystkich
    rolkach razem - final.mp4 nigdy wiecej nie byl czytany po tym jak
    powstal final_with_music.mp4, bo -c:v copy = identyczne wideo).

    Teraz: sklejanie scen + ducking muzyki pod lektorem dzieje sie w JEDNYM
    wywolaniu ffmpeg. final.mp4 (wersja bez muzyki) nigdy nie powstaje -
    jedyny plik wynikowy to final_with_music.mp4 (albo final.mp4 jesli
    brak sciezki muzyki w assets/music - patrz galaz else nizej).

    total_duration -- suma dlugosci wszystkich czesci (intro+sceny+outro),
    potrzebna zeby przyciac zapetlona muzyke do wlasciwej dlugosci BEZ
    wczesniejszego renderowania i mierzenia gotowego pliku (to wlasnie
    wymagalo dwoch przebiegow poprzednio)."""
    n = len(parts)
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in parts:
        cmd += ["-i", str(p)]

    if music_path is None:
        # brak sciezki muzyki (assets/music puste) - dziala jak stary concat_parts,
        # ale nazwa pliku i tak "final.mp4" (bez muzyki, jedyny wynik).
        audio_norm = "".join(
            f"[{i}:a:0]aformat=sample_rates=24000:channel_layouts=mono[a{i}];" for i in range(n)
        )
        concat_inputs = "".join(f"[{i}:v:0][a{i}]" for i in range(n))
        filt = audio_norm + concat_inputs + f"concat=n={n}:v=1:a=1[outv][outa]"
        cmd += [
            "-filter_complex", filt,
            "-map", "[outv]", "-map", "[outa]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(output),
        ]
        run(cmd)
        return

    cmd += ["-i", str(music_path)]  # ostatni input = sciezka muzyki, indeks [n]

    audio_norm = "".join(
        f"[{i}:a:0]aformat=sample_rates=24000:channel_layouts=mono[a{i}];" for i in range(n)
    )
    concat_inputs = "".join(f"[{i}:v:0][a{i}]" for i in range(n))
    filt = (
        audio_norm + concat_inputs +
        f"concat=n={n}:v=1:a=1[outv][outa_raw];"
        "[outa_raw]asplit=2[narr][sc];"
        f"[{n}:a]aloop=loop=-1:size=2e9,atrim=0:{total_duration},volume=0.4[music];"
        "[music][sc]sidechaincompress=threshold=0.02:ratio=10:attack=50:release=500[ducked];"
        "[narr][ducked]amix=inputs=2:duration=first[aout]"
    )

    cmd += [
        "-filter_complex", filt,
        "-map", "[outv]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(output),
    ]
    run(cmd)


def render_video(folder: Path):
    images = folder / "images"
    audio = folder / "audio"
    video = folder / "video"
    video.mkdir(exist_ok=True)

    intro = Path("/root/rod-ai-studio/assets/branding/rod_profilowe.png")
    concat_file = video / "concat.txt"
    parts_dir = video / "parts"
    parts_dir.mkdir(exist_ok=True)

    parts = []
    total_duration = 0.0  # suma dlugosci wszystkich czesci - potrzebne do przyciecia muzyki w JEDNYM przebiegu (patrz concat_parts_with_music)

    try:
        if intro.exists():
            intro_clip = parts_dir / "00_intro.mp4"
            make_intro_animated(intro, intro_clip)
            parts.append(intro_clip)
            total_duration += 2.5

        # NAPRAWIONE 09.07.2026 (Dyskusja, rolka 000085) - liczba PLIKOW to nie to
        # samo co NAJWYZSZY NUMER sceny. Gdy usunieto srodkowa scene (np. 09.jpg
        # skasowany recznie), plikow zostalo mniej (9 zamiast 10: 01-08,10), wiec
        # stary kod (max(liczba_plikow, SCENE_COUNT)) w ogole nie sprawdzal i=10 -
        # ostatnia, istniejaca scena znikala z wideo w milczeniu.
        numery_scen = [int(p.stem) for p in images.glob('*.jpg') if p.stem.isdigit()] if images.exists() else []
        najwyzszy_numer = max(numery_scen) if numery_scen else 0
        upper_bound = max(najwyzszy_numer, SCENE_COUNT)
        for i in range(1, upper_bound + 1):
            img = images / f"{i:02d}.jpg"
            wav = audio / f"{i:02d}.wav"
            if img.exists():
                clip = parts_dir / f"{i:02d}.mp4"
                duration = audio_duration(wav) if wav.exists() else 2.5
                make_clip_kb(img, wav if wav.exists() else None, clip, duration, subs=(folder / "subs" / f"{i:02d}.ass"))
                parts.append(clip)
                total_duration += duration

        # OUTRO — plansza logo na koncu kazdej rolki.
        # Uzyj outro.png jesli istnieje, w przeciwnym razie tej samej planszy co intro.
        outro = Path("/root/rod-ai-studio/assets/branding/outro.png")
        if not outro.exists():
            outro = intro
        if outro.exists():
            outro_clip = parts_dir / "99_outro.mp4"
            make_outro_animated(outro, outro_clip)
            parts.append(outro_clip)
            total_duration += 3.0

        if not parts:
            return {"status": "error", "stderr": "No intro or image clips found"}

        concat_file.write_text(
            "".join([f"file '{p}'\n" for p in parts]),
            encoding="utf-8"
        )

        # Muzyka wmiksowana W TYM SAMYM przebiegu ffmpeg (Dyskusja 09.07.2026) -
        # final.mp4 (bez muzyki) juz nigdy nie powstaje jako osobny plik.
        from src.audio.music import pick_track
        music_path = pick_track()
        output = video / ("final_with_music.mp4" if music_path else "final.mp4")
        concat_parts_with_music(parts, total_duration, output, music_path)

        return {
            "status": "ok",
            "output": str(output),
            "intro": str(intro),
            "concat": str(concat_file),
            "parts": [str(p) for p in parts],
            "music": str(music_path) if music_path else None,
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "stderr": e.stderr.decode(errors="ignore") if isinstance(e.stderr, bytes) else str(e.stderr),
            "concat": concat_file.read_text(encoding="utf-8") if concat_file.exists() else "",
        }


def make_clip_kb(image: Path, audio: Path | None, output: Path, duration: float, subs: Path | None = None):
    """
    Klip sceny z subtelnym najazdem Ken Burns (powolny zoom-in ~6%, wycentrowany).
    Ciecie miedzy scenami zostaje twarde - kazda scena od razu delikatnie wjezdza.
    2x upscale przed zoompan zapewnia plynnosc; -framerate 30 pilnuje dlugosci = audio.
    """
    fps = 30
    frames = max(int(round(duration * fps)), 2)
    last = frames - 1

    zoom = (
        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
        "scale=2160:3840,"
        f"zoompan=z='min(1.0+0.06*on/{last}\\,1.06)':d=1:"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
        "format=yuv420p"
    )

    cmd = ["ffmpeg", "-y", "-framerate", "30", "-loop", "1", "-t", str(duration), "-i", str(image)]

    if audio and audio.exists():
        cmd += ["-i", str(audio)]
    else:
        cmd += ["-f", "lavfi", "-t", str(duration), "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]

    vf = zoom
    if subs is not None and Path(subs).exists():
        subs_esc = str(subs).replace("\\", "/").replace(":", "\\:")
        vf = zoom + ",ass=" + subs_esc

    cmd += [
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-movflags", "+faststart", str(output),
    ]
    run(cmd)


def make_intro_animated(image: Path, output: Path):
    """
    Animowane intro: logo wylania sie z czerni + delikatny zoom-settle + polysk.
    Wszystko w ffmpeg, bez dodatkowych plikow. Stala dlugosc 2.5 s.
    """
    fc = (
        "color=c=white:s=240x2200:d=2.5:r=30,format=rgba,"
        "geq=r=255:g=255:b=255:a='clip(120*exp(-pow((X-120)/60\\,2))\\,0\\,255)'[shine];"
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
        "scale=2160:3840,"
        "zoompan=z='max(1.06-0.06*on/36\\,1.0)':d=1:"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
        "format=yuv420p,fade=t=in:st=0:d=0.5[base];"
        "[base][shine]overlay=x='-240+(t-0.7)/0.9*1320':y='(H-h)/2':"
        "enable='between(t\\,0.7\\,1.6)':format=yuv420[outv]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-framerate", "30", "-loop", "1", "-t", "2.5", "-i", str(image),
        "-f", "lavfi", "-t", "2.5", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-filter_complex", fc,
        "-map", "[outv]", "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-movflags", "+faststart", str(output),
    ]
    run(cmd)


def make_intro_animated(image: Path, output: Path):
    """
    NOWE intro: okragle logo WYLANIA SIE Z CZERNI + zoom-settle + polysk po logo.
    Konczy na logo (ciecie do sceny 1). Stala dlugosc 2.5 s. Nadpisuje wczesniejsza definicje.
    """
    fc = (
        "color=c=black:s=1080x1920:d=2.5:r=30[bg];"
        "color=c=gray:s=900x900:d=2.5:r=30,format=gray,"
        "geq=lum='clip((448-hypot(X-450\\,Y-450))*40\\,0\\,255)'[m];"
        "color=c=white:s=140x900:d=2.5:r=30,format=rgba,"
        "geq=r=255:g=255:b=255:a='clip(120*exp(-pow((X-70)/38\\,2))\\,0\\,255)'[sh];"
        "[0:v]scale=900:900[lg];"
        "[lg][sh]overlay=x='-140+(t-0.9)/0.8*1040':y=0:enable='between(t\\,0.9\\,1.7)'[lgs];"
        "[lgs][m]alphamerge[circle];"
        "[bg][circle]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p,"
        "scale=2160:3840,zoompan=z='max(1.06-0.06*on/36\\,1.0)':d=1:"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
        "fade=t=in:st=0:d=0.7[outv]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-framerate", "30", "-loop", "1", "-t", "2.5", "-i", str(image),
        "-f", "lavfi", "-t", "2.5", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-filter_complex", fc,
        "-map", "[outv]", "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-movflags", "+faststart", str(output),
    ]
    run(cmd)


def make_outro_animated(image: Path, output: Path):
    """
    NOWE outro: okragle logo WYLANIA SIE Z CZERNI, chwila, i CHOWA SIE W CZERN.
    Rolka konczy na czerni. Stala dlugosc 3.0 s.
    """
    fc = (
        "color=c=black:s=1080x1920:d=3:r=30[bg];"
        "color=c=gray:s=900x900:d=3:r=30,format=gray,"
        "geq=lum='clip((448-hypot(X-450\\,Y-450))*40\\,0\\,255)'[m];"
        "[0:v]scale=900:900[lg];"
        "[lg][m]alphamerge[circle];"
        "[bg][circle]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p,"
        "fade=t=in:st=0:d=0.6,fade=t=out:st=2.3:d=0.7[outv]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-framerate", "30", "-loop", "1", "-t", "3", "-i", str(image),
        "-f", "lavfi", "-t", "3", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-filter_complex", fc,
        "-map", "[outv]", "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-movflags", "+faststart", str(output),
    ]
    run(cmd)
