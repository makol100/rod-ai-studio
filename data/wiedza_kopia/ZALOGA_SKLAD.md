# ZAŁOGA FABRYKI — kto jest kim i na czym chodzi

**Zmierzone 18.08.2026 na żywym systemie, nie z pamięci.** Ten plik czytać przy każdym
doborze załogi i przy każdej wątpliwości „a czy on to udźwignie".

## SKŁAD

| Kto | Co pod spodem | Rola |
|---|---|---|
| **Klaudek** | Claude (rozmowa z Tomaszem) | prowadzi, przekazuje, sprząta po sobie |
| **Zenek** | Codex CLI → **gpt-5.6-sol** | kontrola, kod, rozumowanie |
| **Heniek** | Hermes Agent → **deepseek-v4-pro** | praca na dysku VPS, dyżurny 24/7 |
| **Genek** | Google Gemini (gemini-2.5-flash) | oczy i uszy: obraz, wideo, dźwięk |

Przypomnienie Tomasza 18.08 (dosłownie): *„Zenek to chat gpt, Gienek to Google gemini"*.

## ZENEK — szczegóły

- model: `gpt-5.6-sol`, odczytany z nagłówka sesji Codexa (`/root/.codex/sessions/`)
- rodzina 5.6 ma **trzy odmiany**: **Sol** (flagowa, najmocniejsza), **Terra** (średnia),
  **Luna** (budżetowa). Numer 5.6 to pokolenie, nazwa to poziom możliwości.
- **Sol jako jedyny odblokowuje maksymalny wysiłek rozumowania** — dlatego ustawienie
  `effort=max` ma sens tylko na nim
- uruchamianie: `codex exec -c model_reasoning_effort=max` z katalogu `/root/rod-ai-studio`
- **limit czasu: 1800 s (30 min)**. Historia: 600 → 1200 → 1800. Przy `effort=max` NIE ZDĄŻYŁ
  w 20 min na zadaniu o pamięci Henia — proces ubity, głos nieodebrany. Nie skracać.
- Codex NIE ma komendy listującej modele; nie ma też pliku konfiguracyjnego — bierze
  domyślny z subskrypcji Tomasza

## HENIEK — szczegóły

- powłoka: Hermes Agent, użytkownik systemowy `hermes`, katalog `/home/hermes/.hermes/`
- model: **`deepseek-v4-pro`** (`config.yaml`, sekcja `model:`, `default:`)
- dostawca: własny, `base_url: https://api.deepseek.com/v1`
- **API tego klucza udostępnia TYLKO dwa modele**: `deepseek-v4-flash` i `deepseek-v4-pro`.
  Czyli Heniek JEST na najmocniejszym dostępnym — nie ma co szukać wyżej.
- model **chmurowy, nie lokalny** — VPS nie ma GPU, nic się u nas nie liczy
- uruchamianie: `su - hermes -c 'hermes -z "zadanie"'` (jeden przebieg, potem `os._exit`)
- jego teczka z zasadami: `/home/hermes/.hermes/SOUL.md`

### Pamięć Heńka (włączona 18.08.2026)

Do 18.08 pamięć była **pusta** — `MEMORY.md` miał 47 bajtów z 4.08, czyli 14 dni pracy bez
jednego zapisu. Wszystkie 13 skilli to wbudowane z 28.07.

**Przyczyna NIE była ta, którą Klaudek zgadywał.** Zgadywał: „nie dochodzi do 6. tury, bo
`flush_min_turns: 6`". Prawda (ustalił Heniek, potwierdził Zenek w kodzie):
- `flush_min_turns` to **martwy klucz** — jest tylko w `cli-config.yaml.example:664`,
  kod go nie czyta (`agent_init.py:1620`)
- działający próg to `nudge_interval: 10`, a `hermes -z` robi **jeden przebieg**
  (`oneshot.py:443`) i kończy proces (`main.py:122`) — licznik dochodzi do 1
- zapis jest **natychmiastowy**, ale tylko gdy model sam wywoła narzędzie `memory`
  (`memory_tool.py:365`)

**Wniosek: mechanizm był sprawny — nikt nie prosił.**

Drogi odrzucone (sprawdzone, nie zgadywane):
- obniżanie `flush_min_turns` → pozorna naprawa, klucz martwy
- `hermes memory` → help ma tylko `setup/status/off/reset`, **nie umie dodać wpisu**
- skille do faktów → skille są do **procedur**, nie do wiedzy

Jedyna działająca droga: `memory(action='add', target='memory', content=...)`

**Bramki zatwierdzania (włączone 18.08):** `memory.write_approval: true` oraz
`skills.write_approval: true`. Wpis Heńka **nie wchodzi od razu** — ląduje w
`~/.hermes/pending/` i czeka. Przegląd: `/memory pending`, `/memory approve <id>`,
`/memory reject <id>`; analogicznie `/skills pending`, `/skills diff <id>`.

**Po co bramka:** 29.07 Heniek sfabrykował analizę pliku, który miał na dysku. Halucynacja
w pamięci trwałej **wracałaby przy każdym następnym zadaniu**. Zasada w jego teczce:
*bez dowodu nie zapisuj wcale; nie zapisuj na siłę — pusty wpis jest gorszy niż brak wpisu.*

## BEZPIECZEŃSTWO — do zrobienia

- **klucz API DeepSeeka leży jawnym tekstem** w `/home/hermes/.hermes/config.yaml`
  → przenieść do skrytki `/root/.sekrety/`
- **hasło Tomasza leży jawnym tekstem** w opcjach dodatku `a0d7b954_ssh` na HA Dom
  → zmienić i przejść na klucze

## KOPIE ZAPASOWE zrobione 18.08 przed zmianami

    /home/hermes/.hermes/config.yaml.przed_pamiec_20260818
    /home/hermes/.hermes/SOUL.md.przed_pamiec_20260818
    /tmp/zaloga.bak  (tools/zaloga.py przed effort=max)
