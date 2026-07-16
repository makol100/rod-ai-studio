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
from fastapi.responses import FileResponse

from src.ai.ollama import generate

router = APIRouter()

ZARTY_DIR = Path("/root/rod-ai-studio/data/zarty")
ZARTY_DIR.mkdir(parents=True, exist_ok=True)

VEO_MODEL = "fal-ai/veo3.1/fast (t2v + audio)"
CENA_SEK = 0.15          # USD / s, t2v z audio 1080p — jak w zarty_produkcja
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
    RX = (r"KLIP\s*(\d)\s*:\s*OBRAZ:\s*(.+?)"
          r"\s*M[OÓ]WI:\s*([A-Za-zócęąśłżźńÓCĘĄŚŁŻŹŃ]+(?:\s*\((?:G[ŁL]OS|BANK)\))?)\s*KWESTIA:\s*(.+?)"
          r"(?:\s*M[OÓ]WI2:\s*([A-Za-zócęąśłżźńÓCĘĄŚŁŻŹŃ]+(?:\s*\((?:G[ŁL]OS|BANK)\))?)\s*KWESTIA2:\s*(.+?))?"
          r"(?=KLIP\s*\d\s*:|$)")
    for m in re.finditer(RX, scenariusz, re.S | re.I):
        k = {"nr": int(m.group(1)),
             "ruch": " ".join(m.group(2).split()),
             "mowi": m.group(3).strip().upper(),
             "kwestia": " ".join(m.group(4).split()).strip('"')}
        if m.group(5):
            k["mowi2"] = m.group(5).strip().upper()
            k["kwestia2"] = " ".join((m.group(6) or "").split()).strip('"')
        klipy.append(k)
    return sorted(klipy, key=lambda k: k["nr"])

REGULY_AUDYTU = [
    ("puka", "pukanie/stukanie — Veo to psuje; zamien na wolanie"),
    ("stuka", "pukanie/stukanie — Veo to psuje; zamien na wolanie"),
    ("kolacze", "pukanie — Veo to psuje"),
    ("drzwi", "drzwi jako akcja — Veo psuje otwieranie/zamykanie; przenies akcje"),
    ("lapie za", "chwyt precyzyjny — grac reakcja/sugestia, nie kontaktem"),
    ("chwyta", "chwyt precyzyjny — grac reakcja/sugestia"),
    ("sciska", "sciskanie — grac reakcja drugiej strony"),
    ("obejmuje", "kontakt dwoch cial — ryzyko choreografii"),
    ("ciagnie", "kontakt/szarpanie — ryzyko choreografii"),
    ("szarpie", "kontakt/szarpanie — ryzyko choreografii"),
    ("podaje", "przekazywanie z rak do rak — Veo gubi przedmiot"),
    ("wrecza", "przekazywanie z rak do rak — Veo gubi przedmiot"),
    ("na drzewie", "postac na drzewie — lewitacja; grac dol drzewa/glos"),
    ("w koronie", "postac w koronie — lewitacja; grac trzesaca korone/glos"),
    ("na galezi", "postac na galezi — lewitacja"),
    ("wspina", "wspinaczka — Veo psuje fizyke"),
    ("nikogo", "NEGACJA w opisie — modele obrazu robia odwrotnie (przywoluja postac); opisz pozytywnie co MA byc"),
    ("nie widac", "NEGACJA w opisie — modele obrazu robia odwrotnie; opisz pozytywnie"),
    ("nikt nie", "NEGACJA w opisie — modele obrazu robia odwrotnie; opisz pozytywnie"),
    ("bez nikogo", "NEGACJA w opisie — opisz pozytywnie"),
]

def _norm_pl(t: str) -> str:
    for a, b in [("ą","a"),("ć","c"),("ę","e"),("ł","l"),("ń","n"),("ó","o"),("ś","s"),("ż","z"),("ź","z")]:
        t = t.replace(a, b)
    return t

