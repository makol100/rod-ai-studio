import sys, json
sys.path.insert(0, '/app')
import fal_client
B = '/root/rod-ai-studio/data/zarty/10004'
M = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
u2 = fal_client.upload_file(f'{B}/kadr_02.jpg')
u3 = fal_client.upload_file(f'{B}/kadr_03.jpg')
# Retry po content_policy: to sama scena, jezyk jawnie komediowy (bez fear/terror/coercion).
gens = [
 ('f2', u2, u3,
  'Golden dusk orchard, lighthearted comedy sketch. The man in the red backwards cap '
  'below calls out in mock triumph in Polish, grinning, mouth wide open: '
  '"Mam cie! Gadaj, ktos ty?! No gadaj, pokim dobry!" while holding onto the branches. '
  'The skinny man in the grey knitted sweater sitting in the tree crown above is '
  'comically startled, frozen like a statue with huge wide eyes, keeping his mouth '
  'closed. Camera slowly pushes in from the wide shot to a close-up of the wide-eyed '
  'man in the crown. Continuous single take. No captions, no subtitles, no on-screen text.'),
 ('f3', u3, u3,
  'Close-up, golden dusk, lighthearted comedy sketch. The skinny man in the grey '
  'knitted sweater squeezed among apple tree branches, huge comically wide eyes, '
  'suddenly blurts out in Polish in a squeaky, funny, flustered voice: '
  '"To ja, Jozek! Niemowa ze wsi!" He keeps the same position holding the branch for '
  'the entire clip, only his face and mouth move. Natural handheld camera, continuous '
  'single take. No captions, no subtitles, no on-screen text.'),
]
for nr, fu, lu, prompt in gens:
    h = fal_client.submit(M, arguments={'prompt': prompt, 'first_frame_url': fu,
        'last_frame_url': lu, 'duration': '8s', 'aspect_ratio': 'auto', 'resolution': '1080p'})
    json.dump({'rid': h.request_id, 'model': M, 'koszt': 0.64},
              open(f'{B}/gen_state_{nr}.json', 'w'))
    print(nr, 'rid:', h.request_id[-10:])
