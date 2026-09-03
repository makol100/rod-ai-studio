import cv2
import insightface
from insightface.app import FaceAnalysis

app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

def get_face(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return None, 0
    faces = app.get(img)
    if len(faces) == 0:
        return None, 0
    return faces[0].embedding, len(faces)

ref_janusz, _ = get_face('/root/rod-ai-studio/assets/zarty/karty/janusz_baza.jpg')
ref_bohater, _ = get_face('/root/rod-ai-studio/assets/zarty/karty/bohater_baza.jpg')

frames = [
    ('/root/rod-ai-studio/data/zarty/10012/kadry/k01.jpg', 'JANUSZ', ref_janusz),
    ('/root/rod-ai-studio/data/zarty/10012/kadry/k02.jpg', 'BOHATER', ref_bohater),
    ('/root/rod-ai-studio/data/zarty/10012/kadry/k03.jpg', 'BOHATER', ref_bohater),
    ('/root/rod-ai-studio/data/zarty/10012/kadry/k04.jpg', 'JANUSZ', ref_janusz),
    ('/root/rod-ai-studio/data/zarty/10012/kadry/k05.jpg', 'JANUSZ', ref_janusz),
]

import numpy as np
for frame_path, postac, ref_emb in frames:
    emb, count = get_face(frame_path)
    if count == 0:
        print(f"{frame_path}: {postac} - Twarze: {count}")
    else:
        sim = np.dot(ref_emb, emb) / (np.linalg.norm(ref_emb) * np.linalg.norm(emb))
        print(f"{frame_path}: {postac} - Twarze: {count} - Sim: {sim:.4f}")

