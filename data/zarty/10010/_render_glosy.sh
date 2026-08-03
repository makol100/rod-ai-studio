#!/bin/bash
set -e
cd /root/rod-ai-studio/data/zarty/10010
ffmpeg -y -loglevel error -i klip_k06.mp4 -t 6.0 -vn -ac 1 -ar 48000 input.wav
ffmpeg -y -loglevel error -i input.wav -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=mono,asplit=2[human][helium];[human]rubberband=pitch=1.62:formant=preserved:pitchq=quality,vibrato=f=6.2:d=0.16[human2];[helium]asetrate=56640,aresample=48000,atempo=0.84746,highpass=f=500,volume=0.32[helium2];[human2][helium2]amix=inputs=2:weights='1 0.32':normalize=0,highpass=f=300,equalizer=f=2900:t=q:w=1.1:g=5,acompressor=threshold=0.075:ratio=7:attack=4:release=90:makeup=1.8,alimiter=limit=0.94[out]" -map "[out]" -ar 48000 -ac 1 glos_A.wav
ffmpeg -y -loglevel error -i input.wav -af "aformat=sample_rates=48000:channel_layouts=mono,rubberband=pitch=1.38:formant=preserved:transients=smooth:detector=soft:pitchq=quality,vibrato=f=7.4:d=0.34,tremolo=f=5.1:d=0.48,highpass=f=280,equalizer=f=2400:t=q:w=1.25:g=6,equalizer=f=4300:t=q:w=1.4:g=3,acompressor=threshold=0.045:ratio=12:attack=1.5:release=65:makeup=2.4:knee=1.5,alimiter=limit=0.93" -ar 48000 -ac 1 glos_B.wav
ffmpeg -y -loglevel error -i input.wav -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=mono,asplit=2[throat][breath];[throat]rubberband=pitch=1.48:formant=preserved:detector=soft:transients=smooth:pitchq=quality,vibrato=f=8.6:d=0.25,tremolo=f=3.3:d=0.30,highpass=f=360,equalizer=f=3200:t=q:w=0.9:g=7,acompressor=threshold=0.035:ratio=16:attack=0.8:release=130:makeup=2.8:knee=1.2[throat2];[breath]rubberband=pitch=1.21:formant=shifted:detector=soft:pitchq=quality,highpass=f=850,lowpass=f=5200,tremolo=f=6.7:d=0.62,volume=0.20[breath2];[throat2][breath2]amix=inputs=2:weights='1 0.20':normalize=0,acompressor=threshold=0.09:ratio=5:attack=12:release=220:makeup=1.35,alimiter=limit=0.92[out]" -map "[out]" -ar 48000 -ac 1 glos_C.wav
for V in A B C; do
  ffmpeg -y -loglevel error -i klip_k06_niemy.mp4 -i glos_$V.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest -movflags +faststart /root/rod-ai-studio/data/n150files/10010_k06_glos_$V.mp4
done
ls -la /root/rod-ai-studio/data/n150files/10010_k06_glos_*.mp4 | awk '{print $9, $5"B"}'
