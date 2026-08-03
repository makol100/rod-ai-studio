import sys; sys.path.insert(0,'/app')
from faster_whisper import WhisperModel
m = WhisperModel('medium', device='cpu', compute_type='int8')
for f in ['k03_a.wav','k04r_a.wav','k05r_a.wav','glos_Ef16.wav']:
    segs,_ = m.transcribe(f, language='pl', vad_filter=True, word_timestamps=True)
    ws=[w for s in segs for w in s.words]
    print(f, '|', ' '.join(f"[{w.word.strip()} {w.start:.2f}-{w.end:.2f}]" for w in ws))
