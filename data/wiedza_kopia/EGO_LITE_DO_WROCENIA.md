# EGO LITE — WATEK ODLOZONY (rozpoznane 5.08.2026)

**Tomasz wskazal to narzedzie 5.08. Rozpoznane, NIC NIE ZAINSTALOWANO — nie da sie u nas.**

## CO TO JEST

`github.com/citrolabs/ego-lite` · **8647 gwiazdek** · MIT · JavaScript · strona `lite.ego.app`
Zalozone 16.04.2026, ostatnia zmiana **5.08.2026** — projekt zyje intensywnie, ale ma
dopiero **cztery miesiace**.

> *„Przegladarka, w ktorej Ty i Twoi agenci pracujecie rownolegle. Agenci wykonuja zadania
> we wlasnych przestrzeniach, podczas gdy Ty korzystasz ze swojej."*

**Roznica wobec innych narzedzi (browser-use, agent-browser)** — autorzy nazywaja ja wprost:
tamte sa frameworkami automatyzacji i **potrzebuja osobnej przegladarki do sterowania,
a LOGOWANIA SIE NIE PRZENOSZA**. Ego lite **dzieli z agentem Twoja zalogowana sesje.**

## DLACZEGO NIE TERAZ

> *„ego lite runs on macOS today. Windows and Linux are on the roadmap."*

**Tylko macOS.** Nasz serwer to Linux, komputer Tomasza to Windows, Tomasz pracuje z telefonu.
**Zadna z tych drog nie jest obslugiwana.**

## DLACZEGO WARTO DO TEGO WROCIC — PROBLEM JEST REALNY

**5.08 stanelismy DWA RAZY na tym samym**: zadanie wymagalo **zalogowanej przegladarki**,
do ktorej Klaudek nie siega:
1. **Tailscale — 2 trasy czekaja na zatwierdzenie** (Wybickiego). Bez tego urzadzenia w sieci
   mieszkania sa nieosiagalne. Zatwierdza sie w `login.tailscale.com`, w przegladarce.
2. **Tuya — logowanie kodem QR.** Tomasz nie mogl go zeskanowac tym samym telefonem,
   ktory go wyswietla. Obejscie: otworzyc HA na innym ekranie.

Do tego dochodzi publikacja na Facebooku i zarzadzanie Nabu Casa — **wszystko to sa rzeczy
za zalogowana sesja.**

## CZEGO NIE WOLNO PRZEOCZYC, GDY WROCIMY

**BEZPIECZENSTWO — to jest cena tego narzedzia.** Ono dzieli z agentem **cala zalogowana sesje
przegladarki**: bank, poczta, media spolecznosciowe, panele administracyjne. To jest jednoczesnie
jego sila i jego ryzyko. Przed uzyciem rozstrzygnac z Tomaszem, **do czego agent ma miec dostep,
a do czego nie** — najlepiej osobny profil przegladarki tylko do zadan, bez bankowosci.

**MLODOSC PROJEKTU.** Cztery miesiace zycia mimo duzej popularnosci. Sprawdzic ponownie
liczbe gwiazdek, tempo zmian i zgloszone bledy, zanim cokolwiek dostanie dostep do sesji.

## WARUNEK POWROTU

**Pojawienie sie wersji na Windows albo Linux.** Sprawdzac: `lite.ego.app/roadmap`
oraz wydania w `github.com/citrolabs/ego-lite/releases`.
