#!/usr/bin/env python3
"""Prepare the audited upstream checkout locally. No cloud calls or credentials."""
import argparse
import json
from pathlib import Path
import subprocess
from urllib.parse import urlsplit

GUIDE_DIR = Path(__file__).resolve().parents[1]
UPSTREAM_CONFIG = GUIDE_DIR / "config/upstream.json"


def _git(source: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(source), *args], text=True
    ).strip()


def _is_official_origin(value: str) -> bool:
    """Accept only the official GitHub repository over HTTPS or SSH."""
    value = value.strip()
    if value.startswith("git@github.com:"):
        path = value.removeprefix("git@github.com:")
        return path.lower() in {
            "googleads/google-ads-mcp",
            "googleads/google-ads-mcp.git",
        }

    try:
        parsed = urlsplit(value)
        host = (parsed.hostname or "").lower()
        path = parsed.path.rstrip("/").lower()
        if path.endswith(".git"):
            path = path[:-4]
        return (
            parsed.scheme.lower() in {"https", "ssh"}
            and host == "github.com"
            and parsed.port is None
            and parsed.query == ""
            and parsed.fragment == ""
            and path == "/googleads/google-ads-mcp"
            and (parsed.scheme.lower() != "https" or parsed.username is None)
            and (
                parsed.scheme.lower() != "ssh"
                or parsed.username in {None, "git"}
            )
            and parsed.password is None
        )
    except ValueError:
        return False


def prepare(source: Path) -> str:
    baseline = json.loads(UPSTREAM_CONFIG.read_text())
    source = source.resolve()
    try:
        origins = _git(
            source, "remote", "get-url", "--all", "origin"
        ).splitlines()
    except subprocess.CalledProcessError as error:
        raise ValueError(
            "Git origin remote is missing. Use a fresh clone from the official repository."
        ) from error
    if not origins or any(not _is_official_origin(origin) for origin in origins):
        raise ValueError(
            "Git origin is not the official "
            "https://github.com/googleads/google-ads-mcp.git repository. "
            "Use a fresh clone from the official repository."
        )

    head = _git(source, "rev-parse", "--verify", "HEAD")
    if head != baseline["commit"]:
        raise ValueError(
            "Upstream commit differs from config/upstream.json. Stop and review."
        )

    status = _git(
        source,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--ignored=matching",
    )
    if status:
        raise ValueError(
            "Upstream checkout contains modified, untracked, or ignored files. "
            "Do not build from this directory; clone a fresh checkout of the pinned commit."
        )

    dockerfile = source / "Dockerfile"
    before = "RUN uv pip install --system .\n"
    after = 'RUN uv pip install --system ".[firestore]"\n'
    content = dockerfile.read_text()
    before_count = content.count(before)
    after_count = content.count(after)
    if before_count == 1 and after_count == 0:
        content = content.replace(before, after, 1)
    elif before_count != 0 or after_count != 1:
        raise ValueError(
            "Upstream Dockerfile changed; expected installation line was not found."
        )
    if not (source / "LICENSE").is_file():
        raise ValueError("Upstream LICENSE is missing. Preserve its notices.")

    tools_config = (GUIDE_DIR / "config/tools-readonly.yaml").read_text()
    for generated in (source / "tools_config.yaml", source / ".gcloudignore"):
        if generated.exists():
            raise ValueError(
                f"Refusing to overwrite existing {generated.name}; "
                "review the checkout or use a fresh clone."
            )

    dockerfile.write_text(content)
    (source / "tools_config.yaml").write_text(tools_config)
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
    print(
        f"Prepared {revision}: Firestore dependency and read-only tool configuration. "
        "This checkout is now modified; clone a fresh pinned checkout to repeat preparation."
    )
