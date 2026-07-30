import sys, json, urllib.request
pass
import fal_client

B = '/root/rod-ai-studio/data/awatar'
M = 'fal-ai/elevenlabs/tts/eleven-v3'

# TEKST CASTINGU = docelowe intro Izabeli z deklaracja Tomasza (29.07):
# "Zawsze na poczatku moze powiedziec, ze jestem wygenerowanym prezenterem sztucznej inteligencji
#  i zatrudnionym jako reporter do zarzadu."
TEKST = ("Dzień dobry, z tej strony Izabela. "
         "Jestem prezenterką wygenerowaną przez sztuczną inteligencję, pracuję jako reporter "
         "dla zarządu Rodzinnego Ogrodu Działkowego imienia Józefa Lompy w Woźnikach. "
         "Dziś krótko i konkretnie: co się zmienia w naszym ogrodzie i co trzeba zrobić. "
         "Zaczęło się zagospodarowanie wspólnego terenu przy domu działkowca. "
         "Teren był zarośnięty, przez dwa popołudnia pracowała koparka. "
         "Szczegóły znajdziecie w opisie. Do zobaczenia w ogrodzie.")

GLOSY = ['Sarah', 'Alice', 'Matilda', 'Charlotte', 'Jessica', 'Laura']

print(f'ZNAKOW: {len(TEKST)} | GLOSOW: {len(GLOSY)}', flush=True)
udane = 0
for voice in GLOSY:
    try:
        r = fal_client.subscribe(M, arguments={
            'text': TEKST, 'voice': voice, 'language_code': 'pl',
            'stability': 0.4, 'similarity_boost': 0.75, 'speed': 1.0,
            'output_format': 'mp3_44100_128'})
        json.dump(r, open(f'{B}/_iza_{voice}_resp.json', 'w'))
        url = None
        if isinstance(r, dict):
            a = r.get('audio')
            if isinstance(a, dict):
                url = a.get('url')
            elif isinstance(a, str):
                url = a
            url = url or r.get('audio_url') or r.get('url')
        if url:
            urllib.request.urlretrieve(url, f'{B}/iza_casting_{voice}.mp3')
            print(f'OK {voice}', flush=True)
            udane += 1
        else:
            print(f'BRAK URL {voice}: {json.dumps(r)[:160]}', flush=True)
    except Exception as e:
        print(f'BLAD {voice}: {str(e)[:160]}', flush=True)
print(f'KONIEC: {udane}/{len(GLOSY)} glosow', flush=True)
