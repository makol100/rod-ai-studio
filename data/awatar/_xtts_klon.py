import os
os.environ["COQUI_TOS_AGREED"] = "1"
from TTS.api import TTS
tekst = "Dzień dobry, witamy w najnowszym serwisie informacyjnym ROD Woźniki. Z tej strony wasz Działkowy Dziennikarz. Przypominam wszystkim działkowcom, że w najbliższą sobotę odbędzie się obowiązkowy odczyt liczników energii elektrycznej. Pogoda na jutro zapowiada się wspaniale, więc proszę wyciągać leżaki i obficie podlewać pomidory. Do usłyszenia przy płocie!"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
for matka in ["mykyta", "oleksa"]:
    tts.tts_to_file(text=tekst, speaker_wav=f"matka_uk_{matka}.wav", language="pl", file_path=f"probka_xtts_{matka}.wav")
    print(f"GOTOWE: probka_xtts_{matka}.wav", flush=True)
