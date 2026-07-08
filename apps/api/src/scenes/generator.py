"""
Generator scenariusza rolki (etap 1 pipeline'u Fabryki Rolek).

Zamienia surowy tekst/artykuł na scenariusz w formacie SCENA / UJĘCIE / LEKTOR.
Wyjście trafia do:
  - audio/generator.py   -> czyta linie "LEKTOR:" i robi edge-tts (pl-PL-MarekNeural)
  - images/prompts.py     -> liczy nagłówki "SCENA N:" i generuje prompty FLUX

WAŻNE (naprawiony bug): nagłówki są normalizowane do "SCENA N:" z dwukropkiem,
bo images/prompts.py liczy je regexem wymagającym dwukropka. Bez tego licznik
scen dawał 0 dopasowań i cichcem spadał do SCENE_COUNT, powodując rozjazd
liczby lektorów (audio) vs liczby promptów obrazu (render).

DWA WARIANTY PROMPTU (dodane 08.07.2026):
Kategorie tematów mają teraz kolumnę `tryb` (categories.tryb / topics.tryb_override):
  - "organizm"  -> bohaterem kadru jest roslina/grzyb/zwierze/warzywo (PROMPT_TEMPLATE_ORGANIZM)
  - "sprzet"    -> bohaterem kadru jest narzedzie/urzadzenie/dokument/infrastruktura (PROMPT_TEMPLATE_SPRZET)
Powod: jeden uniwersalny prompt na kategorie typu "Smart Ogrod"/"Bezpieczenstwo" dawal
powtorzone sceny (temat za krotki na wymagana liczbe scen przy zalozeniu "jeden punkt
= jedna scena") i gubil skroty techniczne (MPPT -> MPMT). Test porownawczy na starym
temacie roslinnym wyszedl czysto - to nie wada modelu, tylko niedopasowanie promptu.
generate_scenes() domyslnie uzywa "organizm" (kompatybilne wstecz z wywolaniami,
ktore jeszcze nie przekazuja trybu).
"""

from src.ai.ollama import generate
from src.config import SCENE_COUNT
import re


PROMPT_TEMPLATE_ORGANIZM = """
Jesteś scenarzystą krótkich, pionowych rolek (9:16) dla polskiego kanału o ogrodnictwie działkowym (ROD).
Widz to praktyczny działkowiec po pięćdziesiątce. Piszesz prosto, konkretnie, po polsku — bez lania wody.

Na podstawie poniższego tekstu napisz scenariusz złożony z DOKŁADNIE {scene_count} scen.

BUDOWA SCENARIUSZA:
- SCENA 1 to HACZYK: zaskocz, zadaj pytanie albo wytknij częsty błąd. Widz musi zostać w 1 sekundę.
- OSTATNIA scena to puenta i delikatne wezwanie, np.: "Zapisz, żeby nie zapomnieć." albo "Obserwuj po więcej porad z działki."
- SCENY POMIĘDZY: przejdź przez KONKRETNE punkty z tekstu (każde warzywo / każdą poradę) — po JEDNEJ scenie na punkt, w kolejności z tekstu. Nie pomijaj ważnych punktów i NIE dopychaj scenariusza powtórkami ani ogólnym "podlewajcie regularnie".

LEKTOR (tekst mówiony):
- Krótkie, naturalne zdania, 6-14 słów. Tak jak człowiek mówi do drugiego człowieka.
- TYLKO prawdziwe, poprawne polskie słowa. Nie wymyślaj słów ani terminów. Nie zmyślaj liczb ani nazw odmian.
- Jeśli tekst źródłowy zawiera skróty, kody lub łacińskie nazwy gatunkowe, przepisz je DOKŁADNIE litera w literę tak jak w tekście źródłowym.

UJĘCIE (opis jednego zdjęcia) — TU UWAŻAJ, to najczęstsze źródło błędów:
- Bohaterem kadru jest ROŚLINA lub WARZYWO, o którym mówi lektor. Pokaż samą roślinę: liście, owoc, warzywo w ziemi, grządkę.
- Realne, dokumentalne zdjęcie ogrodowe — takie, jakie zrobiłbyś telefonem na działce.
- ZAKAZANE w kadrze: przedmioty domowe i absurdy (zlew, kran, młynek, mikser, losowe sprzęty), narzędzia jako główny temat, dużo rąk i ludzi, dziwne lub nierealne sceny. Dłonie dopuszczalne wyjątkowo, ale nigdy jako bohater kadru.
- Każde UJĘCIE musi być INNE. Nie powtarzaj tego samego opisu (np. "liście i korzeń widoczne") w kolejnych scenach.
- Bez ruchu kamery, bez "przejście", bez tekstu ani logo na obrazie.

FORMAT WYJŚCIA (trzymaj się co do znaku):
SCENA 1:
UJĘCIE: ...
LEKTOR: ...

SCENA 2:
UJĘCIE: ...
LEKTOR: ...

...aż do SCENA {scene_count}:

Nie używaj markdown. Nie dodawaj wstępu, komentarzy ani podsumowania.
Nie pisz niczego przed "SCENA 1:" ani niczego po ostatniej scenie.
Zanim skończysz, po cichu sprawdź: (1) jest dokładnie {scene_count} scen, (2) żadne UJĘCIE się nie powtarza, (3) w kadrach nie ma zlewów, młynków ani przypadkowych przedmiotów.

Tekst:
{text}
""".strip()


