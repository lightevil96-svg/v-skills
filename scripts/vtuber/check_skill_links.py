#!/usr/bin/env python3
"""Check repository Markdown links that point to local files.

Strict about path existence and repo escapes; does NOT check remote URLs or
the target headings of #anchors. Python 3.9+ standard library only.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"\]\(([^)]+)\)")


def check():
    errors = []
    checked = 0
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        content = md.read_text(encoding="utf-8")
        # Ignore fenced code blocks: their markdown links may be samples.
        content = re.sub(r"(?ms)^\s*```[^\n]*\n.*?^\s*```\s*$", "", content)
        for match in LINK.finditer(content):
            raw = match.group(1).strip().split(" ", 1)[0].strip("<>")
            if not raw or raw.startswith("#"):
                continue
            parsed = urlsplit(raw)
            if parsed.scheme in ("http", "https", "mailto") or raw.startswith("//"):
                continue
            if parsed.scheme:
                errors.append(f"{md.relative_to(ROOT)}: Unsupported link scheme: {raw}")
                continue
            target = unquote(parsed.path)
            if not target:
                continue
            path = (md.parent / target).resolve()
            checked += 1
            try:
                path.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{md.relative_to(ROOT)}: Link escapes repository: {raw}")
                continue
            if not path.exists():
                errors.append(f"{md.relative_to(ROOT)}: Missing local target: {raw}")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Local Markdown links checked: {checked}; broken: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(check())
