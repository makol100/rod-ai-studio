# Dokumenty elektryka ROD Woźniki

Stałe szablony pism, które Tomasz (elektryk z uprawnieniami SEP E + D + pomiary do 1 kV)
wystawia działkowcom przy przechodzeniu na indywidualne przyłącza TAURON.

Dekret Tomasza 14.09.2026: *„będziemy je w przyszłości edytować i będziemy wystawiać takie
właśnie oświadczenia protokoły do kolejnych osób"* — ten katalog jest źródłem prawdy.

## Co tu jest

```
dokumenty/elektryk/
├── szablony/oswiadczenie_przepiecie.js   przepięcie działki na przyłącze indywidualne
├── szablony/oswiadczenie_kabel.js        kabel od licznika do punktu przyłączeniowego
├── dane/<dzialka>.json                   dane jednego dokumentu (edytujesz TYLKO to)
├── assets/                               logo ROD + znak elektryczny (nie podmieniać bez powodu)
│   ├── logo_rod.png        okrągłe logo ROD (kopia assets/branding/rod_logo_kolo.png)
│   ├── znak_elektryk.svg   ORYGINALNY znak ISO 7010 W012 (wektor — tak trafia do dokumentu)
│   └── znak_elektryk.png   ten sam znak jako fallback PNG 900x900
└── wystawione/                           gotowe DOCX dla konkretnych działek
```

## Jak wystawić dokument kolejnej osobie

1. Skopiuj `dane/dzialka_23.json` na np. `dane/dzialka_31.json` i zmień pola.
2. Uruchom:
   ```bash
   cd /root/rod-ai-studio/dokumenty/elektryk
   node szablony/oswiadczenie_przepiecie.js dane/dzialka_31.json
   ```
3. Gotowy plik ląduje w `wystawione/`. PDF robi się poza VPS (tu nie ma LibreOffice).

Pole puste lub brakujące = w dokumencie zostają kropki do ręcznego wpisania
(tak jest celowo dla numerów świadectw E i D — Tomasz wpisuje je sam).

## Żelazne zasady tych pism (ustalone 14.09.2026)

- Nagłówek: **logo ROD po lewej**, **znak elektryczny po prawej** + podpis „ELEKTRYK / Tomasz Maksyś".
- Znak elektryczny = **oryginalny ISO 7010 W012** wstawiany **wektorowo** (svg + fallback png),
  proporcje 600×524 — nie rozciągać do kwadratu (od tego robił się rozmyty).
- Uprawnienia wypisane **osobno dla E i osobno dla D** + pomiary ochronne (kontrolno-pomiarowe) do 1 kV.
- **NUMERY UPRAWNIEŃ WPISYWAĆ ZAWSZE** (dekret Tomasza 19.09.2026: „To są moje dane. Wpisuj za każdym
  razem w oświadczenia"). Z jego pieczątki: *Tomasz Maksyś – Elektryk, Uprawnienia SEP G1 (E + D + Pomiary)*,
  nr **G1/E/470/1081/2025** (eksploatacja) i nr **G1/D/470/1082/2025** (dozór). Oba numery są wpisane
  na stałe w szablony — JSON ich nie potrzebuje. Dat ważności na pieczątce NIE MA, więc dokument ich nie
  drukuje; pojawią się tylko wtedy, gdy ktoś poda `wazne_e` / `wazne_d` w JSON.
- **Żadnych danych z TAURONA**: nr umowy, nr licznika Tauronu, nr PPE — nikogo to nie interesuje
  i to dane wrażliwe.
- Podlicznik ogrodowy: typ, numer i **stan na dzień odłączenia** (do rozliczenia z zarządem).
- **STAN LICZNIKA ZAWSZE ZAOKRĄGLAĆ W GÓRĘ** do pełnych kWh (dekret Tomasza 19.09.2026: „Stan licznika
  to 535 zawsze zaokrąglaj do góry"). Czerwony bęben = dziesiąte części; jeśli pokazuje cokolwiek
  powyżej zera, do pełnych kWh dodaje się 1 (534,9 → 535; 17 377,5 → 17 378). Nigdy w dół, nigdy z przecinkiem.
- Sformułowania, na które Tomasz zwracał uwagę:
  - przewody **zaizolowałem** (nie „odizolowałem"), są **zabezpieczone przed porażeniem**;
  - **wewnętrzna sieć działkowa pozostaje pod napięciem** i zasila pozostałe działki
    (odłączona jest tylko ta jedna działka).
- Dwa podpisy: działkowiec (potwierdza odczyt podlicznika) i elektryk.

## Oświadczenie o kablu (oswiadczenie_kabel.js)

Krótkie pismo: kabel zasilający od złącza kablowo-pomiarowego (licznika) do punktu
przyłączeniowego na działce jest wykonany, zabezpieczony i nadaje się do przyłączenia
do sieci. **Dotyczy WYŁĄCZNIE kabla** — dekret Tomasza 14.09.2026: „bez instalacji domku
i w altanie i na działce". W piśmie stoi to wprost jako zdanie wyłączające odpowiedzialność
za instalację altany i resztę instalacji działki. Nie rozszerzać tego zakresu.

## Następne dokumenty do tej rodziny

Kolejne pisma (protokół pomiarów, protokół z oględzin instalacji przed wydaniem KDT)
dokładać jako nowe pliki w `szablony/` — z tym samym nagłówkiem i tymi samymi assetami.
