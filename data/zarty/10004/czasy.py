import sys
sys.path.insert(0, '/app')
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8')
for f in ['cut_03.mp4', 'cut_04.mp4']:
    segs, _ = m.transcribe(f'/root/rod-ai-studio/data/zarty/10004/{f}', language='pl', word_timestamps=True)
    print(f'== {f}')
    for s in segs:
        for w in (s.words or []):
            print(f'  {w.start:5.2f}-{w.end:5.2f} {w.word}')
