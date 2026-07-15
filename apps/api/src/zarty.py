# -*- coding: utf-8 -*-
"""
FABRYKA ŻARTÓW — Droga B (decyzja Tomasza 15.07.2026, "profesjonalnie").

Pipeline: Bielik pisze żart (KLIP/RUCH/DIALOG) -> CHECKPOINT z wyceną w $
-> [po zatwierdzeniu] kadr referencyjny bohaterów (Nano Banana Pro)
-> klipy wideo Veo 3.1 Fast image-to-video (fal.ai, 9:16, 8s, bez audio)
-> dialogi edge-tts (Marek + Zofia) -> ffmpeg: concat + audio + napisy.

KOSZTY (fal.ai, stan 15.07.2026): Veo 3.1 Fast $0.10/s bez audio,
Nano Banana Pro $0.15/obraz. Żart 3x8s ~= $2.55. Checkpoint OBOWIĄZKOWY.
"""
import json
import re
import time
from pathlib import Path

from fastapi import APIRouter, Body, HTTPException

from src.ai.ollama import generate

router = APIRouter()

ZARTY_DIR = Path("/root/rod-ai-studio/data/zarty")
ZARTY_DIR.mkdir(parents=True, exist_ok=True)

VEO_MODEL = "fal-ai/veo3.1/fast/image-to-video"
CENA_SEK = 0.10          # USD / s bez audio (720p/1080p)
CENA_KADR = 0.15         # USD / kadr referencyjny NB Pro
KLIP_SEK = 8

PROMPT_ZART = """Napisz scenariusz KRÓTKIEGO animowanego żartu wideo dla polskich działkowców (ROD).

TEMAT ŻARTU: {temat}

ZASADY HUMORU:
- Struktura: sytuacja -> narastanie -> PUENTA w ostatnim klipie. Puenta ma zaskakiwać.
- Humor życzliwy, działkowy: sąsiedzkie przekomarzanie, walka z przyrodą, duma z plonów.
  Zero polityki, zero chamstwa, zero krzywdy.
- Akcja dzieje się NA DZIAŁCE: grządki, altana, płot, kompostownik, szklarnia.
- Dwoje stałych bohaterów: HENIEK (starszy działkowiec, pewny siebie, zawsze "wie lepiej")
  i HALINKA (sąsiadka zza płotu, rzeczowa, celna riposta). Puenta zwykle należy do Halinki.

FORMAT (dokładnie taki, {n} klipów):
KLIP 1:
RUCH: (opis akcji wideo jednym-dwoma zdaniami: kto co robi, ruch kamery, emocje na twarzach — to trafi do generatora wideo)
DIALOG: HENIEK: "..." / HALINKA: "..." (kto mówi w tym klipie; może mówić jedna osoba; zdania krótkie, mówione)

ZASADY TECHNICZNE:
- Każdy klip = jedna ciągła akcja do ośmiu sekund. Bez cięć wewnątrz klipu.
- W RUCHU żadnych napisów, tablic z tekstem, kalendarzy — generator psuje polskie litery.
- Liczby w DIALOGU zawsze słownie ("dziesięć", nie "10").
- Nie opisuj wyglądu bohaterów w RUCHU (wygląd trzyma kadr referencyjny) — tylko akcję i emocje.

Odpowiedz WYŁĄCZNIE scenariuszem w podanym formacie, bez komentarzy."""

STYL_BOHATEROW = (
    "Ciepła animacja 3D w stylu współczesnych filmów animowanych (nie fotorealizm): "
    "HENIEK — starszy pan około siedemdziesiątki, krępy, siwy wąs, słomkowy kapelusz, "
    "koszula w kratę, szelki, ogorzała twarz, pogodne oczy. "
    "HALINKA — sąsiadka około sześćdziesiątki, drobna, okulary na łańcuszku, chustka "
    "na głowie w drobne kwiatki, fartuch ogrodowy, ironiczny półuśmiech. "
    "Obydwoje stoją przy drewnianym płocie między dwiema zadbanymi działkami: grządki, "
    "altana w tle, ciepłe letnie światło. Pionowy kadr 9:16."
)


