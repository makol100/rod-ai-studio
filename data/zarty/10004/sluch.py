import sys
sys.path.insert(0, '/app')
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8')
segs, _ = m.transcribe('/root/rod-ai-studio/data/zarty/10004/final.mp4', language='pl')
for s in segs:
    print(f'{s.start:5.1f}-{s.end:5.1f}  {s.text.strip()}')
