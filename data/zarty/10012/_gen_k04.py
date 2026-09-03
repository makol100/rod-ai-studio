"""KANAREK 10012 k04 (puenta Janusza) — veo3.1 lite FLF, $0.64. Zgoda: D-0177."""
import sys, json
sys.path.insert(0, '/app')
import fal_client
B = '/root/rod-ai-studio/data/zarty/10012'
M = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
PROMPT = ('Bright sunny day in a lush Polish allotment garden, lighthearted comedy '
 'sketch, mockumentary style. The tall thin man in his mid-sixties with a grey '
 'mustache, reading glasses on a cord and a beige multi-pocket vest stares at the '
 'other man as if he were speaking a foreign language, slowly turns his head and '
 'spits over his shoulder, then shrugs dismissively, and says in Polish, in a dry, '
 'officious elderly Polish male voice, speaking fluent native Polish with a natural '
 'Polish accent: "Panie, to ma prąd przewodzić, a nie mieć jakąś... rezystancję. '
 'Od 30 lat działa!" Natural handheld camera, continuous single take. '
 'No captions, no subtitles, no on-screen text.')

def main():
    u = fal_client.upload_file(f'{B}/kadry/k04.jpg')
    h = fal_client.submit(M, arguments={'prompt': PROMPT, 'first_frame_url': u,
        'last_frame_url': u, 'duration': '8s', 'aspect_ratio': 'auto', 'resolution': '1080p'})
    json.dump({'rid': h.request_id, 'model': M, 'koszt': 0.64},
              open(f'{B}/gen_state_k04.json', 'w'))
    print('k04 SUBMIT rid:', h.request_id)

if __name__ == '__main__':
    main()