def _audyt_scen(klipy: list) -> list:
    problemy = []
    try:
        from src.zarty_produkcja import OPISY_POSTACI
        imiona = list(OPISY_POSTACI.keys())
    except Exception:
        imiona = []
    for k in klipy:
        obraz_raw = k.get("ruch", "") or k.get("obraz", "")
        obraz = _norm_pl(obraz_raw.lower())
        for fraza, opis in REGULY_AUDYTU:
            if fraza in obraz:
                problemy.append({"klip": k["nr"], "fraza": fraza, "problem": opis})
        w_kadrze = [im for im in imiona
                    if _norm_pl(im.lower()) in _norm_pl(obraz_raw.upper().lower())]
        w_kadrze = [im for im in imiona if _norm_pl(im.title().lower()) in obraz or _norm_pl(im.lower()) in obraz]
        if len(set(w_kadrze)) >= 2:
            problemy.append({"klip": k["nr"], "fraza": "+".join(sorted(set(w_kadrze))),
                             "problem": "dwie postacie w jednym kadrze — ryzyko choreografii; rozdziel na osobne klipy"})
    return problemy

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
    platne = [k for k in klipy if "(BANK)" not in (k.get("mowi", "").upper())]
    meta["wycena"] = _wycena(len(platne))
    meta["audyt"] = _audyt_scen(klipy)
    (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1),
                                      encoding="utf-8")
    return {"status": "ok", "klipy": len(klipy), "wycena": meta["wycena"],
            "audyt": meta["audyt"]}


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


@router.get("/zarty/{zid}/kadr/{nr}")
def zart_kadr(zid: str, nr: int):
    """DROGA ROLKA HUMOR: podglad kadru kluczowego klipu."""
    f = ZARTY_DIR / zid / f"kadr_{nr:02d}.jpg"
    if not f.is_file():
        raise HTTPException(status_code=404, detail="brak kadru")
    return FileResponse(f, media_type="image/jpeg")


@router.post("/zart-checkpoint/{zid}/kadry")
def zart_kadry(zid: str, data: dict = Body(None)):
    """DROGA ROLKA HUMOR etap 3: kadry kluczowe scen (nano-banana-pro).
    Tomasz akceptuje OBRAZY zanim ruszy wideo. body: {"klipy":[2,3]} albo puste=wszystkie."""
    folder = ZARTY_DIR / zid
    if not (folder / "scenariusz.txt").is_file():
        raise HTTPException(status_code=404, detail="brak scenariusza")
    sc = (folder / "scenariusz.txt").read_text(encoding="utf-8")
    klipy = _parsuj(sc)
    chciane = set((data or {}).get("klipy") or [k["nr"] for k in klipy])
    from src.ai.image_backend import generate_image
    from src.zarty_produkcja import STYL_BOHATEROW, OPISY_POSTACI
    zrobione, bledy = [], []
    for k in klipy:
        if k["nr"] not in chciane or "(BANK)" in k.get("mowi", "").upper():
            continue
        out = folder / f"kadr_{k['nr']:02d}.jpg"
        w_kadrze = [im for im in OPISY_POSTACI
                    if im.lower() in k["ruch"].lower() or im.title() in k["ruch"]]
        opisy = " ".join(OPISY_POSTACI[im] for im in w_kadrze)
        prompt = (f"{STYL_BOHATEROW} {opisy} First frame of a scene, vertical 9:16, "
                  f"photorealistic golden-hour Polish allotment garden. Scene: {k['ruch']}")
        try:
            generate_image(prompt, out, silnik="fal-ai/nano-banana-pro")
            zrobione.append(k["nr"])
        except Exception as e:
            bledy.append({"klip": k["nr"], "blad": str(e)[:120]})
    _log(folder, f"kadry wygenerowane: {zrobione}" + (f", bledy: {bledy}" if bledy else ""))
    return {"status": "ok", "kadry": zrobione, "bledy": bledy,
            "podglad": [f"/zarty/{zid}/kadr/{n}" for n in zrobione]}


