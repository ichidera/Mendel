#!/usr/bin/env python3
"""Generate the repository directory structure and placeholder files for Mendel.

Usage:
  python scripts/generate_repo_map.py [--dry-run] [--force]

This script is idempotent by default and will not overwrite existing files
unless `--force` is passed. It prints actions taken and exits with 0 on
success.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import textwrap
import sys


ROOT = Path(__file__).resolve().parent.parent


DIRS = [
    "architecture",
    "architecture/moe",
    "architecture/attention",
    "distillation",
    "quantization",
    "retrieval",
    "agent",
    "agent/tools",
    "agent/skills",
    "agent/cli",
    "control",
    "eval",
    "inference",
    "docs",
    "scripts",
    "src",
    "src/api",
    "src/utils",
    "tests",
    "examples",
    "notebooks",
    "configs",
    "assets",
    "data",
    "models",
    ".github",
    ".github/ISSUE_TEMPLATE",
    ".github/DISCUSSION_TEMPLATE",
    ".github/workflows",
]


TOP_LEVEL_FILES = {
    "README.md": "Mendel — lightweight capable model. See MISSION.md for goals.\n",
    "MISSION.md": "",
    "LICENSE": "",
    "CONTRIBUTING.md": "",
    "AUTHORS.md": "",
    "MAINTAINERS.md": "",
    "GOVERNANCE.md": "",
    "ROADMAP.md": "",
    "VISION.md": "",
    "FAQ.md": "",
    ".gitignore": "# Byte-compiled / cache files\n__pycache__/\n*.py[cod]\n.env\n.envrc\n\n# Virtual env\nvenv/\n.env/\n\n# OS files\n.DS_Store\nThumbs.db\n",
    ".gitattributes": "* text=auto\n",
}


GITHUB_FILES = {
    ".github/CODE_OF_CONDUCT.md": "",
    ".github/PULL_REQUEST_TEMPLATE.md": "",
    ".github/FUNDING.yml": "",
    ".github/CODEOWNERS": "",
    ".github/dependabot.yml": "",
    ".github/SUPPORT.md": "",
    ".github/ISSUE_TEMPLATE/bug_report.yml": "",
    ".github/ISSUE_TEMPLATE/feature_request.yml": "",
    ".github/ISSUE_TEMPLATE/config.yml": "",
    ".github/DISCUSSION_TEMPLATE/README.md": "",
    ".github/workflows/ci.yml": "",
    ".github/workflows/test.yml": "",
    ".github/workflows/lint.yml": "",
    ".github/workflows/release.yml": "",
    ".github/workflows/deploy.yml": "",
    ".github/workflows/security.yml": "",
}


def create_dir(path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"[DRY] mkdir -p {path}")
        return
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str, force: bool, dry_run: bool) -> None:
    if path.exists() and not force:
        print(f"skip (exists): {path}")
        return
    if dry_run:
        action = "[DRY] overwrite" if path.exists() and force else "[DRY] create"
        print(f"{action}: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"wrote: {path}")


#!/usr/bin/env python3
"""Scan the repository and print a directory tree map.

Example:
  python scripts/generate_repo_map.py --max-depth 3

Outputs a visual tree to stdout (or to `--output` file). By default, `.git`
is excluded. Hidden files are included unless excluded explicitly.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List


ROOT = Path(__file__).resolve().parent.parent


def walk_dir(path: Path, max_depth: int | None, exclude: Iterable[str]) -> List[str]:
    lines: List[str] = []

    def _walk(p: Path, prefix: str, depth: int) -> None:
        try:
            entries = sorted([e for e in p.iterdir() if e.name not in exclude], key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            lines.append(prefix + '└── [permission denied] ' + p.name)
            return

        for i, entry in enumerate(entries):
            connector = '└──' if i == len(entries) - 1 else '├──'
            lines.append(prefix + connector + ' ' + entry.name)
            if entry.is_dir():
                if max_depth is None or depth + 1 < max_depth:
                    extension = '    ' if i == len(entries) - 1 else '│   '
                    _walk(entry, prefix + extension, depth + 1)

    lines.append('.')
    _walk(path, '', 0)
    return lines


def to_json(path: Path, max_depth: int | None, exclude: Iterable[str]) -> str:
    def node(p: Path, depth: int):
        obj = {"name": p.name, "path": str(p.relative_to(ROOT))}
        if p.is_dir():
            if max_depth is not None and depth >= max_depth:
                obj["children"] = []
            else:
                children = [c for c in sorted(list(p.iterdir()), key=lambda x: (x.is_file(), x.name.lower())) if c.name not in exclude]
                obj["children"] = [node(c, depth + 1) for c in children]
        return obj

    return json.dumps(node(path, 0), indent=2)


def parse_args():
    p = argparse.ArgumentParser(description="Generate a repository directory map")
    p.add_argument("--root", type=Path, default=ROOT, help="Root path to scan")
    p.add_argument("--max-depth", type=int, default=None, help="Max depth to traverse")
    p.add_argument("--exclude", action="append", default=['.git'], help="Names to exclude (can be used multiple times)")
    p.add_argument("--dirs-only", action="store_true", help="Show directories only")
    p.add_argument("--format", choices=["tree", "json"], default="tree", help="Output format")
    p.add_argument("--output", type=Path, help="Write output to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    exclude = set(args.exclude or [])

    if not root.exists():
        print(f"Root not found: {root}")
        return 2

    if args.format == 'tree':
        lines = walk_dir(root, args.max_depth, exclude)
        if args.dirs_only:
            # Build a dirs-only view
            def walk_dirs_only(p: Path, max_depth, exclude):
                out: List[str] = []

                def _walk(pth: Path, prefix: str, depth: int) -> None:
                    try:
                        entries = sorted([e for e in pth.iterdir() if e.name not in exclude and e.is_dir()], key=lambda x: x.name.lower())
                    except PermissionError:
                        out.append(prefix + '└── [permission denied] ' + pth.name)
                        return
                    for i, entry in enumerate(entries):
                        connector = '└──' if i == len(entries) - 1 else '├──'
                        out.append(prefix + connector + ' ' + entry.name)
                        if max_depth is None or depth + 1 < max_depth:
                            extension = '    ' if i == len(entries) - 1 else '│   '
                            _walk(entry, prefix + extension, depth + 1)

                out.append('.')
                _walk(root, '', 0)
                return out

            lines = walk_dirs_only(root, args.max_depth, exclude)

        output_text = '\n'.join(lines) + '\n'
    else:
        output_text = to_json(root, args.max_depth, exclude) + '\n'

    if args.output:
        args.output.write_text(output_text, encoding='utf-8')
        print(f'wrote: {args.output}')
    else:
        print(output_text)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
