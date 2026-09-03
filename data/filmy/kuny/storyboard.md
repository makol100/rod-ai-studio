# STORYBOARD — KUNY, 16:9, DROGA A

STATUS: KROK 0. Nic z tego pliku nie zostalo wyslane do Gemini, fal.ai ani Veo.

Scenariusz ma **9 segmentow montazowych: INTRO + CZESC 1–8**. Okreslenie „8 czesci” oznacza osiem
czesci numerowanych; INTRO jest osobnym segmentem. Stare materialy monitoringu w
`data/filmy/kuny/gęste/`, `wyciete/`, `drzewo_*` i `noc_*` sa poza storyboardem.

## STORYBOARD — INTRO ORAZ CZESCI 1–4

| segment | forma | prompty z `prompty_obrazow.txt` | decyzja i ruch montazowy |
|---|---|---|---|
| INTRO | **Veo 1/4** + klamra Izabeli | 01 jako kadr startowy i klip; 02 jako statyczne dopowiedzenie w pelnym filmie | Prompt 01 ma jawna akcje („sneaking under the open hood”), wiec ruch buduje haczyk. Izabela otwiera i zamyka intro; B-roll zaslania jej usta w srodku wypowiedzi. |
| CZESC 1 — dlaczego auto | **Veo 2/4** + statyki | 03 jako klip; 04 i 05 jako statyki | Podejscie kuny do cieplego silnika pokazuje przyczyne, a nie tylko skutek. Matka z mlodymi i terytorialna agresja sa czytelniejsze jako kontrolowane kadry. |
| CZESC 2 — poznaj wroga | statyki | 06, 07, 08 | Porownanie plam, odchodow i tropow wymaga zatrzymania obrazu; ruch utrudnilby oglad szczegolow. Delikatny pan/zoom 3–5%. |
| CZESC 3 — mity | statyki | 09, 10, 11 | Kazdy mit dostaje osobny kadr i krotki znak „NIE DZIALA” dodany w montazu, nie w generatorze. Szybkie ciecia co 3–5 s. |
| CZESC 4 — co dziala w aucie | **Veo 3/4** + statyki | 12 jako klip; 13, 14, 15 jako statyki | Para i ruch lancy w myjni pokazuja kluczowy krok „najpierw usun zapach”. Plytki, mata i oplot musza zostac ostre i technicznie czytelne. |

## STORYBOARD — CZESCI 5–8

| segment | forma | prompty z `prompty_obrazow.txt` | decyzja i ruch montazowy |
|---|---|---|---|
| CZESC 5 — altana i dach | statyki | 16, 17, 18 | Instrukcja jest przestrzenna: siatka, test gazety i kolnierz na rynnie. Zblizenia montazowe na miejsce mocowania, bez generowanego ruchu dloni. |
| CZESC 6 — co wolno | statyki + lektor Janusz | 19, 20 i nowy 24 | Janusz czyta przepisy z notesika nad statycznym kadrem 24; telefon i otwarta, nieuzywana pulapka zostaja jako przebitki. Zakaz/trutka jako grafika montazowa, nie tekst wypalony przez model. |
| CZESC 7 — Skandynawia | **Veo 4/4** + statyki | 22 jako klip; 21 i nowy 25 jako statyki | Ruch termowizyjnego drona wnosi informacje, ktorej nie daje zwykly pan/zoom. Kadr 21 pokazuje zatwierdzona pulapke uderzeniowa bez inscenizowania zabicia; kadr 25 rozroznia skogsmård od stenmård, sposoby odlowu i zanety. |
| CZESC 8 — puenta | statyk | 23 | Flat-lay czterech zabezpieczen zamyka film jak lista kontrolna. Powolny najazd 4%, bez piatego klipu. |

Wybrane cztery klipy to INTRO/01, CZ1/03, CZ4/12 i CZ7/22. Kazdy ma ruch bedacy nosnikiem
tresci: skradanie, podejscie do ciepla, mycie para, przelot termowizyjny. Pozostale sceny korzystaja
z ruchu montazowego, bo wymagaja porownania lub odczytania detalu.

