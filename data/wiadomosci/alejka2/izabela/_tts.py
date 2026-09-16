import sys, json, urllib.request
sys.path.insert(0, '/app')
import fal_client
# TTS Charlotte — Izabela, wydanie Alejka Polnocna cd. (D-0355). Wzorzec: relacja_alejka/_tts_C.py. Grosze.
B = '/root/rod-ai-studio/data/wiadomosci/alejka2/izabela'
TEKSTY = {
 "I1": "Jestem Izabela. A teraz krok po kroku, co należy do Państwa — jak przepis. Najważniejsze słowa będą też na ekranie.",
 "I3": "Krok trzeci. We własnym zakresie zabezpieczacie Państwo nowy kabel przyłączeniowy u siebie na działce. Musi to zrobić wykwalifikowany elektryk. Odbieracie od niego oświadczenie — protokół elektryka o zabezpieczeniu przyłącza.",
 "I5": "Krok piąty. Z kartą danych technicznych, ka-de-te, podpisujecie Państwo umowę z Tauronem w Lublińcu, przy ulicy Klonowej jeden. To umowa na prąd — jak na telefon albo internet.",
 "I6": "Krok szósty. Gdy Tauron zamontuje licznik — taki jak w domu — zgłaszacie Państwo ten fakt Tomaszowi Maksysiowi. Wtedy nowe zasilanie zostanie przepięte do istniejącego zasilania działki, licznik sieci wewnętrznej zdemontowany, a jego ostatni stan spisany.",
 "I7": "I jeszcze trzy rzeczy. Za licznikiem kabel, szafka i instalacja są po Państwa stronie. Awaria sieci, złącza albo licznika — dzwońcie pod dziewięć dziewięć jeden. Pełna instrukcja jest na stronie rodwozniki kropka pe el, zakładka Dla działkowców.",
}
for n, t in TEKSTY.items():
    r = fal_client.subscribe('fal-ai/elevenlabs/tts/eleven-v3', arguments={'text': t, 'voice': 'Charlotte', 'language_code': 'pl', 'stability': 0.4, 'similarity_boost': 0.75, 'speed': 1.0, 'output_format': 'mp3_44100_128'})
    json.dump(r, open(f'{B}/_tts_{n}_resp.json', 'w'))
    a = r.get('audio'); url = (a.get('url') if isinstance(a, dict) else a) or r.get('audio_url') or r.get('url')
    urllib.request.urlretrieve(url, f'{B}/izabela_{n}.mp3'); print('OK', n, flush=True)
