#!/bin/bash
set -e
D=/root/rod-ai-studio/data/awatar_tomasz
TMP=$D/_henio_tmp
mkdir -p "$TMP"
declare -A FILES=(
  [seg6B2]="$D/ogl_sezon_v3/omni_seg6_B2.mp4"
  [seg2A4]="$D/ogl_sezon_v3/omni_seg2_A4.mp4"
  [seg3C]="$D/ogl_sezon_v3/omni_seg3_C.mp4"
  [seg4v3_v2]="$D/ogl_sezon/omni_seg4_v3.mp4"
  [v4_full]="$D/ogl_sezon_v3/ogloszenie_sezon_v4.mp4"
  [seg6B]="$D/ogl_sezon_v3/omni_seg6_B.mp4"
)
for k in "${!FILES[@]}"; do
  f="${FILES[$k]}"
  wav="$TMP/$k.wav"
  out="$TMP/$k.json"
  ffmpeg -v error -y -i "$f" -vn -ac 1 -ar 16000 "$wav"
  docker exec fabryka-api /app/venv/bin/python "$TMP/_t.py" "$wav" "$out"
  echo "DONE $k -> $out"
done
echo ALLDONE
