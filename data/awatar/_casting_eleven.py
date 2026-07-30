import sys, json, urllib.request
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/awatar'
M = 'fal-ai/elevenlabs/tts/eleven-v3'
TEKST = ("Dzień dobry, witamy w najnowszym serwisie informacyjnym ROD Woźniki. "
         "Z tej strony wasz Działkowy Dziennikarz. Przypominam wszystkim działkowcom, "
         "że w najbliższą sobotę odbędzie się obowiązkowy odczyt liczników energii elektrycznej. "
         "Pogoda na jutro zapowiada się wspaniale, więc proszę wyciągać leżaki i obficie podlewać pomidory. "
         "Do usłyszenia przy płocie!")

for voice in ['George', 'Daniel', 'Eric']:
    try:
        r = fal_client.subscribe(M, arguments={
            'text': TEKST, 'voice': voice, 'language_code': 'pl',
            'stability': 0.4, 'similarity_boost': 0.75, 'speed': 1.0,
            'output_format': 'mp3_44100_128'})
        json.dump(r, open(f'{B}/_casting_{voice}_resp.json', 'w'))
        url = None
        if isinstance(r, dict):
            a = r.get('audio')
            if isinstance(a, dict): url = a.get('url')
            elif isinstance(a, str): url = a
            url = url or r.get('audio_url') or r.get('url')
        if url:
            urllib.request.urlretrieve(url, f'{B}/casting_{voice}.mp3')
            print(f'OK {voice}: casting_{voice}.mp3', flush=True)
        else:
            print(f'BRAK URL {voice}: {json.dumps(r)[:200]}', flush=True)
    except Exception as e:
        print(f'BLAD {voice}: {e}', flush=True)
print('KONIEC CASTINGU')