## NOWE PROMPTY PO D-0139 I D-0140

**24 — JANUSZ CZYTA PRAWO, CZESC 6, statyk 16:9.** Referencja tozsamosci:
`assets/zarty/karty/janusz_baza.jpg`; referencja pomocnicza sylwetki:
`assets/zarty/karty/janusz_arkusz.jpg`.

```text
Use the attached janusz_baza.jpg as the strict identity reference. Photorealistic cinematic
documentary frame, 16:9. In a modest Polish allotment association office in natural daylight,
a tall thin Polish man in his mid-sixties with the same face as the reference, a narrow grey
mustache, reading glasses hanging on a cord and a beige multi-pocket vest sits at a plain desk.
He holds his small violation notebook open at chest height and points to one line with a pencil,
dry officious expression, restrained mock-serious posture, direct eye contact, medium shot,
mouth clearly visible, hands anatomically correct. No other person, no animal, no trap in use.
No text, no captions, no subtitles, no logos, no watermark.
```

Glos Janusza: `a dry, officious elderly Polish male voice, speaking fluent native Polish with a natural Polish accent`.
Wybor produkcyjny: **statyczny obraz 24 + Eleven v3 + delikatny najazd 3%**. OmniHuman nie wnosi
nowej informacji do cytowania prawa, a dla calej kwestii wymagalby dwoch klipow 1080p, bo jedno
audio musi byc krotsze niz 30 s.

**25 — SZWEDZKIE SKOGSMARD I STENMARD, CZESC 7, statyk 16:9.** Do wygenerowania dopiero
z referencyjnymi zdjeciami obu modeli pulapek; sam tekst nie jest kotwica ich geometrii.

```text
Photorealistic educational documentary split-frame, 16:9, Swedish winter forest, non-graphic.
LEFT: native European pine marten, skogsmård, on its established woodland route; an inactive,
empty, approved Trapper mård 90 style instant-kill strike trap secured in its protective setup
high on a tree, about 1.5 metres above ground. Nearby, clean covered bait samples represent hare,
game bird or moose scraps with honey, a game-bird head, jam, fruit and gravad lax. RIGHT: stone
marten, stenmård, beside a parked car with intact cables; a 150 cm Fuchsfalle Fox 1 DeLuxe style
walk-through live trap displayed only as equipment of an official invasive-species control team,
with no private homeowner operating it and no bait shown because the programme bait is unknown.
No trapped animal, no blood, no activation, no suffering. Leave clear space for Polish labels
added later in editing. No generated text, no captions, no logos, no watermark.
```

Napisy `SKOGSMARD — KUNA LESNA`, `STENMARD — KUNA DOMOWA`, `TYLKO ZATWIERDZONA PULAPKA` i
`PROGRAM URZEDOWY — NIE DIY` dodaje montaz, nie generator. Zanety przypisujemy tylko do
skogsmård. Przy stenmård nie pokazujemy zanety, bo program nie podal jej w sprawdzonych zrodlach.
Oleju krewetkowego nie pokazujemy jako skutecznej zanety.

## PILOT INTRO — DOKLADNY UKLAD

Pilot ma trzy odcinki czasu i cztery media zrodlowe:

1. Izabela — poczatek jednego klipu OmniHuman: „Wygląda niewinnie, a potrafi w jedną noc narobić szkód.”
2. Veo 8 s — kuna wchodzi pod maske; glos poza kadrem: zdanie o przewodzie hamulcowym.
3. Izabela — koniec tego samego klipu OmniHuman: „Pokażę, co na kunę działa, za co szkoda pieniędzy i co wolno zgodnie z prawem.”

Obraz z promptu 01 jest jedynym nowym obrazem i zarazem pierwsza/ostatnia klatka Veo. Klip Izabeli
powstaje raz z polaczonych wypowiedzi otwierajacej i zamykajacej (okolo 9 s), po czym jest dzielony
lokalnie. Twarz nie jest generowana ponownie: wejsciem jest `izabela_16x9_v1.png`.