PROMPT_TEMPLATE_SPRZET = """
Jesteś scenarzystą krótkich, pionowych rolek (9:16) dla polskiego kanału o ogrodnictwie działkowym (ROD) — w tym odcinku o sprzęcie, technice, infrastrukturze, prawie działkowym lub dokumentach.
Widz to praktyczny działkowiec po pięćdziesiątce. Piszesz prosto, konkretnie, po polsku — bez lania wody.

Na podstawie poniższego tekstu napisz scenariusz złożony z DOKŁADNIE {scene_count} scen.

BUDOWA SCENARIUSZA:
- SCENA 1 to HACZYK: zaskocz, zadaj pytanie albo wytknij częsty błąd/problem. Widz musi zostać w 1 sekundę.
- OSTATNIA scena to puenta i delikatne wezwanie, np.: "Zapisz, żeby nie zapomnieć." albo "Obserwuj po więcej porad z działki."
- SCENY POMIĘDZY: tekst źródłowy zwykle opisuje JEDEN przedmiot, urządzenie, dokument lub sytuację — nie listę wielu punktów. Rozbij ten JEDEN temat na różne kadry: najpierw całość z dystansu, potem kolejne zbliżenia na osobne elementy/detale/mechanizmy wymienione w tekście, ewentualnie krok procesu (montaż, pomiar, użycie) albo efekt/skutek. Jeśli tekst faktycznie wymienia kilka odrębnych rzeczy — jedna scena na rzecz, w kolejności z tekstu.

LEKTOR (tekst mówiony):
- Krótkie, naturalne zdania, 6-14 słów. Tak jak człowiek mówi do drugiego człowieka.
- TYLKO prawdziwe, poprawne polskie słowa. Nie wymyślaj słów ani terminów. Nie zmyślaj liczb ani nazw.
- Jeśli tekst źródłowy zawiera skróty, kody lub oznaczenia techniczne (np. MPPT, RCD, IP44, BMS, TN-S, Zigbee), przepisz je DOKŁADNIE litera w literę tak jak w tekście źródłowym. Nigdy nie zmieniaj ani nie zgaduj liter w skrócie.

UJĘCIE (opis jednego zdjęcia) — TU UWAŻAJ, to najczęstsze źródło błędów:
- Bohaterem kadru jest PRZEDMIOT, URZĄDZENIE, NARZĘDZIE, DOKUMENT lub ELEMENT INFRASTRUKTURY, o którym mówi lektor. To NIE jest błąd — w tym odcinku sprzęt/dokument MA być głównym bohaterem zdjęcia.
- Dłonie w trakcie pracy z przedmiotem (montaż, pomiar, dokręcanie, podpisywanie) są jak najbardziej pożądane i naturalne w kadrze.
- Realne, dokumentalne zdjęcie — takie, jakie zrobiłbyś telefonem na działce albo w warsztacie.
- ZAKAZANE w kadrze: przypadkowe, niezwiązane z tematem przedmioty w tle jako główny motyw, zbędne twarze/portrety osób, dziwne lub nierealne sceny, tekst ani logo na obrazie.
- Każde UJĘCIE musi być INNE — inny kadr, inny dystans (całość / zbliżenie / makro) albo inny element tego samego przedmiotu. Nie powtarzaj tego samego opisu w kolejnych scenach, nawet jeśli tekst źródłowy jest krótki — wymyśl nowy, wiarygodny kąt lub detal zamiast kopiować poprzednią scenę.
- Bez ruchu kamery, bez "przejście".

FORMAT WYJŚCIA (trzymaj się co do znaku):
SCENA 1:
UJĘCIE: ...
LEKTOR: ...

SCENA 2:
UJĘCIE: ...
LEKTOR: ...

...aż do SCENA {scene_count}:

Nie używaj markdown. Nie dodawaj wstępu, komentarzy ani podsumowania.
Nie pisz niczego przed "SCENA 1:" ani niczego po ostatniej scenie.
Zanim skończysz, po cichu sprawdź: (1) jest dokładnie {scene_count} scen, (2) żadne UJĘCIE się nie powtarza słowo w słowo, (3) wszystkie skróty techniczne są przepisane dokładnie jak w tekście źródłowym.

Tekst:
{text}
""".strip()


