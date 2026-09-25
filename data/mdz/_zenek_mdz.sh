#!/bin/bash
OUT=/root/rod-ai-studio/data/mdz/foto; mkdir -p /tmp/zenek_img; cd /tmp/zenek_img
BAZA="fotorealistyczne zdjecie dokumentalne, PIONOWE 9:16, naturalne swiatlo dzienne, polski ogrod dzialkowy (ROD) jesienia, realistyczne detale botaniczne, bez napisow, bez logo, bez twarzy (dlonie dozwolone)"
while IFS='|' read -r K ROSLINA P; do
  [ -z "$K" ] && continue; [ -f "$OUT/$K.jpg" ] && continue
  timeout 300 codex exec --skip-git-repo-check -s workspace-write "Wygeneruj JEDEN obraz narzedziem do generowania obrazow: $BAZA. Tresc: $P. Zapisz jako /tmp/zenek_img/mdz_$K.png i napisz tylko sciezke." </dev/null >/dev/null 2>&1
  if [ -f /tmp/zenek_img/mdz_$K.png ]; then
    python3 -c "from PIL import Image; Image.open('/tmp/zenek_img/mdz_$K.png').convert('RGB').save('$OUT/$K.jpg',quality=90)"
    python3 /root/rod-ai-studio/tools/tg_foto.py $OUT/$K.jpg "[rolka mieczyki-dalie-zimowit, ZENEK AI 0 zl] $ROSLINA — $P — 👍/👎" >/dev/null 2>&1; echo "OK $K"
  else echo "BLAD $K"; fi
done <<'LISTA'
M2_zolkniece|MIECZYK|kepa mieczykow na grzadce po przekwitnieciu, bez kwiatow, mieczowate liscie zaczynaja zolknac i brazowiec od koncow
M4_suszenie|MIECZYK|bulwy mieczykow z krotkimi przycietymi lodygami rozlozone w jednej warstwie w plytkiej drewnianej skrzynce do suszenia w przewiewnej altanie
D6_mroz|DALIA|kepa dalii na grzadce rano po pierwszym przymrozku: liscie i pedy poczernale, zwarzone i zwiedle, na trawie obok szron
D6b_karpa|DALIA|wykopana karpa dalii (kilka bulw korzeniowych) z pedami przycietymi na kilkanascie cm, odwrocona lodygami w dol na drewnianej skrzynce, zeby z pustych lodyg wyplynela woda
D7_piwnica|DALIA|karpy dalii w drewnianej skrzynce w chlodnej ciemnej piwnicy, czesciowo przysypane suchym piaskiem, obok termometr sciennny
M3b_bulwy|MIECZYK|kilka swiezo wykopanych bulw mieczykow (plaskie, okragle bulwocebule w brazowej luskowatej oslonce, na spodzie drobne bulwki przybyszowe) z lodygami przycietymi na ok. 5-10 cm, lezace na gazecie na stole w altanie, obok sekator
M3c_bulwa|MIECZYK|zblizenie: dlon w rekawicy ogrodowej trzyma jedna wykopana bulwe mieczyka - plaska okragla bulwocebula w brazowej oslonce z przycieta lodyga ok. 5-10 cm, pod nia stara wyschnieta bulwa mateczna, w tle grzadka z mieczowatymi liscmi
LISTA
echo KONIEC
