# INSTRUKCJA DLA TOMASZA — OSOBNY BOT HANSA

Przygotował: Genek (03.08.2026)

---

## 1. JAK ZAŁOŻYĆ NOWEGO BOTA U @BotFather (z telefonu — Samsung Fold, Telegram)

Krok po kroku:

1. Otwórz aplikację Telegram, wyszukaj **@BotFather** (oficjalne konto z niebieską fajką).
2. Otwórz z nim czat i kliknij **START** na dole ekranu (lub wpisz `/start`).
3. Wpisz komendę: `/newbot`
4. BotFather zapyta o nazwę bota (wyświetlaną, np. na liście czatów). Wpisz np.:
   `Hans Kontroler`
5. BotFather zapyta o unikalny "username" bota (musi kończyć się słowem `bot`). Wpisz np.:
   `HansAgentZalogiBot` (jeśli zajęte, spróbuj np. `HansZalogaBot`).
6. Po zatwierdzeniu BotFather wyśle wiadomość z gratulacjami, w której będzie **TOKEN** (wygląda mniej więcej tak: `1234567890:AAHdqTcvCH...`).
7. **Skopiuj ten token**.
8. Wejdź na profil nowo utworzonego bota w Telegramie (klikając w link `t.me/...` w wiadomości od BotFather) i kliknij **START** w rozmowie z Hansem. Bez tego bot nie będzie mógł wysłać Ci pierwszej wiadomości.
9. Żeby bot mógł do Ciebie pisać, musimy znać Twoje ID w Telegramie. 
   - Wyszukaj w Telegramie bota **@userinfobot**.
   - Kliknij START.
   - Odpowie Ci wiadomością zawierającą Twoje `Id` (np. `123456789`). Skopiuj tę liczbę.

---

## 2. GDZIE NA SERWERZE WKLEIĆ TOKEN I ID

Na serwerze mamy już plik konfiguracyjny (wzór: `tools/dzwonek.py` korzysta z konfiguracji Henia do standardowych dzwonków). 
Dla Hansa wykorzystamy ten sam sprawdzony plik:
**Ścieżka:** `/home/hermes/.hermes/.env`

Należy do niego dopisać dwie linijki (najlepiej poprosić nas - Klaudka lub mnie - o wpisanie podanych przez Ciebie danych w ten plik):
```
HANS_BOT_TOKEN="twój_skopiowany_token_z_punktu_6"
HANS_CHAT_ID="twoje_id_z_punktu_9"
```
Nie kasuj przy tym zmiennych `TELEGRAM_BOT_TOKEN` ani `TELEGRAM_HOME_CHANNEL` (używa ich stary bot).

---

## 3. JAK SPRAWDZIĆ, ŻE DZIAŁA

Kiedy token i ID zostaną zapisane w `/home/hermes/.hermes/.env`, uruchomimy na serwerze krótki test (możesz zlecić to załodze komendą "Zróbcie test bota Hansa"):

```bash
python3 -c '
import urllib.request, urllib.parse, json
token, chat_id = "", ""
with open("/home/hermes/.hermes/.env") as f:
    for line in f:
        k, _, v = line.strip().partition("=")
        v = v.strip().strip("\"").strip("\'")
        if k == "HANS_BOT_TOKEN": token = v
        elif k == "HANS_CHAT_ID": chat_id = v
if token and chat_id:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": "🔔 Test Hansa. Zgłaszam gotowość!"}).encode()
    print("OK" if json.load(urllib.request.urlopen(urllib.request.Request(url, data=data)))["ok"] else "BŁĄD")
'
```

Jeżeli na Twój telefon przyjdzie wiadomość "🔔 Test Hansa. Zgłaszam gotowość!", wszystko działa idealnie.

---

## 4. CO HANS MA WYSYŁAĆ I KIEDY (PRÓG ZGŁOSZEŃ)

**CO:**
Hans będzie wysyłał wyłącznie istotne alerty z analizy meldunków Klaudka i ewentualne komunikaty o poważnych uchybieniach, których Klaudek nie zaraportował wprost (np. brak dowodów z narzędzi, samowola w decydowaniu, błędy pominięte w raporcie). Hans NIE służy do powiadamiania, że "rolka jest gotowa" – od tego pozostaje główny kanał powiadomień.

**KIEDY I PROGI:**
Wysłanie raportu następuje:
1. Natychmiast – w sytuacji, gdy po naradzie Hans wykryje, że Klaudek sformułował odpowiedź dla Ciebie BEZ wymaganych dowodów/wywołań narzędzi (Złamanie Kontroli Klaudka z 02.08.2026).
2. Jako paczka (zbiorczo) po zakończeniu wątku/narady, z podaniem co załoga poprawiła.

**PRÓG ZGŁOSZEŃ:**
Aby nie spamować Twojego telefonu w przypadku lawiny błędów (np. awarii API wymuszającej 10 powtórzeń), Hans zastosuje próg: **Maksymalnie 1 powiadomienie (zbiorcze) na jedno pełne zlecenie/naradę.** Dodatkowo twardy limit to **nie więcej niż 3 alerty na godzinę**.
**Uzasadnienie progu:** 
Głównym celem Hansa jest bycie zewnętrzną pamięcią i weryfikatorem dla Ciebie. Jeśli awaria dotyczy samego procesu weryfikacji, wysłanie 15 powiadomień o tym samym błędzie tylko odwróci Twoją uwagę. 3 alerty na godzinę to optymalny balans, który daje Ci znać o problemach, ale nie zmusza do wyciszenia bota w telefonie. Zawsze po godzinie dostaniesz ewentualny skompresowany "raport szkód".
