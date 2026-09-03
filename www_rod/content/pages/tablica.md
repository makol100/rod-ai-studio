---
title: Tablica ogłoszeń
description: Tablica ogłoszeń działkowców ROD im. Józefa Lompy w Woźnikach — sprzedam, oddam, kupię, szukam pomocy, zguby i znaleziska.
slug: tablica
---

# Tablica ogłoszeń działkowców

Miejsce na drobne ogłoszenia sąsiedzkie: sprzedam, oddam, kupię, szukam pomocy, zguby i znaleziska. Każde ogłoszenie sprawdza zarząd, zanim pojawi się na tablicy. Ogłoszenia znikają automatycznie po tygodniu — jeśli sprawa nadal aktualna, wyślij je ponownie.

:::html
<p class="form-ok" id="wyslano">Dziękujemy — ogłoszenie trafiło do zarządu. Po zatwierdzeniu pojawi się na tablicy.</p>
<p class="form-blad" id="blad">Nie udało się wysłać — wpisz tytuł, treść i zaznacz zgodę.</p>

<form class="kontakt-form tablica-form" method="post" action="/tablica/wyslij">
  <label>Kategoria
    <select name="kategoria" required>
      <option value="sprzedam">Sprzedam</option>
      <option value="oddam">Oddam za darmo</option>
      <option value="kupie">Kupię</option>
      <option value="pomoc">Szukam pomocy</option>
      <option value="zguby">Zguby i znaleziska</option>
      <option value="inne">Inne</option>
    </select>
  </label>
  <label>Tytuł ogłoszenia<input name="tytul" type="text" maxlength="100" required placeholder="np. Sprzedam kosiarkę spalinową"></label>
  <label>Treść<textarea name="tresc" rows="4" maxlength="600" required placeholder="Opisz krótko, czego dotyczy ogłoszenie"></textarea></label>
  <label>Kontakt (telefon lub e-mail)<input name="kontakt" type="text" maxlength="80" placeholder="żeby zainteresowani mogli się odezwać"></label>
  <div class="form-para">
    <label>Imię<input name="imie" type="text" maxlength="50" placeholder="opcjonalnie"></label>
    <label>Nr działki<input name="dzialka" type="text" maxlength="20" placeholder="opcjonalnie"></label>
  </div>
  <label class="form-zgoda"><input name="zgoda" type="checkbox" value="tak" required> Zgadzam się na publikację ogłoszenia z podanym kontaktem na stronie ROD.</label>
  <input class="pulapka" name="www" type="text" tabindex="-1" autocomplete="off" aria-hidden="true">
  <button class="button button-primary" type="submit">Wyślij ogłoszenie</button>
</form>
:::

## Aktualne ogłoszenia

{{tablica_ogloszen}}
