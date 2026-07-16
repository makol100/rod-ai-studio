import sys, json
sys.path.insert(0, '/app')
import fal_client
B = '/root/rod-ai-studio/data/zarty/10004'
M = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
u1a = fal_client.upload_file(f'{B}/kadr_01.jpg')
u1b = fal_client.upload_file(f'{B}/kadr_01_koniec.jpg')
u2 = fal_client.upload_file(f'{B}/kadr_02.jpg')
u3 = fal_client.upload_file(f'{B}/kadr_03.jpg')
# DROGA 2.0: jeden mowca na klip, identyfikator wizualny mowcy, no captions.
gens = [
 ('f1', u1a, u1b,
  'Night orchard alley. The heavyset man in the red backwards cap and dark floral '
  'Hawaiian shirt sneaks forward with a flashlight, its beam aimed up at a dark '
  'silhouette swaying in the apple tree crown ahead. He says angrily in Polish: '
  '"Znowu mi ktos jablka podzera!" then adds, determined: "Ide i zlapie go za jajca!" '
  'Slow tense forward walk, natural handheld camera, continuous single take. '
  'No captions, no subtitles, no on-screen text.'),
 ('f2', u2, u3,
  'Golden dusk orchard. The man in the red backwards cap below shouts triumphantly '
  'in Polish, mouth wide open: "Mam cie! Gadaj, ktos ty?! No gadaj, pokim dobry!" '
  'while gripping into the branches. The skinny man in the grey knitted sweater '
  'frozen in the tree crown above him stays completely silent and rigid, terrified '
  'bulging eyes staring down, clutching a branch, his mouth shut. Camera slowly '
  'pushes in from the wide shot to a close-up of the frightened man in the crown. '
  'Continuous single take. No captions, no subtitles, no on-screen text.'),
 ('f3', u3, u3,
  'Close-up, golden dusk. The skinny man in the grey knitted sweater squeezed among '
  'apple tree branches, huge terrified bulging eyes, suddenly bursts out in Polish, '
  'voice cracking and shaking with fear: "To ja, Jozek! Niemowa ze wsi!" He holds '
  'the exact position clutching the branch for the entire clip, only his face and '
  'mouth move, no gesturing. Natural handheld camera, continuous single take. '
  'No captions, no subtitles, no on-screen text.'),
]
for nr, fu, lu, prompt in gens:
    h = fal_client.submit(M, arguments={'prompt': prompt, 'first_frame_url': fu,
        'last_frame_url': lu, 'duration': '8s', 'aspect_ratio': 'auto', 'resolution': '1080p'})
    json.dump({'rid': h.request_id, 'model': M, 'koszt': 0.64},
              open(f'{B}/gen_state_{nr}.json', 'w'))
    print(nr, 'rid:', h.request_id[-10:])
