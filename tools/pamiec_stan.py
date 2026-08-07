#!/usr/bin/env python3
"""Krotkoterminowy rejestr stanu zadania z odwracalnym drill-downem."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
STATUSES = ("zrobione", "w_toku", "bloker")
GRAPH_CAP = 4000
AGENT_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
LINE_RANGE_PATTERN = re.compile(r"^(\d+):(\d+)$")
MOST_SOURCE = ".scratch/hans/most.jsonl"


class StanError(Exception):
    pass


def agent_paths(agent: str) -> tuple[Path, Path, Path]:
    state_dir = ROOT / ".scratch" / "stan" / agent
    refs_dir = ROOT / ".scratch" / "refs" / agent
    return state_dir, refs_dir, state_dir / "rejestr.jsonl"


def load_nodes(agent: str) -> list[dict]:
    _, _, registry = agent_paths(agent)
    if not registry.exists():
        return []
    nodes = []
    for number, line in enumerate(registry.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            node = json.loads(line)
        except json.JSONDecodeError as error:
            raise StanError(f"bledny JSONL, linia {number}: {error}") from error
        nodes.append(node)
    return nodes


def source_path(source: str) -> Path:
    path = Path(source)
    return path if path.is_absolute() else ROOT / path


def most_fragment(range_spec: str) -> tuple[bytes, str | None]:
    path = source_path(MOST_SOURCE)
    if not path.is_file():
        return b"", f"most nie istnieje: {MOST_SOURCE}"
    lines = path.read_bytes().splitlines(keepends=True)
    line_match = LINE_RANGE_PATTERN.fullmatch(range_spec)
    if line_match:
        start, end = map(int, line_match.groups())
        if start < 1 or end < start or end > len(lines):
            return b"", f"zakres linii {range_spec} nie istnieje w {MOST_SOURCE}"
        return b"".join(lines[start - 1 : end]), None
    if ".." not in range_spec:
        return b"", f"bledny zakres mostu: {range_spec}"
    start_text, end_text = range_spec.split("..", 1)
    try:
        start = datetime.fromisoformat(start_text)
        end = datetime.fromisoformat(end_text)
    except ValueError:
        return b"", f"bledny zakres czasu mostu: {range_spec}"
    if end < start:
        return b"", f"odwrocony zakres czasu mostu: {range_spec}"
    selected = []
    for number, raw_line in enumerate(lines, 1):
        try:
            timestamp = datetime.fromisoformat(json.loads(raw_line)["ts"])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            continue
        try:
            in_range = start <= timestamp <= end
        except TypeError:
            return b"", f"niezgodne strefy czasowe zakresu i mostu: {range_spec}"
        if in_range:
            selected.append(raw_line)
    if not selected:
        return b"", f"zakres czasu {range_spec} jest pusty w {MOST_SOURCE}"
    return b"".join(selected), None


def source_warning(node: dict) -> str | None:
    if "zrodlo_most" in node:
        _, warning = most_fragment(node["zrodlo_most"])
        return warning
    if not source_path(node["zrodlo"]).is_file():
        return f'brak pliku zrodlowego: {node["zrodlo"]}'
    return None


def validate_sources(nodes: list[dict]) -> list[str]:
    return [node["node_id"] for node in nodes if source_warning(node)]


def warn(message: str) -> None:
    print(f"OSTRZEZENIE: {message}", file=sys.stderr)


def mermaid_label(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', "'").replace("\n", " ")


def render_graph(nodes: list[dict], collapsed: set[str] | None = None) -> str:
    collapsed = collapsed or set()
    visible = [node for node in nodes if node["node_id"] not in collapsed]
    lines = ["# STAN", "", "```mermaid", "graph TD"]
    if collapsed:
        lines.append(f'  done_collapsed["[... {len(collapsed)} zrobionych ...]"]')
    for node in visible:
        label = mermaid_label(f'{node["node_id"]} | {node["status"]} | {node["opis"]}')
        lines.append(f'  {node["node_id"]}["{label}"]')
    visible_ids = {node["node_id"] for node in visible}
    edges: set[tuple[str, str]] = set()
    for node in visible:
        for dependency in node.get("zaleznosci", []):
            if dependency in visible_ids:
                edges.add((dependency, node["node_id"]))
            elif dependency in collapsed:
                edges.add(("done_collapsed", node["node_id"]))
    lines.extend(f"  {start} --> {end}" for start, end in sorted(edges))
    lines.extend(
        [
            "  classDef zrobione fill:#d8f3dc,stroke:#2d6a4f",
            "  classDef w_toku fill:#fff3bf,stroke:#e67700",
            "  classDef bloker fill:#ffe3e3,stroke:#c92a2a",
        ]
    )
    for status in STATUSES:
        ids = [node["node_id"] for node in visible if node["status"] == status]
        if ids:
            lines.append(f"  class {','.join(ids)} {status}")
    lines.extend(["```", ""])
    return "\n".join(lines)


def capped_graph(nodes: list[dict]) -> str:
    graph = render_graph(nodes)
    if len(graph) <= GRAPH_CAP:
        return graph
    completed = [node["node_id"] for node in nodes if node["status"] == "zrobione"]
    collapsed: set[str] = set()
    for node_id in completed:
        collapsed.add(node_id)
        graph = render_graph(nodes, collapsed)
        if len(graph) <= GRAPH_CAP:
            return graph
    raise StanError("graf przekracza 4000 znakow mimo zwiniecia wszystkich wezlow zrobionych")


def command_add(args: argparse.Namespace) -> None:
    state_dir, refs_dir, registry = agent_paths(args.agent)
    nodes = load_nodes(args.agent)
    existing_ids = {node["node_id"] for node in nodes}
    dependencies = [value for value in (args.zaleznosci or "").split(",") if value]
    unknown = [value for value in dependencies if value not in existing_ids]
    if unknown:
        raise StanError(f"nieistniejace zaleznosci: {','.join(unknown)}")
    next_number = max((int(node["node_id"][1:]) for node in nodes), default=0) + 1
    node_id = f"n{next_number:03d}"

    state_dir.mkdir(parents=True, exist_ok=True)
    source_range = None
    if args.tresc_z_stdin:
        refs_dir.mkdir(parents=True, exist_ok=True)
        raw = sys.stdin.buffer.read()
        path = refs_dir / f"{node_id}.md"
        path.write_bytes(raw)
        source = path.relative_to(ROOT).as_posix()
    elif args.zrodlo_most:
        source = MOST_SOURCE
        source_range = args.zrodlo_most
        _, warning = most_fragment(source_range)
        if warning:
            warn(warning)
    else:
        path = source_path(args.zrodlo)
        if not path.is_file():
            raise StanError(f"zrodlo nie istnieje: {args.zrodlo}")
        try:
            source = path.resolve().relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            source = str(path.resolve())

    node = {
        "node_id": node_id,
        "ts": datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M"),
        "opis": args.opis,
        "status": args.status,
        "zrodlo": source,
        "zaleznosci": dependencies,
    }
    if source_range is not None:
        node["zrodlo_most"] = source_range
    with registry.open("a", encoding="utf-8") as registry_file:
        registry_file.write(json.dumps(node, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(node_id)


def command_graph(args: argparse.Namespace) -> None:
    state_dir, _, _ = agent_paths(args.agent)
    graph_path = state_dir / "graf.md"
    nodes = load_nodes(args.agent)
    missing = validate_sources(nodes)
    if missing:
        for node in nodes:
            warning = source_warning(node)
            if warning:
                warn(f'{node["node_id"]}: {warning}')
    graph = capped_graph(nodes)
    state_dir.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(graph, encoding="utf-8")
    print(graph_path.relative_to(ROOT))


def command_show(args: argparse.Namespace) -> None:
    state_dir, _, _ = agent_paths(args.agent)
    graph_path = state_dir / "graf.md"
    if not args.node_id:
        if not graph_path.is_file():
            raise StanError("graf.md nie istnieje; uruchom najpierw: graf")
        sys.stdout.write(graph_path.read_text(encoding="utf-8"))
        return
    nodes = {node["node_id"]: node for node in load_nodes(args.agent)}
    if args.node_id not in nodes:
        raise StanError(f"nieznany node_id: {args.node_id}")
    node = nodes[args.node_id]
    if "zrodlo_most" in node:
        fragment, warning = most_fragment(node["zrodlo_most"])
        if warning:
            warn(f'{args.node_id}: {warning}')
        sys.stdout.buffer.write(fragment)
        return
    path = source_path(node["zrodlo"])
    if not path.is_file():
        raise StanError(f"brak pliku zrodlowego dla: {args.node_id}")
    sys.stdout.buffer.write(path.read_bytes())


def command_status(args: argparse.Namespace) -> None:
    nodes = load_nodes(args.agent)
    counts = Counter(node["status"] for node in nodes)
    missing = validate_sources(nodes)
    print(f"wezlow: {len(nodes)}")
    print(f"w_toku: {counts['w_toku']}")
    print(f"bloker: {counts['bloker']}")
    print(f"wszystkie_zrodla_istnieja: {'nie' if missing else 'tak'}")
    if missing:
        print(f"brak_zrodel: {','.join(missing)}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    default_agent = os.environ.get("STAN_AGENT", "klaudek")
    root.add_argument("--agent", default=default_agent, help="przestrzen stanu agenta")
    commands = root.add_subparsers(dest="command", required=True)
    add = commands.add_parser("dodaj")
    add.add_argument("--agent", default=argparse.SUPPRESS, help="przestrzen stanu agenta")
    add.add_argument("--opis", required=True)
    add.add_argument("--status", choices=STATUSES, required=True)
    sources = add.add_mutually_exclusive_group(required=True)
    sources.add_argument("--zrodlo")
    sources.add_argument("--zrodlo-most")
    add.add_argument("--zaleznosci")
    sources.add_argument("--tresc-z-stdin", action="store_true")
    add.set_defaults(handler=command_add)
    graph = commands.add_parser("graf")
    graph.add_argument("--agent", default=argparse.SUPPRESS, help="przestrzen stanu agenta")
    graph.set_defaults(handler=command_graph)
    show = commands.add_parser("pokaz")
    show.add_argument("--agent", default=argparse.SUPPRESS, help="przestrzen stanu agenta")
    show.add_argument("--node_id")
    show.set_defaults(handler=command_show)
    status = commands.add_parser("status")
    status.add_argument("--agent", default=argparse.SUPPRESS, help="przestrzen stanu agenta")
    status.set_defaults(handler=command_status)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if not AGENT_PATTERN.fullmatch(args.agent):
            raise StanError("agent moze zawierac tylko litery, cyfry, _ i -")
        args.handler(args)
    except (StanError, KeyError, ValueError) as error:
        print(f"BLAD: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
