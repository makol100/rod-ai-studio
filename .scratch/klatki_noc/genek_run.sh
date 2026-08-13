#!/bin/bash
# Genek (oczy) oglada 6 klatek nocnego patrolu — kazda osobno.
cd /root/rod-ai-studio
K=data/fotopulapka/klatki
W=.scratch/klatki_noc/genek.txt
P='Opisz DOKLADNIE co widac na tym zdjeciu z kamery monitoringu. Odpowiedz po polsku, krotko, w punktach: (1) Czy jest na nim CZLOWIEK, ZWIERZE albo POJAZD? Jesli nie da sie rozstrzygnac - napisz NIE WIEM, nie zgaduj. (2) Co widac w kadrze (obiekty, otoczenie)? (3) Czy zdjecie jest dzienne, zmierzchowe czy nocne/podczerwone? (4) Czy cos jest bardzo blisko obiektywu i zaslania kadr? Opisuj tylko to, co widac - zadnych domyslow o czyichs zamiarach.'
: > "$W"
for f in \
  security_camera_20260812_194046_0.9pc.jpg \
  security_camera_20260812_194132_0.9pc.jpg \
  security_camera_20260812_194901_67.9pc.jpg \
  security_camera_20260812_194947_67.4pc.jpg \
  kamera_taras_20260813_024624_12.3pc.jpg \
  kamera_taras_20260813_025812_15.9pc.jpg ; do
  echo "=============================================================" >> "$W"
  echo "KLATKA: $f" >> "$W"
  echo "=============================================================" >> "$W"
  timeout 180 python3 tools/oczy_uszy.py "$K/$f" --pytanie "$P" >> "$W" 2>&1
  echo >> "$W"
done
echo "KONIEC GENEK $(TZ=Europe/Warsaw date '+%F %T %Z')" >> "$W"
