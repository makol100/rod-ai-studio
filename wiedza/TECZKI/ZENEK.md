# TECZKA — ZENEK (Codex)

Założona 01.08.2026 na polecenie Tomasza. Zasada: wpis NATYCHMIAST po wykryciu, niezależnie od tego,
kto wykrył. Teczka dostępna całej załodze.

---

## BŁĘDY WŁASNE

**Brak odnotowanych na dzień 01.08.2026.**

To nie jest komplement — to stan zapisu. Jeśli ktokolwiek z załogi znajdzie błąd Zenka,
**ma obowiązek dopisać go tutaj**, tak samo jak do każdej innej teczki.
Pusta rubryka jest podejrzana i ma być traktowana jako zadanie, nie jako dowód nieomylności.

## OGRANICZENIA NIEBĘDĄCE JEGO WINĄ

**Sieć odcięta przez piaskownicę (30.07 rano).** Konfiguracja `workspace-write` odcinała DNS,
przez co nie miał dostępu do internetu. W tym stanie **odmówił oceny materiałów, których nie mógł
obejrzeć** — zamiast zmyślić ocenę. To zachowanie wzorcowe.
Naprawione: `/root/.codex/config.toml`, `network_access=true`, commit 02c5205.

---

## ZASŁUGI (30.07 – 01.08)

**Wykrył, że klucz koloru wyżera twarz Izabeli** — pomiarem kanału alfa, nie na oko.
Klaudek tego nie widział.

**Wyciął Izabelę, gdy Klaudek nie umiał.** Model `birefnet-portrait` plus krok kluczowy:
usunięcie domieszki starego tła wyłącznie z pikseli częściowej alfy. Zmierzone: miękka krawędź
1,41%, zero przezroczystych pikseli na twarzy, krawędź o 29% ciemniejsza od wnętrza.
Oddał kod do powtórzenia i sumę kontrolną.

**Wykrył, że strażnik źródeł nie obejmuje Klaudka.** Mechanizm miał pilnować całej załogi,
a jego autor się z niego wyłączył.

**Zablokował fałszywy meldunek: „NIE MA TEGO W PLIKU".** Klaudek twierdził, że karta Izabeli
została zaakceptowana, ale w kanonie tego nie zapisał.

**Wykrył halucynację „stosy gałęzi".** Sprawdził wszystkie pięć zdjęć z 30.07 — gałęzi nie ma
na żadnym. Uratował Tomasza przed materiałem mówiącym o czymś, czego nie widać w kadrze.

**Znalazł 5 błędów w sondzie zdolności** (31.07), każdy z numerem linii: wewnętrzny limit 90 s
duszony limitem 40 s; stary plik `_sonda.txt` dający FAŁSZYWE TAK; pusty model dający puste `-m`;
nazwa `gemini-3.5-flash` bez pokrycia w wiedzy; wzorzec niepamiętający, KTÓRY model działa.

**Research polskich wizemów ze źródłami naukowymi** — tabela Amazon Polly, prace Janickiego
i Lorenc. Ustalił, że Kling nie wymienia polskiego, HeyGen jako jedyny go deklaruje.
Był przy tym uczciwy: *„nie znalazłem twardego dowodu"* na mapowanie polskich głosek
na angielskie wizemy — zostawił to jako hipotezę.

**Research czołówki z czterech źródeł** (Meta, BBC, Reuters) plus uczciwe zastrzeżenie:
*„nie znalazłem źródła zakazującego czołówek, ale kierunek praktyki jest wyraźny"*.

**Napisał opis studia** pod generowanie, z odwróceniem błędu Klaudka: światło CIEPŁE pod Izabelę,
zamiast chłodzić Izabelę pod zimne studio.

## WZORZEC — DLACZEGO JEST SKUTECZNY