@router.post("/zart-checkpoint/{zid}/zwiad")
def zart_zwiad(zid: str, data: dict = Body(...)):
    """DROGA ROLKA HUMOR etap 4: zwiad ruchu jednego klipu na Veo LITE FLF 720p (~$0.40).
    Wymaga kadru. body: {"klip": 2}. Wynik: zwiad_NN.mp4 (nie rusza klipow)."""
    nr = int((data or {}).get("klip", 0))
    folder = ZARTY_DIR / zid
    kadr = folder / f"kadr_{nr:02d}.jpg"
    if not kadr.is_file():
        raise HTTPException(status_code=400, detail=f"brak kadru kadr_{nr:02d}.jpg — najpierw /kadry")
    sc = (folder / "scenariusz.txt").read_text(encoding="utf-8")
    k = next((x for x in _parsuj(sc) if x["nr"] == nr), None)
    if not k:
        raise HTTPException(status_code=404, detail="brak klipu w scenariuszu")

    def _tlo():
        try:
            from src.zarty_produkcja import _klip_flf
            out = folder / f"zwiad_{nr:02d}.mp4"
            _klip_flf(k, kadr, kadr, out, lite=True)
            _log(folder, f"ZWIAD klipu {nr} gotowy ({out.stat().st_size // 1024} KB) — obejrzyj ruch")
            try:
                m = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
                m["koszt_wydany"] = round(float(m.get("koszt_wydany", 0) or 0) + 0.40, 2)
                (folder / "meta.json").write_text(json.dumps(m, ensure_ascii=False, indent=1),
                                                  encoding="utf-8")
            except Exception:
                pass
        except Exception as e:
            _log(folder, f"BLAD ZWIADU {nr}: {e}")

    threading.Thread(target=_tlo, daemon=True).start()
    return {"status": "zwiad_ruszyl", "klip": nr, "koszt_ok_usd": 0.40}


@router.get("/zarty/{zid}/zwiad/{nr}")
def zart_zwiad_video(zid: str, nr: int):
    f = ZARTY_DIR / zid / f"zwiad_{nr:02d}.mp4"
    if not f.is_file():
        raise HTTPException(status_code=404, detail="brak zwiadu")
    return FileResponse(f, media_type="video/mp4", filename=f"zwiad_{zid}_{nr}.mp4")


@router.get("/zarty/{zid}/log")
def zart_log(zid: str):
    f = ZARTY_DIR / zid / "log.txt"
    meta_p = ZARTY_DIR / zid / "meta.json"
    return {"meta": json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.is_file() else {},
            "log": f.read_text(encoding="utf-8").splitlines()[-20:] if f.is_file() else []}


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
def zart_zatwierdz(zid: str, data: dict = Body(None)):
    """START PRODUKCJI (PŁATNE: klipy Veo wg wyceny z checkpointu). W tle."""
    import threading
    from src.zarty_produkcja import produkuj, KADR_GLOBALNY
    folder = ZARTY_DIR / zid
    if not folder.is_dir():
        raise HTTPException(status_code=404, detail="Żart nie znaleziony")
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    if meta.get("stan") not in ("checkpoint", "blad", "zamrozony"):
        raise HTTPException(status_code=400, detail=f"Zły stan: {meta.get('stan')}")
    force = bool((data or {}).get("force"))
    if meta.get("stan") == "zamrozony" and not force:
        raise HTTPException(status_code=409, detail={
            "blokada": "ODCINEK ZAMROZONY",
            "rada": "odmroz swiadomie: zatwierdz z {'force': true}"})
    # BEZPIECZNIK 1: audyt scen (zakazane akcje Veo)
    audyt = meta.get("audyt") or []
    if audyt and not force:
        raise HTTPException(status_code=409, detail={
            "blokada": "AUDYT SCENARIUSZA", "problemy": audyt,
            "rada": "popraw sceny (darmowe) albo force:true po swiadomej decyzji"})
    # BEZPIECZNIK 2: limit 6 USD na odcinek
    _sc = (folder / "scenariusz.txt").read_text(encoding="utf-8")
    _do_gen = [k for k in _parsuj(_sc)
               if not (folder / f"klip_{k['nr']:02d}.mp4").is_file()
               and "(BANK)" not in (k.get("mowi", "").upper())]
    plan = round(len(_do_gen) * 8 * CENA_SEK, 2)
    wydane = round(float(meta.get("koszt_wydany", 0) or 0), 2)
    if wydane + plan > 6.00 and not force:
        meta["stan"] = "zamrozony"
        (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
        raise HTTPException(status_code=409, detail={
            "blokada": "LIMIT 6 USD NA ODCINEK",
            "wydane_usd": wydane, "plan_usd": plan, "razem_usd": round(wydane + plan, 2),
            "rada": "odcinek zamrozony; force:true tylko po swiadomej decyzji"})
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
