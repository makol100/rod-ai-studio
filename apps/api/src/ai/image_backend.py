from pathlib import Path
import requests
import fal_client

# Model i limity — dobrane pod FLUX schnell (szybki) na fal.ai.
# ZMIENIONE 09.07.2026 na wyrazne zyczenie Tomasza: FLUX.2 [max], najmocniejszy
# wariant rodziny FLUX.2 (najwyzsza wiernosc wg Black Forest Labs). Decyzja
# podjeta SWIADOMIE mimo wczesniej znalezionych zglaszanych przez userow
# problemow z anatomia (dlonie/konczyny) w calej rodzinie FLUX.2 - Tomasz
# potwierdzil dwukrotnie (najpierw ogolnie, potem przy wyborze wariantu) ze
# chce to mimo tego ryzyka.
FAL_MODEL = "fal-ai/flux-2-max"
# Nano Banana Pro / Gemini 3 Pro Image (Dyskusja 09.07.2026, na zyczenie
# Tomasza po serii nieudanych prob z FLUX.2 - 80% obrazow do wymiany w
# rolce 000084, mimo identycznego promptu porownawczo wygenerowanego przez
# Tomasza w Gemini "recznie"). To PELNY model jezykowy (Gemini 3 Pro) z
# wbudowanym rozumowaniem PRZED narysowaniem obrazu, nie czysty dyfuzyjny
# model jak FLUX - stad inne podejscie do promptu (patrz zbuduj_konteksty_gemini
# w images/prompts.py). Cena $0.15/obraz (fal.ai) - drozej niz FLUX.2 [max]
# ($0.07), ale Tomasz swiadomie akceptuje ten koszt po utracie wiary w FLUX
# dla tego konkretnego, technicznie wymagajacego tematu (rozdzielnica
# elektryczna). Rolka 000085 potwierdzila ze dziala dobrze w produkcji.
FAL_MODEL_NANO_BANANA_PRO = "fal-ai/nano-banana-pro"
FAL_TIMEOUT = 90          # maks. czas generowania jednego obrazu (s)
FAL_START_TIMEOUT = 60    # maks. czas oczekiwania w kolejce fal (s)
DOWNLOAD_TIMEOUT = 120    # maks. czas pobrania gotowego JPG (s)
RETRIES = 1               # ile dodatkowych prób po pierwszym błędzie


def generate_image(prompt: str, output: Path, silnik: str = None):
    """
    Generuje jeden obraz i zapisuje go do `output`.

    W przeciwieństwie do wersji poprzedniej NIE rzuca wyjątku przy błędzie —
    zwraca {"status": "error", ...}. Dzięki temu pojedynczy zły obraz nie
    wywala całego renderu, a renderer (parujący po numerze pliku) po prostu
    pominie brakującą klatkę.

    silnik -- opcjonalnie wymusza konkretny model fal.ai (np.
    FAL_MODEL_NANO_BANANA_PRO) zamiast domyslnego FAL_MODEL. Dodane
    09.07.2026 - Tomasz stracil zaufanie do FLUX.2 po 80% odrzuconych
    obrazow w rolce 000084 (identyczny prompt, Nano Banana Pro dal
    realistyczny wynik, FLUX plytka atrapa).

    USUNIETE 10.07.2026 (na wyrazne polecenie Tomasza): funkcja "referencje"
    (zdjecia wgrywane recznie na checkpoincie, uzywajace FLUX.1 Kontext
    [pro] multi) - Tomasz przestal uzywac FLUX-a calkowicie (przeszedl na
    Nano Banana Pro), wiec ta sciezka stala sie martwa. Usunieto tez
    endpointy /reel-checkpoint/{id}/referencje/{scena} (topics.py),
    _znajdz_referencje() (pipeline.py) i UI wgrywania w panel.html.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    last_err = None

    uzyty_model = silnik or FAL_MODEL

    arguments = {"prompt": prompt}
    if uzyty_model == FAL_MODEL_NANO_BANANA_PRO:
        # Nano Banana Pro ma inny ksztalt API niz FLUX - "aspect_ratio"
        # (string), nie "image_size" (enum FLUX-a).
        arguments["aspect_ratio"] = "9:16"
    else:
        arguments["image_size"] = "portrait_16_9"

    for attempt in range(1, RETRIES + 2):  # domyślnie próby 1 i 2
        try:
            result = fal_client.run(
                uzyty_model,
                arguments=arguments,
                timeout=FAL_TIMEOUT,
                start_timeout=FAL_START_TIMEOUT,
            )

            url = result["images"][0]["url"]

            r = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
            r.raise_for_status()
            output.write_bytes(r.content)

            return {
                "status": "ok",
                "prompt": prompt,
                "output": str(output),
                "url": url,
                "attempts": attempt,
                "model": uzyty_model,
            }

        except Exception as e:
            last_err = e
            print(f"[image] proba {attempt} nieudana dla {output.name}: {e}", flush=True)

    return {
        "status": "error",
        "prompt": prompt,
        "output": str(output),
        "error": str(last_err),
    }
