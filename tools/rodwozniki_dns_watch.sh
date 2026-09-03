#!/bin/bash
# czeka na rekordy A rodwozniki.pl/www → 157.90.155.155, potem sprawdza HTTPS i melduje Tomaszowi na Telegram (jednorazowo)
for i in $(seq 1 240); do
  A=$(dig +short A rodwozniki.pl @1.1.1.1 | head -1)
  if [ "$A" = "157.90.155.155" ]; then
    sleep 20; K=$(curl -s -m 25 -o /dev/null -w "%{http_code}" https://rodwozniki.pl/); W=$(dig +short A www.rodwozniki.pl @1.1.1.1 | head -1)
    cd /root/rod-ai-studio && python3 -c "
import sys; sys.path.insert(0,'tools'); import hans_ucho as h
tok,czat=h._wczytaj_token_hansa(); h._odpowiedz(tok,str(czat),'Hans: DNS rodwozniki.pl wskazuje na VPS. https://rodwozniki.pl odpowiada HTTP $K (www: ${W:-brak rekordu}). Strona ROD jest w internecie.')"
    echo "$(date) DNS OK, HTTP $K" >> /root/rod-ai-studio/logs/rodwozniki_dns.log; exit 0
  fi
  sleep 30
done
