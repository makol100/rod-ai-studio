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

# Rola: wersja profesjonalna. (Propozycja Tomasza: "Steven Spielberg pił wodę
# z miski, w której moczyłem nogi" — kanon zespołu, ale IQ modelu nie podnosi.
# Podnosi je rzemiosło + wzorzec poniżej.)
# Rola: wersja rzemieslnicza. (Tomasz proponowal: "Steven Spielberg pil wode
# z miski, w ktorej moczylem nogi" — kanon zespolu, ale IQ modelu nie podnosi.)
# Rola: wersja rzemieslnicza. (Tomasz proponowal: "Steven Spielberg pil wode
# z miski, w ktorej moczylem nogi" — kanon zespolu, ale IQ modelu nie podnosi.)
PROMPT_ZART = '''Jesteś doświadczonym scenarzystą komediowym. Twoja specjalność: 30-sekundowe skecze wizualne, w których GAG DZIEJE SIĘ W OBRAZIE, a słowa tylko go dobijają. Piszesz o polskiej działce (ROD).
skecze wizualne — gag dzieje się W OBRAZIE, kwestia tylko go dobija. Piszesz
o polskiej działce (ROD).
Napisz scenariusz 3-klipowego żartu wideo (każdy klip 8 sekund) na temat: {temat}

OBSADA (używaj TYLKO tych postaci):
MIECZYSŁAW - mądry ogrodnik ok. 70 lat, MAŁOMÓWNY, mówi tylko puentę.
HELENA - jego żona, ciepła, konkretna.
TOMASZ - sąsiad kombinator, wiecznie testuje "nowoczesne" pomysły.
JACUŚ - dorosły wnuk, mówi na głos to, co wszyscy myślą.

ŻELAZNY FORMAT (dokładnie tak, 3 klipy):
KLIP 1: OBRAZ: [co widać - absurd/problem widoczny od pierwszej sekundy] MÓWI: [imię] KWESTIA: [maks 10 słów]
KLIP 2: OBRAZ: [eskalacja - sytuacja się pogłębia] MÓWI: [imię] KWESTIA: [maks 10 słów]
KLIP 3: OBRAZ: [Mieczysław reaguje spokojnie] MÓWI: MIECZYSŁAW KWESTIA: [puenta, maks 10 słów, sucha i celna]

ZASADA NADRZĘDNA (ważniejsza od wszystkich):
ŻART MUSI BYĆ ZROZUMIAŁY W TRZY SEKUNDY DLA KAŻDEGO — dziesięciolatka i babci.

WZORZEC RYTMU I STYLU (sprawdzony na publiczności — NIE kopiuj tematu, miejsca ani rekwizytów, kopiuj RYTM i typ humoru):
KLIP 1: OBRAZ: OGRÓD: Helena wjeżdża przez furtkę z taczką pełną ogromnych cukinii, zatrzymuje taczkę przed drewnianą altaną i woła w stronę jej okna. MÓWI: HELENA KWESTIA: Tomku! Przyniosłam ci świeżutkie cukinie!
KLIP 2: OBRAZ: WNĘTRZE ALTANY, kamera w środku pomieszczenia: Tomasz kuca na podłodze pod oknem, przyciśnięty do ściany, i zerka zza firanki; przez szybę widać rozmyty ogród. MÓWI: TOMASZ KWESTIA: Ciii... może pomyśli, że wyjechałem.
KLIP 3: OBRAZ: PRZY PŁOCIE: Mieczysław opiera się o drewniany płot i spokojnie kiwa głową. MÓWI: MIECZYSŁAW KWESTIA: W zeszłym tygodniu to on udawał remont.
Dlaczego działa: absurd WIDAĆ od pierwszej sekundy, eskalacja jest fizyczna, puenta ujawnia STAŁY numer Tomka — zaskoczenie w ostatnich słowach.

WZORZEC RYTMU I STYLU (sprawdzony na publiczności — NIE kopiuj tematu, miejsca ani rekwizytów, kopiuj RYTM i typ humoru):
KLIP 1: OBRAZ: OGRÓD: Helena wjeżdża przez furtkę z taczką pełną ogromnych cukinii, zatrzymuje taczkę przed drewnianą altaną i woła w stronę jej okna. MÓWI: HELENA KWESTIA: Tomku! Przyniosłam ci świeżutkie cukinie!
KLIP 2: OBRAZ: WNĘTRZE ALTANY, kamera w środku pomieszczenia: Tomasz kuca na podłodze pod oknem, przyciśnięty do ściany, i zerka zza firanki; przez szybę widać rozmyty ogród. MÓWI: TOMASZ KWESTIA: Ciii... może pomyśli, że wyjechałem.
KLIP 3: OBRAZ: PRZY PŁOCIE: Mieczysław opiera się o drewniany płot i spokojnie kiwa głową. MÓWI: MIECZYSŁAW KWESTIA: W zeszłym tygodniu to on udawał remont.
Dlaczego działa: absurd WIDAĆ od pierwszej sekundy, eskalacja jest fizyczna (dorosły facet chowa się we własnej altanie), puenta ujawnia STAŁY numer Tomka — zaskoczenie w ostatnich słowach.

WZORZEC RYTMU I STYLU (sprawdzony na publiczności — NIE kopiuj tematu, miejsc
ani rekwizytów; kopiuj wyłącznie RYTM i typ humoru):
KLIP 1: OBRAZ: OGRÓD: Helena wjeżdża przez furtkę z taczką pełną ogromnych cukinii, zatrzymuje taczkę przed drewnianą altaną i woła w stronę jej okna. MÓWI: HELENA KWESTIA: Tomku! Przyniosłam ci świeżutkie cukinie!
KLIP 2: OBRAZ: WNĘTRZE ALTANY, kamera w środku pomieszczenia: Tomasz kuca na podłodze pod oknem, przyciśnięty do ściany, i zerka zza firanki; przez szybę widać rozmyty ogród. MÓWI: TOMASZ KWESTIA: Ciii... może pomyśli, że wyjechałem.
KLIP 3: OBRAZ: PRZY PŁOCIE: Mieczysław opiera się o drewniany płot i spokojnie kiwa głową. MÓWI: MIECZYSŁAW KWESTIA: W zeszłym tygodniu to on udawał remont.
Dlaczego działa: absurd widać w 1. sekundzie (taczka gigantycznych cukinii),
eskalacja jest FIZYCZNA (dorosły facet ukrywa się we własnej altanie), a puenta
ujawnia, że to stały wzorzec zachowania — zaskoczenie w ostatnich słowach.
Zero wiedzy fachowej (taryfy, przepisy, technika). Mechanizm śmieszności musi być
WIDOCZNY NA EKRANIE: śmieszy to, co widać, a kwestie tylko dobijają.
Test: gdyby wyciszyć dźwięk, sytuacja nadal ma być zabawna.

ZASADY HUMORU:
1. SYTUACYJNY i ZROZUMIAŁY: śmieszy obraz plus jedna celna kwestia. Każdy ma się rozpoznać (ślimaki, krety, sąsiedzi, nadmiar plonów, pogoda, pożyczanie narzędzi).
2. ZERO gierek słownych, ZERO abstrakcji. Babcia i wnuk mają zrozumieć bez tłumaczenia.
3. Jedna kwestia na klip. Krótko. Mieczysław mówi TYLKO w klipie 3.
4. Puenta to spokojna mądrość albo sucha riposta. Po puencie NIC już nie ma.
5. Postaci NIE tłumaczą żartu. Żart ma się sam bronić.
6. SUCHY SARKAZM zamiast wygłupów: postaci traktują absurd śmiertelnie poważnie.
7. KONTRAST: dramatyczna reakcja, przyziemna przyczyna (im zwyklejsza, tym śmieszniej).
8. W OBRAZIE wymieniaj WYŁĄCZNIE postaci widoczne w kadrze. Miejsca opisuj bez imion
   (pisz "altana", NIGDY "altana Tomasza") — każde imię w OBRAZIE trafia do kadru!
9. LOGIKA MIĘDZY KLIPAMI: jeśli ktoś się ukrywa, wcześniej nie mógł być widoczny.
10. KAŻDY OBRAZ zaczyna się od miejsca: "WNĘTRZE ALTANY:" albo "OGRÓD:" albo
    "PRZY PŁOCIE:". Przy wnętrzu dopisz, że kamera jest w środku pomieszczenia.
11. Unikaj akcji, które generator psuje: pukanie do drzwi, otwieranie drzwi,
    precyzyjne gesty dłońmi. Lepiej: wołanie, niesienie, patrzenie, kucanie.

Odpowiedz WYŁĄCZNIE scenariuszem w podanym formacie, bez komentarzy.'''

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
    for m in re.finditer(r"KLIP\s*(\d)\s*:\s*OBRAZ:\s*(.+?)\s*M[OÓ]WI:\s*([A-Za-złśŁŚ]+)\s*KWESTIA:\s*(.+?)(?=KLIP\s*\d\s*:|$)",
                         scenariusz, re.S | re.I):
        klipy.append({"nr": int(m.group(1)),
                      "ruch": " ".join(m.group(2).split()),
                      "mowi": m.group(3).strip().upper(),
                      "kwestia": " ".join(m.group(4).split()).strip('"')})
    return sorted(klipy, key=lambda k: k["nr"])
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
        "dla polskich działkowców. Format: KLIP N: / OBRAZ: [scena] / MÓWI: [IMIĘ] / KWESTIA: [jedna kwestia bez cudzysłowów]. Postacie: MIECZYSŁAW "
        "(mądry, małomówny — jak powie, to już powie), HELENA (żona, ciepła, praktyczna), "
        "TOMASZ (sąsiad-kombinator), JACUŚ (wnuczek 8 lat, szczery). Sprawdź i NAPRAW:\n"
        "1. NAPISY w OBRAZ ('z napisem X', tablice, etykiety) — generator wideo psuje polski "
        "tekst; zamień na opis wyglądu przedmiotu.\n"
        "2. Dokładnie JEDNA kwestia na klip; postać z MÓWI musi być widoczna w OBRAZIE; "
        "milczenie opisuje się w OBRAZIE; zero gwiazdek i didaskaliów w KWESTII.\n"
        "3. Liczby w KWESTII słownie z polską gramatyką.\n"
        "0a. Imię postaci w OBRAZIE = postać w kadrze; sprawdź, czy nie psuje to logiki (np. ukrywający się widoczny wcześniej). Miejsca bez imion.\n"
        "0. GRZECH GŁÓWNY: żart wymaga wiedzy fachowej (taryfy, przepisy, technika) albo mechanizm śmieszności NIE jest widoczny w OBRAZIE — wtedy odrzuć całość i zaproponuj prostszy koncept.\n"
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
