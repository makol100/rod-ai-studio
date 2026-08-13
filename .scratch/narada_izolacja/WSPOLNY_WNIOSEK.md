# WSPÓLNY WNIOSEK (Zenek + Henio): OBRAZ kamer Xiaomi w HA Dzialki
# 8.08.2026 ~09:50 CEST

## ZGODNE (oba głosy)

1. **go2rtc addon 1.9.13 w HA Dzialki (host mode) = NAJLEPSZY test.**
   Jednocześnie sprawdza łączność HA→kamera i przygotowuje środowisko docelowe.

2. **ha_eval_template NIE DAJE RADY** do testów sieciowych. Szablony HA nie mają dostępu do ping/socketów/TCP.

3. **Router — TYLKO ODCZYT, NIE zmieniać** bez zgody Tomasza (D-0066).
   Odczyt AP isolation przez panel WWW (ręcznie Tomasz) lub tplinkrouterc6u (gdy działa).

4. **VPS bezużyteczny** — go2rtc MUSI być w LAN Działki. go2rtc xiaomi:// to P2P lokalne.

5. **Kolejność: odczyt → instalacja go2rtc → test .112 → log rozstrzyga → decyzja o routerze.**

6. **Miot integracja = test POMOCNICZY**, nie zastępuje go2rtc.

7. **Token V1 = go2rtc WebUI**, logowanie do Mi Home (może wymagać telefonu Tomasza — zaufane urządzenie).

## RÓŻNICE (rozstrzyga Tomasz)

| Temat | Zenek | Henio |
|---|---|---|
| 021a04/029a02 = CS2? | Hipoteza (niepotwierdzone) | POTWIERDZONE (szukaj_net.py) |
| ipc019 (.127) | Nie poruszał | POTWIERDZONE legacy/TUTK/EOF — prawdopodobnie bezużyteczna |
| go2rtc config | Trzeba sprawdzić w dokumentacji | Składnia POTWIERDZONA: `xiaomi://USERID:REGION@IP?did=DID&model=MODEL` + `xiaomi: {USERID: "V1-token"}` |
| Transport UDP/TCP | Nie zgadywać | CS2 = domyślny (UDP → TCP fallback), nie trzeba ustawiać |
| "Host mode" addonu | Sprawdzić manifest, nie wierzyć na słowo | Host mode wymagany (musi dosięgać kamer w LAN) |

## PLAN (wspólny, krok po kroku)

### Faza 0: ODCZYT (0 zł)
1. **[Klaudek]** Panel HA Działki :8123 → Sklep z dodatkami → czy można dodać repo `https://github.com/AlexxIT/hassio-addons`
2. **[Klaudek]** Sprawdzić możliwości `ha_manage_addon` (czy instaluje nowe dodatki)
3. **[Tomasz — opcjonalnie]** Panel routera 192.168.0.1 → Wireless → sprawdzić "AP Isolation"

### Faza 1: INSTALACJA go2rtc (0 zł)
4. Dodać repo AlexxIT w HA Działki
5. Zainstalować go2rtc **1.9.13** (NIE latest — bug CS2 w 1.9.14, issues #2294/#2048)
6. Konfiguracja: `network: host`
7. Uruchomić, sprawdzić WebUI na :1984

### Faza 2: TOKEN (wymaga Tomasza)
8. go2rtc WebUI → "Xiaomi Home" → zalogować konto Mi Home
9. WebUI automatycznie pobiera V1 token
10. Może wymagać zaufanego urządzenia (telefon Tomasza) — jak Extractor

### Faza 3: TEST .112 (021a04, CS2)
11. Dodać stream:
    ```
    xiaomi://6338598787:de@192.168.0.112?did=1022085077&model=chuangmi.camera.021a04
    ```
12. Log rozstrzyga:
    - **timeout** → NIE dosięga (izolacja/trasa) → Faza 4
    - **auth error** → DOSIĘGA, poprawić token → Faza 3 dalej
    - **CS2/negotiation error** → DOSIĘGA, problem protokołu → próbować `transport=tcp`
    - **obraz** → DZIAŁA → Faza 5

### Faza 4: IZOLACJA (jeśli timeout)
13. Odczyt routera (AP isolation) — panel WWW
14. **Meldunek do Tomasza:** log go2rtc (dowód timeoutu) + odczyt routera → DECYZJA
15. Po zgodzie: wyłączyć AP isolation → powtórzyć test

### Faza 5: POZOSTAŁE KAMERY
16. .114 (029a02): format j.w., did=371002387. CS2 potwierdzone — powinno działać.
17. .121 (025b02): did=448715358. Prawdopodobnie CS2, do sprawdzenia.
18. .127 (ipc019): did=323183877. **Wysokie ryzyko FAIL** (legacy/TUTK/EOF). Testować ostatnią.

### Faza 6: INTEGRACJA Z HA
19. Generic Camera lub WebRTC Camera (AlexxIT) → RTSP/WebRTC z go2rtc
20. Encje `camera.*` widoczne w HA

## CO WYMAGA TOMASZA
- Logowanie Mi Home w go2rtc WebUI (telefon, zaufane urządzenie)
- Wyłączenie AP isolation na routerze (JEŚLI timeout w logu go2rtc + isolation włączone)
- Decyzja o ipc019 (może być bezużyteczna)

## CO NIE WYMAGA TOMASZA (robi Klaudek)
- Dodanie repo AlexxIT, instalacja go2rtc 1.9.13
- Konfiguracja streamów, test, analiza logów
- Integracja z HA po uzyskaniu obrazu

## RYZYKA (wspólne)
1. **ipc019 legacy** — prawdopodobnie nie zadziała (EOF). Alternatywa: podmiana kamery.
2. **Token V1** — go2rtc WebUI może mieć tę samą barierę co Extractor (captcha dla VPS, tylko telefon działa). Klaudek może otworzyć WebUI na telefonie Tomasza przez android_open_uri.
3. **go2rtc bez możliwości przypięcia 1.9.13** — jeśli addon zmusza do latest, zaakceptować ryzyko bugu 1.9.14.
4. **AP isolation wyłączone, a timeout nadal jest** — wtedy problem leży gdzie indziej (firewall kamery, VLAN, routing). Do osobnego researchu.
