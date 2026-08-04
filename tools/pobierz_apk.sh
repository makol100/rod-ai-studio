#!/usr/bin/env bash
# POBIERZ APK — sciaga najnowsza zbudowana aplikacje z wydania GitHub do data/rolka-prad/
#
# Zbudowane 4.08.2026 na polecenie Tomasza: "Automatyzacja kopiowania aplikacji po kazdym
# zbudowaniu wykonac". Watek lezal otwarty od 15.07 z notatka:
#   "Po kazdym buildzie skopiowac nowy APK do data/rolka-prad/app-debug.apk (TODO: zautomatyzowac)"
#
# DLACZEGO TAK, A NIE PRZEZ COMMIT W WORKFLOW:
# APK ma 2,3 MB i NIE JEST sledzony w gicie (sprawdzone: git ls-files -> pusto, 0 commitow).
# Wgrywanie go przy kazdym budowaniu wsadzaloby binaria do historii — dokladnie to, czego
# Tomasz nie chcial przy rolkach (D-0020: "nie robimy kopii gotowych rolek na GitHubie").
# Przeplyw .github/workflows/build-apk.yml JUZ publikuje APK jako wydanie 'apk-latest'.
# Wiec zamiast dublowac plik w repo — pobieramy go z wydania. Repo zostaje czyste,
# a plik lokalny jest zawsze najswiezszy.
#
# Uzycie:
#   tools/pobierz_apk.sh            # pobierz, jesli wydanie jest nowsze niz plik lokalny
#   tools/pobierz_apk.sh --zawsze   # pobierz bezwarunkowo
#   tools/pobierz_apk.sh --sprawdz  # tylko sprawdz, nic nie pobieraj

set -uo pipefail

REPO_KAT="/root/rod-ai-studio"
CEL="$REPO_KAT/data/rolka-prad/app-debug.apk"
ZRODLO="https://github.com/makol100/rod-ai-studio/releases/download/apk-latest/app-debug.apk"
API="https://api.github.com/repos/makol100/rod-ai-studio/releases/tags/apk-latest"

TRYB="${1:-}"

czas_tomasza() { TZ=Europe/Vienna date "+%d.%m.%Y %H:%M"; }

# data ostatniej publikacji wydania
DATA_WYDANIA=$(curl -sS -m 30 "$API" 2>/dev/null \
  | python3 -c "import sys,json;print(json.load(sys.stdin).get('published_at',''))" 2>/dev/null)

if [ -z "$DATA_WYDANIA" ]; then
  echo "[apk] NIE MOGE odczytac wydania (brak sieci albo wydania jeszcze nie ma)"
  echo "[apk] plik lokalny zostaje nietkniety: $CEL"
  exit 1
fi

STEMPEL_WYDANIA=$(date -d "$DATA_WYDANIA" +%s 2>/dev/null || echo 0)
STEMPEL_LOKALNY=$(stat -c%Y "$CEL" 2>/dev/null || echo 0)

echo "[apk] wydanie:      $(date -d "$DATA_WYDANIA" "+%d.%m.%Y %H:%M" 2>/dev/null)"
if [ "$STEMPEL_LOKALNY" -gt 0 ]; then
  echo "[apk] plik lokalny: $(date -d "@$STEMPEL_LOKALNY" "+%d.%m.%Y %H:%M")"
else
  echo "[apk] plik lokalny: BRAK"
fi

if [ "$TRYB" = "--sprawdz" ]; then
  if [ "$STEMPEL_WYDANIA" -gt "$STEMPEL_LOKALNY" ]; then
    echo "[apk] JEST NOWSZA WERSJA do pobrania"
    exit 10
  fi
  echo "[apk] plik lokalny jest aktualny"
  exit 0
fi

if [ "$TRYB" != "--zawsze" ] && [ "$STEMPEL_WYDANIA" -le "$STEMPEL_LOKALNY" ]; then
  echo "[apk] plik lokalny juz aktualny — nic nie pobieram"
  exit 0
fi

mkdir -p "$(dirname "$CEL")"
TMP="$CEL.pobierany"
if ! curl -sSL -m 300 -o "$TMP" "$ZRODLO" 2>/dev/null; then
  echo "[apk] BLAD pobierania — plik lokalny NIETKNIETY"
  rm -f "$TMP"
  exit 1
fi

# sprawdzenie, czy to naprawde APK (plik ZIP zaczyna sie od PK)
if [ "$(head -c2 "$TMP" 2>/dev/null)" != "PK" ] || [ ! -s "$TMP" ]; then
  echo "[apk] POBRANY PLIK NIE JEST APK — odrzucam, plik lokalny NIETKNIETY"
  rm -f "$TMP"
  exit 1
fi

# kopia poprzedniej wersji — dekret Tomasza 2.08: nikt niczego nie usuwa
if [ -f "$CEL" ]; then
  cp -a "$CEL" "$CEL.poprzedni"
fi
mv "$TMP" "$CEL"
echo "[apk] POBRANO: $(du -h "$CEL" | cut -f1), $(czas_tomasza)"
[ -f "$CEL.poprzedni" ] && echo "[apk] poprzednia wersja zachowana: $CEL.poprzedni"
exit 0
