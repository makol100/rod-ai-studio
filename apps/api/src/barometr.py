# -*- coding: utf-8 -*-
"""
TESTOWY BAROMETR GRZYBIARZA — Woźniki i okolice (~20 km).

Pomysł: grzyby sypią się po deszczu + kilku ciepłych dniach. Zamiast czytać
grupy na FB (prywatne, nie da się legalnie automatem) liczymy sygnał z pogody:
  - suma opadów z 10 dni (im więcej, tym lepiej, nasycenie ~25 mm)
  - BONUS za deszcz sprzed 4-10 dni (grzybnia potrzebuje czasu, nie wczorajszej ulewy)
  - średnia temperatura z 5 dni (optimum 12-19 st. C)
  - KARA za przymrozek w ostatnich 5 dniach

Dane: Open-Meteo (za darmo, bez klucza). Cache 3 h — nie walimy w API przy każdym wejściu.
To wersja TESTOWA — kalibrowana o obserwacje z grup grzybiarskich, nie zastępuje lasu.
"""
import json
import os
import time
import requests

CACHE = "/root/rod-ai-studio/data/barometr_cache.json"
CACHE_SEK = 3 * 3600

LOKALIZACJE = [
    ("Woźniki",   50.588, 18.989),
    ("Lubliniec", 50.667, 18.684),
    ("Koszęcin",  50.633, 18.833),
    ("Boronów",   50.683, 18.900),
]


def _pogoda(lat, lon):
    """Ostatnie 10 dni: opady dzienne, temp. średnia i min."""
    import datetime as dt
    dzis = dt.date.today()
    start = dzis - dt.timedelta(days=10)
    koniec = dzis - dt.timedelta(days=1)
    r = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": lat, "longitude": lon,
            "start_date": start.isoformat(), "end_date": koniec.isoformat(),
            "daily": "precipitation_sum,temperature_2m_mean,temperature_2m_min",
            "timezone": "Europe/Warsaw",
        }, timeout=20)
    r.raise_for_status()
    return r.json()["daily"]


def _wskaznik(d):
    """0-100 + rozbicie na czynniki (żeby dało się wytłumaczyć wynik)."""
    opady = [x or 0 for x in d["precipitation_sum"]]
    t_sr = d["temperature_2m_mean"]
    t_min = d["temperature_2m_min"]

    suma10 = sum(opady)
    # deszcz sprzed 4-10 dni (indeksy 0..6 przy oknie 10-dniowym konczacym sie wczoraj)
    suma_stare = sum(opady[:7])
    t5 = sum(t_sr[-5:]) / 5
    min5 = min(t_min[-5:])

    p_deszcz = min(suma10 / 25.0, 1.0) * 45
    p_bonus = min(suma_stare / 15.0, 1.0) * 15
    if 12 <= t5 <= 19:
        p_temp = 40.0
    elif t5 < 12:
        p_temp = max(0.0, (t5 - 5) / 7) * 40
    else:
        p_temp = max(0.0, (26 - t5) / 7) * 40
    kara = -20 if min5 < 2 else 0

    razem = max(0, min(100, round(p_deszcz + p_bonus + p_temp + kara)))
    return {
        "wynik": razem,
        "opady_10dni_mm": round(suma10, 1),
        "opady_4_10dni_mm": round(suma_stare, 1),
        "temp_srednia_5dni": round(t5, 1),
        "temp_min_5dni": round(min5, 1),
        "skladowe": {"deszcz": round(p_deszcz), "bonus_stary_deszcz": round(p_bonus),
                     "temperatura": round(p_temp), "kara_przymrozek": kara},
        "opady_dzienne": opady,
        "dni": d["time"],
    }


def _status(w):
    if w >= 75:
        return "IDŹ DO LASU", "#1F7A5C", "Warunki bardzo dobre. Po takiej pogodzie zwykle się sypie."
    if w >= 55:
        return "Warto sprawdzić", "#2E9E7A", "Jest wilgoć, jest ciepło. Dobre typy: skraje lasów, młodniki."
    if w >= 30:
        return "Coś się rusza", "#C8922E", "Za wcześnie na kosze, ale zwiad nie zaszkodzi."
    return "Sucho", "#A2533F", "Szkoda benzyny. Czekamy na deszcz."


def dane(wymus=False):
    if not wymus and os.path.exists(CACHE):
        try:
            c = json.load(open(CACHE, encoding="utf-8"))
            if time.time() - c.get("ts", 0) < CACHE_SEK:
                return c
        except Exception:
            pass

    lok = []
    for nazwa, lat, lon in LOKALIZACJE:
        try:
            w = _wskaznik(_pogoda(lat, lon))
            w["nazwa"] = nazwa
            lok.append(w)
        except Exception as e:
            lok.append({"nazwa": nazwa, "blad": str(e)})

    ok = [x for x in lok if "wynik" in x]
    sredni = round(sum(x["wynik"] for x in ok) / len(ok)) if ok else 0
    status, kolor, opis = _status(sredni)

    wynik = {
        "ts": time.time(),
        "aktualizacja": time.strftime("%d.%m.%Y %H:%M"),
        "wynik": sredni,
        "status": status,
        "kolor": kolor,
        "opis": opis,
        "lokalizacje": lok,
    }
    try:
        json.dump(wynik, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    except Exception:
        pass
    return wynik
