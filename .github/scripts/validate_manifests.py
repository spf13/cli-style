#!/usr/bin/env python3
"""Validate the plugin manifests against the published schemastore schemas.

Covers `.claude-plugin/marketplace.json` and `cli-style/.claude-plugin/plugin.json`.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[2]

MARKETPLACE_SCHEMA = "https://json.schemastore.org/claude-code-marketplace.json"
PLUGIN_SCHEMA = "https://json.schemastore.org/claude-code-plugin-manifest.json"


def fetch_schema(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def validate(path: Path, schema: dict, schema_name: str, errors: list[str]) -> None:
    document = json.loads(path.read_text(encoding="utf-8"))
    validator = Draft7Validator(schema)
    for error in sorted(validator.iter_errors(document), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.absolute_path) or "<root>"
        errors.append(f"{path.relative_to(ROOT)} [{schema_name}] {where}: {error.message}")


def main() -> int:
    errors: list[str] = []

    marketplace_schema = fetch_schema(MARKETPLACE_SCHEMA)
    plugin_schema = fetch_schema(PLUGIN_SCHEMA)

    targets = [
        (ROOT / ".claude-plugin" / "marketplace.json", marketplace_schema, "marketplace"),
        (ROOT / "cli-style" / ".claude-plugin" / "plugin.json", plugin_schema, "plugin"),
    ]

    for path, schema, schema_name in targets:
        validate(path, schema, schema_name, errors)

    if errors:
        print("manifest validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"validated {len(targets)} manifest(s) against the published schemastore schemas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
