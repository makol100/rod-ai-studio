# ZACZEP W MOSCIE — NIEMY REJESTRATOR (5.08.2026)

**Tomasz: „Budować zgodnie z grupą."** Zbudowany wg JEDNOMYSLNEJ rekomendacji Zenka, Henia i Genka.

## CO ROBI

Zapisuje **surowe zdarzenia** z kazdego wywolania narzedzia Klaudka do
`.scratch/hans/most.jsonl`. Jeden wiersz JSON na wywolanie:

| pole | znaczenie |
|---|---|
| `ts` | znacznik czasu |
| `narzedzie` | execute_command / read_file / write_file / append_file / list_dir |
| `zlecenie_dla_zalogi` | czy w tresci byl `zaloga.py`, `odpal.py`, `hermes -z`, `dzwonek.py` |
| `wyglada_na_naprawe` | czy byl `pip install`, `apt install`, `systemctl restart/start/stop`, `pkill`, `kill -9`, `systemd-run`, `docker restart`, `npm install`, `bun install` |
| `podglad` | pierwsze 160 znakow |

## CZEGO NIE ROBI — I DLACZEGO

**NIC NIE OCENIA i NIC NIE DOKLEJA do wyniku narzedzia.**

Zenek rozstrzygnal konflikt, ktory Klaudek uwazal za nierozstrzygalny:
> *„komunikat doklejony do WYNIKU przychodzi juz PO wykonaniu instalacji.
> Nie zatrzyma biezacego odruchu; moze wplynac dopiero na nastepna akcje."*

Czyli ostrzeganie na zywo bylo z definicji spoznione — a przy tym **psulo pomiar**,
bo zmienia zachowanie mierzonego. Henio nazwal ten konflikt **falszywym**:
> *„Naprawa NIE musi byc na zywo. Hans i tak dziala PO FAKCIE — ucho co 60 s, oczy co 15 min."*

**OCENIA HANS** (`tools/hans.py`, wlasnosc Henia, D-0006) — z zewnatrz.
Klaudek nie moze byc sedzia we wlasnej sprawie; to on sam zglosil te slabosc Tomaszowi.

## ZABEZPIECZENIA

**FAIL-OPEN.** Kazdy blad zapisu jest polykany (`except Exception: pass`).
Most MUSI dzialac tak, jakby zaczepu nie bylo — **utrata mostu = Klaudek traci dostep do serwera**.
Sprawdzone 5.08 trzema probami: zapis normalny, zapis do niemozliwej sciezki, wylacznik.
Zaden nie rzucil wyjatkiem.

**WYLACZNIK.** `ZACZEP_WYLACZONY=1` w `/root/claude-vps-mcp/mcp.env` gasi go bez dotykania kodu.
Moze to zrobic Tomasz albo Henio.

**KOPIA.** Wersja sprzed zaczepu: `/tmp/mcp_server_przed_zaczepem.py`
oraz w repo: `wdrozenie/most/mcp_server.py` (wersja Z zaczepem, do odtworzenia).

## JAK BYL WDRAZANY (procedura, do powtorzenia)

1. kopia oryginalu
2. nowa wersja zapisana OBOK jako `mcp_server_NOWY.py`
3. sprawdzenie skladni
4. **proba na INNYM porcie (8799)** z tym samym srodowiskiem (`mcp.env`, venv) — wstal
5. test fail-open na trzech przypadkach
6. dopiero potem podmiana i restart
7. natychmiastowe sprawdzenie, czy Klaudek ma dostep

## MIARA DO SPRAWDZENIA PO TYGODNIU

**`solo_bez_narady`** (nazwa Henia): ile razy Klaudek uruchomil cos z `wyglada_na_naprawe=true`,
nie majac `zlecenie_dla_zalogi=true` w oknie poprzedzajacym.

**Zenek zastrzega:** najpierw **FAZA CICHA** jako punkt odniesienia — bez tego za tydzien
nie bedzie z czym porownac. Faza ostrzegajaca (jesli w ogole) osobno, wynik pokazywany
oddzielnie przed i po.

## PO CO TO — pytanie Tomasza

To **nie naprawia Klaudka na zywo**. Odpowiada liczba zamiast wrazeniem na pytanie,
czy problem lezy w braku przypomnien — i **czy ClawMem (4 GB, obce srodowisko) ma sens**,
zanim pojda na niego dni pracy.