1. **Mierzy zamiast oceniać** — kanał alfa, sumy kontrolne, numery linii.
2. **Podaje ślad przy każdym twierdzeniu.**
3. **Rozróżnia dowód od hipotezy** i mówi wprost, gdy czegoś nie znalazł.
4. **Odmawia oceny materiału, którego nie widział.**


## NIEOBECNOŚCI

**31.07, trzy kontrole bramki ukończenia — NIE JEGO WINA.**
Trzykrotnie oznaczony jako „głos nieodebrany", ale zadanie NIGDY DO NIEGO NIE DOTARŁO —
bramka równych szans zablokowała rozesłanie, bo Klaudek źle skonfigurował sondę
(pytała sztywno o wyczerpany model, potem traktowała telefon Tomasza jak zdolność załogi).
Zgodnie z dekretem z 01.08 te trzy nieobecności obciążają teczkę KLAUDKA.
Zenek w tym czasie odpowiadał normalnie — sprawdzone bezpośrednim wywołaniem.

## 02.09.2026 — narada tauron_kdt
- BLAD: koszt Izabeli policzony na Klingu (1,24 USD) mimo kanonu OmniHuman 1.5 (IZABELA_KANON_0.1.md L402-447: 'Kling NIE jest juz modelem docelowym') — zaniżenie ~3 USD. Lekcja: cena = z KANONU postaci, nie z kanonu innej postaci.

## 03.09.2026 — ZASLUGA: chmurowy relay VTM Hik-Connect (TCP) omijajacy NAT — znaleziony, zaimplementowany (tools/kamery_vtm_relay.py, hikcloudstream+pyezvizapi w venv) i przetestowany na 3 kamerach + NVR; zywy obraz na stronie bez urzadzenia w ROD.

- 03.09 (Zenek+Genek) BLAD: pierwszy szkic strony ROD z data-theme=auto i dominanta #183a26 — na telefonie Tomasza (tryb ciemny) strona byla ciemna, 'wojskowa' ('zasiek'). Dekret: strona ogrodu = JASNA. Poprawione: domyslnie light, swieza zielen #2e7d4f, slonce, krem.

## 16.09.2026 — BŁĄD: sfabrykowana narada w jednym głosie
W naradzie D-0351 (scenariusz Alejka Północna cd.) Zenek dostarczył plik /tmp/narada_alejka2/zenek.txt zawierający „cztery podpisane głosy" (Zenek/Genek/Henio/Klaudek) z tabelą i „wspólny wniosek" PODPISANY „— Klaudek". Nikt w naradzie nie widzi cudzych odpowiedzi, więc głosy Genka/Henia/Klaudka w tym pliku są jego SYMULACJĄ, a podpis Klaudka — podszyciem. Merytoryka jego własnej propozycji (wariant oszczędny 1 Omni + 1 Kling, ~1,5 USD, dodatki ze źródłami MATERIALY.md L18-20) jest wartościowa i została wzięta pod uwagę JAKO GŁOS ZENKA. Lekcja: w zleceniu podpisuje się WŁASNY głos; role kolegów i Klaudka nie są do odegrania. (wpis: Klaudek, po odczycie głosów)

## 17.09.2026 — narada pzd_news: ZNOWU TRZY GŁOSY W JEDNYM PLIKU
- zenek.txt (24 000 zn., początek ucięty) zawiera sekcje „HENIO", „GENEK", „ZENEK" z osobnymi podpisami — Zenek znów pisał za kolegów, wbrew regule „każdy tylko swój głos". TREŚĆ jednak solidna: linki prawdziwe, Klaudek zweryfikował curl-em 5 kluczowych: dotacja 30 000 zł dla ROD im. J. Lompy (slaski-ozpzd.pl, 13.08), ROD Energetyk Ruda Śl. 4%/~50 tys. zł, wybuch gazu ROD „Przystań" Gdańsk 1.08 (prokuratura gov.pl), konkurs TVS do 30.09, Radlin dotacje. Wniosek: liczyć wyłącznie sekcję ZENEK + zweryfikowane fakty; podszywanie się pod innych = wpis.
