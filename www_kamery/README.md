# Kamery ROD — kandydat wdrożeniowy

Stan: pliki strony są gotowe, ale host nie został dopisany do aktywnego Caddyfile i Caddy nie został przeładowany.

## Przyjęta architektura

1. Jedna aktywna kamera naraz; wybór następnej natychmiast zamyka poprzedniego konsumenta.
2. MSE po WebSocket `/api/ws` przez HTTPS/443; brak zależności od WebRTC/8555 i NAT widza.
3. Tylko trzy jawne wartości `src` przechodzą do go2rtc; `/api/streams`, panel, konfiguracja i pozostałe API zwracają 404.
4. Trzy pliki odtwarzacza go2rtc są przepuszczone jako statyczne zasoby strony; pozostałe UI go2rtc jest zamknięte.
5. Dostęp domyślnie chroni `basic_auth`; dane logowania mają trafić do zmiennych kontenera, nie do repozytorium.

## Brakujące dane i decyzje przed publikacją

1. Tomasz wybiera dostęp: rekomendowany pilotaż za hasłem dla członków; wariant publiczny wymaga osobnej oceny prawnej kadrów i podstawy publikacji.
2. Administrator uzupełnia pełną nazwę, adres, kontakt, podstawę prawną, okres przechowywania, odbiorców i prawa osób w `index.html`.
3. Zarząd potwierdza tablice informacyjne przed wejściem w obszar kamer i zakres każdego kadru.
4. Do kontenera Caddy trzeba dodać montowanie `/root/rod-ai-studio/www_kamery:/srv/www_kamery:ro`.
5. Po kopii aktywnego Caddyfile dopisać blok hosta, uruchomić `caddy validate`, dopiero potem `caddy reload`.

## Walidacja kandydata bez wdrożenia

Wartości są przykładowe tylko dla walidacji składni:

```bash
HASH=$(docker exec caddy-mcp caddy hash-password --plaintext 'test-only')
docker run --rm \
  -e KAMERY_USER=test \
  -e KAMERY_PASSWORD_HASH="$HASH" \
  -v /root/rod-ai-studio/www_kamery/Caddyfile:/etc/caddy/Caddyfile:ro \
  caddy:2.11.4 caddy validate --config /etc/caddy/Caddyfile
```

Po wdrożeniu sprawdzić z internetu: strona żąda hasła, poprawne konto otwiera widok, trzy nazwy kamer działają, a `/api/streams`, `/config.html` i `/api/ws?src=nieznany` zwracają 404.
