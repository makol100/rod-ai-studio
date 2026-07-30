#!/bin/bash
cd /root/rod-ai-studio/data/awatar
export COQUI_TOS_AGREED=1
TEKST="Dzień dobry, witamy w najnowszym serwisie informacyjnym ROD Woźniki. Z tej strony wasz Działkowy Dziennikarz. Przypominam wszystkim działkowcom, że w najbliższą sobotę odbędzie się obowiązkowy odczyt liczników energii elektrycznej. Pogoda na jutro zapowiada się wspaniale, więc proszę wyciągać leżaki i obficie podlewać pomidory. Do usłyszenia przy płocie!"
for M in mykyta oleksa; do
  /opt/xtts/bin/tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
    --speaker_wav matka_uk_$M.wav --language_idx pl \
    --text "$TEKST" --out_path xtts_${M}_pl.wav && echo "GOTOWE: xtts_${M}_pl.wav"
done