Tekst pilota jest skrotem INTRO do zatwierdzenia przez Tomasza; nie nadpisuje scenariusza.
Polskie znaki sa normalizacja dla TTS, bez zmiany znaczenia.

## KOSZT PILOTA PO OSOBNYM OK TOMASZA

| pozycja | model i jednostka | koszt USD |
|---|---|---:|
| 1 obraz 1K | `gemini-3.1-flash-image`, 1K | 0.067 |
| glos Charlotte | Eleven v3: 55 + 106 + 78 = 239 znakow | 0.0239 |
| 1 klip Veo | Lite FLF, 1080p, 8 s, `generate_audio=false`: 8 × 0.05 | 0.4000 |
| Izabela | OmniHuman v1.5: maks. 10 s × 0.16 | **maks. 1.6000** |
| PIL, ffmpeg, bramki i montaz | lokalnie | 0.0000 |

**Twardy limit pilota: 2.0909 USD.** Dokladnego kosztu OmniHuman przed powstaniem TTS **NIE WIEM**,
bo fal rozlicza rzeczywista dlugosc audio. Przed submitem skrypt mierzy audio i zatrzymuje sie przy
czasie ponad 10,000 s. Przy kanonicznym tempie 14,8 znaku/s klamra 134 znakow powinna trwac okolo
9,05 s, czyli OmniHuman okolo 1,45 USD; to szacunek, nie pomiar.

