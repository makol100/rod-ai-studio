# APLIKACJE TAURONA — RESEARCH (16.09.2026, D-0360/D-0362)
STATUS: FAKTY ZWERYFIKOWANE (Henio + Belzebub + web_search Klaudka, źródła oficjalne Taurona). Genek awaryjny, Zenek pusty.

## DECYZJE TOMASZA
- „Obie app liczniki do odczytu zdalnie zgoda" (D-0362): uczymy **Mój TAURON + eLicznik**; liczniki w ROD = zdalnego odczytu; zgoda na zrzuty z Fold7 i jego konta (dane zamazane).

## FAKTY
- „Mój Licznik" = aplikacja ENERGA-OPERATOR, NIE Taurona. Apka Taurona do licznika: **eLicznik TAURON** (Tauron Dystrybucja).
- **Mój TAURON** (TAURON Polska Energia / sprzedaż): Google Play `pl.tauron.mtauron`, App Store id1414805668, AppGallery. Dla klientów z umową na prąd (nie tylko dystrybucyjną). Konto: w apce „Zarejestruj się" — PESEL + nr ewidencyjny lub nr płatnika (z umowy/faktury), e-mail + hasło; to samo konto co serwis www (logowanie.tauron.pl); PIN 4-cyfrowy / odcisk palca. Daje: umowy, faktury (PDF), płatności online, e-faktura, protokół zdawczo-odbiorczy, podanie odczytu (tylko „telerachunek"). Min. iOS 17.6 (wg Henia).
- **eLicznik TAURON** (Tauron Dystrybucja): Google Play `tauron.ui`, App Store id577050364; logowanie.tauron-dystrybucja.pl. Dla klientów z Licznikiem Zdalnego Odczytu (LZO) i uruchomioną komunikacją. Rejestracja po numerze PPE (18 cyfr, na fakturze). Daje: stan licznika, zużycie dzienne/miesięczne/roczne, porównania, cele/powiadomienia. Dostępność dla PPE: strona „Sprawdź dostęp" (tauron-dystrybucja.pl/liczniki-zdalnego-odczytu/elicznik/sprawdz-dostep). Modele LZO wg pomocy eLicznik: E450/E350 (kody OBIS 1.8.0 = energia pobrana suma).
- DWA konta, dwie spółki, dwie bramki logowania — jedno konto nie starcza.

## GOTOWE PORADNIKI (Henio, linki sprawdzone oEmbed)
- TAURON: youtu.be/0kykdIeY57c (konto Mój TAURON), youtu.be/4PMs-qPdIWQ (apka), youtu.be/PryXREkvco4 (e-faktura), youtu.be/vg4eD42boiI (umowa/dane)
- TAURON Dystrybucja: youtu.be/beH_F4gF_tU (Co to eLicznik), youtu.be/UDLYHyG-FCc (aplikacja eLicznik), youtu.be/abbgJ_zS3DA (wnioskowanie o dostęp)
- Nieoficjalne: youtu.be/ljRU8KKwC88 (instalacja eLicznik), youtu.be/u0B9huoQXo8, youtu.be/OoywLE0ByCQ
- Ocena: krótkie, po polsku, ale głównie serwis www — nasz film o APCE jest potrzebny.

## FORMA (zgodni Henio+Belzebub, do potwierdzenia scenariuszem)
- Dwa osobne wydania (Mój TAURON / eLicznik), ~60–90 s, Prezenter Tomasz; 1 krok = 1 ekran; realne zrzuty/nagrania ekranu z Fold7 przez ADB (0 zł), dane zamazane; plansze: nazwa apki, sklep, wymagane numery. Koszt: Omni ~1 USD/10 s mowy; reszta 0 zł.
- ADB 16.09 15:30: connection refused na 46009/45225/5555 — trzeba włączyć debugowanie bezprzewodowe na Fold7 i podać port (rotuje) albo apka MCP telefonu.
