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
"""

from src.ai.ollama import generate
from src.config import SCENE_COUNT
import re


PROMPT_TEMPLATE = """
Jesteś scenarzystą krótkich, pionowych rolek (format 9:16) dla polskiego kanału o ogrodnictwie działkowym (ROD).
Widz to praktyczny działkowiec, często po pięćdziesiątce. Piszesz prosto, konkretnie i z sensem — bez lania wody.

Na podstawie poniższego tekstu napisz scenariusz złożony z DOKŁADNIE {scene_count} scen.

ZASADY TREŚCI:
- SCENA 1 to HACZYK. W pierwszym zdaniu zaskocz, zadaj pytanie albo wytknij częsty błąd. Widz musi zostać w ciągu 1 sekundy.
- Każda kolejna scena rozwija JEDNĄ myśl. Bez powtórzeń, bez ogólników, bez "dziś powiem wam o...".
- LEKTOR to tekst MÓWIONY: krótkie zdania, 6-14 słów, naturalny język. Tak jak człowiek mówi do drugiego człowieka.
- Trzymaj się faktów z tekstu. Nie zmyślaj liczb, nazw odmian ani terminów.
- Ostatnia scena to puenta i delikatne wezwanie, np.: "Zapisz, żeby nie zapomnieć." albo "Obserwuj po więcej porad z działki."

ZASADY UJĘCIA:
- UJĘCIE opisuje JEDNO realne, dokumentalne zdjęcie pasujące do tego, co mówi lektor w tej scenie.
- Opisuj to, co widać: roślinę, dłonie, glebę, narzędzie, objaw problemu. Konkret, nie ozdoby.
- Bez ruchu kamery, bez "przejście", bez tekstu na obrazie.

FORMAT WYJŚCIA (trzymaj się co do znaku):
SCENA 1:
UJĘCIE: ...
LEKTOR: ...

SCENA 2:
UJĘCIE: ...
LEKTOR: ...

...i tak dalej aż do SCENA {scene_count}:

Nie używaj markdown. Nie dodawaj wstępu, komentarzy ani podsumowania.
Nie pisz niczego przed "SCENA 1:" ani niczego po ostatniej scenie.
Zanim skończysz, po cichu sprawdź, że istnieją wszystkie sceny od 1 do {scene_count} i każda ma UJĘCIE oraz LEKTOR.

Tekst:
{text}
""".strip()


# Etykiety tolerują warianty gemma3:4b (ogonki, dwukropek/myślnik, wielkość liter).
_HEADER_RE = re.compile(r"^\s*scena\s*(\d+)\b", re.IGNORECASE)
_UJECIE_RE = re.compile(r"^\s*uj[eę]cie\s*[:\-]\s*", re.IGNORECASE)
_LEKTOR_RE = re.compile(r"^\s*lektor\s*[:\-]\s*", re.IGNORECASE)
_COUNT_RE = re.compile(r"^SCENA\s+\d+:", re.IGNORECASE | re.MULTILINE)


def _normalize(raw: str) -> str:
    """Sprząta wyjście modelu do kanonicznego formatu SCENA N: / UJĘCIE: / LEKTOR:."""
    raw = re.sub(r"```[a-zA-Z]*", "", raw).replace("```", "").strip()

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


def generate_scenes(text: str, scene_count=None) -> str:
    """
    Główna funkcja etapu 1. Zwraca surowy, znormalizowany scenariusz (string).

    scene_count (opcjonalny) — ile scen wygenerować. Gdy brak/niepoprawny,
    używa domyślnego SCENE_COUNT z config.py. Odporne na None, int i string.
    Przykład: zapowiedź na 5 scen, poradnik na 12.
    """
    try:
        sc = int(scene_count)
    except (TypeError, ValueError):
        sc = None
    count = sc if (sc and 1 <= sc <= 20) else SCENE_COUNT

    prompt = PROMPT_TEMPLATE.format(scene_count=count, text=text)
    result = _normalize(generate(prompt))

    # Jeśli model kompletnie spudłował (0 scen), jedna próba naprawcza ze wzmocnieniem formatu.
    if _count(result) == 0:
        retry = generate(
            prompt
            + "\n\nPRZYPOMNIENIE: Zacznij dokładnie od 'SCENA 1:' i w każdej scenie użyj etykiet 'UJĘCIE:' oraz 'LEKTOR:'."
        )
        result = _normalize(retry)

    return result


def parse_scenes(raw: str) -> list[dict]:
    """
    Bonus na przyszłość: zamienia scenariusz na strukturę
    [{"scena": 1, "ujecie": "...", "lektor": "..."}, ...]
    Gotowe pod strukturalny endpoint /generate-script zwracający JSON.
    """
    raw = _normalize(raw)
    scenes: list[dict] = []
    current: dict | None = None

    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        h = re.match(r"^SCENA\s+(\d+):", s, re.IGNORECASE)
        if h:
            if current:
                scenes.append(current)
            current = {"scena": int(h.group(1)), "ujecie": "", "lektor": ""}
        elif current is not None and s.upper().startswith("UJĘCIE:"):
            current["ujecie"] = s.split(":", 1)[1].strip()
        elif current is not None and s.upper().startswith("LEKTOR:"):
            current["lektor"] = s.split(":", 1)[1].strip()

    if current:
        scenes.append(current)
    return scenes
