#!/usr/bin/env python3
"""Fabryka VPS MCP server — full shell access for Claude.
Tools: execute_command, read_file, write_file, append_file, list_dir.
Every execute_command call is logged to /var/log/claude-mcp/audit.log."""
import os, subprocess, datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from mcp.server.fastmcp import FastMCP

SECRET = os.environ.get("CLAUDE_MCP_SECRET")
if not SECRET or len(SECRET) < 32:
    raise SystemExit("CLAUDE_MCP_SECRET env var must be a long random string (openssl rand -hex 32).")

LOG_DIR = Path("/var/log/claude-mcp")
LOG_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = LOG_DIR / "audit.log"
HOST = os.environ.get("MCP_HOST", "127.0.0.1")
PORT = int(os.environ.get("MCP_PORT", "8765"))

mcp = FastMCP("fabryka-vps")
mcp.settings.host = HOST
mcp.settings.port = PORT
mcp.settings.streamable_http_path = f"/mcp/{SECRET}"
mcp.settings.stateless_http = True

from mcp.server.transport_security import TransportSecuritySettings
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=["157-90-155-155.sslip.io", "127.0.0.1:*", "localhost:*"],
    allowed_origins=["https://157-90-155-155.sslip.io"],
)

def _audit(kind: str, detail: str) -> None:
    ts = datetime.datetime.now(STREFA_TOMASZA).isoformat(timespec="seconds")
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {kind}: {detail}\n")


# ==========================================================================
# ZACZEP — NIEMY REJESTRATOR (5.08.2026, D-0051)
# Zbudowany zgodnie z JEDNOMYSLNA rekomendacja zalogi (Zenek, Henio, Genek).
#
# CO ROBI: zapisuje surowe zdarzenia do .scratch/hans/most.jsonl.
# CZEGO NIE ROBI: NIC NIE OCENIA i NIC NIE DOKLEJA do wyniku narzedzia.
#   Zenek: „komunikat doklejony do wyniku przychodzi juz PO wykonaniu instalacji.
#   Nie zatrzyma biezacego odruchu." Ostrzeganie na zywo = interwencja, ktora
#   psuje pomiar. Ocenia HANS (tools/hans.py, wlasnosc Henia) z zewnatrz —
#   bo Klaudek nie moze byc sedzia we wlasnej sprawie.
#
# FAIL-OPEN: kazdy blad zapisu jest polykany. Most MUSI dzialac tak, jakby
#   zaczepu nie bylo. Utrata mostu = Klaudek traci dostep do serwera.
# WYLACZNIK: zmienna srodowiskowa ZACZEP_WYLACZONY=1 gasi go bez dotykania kodu.
# ==========================================================================
# CZAS TOMASZA — dekret 5.08.2026: „Poprawić i nigdy nie zgubić mojej godziny."
# Serwer chodzi na UTC. Zaczep zapisywal 07:39, gdy u Tomasza bylo 09:39 — przy zestawieniu
# z jego decyzjami i slowami wszystko wychodziloby przesuniete o 2 godziny.
# KAZDY znacznik czasu widziany przez Tomasza albo porownywany z jego zapisami
# MA BYC W JEGO STREFIE.
STREFA_TOMASZA = ZoneInfo("Europe/Vienna")

ZACZEP_PLIK = Path("/root/rod-ai-studio/.scratch/hans/most.jsonl")
_ZACZEP_WYLACZONY = os.environ.get("ZACZEP_WYLACZONY", "") in ("1", "true", "TRUE", "yes")

# wzorce rozstrzygalne, nie uznaniowe — Hans ma liczyc, nie interpretowac
_WZORCE_ZLECENIA = ("zaloga.py", "odpal.py", "hermes -z", "tools/dzwonek.py")
_WZORCE_NAPRAWY = ("pip install", "pip3 install", "apt-get install", "apt install",
                   "npm install", "npm i ", "systemctl restart", "systemctl start",
                   "systemctl stop", "docker restart", "pkill", "kill -9",
                   "systemd-run", "set-property", "bun install")


def _zaczep(narzedzie: str, tresc: str) -> None:
    """Niemy zapis zdarzenia. Nigdy nie rzuca wyjatkiem. Nigdy nic nie zwraca."""
    if _ZACZEP_WYLACZONY:
        return
    try:
        import json as _json
        t = (tresc or "")[:400]
        niski = t.lower()
        wpis = {
            "ts": datetime.datetime.now(STREFA_TOMASZA).isoformat(timespec="seconds"),
            "narzedzie": narzedzie,
            "zlecenie_dla_zalogi": any(w in t for w in _WZORCE_ZLECENIA),
            "wyglada_na_naprawe": any(w in niski for w in _WZORCE_NAPRAWY),
            "podglad": t[:160],
        }
        ZACZEP_PLIK.parent.mkdir(parents=True, exist_ok=True)
        with open(ZACZEP_PLIK, "a", encoding="utf-8") as f:
            f.write(_json.dumps(wpis, ensure_ascii=False) + "\n")
    except Exception:
        pass  # FAIL-OPEN — most dziala dalej, jakby zaczepu nie bylo

@mcp.tool()
def execute_command(command: str, cwd: str = None, timeout: int = 120) -> str:
    """Run a bash command on the VPS host, return stdout/stderr + exit code."""
    _audit("CMD", f"cwd={cwd!r} timeout={timeout} :: {command}")
    _zaczep("execute_command", command)
    try:
        result = subprocess.run(["bash", "-lc", command], cwd=cwd,
            capture_output=True, text=True, timeout=timeout)
        out, err = result.stdout or "", result.stderr or ""
        _audit("RESULT", f"exit_code={result.returncode} stdout_len={len(out)} stderr_len={len(err)}")
        return f"exit_code={result.returncode}\n--- stdout ---\n{out}\n--- stderr ---\n{err}"
    except subprocess.TimeoutExpired:
        _audit("TIMEOUT", command)
        return f"TIMEOUT after {timeout}s"
    except Exception as e:
        _audit("ERROR", f"{command} :: {e}")
        return f"ERROR: {e}"

@mcp.tool()
def read_file(path: str) -> str:
    """Read and return the full text content of a file on the VPS."""
    _audit("READ", path)
    _zaczep("read_file", path)
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"ERROR reading {path}: {e}"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Create or overwrite a file on the VPS with the given content."""
    _audit("WRITE", f"{path} ({len(content)} chars)")
    _zaczep("write_file", path)
    try:
        p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"OK wrote {len(content)} chars to {path}"
    except Exception as e:
        return f"ERROR writing {path}: {e}"

@mcp.tool()
def append_file(path: str, content: str) -> str:
    """Append content to the end of a file on the VPS."""
    _audit("APPEND", f"{path} (+{len(content)} chars)")
    _zaczep("append_file", path)
    try:
        p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "a", encoding="utf-8") as f:
            f.write(content)
        return f"OK appended {len(content)} chars to {path}"
    except Exception as e:
        return f"ERROR appending {path}: {e}"

@mcp.tool()
def list_dir(path: str = ".") -> str:
    """List files/directories at path (like ls -la)."""
    _audit("LIST", path)
    _zaczep("list_dir", path)
    try:
        result = subprocess.run(["ls", "-la", path], capture_output=True, text=True, timeout=15)
        return result.stdout or result.stderr
    except Exception as e:
        return f"ERROR listing {path}: {e}"

if __name__ == "__main__":
    print(f"Fabryka VPS MCP server on {HOST}:{PORT}, audit log: {AUDIT_LOG}")
    mcp.run(transport="streamable-http")
