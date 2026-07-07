from pathlib import Path
import fal_client

WHISPER_MODEL = "fal-ai/whisper"
WHISPER_TIMEOUT = 300
WHISPER_START_TIMEOUT = 120
UPLOAD_TIMEOUT = 120
RETRIES = 1

PLAY_RES_X = 1080
PLAY_RES_Y = 1920
FONT_NAME = "DejaVu Sans"
FONT_SIZE = 54
MARGIN_V = 180
WORDS_PER_LINE = 6

COLOR_TEXT = "&H00FFFFFF"
COLOR_OUTLINE = "&H00000000"
COLOR_BACK = "&H80000000"


def _sec_to_ass_time(t):
    if t < 0:
        t = 0.0
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    cs = int(round((t - int(t)) * 100))
    if cs == 100:
        cs = 0
        s += 1
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _wrap_words(text, n):
    words = text.split()
    if not words:
        return ""
    lines = [" ".join(words[i:i + n]) for i in range(0, len(words), n)]
    return "\\N".join(lines)


def _ass_escape(text):
    return text.replace("{", "(").replace("}", ")").strip()


def transcribe_scene(wav):
    last_err = None
    for attempt in range(1, RETRIES + 2):
        try:
            audio_url = fal_client.upload_file(str(wav))
            result = fal_client.subscribe(
                WHISPER_MODEL,
                arguments={
                    "audio_url": audio_url,
                    "task": "transcribe",
                    "language": "pl",
                    "chunk_level": "word",
                },
            )
            chunks = result.get("chunks") or []
            words = []
            for ch in chunks:
                ts = ch.get("timestamp") or [None, None]
                start = ts[0] if ts and ts[0] is not None else None
                end = ts[1] if ts and len(ts) > 1 and ts[1] is not None else None
                txt = (ch.get("text") or "").strip()
                if txt and start is not None and end is not None:
                    words.append({"start": float(start), "end": float(end), "text": txt})
            groups = []
            for k in range(0, len(words), WORDS_PER_LINE):
                grp = words[k:k + WORDS_PER_LINE]
                if not grp:
                    continue
                groups.append({"start": grp[0]["start"], "end": grp[-1]["end"], "text": " ".join(w["text"] for w in grp)})
            if groups:
                return groups
            full = (result.get("text") or "").strip()
            if full:
                return [{"start": 0.0, "end": None, "text": full}]
            return []
        except Exception as e:
            last_err = e
            print(f"[napisy] proba {attempt} nieudana dla {wav.name}: {e}", flush=True)
    print(f"[napisy] REZYGNACJA z napisow dla {wav.name}: {last_err}", flush=True)
    return []


def build_ass(segments, out, fallback_duration=3.0):
    out.parent.mkdir(parents=True, exist_ok=True)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {PLAY_RES_X}
PlayResY: {PLAY_RES_Y}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Napis,{FONT_NAME},{FONT_SIZE},{COLOR_TEXT},{COLOR_TEXT},{COLOR_OUTLINE},{COLOR_BACK},0,0,0,0,100,100,0,0,4,3,0,2,60,60,{MARGIN_V},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, Effect, Text
"""
    lines = [header]
    for seg in segments:
        start = seg["start"]
        end = seg["end"]
        if end is None:
            end = start + fallback_duration
        if end <= start:
            end = start + 0.6
        text = _wrap_words(_ass_escape(seg["text"]), WORDS_PER_LINE)
        if not text:
            continue
        lines.append(
            f"Dialogue: 0,{_sec_to_ass_time(start)},{_sec_to_ass_time(end)},Napis,,0,0,0,,{text}\n"
        )
    out.write_text("".join(lines), encoding="utf-8")
    return out


def make_subtitles(folder):
    audio_dir = folder / "audio"
    subs_dir = folder / "subs"
    subs_dir.mkdir(parents=True, exist_ok=True)
    if not audio_dir.exists():
        print("[napisy] brak katalogu audio", flush=True)
        return {"status": "error", "reason": "no audio dir", "count": 0, "files": []}
    wavs = sorted(audio_dir.glob("*.wav"))
    made = []
    for wav in wavs:
        stem = wav.stem
        print(f"[napisy] transkrypcja sceny {stem}...", flush=True)
        segments = transcribe_scene(wav)
        if not segments:
            print(f"[napisy] scena {stem}: brak segmentow, pomijam", flush=True)
            continue
        ass_path = subs_dir / f"{stem}.ass"
        build_ass(segments, ass_path)
        made.append(str(ass_path))
        print(f"[napisy] scena {stem}: {len(segments)} linijek -> {ass_path.name}", flush=True)
    return {"status": "ok" if made else "empty", "count": len(made), "files": made}
