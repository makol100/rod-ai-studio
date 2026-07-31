#!/bin/bash
# ============================================================================
# FOTO -> UJECIE PIONOWE 1080x1920. Kanon ruchu zdjec, decyzje Tomasza 30.07.2026:
#   zdjecia PIONOWE  -> NAJAZD (powolne zblizenie), jego slowo: "Najazd"
#   zdjecia POZIOME  -> ZE ROZMYTYM TLEM (wariant 3), nic ze zdjecia nie ginie
# Orientacje WYKRYWANE automatycznie po dekodowaniu, bo telefon zapisuje pionowe
# zdjecia jako poziome z obrotem -90 w metadanych (wykryte 30.07 — bez tego
# wycielibysmy dwie trzecie kadru z czterech zdjec).
# Uzycie: tools/foto_ruch.sh <zdjecie> <sekundy> <plik_wyjsciowy>
# ============================================================================
set -e
F="$1"; T="${2:-4}"; OUT="$3"; PODPIS="$4"
[ -z "$OUT" ] && { echo "uzycie: $0 <zdjecie> <sekundy> <wyjscie.mp4> [podpis autora]"; exit 1; }
# PODPIS AUTORA — wariant 2 wybrany przez Tomasza 30.07: prawy dolny rog, 34 px, cien zamiast paska.
# Uzywany dla zdjec nie naszego autorstwa (np. "fot. Roman Sitko" na zdjeciu zarosnietego terenu z FB).
if [ -n "$PODPIS" ]; then
  DT=",drawtext=text='${PODPIS}':x=w-tw-40:y=h-th-40:fontsize=34:fontcolor=white@0.92:shadowcolor=black@0.85:shadowx=2:shadowy=2"
else
  DT=""
fi
ffmpeg -v error -i "$F" -frames:v 1 /tmp/_orient.png -y
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 /tmp/_orient.png)
H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 /tmp/_orient.png)
FPS=30
# 30.07: sam warunek "pionowe" NIE wystarcza. Zdjecie 1536x2048 (proporcje 3:4) jest pionowe,
# ale po dopasowaniu szerokosci do 1080 ma tylko 1440 px wysokosci — na kadr 1920 brakuje 480.
# Najazd wymaga, zeby po przeskalowaniu do szerokosci 1080 wysokosc byla WIEKSZA niz 1920.
WYS_PO=$(python3 -c "print(int($H*1080/$W))")
if [ "$WYS_PO" -gt 1990 ]; then
  # PIONOWE — najazd z 1.0 do 1.15 przez caly czas trwania
  KROK=$(python3 -c "print(round(0.15/($T*$FPS), 8))")
  ffmpeg -v error -loop 1 -i "$F" -t "$T" -r $FPS -vf \
    "scale=1080:-2,crop=1080:1920:0:'(ih-1920)*0.4',zoompan=z='min(1.15,1+$KROK*on)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=$FPS${DT},setsar=1" \
    -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p "$OUT" -y
  echo "$(basename "$F"): PIONOWE -> najazd, ${T}s"
else
  # POZIOME (i pionowe za niskie na najazd) — cale zdjecie w kadrze na rozmytym tle,
  # CALOSC z NAJAZDEM. Tomasz 30.07: "Nic sie nie dzieje na tym zdjeciu" — pierwsza wersja
  # byla nieruchoma. Wariant A: zdjecie i tlo zblizaja sie razem, ruch spojny z pionowymi.
  KROK=$(python3 -c "print(round(0.14/($T*$FPS), 8))")
  ffmpeg -v error -loop 1 -i "$F" -t "$T" -r $FPS -filter_complex \
    "[0:v]scale=-2:2200,crop=1240:2200:'(iw-1240)/2':0,boxblur=30:2,eq=brightness=-0.08,zoompan=z='min(1.14,1+${KROK}*on)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=$FPS[tlo];[0:v]scale=1240:-2,zoompan=z='min(1.14,1+${KROK}*on)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x469:fps=$FPS[przod];[tlo][przod]overlay=(W-w)/2:(H-h)/2${DT},setsar=1" \
    -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p "$OUT" -y
  echo "$(basename "$F"): POZIOME -> rozmyte tlo + najazd, ${T}s"
fi