def _nowy_id() -> str:
    stare = [int(p.name) for p in ZARTY_DIR.iterdir() if p.is_dir() and p.name.isdigit()]
    return f"{(max(stare) + 1) if stare else 1:04d}"


def _parsuj(scenariusz: str) -> list:
    klipy = []
    for m in re.finditer(r"KLIP\s+(\d+):\s*\nRUCH:\s*(.+?)\nDIALOG:\s*(.+?)(?=\nKLIP\s+\d+:|\Z)",
                         scenariusz, re.S):
        klipy.append({"nr": int(m.group(1)), "ruch": m.group(2).strip(),
                      "dialog": m.group(3).strip()})
    return klipy


def _wycena(n_klipow: int) -> dict:
    klipy_usd = n_klipow * KLIP_SEK * CENA_SEK
    return {"klipy": n_klipow, "sekundy": n_klipow * KLIP_SEK,
            "koszt_klipy_usd": round(klipy_usd, 2),
            "koszt_kadr_usd": CENA_KADR,
            "koszt_razem_usd": round(klipy_usd + CENA_KADR, 2),
            "model": VEO_MODEL, "cena_za_sekunde": CENA_SEK}


@router.post("/generate-zart")
def generate_zart(data: dict = Body(...)):
    """Bielik pisze scenariusz żartu (DARMOWE) i staje na checkpoincie.
    Nic płatnego nie rusza bez /zart-checkpoint/{id}/zatwierdz."""
    temat = (data.get("temat") or "").strip()
    if not temat:
        raise HTTPException(status_code=400, detail="Podaj temat żartu")
    n = int(data.get("klipy") or 3)
    n = max(2, min(n, 4))

    zid = _nowy_id()
    folder = ZARTY_DIR / zid
    folder.mkdir(parents=True, exist_ok=True)

    scenariusz = generate(PROMPT_ZART.format(temat=temat, n=n), temperature=0.85,
                          max_tokens=1600)
    klipy = _parsuj(scenariusz)

    (folder / "scenariusz.txt").write_text(scenariusz, encoding="utf-8")
    (folder / "temat.txt").write_text(temat, encoding="utf-8")
    meta = {"id": zid, "temat": temat, "stan": "checkpoint", "ts": time.time(),
            "klipy_sparsowane": len(klipy), "wycena": _wycena(len(klipy) or n)}
    (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1),
                                      encoding="utf-8")
    return {**meta, "scenariusz": scenariusz,
            "uwaga": "CHECKPOINT: nic płatnego nie ruszyło. Zatwierdź przez "
                     f"/zart-checkpoint/{zid}/zatwierdz po akceptacji wyceny."}


@router.get("/zart-checkpoint/{zid}")
def zart_checkpoint(zid: str):
    folder = ZARTY_DIR / zid
    if not folder.is_dir():
        raise HTTPException(status_code=404, detail="Żart nie znaleziony")
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    meta["scenariusz"] = (folder / "scenariusz.txt").read_text(encoding="utf-8")
    return meta


@router.post("/zart-checkpoint/{zid}/zapisz")
def zart_zapisz(zid: str, data: dict = Body(...)):
    """Ręczna poprawka scenariusza — darmowa, checkpoint zostaje otwarty."""
    folder = ZARTY_DIR / zid
    if not folder.is_dir():
        raise HTTPException(status_code=404, detail="Żart nie znaleziony")
    sc = (data.get("scenariusz") or "").strip()
    if not sc:
        raise HTTPException(status_code=400, detail="Pusty scenariusz")
    (folder / "scenariusz.txt").write_text(sc, encoding="utf-8")
    klipy = _parsuj(sc)
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    meta["klipy_sparsowane"] = len(klipy)
    meta["wycena"] = _wycena(len(klipy))
    (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1),
                                      encoding="utf-8")
    return {"status": "ok", "klipy": len(klipy), "wycena": meta["wycena"]}


@router.get("/zarty")
def lista_zartow():
    out = []
    for p in sorted(ZARTY_DIR.iterdir(), reverse=True):
        if not (p / "meta.json").is_file():
            continue
        m = json.loads((p / "meta.json").read_text(encoding="utf-8"))
        m["final"] = (p / "final.mp4").is_file()
        out.append(m)
    return out
