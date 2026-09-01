# DROGA DOMOWA — jak fabryka czyta filmy z YouTube (17.08.2026)

**Dekret Tomasza:** "Kurwa szukać wszyscy narzędzi żeby przynajmniej Heniek widział
i słyszał YouTube". To jest odpowiedź: droga, która DZIAŁA i którą Henio może
uruchomić sam, bez telefonu Tomasza i bez oddawania konta Google.

## SEDNO

YouTube blokuje **adresy centrów danych**, nie nas. VPS Hetzner = centrum danych = blokada.
**HA Dom (Walding) ma adres domowy** — i YouTube go wpuszcza bez żadnego pytania.
Więc pobieramy tam, a plik przesyłamy na VPS przez tailnet.

DOWÓD (17.08.2026): film Szewczyka XTV-4f90Edg — z VPS niemożliwy przez cały dzień
(yt-dlp, youtube-transcript-api, 8 instancji Invidious, Piped, tactiq, TranscriptAPI.io
i .com — wszystko odbite). Z HA Dom: pobrany za pierwszym razem, 356 784 B napisów,
1066 linii tekstu. Zero kosztu.

## PRZEPIS (kroki, które działają)

### 1. Odbiornik na VPS
    python3 /tmp/odb.py &      # nasłuch na :8099, zapisuje do /tmp/odbior/
UWAGA: port 8000 jest ZAJĘTY przez fabryka-api (zwraca 422 i plik przepada). Używać 8099.

### 2. Pobranie na HA Dom + wysyłka (dodatek Advanced SSH jako ręce)
    ha_manage_addon(slug="a0d7b954_ssh", options={
      "packages": ["yt-dlp", "python3"],
      "init_commands": ["(cd /config/www/yt && yt-dlp --skip-download --write-auto-subs "
        "--write-subs --sub-langs 'pl,en' --sub-format vtt -o '%(id)s.%(ext)s' '<URL>' 2>&1 | tail -3; "
        "for f in *.vtt; do [ -f \"$f\" ] && curl -s -m 180 -F \"plik=@$f\" "
        "http://100.79.116.107:8099/upload; done) 2>&1; true"]})
    ha_manage_addon(slug="a0d7b954_ssh", action="restart")   # init_commands odpalają się przy starcie
    ha_get_logs(slug="a0d7b954_ssh", source="supervisor", search="...")  # tak się czyta wynik

### 3. Na VPS: VTT -> czysty tekst
    czyszczenie: wyrzucić nagłówki WEBVTT/Kind/Language, linie z "-->", numery,
    tagi <...>, oraz POWTÓRZONE linie (napisy automatyczne dublują każdą linię).

## PUŁAPKI (wszystkie nadepnięte 17.08, nie powtarzać)

1. **`/local/` nie serwuje tych plików** — `http://<ha>:8123/local/yt/plik.vtt` = 404,
   mimo że plik leży w `/config/www/yt/`. Dlatego wysyłka POST-em, nie pobieranie GET-em.
2. **`import cgi` nie istnieje** w Pythonie 3.13+ (usunięty). Odbiornik parsuje
   multipart ręcznie (regex na boundary) — patrz /tmp/odb.py.
3. **Port 8000 zajęty** przez fabryka-api → 422, plik przepada po cichu.
4. **`rm -f` w init_commands kasuje świeżo pobrany plik przy KOLEJNYM restarcie**
   — init_commands wykonują się przy każdym starcie dodatku. Nie kasować w tym samym
   poleceniu, w którym się pobiera.
5. **Nie każdy film ma napisy w każdym języku.** Film FEUyEfwX9gw (angielski) nie dał
   `pl` przy `--sub-langs 'pl'`. Podawać kilka: `'pl,en,en-orig'`.
6. **Logi dodatku są od najnowszego** — `ha_get_logs` zwraca `order: newest`, więc
   kolejność w odczycie bywa odwrotna do wykonania. Nie mylić przyczyny ze skutkiem.
7. **ZAKAZ (D-0098):** nie przełączać VPS na exit-node. Ta droga tego NIE wymaga —
   ruch wychodzi z HA Dom, VPS niczego nie przełącza.

## CO Z TEGO MA HENIO

Transkrypcja ląduje jako **plik na dysku fabryki** (`data/filmy/<id>/transkrypcja.txt`).
Henio czyta ją jak każdy inny dokument — nie potrzebuje ekranu, telefonu ani pośrednika.
To spełnia dekret: "żeby Heniek widział i słyszał YouTube".

## CZEGO TA DROGA NIE DAJE

- **Obrazu z filmu.** Napisy to tekst. Miniatury i storyboardy są publiczne i schodzą
  nawet z VPS (`i.ytimg.com/vi/<id>/maxresdefault.jpg` = 200, 282 kB — sprawdzone),
  ale klatki z wnętrza filmu wymagałyby pobrania wideo.
- **Filmów bez napisów.** Wtedy trzeba by pobrać dźwięk i rozpoznać mowę lokalnie
  (whisper na CPU) — niesprawdzone, osobny temat.
- **Automatyzacji.** Dziś to 3 ruchy ręczne. Do zrobienia: `tools/film.py --droga-domowa`,
  żeby to był jeden strzał.

## ODRZUCONE PO POMIARACH (nie wracać bez powodu)

- TranscriptAPI.io — klucz mamy, ale **5 z 6 filmów = HTTP 500**; działa wyłącznie na
  dQw4w9WgXcQ (prawdopodobnie cache). Praktycznie martwa.
- TranscriptAPI.com — 403 (error 1010) z naszego IP, przed uwierzytelnieniem.
- ClawLink — YouTube Data API nie daje napisów CUDZYCH filmów + oddanie OAuth do konta.
- Glasp — pod spodem to samo, co nam blokują; API nie zwraca transkrypcji.
- Invidious (8 instancji), Piped, tactiq, youtubetotranscript — puste/captcha/403/502.
