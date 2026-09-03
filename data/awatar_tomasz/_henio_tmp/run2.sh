#!/bin/bash
set -e
D=/root/rod-ai-studio/data/awatar_tomasz
TMP=$D/_henio_tmp
declare -A FILES=(
  [seg4v3_v2]="$D/ogl_sezon/omni_seg4_v3.mp4"
  [seg6B]="$D/ogl_sezon_v3/omni_seg6_B.mp4"
  [seg2v3_v2]="$D/ogl_sezon/omni_seg2_v3.mp4"
)
for k in "${!FILES[@]}"; do
  f="${FILES[$k]}"
  wav="$TMP/$k.wav"
  out="$TMP/$k.json"
  ffmpeg -v error -y -i "$f" -vn -ac 1 -ar 16000 "$wav"
  docker exec fabryka-api /app/venv/bin/python "$TMP/_t2.py" "$wav" "$out"
done
echo ALLDONE
