"""Batch 10009: 8 klipow (k01 niemy + 7 dialogowych). Preflight kazdego,
submit WSZYSTKICH tylko gdy komplet ZIELONY. Kwestie VERBATIM z KANON.md
(jedyna transpozycja: wewnetrzne cudzyslowy "Czarny Ksiaze" -> typograficzne,
zeby nie zlamac kontroli jednej pary cudzyslowow dialogowych)."""
import sys, json, subprocess
sys.path.insert(0, '/app')
import fal_client

B = '/root/rod-ai-studio/data/zarty/10009'
M = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
PF = '/root/rod-ai-studio/tools/preflight.py'

SW = "Golden hour, low warm sun just before dusk in a lush Polish allotment garden, lighthearted comedy sketch, mockumentary style. "
TOM = "The man with a long ponytail, full salt-and-pepper beard, wearing a dark casual jacket over a black t-shirt, "
JAN = "The tall thin man in his mid-sixties with a grey mustache, wearing dark sunglasses and a grey hoodie with the hood pulled over his head like an amateur gangster, "
GT = "in a low, gruff, determined middle-aged Polish male voice, speaking fluent native Polish with a natural Polish accent"
GJ = "in a dry, officious elderly Polish male voice, speaking fluent native Polish with a natural Polish accent"
KON = " Natural handheld camera, continuous single take. No captions, no subtitles, no on-screen text."

K = {
 "k01": dict(mowca="BOHATER", niemy=True, kwestia="", prompt=SW + TOM +
   "stands by a low wooden garden fence glancing around nervously left and right. " + JAN +
   "approaches him slowly along the fence like in a gangster movie. Neither of them speaks. "
   "Quiet evening garden ambience, distant birds." + KON),
 "k03a": dict(mowca="BOHATER", kwestia='Mam. Odmiana „Czarny Książę". Słodkie jak miód, odporne na zarazę ziemniaczaną.',
   prompt=SW + TOM + "secretly pulls a small flower pot with a young tomato seedling from inside his jacket, hunched and conspiratorial, and says in Polish in a hushed conspiratorial whisper, " + GT +
   ': "Mam. Odmiana „Czarny Książę". Słodkie jak miód, odporne na zarazę ziemniaczaną." He keeps the hunched secretive pose for the entire clip.' + KON),
 "k03b": dict(mowca="BOHATER", kwestia="Ale co masz dla mnie w zamian? Miała być czysta, naturalna waluta.",
   prompt=SW + TOM + "holds the small flower pot with a young tomato seedling at chest height, gives a questioning bargaining look, and says in Polish in a hushed conspiratorial whisper, " + GT +
   ': "Ale co masz dla mnie w zamian? Miała być czysta, naturalna waluta." He keeps the pose for the entire clip.' + KON),
 "k04a": dict(mowca="JANUSZ", kwestia="Prosto od rolnika spod Grójca. Trzyletni, przekompostowany obornik koński.",
   prompt=SW + JAN + "proudly reveals a small plastic bucket with a lid from behind his back presenting it like contraband, and says in Polish, " + GJ +
   ': "Prosto od rolnika spod Grójca. Trzyletni, przekompostowany obornik koński."' + KON),
 "k04b": dict(mowca="JANUSZ", kwestia="Żadnej chemii, sam czysty azot. Twoje ogórki po tym wystrzelą w kosmos.",
   prompt=SW + JAN + "slightly lifts the lid of the small bucket, grimaces with comic delight at the smell, and says in Polish, " + GJ +
   ': "Żadnej chemii, sam czysty azot. Twoje ogórki po tym wystrzelą w kosmos."' + KON),
 "k04c": dict(mowca="JANUSZ", kwestia="Bierz, zanim prezes zauważy, bo oficjalnie w tym tygodniu jest zakaz wwożenia gabarytów na alejki.",
   prompt=SW + JAN + "leans in urgently holding the closed bucket with both hands, glancing over his shoulder, and says in Polish, " + GJ +
   ': "Bierz, zanim prezes zauważy, bo oficjalnie w tym tygodniu jest zakaz wwożenia gabarytów na alejki."' + KON),
 "k05": dict(mowca="BOHATER", kwestia="Dobry towar. Umowa stoi. Tylko nikomu ani słowa, zwłaszcza tej sąsiadce z naprzeciwka.",
   prompt=SW + "Two men at the fence mid-exchange. " + TOM + "takes the small lidded bucket with one hand while handing over the flower pot with the tomato seedling, and says in Polish in a hushed conspiratorial whisper, " + GT +
   ': "Dobry towar. Umowa stoi. Tylko nikomu ani słowa, zwłaszcza tej sąsiadce z naprzeciwka." ' + JAN +
   "receives the pot silently, seen slightly from the side, and does not speak." + KON),
 "k06": dict(mowca="JANUSZ", kwestia="Grażyna? Ona sypie sztuczny nawóz z marketu, amatorka... Nie zna życia. Do następnego, młody.",
   prompt=SW + JAN + "tucks the small flower pot with the tomato seedling under his hoodie with a proud smirk, half turned on his heel, and says in Polish, " + GJ +
   ': "Grażyna? Ona sypie sztuczny nawóz z marketu, amatorka... Nie zna życia. Do następnego, młody." At the end he starts turning away as if to vanish behind the bushes.' + KON),
}

def preflight(nazwa, d):
    kadr = f"{B}/kadry/{nazwa}.jpg"
    cmd = ['/app/venv/bin/python', PF, '--odcinek', '10009', '--mowca', d['mowca'],
           '--kadr-start', kadr, '--kadr-koniec', kadr, '--prompt', d['prompt'],
           '--koszt', '0.64', '--limit', '12.0']
    if d.get('niemy'):
        cmd += ['--bez-dialogu']
    else:
        cmd += ['--kwestia', d['kwestia']]
    r = subprocess.run(cmd, capture_output=True, text=True)
    ok = 'ZIELONY' in r.stdout
    print(f"[pf] {nazwa}: {'ZIELONY' if ok else 'CZERWONY'}", flush=True)
    if not ok:
        for l in r.stdout.splitlines():
            if l.startswith(('FAIL', 'FLAG')):
                print('   ', l, flush=True)
    return ok

if __name__ == '__main__':
    wyniki = {n: preflight(n, d) for n, d in K.items()}
    if not all(wyniki.values()):
        print("[batch] STOP — nie wszystkie zielone, ZERO submitow", flush=True)
        sys.exit(1)
    
    print("[batch] komplet ZIELONY — submit 8 klipow", flush=True)
    for n, d in K.items():
        u = fal_client.upload_file(f"{B}/kadry/{n}.jpg")
        h = fal_client.submit(M, arguments={'prompt': d['prompt'], 'first_frame_url': u,
            'last_frame_url': u, 'duration': '8s', 'aspect_ratio': 'auto', 'resolution': '1080p'})
        json.dump({'rid': h.request_id, 'model': M, 'koszt': 0.64},
                  open(f"{B}/gen_state_{n}.json", 'w'))
        print(f"[batch] {n} rid: ...{h.request_id[-10:]}", flush=True)
    print("[batch] KONIEC SUBMITOW", flush=True)
