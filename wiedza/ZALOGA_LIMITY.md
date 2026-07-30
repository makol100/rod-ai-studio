# LIMITY ZAŁOGI (badanie Zenka 27.07.2026, źródła: oficjalne docs OpenAI/Google)

## KLAUDEK (Claude, prowadzi)
- Konto: Claude Max Tomasza (najdroższy pakiet). Okna czasowe Claude.

## ZENEK (Codex CLI, gpt-5.6-sol)
- Konto: ChatGPT Plus Tomasza ($20/mies.) — praca WLICZONA w abonament, zero dopłat.
- Limit: ruchome okno 5 h, ~15-90 wiadomości (zależnie od ciężkości: research/długi kontekst jedzą więcej) + niepublikowany limit tygodniowy.
- NIE dzieli puli ze zwykłym czatem ChatGPT w przeglądarce (dzieli z funkcjami agentowymi: Codex, ChatGPT Work, Excel).
- Po wyczerpaniu: czekanie na reset okna; rozpoczęte zadanie się dokończy. Brak auto-degradacji modelu.
- Licznik: chatgpt.com/codex/settings/usage (lub /status w interaktywnym CLI; codex exec nie ma odczytu licznika).
- Źródła: learn.chatgpt.com/docs/pricing, help.openai.com (credits/flexible usage).

## GENEK (Gemini CLI) — AKTUALIZACJA 30.07.2026: PŁATNOŚĆ WŁĄCZONA

**Tomasz włączył płatny tier 30.07.2026** („Dodane i naładowane"). Decyzja, która wisiała od 27.07,
zamknięta. Powód: darmowa pula dawała 503 „This model is currently experiencing high demand" —
Genek tracił dostęp do dysku w trakcie narady i debata musiała być powtórzona.

**KANON MODELU (decyzja całej załogi 30.07, zbieżnie Zenek + Genek + Henio):**
- Genek pracuje na **`gemini-3.1-pro-preview`** — KONKRETNY model, nigdy alias
- **Alias `gemini-pro-latest` ODRZUCONY**: Google podmienia model w tle (`gemini-pro` wskazywało rok
  na 1.5 Pro, potem przeskoczyło na 2.0) — zmienia to koszt i zachowanie bez naszej wiedzy
- **Bez degradacji**: gdy pro niedostępny → ZATRZYMAĆ z komunikatem, nie schodzić na słabszy model
  (zasada Zenka). Inaczej dostajesz odpowiedź gorszego modelu, myśląc że to ten wyższy
- **Oczy i uszy zostają na flash** (`tools/oczy_uszy.py`) — zbieżnie wszyscy trzej: oglądanie wideo
  zjada ogromne ilości tokenów, a flash robi to równie dobrze. Pro rezerwujemy na pracę z dyskiem

**ZMIERZONE PO WŁĄCZENIU PŁATNOŚCI (30.07):**
- `gemini-3.1-pro-preview` → 200, CLI przechodzi, pełna ścieżka (odczyt z numerem linii + zapis) działa
- `gemini-3.6-flash` w CLI → przechodzi (wcześniej 503 po 7 próbach)
- `gemini-2.5-flash` w CLI → nadal 503
- `gemini-2.5-pro` i `gemini-3-pro-preview` → 404, tych nazw nie ma na naszym kluczu
- seria 6 szybkich wywołań na pro: 200 200 200 **503** 200 200 — **jeden na sześć nadal odbija**,
  czyli płatność nie znosi przeciążeń Google całkowicie. Dlatego trzy próby tego samego modelu.

## GENEK — stan sprzed 30.07 (archiwalnie)
- Konto: **PŁATNY Tier 1 — WŁĄCZONY 30.07.2026 przez Tomasza** („Dodane i naładowane"). Wcześniej darmowy free tier.
- Limit: był 20 zapytań/DZIEŃ na darmowym; po włączeniu Tier 1 rośnie do ~10 000/dzień.
- Zapas: gemini-2.5-flash (osobna darmowa pula, ale bywa 503 przy przeciążeniu Google); 2.5-flash-lite w CLI: 404 (brak).
- Drugi klucz w tym samym projekcie NIC nie daje (limit per projekt); drugie konto dla obejścia limitu ZABRONIONE w ToS Google.
- Płatny Tier 1 (**PODJĘTA I WŁĄCZONA 30.07**): $0.50/1M wej + $3/1M wyj → narada 0,4-0,8 centa, miesiąc ~$1,20-2,40 (budżet $5 z alarmem); limit rośnie do ~10 000/dzień. Rekomendacja Zenka: włączyć.
- Źródła: ai.google.dev/gemini-api/docs/pricing, /rate-limits, developers.google.com/terms.

## PLANOWANIE NARAD (wnioski)
- Genka oszczędzać: JEDNO zbiorcze zapytanie zamiast wielu małych; ciężki research → Zenek.
- Multimodalność (oglądanie obrazów): TYLKO Genek — rezerwować mu pulę na oceny wizualne.
- Przy wyczerpaniu Genka: jawnie meldować Tomaszowi, nie zmyślać jego głosu; opinie dopisze po 9:00.

## MODEL GENKA — USTALONY 30.07.2026 (narada całej załogi)
Dekret Tomasza: „Genek ma zostać na najwyższym wolnym dla nas modelu zawsze."
**Model: `gemini-3.1-pro-preview`** — konkretny, NIGDY alias.
- Zmierzone przed włączeniem płatności: flash 2.5 i 3.6 w CLI → 503 „high demand" po 5–7 próbach;
  3.1-pro → przeszedł za pierwszym razem. Po włączeniu Tier 1: trzy próby pod rząd, zero 503.
- `gemini-2.5-pro` i `gemini-3-pro-preview` → **404 również po opłaceniu**. To nie kwestia pieniędzy:
  te nazwy nie istnieją pod tym endpointem. Płatność otworzyła przepustowość, nie katalog.
- Alias `gemini-pro-latest` ODRZUCONY jednogłośnie: Google podmienia model pod aliasem bez uprzedzenia,
  co zmienia koszt i zachowanie w tle.
- **Oczy i uszy (`tools/oczy_uszy.py`) ZOSTAJĄ na flash** — zgodnie wszyscy trzej. Wideo zjada ogromne
  ilości tokenów wejściowych, a flash opisuje kadry równie dobrze; pro byłby tam ~16× droższy bez zysku.
- Gdy pro niedostępny: **zatrzymać zadanie z jawnym komunikatem**, nie schodzić po cichu niżej.
