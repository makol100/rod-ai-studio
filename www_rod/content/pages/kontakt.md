---
title: Kontakt
description: Napisz do zarządu ROD im. Józefa Lompy w Woźnikach — e-mail rodwozniki@gmail.com lub formularz kontaktowy.
slug: kontakt
---

# Kontakt

**Rodzinny Ogród Działkowy im. Józefa Lompy w Woźnikach**

ul. Młyńska 40c, 42-289 Woźniki

E-mail: **[rodwozniki@gmail.com](mailto:rodwozniki@gmail.com)**

## Napisz do zarządu

:::html
<p class="form-ok" id="wyslano">Dziękujemy — wiadomość dotarła do zarządu. Odpowiemy na podany e-mail.</p>
<p class="form-blad" id="blad">Nie udało się wysłać — wpisz treść wiadomości i zaznacz zgodę (adres e-mail musi być poprawny).</p>

<form class="kontakt-form" method="post" action="/kontakt/wyslij">
  <label for="imie">Imię i nazwisko (lub numer działki)</label>
  <input id="imie" name="imie" type="text" maxlength="120" autocomplete="name">
  <label for="email">Twój e-mail (żebyśmy mogli odpowiedzieć)</label>
  <input id="email" name="email" type="email" maxlength="200" autocomplete="email" inputmode="email">
  <label for="tresc">Wiadomość</label>
  <textarea id="tresc" name="tresc" rows="6" maxlength="4000" required></textarea>
  <input class="pulapka" name="www" type="text" tabindex="-1" autocomplete="off" aria-hidden="true">
  <label class="zgoda"><input name="zgoda" type="checkbox" value="tak" required> Wyrażam zgodę na przetwarzanie podanych danych w celu odpowiedzi na moją wiadomość (administrator: Zarząd ROD im. Józefa Lompy w Woźnikach, ul. Młyńska 40c; szczegóły w <a href="/prywatnosc/">polityce prywatności</a>).</label>
  <button class="button button-primary" type="submit">Wyślij wiadomość</button>
</form>
:::
