import sys, json, urllib.request
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/awatar'
TEKST = ("Dzień dobry państwu, kłaniam się nisko. Nazywam się Stanisław i od dziś będę państwa "
 "Działkowym Dziennikarzem. Zapraszam na Wiadomości Działkowe. Przyniosę państwu najświeższe "
 "wieści z ogrodu, ważne komunikaty zarządu oraz pogodę, która nas nie zaskoczy. To będzie "
 "nasza wspólna kronika wydarzeń z Rodzinnego Ogrodu Działkowego imienia Józefa Lompy w Woźnikach. "
 "Obiecuję rzetelność i szczyptę humoru, bo na działce nawet chwasty mają czasem swoje dobre strony. "
 "Zatem zapraszam serdecznie przed ekrany. Do usłyszenia przy płocie, z gorącą herbatą w ręku!")
open(f'{B}/powitanie_stanislaw.txt','w').write(TEKST)
print('znaki:', len(TEKST))

r = fal_client.subscribe('fal-ai/elevenlabs/tts/eleven-v3', arguments={
    'text': TEKST, 'voice': 'Daniel', 'language_code': 'pl',
    'stability': 0.4, 'similarity_boost': 0.75, 'speed': 1.0,
    'output_format': 'mp3_44100_128'})
url = (r.get('audio') or {}).get('url') if isinstance(r.get('audio'), dict) else r.get('audio') or r.get('url')
if url:
    urllib.request.urlretrieve(url, f'{B}/powitanie_daniel.mp3')
    print('OK: powitanie_daniel.mp3')
else:
    print('BRAK URL:', json.dumps(r)[:300])
