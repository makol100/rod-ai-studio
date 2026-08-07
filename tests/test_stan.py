#!/usr/bin/env python3
"""Test akceptacyjny prototypu pamieci roboczej STAN."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "pamiec_stan.py"


class PamiecStanTest(unittest.TestCase):
    def run_stan(
        self,
        cwd: Path,
        *args: str,
        stdin: bytes | None = None,
        agent_env: str | None = None,
    ) -> subprocess.CompletedProcess[bytes]:
        environment = os.environ.copy()
        environment.pop("STAN_AGENT", None)
        if agent_env is not None:
            environment["STAN_AGENT"] = agent_env
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd,
            input=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
            check=True,
        )

    def test_petla_zdaj_oblej_po_kompakcji(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            workspace = Path(temporary_directory)
            source_dir = workspace / ".scratch" / "material"
            source_dir.mkdir(parents=True)

            nodes = [
                ("Rozpoznano wymagania", "zrobione", [], "dowod-1\n"),
                ("Wybrano format JSONL", "zrobione", ["n001"], "dowod-2\n"),
                ("Zapisano decyzje", "zrobione", ["n002"], "dowod-3\n"),
                ("Sprawdzono zaleznosci", "zrobione", ["n002"], "dowod-4\n"),
                ("Trwa implementacja", "w_toku", ["n003", "n004"], None),
                ("Brakuje odpowiedzi API", "bloker", ["n005"], None),
                ("Trwa kontrola limitu", "w_toku", ["n005"], "dowod-7\n"),
                ("Przygotowano raport", "zrobione", ["n006", "n007"], "dowod-8\n"),
            ]
            offloads = {
                "n005": b"pelny surowy log\x00\nlinia druga\n" + "UTF-8: lodz\n".encode("utf-8"),
                "n006": b"odpowiedz serwera: 503\r\nretry-after: 17\r\n",
            }

            for index, (opis, status, dependencies, source_text) in enumerate(nodes, 1):
                node_id = f"n{index:03d}"
                arguments = ["dodaj", "--opis", opis, "--status", status]
                if dependencies:
                    arguments += ["--zaleznosci", ",".join(dependencies)]
                if node_id in offloads:
                    arguments.append("--tresc-z-stdin")
                    result = self.run_stan(workspace, *arguments, stdin=offloads[node_id])
                else:
                    source = source_dir / f"{node_id}.txt"
                    source.write_text(source_text or "", encoding="utf-8")
                    arguments += ["--zrodlo", str(source.relative_to(workspace))]
                    result = self.run_stan(workspace, *arguments)
                self.assertIn(node_id.encode(), result.stdout)

            self.run_stan(workspace, "graf")
            graph_path = workspace / ".scratch" / "stan" / "klaudek" / "graf.md"
            graph = graph_path.read_text(encoding="utf-8")
            self.assertIn("graph TD", graph)
            self.assertLess(len(graph), 4000)
            for index in range(1, 9):
                self.assertIn(f"n{index:03d}", graph)

            registry_path = workspace / ".scratch" / "stan" / "klaudek" / "rejestr.jsonl"
            registry = [json.loads(line) for line in registry_path.read_text().splitlines()]
            self.assertEqual(8, len(registry))
            for node in registry:
                self.assertTrue((workspace / node["zrodlo"]).is_file(), node["node_id"])

            # Symulacja kompakcji: dalsze odtwarzanie korzysta tylko z grafu.
            expected_from_graph = {
                node_id: (opis, status, dependencies)
                for node_id, (opis, status, dependencies, _) in zip(
                    (f"n{i:03d}" for i in range(1, 9)), nodes
                )
            }
            compacted_graph = graph
            for node_id, (opis, status, dependencies) in expected_from_graph.items():
                self.assertRegex(compacted_graph, rf"{node_id}[^\n]*{re.escape(opis)}")
                self.assertRegex(compacted_graph, rf"{node_id}[^\n]*{status}")
                for dependency in dependencies:
                    self.assertRegex(compacted_graph, rf"{dependency}\s*-->\s*{node_id}")

            active_ids = set(
                re.findall(r"\b(n\d{3})\b[^\n]*(?:w_toku|bloker)", compacted_graph)
            )
            self.assertEqual({"n005", "n006", "n007"}, active_ids)
            for node_id in ("n005", "n006"):
                drill_down = self.run_stan(workspace, "pokaz", "--node_id", node_id)
                self.assertEqual(offloads[node_id], drill_down.stdout)

            status = self.run_stan(workspace, "status").stdout.decode("utf-8")
            self.assertIn("wezlow: 8", status)
            self.assertIn("w_toku: 2", status)
            self.assertIn("bloker: 1", status)
            self.assertIn("wszystkie_zrodla_istnieja: tak", status)

    def test_agenci_maja_osobne_przestrzenie_i_node_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            workspace = Path(temporary_directory)
            klaudek_raw = b"dowod Klaudka\n"
            zenek_raw = b"dowod Zenka\n"

            klaudek = self.run_stan(
                workspace,
                "--agent",
                "klaudek",
                "dodaj",
                "--opis",
                "Krok Klaudka",
                "--status",
                "w_toku",
                "--tresc-z-stdin",
                stdin=klaudek_raw,
            )
            zenek = self.run_stan(
                workspace,
                "dodaj",
                "--opis",
                "Krok Zenka",
                "--status",
                "bloker",
                "--tresc-z-stdin",
                stdin=zenek_raw,
                agent_env="zenek",
            )
            self.assertEqual(b"n001\n", klaudek.stdout)
            self.assertEqual(b"n001\n", zenek.stdout)

            for agent in ("klaudek", "zenek"):
                self.run_stan(workspace, "--agent", agent, "graf")

            klaudek_registry = workspace / ".scratch" / "stan" / "klaudek" / "rejestr.jsonl"
            zenek_registry = workspace / ".scratch" / "stan" / "zenek" / "rejestr.jsonl"
            self.assertIn("Krok Klaudka", klaudek_registry.read_text(encoding="utf-8"))
            self.assertNotIn("Krok Zenka", klaudek_registry.read_text(encoding="utf-8"))
            self.assertIn("Krok Zenka", zenek_registry.read_text(encoding="utf-8"))
            self.assertNotIn("Krok Klaudka", zenek_registry.read_text(encoding="utf-8"))

            klaudek_ref = workspace / ".scratch" / "refs" / "klaudek" / "n001.md"
            zenek_ref = workspace / ".scratch" / "refs" / "zenek" / "n001.md"
            self.assertEqual(klaudek_raw, klaudek_ref.read_bytes())
            self.assertEqual(zenek_raw, zenek_ref.read_bytes())
            self.assertEqual(
                klaudek_raw,
                self.run_stan(workspace, "--agent", "klaudek", "pokaz", "--node_id", "n001").stdout,
            )
            self.assertEqual(
                zenek_raw,
                self.run_stan(workspace, "--agent", "zenek", "pokaz", "--node_id", "n001").stdout,
            )

            klaudek_graph = (workspace / ".scratch" / "stan" / "klaudek" / "graf.md").read_text()
            zenek_graph = (workspace / ".scratch" / "stan" / "zenek" / "graf.md").read_text()
            self.assertIn("Krok Klaudka", klaudek_graph)
            self.assertNotIn("Krok Zenka", klaudek_graph)
            self.assertIn("Krok Zenka", zenek_graph)
            self.assertNotIn("Krok Klaudka", zenek_graph)

    def test_zrodlo_most_drill_down_wycina_wskazany_fragment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            workspace = Path(temporary_directory)
            most = workspace / ".scratch" / "hans" / "most.jsonl"
            most.parent.mkdir(parents=True)
            lines = [
                b'{"ts":"2026-08-06T10:00:00","podglad":"pierwszy"}\n',
                b'{"ts":"2026-08-06T10:01:00","podglad":"drugi"}\n',
                b'{"ts":"2026-08-06T10:02:00","podglad":"trzeci"}\n',
                b'{"ts":"2026-08-06T10:03:00","podglad":"czwarty"}\n',
            ]
            most.write_bytes(b"".join(lines))

            added = self.run_stan(
                workspace,
                "dodaj",
                "--opis",
                "Dowod z mostu",
                "--status",
                "w_toku",
                "--zrodlo-most",
                "2:3",
            )
            self.assertEqual(b"n001\n", added.stdout)
            registry_path = workspace / ".scratch" / "stan" / "klaudek" / "rejestr.jsonl"
            node = json.loads(registry_path.read_text(encoding="utf-8"))
            self.assertEqual(".scratch/hans/most.jsonl", node["zrodlo"])
            self.assertEqual("2:3", node["zrodlo_most"])

            drill_down = self.run_stan(workspace, "pokaz", "--node_id", "n001")
            self.assertEqual(b"".join(lines[1:3]), drill_down.stdout)
            self.assertEqual(b"", drill_down.stderr)

            by_time = self.run_stan(
                workspace,
                "dodaj",
                "--opis",
                "Dowod z mostu po czasie",
                "--status",
                "zrobione",
                "--zrodlo-most",
                "2026-08-06T10:01:00..2026-08-06T10:02:00",
            )
            self.assertEqual(b"n002\n", by_time.stdout)
            time_drill_down = self.run_stan(workspace, "pokaz", "--node_id", "n002")
            self.assertEqual(b"".join(lines[1:3]), time_drill_down.stdout)


if __name__ == "__main__":
    unittest.main()