Ceny sprawdzone w oficjalnych cennikach przed zapisaniem planu:
[Google Gemini](https://ai.google.dev/gemini-api/docs/pricing),
[fal Veo Lite FLF](https://fal.ai/models/fal-ai/veo3.1/lite/first-last-frame-to-video),
[fal Eleven v3](https://fal.ai/models/fal-ai/elevenlabs/tts/eleven-v3),
[fal OmniHuman v1.5](https://fal.ai/models/fal-ai/bytedance/omnihuman/v1.5).

## KOSZT KOREKTY D-0139 I D-0140

Po korekcie storyboard ma **25 obrazow zamiast 23: doszly 2** (24 Janusz, 25 Szwecja).
Scenariusz ma **6088 znakow mowionych zamiast 5466: doszly 622 znaki**. Sama czesc Janusza ma
656 znakow mowionych. Liczenie obejmuje tekst pomiedzy cudzyslowami; didaskalia nie sa lektorem.

| wariant czesci 6 | rachunek | koszt USD |
|---|---|---:|
| **wybrany: statyk Janusza + Eleven v3** | obraz 1K 0.067 + 656 × 0.10/1000 | **0.1326 USD** |
| alternatywa: ten sam obraz + Eleven v3 + OmniHuman | 0.1326 + (656/14.8) × 0.16 | **ok. 7.2245 USD** |

Koszt OmniHuman jest szacunkiem: tempo 14,8 znaku/s zmierzono dla Charlotte, nie dla wybranego
glosu Janusza. Daje to okolo 44,32 s audio, wiec przy limicie krotszym niz 30 s na klip 1080p
potrzebne bylyby 2 klipy. Dokladnego kosztu przed wygenerowaniem i zmierzeniem audio **NIE WIEM**.
Jawne stawki w repo: obraz `gemini-3.1-flash-image` 1K = 0.067 USD, Eleven v3 = 0.10 USD/1000
znakow, OmniHuman w tym planie = 0.16 USD/s.

Przy wybranym statyku przyrost kosztu calego filmu wzgledem poprzedniego storyboardu to
**0.1962 USD**: 2 obrazy × 0.067 + 622 dodatkowe znaki × 0.10/1000. Wariant OmniHuman
podnioslby ten przyrost do okolo **7.2881 USD**. To kosztorys, nie wydane srodki.

**Pilot INTRO pozostaje bez zmian: 1 obraz, 239 znakow, 1 Veo i maks. 10 s Izabeli; jego twardy
limit nadal wynosi 2.0909 USD.** Janusz i rozszerzona Szwecja sa poza pilotem.

## BRAMKI PRZED KAZDYM SUBMITEM

1. Tomasz wydaje osobne „OK PILOT INTRO”; bez tego nie wolno dopisac `--zaplac`.
2. `tools/zenek_obraz.py` najpierw idzie bez `--zaplac`; wynik musi pokazac `DRY-RUN (NIC NIE WYSLANO)`, model, prompt, 16:9, 1K i 0.067 USD.
3. Przed kazdym wywolaniem fal: odczyt `billing/user_balance`; saldo po odjeciu rezerwy 2.0239 USD nie moze byc ujemne, a suma pilota nie moze przekroczyc 2.0909 USD.
4. Przed Veo: kadr istnieje, ma proporcje 16:9 i mniej niz 8 MB; prompt zawiera `No captions`, `generate_audio=false`, 1080p i 8 s.
5. Przed OmniHuman: kadr Izabeli ma 1920×1080, audio klamry ma maks. 10,000 s, `turbo_mode=false`; po generacji wynik przechodzi kontrole ust i tozsamosci.

`tools/preflight.py` i `tools/kanarek.py` nie sa bramka przed submitem tego pilota: pierwszy wymusza
9:16, drugi czyta wylacznie `data/zarty/<odcinek>` i wymusza 1080×1920. Uzycie ich bez adaptera
daloby czerwony wynik dla poprawnego filmu 16:9. Kanarkiem jest jeden klip INTRO; po pobraniu
sprawdza go bezposrednio `tools/straznik.py`.

## KOMENDY — PRZYGOTOWANIE I OBRAZ

Te trzy komendy sa bezplatne; ostatnia wyswietla request i niczego nie wysyla:

```bash
mkdir -p data/filmy/kuny/pilot
python3 tools/zenek_obraz.py --lista
python3 tools/zenek_obraz.py --model gemini-3.1-flash-image --aspect 16:9 --resolution 1K --output data/filmy/kuny/pilot/intro_kadr_01.png --prompt 'Stone marten at night sneaking under the open hood of a parked car, dramatic low light, glowing eyes, cinematic, photorealistic, 16:9, no text, no captions, no watermarks'
```

STOP. Dopiero po „OK PILOT INTRO” Tomasza obraz generuje ta sama komenda z dopisana flaga:

```bash
python3 tools/zenek_obraz.py --model gemini-3.1-flash-image --aspect 16:9 --resolution 1K --output data/filmy/kuny/pilot/intro_kadr_01.png --prompt 'Stone marten at night sneaking under the open hood of a parked car, dramatic low light, glowing eyes, cinematic, photorealistic, 16:9, no text, no captions, no watermarks' --zaplac
```

Kontrola obrazu po pobraniu:

```bash
python3 - <<'PY'
from pathlib import Path
from PIL import Image
p = Path('data/filmy/kuny/pilot/intro_kadr_01.png')
im = Image.open(p)
w, h = im.size
assert p.stat().st_size < 8 * 1024 * 1024
assert abs(w / h - 16 / 9) < 0.02, (w, h)
assert min(w, h) >= 700, (w, h)
print({'PASS': True, 'w': w, 'h': h, 'bytes': p.stat().st_size})
PY
```

## KOMENDY — GLOS CHARLOTTE

Najpierw bezplatna bramka salda:

```bash
curl -fsS -H "Authorization: Key $FAL_KEY" https://rest.fal.ai/billing/user_balance
```

STOP. Nastepna komenda kosztuje 0.0239 USD i wolno ja wykonac tylko po „OK PILOT INTRO”:

```bash
PYTHONPATH=/root/rod-ai-studio/apps/api/venv/lib/python3.14/site-packages python3 - --zaplac <<'PY'
import json, sys, urllib.request
from pathlib import Path
import fal_client

assert sys.argv[1:] == ['--zaplac']
folder = Path('data/filmy/kuny/pilot')
teksty = {
    'intro_open.mp3': 'Wygląda niewinnie, a potrafi w jedną noc narobić szkód.',
    'intro_broll.mp3': 'Zdarza się, że kierowca rusza rano i musi hamować ręcznym, bo kuna przegryzła mu w nocy przewód hamulcowy.',
    'intro_close.mp3': 'Pokażę, co na kunę działa, za co szkoda pieniędzy i co wolno zgodnie z prawem.',
}
assert sum(map(len, teksty.values())) == 239
for nazwa, tekst in teksty.items():
    wynik = fal_client.subscribe('fal-ai/elevenlabs/tts/eleven-v3', arguments={
        'text': tekst, 'voice': 'Charlotte', 'language_code': 'pl',
        'stability': 0.4, 'similarity_boost': 0.75, 'speed': 1.0,
        'output_format': 'mp3_44100_128'})
    url = wynik['audio']['url']
    urllib.request.urlretrieve(url, folder / nazwa)
    (folder / (nazwa + '.json')).write_text(json.dumps(wynik, ensure_ascii=False, indent=2), encoding='utf-8')
PY
ffmpeg -y -v error -i data/filmy/kuny/pilot/intro_open.mp3 -i data/filmy/kuny/pilot/intro_close.mp3 -filter_complex '[0:a][1:a]concat=n=2:v=0:a=1[a]' -map '[a]' -ar 48000 -ac 2 data/filmy/kuny/pilot/intro_klamra.wav
```

## KOMENDY — VEO KANAREK

STOP. Komenda ponizej wysyla platny submit 0.40 USD; tylko po zielonych bramkach i „OK PILOT INTRO”:

```bash
PYTHONPATH=/root/rod-ai-studio/apps/api/venv/lib/python3.14/site-packages python3 - --zaplac <<'PY'
import json, sys, time, urllib.request
from pathlib import Path
import fal_client

assert sys.argv[1:] == ['--zaplac']
folder = Path('data/filmy/kuny/pilot')
kadr = folder / 'intro_kadr_01.png'
prompt = ('A stone marten cautiously sneaks deeper under the open hood of a parked car at night, '
          'sniffs the warm engine bay and steps between cables. Slow controlled dolly-in, realistic '
          'animal motion, continuous single take, cinematic low light. Silent visual B-roll. '
          'No captions, no subtitles, no on-screen text, no watermark.')
url = fal_client.upload_file(str(kadr))
model = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
args = {'prompt': prompt, 'first_frame_url': url, 'last_frame_url': url,
        'duration': '8s', 'aspect_ratio': '16:9', 'resolution': '1080p',
        'generate_audio': False, 'auto_fix': False, 'safety_tolerance': '4'}
handle = fal_client.submit(model, arguments=args)
(folder / 'intro_veo_state.json').write_text(json.dumps({'rid': handle.request_id, 'model': model, 'koszt_max': 0.40}), encoding='utf-8')
for _ in range(40):
    if type(fal_client.status(model, handle.request_id)).__name__ == 'Completed':
        wynik = fal_client.result(model, handle.request_id)
        urllib.request.urlretrieve(wynik['video']['url'], folder / 'intro_veo.mp4')
        break
    time.sleep(10)
else:
    raise SystemExit('STOP: timeout; request_id zapisany, NIE wysylac drugiego submitu')
PY
python3 tools/straznik.py data/filmy/kuny/pilot/intro_veo.mp4 --exp-w 1920 --exp-h 1080 --freeze-ok --json
```

FAIL straznika = STOP. Nie ma drugiego Veo bez nowej decyzji Tomasza.

## KOMENDY — OZYWIENIE IZABELI

Bezkosztowa bramka dlugosci:

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 data/filmy/kuny/pilot/intro_klamra.wav
```

STOP. Nastepna komenda kosztuje `czas_audio × 0.16 USD`, maksymalnie 1.60 USD:

```bash
PYTHONPATH=/root/rod-ai-studio/apps/api/venv/lib/python3.14/site-packages python3 - --zaplac <<'PY'
import json, subprocess, sys, time, urllib.request
from pathlib import Path
import fal_client

assert sys.argv[1:] == ['--zaplac']
folder = Path('data/filmy/kuny/pilot')
audio = folder / 'intro_klamra.wav'
czas = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(audio)], text=True))
assert 0 < czas <= 10.0, czas
model = 'fal-ai/bytedance/omnihuman/v1.5'
iu = fal_client.upload_file('data/filmy/kuny/izabela_16x9_v1.png')
au = fal_client.upload_file(str(audio))
args = {'image_url': iu, 'audio_url': au,
        'prompt': 'Calm factual presentation, direct eye contact, natural blinking, subtle head and shoulder movement, restrained serious expression, locked camera.',
        'resolution': '1080p', 'turbo_mode': False}
handle = fal_client.submit(model, arguments=args)
(folder / 'intro_izabela_state.json').write_text(json.dumps({'rid': handle.request_id, 'model': model, 'czas_audio': czas, 'koszt_max': czas * 0.16}), encoding='utf-8')
for _ in range(60):
    if type(fal_client.status(model, handle.request_id)).__name__ == 'Completed':
        wynik = fal_client.result(model, handle.request_id)
        urllib.request.urlretrieve(wynik['video']['url'], folder / 'intro_izabela.mp4')
        break
    time.sleep(10)
else:
    raise SystemExit('STOP: timeout; request_id zapisany, NIE wysylac drugiego submitu')
PY
```

Po pobraniu: kontrola ust/tozsamosci, potem lokalny podzial w punkcie rownym dlugosci `intro_open.mp3`:

```bash
python3 tools/straznik.py data/filmy/kuny/pilot/intro_izabela.mp4 --kwestia 'Wygląda niewinnie, a potrafi w jedną noc narobić szkód. Pokażę, co na kunę działa, za co szkoda pieniędzy i co wolno zgodnie z prawem.' --wzorzec IZABELA=assets/izabela/IZABELA_ODKLEJONA_v2.png --exp-w 1920 --exp-h 1080 --tekst-dozwolony --freeze-ok --json
D_OPEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 data/filmy/kuny/pilot/intro_open.mp3)
ffmpeg -y -v error -i data/filmy/kuny/pilot/intro_izabela.mp4 -t "$D_OPEN" -an -c:v libx264 -crf 18 -preset veryfast data/filmy/kuny/pilot/intro_izabela_open.mp4
ffmpeg -y -v error -ss "$D_OPEN" -i data/filmy/kuny/pilot/intro_izabela.mp4 -an -c:v libx264 -crf 18 -preset veryfast data/filmy/kuny/pilot/intro_izabela_close.mp4
```

## KOMENDA MONTAZU PILOTA

Manifest po powstaniu mediow:

```json
{
  "sceny": [
    {"media": "intro_izabela_open.mp4", "audio": "intro_open.mp3"},
    {"media": "intro_veo.mp4", "audio": "intro_broll.mp3"},
    {"media": "intro_izabela_close.mp4", "audio": "intro_close.mp3"}
  ]
}
```

Zapisac go jako `data/filmy/kuny/pilot/manifest.json`, a potem:

```bash
python3 tools/film_rod/buduj_film.py data/filmy/kuny/pilot/manifest.json --wynik data/filmy/kuny/pilot/intro_pilot_v1.mp4
python3 tools/straznik.py data/filmy/kuny/pilot/intro_pilot_v1.mp4 --exp-w 1920 --exp-h 1080 --final 2 --freeze-ok --tekst-dozwolony --json
```

Eksport jest dozwolony tylko przy 1920×1080, 24 fps, H.264, AAC 48 kHz stereo,
`|duration_video-duration_audio| < 0.05 s` i `faststart=true`. Publikacja nie jest czescia pilota.

— Zenek
