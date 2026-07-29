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

## GENEK (Gemini CLI)
- Konto: DARMOWY free tier Google AI Studio (klucz GEMINI_API_KEY bez billingu).
- Limit: 20 zapytań/DZIEŃ na gemini-3-flash-preview; reset 00:00 Pacific = 9:00 rano PL.
- Zapas: gemini-2.5-flash (osobna darmowa pula, ale bywa 503 przy przeciążeniu Google); 2.5-flash-lite w CLI: 404 (brak).
- Drugi klucz w tym samym projekcie NIC nie daje (limit per projekt); drugie konto dla obejścia limitu ZABRONIONE w ToS Google.
- Płatny Tier 1 (decyzja Tomasza NIEPODJĘTA): $0.50/1M wej + $3/1M wyj → narada 0,4-0,8 centa, miesiąc ~$1,20-2,40 (budżet $5 z alarmem); limit rośnie do ~10 000/dzień. Rekomendacja Zenka: włączyć.
- Źródła: ai.google.dev/gemini-api/docs/pricing, /rate-limits, developers.google.com/terms.

## PLANOWANIE NARAD (wnioski)
- Genka oszczędzać: JEDNO zbiorcze zapytanie zamiast wielu małych; ciężki research → Zenek.
- Multimodalność (oglądanie obrazów): TYLKO Genek — rezerwować mu pulę na oceny wizualne.
- Przy wyczerpaniu Genka: jawnie meldować Tomaszowi, nie zmyślać jego głosu; opinie dopisze po 9:00.
