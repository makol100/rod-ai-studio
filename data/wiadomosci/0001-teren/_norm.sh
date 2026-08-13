#!/bin/bash
SRC=/root/rod-ai-studio/data/upload/0001-teren
WRK=/root/rod-ai-studio/data/wiadomosci/0001-teren/work
for f in "$SRC"/*.mp4; do
  B=$(basename "$f" .mp4)
  ffmpeg -y -v error -i "$f" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=30" -an -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p "$WRK/norm_${B}.mp4"
done
echo NORM-DONE > "$WRK/_norm_done.flag"
