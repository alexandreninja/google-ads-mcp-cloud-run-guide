#!/usr/bin/env python3
"""Check local Markdown links, JSON examples and Bash syntax without running cloud commands."""
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote
import unicodedata

ROOT = Path(__file__).resolve().parents[1]

def anchors(path):
    counts = {}
    found = set()
    in_code = False
    for line in path.read_text().splitlines():
        if re.match(r"^\s*(`{3,}|~{3,})", line):
            in_code = not in_code
        if in_code:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            heading = re.sub(r"<[^>]*>", "", match.group(1)).lower().replace("`", "")
            heading = "".join(c for c in heading if c in "-_ " or unicodedata.category(c)[0] in "LNM")
            slug = heading.replace(" ", "-")
            count = counts.get(slug, 0)
            counts[slug] = count + 1
            found.add(slug + (f"-{count}" if count else ""))
    return found

def check():
    errors = []
    pages = 0
    blocks = 0
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", ".work", "node_modules", ".venv"} for part in path.parts):
            continue
        pages += 1
        text = path.read_text()
        code = []
        fence = None
        language = ""
        for number, line in enumerate(text.splitlines(), 1):
            match = re.match(r"^\s*(`{3,}|~{3,})(\w*)\s*$", line)
            if match:
                token = match.group(1)
                if fence is None:
                    fence, language, code = token, match.group(2), []
                elif token[0] == fence[0] and len(token) >= len(fence):
                    value = "\n".join(code)
                    blocks += 1
                    if language in {"bash", "sh", "shell"}:
                        result = subprocess.run(["bash", "-n"], input=value, text=True, capture_output=True)
                        if result.returncode:
                            errors.append(f"{path.relative_to(ROOT)}:{number}: Bash syntax: {result.stderr.strip()}")
                    elif language == "json":
                        try:
                            json.loads(value)
                        except ValueError as error:
                            errors.append(f"{path.relative_to(ROOT)}:{number}: JSON: {error}")
                    fence = None
                continue
            if fence is not None:
                code.append(line)
                continue
            for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)", line):
                if target.startswith(("http:", "https:", "mailto:")):
                    continue
                pieces = target.split("#", 1)
                destination = unquote(pieces[0])
                resolved = (path.parent / destination) if destination else path
                if not resolved.exists():
                    errors.append(f"{path.relative_to(ROOT)}:{number}: missing target {destination}")
                elif len(pieces) == 2 and resolved.suffix == ".md" and unquote(pieces[1]) not in anchors(resolved):
                    errors.append(f"{path.relative_to(ROOT)}:{number}: missing heading {target}")
        if fence:
            errors.append(f"{path.relative_to(ROOT)}: unclosed code fence")
    print(f"Checked {pages} Markdown files and {blocks} code blocks; no cloud commands executed.")
    for error in errors:
        print(error, file=sys.stderr)
    return bool(errors)

if __name__ == "__main__":
    raise SystemExit(check())
