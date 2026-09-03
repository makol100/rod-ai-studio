#!/bin/bash
# Czeka na rekord A kamery.rodwozniki.pl -> 157.90.155.155, potem dopina host w Caddy (edycja W MIEJSCU, nie sed -i) i powiadamia Tomasza
for i in $(seq 1 180); do
  IP=$(dig +short A kamery.rodwozniki.pl @1.1.1.1 | head -1)
  [ -z "$IP" ] && IP=$(dig +short A kamery.rodwozniki.pl @dns.home.pl | head -1)
  if [ "$IP" = "157.90.155.155" ]; then
    cd /root/claude-vps-mcp && cp Caddyfile Caddyfile.bak-domena-$(date +%m%d%H%M)
    python3 - <<'PY'
s=open('Caddyfile',encoding='utf-8').read()
old='kamery.157-90-155-155.sslip.io {'
if 'kamery.rodwozniki.pl' not in s:
    s=s.replace(old,'kamery.rodwozniki.pl, '+old,1)
    open('Caddyfile','w',encoding='utf-8').write(s)   # zapis w miejscu (ten sam inode)
print('caddy host dodany')
PY
    docker exec caddy-mcp caddy validate --config /etc/caddy/Caddyfile >/dev/null 2>&1 && docker exec caddy-mcp caddy reload --config /etc/caddy/Caddyfile >/dev/null 2>&1
    sleep 25; CODE=$(curl -s -m 20 -o /dev/null -w "%{http_code}" https://kamery.rodwozniki.pl/)
    cd /root/rod-ai-studio && python3 -c "
import sys; sys.path.insert(0,'tools'); import hans_ucho as h
tok,czat=h._wczytaj_token_hansa(); h._odpowiedz(tok,str(czat),'Hans: DNS kamery.rodwozniki.pl wskazuje na VPS. Strona kamer: https://kamery.rodwozniki.pl (odpowiedz bez hasla: HTTP $CODE, 401 = OK). Login/haslo bez zmian.')"
    python3 tools/decyzje.py --dodaj "03.09 DOMENA: rekord A kamery.rodwozniki.pl → 157.90.155.155 pojawil sie w DNS; host dodany do Caddy (alias przy kamery.157-90-155-155.sslip.io), certyfikat automatyczny; test bez hasla HTTP $CODE." --temat kamery >/dev/null 2>&1
    echo "GOTOWE $(date)"; exit 0
  fi
  sleep 60
done
echo "TIMEOUT 3h bez rekordu"
