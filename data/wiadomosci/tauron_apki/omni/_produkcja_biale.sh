#!/bin/bash
# Okno A (D-0368): 16 klipow Omni, biale tlo (D-0366), kanarek whisper po kazdym; blokada Google -> zapis i dalej
cd /root/rod-ai-studio/data/wiadomosci/tauron_apki/omni
for k in W1_2 W1_3 W1_4 W1_5 W1_6 W1_7 W1_8 W2_1 W2_2 W2_3 W2_4 W2_5 W2_6 W2_7 W2_8 W2_9; do
  [ -f omni_$k.mp4 ] && { echo "$k: juz jest"; continue; }
  python3 _gen_omni.py $k 10s > _gen_$k.log 2>&1 || { echo "$k: BLAD $(grep -o "prohibited content\|Error code: [0-9]*" _gen_$k.log | head -1)"; continue; }
  W=$(docker exec -i -w /app -e PYTHONPATH=/app fabryka-api ./venv/bin/python /root/rod-ai-studio/data/wiadomosci/tauron_apki/omni/_kanarek.py $k 2>&1 | grep -v Warning | tail -1)
  echo "$k: $W"
done
echo "PRODUKCJA ZAKONCZONA"
