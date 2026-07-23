#!/bin/sh
# n150fix — dogranie modulow storage w zywym Alpine netboot (modloop nie wjechal)
# 19.07.2026, okno A. Po sukcesie sam odpala instalator /n150 (SKRYPT v3).
KVER=$(uname -r)
echo "==============================================="
echo "  N150 FIX: dogrywam sterowniki dyskow"
echo "  kernel: $KVER"
echo "==============================================="
mkdir -p /lib/modules
echo "[1/4] Proba glowna: modloop (paczka modulow Alpine)..."
cd /tmp
rm -f /tmp/modloop-lts
if wget -q "http://dl-cdn.alpinelinux.org/alpine/v3.22/releases/x86_64/netboot/modloop-lts"; then
  mkdir -p /tmp/ml
  if mount -o loop -t squashfs /tmp/modloop-lts /tmp/ml 2>/dev/null; then
    echo "  modloop zamontowany — kopiuje moduly $KVER do RAM..."
    cp -a "/tmp/ml/modules/$KVER" /lib/modules/ 2>/dev/null || cp -a /tmp/ml/modules/* /lib/modules/ 2>/dev/null
    umount /tmp/ml 2>/dev/null
    depmod -a 2>/dev/null || true
  else
    echo "  mount squashfs nie dziala (kernel bez loop/squashfs) — ide do planu B"
  fi
else
  echo "  nie moge pobrac modloop — ide do planu B"
fi
if ! modprobe ahci 2>/dev/null; then
  echo "[2/4] PLAN B: instaluje pakiet linux-lts przez apk (moze potrwac 1-3 min)..."
  echo "http://dl-cdn.alpinelinux.org/alpine/v3.22/main" > /etc/apk/repositories
  apk update >/dev/null 2>&1 || apk update || true
  apk add linux-lts >/dev/null 2>&1 || apk add linux-lts || true
  depmod -a 2>/dev/null || true
fi
echo "[3/4] Laduje sterowniki: ahci / sd_mod / nvme / mmc..."
for m in libata libahci ahci sd_mod nvme mmc_block; do modprobe "$m" 2>/dev/null || true; done
mdev -s 2>/dev/null || true
sleep 2
mdev -s 2>/dev/null || true
echo "--- /proc/partitions teraz: ---"
cat /proc/partitions
if [ -b /dev/sda ] || [ -b /dev/nvme0n1 ] || [ -b /dev/mmcblk0 ]; then
  echo ""
  echo "[4/4] DYSK WIDOCZNY. Przechodze do instalatora HAOS..."
  sleep 2
  wget -q -O /tmp/n150 http://157.90.155.155:8000/n150
  exec sh /tmp/n150
fi
echo ""
echo "BLAD: dalej brak dysku. Dodatkowa diagnoza:"
lsmod | head -15
dmesg | grep -iE 'ahci|ata[0-9]|nvme|mmc' | tail -10 || true
echo ">>> ZROB ZDJECIE TEGO EKRANU <<<"
exit 1
