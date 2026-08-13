#!/bin/bash
# hilook_wczytaj.sh — bierze plik .txt wgrany przez panel /upload i przenosi dane
# logowania do /root/.hilook_cred. NIGDY nie drukuje hasla. Po wczytaniu kasuje zrodlo.
set -u
SRC_DIR=/root/hilook_wrzut
CRED=/root/.hilook_cred

PLIK=$(ls -t "$SRC_DIR"/*.txt 2>/dev/null | head -1)
if [ -z "${PLIK:-}" ]; then
  echo "BRAK PLIKU .txt w $SRC_DIR — Tomasz jeszcze nie wgral."
  exit 1
fi

echo "ZNALEZIONO: $(basename "$PLIK")  ($(stat -c%s "$PLIK") bajtow, $(stat -c%y "$PLIK" | cut -d. -f1))"

USER=""
PASS=""

# Wariant 1: klucz=wartosc (HILOOK_USER=..., HILOOK_PASS=... / user=, pass=, haslo=, login=)
while IFS= read -r linia; do
  linia=$(printf '%s' "$linia" | tr -d '\r')
  case "$(printf '%s' "$linia" | tr 'A-Z' 'a-z')" in
    hilook_user=*|user=*|login=*|uzytkownik=*) USER="${linia#*=}" ;;
    hilook_pass=*|pass=*|haslo=*|password=*)   PASS="${linia#*=}" ;;
  esac
done < "$PLIK"

# Wariant 2: goly tekst — pierwsza niepusta linia = haslo, user domyslnie admin
if [ -z "$PASS" ]; then
  PASS=$(grep -m1 -v '^[[:space:]]*$' "$PLIK" | tr -d '\r\n')
fi
[ -z "$USER" ] && USER=admin

if [ -z "$PASS" ]; then
  echo "PLIK PUSTY albo nie rozpoznano formatu. Nic nie zapisano."
  exit 1
fi

printf 'HILOOK_USER=%s\nHILOOK_PASS=%s\n' "$USER" "$PASS" > "$CRED"
chmod 600 "$CRED"

shred -u "$PLIK" 2>/dev/null || rm -f "$PLIK"

echo "ZAPISANO do $CRED"
echo "  uzytkownik: $USER"
echo "  haslo: ustawione, dlugosc ${#PASS} znakow (tresc NIE jest drukowana)"
echo "  plik zrodlowy skasowany z $SRC_DIR"
