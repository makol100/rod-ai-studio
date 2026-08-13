#!/bin/bash
B=/root/rod-ai-studio/data/wiadomosci/0001-teren
for i in $(seq 1 40); do
  R=$(docker exec fabryka-api /app/venv/bin/python $B/_kling_0001_pull.py 2>&1 | tail -1)
  echo "$(date +%H:%M:%S) próba $i: $R"
  if [ "$R" = "POBRANY" ] || [ "$R" = "JUZ POBRANY" ]; then
    bash $B/_montaz.sh && echo "MONTAZ-ZROBIONY" && touch $B/work/_gotowe.flag
    exit 0
  fi
  echo "$R" | grep -q "BRAK URL\|BLAD" && exit 1
  sleep 60
done
