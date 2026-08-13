#!/bin/bash
# Watchdog ucha Hansa — luka wskazana przez Henia 13.08:
# wbudowany alarm ucha gasi TYLKO przy awarii POLACZENIA, nie przy "service stopped".
# 12.08 ucho padlo o 13:40 i nikt sie nie dowiedzial.
export TZ=Europe/Warsaw
STAN=$(systemctl is-active hans-ucho.service || true)
if [ "$STAN" != "active" ]; then
  python3 /root/rod-ai-studio/tools/dzwonek.py \
    "UCHO HANSA NIE CHODZI (systemctl: $STAN). Twoje wiadomosci do @HansFabrykaRolek_bot NIE SA zapisywane, a /pakiet NIE ZADZIALA." \
    --tytul "WATCHDOG: ucho Hansa stoi" || true
  systemctl start hans-ucho.service || true
fi
