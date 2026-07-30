#!/bin/bash
# ============================================================================
# STUDIO IZABELI — KANON. Tło robione KODEM, postać wklejana z wyciętej karty.
# ============================================================================
# Decyzje Tomasza (30.07.2026), po kolei:
#   "Dopracować do perfekcji studio neutralne"     -> tło bez udawania miejsca
#   "Dodać na stałe w górnym prawym rogu logo"     -> assets/branding/rod_profilowe.png
#   "Logo najmniejsze w kółku"                     -> 110 px, maska okrągła
#   "Tło nie przygnębiające. Żywe jak natura"      -> odejście od ciemnej umbry
#   "Ma być dopasowany do tej pięknej Izabeli"     -> kolor dobrany po jej wygenerowaniu
#   "Poproszę jaśniejsze tło" -> wariant 2         -> baza #A89464 (zboże jasne)
#   cień za postacią: wariant B                    -> delikatny, siła 30
#
# Kolor dobrany do NIEJ, nie na oko: jej bluzka to #466270 (12% kadru, największa
# powierzchnia po tle), włosy i skóra #624638. Ciepłe zboże kontrastuje z turkusem bluzki.
#
# Separacja postaci od tła: NIE samym kolorem, ale CIENIEM za postacią (propozycja Zenka
# z narady 30.07 — "separacja światłem"). Bramka oka na wersji bez cienia: "kontrast jest,
# ale nie ma wyraźnego odcięcia, obraz wydaje się nieco płaski".
#
# Postać: assets/izabela/IZABELA_ODKLEJONA.png — wycięta przez Zenka modelem birefnet-portrait
# z usunięciem domieszki starego tła z pikseli częściowej alfy. Miękka krawędź 1,41%,
# zero przezroczystych pikseli na twarzy, szyi i bluzce, zero obwódek.
# Klucz koloru (colorkey) NIE nadaje się — wyżerał fragmenty czoła, policzków, nosa i szyi.
# ============================================================================
set -e
REPO=/root/rod-ai-studio
IZA="$REPO/assets/izabela/IZABELA_ODKLEJONA.png"
LOGO="$REPO/assets/branding/rod_profilowe.png"
OUT="${1:-$REPO/assets/izabela/STUDIO_IZABELI_CANON.png}"
NAPIS="${2:-PREZENTERKA AI}"

ffmpeg -v error -f lavfi -i "color=c=0xA89464:s=1080x1920" -i "$IZA" -i "$LOGO" -filter_complex "
[0:v]geq=
 r='clip(168+38*exp(-((X-540)*(X-540)/(2*520*520)+(Y-560)*(Y-560)/(2*640*640)))-30*exp(-((X-540)*(X-540)/(2*300*300)+(Y-1150)*(Y-1150)/(2*520*520))),0,255)':
 g='clip(148+36*exp(-((X-540)*(X-540)/(2*520*520)+(Y-560)*(Y-560)/(2*640*640)))-30*exp(-((X-540)*(X-540)/(2*300*300)+(Y-1150)*(Y-1150)/(2*520*520))),0,255)':
 b='clip(100+30*exp(-((X-540)*(X-540)/(2*520*520)+(Y-560)*(Y-560)/(2*640*640)))-30*exp(-((X-540)*(X-540)/(2*300*300)+(Y-1150)*(Y-1150)/(2*520*520))),0,255)'[tlo];
[1:v]scale=1080:-1[iza];
[tlo][iza]overlay=(W-w)/2:H-h[z1];
[2:v]scale=110:110,format=rgba,
 geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lte((X-55)*(X-55)+(Y-55)*(Y-55),55*55),255,0)'[lg];
[z1][lg]overlay=W-110-45:45[z2];
[z2]drawtext=text='$NAPIS':x=60:y=78:fontsize=42:fontcolor=white@0.95:
 box=1:boxcolor=black@0.26:boxborderw=14
" -frames:v 1 "$OUT" -y
echo "studio: $OUT"
