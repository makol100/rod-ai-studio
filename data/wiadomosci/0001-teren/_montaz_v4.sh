#!/bin/bash
# MONTAZ v4 — jak v3, ale FINAL (slot 39-45) wraca do STAREGO frag_p6 (autorotate, pion natywny prosty).
# Diagnoza 28.07 wieczor: operator @56s zrodla 093926 trzymal telefon PIONOWO (powrot z poziomu ~50-62s wg vidstab),
# wiec stare ciecie autorotate bylo prawidlowe, a blur-fill p6_v2 wprowadzil lezaca tresc.
set -e
W=/root/rod-ai-studio/data/wiadomosci/0001-teren/work
F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
ffmpeg -y -v error \
 -noautorotate -i "$W/stanislaw_0001_raw.mp4" \
 -noautorotate -i "$W/frag_p1_v2b.mp4" -noautorotate -i "$W/frag_p2_v2b.mp4" \
 -noautorotate -i "$W/frag_p3_v3.mp4" -noautorotate -i "$W/frag_p4_v3.mp4" \
 -noautorotate -i "$W/frag_p5_v2.mp4" -noautorotate -i "$W/frag_p6.mp4" \
 -noautorotate -i "$W/../WD_0001_teren_master.mp4" \
 -filter_complex "\
[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=30[base];\
[1:v]setpts=PTS-STARTPTS+9/TB[v1];[2:v]setpts=PTS-STARTPTS+16/TB[v2];\
[3:v]setpts=PTS-STARTPTS+21/TB[v3];[4:v]setpts=PTS-STARTPTS+27/TB[v4];\
[5:v]setpts=PTS-STARTPTS+32/TB[v5];[6:v]setpts=PTS-STARTPTS+39/TB[v6];\
[base][v1]overlay=eof_action=pass:enable='between(t,9,16)'[o1];\
[o1][v2]overlay=eof_action=pass:enable='between(t,16,21)'[o2];\
[o2][v3]overlay=eof_action=pass:enable='between(t,21,27)'[o3];\
[o3][v4]overlay=eof_action=pass:enable='between(t,27,32)'[o4];\
[o4][v5]overlay=eof_action=pass:enable='between(t,32,39)'[o5];\
[o5][v6]overlay=eof_action=pass:enable='between(t,39,45)'[o6];\
[o6]drawtext=fontfile=$F:text='WIADOMOŚCI DZIAŁKOWE':fontsize=72:fontcolor=white:borderw=6:bordercolor=black:x=(w-text_w)/2:y=150:enable='lt(t,3.2)',\
drawtext=fontfile=$F:text='ROD im. Józefa Lompy w Woźnikach':fontsize=44:fontcolor=white:borderw=5:bordercolor=black:x=(w-text_w)/2:y=250:enable='lt(t,3.2)'[vout]" \
 -map "[vout]" -map 7:a -c:a copy \
 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
 -movflags +faststart \
 "$W/../WD_0001_teren_master_v4.mp4"
echo MONTAZ-V4-OK
