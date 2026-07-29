#!/usr/bin/env python3
"""oczy_uszy.py — CALA zaloga widzi i slyszy. Nie tylko Genek, nie tylko w jego glowie.

Powod powstania (29.07.2026, Tomasz: "Dlaczego jeszcze nie wdrozyles nic zeby widziec i slyszec
jak np. na YouTube"): 29.07 Klaudek nie mogl obejrzec filmu z YouTube. Genek mogl, ale trzeba
bylo pisac skrypt od zera. Teraz to jest jedno polecenie, dostepne dla kazdego na VPS.

Uzycie:
    python3 tools/oczy_uszy.py https://www.youtube.com/watch?v=XXXX --co transkrypcja
    python3 tools/oczy_uszy.py /sciezka/film.mp4 --co opis
    python3 tools/oczy_uszy.py /sciezka/nagranie.mp3 --co transkrypcja --zapis /tmp/wynik.txt
    python3 tools/oczy_uszy.py film.mp4 --pytanie "Czy w 24 sekundzie zdjecie lezy czy stoi?"

Tryby (--co):
    transkrypcja  doslowny zapis sciezki dzwiekowej, slowo w slowo, zero interpretacji
    opis          co widac na ekranie, chronologicznie, z czasami
    oba           transkrypcja + opis obrazu
    (--pytanie zastepuje tryb: zadaje konkretne pytanie o material)

YouTube idzie przez fileUri (Google pobiera film po swojej stronie — omija blokade botow na VPS).
Plik lokalny idzie przez Files API (do 2 GB), z czekaniem na przetworzenie.
Fail-closed: blad API, pusta odpowiedz albo uciety JSON = wyjscie 2 i komunikat, NIGDY zmyslona tresc.

UWAGA — ZMIERZONE 29.07, NIE POWTARZAC BLEDU:
Pytanie o KONKRETNA SEKUNDE calego filmu jest NIEWIARYGODNE. Test na WD_0001 v6 (58 s): model dostal
tylko 15 254 tokeny wideo na cale nagranie, czyli mocno przerzedzone klatki w niskiej rozdzielczosci —
i odpowiedzial, ze zdjecie w 24 s "lezy". Ta sama sekunda wyciagnieta ffmpegiem jako pelna klatka
i zapytana OTWARTYM pytaniem: "uklad kadru jest pionowy, niebo u gory, ziemia u dolu".
ZASADA: orientacje, detal i ocene pojedynczej sekundy rozstrzyga KLATKA (tools/bramka_oka.py),
a nie pytanie o cale wideo. Cale wideo sluzy do transkrypcji, przebiegu i ogolnego opisu.
"""
import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

MODEL = "gemini-2.5-flash"
BAZA = "https://generativelanguage.googleapis.com"

POLECENIA = {
    "transkrypcja": (
        "Wysluchaj material w CALOSCI. Sporzadz WIERNY, DOSLOWNY zapis sciezki dzwiekowej — slowo w slowo, "
        "w jezyku oryginalu. NIE streszczaj, NIE komentuj, NIE oceniaj, NIE dodawaj nic od siebie. "
        "Zachowaj kolejnosc wypowiedzi."
    ),
    "opis": (
        "Obejrzyj material w CALOSCI. Opisz chronologicznie CO WIDAC na ekranie, z przyblizonymi czasami "
        "w formacie [mm:ss]. Opisuj wylacznie to, co realnie widzisz w kadrze — ujecia, osoby, przedmioty, "
        "napisy, orientacje obrazu. NIE domyslaj sie, NIE interpretuj intencji."
    ),
    "oba": (
        "Obejrzyj i wysluchaj material w CALOSCI. Zwroc DWIE sekcje: "
        "'=== SCIEZKA DZWIEKOWA ===' z doslowna transkrypcja slowo w slowo, oraz "
        "'=== OBRAZ ===' z chronologicznym opisem tego, co widac, z czasami [mm:ss]. "
        "Wylacznie fakty z materialu, zero interpretacji."
    ),
}


def klucz() -> str:
    for linia in open("/root/.gemini/.env", encoding="utf-8"):
        if linia.startswith("GEMINI_API_KEY="):
            return linia.split("=", 1)[1].strip()
    raise SystemExit("BLAD: brak GEMINI_API_KEY w /root/.gemini/.env")


