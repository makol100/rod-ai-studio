# JAK OBIEKTYWNIE ZMIERZYĆ KIERUNEK WZROKU NA OBRAZIE? Zenek — praktycy + rekomendacja.
KONTEKST: karta prezentera (start frame do Kling Avatar) musi patrzeć w obiektyw. Mały VLM (qwen2.5vl:7b) dał 3 SPRZECZNE pomiary kierunku źrenic na v1/v2. Potrzebujemy rozstrzygnięcia lepszego niż zgadywanie, zanim wydamy 4.64 USD na generację.
ZADANIE (bez wydawania centa, research + ocena wykonalności na VPS bez GPU):
1. PRAKTYCY: jakie sprawdzone metody oceny gaze na pojedynczym zdjęciu? (mediapipe iris? L2CS-Net? geometria: pozycja źrenicy względem kącików oczu? inne?) Co realnie działa i jest proste?
2. WYKONALNOŚĆ U NAS: co da się odpalić szybko na CPU (Python 3.14 w kontenerze lub host python3): instalacja, 10-linijkowy sposób użycia. Jeśli nic sensownego na CPU — powiedz wprost.
3. ALTERNATYWA PROCESOWA: jeśli automatyczny pomiar niepewny — jaki proces decyzyjny rekomendujesz? (np. ludzkie oko Tomasza jako sędzia + duży model multimodalny jako drugi głos)
4. RYZYKO: jeśli start frame patrzy minimalnie obok — jak bardzo to psuje wynik Kling Avatar wg praktyków?
Format: ## METODY / ## U NAS / ## PROCES / ## WERDYKT ZENKA. Zwięźle, ze źródłami.
