#!/bin/bash
cd /root/rod-ai-studio/data/rolki_info/tauron_kdt/tomasz
for S in 2 3 4 5 6; do
  for PROBA in 1 2; do
    SUF="_T"; [ $PROBA = 2 ] && SUF="_T2"
    IREF=/root/rod-ai-studio/data/rolki_info/tauron_kdt/tomasz/iref_T1.jpg SUFIKS=$SUF timeout 960 /root/omni_venv/bin/python _gen_seg.py $S - 10s 2>&1 | tail -1
    W=$(timeout 500 python3 _bramka_mowy.py omni_seg${S}${SUF}.mp4 $S 2>/dev/null)
    echo "$W" | tail -6
    if echo "$W" | grep -q "WERDYKT MOWY: CZYSTO"; then echo "SEG $S OK ($SUF)"; cp omni_seg${S}${SUF}.mp4 T${S}_OK.mp4; break; else echo "SEG $S PROBLEM ($SUF) — proba $PROBA"; fi
  done
done
echo PETLA_KONIEC
