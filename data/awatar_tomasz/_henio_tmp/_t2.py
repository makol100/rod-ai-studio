import sys, json
from faster_whisper import WhisperModel
wav = sys.argv[1]
outjson = sys.argv[2]
m = WhisperModel('medium', device='cpu', compute_type='int8')
res = {'segs': [], 'words': [], 'word_ts': False}
try:
    segs, info = m.transcribe(wav, language='pl', word_timestamps=True, beam_size=5)
    res['word_ts'] = True
    for s in segs:
        res['segs'].append([round(s.start,2), round(s.end,2), s.text.strip()])
        for w in (s.words or []):
            res['words'].append([round(w.start,2), w.word.strip(), round(w.probability,2)])
except Exception as e:
    # fallback: segment-level only (word_timestamps bug on some files)
    segs, info = m.transcribe(wav, language='pl', word_timestamps=False, beam_size=5)
    for s in segs:
        res['segs'].append([round(s.start,2), round(s.end,2), s.text.strip()])
    res['words'] = []
    res['word_ts'] = False
    res['err'] = str(e)[:200]
json.dump(res, open(outjson,'w'), ensure_ascii=False)
print('OK', outjson, 'word_ts=', res['word_ts'])
