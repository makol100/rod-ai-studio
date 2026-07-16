import sys, json
sys.path.insert(0, '/app')
import fal_client
B = '/root/rod-ai-studio/data/zarty/10004'
M = 'fal-ai/veo3.1/lite/first-last-frame-to-video'
u1a = fal_client.upload_file(f'{B}/kadr_01.jpg')
u1b = fal_client.upload_file(f'{B}/kadr_01_koniec.jpg')
u2 = fal_client.upload_file(f'{B}/kadr_02.jpg')
gens = [
 ('01', u1a, u1b, 'Tomasz walks forward on the garden path at dusk pointing his flashlight at the apple tree ahead, annoyed then determined, and says in Polish: "Znowu mi ktos jablka podzera! Ide i zlapie go za jajca!" Continuous single take, natural handheld camera.'),
 ('02a', u2, u2, 'Tomasz says in Polish with a loud angry determined voice: "Ktos ty?! Pytam, ktos ty?!" He holds the exact pose and grip from the frame for the entire clip, right hand locked deep in the foliage, speaking through clenched teeth, without gesturing, left arm still. The branches shake. Continuous single take, natural handheld camera.'),
 ('02b', u2, u2, 'He holds the exact pose and grip from the frame for the entire clip without gesturing, listening intently. From inside the tree crown a high-pitched squeaky voice calls in Polish: "Jozek......" Tomasz, still gripping, answers through clenched teeth in Polish: "Jaki Jozek?!" Then an unseen older man answers calmly from off-screen in Polish: "Jozek... ten niemowa!" The branches tremble. Continuous single take, natural handheld camera.'),
]
for nr, fu, lu, prompt in gens:
    h = fal_client.submit(M, arguments={'prompt': prompt, 'first_frame_url': fu,
        'last_frame_url': lu, 'duration': '8s', 'aspect_ratio': 'auto', 'resolution': '1080p'})
    json.dump({'rid': h.request_id, 'model': M, 'koszt': 0.64},
              open(f'{B}/gen_state_{nr}.json', 'w'))
    print(nr, 'rid:', h.request_id[-10:])
