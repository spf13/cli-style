#!/usr/bin/env python3
"""Assert the cross-file invariants documented in CONTRIBUTING.md and 56-principle completeness."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

NAME = "cli-style"
ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / NAME
CANONICAL_PRINCIPLES = Path(__file__).with_name("canonical_principles.txt")
ENTRY_KEYS = {"name", "source", "category", "tags"}
MIN_DESCRIPTION, MAX_DESCRIPTION = 40, 1024
DIVERGENT = {32, 33, 39, 40}

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(path: Path) -> dict[str, str]:
    """Parse the leading YAML frontmatter: folded/literal scalars and one level of `metadata:` keys."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    key: str | None = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        nested = re.match(r"^\s+([a-z_]+):\s*(.*)$", line)
        if key == "metadata" and nested:
            fields[f"metadata.{nested[1]}"] = nested[2].strip().strip('"')
        elif line[:1].strip() and ":" in line:
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            fields[key] = "" if value in (">", "|", ">-", "|-", ">+", "|+") else value
        elif key and line[:1] in (" ", "\t"):
            fields[key] = f"{fields[key]} {line.strip()}".strip()
    return fields


def semver(value: str) -> tuple[int, int, int] | None:
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", value)
    return (int(match[1]), int(match[2]), int(match[3])) if match else None


def version_tags(*args: str) -> list[tuple[int, int, int]]:
    """Semantic `v*` tags, filtered by extra `git tag` arguments."""
    result = subprocess.run(
        ["git", "tag", "-l", "v*", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    return [v for v in map(semver, result.stdout.split()) if v]


def check_principles(text: str) -> None:
    """10 Parts; principles 1..56 whose anchors and titles match cli.style; the ⚡ Divergent set."""
    parts = re.findall(r"^## Part [IVX]+ · ", text, flags=re.MULTILINE)
    if len(parts) != 10:
        fail(f"cli-style/SKILL.md: expected 10 Part headings, found {len(parts)}")

    found = re.findall(r"^(\d{1,2})\.\s+\*\*([^*]+)\*\*\s+\(`#([a-z0-9-]+)`\)", text, flags=re.MULTILINE)
    numbers = [int(number) for number, _, _ in found]
    if numbers != list(range(1, 57)):
        fail(f"cli-style/SKILL.md: expected numbered principles 1..56 with anchors, got {len(numbers)} ({numbers})")
        return

    canonical = [
        line.strip().split(maxsplit=1)
        for line in CANONICAL_PRINCIPLES.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if len(canonical) != len(found) or any(len(row) != 2 for row in canonical):
        fail(f"canonical_principles.txt lists {len(canonical)} principles; expected {len(found)} `anchor title` lines")
        return
    for number, ((_, title, anchor), (want_anchor, want_title)) in enumerate(zip(found, canonical), start=1):
        if anchor != want_anchor:
            fail(f"cli-style/SKILL.md: principle {number} anchor is #{anchor}; cli.style uses #{want_anchor}")
        title = title.replace("⚡ Divergent", "").replace("`", "").strip()
        if title != want_title:
            fail(f"cli-style/SKILL.md: principle {number} title is {title!r}; cli.style uses {want_title!r}")

    divergent = {int(number) for number, title, _ in found if "⚡ Divergent" in title}
    if divergent != DIVERGENT:
        fail(f"cli-style/SKILL.md: ⚡ Divergent principles are {sorted(divergent)}; expected {sorted(DIVERGENT)}")


def check_version(version: str) -> None:
    """The version has a CHANGELOG entry, matches a release tag at HEAD, and never goes backwards."""
    current = semver(version)
    if current is None:
        fail(f"plugin.json version {version!r} is not MAJOR.MINOR.PATCH")
        return
    if os.environ.get("GITHUB_REF_TYPE") == "tag":
        released = [semver(os.environ.get("GITHUB_REF_NAME", ""))]
    else:
        released = version_tags("--points-at", "HEAD")
    if any(tag and tag != current for tag in released):
        fail(f"HEAD is tagged {released} but plugin.json version is {version}")
    if any(tag > current for tag in version_tags()):
        fail(f"plugin.json version {version} is older than the latest tag")
    changelog = ROOT / "CHANGELOG.md"
    if not changelog.is_file():
        fail("CHANGELOG.md is missing")
    elif not re.search(rf"^##\s*\[{re.escape(version)}\]", changelog.read_text(encoding="utf-8"), re.MULTILINE):
        fail(f"CHANGELOG.md has no '## [{version}]' entry")


def main() -> int:
    entries = read_json(ROOT / ".claude-plugin" / "marketplace.json").get("plugins", [])
    manifest = read_json(SKILL_DIR / ".claude-plugin" / "plugin.json")
    skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    skill = frontmatter(SKILL_DIR / "SKILL.md")

    if len(entries) != 1:
        fail(f"marketplace.json must list exactly one plugin, got {len(entries)}")
    entry = entries[0] if entries else {}
    if set(entry) != ENTRY_KEYS:
        fail(f"marketplace entry keys must be exactly {sorted(ENTRY_KEYS)}, got {sorted(entry)}")
    if entry.get("source") != f"./{NAME}":
        fail(f"marketplace entry source must be './{NAME}', got {entry.get('source')!r}")
    for label, value in (
        ("marketplace entry", entry.get("name")),
        ("plugin.json", manifest.get("name")),
        ("SKILL.md frontmatter", skill.get("name")),
    ):
        if value != NAME:
            fail(f"{label} name is {value!r}; must be {NAME!r}")

    link = f"[`{NAME}`](./{NAME}/SKILL.md)"
    if not any(line.startswith(f"| {link}") for line in (ROOT / "README.md").read_text(encoding="utf-8").splitlines()):
        fail(f"README skills table must list {link}")

    description = skill.get("description", "")
    if not MIN_DESCRIPTION <= len(description) <= MAX_DESCRIPTION:
        fail(f"SKILL.md description is {len(description)} chars; must be {MIN_DESCRIPTION}..{MAX_DESCRIPTION}")

    version, keywords = manifest.get("version", ""), manifest.get("keywords", [])
    if skill.get("metadata.version") != version:
        fail(f"SKILL.md metadata.version {skill.get('metadata.version')!r} != plugin.json version {version!r}")
    if skill.get("metadata.category") != entry.get("category"):
        fail(
            f"SKILL.md metadata.category {skill.get('metadata.category')!r} "
            f"!= marketplace category {entry.get('category')!r}"
        )
    skill_tags = [tag.strip() for tag in skill.get("metadata.tags", "").split(",") if tag.strip()]
    if sorted(skill_tags) != sorted(keywords):
        fail(f"SKILL.md metadata.tags {sorted(skill_tags)} != plugin.json keywords {sorted(keywords)}")
    tags = entry.get("tags", [])
    if sorted(tags) != sorted(keywords):
        fail(f"marketplace tags {sorted(tags)} != plugin.json keywords {sorted(keywords)}")
    if len(set(keywords)) != len(keywords):
        fail(f"plugin.json keywords must be free of duplicates: {keywords}")

    check_principles(skill_text)
    check_version(version)

    if errors:
        print(f"invariant check failed ({len(errors)} problem(s)):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"invariants hold for {NAME}; version {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
