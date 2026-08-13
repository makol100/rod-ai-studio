#!/usr/bin/env python3
"""Wywolanie narzedzia na serwerze MCP Wybickiego (Sosnowiec) — bez lacznika w aplikacji.

Powstalo 5.08.2026: klucz dlugoterminowy HA NIE SIEGA Supervisora (401 na /api/hassio/*),
wiec dodatkow nie da sie instalowac zwyklym API. ALE dodatek ha-mcp dziala WEWNATRZ HA
i ma wlasny token Supervisora — wiec robi to, czego klucz nie moze.

Uzycie:
  python3 tools/mcp_wybickiego.py --lista
  python3 tools/mcp_wybickiego.py --narzedzie ha_manage_addon --argumenty '{"slug":"core_ssh","action":"install"}'
"""
import argparse
import json
import urllib.request

BAZA = "http://100.67.61.100:9583/private_1S_c5tNNIZ_qWO_4Ks777A"


def _zapytaj(tresc, sesja=None):
    naglowki = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if sesja:
        naglowki["mcp-session-id"] = sesja
    req = urllib.request.Request(BAZA, data=json.dumps(tresc).encode(), headers=naglowki)
    with urllib.request.urlopen(req, timeout=300) as o:
        sid = o.headers.get("mcp-session-id")
        surowe = o.read().decode("utf-8", errors="replace")
    dane = None
    for linia in surowe.splitlines():
        if linia.startswith("data: "):
            dane = json.loads(linia[6:])
    return dane, sid


def polacz():
    odp, sid = _zapytaj({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "klaudek", "version": "1"}},
    })
    _zapytaj({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    return sid


def main():
    a = argparse.ArgumentParser(description="Narzedzia MCP Wybickiego")
    a.add_argument("--lista", action="store_true")
    a.add_argument("--narzedzie")
    a.add_argument("--argumenty", default="{}")
    args = a.parse_args()

    sid = polacz()

    if args.lista:
        odp, _ = _zapytaj({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, sid)
        for t in odp.get("result", {}).get("tools", []):
            print(f"  {t['name']}")
        return

    if not args.narzedzie:
        a.error("podaj --narzedzie albo --lista")

    odp, _ = _zapytaj({
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": args.narzedzie, "arguments": json.loads(args.argumenty)},
    }, sid)

    w = odp.get("result", {})
    for c in w.get("content", []):
        if c.get("type") == "text":
            print(c["text"])
    if odp.get("error"):
        print("BLAD:", json.dumps(odp["error"])[:400])


if __name__ == "__main__":
    main()
