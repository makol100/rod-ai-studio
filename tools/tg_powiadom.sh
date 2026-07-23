#!/bin/bash
# tg_powiadom.sh "tekst" [url] — powiadomienie Telegram przez HA Dom
# (webhook fabryka_rolka_gotowa; token bota mieszka w HA Dom, NIE na VPS — PROCEDURY)
T="${1:?uzycie: tg_powiadom.sh \"tekst\" [url]}"; U="${2:-}"
curl -s --max-time 15 -X POST \
  https://kzdoj77rzm29x15ipkor8zo2jnh884rs.ui.nabu.casa/api/webhook/fabryka_rolka_gotowa \
  -H 'Content-Type: application/json' \
  -d "$(python3 -c "import json,sys;print(json.dumps({'video_url':sys.argv[2],'caption':sys.argv[1]}))" "$T" "$U")" \
  -o /dev/null -w 'HTTP %{http_code}\n'
