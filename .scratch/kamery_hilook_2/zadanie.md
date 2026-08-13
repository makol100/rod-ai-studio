# ZADANIE: KAMERY I NAGRYWARKA HILOOK — DOM DZIAŁKOWCA ROD (runda 2, 12.08.2026 wieczór)

Tomasz: "Zwołaj grupę i przedstaw jak jest."
To jest RUNDA 2. Runda 1 (.scratch/kamery_hilook, 12.08 17:50) dała zgodny werdykt Zenka i Henia:
opcja D — integracja `hikvision` (ISAPI) w HA Działka, wycelowana w NVR 192.168.3.110.
Teraz doszły NOWE FAKTY od Tomasza. Trzeba je ocenić i powiedzieć, czy zmieniają rekomendację.

## STAN FAKTYCZNY (ślad: pomiary z 12.08, TELEPORT_HA.md linia 609 + skany z VPS)

SIEĆ
- Sprzęt siedzi w podsieci 192.168.3.0/24 (Dom Działkowca ROD), trasa z VPS przez Tailscale → homeassistant-1 (Działka).
- 192.168.3.1 = router DOSTAWCY (lighttpd). ZAKAZ TOMASZA: nie ruszać. Wchodzimy wyłącznie na jego routery Linksys.
- Osobny zakaz bezterminowy (D-0066/D-0067): "Zostaw router na działce w spokoju!!" — dotyczy routera Działki.
- Podsieci 192.168.0.0/24 (HA Działka .250, Xiaomi, Reolink .207) i 192.168.1.0/24 to INNE sieci — sprzętu HiLook tam nie ma.

SPRZĘT (zmierzony, żywy, osiągalny z VPS)
- NVR HiLook/Hikvision: 192.168.3.110 — porty 80/554/8000, bez 443; /doc/page/login.asp; ISAPI 401 Digest, realm 5048c9083c2853c12763f499.
- Kamery: 192.168.3.111, .112, .114 — realm "IP Camera(FG092)"; 192.168.3.113 — realm "IP Camera(FQ921)". Porty 80/443/554/8000.
- /onvif/device_service = 404 na wszystkich pięciu → ONVIF najpewniej WYŁĄCZONY.
- HA Działka: API 200; ma integracje camera + ffmpeg + reolink + tuya. BRAK onvif, BRAK hikvision, BRAK generic.
- Na VPS stoi już skompilowany ze źródeł `go2rtc-hik` (build 12.08 15:25, porty 1984/8554/8555, config w /root/go2rtc-hik/cfg).

NOWE FAKTY OD TOMASZA (12.08 wieczór) — TO JEST SEDNO TEJ RUNDY
1. "Domyślam się hasła, bo tylko hasło było mi potrzebne, żeby zalogować się do kamer" — do kamer wchodzi SAMYM HASŁEM (login najpewniej standardowy/zapamiętany).
2. "Nagrywarka też zaczęła pokazywać automatycznie po wpisaniu tylko hasła do kamery" — po ustawieniu/podaniu hasła kamery NVR sam zaczął pokazywać obraz z kamer.
3. Hasło NIE MOŻE iść przez czat: wklejenie danych logowania do okna czatu wywala okno — zdarzyło się już 3-4 razy. Hasło przyjdzie plikiem txt na https://wgraj.157-90-155-155.sslip.io (dufs → /root/rod-ai-studio/data/upload).

## PYTANIA ROZSTRZYGALNE (każdy odpowiada osobno i podpisuje się)

P1. Fakt 1+2 (samo hasło do kamer; NVR sam podjął obraz) — co on mówi o konfiguracji tego zestawu?
    Rozstrzygnąć między: (a) kamery są w trybie plug&play NVR-a i dziedziczą po nim hasło aktywacyjne,
    (b) wszystkie urządzenia mają jedno wspólne hasło ustawione ręcznie, (c) coś innego.
    Podać, po czym POZNAMY to pomiarem, gdy dostaniemy hasło (konkretne wywołanie ISAPI, nie ogólnik).

P2. Czy ten fakt ZMIENIA rekomendację z rundy 1 (integracja hikvision na NVR .110)?
    Odpowiedź TAK/NIE + jedno zdanie uzasadnienia. Jeżeli NIE — czy celować w NVR .110 (kanały 101/201/301/401),
    czy w 4 kamery osobno (.111-.114)? Które daje pewniejszą detekcję ruchu i mniej punktów awarii?

P3. Na VPS stoi już własny go2rtc-hik. Czy strumienie HiLook mają iść przez NIEGO (VPS),
    czy przez go2rtc na HA Działka (addon, host_network, wzorzec Xiaomi z 8.08)? Wskazać jedną drogę i powiedzieć,
    co przemawia przeciw tej odrzuconej (trasa przez Tailscale, opóźnienie, punkt awarii, kto to potem utrzymuje).

P4. KOLEJNOŚĆ WYKONANIA. Wypisać kroki od momentu "hasło jest na VPS" do "4 kamery widoczne w HA Działka
    z detekcją ruchu", w kolejności, z zaznaczeniem, który krok jest odwracalny, a który nie.
    Zaznaczyć każdy krok, który dotyka routera lub NVR-a w sposób trwały — te wymagają OSOBNEJ zgody Tomasza.

P5. RYZYKA I KOSZT. Czy któryś krok kosztuje pieniądze albo grozi utratą dostępu do monitoringu
    (np. zmiana hasła, blokada konta po nieudanych próbach, limit sesji NVR)? Jeżeli tak — jak to obejść.

## ZASADY
- Każde twierdzenie ze śladem z TEJ tury. Bez śladu = "NIE WIEM". Trzeciej drogi nie ma.
- Zakaz zgadywania hasła i zakaz prób logowania metodą prób i błędów (ryzyko blokady konta).
- Nie wolno wykonywać żadnych zmian na NVR, kamerach ani routerach — to badanie, nie wdrożenie.
- Odpowiadać po polsku, zwięźle, podpisać się imieniem.
