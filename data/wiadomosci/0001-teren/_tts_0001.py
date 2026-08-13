import sys, json, urllib.request
import fal_client
B = '/root/rod-ai-studio/data/wiadomosci/0001-teren'
TEKST = open(f'{B}/scenariusz_0001_v2.txt').read().strip()
assert TEKST.startswith('Dzień dobry państwu, kłaniam się nisko. Zapraszam na Wiadomości Działkowe.'), 'INTRO!'
assert TEKST.endswith('Do usłyszenia przy płocie.'), 'OUTRO!'
print('znaki:', len(TEKST.replace('\n','')))
r = fal_client.subscribe('fal-ai/elevenlabs/tts/eleven-v3', arguments={
    'text': TEKST, 'voice': 'Daniel', 'language_code': 'pl',
    'stability': 0.4, 'similarity_boost': 0.75, 'speed': 1.0,
    'output_format': 'mp3_44100_128'})
url = (r.get('audio') or {}).get('url') if isinstance(r.get('audio'), dict) else r.get('audio') or r.get('url')
if url:
    urllib.request.urlretrieve(url, f'{B}/work/stanislaw_0001.mp3')
    print('OK: stanislaw_0001.mp3')
else:
    print('BRAK URL:', json.dumps(r)[:300]); sys.exit(1)
