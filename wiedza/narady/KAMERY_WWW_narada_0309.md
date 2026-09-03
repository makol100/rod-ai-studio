# NARADA 03.09.2026 — strona z kamerami ROD na zywo (glosy doslownie)


## ZENEK
Strona jest zbudowana i zwalidowana, ale celowo nie została opublikowana.

1. Gotowe pliki: [www_kamery](/root/rod-ai-studio/www_kamery), w tym [Caddyfile](/root/rod-ai-studio/www_kamery/Caddyfile) i [instrukcja wdrożenia](/root/rod-ai-studio/www_kamery/README.md).

2. Strona pokazuje jedną kamerę naraz, ma trzy selektory, pełny ekran, status LIVE, godzinę ostatniej klatki, komunikat utraty sygnału i układ mobilny. Używa MSE przez WSS/443.

3. Caddy dopuszcza wyłącznie trzy nazwy strumieni i potrzebne pliki. Pozostałe API oraz panel go2rtc zwracają 404. Dostęp jest przygotowany pod hasło.

4. Wyniki kontroli:

   - JavaScript: OK
   - HTML i CSS: OK
   - Caddy: `Valid configuration`
   - pliki HTTP: 200
   - bramka dowodowa: `PRZEPUSCIC`
   - snapshot go2rtc: awaria — przekroczony limit czasu, `0 bytes received`