PROMPT_TEMPLATE_ORGANIZM_EN = """
You are a scriptwriter for short, vertical (9:16) reels for a Polish allotment-garden (ROD) channel.
The viewer is a practical gardener in their fifties. Write simply and concretely in ENGLISH -
this English version will be used directly for image generation, and the narration will be
translated to Polish in a separate later step. No filler.

Based on the text below, write a script made of EXACTLY {scene_count} scenes.

SCRIPT STRUCTURE:
- SCENE 1 is the HOOK: surprise the viewer, ask a question, or point out a common mistake.
- The LAST scene is the payoff and a gentle call to action, e.g. "Follow for more allotment tips."
- SCENES IN BETWEEN: go through the SPECIFIC points from the text (each plant / each tip) -
  ONE scene per point, in the order given in the text. Do not skip points, do not pad with
  repeats or generic filler like "water regularly".

NARRATOR (spoken line):
- Short, natural sentences, 6-14 words, the way one person talks to another.
- ONLY real, correct English words. Do not invent words, numbers, or variety names.
- If the source text contains abbreviations, codes, or Latin species names, copy them EXACTLY
  letter for letter as in the source text.

SHOT (description of one photo) - PAY ATTENTION HERE, this is the most common source of errors:
- The subject of the frame is the PLANT or VEGETABLE the narrator is talking about. Show the
  plant itself: leaves, fruit, vegetable in soil, garden bed.
- Real, documentary-style garden photo - the kind you'd take with a phone at an allotment.
- FORBIDDEN in frame: household objects and absurd items (sink, tap, blender, random appliances),
  tools as the main subject, lots of hands or people, strange or unrealistic scenes. Hands are
  acceptable occasionally, never as the subject.
- Every SHOT must be DIFFERENT. Do not repeat the same description across scenes.
- No camera movement, no "transition", no text or logo in the image.

OUTPUT FORMAT (follow exactly - KEEP these exact labels, even though the content is English):
SCENA 1:
UJĘCIE: ...
LEKTOR: ...

SCENA 2:
UJĘCIE: ...
LEKTOR: ...

...through SCENA {scene_count}:

Do not use markdown. Do not add an introduction, comments, or a summary.
Do not write anything before "SCENA 1:" or anything after the last scene.

Text:
{text}
""".strip()


# Alias wsteczny — gdyby cos jeszcze importowalo stara nazwe bezposrednio.
PROMPT_TEMPLATE = PROMPT_TEMPLATE_ORGANIZM

_TEMPLATES = {
    "organizm": PROMPT_TEMPLATE_ORGANIZM,
    "sprzet": PROMPT_TEMPLATE_SPRZET,
}


