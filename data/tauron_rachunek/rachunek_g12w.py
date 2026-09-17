# Rachunek miesieczny — umowa kompleksowa TAURON, G12W, 1F, rozliczenie miesieczne (D-0380)
# DYSTRYBUCJA: oficjalny wyciag Taryfy TAURON Dystrybucja 2026 dla grup G (URE 17.12.2025), netto:
SIEC_STALA_1F = 7.38      # zl/m-c, uklad 1-fazowy
ABONAMENT_1M  = 4.56      # zl/m-c, okres rozliczeniowy 1-miesieczny
SIEC_ZM_SZCZYT, SIEC_ZM_POZA = 0.3298, 0.0512   # zl/kWh G12w
JAKOSC = 0.0331; OZE = 0.0073; KOGEN = 0.0030      # zl/kWh
MOCOWA = {"<500": 4.29, "500-1200": 10.31, "1200-2800": 17.18, ">2800": 24.05}  # zl/m-c wg zuzycia rocznego
# SPRZEDAZ (PRZYBLIZENIE — taryfa TAURON Sprzedaz 2026 zatwierdzona przez URE, G12 szczyt/pozaszczyt netto wg czyczy.pl;
# cennik z umowy 'EE_GD GR5 B_ule TS_3_Q3' moze miec INNE ceny + oplate handlowa — do podmiany po otrzymaniu zalacznika):
EN_SZCZYT, EN_POZA = 0.54472, 0.41463
HANDLOWA = 0.0   # NIEZNANA — z cennika umowy
VAT = 1.23
def licz(kwh, prog_mocowy):
    dz, noc = kwh/3, kwh*2/3
    stale = {"siec. stala 1F": SIEC_STALA_1F, "abonament": ABONAMENT_1M, "mocowa": MOCOWA[prog_mocowy], "handlowa (?)": HANDLOWA}
    zm = {"energia dzien": dz*EN_SZCZYT, "energia noc": noc*EN_POZA, "siec. zm. dzien": dz*SIEC_ZM_SZCZYT, "siec. zm. noc": noc*SIEC_ZM_POZA,
          "jakosciowa": kwh*JAKOSC, "OZE": kwh*OZE, "kogeneracyjna": kwh*KOGEN}
    n = sum(stale.values()) + sum(zm.values())
    print(f"\n=== {kwh} kWh/m-c ({dz:.1f} dzien / {noc:.1f} noc), oplata mocowa prog {prog_mocowy} ===")
    for k, v in {**stale, **zm}.items(): print(f"  {k:18s} {v:7.2f} zl netto")
    print(f"  RAZEM netto {n:7.2f} zl  ->  BRUTTO (VAT 23%) {n*VAT:7.2f} zl")
    return n*VAT
a = licz(0, "<500"); b = licz(100, "500-1200"); c = licz(100, "<500")
print(f"\nPODSUMOWANIE brutto: 0 kWh = {a:.2f} zl/m-c | 100 kWh = {b:.2f} zl/m-c (pierwsze miesiace, dopoki zuzycie skumulowane <500 kWh: {c:.2f} zl)")
