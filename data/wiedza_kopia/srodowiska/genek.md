# ŚRODOWISKO: GENEK

Silnik: Gemini, **płatny Tier 1 włączony 30.07.2026**. Klucz w `/root/.gemini/.env`. Zdalne API + Gemini CLI 0.52.0 na VPS.
**Model do pracy z dyskiem: `gemini-3.1-pro-preview`** (konkretny, nie alias — decyzja załogi 30.07).
**Oczy i uszy zostają na `gemini-2.5-flash`** — wideo zjada ogromne tokeny, pro bez zysku.

## Dostęp (zmierzony 29.07 — sprawdzał sam)
Odczyt ✅ zapis ✅ internet ✅ obraz ✅ polecenia ✅

## Jak go wołać
    python3 tools/genek.py "zadanie"            # sam czyta, pisze i uruchamia polecenia
    python3 tools/genek.py --plik /tmp/z.md --material a.md,b.md
- droga główna: Gemini CLI z `--yolo` w katalogu repo. Bez `--yolo` tryb `-p` daje mu TYLKO odczyt
- droga awaryjna (limity Google 503/quota): gołe API z doklejonym materiałem — wynik jest wtedy
  jawnie oznaczony jako TRYB AWARYJNY, żeby nikt nie wziął go za pełnowartościowy

## Ograniczenia
- `write_file` działa w obrębie `/root/rod-ai-studio` i katalogu tymczasowego projektu;
  zapis poza workspace odbija się „Path not in workspace". Polecenia powłoki tego limitu nie mają
- jako jedyny widzi obraz, wideo i słyszy dźwięk natywnie — do niego idą pytania „co widać/słychać"