# Etykiety tolerują warianty gemma3:4b (ogonki, dwukropek/myślnik, wielkość liter).
_HEADER_RE = re.compile(r"^\s*scena\s*(\d+)\b", re.IGNORECASE)
_UJECIE_RE = re.compile(r"^\s*uj[eę]ci\w*\s*[:\-]\s*", re.IGNORECASE)
_LEKTOR_RE = re.compile(r"^\s*lekt[o]{1,2}r\w*\s*[:\-]\s*", re.IGNORECASE)
_COUNT_RE = re.compile(r"^SCENA\s+\d+:", re.IGNORECASE | re.MULTILINE)


def _normalize(raw: str) -> str:
    """Sprząta wyjście modelu do kanonicznego formatu SCENA N: / UJĘCIE: / LEKTOR:."""
    raw = re.sub(r"```[a-zA-Z]*", "", raw).replace("```", "").replace("**", "").strip()

    out = []
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            out.append("")
            continue
        # LEKTOR/UJĘCIE sprawdzamy PRZED nagłówkiem — treść lektora może zaczynać się od "Scena...".
        if _LEKTOR_RE.match(s):
            out.append("LEKTOR: " + _LEKTOR_RE.sub("", s).strip())
        elif _UJECIE_RE.match(s):
            out.append("UJĘCIE: " + _UJECIE_RE.sub("", s).strip())
        else:
            h = _HEADER_RE.match(s)
            if h:
                out.append(f"SCENA {int(h.group(1))}:")  # <-- naprawia rozjazd z images/prompts.py
            else:
                out.append(s)

    text = "\n".join(out)

    # Utnij wszystko przed pierwszą sceną (wstępy typu "Oto scenariusz:").
    first = _COUNT_RE.search(text)
    if first:
        text = text[first.start():]

    text = re.sub(r"\n{3,}", "\n\n", text)  # bez nadmiaru pustych linii
    return text.strip()


def _count(raw: str) -> int:
    return len(_COUNT_RE.findall(raw))


def generate_scenes(text: str, scene_count=None, tryb: str = "organizm") -> str:
    """
    Główna funkcja etapu 1. Zwraca surowy, znormalizowany scenariusz (string).

    scene_count (opcjonalny) — ile scen wygenerować. Gdy brak/niepoprawny,
    używa domyślnego SCENE_COUNT z config.py. Odporne na None, int i string.
    Przykład: zapowiedź na 5 scen, poradnik na 12.

    tryb — "organizm" (domyślnie, rośliny/grzyby/zwierzęta) albo "sprzet"
    (narzędzia/urządzenia/dokumenty/infrastruktura). Nieznana wartość -> "organizm".
    """
    try:
        sc = int(scene_count)
    except (TypeError, ValueError):
        sc = None
    count = sc if (sc and 1 <= sc <= 20) else SCENE_COUNT

    template = _TEMPLATES.get(tryb, PROMPT_TEMPLATE_ORGANIZM)
    prompt = template.format(scene_count=count, text=text)
    result = _normalize(generate(prompt))

    # Jeśli model kompletnie spudłował (0 scen), jedna próba naprawcza ze wzmocnieniem formatu.
    if _count(result) < count:
        retry = generate(
            prompt
            + "\n\nPRZYPOMNIENIE: Zacznij dokładnie od 'SCENA 1:' i w każdej scenie użyj etykiet 'UJĘCIE:' oraz 'LEKTOR:'."
        )
        result = _normalize(retry)

    return result


def generate_scenes_en(text: str, scene_count=None, tryb: str = "organizm") -> str:
    """Wariant generate_scenes() dla sciezki EN->PL v2 (Dyskusja 08.07.2026):
    Llama pisze scenariusz PO ANGIELSKU (etykiety SCENA/UJECIE/LEKTOR zostaja
    po polsku dla kompatybilnosci z parse_scenes/images/prompts/audio - tylko
    TRESC jest po angielsku). Celowo BEZ instrukcji "po cichu sprawdz" z
    polskich szablonow - to prawdopodobne zrodlo "### Ocena" wyciekajacego
    do widocznego wyjscia (znalezione przy budowie tej funkcji)."""
    from src.ai.ollama import generate, PROMPT_MODEL
    try:
        sc = int(scene_count)
    except (TypeError, ValueError):
        sc = None
    count = sc if (sc and 1 <= sc <= 20) else SCENE_COUNT

    prompt = PROMPT_TEMPLATE_ORGANIZM_EN.format(scene_count=count, text=text)
    result = _normalize(generate(prompt, model=PROMPT_MODEL))

    if _count(result) < count:
        retry = generate(
            prompt + '\n\nREMINDER: Start exactly with \'SCENA 1:\' and use the labels \'UJĘCIE:\' and \'LEKTOR:\' in every scene.',
            model=PROMPT_MODEL
        )
        result = _normalize(retry)

    return result


