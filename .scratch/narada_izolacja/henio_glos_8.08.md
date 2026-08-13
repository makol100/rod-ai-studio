# GŁOS HENIA — OBRAZ kamer Xiaomi w HA Dzialki (8.08.2026 09:50 CEST)

## POTWIERDZONE (ze śladami z tej sesji)

1. **021a04 i 029a02 = CS2, działają z go2rtc.** Szukaj_net.py potwierdza: 021a04 "Mi 360 Home Security Camera 2K Pro", 029a02 "Mi 360 Home Security Camera 2K", oba CS2, kodek HEVC, audio PCMA, działają płynnie przez MSE. (Ślad: szukaj_net.py, zapytanie "go2rtc xiaomi provider CS2 021a04 029a02")

2. **ipc019 = legacy/TUTK, EOF.** Szukaj_net.py: "częściowo działa z dostawcą xiaomi, ale strumień kończy się błędem EOF. Sugeruje się, że ta kamera może należeć do starszej gałęzi Xiaomi legacy/TUTK". (Ślad: j.w.)

3. **go2rtc 1.9.14 bug CS2 i/o timeout — POTWIERDZONE.** Issues #2294 (Windows, C300, losowe timeouty) i #2048 (Mac arm64, CS2 zawsze timeout; v1.9.13 działa). (Ślad: szukaj_net.py, issues GitHub)

4. **go2rtc xiaomi:// config:** `xiaomi://USERID:REGION@IP?did=DID&model=MODEL` + sekcja `xiaomi: {USERID: "V1-token"}`. Token V1 = logowanie w go2rtc WebUI do konta Mi Home (automatyczne pobranie). (Ślad: szukaj_net.py)

5. **AlexxIT/hassio-addons = repozytorium społecznościowe** (NIE oficjalne HA), URL `https://github.com/AlexxIT/hassio-addons`, zawiera go2rtc. (Ślad: szukaj_net.py)

6. **go2rtc NIE zainstalowany na HA Działki** — port 1984 refused. (Ślad: TELEPORT_fabryka.md:2870, 2898)

7. **VPS NIE dosięga kamer:** .112 głucha na PING i portach 554/6668/8554/54321/5000. Router .0.1 z VPS ping OK. (Ślad: TELEPORT_fabryka.md:2905)

8. **tplinkrouterc6u — router Archer AX3000** rozpoznany jako TplinkRouterSG (nie V1_11, nie C80). authorize() nie działa poprawnie w tej sesji (Not authorised dla requestów, brak get_clients). get_wifi() z TplinkRouterV1_11 nie pokazuje AP isolation — tylko ssid/encryption/channel. (Ślad: terminal, 5 prób)

9. **MCP HA Działka niedostępny w sesji Henia** — narzędzia ha_* nie ładują się przez tool_search. Tylko Klaudek ma do nich dostęp w swojej sesji.

## HIPOTEZY

- **021a04/029a02 = CS2, transport domyślny (UDP → TCP fallback).** CS2 potwierdzone wyszukiwarką. Transport: go2rtc domyślnie próbuje UDP, fallback do TCP — nie ma potrzeby ręcznego ustawiania.
- **ipc019 prawdopodobnie BEZUŻYTECZNY** (EOF, legacy). Można próbować z `transport=tcp` i różnymi subtype, ale szansa mała.
- **025b02 (.121 "Kamera Furtka")** — nie sprawdzany wyszukiwarką. Prawdopodobnie też CS2 (chuangmi.camera.*), ale do potwierdzenia.
- **Brak odpowiedzi .112 z VPS ≠ client isolation.** Kamery Xiaomi nie muszą odpowiadać na ping ani mieć otwartych portów TCP. P2P/CS2 używa własnego protokołu UDP z hole-punchingiem, który nie wygląda jak standardowe usługi.
- **Router Działki może NIE mieć AP isolation.** TP-Link Archer AX3000 domyślnie NIE izoluje klientów. Izolacja to świadoma decyzja. Brak możliwości odczytu przez tplinkrouterc6u = trzeba sprawdzić w panelu WWW routera (albo przez MCP).
- **Najlepszy test: go2rtc addon w HA Działki.** To jednocześnie test łączności HA→kamera i przygotowanie środowiska docelowego.

## ODPOWIEDZI NA PYTANIA

### 1. Jak ZDIAGNOZOWAĆ czy kamery są dostępne z LAN Działki?

