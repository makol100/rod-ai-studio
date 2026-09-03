#!/bin/bash
set -e
D=/root/rod-ai-studio/data/awatar_tomasz
TMP=$D/_henio_tmp
cd "$D/ogl_sezon_v3"
for k in data17 data_final kw4_omni v2_kw3; do
  ffmpeg -v error -y -i "$k.wav" -ac 1 -ar 16000 "$TMP/${k}_n.wav" 2>/dev/null
  docker exec fabryka-api /app/venv/bin/python "$TMP/_t.py" "$TMP/${k}_n.wav" "$TMP/${k}.json" 2>&1 | tail -1
done
echo ALLDONE
