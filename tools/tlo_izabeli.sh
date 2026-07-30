#!/bin/bash
# ============================================================================
# STUDIO IZABELI — TŁO KANONICZNE. Robione KODEM, nie generatorem obrazu.
# ============================================================================
# Decyzje Tomasza (30.07.2026), po kolei:
#   "Dopracować do perfekcji studio neutralne"  -> droga B, tło bez udawania miejsca
#   "Ziemisty brąz"                             -> baza #403A35
#   "Dodać na stałe w górnym prawym rogu logo"  -> assets/branding/rod_profilowe.png
#   "Logo najmniejsze w kółku"                  -> 110 px, maska okrągła
#   "Nie musi być zielony. Dopasować do logo"   -> po researchu wrócił do wariantu A (#403A35)
#
# Wytyczne praktyków (research 30.07, źródła w wiedza/IZABELA_KANON_0.1.md):
#   - unikać beżu/tanu/brzoskwini: imitują odcień skóry, twarz się rozpływa
#   - unikać zimnej szarości: oliwkowa skóra wychodzi zielonawo
#   - dobre: głębokie zgaszone — węgiel, granat, śliwka, ciemne taupe z brązowym podtonem
#   #403A35 to dokładnie "dark taupe with brown undertones" — trafiony wybór Tomasza
#
# Załoga jednogłośnie (Zenek, Genek, Henio): tło w czystym kodzie = identyczność co do piksela,
# zero dryfu między odcinkami, zero zależności od modelu AI, zero kosztu.
# ŻADNYCH elementów w tle poza gradientem i logo — każdy element może się przesunąć.
#
# Zmierzone: krawędzie #403A35, środek #61564B, wysokość twarzy #5D5348, pas napisu #4E463E.
# Dwa niezależne przebiegi dają IDENTYCZNY plik (SHA-256 zgodne).
# ============================================================================
set -e
REPO=/root/rod-ai-studio
LOGO="$REPO/assets/branding/rod_profilowe.png"
OUT="${1:-$REPO/assets/izabela/STUDIO_IZABELI_CANON.png}"
NAPIS="${2:-PREZENTERKA AI}"

ffmpeg -v error -f lavfi -i "color=c=0x403A35:s=1080x1920" -i "$LOGO" -filter_complex "
[0:v]geq=
 r='clip(64+33*exp(-((X-540)*(X-540)/(2*330*330)+(Y-700)*(Y-700)/(2*430*430))),0,255)':
 g='clip(58+28*exp(-((X-540)*(X-540)/(2*330*330)+(Y-700)*(Y-700)/(2*430*430))),0,255)':
 b='clip(53+22*exp(-((X-540)*(X-540)/(2*330*330)+(Y-700)*(Y-700)/(2*430*430))),0,255)'[tlo];
[1:v]scale=110:110,format=rgba,
 geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lte((X-55)*(X-55)+(Y-55)*(Y-55),55*55),255,0)'[log];
[tlo][log]overlay=W-110-45:45[zlog];
[zlog]drawtext=text='$NAPIS':x=60:y=78:fontsize=42:fontcolor=white@0.92:
 box=1:boxcolor=black@0.30:boxborderw=14
" -frames:v 1 "$OUT" -y
echo "studio: $OUT"