def wyslij_plik(sciezka: str, k: str) -> str:
    """Files API: upload + czekanie az stan bedzie ACTIVE. Zwraca file_uri."""
    typ = mimetypes.guess_type(sciezka)[0] or "application/octet-stream"
    rozmiar = os.path.getsize(sciezka)
    print(f"[oczy_uszy] wysylam {os.path.basename(sciezka)} ({rozmiar // 1024} KB, {typ})", file=sys.stderr)
    start = urllib.request.Request(
        f"{BAZA}/upload/v1beta/files?key={k}",
        data=json.dumps({"file": {"display_name": os.path.basename(sciezka)}}).encode(),
        headers={
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Header-Content-Length": str(rozmiar),
            "X-Goog-Upload-Header-Content-Type": typ,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(start, timeout=120) as r:
        url = r.headers.get("X-Goog-Upload-URL")
    if not url:
        raise SystemExit("BLAD: Files API nie zwrocilo adresu wysylki")
    with open(sciezka, "rb") as f:
        dane = f.read()
    wgraj = urllib.request.Request(
        url, data=dane,
        headers={"Content-Length": str(rozmiar), "X-Goog-Upload-Offset": "0",
                 "X-Goog-Upload-Command": "upload, finalize"},
    )
    with urllib.request.urlopen(wgraj, timeout=900) as r:
        info = json.loads(r.read())
    nazwa = info["file"]["name"]
    uri = info["file"]["uri"]
    for _ in range(60):
        with urllib.request.urlopen(f"{BAZA}/v1beta/{nazwa}?key={k}", timeout=60) as r:
            stan = json.loads(r.read()).get("state")
        if stan == "ACTIVE":
            return uri
        if stan == "FAILED":
            raise SystemExit("BLAD: przetwarzanie pliku po stronie Google nie powiodlo sie")
        print(f"[oczy_uszy] przetwarzanie... ({stan})", file=sys.stderr)
        time.sleep(5)
    raise SystemExit("BLAD: plik nie stal sie ACTIVE w 5 minut")


def patrz(zrodlo: str, polecenie: str, k: str, limit: int) -> str:
    if zrodlo.startswith(("http://", "https://")):
        czesc = {"file_data": {"file_uri": zrodlo}}
    else:
        if not os.path.isfile(zrodlo):
            raise SystemExit(f"BLAD: nie ma pliku {zrodlo}")
        typ = mimetypes.guess_type(zrodlo)[0] or "application/octet-stream"
        czesc = {"file_data": {"file_uri": wyslij_plik(zrodlo, k), "mime_type": typ}}
    body = json.dumps({
        "contents": [{"parts": [czesc, {"text": polecenie}]}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": limit,
                             "thinkingConfig": {"thinkingBudget": 0}},
    }).encode()
    req = urllib.request.Request(
        f"{BAZA}/v1beta/models/{MODEL}:generateContent?key={k}",
        data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            odp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"BLAD API {e.code}: {e.read().decode()[:500]}")
    kandydaci = odp.get("candidates") or []
    if not kandydaci:
        raise SystemExit(f"BLAD: model nie zwrocil tresci ({json.dumps(odp)[:300]})")
    c = kandydaci[0]
    tekst = "".join(p.get("text", "") for p in c.get("content", {}).get("parts", []))
    if not tekst.strip():
        raise SystemExit("BLAD: pusta odpowiedz — NIE zmyslam zastepczej tresci")
    uzycie = odp.get("usageMetadata", {})
    szczegoly = {d.get("modality"): d.get("tokenCount") for d in uzycie.get("promptTokensDetails", [])}
    print(f"[oczy_uszy] powod zakonczenia: {c.get('finishReason')} | tokeny wejscia: {szczegoly}", file=sys.stderr)
    if c.get("finishReason") not in (None, "STOP"):
        print(f"[oczy_uszy] UWAGA: odpowiedz moze byc niepelna ({c.get('finishReason')})", file=sys.stderr)
    return tekst


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("zrodlo", help="URL YouTube albo sciezka do pliku wideo/audio/obrazu")
    p.add_argument("--co", default="oba", choices=list(POLECENIA))
    p.add_argument("--pytanie", default="", help="konkretne pytanie o material (zastepuje --co)")
    p.add_argument("--zapis", default="", help="zapisz wynik do pliku")
    p.add_argument("--limit", type=int, default=30000, help="maks. tokenow odpowiedzi")
    a = p.parse_args()

    polecenie = a.pytanie.strip() or POLECENIA[a.co]
    if a.pytanie.strip():
        polecenie += ("\nOdpowiadaj WYLACZNIE na podstawie tego, co widzisz i slyszysz w materiale. "
                      "Jesli material nie rozstrzyga — napisz NIE WIEM.")
    wynik = patrz(a.zrodlo, polecenie, klucz(), a.limit)
    if a.zapis:
        with open(a.zapis, "w", encoding="utf-8") as f:
            f.write(wynik)
        print(f"[oczy_uszy] zapisane: {a.zapis} ({len(wynik)} znakow)", file=sys.stderr)
    print(wynik)
    return 0


if __name__ == "__main__":
    sys.exit(main())
