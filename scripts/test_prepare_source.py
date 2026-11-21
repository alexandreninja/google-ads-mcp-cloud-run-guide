"""Offline checks for preparation invariants; never contacts Google Cloud."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prepare_source", ROOT / "scripts/prepare_source.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
PIN = json.loads((ROOT / "config/upstream.json").read_text())["commit"]

class PreparationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name)
        (self.source / "Dockerfile").write_text("FROM python:3.11-slim\nRUN uv pip install --system .\n# compatibility guard must survive\n")
        (self.source / "LICENSE").write_text("Upstream license must remain unchanged\n")
        self.mock = patch.object(module.subprocess, "check_output", return_value=PIN + "\n").start()
        self.addCleanup(patch.stopall)

    def test_pinned_source_is_idempotent_and_preserves_upstream(self):
        module.prepare(self.source)
        before = {p.name: p.read_bytes() for p in self.source.iterdir()}
        module.prepare(self.source)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.source.iterdir()})
        self.assertIn("# compatibility guard must survive", (self.source / "Dockerfile").read_text())
        self.assertEqual((self.source / "LICENSE").read_text(), "Upstream license must remain unchanged\n")

    def test_wrong_revision_changes_nothing(self):
        self.mock.return_value = "0" * 40
        before = (self.source / "Dockerfile").read_bytes()
        with self.assertRaises(ValueError):
            module.prepare(self.source)
        self.assertEqual(before, (self.source / "Dockerfile").read_bytes())
        self.assertFalse((self.source / "tools_config.yaml").exists())

    def test_unexpected_dockerfile_stops(self):
        (self.source / "Dockerfile").write_text("FROM unexpected:latest\n")
        with self.assertRaises(ValueError):
            module.prepare(self.source)
        self.assertFalse((self.source / "tools_config.yaml").exists())

    def test_missing_upstream_license_stops_before_writing(self):
        (self.source / "LICENSE").unlink()
        before = (self.source / "Dockerfile").read_bytes()
        with self.assertRaises(ValueError):
            module.prepare(self.source)
        self.assertEqual(before, (self.source / "Dockerfile").read_bytes())

    def test_explicit_tool_surface_excludes_mutations(self):
        module.prepare(self.source)
        config = (self.source / "tools_config.yaml").read_text()
        for name in ("customers", "search", "metadata"):
            self.assertIn(f"  {name}: true", config)
        for name in ("labels", "assets"):
            self.assertIn(f"  {name}: false", config)
        self.assertIn(".env", (self.source / ".gcloudignore").read_text())

if __name__ == "__main__":
    unittest.main()
