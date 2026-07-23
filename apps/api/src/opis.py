"""
Generator OPISU do publikacji (Facebook / Shorts) — z gotowego scenariusza rolki.

Bielik uparcie dokleja etykiety ("Haczyk:", "Konkrety:", "Hasztagi:") mimo zakazu w prompcie.
Dlatego nie ufamy instrukcji — sprzątamy wynik siłą, po fakcie.
"""
import os
import re
import unicodedata
from src.ai.ollama import generate

REELS = "/root/rod-ai-studio/data/reels"
OBOWIAZKOWE = ["#ROD", "#działka", "#ogróddziałkowy"]

PROMPT_OPIS = """
Jesteś polskim twórcą treści. Piszesz opis pod rolkę na Facebooka dla działkowców.

Poniżej masz teksty lektora z gotowej rolki. Napisz na ich podstawie opis do posta.

ZASADY:
- Pierwsze zdanie to HACZYK. Ma zatrzymać przewijanie: zaskoczeniem, pytaniem albo
  obaleniem tego, w co ludzie wierzą.
- Potem 3-5 krótkich akapitów z konkretami. Bez lania wody.
- Piszesz do widza wprost, na "Ty". Żywa polszczyzna, krótkie zdania.
- Zero kalk z angielskiego, zero encyklopedycznego tonu.
- Nie wymyślaj faktów, których nie ma w tekstach lektora.
- Na końcu jedno pytanie do czytelnika, żeby zostawił komentarz.

PISZ SAM GOTOWY TEKST POSTA.
Nie pisz etykiet ani nagłówków. Żadnego "Haczyk:", "Konkrety:", "Hasztagi:", "Opis:".
Nie dodawaj hasztagów — dopiszemy je sami.

TEKSTY LEKTORA:
{scenariusz}
"""


def _scenariusz(reel_id: str) -> str:
    p = os.path.join(REELS, reel_id, "scenes.txt")
    if not os.path.exists(p):
        raise FileNotFoundError(f"brak scenes.txt dla rolki {reel_id}")
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read().strip()


def _tylko_lektor(txt: str) -> str:
    linie = [l.split(":", 1)[1].strip().strip('"')
             for l in txt.split("\n") if l.strip().upper().startswith("LEKTOR")]
    return "\n".join(f"- {l}" for l in linie)


def _bez_ogonkow(s: str) -> str:
    """dzialka == działka — do porównywania hasztagów"""
    return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(c) != "Mn").replace("ł", "l")


def _sprzataj(t: str) -> str:
    # 1) etykiety na początku linii — usuwamy SAM PREFIKS, treść zostaje
    t = re.sub(r'^[ \t]*(haczyk|hook|opis|post|wstęp|wstep)[ \t]*:[ \t]*',
               '', t, flags=re.I | re.M)
    t = re.sub(r'^[ \t]*(pytanie do czytelnika|pytanie|cta)[ \t]*:[ \t]*',
               '', t, flags=re.I | re.M)
    # 2) linie, które są SAMĄ etykietą — kasujemy w całości
    t = re.sub(r'^[ \t]*(konkrety|punkty|treść|tresc|rozwinięcie|rozwiniecie)[ \t]*:?[ \t]*$',
               '', t, flags=re.I | re.M)
    # 3) linia z hasztagami od Bielika — kasujemy, dopiszemy własne
    t = re.sub(r'^[ \t]*hasztagi[ \t]*:.*$', '', t, flags=re.I | re.M)
    # 4) grzecznościowe wstępy
    t = re.sub(r'^(oto|oczywiście|jasne|proszę)[^\n]*\n+', '', t, flags=re.I).strip()
    # 5) markdown i nadmiar pustych linii
    t = t.replace("**", "").replace("##", "")
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()


def generuj_opis(reel_id: str) -> dict:
    lektor = _tylko_lektor(_scenariusz(reel_id))
    tekst = generate(PROMPT_OPIS.format(scenariusz=lektor), temperature=0.7, max_tokens=900)
    tekst = _sprzataj(tekst.strip())

    # hasztagi: zbierz, odfiltruj duplikaty (dzialka == działka), dołóż obowiązkowe
    znalezione = re.findall(r"#[\w\u0080-\uFFFF]+", tekst)
    tekst = re.sub(r'(\s*#[\w\u0080-\uFFFF]+)+\s*$', '', tekst).rstrip()

    finalne, widziane = [], set()
    for h in OBOWIAZKOWE + znalezione:
        k = _bez_ogonkow(h)
        if k not in widziane:
            widziane.add(k)
            finalne.append(h)

    tekst = tekst + "\n\n" + " ".join(finalne[:7])
    return {"id": reel_id, "opis": tekst, "hasztagi": finalne[:7], "znakow": len(tekst)}
