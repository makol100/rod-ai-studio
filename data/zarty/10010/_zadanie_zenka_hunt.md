# WYKONALNOŚĆ NA VPS — którą drogę pobrania udźwigniemy
Zenek: oceń techniczną wykonalność na NASZYM VPS (Linux, CPU-only bez GPU, RAM 19G wolne, dysk 95G, Python 3.11 venv w kontenerze, ffmpeg z rubberband, docker; instalacje pip/npm/apt dozwolone) dla dróg zmiany CHARAKTERU głosu (words+prozodia zostają z naszego nagrania):
(a) RVC v2 (Retrieval-based Voice Conversion) inference na CPU — realny czas dla 6 s audio? co instalować (repo, zależności), pułapki;
(b) praat (phonetics tool) — skrypty manipulacji: pitch floor/jitter/shimmer/formant shift dla efektu "duszonego" — czy da naturalniejszy efekt niż nasz ffmpeg, przykładowy skrypt;
(c) world vocoder / soundtouch / inne lekkie CPU narzędzia warte uwagi;
(d) so-vits-svc — czy w ogóle rozważać na CPU.
WYNIK: ## MACIERZ (droga | instalacja min | czas dla 6s na CPU | ryzyko | werdykt TAK/NIE) / ## NAJLEPSZA DROGA (1 zdanie) / ## KOMENDY instalacji dla najlepszej. Po polsku. Na końcu przypomnij prowadzącemu o naradzie, zapisach i praktykach.
