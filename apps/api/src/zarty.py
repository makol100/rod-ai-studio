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
- Czworo stałych bohaterów:
  MIECZYSŁAW — ogrodnik, mądry i małomówny. Odzywa się rzadko; jak powie, to już powie.
  HELENA — jego żona, ciepła, praktyczna, zarządza wszystkim z drugiego planu.
  TOMASZ — sąsiad, nieogarnięty ale cwany: wielkie plany, kiepskie wykonanie, kombinuje.
  JACUŚ — dorosły wnuk (rodzina dalej mówi mu "Jacuś"), zadaje pytania i mówi na głos to, co wszyscy myślą.
- PUENTA należy do MIECZYSŁAWA (jedno krótkie, celne zdanie po długim milczeniu)
  ALBO do JACUSIA (rozbrajająca szczerość — mówi wprost to, co wszyscy myślą). Nigdy nie tłumacz puenty.
- W jednym klipie pokazuj maksymalnie dwie-trzy postacie (nie zawsze wszystkich).

FORMAT (dokładnie taki, {n} klipów):
KLIP 1:
RUCH: (opis akcji wideo jednym-dwoma zdaniami: kto co robi, ruch kamery, emocje na twarzach — to trafi do generatora wideo)
DIALOG: MIECZYSŁAW: "..." / HELENA: "..." / TOMASZ: "..." / JACUŚ: "..."
(WYŁĄCZNIE kwestie w cudzysłowach, didaskalia tylko krótko w nawiasie PRZED dwukropkiem,
np. TOMASZ (drapiąc się w głowę): "No jak to?". Jeśli postać w klipie MILCZY — nie wypisuj
jej w DIALOG w ogóle; milczenie i gesty opisuj w RUCH. Zero gwiazdek i formatowania.)

ZASADY TECHNICZNE:
- Każdy klip = jedna ciągła akcja do ośmiu sekund. Bez cięć wewnątrz klipu.
- ZAKAZ w RUCH: palenie (fajka, papieros), alkohol, broń — generator wideo Google
  odrzuca takie treści (content policy) i cała produkcja pada.
- W RUCHU absolutny ZAKAZ napisów i tekstu do pokazania: żadnych 'pudełko z napisem X',
  'transparent Y', 'tablica Z', etykiet, kalendarzy. Generator wideo psuje polskie litery.
  ŹLE: 'pudełko z napisem Elektroniczny odstraszacz'. DOBRZE: 'plastikowe pudełko z antenką
  i migającą diodą'. Przedmiot opisuj wyglądem, nigdy napisem.
- Liczby w DIALOGU zawsze słownie ("dziesięć", nie "10").
- Nie opisuj wyglądu bohaterów w RUCHU (wygląd trzyma kadr referencyjny) — tylko akcję i emocje.

