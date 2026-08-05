#!/usr/bin/env python3
"""SYGNAL DZWIEKOWY WIADOMOSCI DZIALKOWYCH — skladany kodem, wlasnosc fabryki.

Decyzja Tomasza 4.08.2026: „Robcie sygnal."
Powod: muzyka, ktora mamy (Kevin MacLeod + katalog music_atrybucja), wymaga podawania autora,
a nasza wlasna zasada z wiedza/NAUKI.md brzmi „audio wylacznie PD/CC0 — po lekcji werbla".
Sygnal zlozony z czystych tonow jest NASZA wlasnoscia: zero licencji, zero atrybucji, zero kosztu.

Charakter wg Henia: „nie muzyka — SYGNAL. 3-4 tony, ktore mowia: uwaga, zaczyna sie."
Wg Zenka: spokojny, nowoczesny, oficjalny — bez fanfar, bez werbla, bez wiejskiego motywu.

Wynik: WAV 48 kHz stereo, dopasowany dlugoscia do czolowki (6 s).
"""
import argparse
import math
import struct
import wave
from pathlib import Path

CZESTOTLIWOSC = 48000
SEKUND = 6.0

# Akord durowy — spokojny i oficjalny. Tony w hercach.
# A3 (220) -> D4 (293,66) -> Fis4 (369,99) -> A4 (440)
# Wznoszaca sekwencja = „zaczyna sie", bez fanfary i bez werbla.
TONY = [
    # (start_s, dlugosc_s, czestotliwosc_Hz, glosnosc)
    # WERSJA 2 (Tomasz 4.08: „Troszke weselej") — wyzej, zwawiej, z jasnym domknieciem.
    # Poprzednia byla za powazna: niski A3 i wolne wchodzenie brzmialy dostojnie, ale ciezko.
    (0.30, 1.6, 293.66, 0.15),   # D4   — start juz w jasniejszym rejestrze
    (0.80, 1.5, 369.99, 0.15),   # Fis4 — tercja wielka, to ona daje „wesolo"
    (1.30, 1.5, 440.00, 0.15),   # A4
    (1.80, 2.3, 587.33, 0.17),   # D5   — oktawa wyzej, jasne domkniecie
    # lekka iskra przy tytule — krotkie, wysokie, delikatne
    (2.60, 0.5, 739.99, 0.09),   # Fis5
    (2.95, 0.5, 880.00, 0.09),   # A5
    (3.30, 1.5, 1174.66, 0.08),  # D6 — wysoki blysk, cichy
    # cieple domkniecie pod przejsciem do Izabeli
    (4.40, 1.5, 440.00, 0.10),   # A4
    (4.40, 1.5, 587.33, 0.09),   # D5 — razem, czysta kwarta
]

PODKLAD = (146.83, 0.030)        # D3 — wyzej niz w wersji 1, lzejszy


def obwiednia(t, dlugosc):
    """Miekkie wejscie i wyjscie tonu — bez klikniec i bez ataku perkusyjnego."""
    naras = min(0.12, dlugosc * 0.2)
    zanik = dlugosc * 0.65
    if t < naras:
        a = t / naras
        return a * a * (3 - 2 * a)
    reszta = dlugosc - naras
    if reszta <= 0:
        return 1.0
    p = (t - naras) / reszta
    return max(0.0, (1.0 - p) ** 1.7)


def zbuduj(wyjscie):
    n = int(CZESTOTLIWOSC * SEKUND)
    probki = [0.0] * n

    for start, dlug, f, glos in TONY:
        i0 = int(start * CZESTOTLIWOSC)
        for i in range(int(dlug * CZESTOTLIWOSC)):
            if i0 + i >= n:
                break
            t = i / CZESTOTLIWOSC
            e = obwiednia(t, dlug)
            faza = 2 * math.pi * f * t
            # ton podstawowy + cicha oktawa = cieplejsze brzmienie niz goly sinus
            v = math.sin(faza) + 0.30 * math.sin(2 * faza) + 0.12 * math.sin(3 * faza)
            probki[i0 + i] += v * glos * e

    # podklad przez cala dlugosc, wchodzi i wychodzi miekko
    f, glos = PODKLAD
    for i in range(n):
        t = i / CZESTOTLIWOSC
        e = min(1.0, t / 0.8) * min(1.0, max(0.0, (SEKUND - t) / 1.2))
        probki[i] += math.sin(2 * math.pi * f * t) * glos * e

    # zabezpieczenie przed przesterowaniem
    szczyt = max(abs(min(probki)), abs(max(probki)), 1e-9)
    if szczyt > 0.89:
        probki = [p * (0.89 / szczyt) for p in probki]

    Path(wyjscie).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(wyjscie), "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(CZESTOTLIWOSC)
        ramki = bytearray()
        for p in probki:
            v = int(max(-1.0, min(1.0, p)) * 32767)
            ramki += struct.pack("<hh", v, v)
        w.writeframes(bytes(ramki))
    print(wyjscie)


if __name__ == "__main__":
    a = argparse.ArgumentParser(description="Sygnal dzwiekowy Wiadomosci Dzialkowych")
    a.add_argument("--output", default="/root/rod-ai-studio/assets/audio/SYGNAL_WIADOMOSCI.wav")
    args = a.parse_args()
    zbuduj(args.output)
