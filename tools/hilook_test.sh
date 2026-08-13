#!/bin/bash
# hilook_test.sh — test logowania do NVR HiLook i kamer w 192.168.3.0/24
# Czyta /root/.hilook_cred. NIGDY nie drukuje hasla. Drukuje tylko kod HTTP i model.
set -u
CRED=/root/.hilook_cred

if [ ! -f "$CRED" ]; then
  echo "BRAK PLIKU $CRED — Tomasz jeszcze nie wpisal danych."
  exit 1
fi

# shellcheck disable=SC1090
. "$CRED"

if [ -z "${HILOOK_USER:-}" ] || [ -z "${HILOOK_PASS:-}" ]; then
  echo "PLIK JEST, ale brak HILOOK_USER lub HILOOK_PASS."
  exit 1
fi

# curl-config w pamieci (haslo nie trafia do argv ani do ps)
CFG=$(mktemp /dev/shm/.hlk.XXXXXX)
chmod 600 "$CFG"
printf 'user = "%s:%s"\ndigest\n' "$HILOOK_USER" "$HILOOK_PASS" > "$CFG"
trap 'rm -f "$CFG"' EXIT

for ip in 192.168.3.110 192.168.3.111 192.168.3.112 192.168.3.113 192.168.3.114; do
  OUT=$(curl -s -m 10 -K "$CFG" -o /tmp/hlk_body.$$ -w "%{http_code}" \
        "http://$ip/ISAPI/System/deviceInfo" 2>/dev/null)
  MODEL=$(grep -oE "<model>[^<]*</model>|<deviceName>[^<]*</deviceName>|<firmwareVersion>[^<]*</firmwareVersion>" /tmp/hlk_body.$$ 2>/dev/null | tr '\n' ' ')
  rm -f /tmp/hlk_body.$$
  case "$OUT" in
    200) echo "$ip  HTTP 200  ZALOGOWANO  $MODEL" ;;
    401) echo "$ip  HTTP 401  ZLE DANE LOGOWANIA" ;;
    000) echo "$ip  BRAK ODPOWIEDZI (timeout/niedostepny)" ;;
    *)   echo "$ip  HTTP $OUT" ;;
  esac
done
