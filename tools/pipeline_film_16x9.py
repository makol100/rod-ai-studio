#!/usr/bin/env python3
"""Jedna komenda: scenariusz Pythona -> kadry -> montaz -> kontrola -> eksport.

Scenariusz musi byc istniejacym skryptem korzystajacym z film_rod/buduj_film.py.
Pipeline nie generuje mediow i akceptuje tylko material obecny na dysku.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("scenariusz", type=Path, help="istniejacy skrypt scenariusza .py")
    p.add_argument("--master", type=Path, required=True, help="plik tworzony przez scenariusz")
    p.add_argument("--eksport", type=Path, required=True)
    p.add_argument("--planowane-ciecia", type=int, required=True,
                   help="liczba cieć wynikajaca ze scenariusza; obce ciecia nadal blokuja eksport")
    p.add_argument("--tylko-kontrola", action="store_true")
    args = p.parse_args()
    scenario = args.scenariusz.resolve()
    master = args.master.resolve()
    if not scenario.is_file():
        p.error(f"brak scenariusza: {scenario}")
    if scenario.suffix != ".py":
        p.error("scenariusz musi byc skryptem .py")
    if not args.tylko_kontrola:
        run([sys.executable, str(scenario)])
    if not master.is_file():
        raise SystemExit(f"BRAK MASTER po montazu: {master}")
    run([sys.executable, str(ROOT / "tools/straznik.py"), str(master),
         "--exp-w", "1920", "--exp-h", "1080", "--final", str(args.planowane_ciecia),
         "--freeze-ok", "--json"])
    args.eksport.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(master, args.eksport)
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration",
                            "-of", "json", str(args.eksport)], check=True, capture_output=True, text=True)
    print(json.dumps({"status": "OK", "eksport": str(args.eksport), "ffprobe": json.loads(probe.stdout)},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
