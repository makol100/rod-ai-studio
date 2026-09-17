#!/bin/bash
# zatrzymanie petli produkcji Omni (uruchamiac z pliku — pkill -f lapie wlasne polecenie)
for p in $(pgrep -f "_produkcja_biale.sh"); do kill "$p" 2>/dev/null; done
for p in $(pgrep -f "_gen_omni.py"); do kill "$p" 2>/dev/null; done
sleep 1
echo "pozostale: $(pgrep -fc '_produkcja_biale|_gen_omni')"