5. Pełny research siedmiu stron, technika, obciążenie, WebRTC/LTE oraz rekomendacja prawna są zapisane w [zenek.txt](/tmp/n_kamery_www/zenek.txt). Publicznego obrazu parkingu nie rekomenduję: podgląd na żywo osób możliwych do identyfikacji jest przetwarzaniem danych, a publikacja w internecie wymaga osobnej podstawy prawnej. [UODO](https://uodo.gov.pl/pl/677/4283), [Wytyczne EROD 3/2019](https://uodo.gov.pl/art-docs/7358.pdf).

Teraz: Tomasz wybiera „pilotaż za hasłem”, następnie administrator uzupełnia trzy pola klauzuli RODO i montuje katalog strony do Caddy.

— Zenek


## HENIO
GŁOS HENIA — zapisany w całości do /tmp/n_kamery_www/henio.txt (183 linie). Tu treść:

## NAJWAŻNIEJSZE — STAN JEST INNY NIŻ W ZLECENIU

1. Klaudek pisze „3 strumienie NA ŻYWO". POMIAR: strumienie NIE dostarczają obrazu. Każde połączenie producenta ezviz kończy się w logu: `SRT data session did not start within 15s (device offline, blocked UDP/NAT, or channel 1 not streaming)`. Ten sam błąd 12.08, 18.08 i dziś 03.09 07:32–07:35. Zero udanego połączenia w całym dzienniku.
2. Ale chmura DZIAŁA: `GET /api/ezviz` zwraca 4 urządzenia „online" — FG0924766/802/072 (DS-2CDVT-CM-1B1K1M, 1 MP) + NVR FC0143848. Czyli login REST OK, sesja medialna P2P/SRT — nie startuje.
3. WNIOSEK: zanim powstanie strona, trzeba rozwiązać SRT. Bez tego strona pokaże 3 puste kafelki. Hipotezy: NAT routera ROD blokuje UDP hole-punch / kanal 1 nie streamuje / blokada UDP w firewallu chmurowym Hetzner. NIE WIEM która.

## TECHNIKA

1. go2rtc-hik: PID 113985, działa od 18.08, wersja 1.9.14+dev.1c84d99, nasłuchy WSZYSTKO na 127.0.0.1 (API :1984, RTSP :8554, WebRTC :8555) — nic nie wystaje, zostaje.
2. Kamery są H.265 (main 1280x720 20fps, sub 640x360 8fps — KUNY_MONITORING.md). Przeglądarki grają tylko H.264 → transkodowanie H.265→H.264 jest OBOWIĄZKOWE (internal/ezviz/README.md linie 73–96). go2rtc nie zrobi frame.jpeg z H.265 (0 bajtów) — potwierdzone dziś.
3. VPS: 12 CPU AMD EPYC, 23 451 MB RAM, swap 0. ffmpeg 8.0.1 + libx264 już jest. BRAK sprzętowego enkodera (/dev/dri/card1 = virtio-gpu) — tylko software libx264. NIC nie trzeba doinstalowywać.
4. Architektura: statyczny HTML+JS+CSS (Zenek), 3 strumienie transkodujące `ffmpeg:<nazwa>#video=h264#audio=copy` w go2rtc.yaml (kopia PRZED zmianą + systemctl restart), Caddy host kamery.* przepuszcza tylko / + /api/ws + /api/frame.jpeg, reszta go2rtc zamknięta.
5. Transport widza: WebRTC (UDP :8555) jest teraz na 127.0.0.1 i nie przejdzie przez Caddy — wymagałby otwarcia UDP 8555 + STUN/TURN i i tak może paść na LTE/NAT. MSE (WebSocket przez 443) działa ZAWSZE, bez UDP — to podstawowy tryb. HLS jako fallback dla starych iOS.
6. Limity Hik-Connect: w kodzie forka NIE MA limitu rate/strumieni (jedyne: paginacja limit=50, SRT timeout 15s, playbackIdle 10s). Media idzie P2P bezpośrednio, nie przez serwery chmury. Limit realny = uplink dzialki + ewentualny nieudokumentowany limit sesji konta.

## POMIAR OBCIĄŻENIA (wykonany, liczby prawdziwe)

1. 5 widzów MSE (40 s): 16,41 Mbps, 0 błędów. go2rtc średnio 2,9% CPU (max 4%), ffmpeg(copy) 0,7%.
2. 1 transkod H.265→H.264 720p superfast: średnio 30,2% jednego rdzenia (n=10), RSS 131 MB.
3. Wniosek: 3 kamery = ~0,9 rdzenia transkodu (koszt STAŁY, niezależny od widzów) + ~0,6% rdzenia/widza fan-out. 50 widzów = ~10% VPS. Wąskie gardło to NIE CPU, tylko uplink dzialki i egress VPS. Skrypty: /tmp/n_kamery_www/load_test.py, mse_viewers.py.

## BEZPIECZEŃSTWO / PRAWO (rekomendacja podpisana)

1. Wizerunek = dane osobowe (art. 4 RODO); publikacja nagrania to ODRĘBNE przetwarzanie wymagające własnej podstawy (art. 6). Publikacja bez zgody = poważne naruszenie (precedens UODO: nakaz usunięcia). Zasada minimalizacji (art. 5(1)(c)).
2. REKOMENDACJA: ZA HASŁEM (tylko członkowie), NIE publicznie. Ograniczony dostęp nie jest „upublicznieniem" i da się obronić art. 6(1)(f). Publiczny live = ryzyko nakazu + kary.
3. Niezależnie od hasła: fizyczna tablica przy bramie + klauzula art. 13 na stronie (administrator, cel, podstawa prawna, okres przechowywania, prawa, IOD, skarga do PUODO) — teksty Belzebub.
4. Decyzję i tak podejmuje Tomasz. Technicznie hasło nic nie kosztuje (wzorzec cookie panel_auth już jest w Caddyfile).

## JEDNA RZECZ DO ZROBIENIA

Rozwiązać SRT (bloker z pkt 1), zanim ktoś buduje stronę — np. test `subtype=sub` zamiast `main` albo diagnoza NAT routera ROD. Bez działającego strumienia strona będzie miała 3 puste kafelki; reszta (architektura, Caddy, klauzula) jest gotowa do zbudowania, ale nie ma czego wyświetlać.

-- Henio

## BELZEBUB
# GLOS BELZEBUBA 2.0 — doslownie, bez parafrazy (model huihui-ai/Huihui-Qwen3.8-27B-abliterated, narzedzia: web_search+fetch_page)

Belzebub: błąd API {'message': 'This model is busy, please try again later.', 'type': 'server_error', 'code': 'completion_error'}