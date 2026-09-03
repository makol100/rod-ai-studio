from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
for n in ["k01", "k05"]:
    segs, info = m.transcribe(f"/root/rod-ai-studio/data/zarty/10012/{n}.mp4")
    segs = list(segs)
    print(f"=== {n}: jezyk={info.language}({info.language_probability:.2f}) segmentow={len(segs)}", flush=True)
    for s in segs[:5]:
        print(f"   [{s.start:.1f}-{s.end:.1f}] {s.text!r}", flush=True)
