import sys, difflib, re, subprocess
sys.path.insert(0,'/app')
from faster_whisper import WhisperModel
nazwa = sys.argv[1]
import importlib.util as _u; _s=_u.spec_from_file_location('k','/root/rod-ai-studio/data/wiadomosci/tauron_apki/omni/KWESTIE.py'); _m=_u.module_from_spec(_s); _s.loader.exec_module(_m); KW=_m.KWESTIE
_STARE = {"K1":"Dzień dobry, tu Tomasz. Kable w górnej alejce są położone i zasypane. Teraz do dwóch tygodni dajemy czas na uleżenie gleby i kabla.",
      "K2":"Potem podłączymy kable do poszczególnych zabezpieczonych miejsc licznikowych, przypisanych do danej działki.",
      "K4":"Z tym pismem przychodzą Państwo do zarządu, do mnie — Tomasza Maksysia. Wydam kartę danych technicznych, w skrócie ka-de-te."}
p = f"/root/rod-ai-studio/data/wiadomosci/tauron_apki/omni/omni_{nazwa}.mp4"
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, info = m.transcribe(p, language="pl", word_timestamps=True); segs = list(segs)
txt = " ".join(s.text.strip() for s in segs)
norm = lambda s: re.sub(r"[^\wąćęłńóśźż ]", "", s.lower()).split()
a, b = norm(KW[nazwa]), norm(txt)
ratio = difflib.SequenceMatcher(None, a, b).ratio()
ost = max((w.end for s in segs for w in (s.words or [])), default=0)
print(f"WHISPER [{nazwa}]: {txt}")
print(f"slowa kanon={len(a)} whisper={len(b)} podobienstwo={ratio:.2f} | ostatnie slowo konczy sie {ost:.2f}s | brakuje: {[w for w in a if w not in b]}")
