from faster_whisper import WhisperModel
import sys
m = WhisperModel("medium", compute_type="int8")
segs, info = m.transcribe("/root/rod-ai-studio/data/zarty/10010/klip_k06_niemy.mp4", language="pl", vad_filter=True)
segs = list(segs)
txt = " ".join(s.text.strip() for s in segs).strip()
print(f"TRANSKRYPCJA: '{txt}' | segmentów mowy: {len(segs)}")
ok = len(txt) < 3
print("CISZA:", "PASS — nikt nie mówi" if ok else "FAIL — słychać mowę!")
sys.exit(0 if ok else 1)