**Metoda A (NAJLEPSZA): go2rtc addon w HA Działki (host mode) + log.**
Instalujesz go2rtc 1.9.13 jako addon, dodajesz stream dla .112 (021a04), patrzysz w log:
- `i/o timeout` na IP kamery → NIE dosięga (izolacja/trasa)
- `unauthorized` / błąd autoryzacji → DOSIĘGA, problem z tokenem/kontem
- błąd CS2/negocjacji → DOSIĘGA, problem z protokołem
- obraz → DZIAŁA

**Metoda B (POMOCNICZA): HA integracja Xiaomi Miot Auto — dodaj kamerę po IP.**
Jeśli HA widzi encje kamery (nawet bez strumienia) = DOSIĘGA. Jeśli timeout = NIE dosięga (albo model nieobsługiwany).
Ale to test DRUGIEGO wyboru — Miot może iść przez chmurę.

**Metoda C: ODCZYT routera — panel WWW (ręcznie Tomasz) lub tplinkrouterc6u.**
W TP-Link Archer AX3000: Wireless → Wireless Settings → "AP Isolation" (checkbox).
Dziś tplinkrouterc6u NIE DAŁ RADY (authorize nie działa). Panel WWW = decyzja Tomasza.

**Metoda D (NIE DZIAŁA): ha_eval_template.** Szablony HA nie mają dostępu do sieci (potwierdzone: Zenek + dokumentacja HA).

### 2. GDZIE go2rtc? Addon vs docker vs supervisor?

**Repozytorium:** `https://github.com/AlexxIT/hassio-addons` (społecznościowe, nieoficjalne).
**Instalacja w HA Działki:**
1. Panel :8123 → Ustawienia → Dodatki → Sklep z dodatkami → ⋮ → Repozytoria → Dodaj URL
2. Zainstalować "go2rtc" z listy (NIE latest — **przypiąć wersję 1.9.13** jeśli addon na to pozwala)
3. Konfiguracja addonu: `network: host` (wymagane do łączności z kamerami w LAN)
4. Start → logi → test

**Przez MCP (gdy Klaudek ma dostęp):** `ha_manage_addon` — ale nie wiadomo czy potrafi DODAWAĆ repozytoria i instalować NOWE dodatki (Zenek słusznie to flaguje). Może tylko zarządzać istniejącymi.

**Alternatywa (jeśli addon nie zadziała):** docker bezpośrednio na HA Działki — ale SSH zamknięty, odpada.

### 3. Czy wyłączyć client isolation? Droga BEZ ruszania routera?

**Jeśli isolation POTWIERDZONE** (dwa dowody: log go2rtc timeout + odczyt routera):
- **BEZ zmiany routera NIE MA drogi.** go2rtc MUSI być w tym samym segmencie LAN co kamery. Żaden chmurowy bypass nie istnieje (go2rtc README: "connection to the camera is LOCAL ONLY", stream P2P bezpośrednio do IP kamery).
- Potrzebna DECYZJA TOMASZA (D-0066). Przedstawić dowody: log go2rtc + odczyt routera.
- Alternatywy (wszystkie wymagają zmiany/routera): (a) wyłączyć AP isolation na SSID kamer, (b) osobny AP/VLAN bez izolacji, (c) przełączyć HA na Ethernet (jeśli izolacja dotyczy tylko WiFi).

**Jeśli isolation NIEpotwierdzone** (go2rtc DOSIĘGA kamerę): problem był tylko z VPS (trasa Tailscale/VLAN). Idziemy dalej z konfiguracją.

### 4. Config go2rtc dla 021a04/029a02

```
# streams (go2rtc.yaml w addonie lub WebUI)
streams:
  dzialka_zachod:
    xiaomi://6338598787:de@192.168.0.112?did=1022085077&model=chuangmi.camera.021a04
  domek_srodek:
    xiaomi://6338598787:de@192.168.0.114?did=371002387&model=chuangmi.camera.029a02

# token konta (pobrany przez go2rtc WebUI)
xiaomi:
  "6338598787": "<V1-token-z-webui>"
```