def parse_scenes(raw: str) -> list[dict]:
    """
    Zamienia scenariusz na strukture
    [{"scena": 1, "ujecie": "...", "lektor": "..."}, ...]

    Odporne na dwa warianty wyjscia modelu:
      UJĘCIE: tresc w tej samej linii
    oraz
      UJĘCIE:
      tresc w nastepnej linii (czasem nawet kilku)
    Kolejne linie bez wlasnej etykiety doklejane sa do ostatnio aktywnego pola,
    az do napotkania nowego naglowka SCENA/UJĘCIE/LEKTOR.
    """
    raw = _normalize(raw)
    scenes: list[dict] = []
    current: dict | None = None
    active_field: str | None = None  # "ujecie" albo "lektor"

    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        h = re.match(r"^SCENA\s+(\d+):", s, re.IGNORECASE)
        if h:
            if current:
                scenes.append(current)
            current = {"scena": int(h.group(1)), "ujecie": "", "lektor": ""}
            active_field = None
            continue
        if current is not None and s.upper().startswith("UJĘCIE:"):
            current["ujecie"] = s.split(":", 1)[1].strip()
            active_field = "ujecie"
        elif current is not None and s.upper().startswith("LEKTOR:"):
            current["lektor"] = s.split(":", 1)[1].strip()
            active_field = "lektor"
        elif current is not None and active_field:
            if current[active_field]:
                current[active_field] += " " + s
            else:
                current[active_field] = s

    if current:
        scenes.append(current)
    return scenes


def validate_scenario(scenes_text: str, requested_count=None) -> list:
    """Sprawdza scenariusz PRZED kosztownym etapem obrazow/audio (fal.ai).
    Zwraca liste twardych problemow - pusta lista = OK, mozna isc dalej.
    Ustalone w Dyskusji 08.07.2026 po awarii rolki 000061 (zdublowany
    scenariusz -> 18 obrazow zamiast 9, podwojny koszt).
    """
    import re
    problemy = []

    if re.search(r"<\|[a-z_]+\|>", scenes_text, re.IGNORECASE):
        problemy.append("wykryto zabladzony token specjalny modelu (np. <|...|>)")

    for wzorzec in ("### ocena", "spełnia wszystkie kryteria", "gotowy do realizacji", "gotowy do publikacji", "gotowa do realizacji"):
        if wzorzec in scenes_text.lower():
            problemy.append(f"wykryto komentarz metatekstowy modelu (znaleziono: '{wzorzec}')")
            break

    numery_scen = re.findall(r"SCENA\s+(\d+)", scenes_text, re.IGNORECASE)
    if len(numery_scen) != len(set(numery_scen)):
        problemy.append(f"powtorzone numery scen - scenariusz prawdopodobnie zdublowany (numery: {numery_scen})")

    if requested_count and len(set(numery_scen)) != requested_count:
        problemy.append(f"liczba unikalnych scen ({len(set(numery_scen))}) nie zgadza sie z zamowieniem ({requested_count})")

    # Identyczny tekst lektora w dwoch roznych scenach - tanie sprawdzenie,
    # bez nowego wywolania modelu. Zlapane przy tescie sciezki en_pl v2
    # (Dyskusja 08.07.2026): sceny 4 i 5 mialy dokladnie ten sam LEKTOR,
    # a has_repetition_loop() tego nie wykryl (to nie krotki powtarzajacy
    # sie fragment, tylko dwie CALE, identyczne, dluzsze linie).
    parsed = parse_scenes(scenes_text)
    lektory = [s["lektor"].strip().lower() for s in parsed if s.get("lektor", "").strip()]
    if len(lektory) != len(set(lektory)):
        problemy.append("identyczny tekst lektora powtorzony w dwoch roznych scenach")

    return problemy
