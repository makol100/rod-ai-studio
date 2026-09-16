import numpy as np, cv2, sys
from insightface.app import FaceAnalysis
app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"]); app.prepare(ctx_id=0, det_size=(640, 640))
def emb(p):
    im = cv2.imread(p); f = app.get(im)
    if not f: return None
    f = max(f, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1])); return f.normed_embedding
K = emb("/root/rod-ai-studio/assets/izabela/IZABELA_CANON_v2.png")
for n, p in [("stoi_v1 (08.09, przeszlo)", "/root/rod-ai-studio/data/awatar/relacja_alejka/izabela_stoi_v1.jpg"), ("stoi_v2 (nowy)", "/root/rod-ai-studio/data/wiadomosci/alejka2/izabela/izabela_stoi_v2.jpg")]:
    e = emb(p); print(n, "-> cos vs KANON:", None if e is None else round(float(np.dot(K, e)), 3))
