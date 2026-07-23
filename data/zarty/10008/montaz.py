# -*- coding: utf-8 -*-
"""Montaz 10008 Kontrola zza plotu: trimy wg mowy, ASS napisy duetu, sklejka."""
import sys, re, json, subprocess
sys.path.insert(0, '/app')
from pathlib import Path
from src.zarty_produkcja import ASS_HEADER, KOLORY_ASS

B = Path('/root/rod-ai-studio/data/zarty/10008')

# konce mowy z whisper (ostatni segment kazdego klipu) + zapas 0.45s
KONCE = {
 'klip_01': 6.5,   # niemy hook — staly czas
 'klip_02': 7.88, 'klip_03': 7.96, 'klip_04': 5.00, 'klip_05': 7.52,
 'klip_06': 5.00, 'klip_07': 6.00, 'klip_08': 8.00, 'klip_09': 5.68,
}
KOL = ['klip_01','klip_02','klip_03','klip_04','klip_05','klip_06','klip_07','klip_08','klip_09']
trimy = []
for k in KOL:
    t = KONCE[k]
    trimy.append(min(8.0, round(t + (0.5 if k=='klip_01' else 0.45), 2)))
(B/'trimy.txt').write_text(' '.join(str(t) for t in trimy))

kb = KOLORY_ASS['BOHATER']; kj = KOLORY_ASS['JANUSZ']; bialy='&HFFFFFF&'
# kwestie VERBATIM z kanonu + kolor mowcy
KW = {
 'klip_02': (kj, 'JANUSZ: Noooo, sąsiedzie... Widzę, że u was dzisiaj dzień lenia. A chwasty u panienki obok to już prawie regulaminową wysokość żywopłotu przekroczyły!'),
 'klip_03': (kb, 'TOMEK: Dzień dobry, panie Januszu. Sobota jest, odpoczywam. Ziemniaki posadzone, trawa skoszona...'),
 'klip_04': (kj, 'JANUSZ: No właśnie widzę to skoszone. Centymetra zabrakło!'),
 'klip_05': (kj, 'JANUSZ: Regulamin PZD wyraźnie mówi: trawa ma mieć trzy centymetry, a u pana w rogu przy kompostowniku widziałem cztery i pół. Kret panu wejdzie, wspomni pan moje słowa!'),
 'klip_06': (kb, 'TOMEK: Panie Januszu, pan to mierzył linijką?'),
 'klip_07': (kj, 'JANUSZ: Oko mam, trzydzieści lat tu gospodarzę!'),
 'klip_08': (kj, 'JANUSZ: I ten... grillujecie dzisiaj? Bo jakby węgiel drzewny dymił w stronę moich pomidorów malinowych, to wie pan... paragraf siódmy regulaminu o immisjach zapachowych...'),
 'klip_09': (kb, 'TOMEK: Kupię mu chyba tę działkę obok, żeby miał bliżej do sprawdzania...'),
}
def czas(s):
    return f'{int(s//3600)}:{int(s%3600//60):02d}:{s%60:05.2f}'

linie = []
# HOOK na niemym k01
linie.append((0.40, trimy[0]-0.30, bialy, 'Kiedy próbujesz odpocząć na RODOS...'))
off = 0.0
for k, t in zip(KOL, trimy):
    if k in KW:
        kolor, txt = KW[k]
        linie.append((off + 0.10, off + t - 0.05, kolor, txt))
    off += t

tresc = ''.join(f'Dialogue: 0,{czas(a)},{czas(b)},Default,,0,0,0,,{{\\c{k}}}{t}\n'
                for a,b,k,t in linie)
(B/'napisy8.ass').write_text(ASS_HEADER + tresc, encoding='utf-8')
print('trimy:', trimy, '| suma:', round(sum(trimy),1), 's | linii ASS:', len(linie))
