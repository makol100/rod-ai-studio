#!/bin/sh
# N150 -> HAOS 18.1 — v3 (okno A, 19.07.2026)
# v3: aktywne wykrywanie dysku (modprobe+mdev+petla 30s, sda/nvme/mmc),
#     pelna diagnoza przy braku, bezpiecznik anty-USB, dd na wykryty dysk
set -e
echo "==============================================="
echo "  N150 -> Home Assistant OS 18.1   [SKRYPT v3]"
echo "==============================================="
modprobe ahci 2>/dev/null || true
modprobe sd_mod 2>/dev/null || true
modprobe nvme 2>/dev/null || true
modprobe mmc_block 2>/dev/null || true
mdev -s 2>/dev/null || true
DISK=""
i=0
while [ $i -lt 30 ]; do
  for c in /dev/sda /dev/nvme0n1 /dev/mmcblk0; do
    if [ -b "$c" ]; then DISK="$c"; break; fi
  done
  [ -n "$DISK" ] && break
  [ $i -eq 0 ] && echo "Czekam na dysk (do 30 s)..."
  sleep 1
  mdev -s 2>/dev/null || true
  i=$((i+1))
done
if [ -z "$DISK" ]; then
  echo ""
  echo "BLAD: zaden dysk nie pojawil sie po 30 s. DIAGNOZA:"
  echo "--- /proc/partitions ---"
  cat /proc/partitions
  echo "--- moduly storage ---"
  lsmod | grep -E 'ahci|nvme|sd_mod|mmc|libata' || echo "(BRAK modulow storage — modloop nie wjechal?)"
  echo "--- dmesg storage ---"
  dmesg | grep -iE 'ahci|sata|nvme|scsi|mmc|ata[0-9]' | tail -12 || true
  echo ""
  echo ">>> ZROB ZDJECIE TEGO EKRANU <<<"
  exit 1
fi
B=$(basename "$DISK")
TRANS=$(readlink -f "/sys/block/$B" 2>/dev/null || true)
REMOV=$(cat "/sys/block/$B/removable" 2>/dev/null || echo 0)
case "$TRANS" in
  *usb*) echo "STOP: $DISK wyglada na urzadzenie USB — NIE PISZE. ($TRANS)"; exit 1;;
esac
if [ "$REMOV" = "1" ]; then
  echo "STOP: $DISK oznaczony jako wymienny — NIE PISZE."
  exit 1
fi
echo "OK: dysk wewnetrzny znaleziony: $DISK"
fdisk -l "$DISK" 2>/dev/null | head -3
echo ""
echo "!!! ZA 10 SEKUND CALY DYSK $DISK ZOSTANIE WYMAZANY !!!"
echo "!!! Ctrl+C zeby przerwac !!!"
sleep 10
echo "Pobieram HAOS 18.1 (578 MB) i pisze na $DISK ..."
echo "Kilka-kilkanascie minut CISZY = NORMALNE. Nie wylaczac zasilania."
wget -q -O- "https://github.com/home-assistant/operating-system/releases/download/18.1/haos_generic-x86-64-18.1.img.xz" | unxz | dd of="$DISK" bs=4M
sync
echo ""
echo "=== GOTOWE. HAOS na dysku $DISK. Restart za 5 s ==="
sleep 5
reboot -f
