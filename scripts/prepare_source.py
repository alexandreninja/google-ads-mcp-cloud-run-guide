#!/usr/bin/env python3
"""Prepare the audited upstream checkout locally. No cloud calls or credentials."""
import argparse
import json
from pathlib import Path
import subprocess

def prepare(source: Path) -> str:
    guide = Path(__file__).resolve().parents[1]
    baseline = json.loads((guide / "config/upstream.json").read_text())
    source = source.resolve()
    head = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    if head != baseline["commit"]:
        raise ValueError("Upstream commit differs from config/upstream.json. Stop and review.")
    dockerfile = source / "Dockerfile"
    before = "RUN uv pip install --system .\n"
    after = 'RUN uv pip install --system ".[firestore]"\n'
    content = dockerfile.read_text()
    if content.count(before) == 1:
        content = content.replace(before, after, 1)
    elif content.count(after) != 1:
        raise ValueError("Upstream Dockerfile changed; expected installation line was not found.")
    if not (source / "LICENSE").is_file():
        raise ValueError("Upstream LICENSE is missing. Preserve its notices.")
    dockerfile.write_text(content)
    (source / "tools_config.yaml").write_text(
        (guide / "config/tools-readonly.yaml").read_text()
    )
    (source / ".gcloudignore").write_text(
        ".git\n.venv\n__pycache__\n.env\n.env.*\n**/*credentials*.json\n"
    )
    return head

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to the upstream git checkout")
    args = parser.parse_args()
    try:
        revision = prepare(args.source)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Preparation stopped: {error}\n")
    print(f"Prepared {revision}: Firestore dependency and read-only tool configuration.")
