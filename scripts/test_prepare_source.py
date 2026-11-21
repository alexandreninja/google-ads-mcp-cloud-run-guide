"""Offline checks using real temporary Git repositories; never calls Google Cloud."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "prepare_source", ROOT / "scripts/prepare_source.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def git(source: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(source), *args], text=True
    ).strip()


class PreparationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "upstream"
        self.source.mkdir()
        subprocess.run(["git", "init", "--quiet", str(self.source)], check=True)
        git(self.source, "config", "user.name", "Preparation Test")
        git(self.source, "config", "user.email", "prepare-test@example.invalid")

        self.original_dockerfile = (
            "FROM python:3.11-slim\n"
            "RUN uv pip install --system .\n"
            "# compatibility guard must survive\n"
        )
        (self.source / "Dockerfile").write_text(self.original_dockerfile)
        (self.source / "LICENSE").write_text("Upstream license must remain unchanged\n")
        (self.source / ".gitignore").write_text("*.secret\n")
        package = self.source / "ads_mcp"
        package.mkdir()
        (package / "server.py").write_text("# committed upstream source\n")
        git(
            self.source,
            "add",
            "Dockerfile",
            "LICENSE",
            ".gitignore",
            "ads_mcp/server.py",
        )
        git(self.source, "commit", "--quiet", "-m", "pinned fixture")
        git(
            self.source,
            "remote",
            "add",
            "origin",
            "https://github.com/googleads/google-ads-mcp.git",
        )

        self.pin = git(self.source, "rev-parse", "HEAD")
        self.baseline_path = self.root / "upstream.json"
        self.write_baseline(self.pin)
        self.baseline_patch = patch.object(
            module, "UPSTREAM_CONFIG", self.baseline_path
        )
        self.baseline_patch.start()
        self.addCleanup(self.baseline_patch.stop)

    def write_baseline(self, commit: str):
        self.baseline_path.write_text(
            json.dumps(
                {
                    "repository": "https://github.com/googleads/google-ads-mcp",
                    "commit": commit,
                    "package_version": "0.0.6",
                    "reviewed_on": "2026-11-21",
                }
            )
        )

    def assert_preparation_outputs_absent(self):
        self.assertFalse((self.source / "tools_config.yaml").exists())
        self.assertFalse((self.source / ".gcloudignore").exists())

    def test_clean_pinned_checkout_changes_only_expected_dockerfile_line(self):
        revision = module.prepare(self.source)
        expected = self.original_dockerfile.replace(
            "RUN uv pip install --system .\n",
            'RUN uv pip install --system ".[firestore]"\n',
            1,
        )

        self.assertEqual(revision, self.pin)
        self.assertEqual((self.source / "Dockerfile").read_text(), expected)
        self.assertIn("# compatibility guard must survive", expected)
        self.assertEqual(
            (self.source / "LICENSE").read_text(),
            "Upstream license must remain unchanged\n",
        )
        self.assertEqual(
            (self.source / "tools_config.yaml").read_text(),
            (ROOT / "config/tools-readonly.yaml").read_text(),
        )
        self.assertEqual(
            (self.source / ".gcloudignore").read_text(),
            ".git\n.venv\n__pycache__\n.env\n.env.*\n**/*credentials*.json\n",
        )

    def test_wrong_revision_changes_nothing(self):
        self.write_baseline("0" * 40)
        with self.assertRaisesRegex(ValueError, "commit differs"):
            module.prepare(self.source)

        self.assertEqual(
            (self.source / "Dockerfile").read_text(), self.original_dockerfile
        )
        self.assert_preparation_outputs_absent()

    def test_modified_tracked_source_stops_before_writing(self):
        (self.source / "ads_mcp/server.py").write_text("# modified after pin\n")

        with self.assertRaisesRegex(ValueError, "modified, untracked, or ignored"):
            module.prepare(self.source)

        self.assertEqual(
            (self.source / "Dockerfile").read_text(), self.original_dockerfile
        )
        self.assert_preparation_outputs_absent()

    def test_staged_source_change_stops_before_writing(self):
        (self.source / "ads_mcp/server.py").write_text("# staged after pin\n")
        git(self.source, "add", "ads_mcp/server.py")

        with self.assertRaisesRegex(ValueError, "modified, untracked, or ignored"):
            module.prepare(self.source)

        self.assertEqual(
            (self.source / "Dockerfile").read_text(), self.original_dockerfile
        )
        self.assert_preparation_outputs_absent()

    def test_untracked_source_stops_before_writing(self):
        (self.source / "extra.py").write_text("# untracked build input\n")

        with self.assertRaisesRegex(ValueError, "modified, untracked, or ignored"):
            module.prepare(self.source)

        self.assertEqual(
            (self.source / "Dockerfile").read_text(), self.original_dockerfile
        )
        self.assert_preparation_outputs_absent()

    def test_ignored_source_stops_before_writing(self):
        (self.source / "customer.secret").write_text("not for a build context\n")

        with self.assertRaisesRegex(ValueError, "modified, untracked, or ignored"):
            module.prepare(self.source)

        self.assertEqual(
            (self.source / "Dockerfile").read_text(), self.original_dockerfile
        )
        self.assert_preparation_outputs_absent()

    def test_non_official_origin_stops_before_writing(self):
        git(
            self.source,
            "remote",
            "set-url",
            "origin",
            "https://github.com/someone-else/google-ads-mcp.git",
        )

        with self.assertRaisesRegex(ValueError, "not the official"):
            module.prepare(self.source)

        self.assertEqual((self.source / "Dockerfile").read_text(), self.original_dockerfile)
        self.assert_preparation_outputs_absent()

    def test_incompatible_pinned_dockerfile_stops_before_writing(self):
        (self.source / "Dockerfile").write_text("FROM unexpected:latest\n")
        git(self.source, "add", "Dockerfile")
        git(self.source, "commit", "--quiet", "-m", "fixture with changed Dockerfile")
        self.write_baseline(git(self.source, "rev-parse", "HEAD"))

        with self.assertRaisesRegex(ValueError, "Dockerfile changed"):
            module.prepare(self.source)

        self.assertEqual(
            (self.source / "Dockerfile").read_text(), "FROM unexpected:latest\n"
        )
        self.assert_preparation_outputs_absent()

    def test_missing_license_in_pinned_commit_stops_before_writing(self):
        (self.source / "LICENSE").unlink()
        git(self.source, "add", "LICENSE")
        git(self.source, "commit", "--quiet", "-m", "fixture without upstream license")
        self.write_baseline(git(self.source, "rev-parse", "HEAD"))

        with self.assertRaisesRegex(ValueError, "LICENSE is missing"):
            module.prepare(self.source)

        self.assertEqual(
            (self.source / "Dockerfile").read_text(), self.original_dockerfile
        )
        self.assert_preparation_outputs_absent()

    def test_prepared_checkout_requires_a_fresh_clone_to_repeat(self):
        module.prepare(self.source)

        with self.assertRaisesRegex(ValueError, "fresh checkout"):
            module.prepare(self.source)

    def test_official_ssh_origin_is_accepted(self):
        git(
            self.source,
            "remote",
            "set-url",
            "origin",
            "git@github.com:googleads/google-ads-mcp.git",
        )

        self.assertEqual(module.prepare(self.source), self.pin)


if __name__ == "__main__":
    unittest.main()
