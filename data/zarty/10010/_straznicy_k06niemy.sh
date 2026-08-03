#!/bin/bash
D=/root/rod-ai-studio/data/zarty/10010
run() { docker exec -w /app -e PYTHONPATH=/app fabryka-api /app/venv/bin/python "$@"; }
echo "===== 1. KANAREK ====="; run $D/_straz_k06niemy.py
echo "===== 2. CISZA (whisper medium) ====="; run $D/_cisza_k06.py; C=$?
echo "===== 3. USTA ====="; run $D/_pomiar_ust_k06niemy.py 2>&1 | tail -6
echo "===== 4. MAD ŚRODKA vs KADR ====="
ffmpeg -y -loglevel error -ss 4 -i $D/klip_k06_niemy.mp4 -frames:v 1 -vf scale=768:-1 /root/rod-ai-studio/data/n150files/10010_srodek_k06niemy.jpg
docker exec -i fabryka-api /app/venv/bin/python - << 'PYEOF'
from PIL import Image
import numpy as np
a=np.asarray(Image.open("/root/rod-ai-studio/data/n150files/10010_srodek_k06niemy.jpg").convert("L").resize((256,455)),dtype=float)
b=np.asarray(Image.open("/root/rod-ai-studio/data/zarty/10010/kadry/k06.jpg").convert("L").resize((256,455)),dtype=float)
m=abs(a-b).mean(); print(f"MAD = {m:.1f} (wzorzec zdrowia 15.4, chore >>20)")
PYEOF
echo "WERDYKT: sekcje wyżej — cisza exit=$C (0=PASS)"
