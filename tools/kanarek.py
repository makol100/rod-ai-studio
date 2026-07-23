#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KANAREK Z PĘTLĄ KOREKCJI (DROGA HUMOR, decyzja Tomasza 23.07 "1 i 3 wdrożenie").
Owija strażnika w warstwę DIAGNOSTYCZNĄ: przy FAIL nie mówi tylko "źle", ale
KONKRETNIE co poprawić (mapowanie werdyktu -> zalecenie). Przy PASS zapisuje
prompt do banku promptów-zwycięzców (Mechanizm 3).

NIE robi automatycznych kolejnych generacji ($) — diagnozuje, decyzję o korekcie
i drugim locie podejmuje Tomasz (żelazna zasada kosztów).

Użycie:
/app/venv/bin/python tools/kanarek.py --odcinek 10008 --klip klip_02.mp4 \
  --mowca JANUSZ --kwestia "..." --kadr KADR.jpg --wzorzec JANUSZ=baza.jpg \
  --prompt "PROMPT_UŻYTY" [--typ "mówiący plan średni"] [--domena dzień]
"""
import argparse, sys, json
sys.path.insert(0, '/app')
sys.path.insert(0, '/root/rod-ai-studio/tools')
from pathlib import Path
import straznik as S

BANK = Path('/root/rod-ai-studio/wiedza/PROMPTY_WZORCE.md')

# Mapowanie: werdykt strażnika -> konkretne zalecenie korekty
def diagnoza(nazwa, wynik):
    st = wynik.get('status')
    det = wynik.get('detale', {})
    if st in ('PASS', 'POMINIĘTY'):
        return None
    if nazwa == 'język':
        if isinstance(det, dict) and det.get('język_lektora') and det['język_lektora'] != 'pl':
            return (f"JĘZYK: lektor mówi w «{det['język_lektora']}» zamiast pl "
                    f"(usłyszano: {det.get('usłyszane','')[:60]}). ZALECENIE: wzmocnij blok "
                    f"głosu w prompcie — dodaj mocniej «speaking fluent native Polish with a "
                    f"natural Polish accent», rozważ inną barwę głosu z GLOSY_VEO.")
        if isinstance(det, dict) and det.get('zgodność', 1) < 0.55:
            return (f"KWESTIA: rozjazd z kanonem (zgodność {det.get('zgodność')}). "
                    f"Usłyszano: «{det.get('usłyszane','')[:70]}». ZALECENIE: skróć kwestię, "
                    f"jedno zdanie na oddech; sprawdź trudne słowa (safety_tolerance=6).")
    if nazwa == 'tożsamość':
        if isinstance(det, dict):
            if det.get('obce_twarze'):
                return (f"TOŻSAMOŚĆ: obca twarz w kadrze {det['obce_twarze'][:2]}. "
                        f"ZALECENIE: zła referencja lub przeciek drugiej postaci — użyj kadru "
                        f"z JEDNĄ osobą, referencja z właściwej domeny światła.")
            if det.get('małe_twarze_WARN'):
                return (f"TWARZ ZA MAŁA: {det['małe_twarze_WARN'][:2]} (plan za szeroki, "
                        f"tożsamość niepewna). ZALECENIE: kadr startowy z WIĘKSZYM planem "
                        f"twarzy (plan średni/zbliżenie), nie szeroki.")
            if det.get('graniczne_WARN'):
                return (f"TOŻSAMOŚĆ GRANICZNA: {det['graniczne_WARN'][:2]}. ZALECENIE: "
                        f"referencja bliżej domeny światła sceny; rozważ mocniejszy identity-lock.")
    if nazwa == 'kotwice':
        return (f"KADR≠PROMPT: kotwice FLF za wysokie {det}. ZALECENIE: kadr startowy "
                f"za daleki od treści promptu — dopasuj kadr do opisywanej akcji/planu.")
    if nazwa == 'techniczny':
        return (f"TECHNIKA: {det.get('problemy', det)}. ZALECENIE: wada modelu "
                f"(czarne/zamrożone klatki) — regeneruj ten sam prompt, to loteria nie błąd promptu.")
    if nazwa == 'napisy':
        return (f"NAPISY-WIDMO: model wypalił tekst {det}. ZALECENIE: wzmocnij "
                f"«no captions, no subtitles, no on-screen text» w prompcie.")
    return f"{nazwa}: {st} — {str(det)[:80]}"


def zapisz_do_banku(a, werdykty):
    """Dopisuje prompt-zwycięzca do banku (wywoływane tylko przy globalnym PASS)."""
    tagi = f"[{a.mowca}]"
    if a.typ:
        tagi += f" [{a.typ}]"
    if a.domena:
        tagi += f" [{a.domena}]"
    wpis = (f"\n### {a.odcinek}/{Path(a.klip).stem} {tagi}\n"
            f"KWESTIA: {a.kwestia or '(niema)'}\n"
            f"PROMPT-ZWYCIĘZCA (przeszedł kanarka {a.data_pass}):\n"
            f"{a.prompt}\n")
    with open(BANK, 'a', encoding='utf-8') as f:
        f.write(wpis)
    return wpis


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--odcinek', required=True)
    ap.add_argument('--klip', required=True)
    ap.add_argument('--mowca', required=True)
    ap.add_argument('--kwestia', default='')
    ap.add_argument('--kadr', required=True)
    ap.add_argument('--wzorzec', action='append', default=[], help='POSTAĆ=ścieżka.jpg')
    ap.add_argument('--prompt', required=True)
    ap.add_argument('--typ', default='')
    ap.add_argument('--domena', default='')
    ap.add_argument('--zapis-bank', dest='zapis_bank', action='store_true',
                    help='przy PASS zapisz prompt do banku')
    ap.add_argument('--data-pass', dest='data_pass', default='')
    a = ap.parse_args()

    folder = Path(f'/root/rod-ai-studio/data/zarty/{a.odcinek}')
    plik = folder / a.klip
    if not plik.is_file():
        print(f'FAIL: brak pliku {plik}'); sys.exit(2)

    wzorce = {}
    for w in a.wzorzec:
        if '=' in w:
            k, v = w.split('=', 1); wzorce[k] = v

    # Zbierz werdykty strażników
    werdykty = {
        'techniczny': S.straznik_techniczny(plik, 1080, 1920),
        'napisy': S.straznik_napisow(plik),
        'język': S.straznik_scenariusza(plik, a.kwestia) if a.kwestia else {'status': 'POMINIĘTY', 'detale': 'klip niemy'},
        'tożsamość': S.straznik_tozsamosci(plik, wzorce) if wzorce else {'status': 'POMINIĘTY', 'detale': 'brak wzorca'},
    }

    print(f'=== KANAREK: {a.odcinek}/{a.klip} ({a.mowca}) ===')
    fail = False
    zalecenia = []
    for nazwa, w in werdykty.items():
        print(f'[{w["status"]:9}] {nazwa}')
        if w['status'] == 'FAIL':
            fail = True
        d = diagnoza(nazwa, w)
        if d:
            zalecenia.append(d)

    print('---')
    if fail:
        print('WERDYKT KANARKA: FAIL — batch ZABLOKOWANY. Konkretne zalecenia:')
        for z in zalecenia:
            print(f'  * {z}')
        print('\nDECYZJA TOMASZA: popraw wg zaleceń i puść drugiego kanarka ($0.64), '
              'albo zaakceptuj mimo (force). Automat nie wydaje kolejnych $ sam.')
        sys.exit(1)
    else:
        if zalecenia:
            print('WERDYKT KANARKA: PASS Z UWAGAMI — batch dozwolony, ale zwróć uwagę:')
            for z in zalecenia:
                print(f'  * {z}')
        else:
            print('WERDYKT KANARKA: PASS CZYSTY — prompt udowodniony, batch dozwolony.')
        if a.data_pass or a.zapis_bank:
            zapisz_do_banku(a, werdykty)
            print('\nPrompt zapisany do banku wzorców (PROMPTY_WZORCE.md).')
        else:
            print('\n(prompt NIE zapisany do banku — dodaj --zapis-bank po akceptacji finału)')
        sys.exit(0)


if __name__ == '__main__':
    main()