Odpowiedz WYŁĄCZNIE scenariuszem w podanym formacie, bez komentarzy."""

STYL_BOHATEROW = (
    "Ciepła animacja 3D w stylu współczesnych filmów animowanych (nie fotorealizm). "
    "CZTERY postacie na polskiej działce przy altanie: "
    "MIECZYSŁAW — ogrodnik około siedemdziesiątki, wysoki, spokojny, siwy krótki zarost, "
    "kaszkiet, kamizelka ogrodowa, mądre zmrużone oczy, postawa człowieka, "
    "który wie. "
    "HELENA — jego żona, około sześćdziesięciu pięciu lat, ciepła twarz, siwy kok, kwiecista "
    "sukienka i fartuch kuchenny, w dłoniach często blacha z ciastem. "
    "TOMASZ — sąsiad około pięćdziesiątki, lekko zaokrąglony, przekrzywiona czapka z daszkiem, "
    "rozpięta koszula hawajska, szeroki niepewny uśmiech, w ręku zawsze jakiś gadżet. "
    "JACUŚ — dorosły wnuk około dwudziestu pięciu lat, szczupły, odstające uszy, piegi, "
    "luźna koszulka, ciekawskie wielkie oczy, wiecznie z telefonem w kieszeni. "
    "Tło: zadbana działka ROD — grządki, altana z pnączem, płot, konewki, letnie światło. "
    "Pionowy kadr 9:16, wszyscy czworo widoczni."
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
    from src.zarty_produkcja import KADR_GLOBALNY
    klipy_usd = n_klipow * KLIP_SEK * CENA_SEK
    kadr_usd = 0.0 if KADR_GLOBALNY.is_file() else CENA_KADR
    return {"klipy": n_klipow, "sekundy": n_klipow * KLIP_SEK,
            "koszt_klipy_usd": round(klipy_usd, 2),
            "koszt_kadr_usd": kadr_usd,
            "koszt_razem_usd": round(klipy_usd + kadr_usd, 2),
            "model": VEO_MODEL, "cena_za_sekunde": CENA_SEK,
            "postacie": "gotowe (koszt zero)" if KADR_GLOBALNY.is_file() else "do wygenerowania raz ($0.15)"}


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


@router.post("/zart-checkpoint/{zid}/zatwierdz")
def zart_zatwierdz(zid: str):
    """URUCHAMIA PŁATNĄ PRODUKCJĘ (kadr NB Pro + klipy Veo). Wołać tylko po
    świadomej akceptacji wyceny z checkpointu."""
    import threading
    folder = ZARTY_DIR / zid
    if not folder.is_dir():
        raise HTTPException(status_code=404, detail="Żart nie znaleziony")
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    if meta.get("stan") in ("produkcja", "klipy_veo", "dialogi", "render"):
        return {"status": "juz_trwa", "stan": meta["stan"]}
    from src.zarty_produkcja import produkuj
    threading.Thread(target=produkuj, args=(folder, STYL_BOHATEROW), daemon=True).start()
    return {"status": "produkcja_ruszyla", "wycena": meta.get("wycena"),
            "podglad_logu": f"/zarty/{zid}/log"}


@router.get("/zarty/{zid}/video")
def zart_video(zid: str):
    from fastapi.responses import FileResponse
    f = ZARTY_DIR / zid / "final.mp4"
    if not f.is_file():
        raise HTTPException(status_code=404, detail="Final jeszcze nie istnieje")
    return FileResponse(f, media_type="video/mp4", filename=f"zart_{zid}.mp4")


@router.get("/zarty/{zid}/log")
def zart_log(zid: str):
    f = ZARTY_DIR / zid / "log.txt"
    meta_p = ZARTY_DIR / zid / "meta.json"
    return {"meta": json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.is_file() else {},
            "log": f.read_text(encoding="utf-8").splitlines()[-20:] if f.is_file() else []}


@router.post("/zart-checkpoint/{zid}/zatwierdz")
def zart_zatwierdz(zid: str):
    """URUCHAMIA PŁATNĄ produkcję (kadr NB Pro + klipy Veo) w wątku.
    Wołać wyłącznie po akceptacji wyceny przez Tomasza."""
    import threading
    folder = ZARTY_DIR / zid
    if not folder.is_dir():
        raise HTTPException(status_code=404, detail="Żart nie znaleziony")
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    if meta.get("stan") in ("produkcja", "klipy_veo", "dialogi", "render"):
        return {"status": "juz_trwa", "stan": meta["stan"]}
    from src.zarty_produkcja import produkuj
    threading.Thread(target=produkuj, args=(folder, STYL_BOHATEROW), daemon=True).start()
    return {"status": "produkcja_ruszyla", "wycena": meta.get("wycena"),
            "podglad": f"/zart-checkpoint/{zid}"}


@router.get("/zarty/{zid}/video")
def zart_video(zid: str):
    from fastapi.responses import FileResponse
    f = ZARTY_DIR / zid / "final.mp4"
    if not f.is_file():
        raise HTTPException(status_code=404, detail="Brak final.mp4")
    return FileResponse(f, media_type="video/mp4", filename=f"zart_{zid}.mp4")


@router.get("/zarty/casting")
def zart_casting():
    from fastapi.responses import FileResponse
    f = ZARTY_DIR / "casting.mp3"
    if not f.is_file():
        raise HTTPException(status_code=404, detail="Brak castingu")
    return FileResponse(f, media_type="audio/mpeg", filename="casting.mp3")


# ---------------------------------------------------------------- POSTACIE (raz na zawsze)
@router.post("/zarty-postacie/generuj")
def postacie_generuj(data: dict = Body(None)):
    """Jednorazowy casting: kadr referencyjny 4 postaci (NB Pro, $0.15).
    wymus=true regeneruje (stary kadr -> .bak). Tomasz akceptuje wygląd."""
    from src.zarty_produkcja import zrob_kadr_globalny, KADR_GLOBALNY
    wymus = bool((data or {}).get("wymus"))
    if KADR_GLOBALNY.is_file() and not wymus:
        return {"status": "juz_istnieje", "podglad": "/zarty-postacie",
                "info": "Kadr postaci już jest. wymus=true żeby przegenerować."}
    zrob_kadr_globalny(STYL_BOHATEROW, wymus=wymus)
    return {"status": "ok", "podglad": "/zarty-postacie", "koszt_usd": 0.15}


@router.get("/zarty-postacie")
def postacie_podglad():
    from fastapi.responses import FileResponse
    from src.zarty_produkcja import KADR_GLOBALNY
    if not KADR_GLOBALNY.is_file():
        raise HTTPException(status_code=404, detail="Kadru jeszcze nie ma — POST /zarty-postacie/generuj")
    return FileResponse(KADR_GLOBALNY, media_type="image/jpeg")


@router.post("/zart-checkpoint/{zid}/zatwierdz")
def zart_zatwierdz(zid: str):
    """START PRODUKCJI (PŁATNE: klipy Veo wg wyceny z checkpointu). W tle."""
    import threading
    from src.zarty_produkcja import produkuj, KADR_GLOBALNY
    folder = ZARTY_DIR / zid
    if not folder.is_dir():
        raise HTTPException(status_code=404, detail="Żart nie znaleziony")
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    if meta.get("stan") not in ("checkpoint", "blad"):
        raise HTTPException(status_code=400, detail=f"Zły stan: {meta.get('stan')}")
    threading.Thread(target=produkuj, args=(folder, STYL_BOHATEROW), daemon=True).start()
    return {"status": "produkcja_ruszyla", "wycena": meta.get("wycena"),
            "podglad_stanu": f"/zart-checkpoint/{zid}"}


@router.get("/zarty/{zid}/video")
def zart_video(zid: str):
    from fastapi.responses import FileResponse
    f = ZARTY_DIR / zid / "final.mp4"
    if not f.is_file():
        raise HTTPException(status_code=404, detail="Jeszcze nie ma finalu")
    return FileResponse(f, media_type="video/mp4", filename=f"zart_{zid}.mp4")


@router.get("/zarty/{zid}/log")
def zart_log(zid: str):
    f = ZARTY_DIR / zid / "log.txt"
    if not f.is_file():
        return {"log": []}
    return {"log": f.read_text(encoding="utf-8").splitlines()[-25:]}


@router.post("/zart-checkpoint/{zid}/audytuj")
def zart_audytuj(zid: str, data: dict = Body(None)):
    """Audyt żartu przez Claude Fable 5 — grzechy: napisy w RUCH, zły format
    DIALOG, cyfry, słaba puenta, za długie kwestie na 8s klipu."""
    import os
    import requests as req
    folder = ZARTY_DIR / zid
    if not folder.is_dir():
        raise HTTPException(status_code=404, detail="Żart nie znaleziony")
    sc = (data or {}).get("scenariusz") or (folder / "scenariusz.txt").read_text(encoding="utf-8")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Brak ANTHROPIC_API_KEY")
    system = (
        "Jesteś audytorem scenariuszy 24-sekundowych animowanych żartów (3 klipy po 8 s) "
        "dla polskich działkowców. Format: KLIP N: / RUCH: / DIALOG:. Postacie: MIECZYSŁAW "
        "(mądry, małomówny — jak powie, to już powie), HELENA (żona, ciepła, praktyczna), "
        "TOMASZ (sąsiad-kombinator), JACUŚ (wnuczek 8 lat, szczery). Sprawdź i NAPRAW:\n"
        "1. NAPISY w RUCH ('z napisem X', tablice, etykiety) — generator wideo psuje polski "
        "tekst; zamień na opis wyglądu przedmiotu.\n"
        "2. Format DIALOG: wyłącznie kwestie IMIĘ: \"tekst\" (didaskalia krótko w nawiasie "
        "przed dwukropkiem); milczenie opisuje się w RUCH, nie w DIALOG; zero gwiazdek.\n"
        "3. Liczby w DIALOG słownie z polską gramatyką.\n"
        "4. Suma mówienia w klipie ≤ 7 sekund (ok. 16-18 słów) — dłuższe skróć.\n"
        "5. Jedna ciągła akcja na klip (RUCH bez cięć i 'następnego dnia' w środku klipu).\n"
        "6. PUENTA: ostatni klip musi zaskakiwać; należy do MIECZYSŁAWA (krótko, celnie) "
        "albo JACUSIA (dziecięca szczerość). Nie tłumaczy się jej.\n"
        "7. Humor życzliwy, działkowy — zero polityki i przykrości.\n"
        "Odpowiedz DOKŁADNIE w formacie:\nPROBLEMY:\n- ...(albo 'Brak problemow.')\n"
        "PROPOZYCJA_SCENARIUSZA:\n(cały scenariusz KLIP/RUCH/DIALOG — poprawiony, albo "
        "przepisany bez zmian gdy brak problemów)"
    )
    r = req.post("https://api.anthropic.com/v1/messages",
                 headers={"x-api-key": api_key, "anthropic-version": "2023-06-01",
                          "content-type": "application/json"},
                 json={"model": "claude-fable-5", "max_tokens": 4096, "system": system,
                       "messages": [{"role": "user", "content": sc}]},
                 timeout=120)
    r.raise_for_status()
    odp = "".join(b.get("text", "") for b in r.json().get("content", []))
    problemy, propozycja = odp, ""
    if "PROPOZYCJA_SCENARIUSZA:" in odp:
        problemy, propozycja = odp.split("PROPOZYCJA_SCENARIUSZA:", 1)
    problemy = [l.strip(" -") for l in problemy.replace("PROBLEMY:", "").splitlines()
                if l.strip().startswith("-")]
    return {"problemy": problemy, "propozycja": propozycja.strip(),
            "brak_problemow": bool(problemy) and "brak problem" in problemy[0].lower()}
