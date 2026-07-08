#!/usr/bin/env python3
"""Fabryka VPS MCP server — full shell access for Claude.
Tools: execute_command, read_file, write_file, append_file, list_dir.
Every execute_command call is logged to /var/log/claude-mcp/audit.log."""
import os, subprocess, datetime
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

def _audit(kind: str, detail: str) -> None:
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {kind}: {detail}\n")

@mcp.tool()
def execute_command(command: str, cwd: str = None, timeout: int = 120) -> str:
    """Run a bash command on the VPS host, return stdout/stderr + exit code."""
    _audit("CMD", f"cwd={cwd!r} timeout={timeout} :: {command}")
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
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"ERROR reading {path}: {e}"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Create or overwrite a file on the VPS with the given content."""
    _audit("WRITE", f"{path} ({len(content)} chars)")
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
    try:
        result = subprocess.run(["ls", "-la", path], capture_output=True, text=True, timeout=15)
        return result.stdout or result.stderr
    except Exception as e:
        return f"ERROR listing {path}: {e}"

if __name__ == "__main__":
    print(f"Fabryka VPS MCP server on {HOST}:{PORT}, audit log: {AUDIT_LOG}")
    mcp.run(transport="streamable-http")
