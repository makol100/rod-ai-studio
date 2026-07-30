#!/bin/bash
cd /root/rod-ai-studio/data/awatar
set -a; . /root/.gemini/.env; set +a
export GEMINI_CLI_TRUST_WORKSPACE=true
echo "[$(date)] Budzik: odpalam Genka" >> _genek_budzik.log
gemini -m gemini-3-flash-preview -p "$(cat _zadanie_biblia_genek2.md)" > _genek_biblia2_out.txt 2>&1
echo "[$(date)] Genek skończył, exit=$?, rozmiar=$(wc -c < _genek_biblia2_out.txt)" >> _genek_budzik.log
