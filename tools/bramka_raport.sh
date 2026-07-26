#!/bin/bash
# Kazdy bieg bramki (preflight/kanarek/straznik) przez ten wrapper:
# pelny werdykt laduje jako plik na panelu + ping Telegram do Tomasza.
# Uzycie: bramka_raport.sh <odcinek> <nazwa_raportu> <komenda...>
ODC="$1"; NAZWA="$2"; shift 2
PLIK="/root/rod-ai-studio/data/zarty/${ODC}/raporty/${NAZWA}.txt"
PUB="/root/rod-ai-studio/data/n150files/${ODC}_raport_${NAZWA}.txt"
{ echo "=== RAPORT BRAMKI: ${ODC}/${NAZWA} | $(date -Is) ==="; "$@" 2>&1 \
  | grep -viE "insightface|Applied providers|find model|set det-size"; } | tee "$PLIK"
cp "$PLIK" "$PUB"
URL="https://panel.157-90-155-155.sslip.io/n150files/${ODC}_raport_${NAZWA}.txt"
WERDYKT=$(grep -m1 -E "WERDYKT" "$PLIK" || echo "raport bez werdyktu")
bash /root/rod-ai-studio/tools/tg_powiadom.sh "Bramka ${ODC}/${NAZWA}: ${WERDYKT}" "$URL" >/dev/null 2>&1 \
  && echo "[raport] Telegram wyslany" || echo "[raport] Telegram NIE poszedl (HA Dom?)"
echo "[raport] ${URL}"
