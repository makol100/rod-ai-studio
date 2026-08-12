#!/usr/bin/env python3
"""Bezpieczny klient Gemini Image Zenka.

Bez --zaplac nie wysyla zadania generacji: wolno tylko listowac modele i
wydrukowac request. Klucz jest czytany z GEMINI_API_KEY lub repozytoryjnego .env.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://generativelanguage.googleapis.com/v1beta"
# MARTWE NA NASZYM KONCIE (usuniete 12.08.2026 po tescie): imagen-4.0-fast-generate-001
# -> API 404 "no longer available to new users". Nie przywracac bez ponownego testu.
MODELE = {
    "gemini-3.1-flash-image": ("gemini-3.1-flash-image", 0.067, "generateContent"),
    "nano-banana-pro": ("nano-banana-pro-preview", 0.134, "generateContent"),
    "nano-banana-pro-preview": ("nano-banana-pro-preview", 0.134, "generateContent"),
}


def klucz() -> str:
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    env = ROOT / ".env"
    if env.exists():
        for raw in env.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                if name.strip() == "GEMINI_API_KEY":
                    return value.strip().strip("'\"")
    raise SystemExit("BRAK AUTH: ustaw GEMINI_API_KEY albo wpisz go do .env")


def request_json(method: str, url: str, key: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:1000]
        raise SystemExit(f"API HTTP {exc.code}: {detail}") from exc


def lista_modeli(key: str) -> int:
    result = request_json("GET", f"{API}/models?pageSize=1000", key)
    names = sorted(x.get("name", "") for x in result.get("models", []))
    image = [n for n in names if "image" in n.lower() or "imagen" in n.lower() or "banana" in n.lower()]
    print(json.dumps({"auth": "OK", "liczba_modeli": len(names), "modele_obrazowe": image},
                     ensure_ascii=False, indent=2))
    return 0


def opis_requestu(model_alias: str, prompt: str, aspect: str, resolution: str) -> tuple[str, dict, float]:
    model, cena_2k, metoda = MODELE[model_alias]
    if metoda == "predict":
        payload = {"instances": [{"prompt": prompt}],
                   "parameters": {"sampleCount": 1, "aspectRatio": aspect}}
    else:
        payload = {"contents": [{"parts": [{"text": prompt}]}],
                   "generationConfig": {"responseModalities": ["TEXT", "IMAGE"],
                                        "imageConfig": {"aspectRatio": aspect, "imageSize": resolution}}}
    url = f"{API}/models/{model}:{metoda}"
    cena = 0.24 if model == "nano-banana-pro-preview" and resolution == "4K" else cena_2k
    return url, payload, cena


def zapisz_obraz(response: dict, output: Path) -> None:
    candidates = response.get("candidates", [])
    parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
    encoded = next((p.get("inlineData", {}).get("data") for p in parts if p.get("inlineData")), None)
    if encoded is None:
        predictions = response.get("predictions", [])
        encoded = predictions[0].get("bytesBase64Encoded") if predictions else None
    if not encoded:
        raise SystemExit("API nie zwrocilo obrazu; odpowiedz: " + json.dumps(response)[:1000])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(base64.b64decode(encoded))


def main() -> int:
    p = argparse.ArgumentParser(description="Gemini Image z twarda bramka kosztowa")
    p.add_argument("--lista", action="store_true", help="darmowa walidacja auth przez models.list")
    p.add_argument("--model", choices=sorted(MODELE), default="gemini-3.1-flash-image")
    p.add_argument("--prompt")
    p.add_argument("--aspect", default="16:9")
    p.add_argument("--resolution", choices=("1K", "2K", "4K"), default="1K")
    p.add_argument("--output", type=Path, default=Path("obraz.png"))
    p.add_argument("--zaplac", action="store_true", help="JAWNA zgoda na jedno platne wywolanie")
    args = p.parse_args()
    if args.lista:
        return lista_modeli(klucz())
    if not args.prompt:
        p.error("wymagane --prompt albo --lista")
    url, payload, cena = opis_requestu(args.model, args.prompt, args.aspect, args.resolution)
    dry = {"tryb": "PLATNY" if args.zaplac else "DRY-RUN (NIC NIE WYSLANO)",
           "szacowany_koszt_usd": cena, "url": url, "request": payload, "output": str(args.output)}
    print(json.dumps(dry, ensure_ascii=False, indent=2))
    if not args.zaplac:
        return 0
    print(f"PLATNE WYWOŁANIE: maksymalny szacunek {cena:.3f} USD", file=sys.stderr)
    response = request_json("POST", url, klucz(), payload)
    zapisz_obraz(response, args.output)
    print(f"ZAPISANO {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