- **CS2:** domyślny (go2rtc automatycznie negocjuje)
- **Transport:** domyślny UDP → TCP fallback (nie trzeba ustawiać)
- **Subtype:** brak (go2rtc nie używa subtype dla xiaomi://)
- **Token V1:** go2rtc WebUI → przycisk "Xiaomi Home" → logowanie do konta Mi → automatycznie pobiera V1 token. Może wymagać telefonu Tomasza (jak Extractor — zaufane urządzenie, bez captcha).
- **ipc019 (.127):** format ten sam, model=chuangmi.camera.ipc019. Może nie zadziałać (EOF). Jeśli timeout/EOF — prawdopodobnie bezużyteczny.
- **025b02 (.121):** format ten sam, model=chuangmi.camera.025b02. Do sprawdzenia.

### 5. PLAN krok po kroku (najniższy koszt)

**FAZA 0: ODCZYT (0 zł, nie wymaga zgód)**
1. [Klaudek] Sprawdzić panel HA Działki :8123 → czy można dodać repo AlexxIT i czy addon go2rtc jest dostępny.
2. [Klaudek] Sprawdzić co dokładnie potrafi `ha_manage_addon` — czy instalować nowe, czy tylko istniejące.
3. [Tomasz — jeśli chce] Zalogować się w panel routera 192.168.0.1 → Wireless → AP Isolation (checkbox). Tylko odczyt.

**FAZA 1: INSTALACJA go2rtc (0 zł, wymaga Klaudka + panel HA)**
4. Dodać repo AlexxIT w HA Działki.
5. Zainstalować go2rtc (1.9.13, NIE latest), `network: host`.
6. Uruchomić, sprawdzić WebUI :1984.

**FAZA 2: TOKEN V1 (wymaga Tomasza — telefon/logowanie)**
7. W go2rtc WebUI → "Xiaomi Home" → zalogować się kontem Mi Home Tomasza.
8. go2rtc automatycznie pobiera V1 token.
9. **Może zadziałać tylko z telefonu Tomasza** (zaufane urządzenie) — go2rtc WebUI przez przeglądarkę telefonu. Można otworzyć przez android_open_uri (Klaudek + connector Telefon Fold7).

**FAZA 3: TEST .112 (0 zł)**
10. Dodać stream dla .112 (021a04, CS2) w go2rtc.
11. Sprawdzić log — co mówi: timeout / auth error / CS2 error / stream OK.
12. Jeśli stream OK → obraz widoczny w WebUI :1984.

**FAZA 4: ROZSTRZYGNIĘCIE IZOLACJI**
13. Jeśli go2rtc timeout na IP .112:
    - Odczyt AP isolation w routerze (panel albo tplinkrouterc6u).
    - **Przedstawić Tomaszowi:** log go2rtc (dowód timeoutu) + odczyt routera (dowód izolacji).
    - **Decyzja Tomasza:** wyłączyć AP isolation na SSID kamer.
14. Jeśli go2rtc łączy się (auth error / CS2 error) → izolacji NIE MA, kontynuować.

**FAZA 5: POZOSTAŁE KAMERY**
15. .114 (029a02) — ta sama procedura, powinno zadziałać (CS2, potwierdzone).
16. .121 (025b02) — prawdopodobnie CS2, do testu.
17. .127 (ipc019) — ostatnia. Jeśli EOF → prawdopodobnie bezużyteczna (legacy/TUTK).

**FAZA 6: INTEGRACJA Z HA**
18. Dodać kamery jako generic camera w HA (RTSP/WebRTC z go2rtc).
19. Alternate: WebRTC Camera integration (AlexxIT) — natywnie współpracuje z go2rtc.

### Co wymaga Tomasza
- Logowanie do Mi Home w go2rtc WebUI (telefon, jak Extractor)
- Wyłączenie AP isolation na routerze (JEŚLI potwierdzone)
- Ewentualna wymiana/porzucenie ipc019

### Co NIE wymaga Tomasza (robi Klaudek)
- Dodanie repo AlexxIT w HA
- Instalacja go2rtc addon 1.9.13
- Konfiguracja streamów
- Test i analiza logów
- Integracja z HA po uzyskaniu obrazu

### Ryzyka
- **ipc019 (.127):** wysokie ryzyko FAIL (legacy/TUTK/EOF). Nastawić się, że może być bezużyteczna.
- **025b02 (.121):** średnie ryzyko (niepotwierdzony CS2).
- **Token V1:** go2rtc WebUI może wymagać telefonu Tomasza (zaufane IP/urządzenie) — ta sama bariera co Extractor.
- **go2rtc addon wersja:** może nie pozwolić na przypięcie 1.9.13 — wtedy ryzyko bugu 1.9.14 trzeba zaakceptować albo instalować ręcznie.
- **AP isolation:** może być wyłączone, a problem leży gdzie indziej (firewall kamery, VLAN).

## WNIOSEK HENIA

go2rtc 1.9.13 jako addon w HA Działki to NAJTAŃSZY i NAJSZYBSZY test. Dla 021a04/029a02 CS2 potwierdzone — powinny działać. ipc019 prawdopodobnie bezużyteczna.

Kluczowa niepewność: czy HA Działki dosięga kamer. Rozstrzygnie to DOPIERO log go2rtc. Nie zgadywać — testować.

Router odczytać (panel WWW przez Tomasza), NIE zmieniać bez zgody.
