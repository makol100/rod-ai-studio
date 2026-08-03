# NARADA TRÓJKI — KRYTYCZNE zgłoszenie bramki B: k06 — widoczny Tomek mówi kwestię Józka

Rola: Zenek, pracownik. Protokół trójki + rozkaz Tomasza "Analizuj to z pracownikami!!! Zawsze!!!!". Nic nie zapisujesz na dysk; wynik na stdout, po polsku.

## Zgłoszenie Tomasza (bramka B, nadrzędna)
W klip_k06_reroll.mp4 widoczny mężczyzna pod drzewem (Tomek) WYPOWIADA puentę "To ja... Józek... niemowa ze wsi!" — rusza ustami — zamiast stać z zamkniętymi ustami, gdy kwestia pada z offu (z ukrytej korony). To zabija sedno żartu: niemowa ma przemówić Z KORONY.

## Fakty
1. Prompt k06 (data/zarty/10010/_klipy_reroll.json) mówił WPROST: "He does not speak. ... His face, mouth ... remain perfectly still." + "From high up in the hidden tree crown comes an off-screen voice ... crying out in Polish: [kwestia]". Veo to zignorowało i przypisało kwestię widocznej twarzy.
2. Strażnik języka (whisper) potwierdza, że kwestia PADŁA — ale nie sprawdza, KTO ją mówi. Tożsamość: to Tomek. Środek: poza trzyma. Żadna bramka nie łapie ust.
3. Wzorzec z wcześniejszych podejść: batchowy k06 dał głos 145 Hz (niski męski jak Tomek, zero pisku) — spójne z tym, że Veo od początku kładzie kwestię w usta widocznej postaci.
4. Znane z serii: Veo z natywnym audio lip-syncuje kwestię do widocznej twarzy (na tym stoi cała seria mówiących postaci) — to jego silny magnes.

## Zadania
1. **DIAGNOZA**: dlaczego Veo przypisuje off-screen kwestię widocznej twarzy mimo wprost zakazu; czy da się to w ogóle wiarygodnie wymusić promptem w veo3.1 lite FLF, czy off-screen dialog w tym narzędziu to loteria. Jeśli masz dostęp do sieci — sprawdź praktyków; jeśli nie — zaznacz to i bazuj na logice + znanych wzorcach.
2. **SKRYPT pomiaru ust ($0)**: kompletny Python (kontener, /app/venv/bin/python, insightface buffalo_l, ffmpeg pod /usr/bin/ffmpeg), który: wyciąga klatki 2/s z /root/rod-ai-studio/data/zarty/10010/klip_k06_reroll.mp4, dla każdej klatki mierzy ROZWARCIE UST widocznej twarzy (landmarki insightface — dystans warg znormalizowany wysokością twarzy), wypisuje tabelę czas→rozwarcie i WERDYKT: USTA PRACUJĄ (mówi) / USTA ZAMKNIĘTE. Ścieżki bezwzględne, zapis tylko do /tmp.
3. **PROPOZYCJE naprawy** (min. 3, z $; stawki: klip Veo lite $0.64, edycja kadru $0.15, montaż $0; budżet $11.09/12, zostało $0.91) — obowiązkowo rozważ wariant: **klip w pełni NIEMY z Veo (zero kwestii w prompcie) + głos Józka położony w MONTAŻU** (pisk robimy i tak deterministycznie pitch-upem; źródło audio: kwestia wycięta z obecnego k06_reroll albo z batchowego k06). Rekomendacja jednym zdaniem.
4. **PROJEKT bramki "KTO MÓWI"** na stałe: dla klipów z mówcą zza kadru — automatyczna kontrola zamkniętych ust widocznej postaci; opisz wejścia/wyjścia/próg, do wdrożenia po odcinku.

## Format wyniku
Sekcje: DIAGNOZA / SKRYPT (```python```) / PROPOZYCJE (z $) / BRAMKA-KTO-MÓWI.
