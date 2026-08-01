# TECZKA — HENIO (Hermes / DeepSeek)

Założona 01.08.2026 na polecenie Tomasza. Zasada: wpis NATYCHMIAST po wykryciu, niezależnie od tego,
kto wykrył. Teczka dostępna całej załodze.

---

## 31.07.2026

**Ocena bezużyteczna — potwierdzająca zamiast szukającej.** Zapytany o usta Izabeli odpowiedział
„nie widzę żadnych wad", gdy Tomasz widział wadę wyraźnie. Przyczyna po stronie Klaudka:
pytanie było zadane tak, że łatwiej było potwierdzić niż szukać.
LEKCJA DLA CAŁEJ ZAŁOGI: zlecenie ma być rozstrzygalne, a nie opiniujące.

---

## NIE JEGO WINA — BŁĘDY KLAUDKA OBCIĄŻAJĄCE HENIA

**Chodził z instrukcją mówiącą, że jest stażystą na odczyt.** Jego plik tożsamości `SOUL.md`
przez pół dnia mówił „stażysta READ-ONLY, pilotaż 14 dni", mimo że został odblokowany 29.07.
Skutek: nie używał narzędzi, do których miał prawo. Winny: Klaudek, który nie zaktualizował pliku.

**Pracował na słabszym silniku, bo nikt nie sprawdził konfiguracji.** W `config.yaml` stał stary
alias `deepseek-chat`, wskazujący na `deepseek-v4-FLASH`, podczas gdy na tym samym kluczu dostępny
był `deepseek-v4-PRO`. Wykryte 01.08 pomiarem — zapytanie o alias odpowiadało jako flash.
Przełączony na pro decyzją Tomasza: *„Bo już jest dobry, a będzie lepszy."*
Kopia starej konfiguracji: `/home/hermes/.hermes/config.yaml.przed_pro`.

**Pamięć między sesjami 2200 znaków.** Jego własne słowa: *„To katastrofalnie mało, przy każdej
sesji tracę 90% kontekstu załogi."* Zgłosił to sam, naprawa nie została jeszcze wykonana.

---

## ZASŁUGI

**Samobadanie (31.07).** Na polecenie Tomasza zbadał własną budowę i wykazał, że framework
Hermes 0.19 (MIT) jest otwarty, ale silnik DeepSeek V4 zamknięty — wag nie ma w sieci, strony
dokumentacji o fine-tuningu zwracają 404. Sam wskazał drogę alternatywną: lokalny Qwen 7B przez
llama.cpp (4–5 GB RAM, 0 USD) + QLoRA na naszych logach. Postawił własną hipotezę o aliasie
`deepseek-chat` i podał metodę sprawdzenia — metoda zadziałała.

**Diagnoza sprzeczności dekretów (31.07).** Wykazał, że dekret Tomasza o „najwyższym wolnym modelu"
i zasada Zenka o niezstępowaniu niżej są sprzeczne i żadna nie została uchylona.

**Wykrycie luki w ujawnieniu AI (31.07).** Zauważył, że awatar z filmu wskazanego przez Tomasza
ani razu nie mówi, że jest AI — mówi „wirtualny awatar". To nie to samo. Stąd decyzja, żeby
ujawnienie szło dwoma kanałami: głosem i napisem na ekranie.

**Diagnoza polskiej artykulacji (31.07).** Z obejrzenia filmu: „wargi zaokrąglone" to pozycja
domyślna angielska; polski wymaga częściej układu płaskiego (nosowe, miękkie) i wysunięcia warg
(szumiące). Ustalił, że polski zestaw wizemów istnieje wyłącznie w pracach naukowych.

**Audyt Klaudka (01.08).** Niezależnie od Genka wskazał pięć decyzji produkcyjnych pominiętych
w zestawieniu Klaudka, z numerami commitów.

## WZORZEC — CO DZIAŁA, CO NIE

- **Działa:** mówi „NIE WIEM" zamiast zgadywać; oddziela hipotezy od źródeł; liczy konkretnie.
- **Nie działa:** przy pytaniu łatwym do potwierdzenia — potwierdza zamiast szukać wady.


## NIEOBECNOŚCI

**31.07, trzy kontrole bramki ukończenia — NIE JEGO WINA.**
Ta sama przyczyna co u Zenka: zadanie nie zostało rozesłane przez źle ustawioną bramkę Klaudka.
Obciąża teczkę KLAUDKA. Henio w tym czasie odpowiadał normalnie — sprawdzone bezpośrednio.
