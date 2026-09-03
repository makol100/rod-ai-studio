"""BATCH 10012: k01,k02,k03,k05 — veo3.1 lite FLF, 4x$0.64. Zgoda: D-0179."""
import sys, json
sys.path.insert(0, '/app')
import fal_client
B = '/root/rod-ai-studio/data/zarty/10012'
M = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
STYL = ('Bright sunny day in a lush Polish allotment garden, lighthearted comedy '
        'sketch, mockumentary style. ')
KONC = (' Natural handheld camera, continuous single take. '
        'No captions, no subtitles, no on-screen text.')
GENS = {
 'k01': STYL + ('The tall thin man in his mid-sixties with a grey mustache, reading '
   'glasses on a cord and a beige multi-pocket vest crouches beside a rickety old '
   'lawnmower, slowly wrapping grey electrical tape around a frayed, cracked old '
   'extension cord, trying to patch it up. He does not speak. Natural ambient garden '
   'sounds. Cinematic realistic footage, warm golden summer light. Vertical 9:16.') + KONC,
 'k02': STYL + ('The man with a long ponytail, full salt-and-pepper beard and a black '
   't-shirt steps into frame, a rugged yellow professional multimeter with no logo '
   'hanging from a strap around his neck, looks at the cord with grave seriousness, '
   'and says in Polish, in a low, gruff, determined middle-aged Polish male voice, '
   'speaking fluent native Polish with a natural Polish accent: "Janusz, badałeś ty '
   'kiedyś ciągłość przewodu ochronnego i rezystancję izolacji na tym kablu YKY?"') + KONC,
 'k03': STYL + ('The man with a long ponytail, full salt-and-pepper beard and a black '
   't-shirt, still with the rugged yellow professional multimeter hanging from his '
   'neck, points toward the mower with concern, and says in Polish, in a low, gruff, '
   'determined middle-aged Polish male voice, speaking fluent native Polish with a '
   'natural Polish accent: "Przecież tu ci zaraz różnicówkę wywali w kosmos."') + KONC,
 'k05': STYL + ('The tall thin man in his mid-sixties with a grey mustache, reading '
   'glasses on a cord and a beige multi-pocket vest confidently plugs the taped '
   'extension cord into an outdoor power socket mounted on a wooden post beside the '
   'rickety old lawnmower, full wide shot showing his whole body and arm. He does '
   'not speak. Natural ambient garden sounds. Cinematic realistic footage, warm '
   'golden summer light. Vertical 9:16.') + KONC,
}

def main():
    for nr, prompt in GENS.items():
        u = fal_client.upload_file(f'{B}/kadry/{nr}.jpg')
        h = fal_client.submit(M, arguments={'prompt': prompt, 'first_frame_url': u,
            'last_frame_url': u, 'duration': '8s', 'aspect_ratio': 'auto',
            'resolution': '1080p'})
        json.dump({'rid': h.request_id, 'model': M, 'koszt': 0.64},
                  open(f'{B}/gen_state_{nr}.json', 'w'))
        print(nr, 'SUBMIT rid:', h.request_id, flush=True)

if __name__ == '__main__':
    main()
