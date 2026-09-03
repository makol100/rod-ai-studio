import sys, json
sys.path.insert(0, '/app')
from src.zarty_produkcja import ASS_HEADER, KOLORY_ASS
json.dump({"ASS_HEADER": ASS_HEADER, "KOLORY_ASS": KOLORY_ASS},
          open("/root/rod-ai-studio/data/zarty/10012/_stale.json", "w"))
print("stale zapisane:", list(KOLORY_ASS.keys()))
