import sys; sys.path.insert(0,'/app')
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(sys.argv[1], language="pl", word_timestamps=True)
for s in segs:
    for w in (s.words or []): print(f"{w.start:.2f}-{w.end:.2f} {w.word}")
