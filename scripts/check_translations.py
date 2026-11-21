#!/usr/bin/env python3
"""Compare executable Bash/JSON examples across Portuguese and English guides."""
from pathlib import Path
import difflib
import re

ROOT = Path(__file__).resolve().parents[1]

def commands(path):
    out = []
    fence = None
    language = ""
    block = []
    for line in path.read_text().splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(\w*)\s*$", line)
        if match:
            if fence is None:
                fence, language, block = match[1], match[2], []
            elif match[1][0] == fence[0]:
                if language in {"bash", "shell", "sh", "json"}:
                    out.extend(l.strip() for l in block if l.strip() and not l.lstrip().startswith("#"))
                fence = None
        elif fence:
            block.append(line)
    return out

def check():
    failures = 0
    pairs = 0
    for english in sorted((ROOT / "docs/en").rglob("*.md")):
        portuguese = ROOT / "docs" / english.relative_to(ROOT / "docs/en")
        if not portuguese.exists():
            continue
        pairs += 1
        left, right = commands(portuguese), commands(english)
        if left != right:
            failures += 1
            print("\n".join(difflib.unified_diff(left, right, fromfile=str(portuguese.relative_to(ROOT)), tofile=str(english.relative_to(ROOT)))))
    print(f"Checked executable examples in {pairs} PT/EN document pairs; mismatches: {failures}.")
    return bool(failures)

if __name__ == "__main__":
    raise SystemExit(check())
