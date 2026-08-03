# Usługi Hansa (wdrożone 4.08.2026, 01:41)

Kopie z `/etc/systemd/system/` — trzymane w repo, żeby po przenosinach serwera
nie trzeba było ich odtwarzać z pamięci.

- `hans-ucho.service` — nasłuch wiadomości Tomasza na `@HansFabrykaRolek_bot` co 60 s.
  Zapisuje jego słowa do `wiedza/SLOWA_TOMASZA.md` **bez pośrednictwa Klaudka**.
  To zrywa zależność kołową: dotąd słowa Tomasza zapisywał Klaudek, więc jeśli
  wypadły mu z kontekstu zanim je zapisał — nie zapisywały się wcale.
- `hans-oczy.service` + `.timer` — co 15 minut skanuje repo i szuka
  **niedokończonych śladów Klaudka** (kod zmieniony bez aktualizacji wiedzy).

Instalacja: `cp *.service *.timer /etc/systemd/system/ && systemctl daemon-reload
&& systemctl enable --now hans-ucho.service hans-oczy.timer`
