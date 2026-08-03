import sys; sys.path.insert(0,'/app')
from faster_whisper import WhisperModel
m = WhisperModel('medium', device='cpu', compute_type='int8')
for f in ['k03_a.wav','k04r_a.wav','k05r_a.wav','glos_Ef16.wav']:
    segs,_ = m.transcribe(f, language='pl', vad_filter=True)
    segs=list(segs)
    print(f, '|', ' || '.join(f"{s.start:.2f}-{s.end:.2f} {s.text.strip()}" for s in segs) if segs else 'CISZA')
