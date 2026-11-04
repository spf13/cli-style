# Contributing

This repository publishes the official [CLI Style](https://cli.style/) Agent Skill (`cli-style`).

Every structural invariant below is enforced by CI in `.github/workflows/validate.yml`.

## Repository Shape

```text
cli-style/
  SKILL.md
  .claude-plugin/
    plugin.json
.claude-plugin/
  marketplace.json
```

- `cli-style/SKILL.md` sits at the skill directory root so it is discovered simultaneously by `sage`, `npx skills`, and Claude Code.
- `.claude-plugin/marketplace.json` lists the skill entry and must correspond 1:1 with the `cli-style/` directory.
- The Skill Catalog table in `README.md` links to `./cli-style/SKILL.md`.

## Manifest Contract

`cli-style/.claude-plugin/plugin.json` is the source of truth for plugin display metadata (`name`, `displayName`, `description`, `version`, `author`, `homepage`, `repository`, `license`, `keywords`).

The matching `.claude-plugin/marketplace.json` entry carries four keys:

```json
{ "name": "cli-style", "source": "./cli-style", "category": "development", "tags": ["..."] }
```

- `name` must equal `"cli-style"` across the directory name, `SKILL.md` frontmatter, `plugin.json`, and `marketplace.json`.
- `tags` in `marketplace.json` must equal `keywords` in `plugin.json` as a set, with no duplicates.
- `SKILL.md` frontmatter `metadata.version`, `metadata.category`, and `metadata.tags` must equal `plugin.json` `version`, the marketplace `category`, and `plugin.json` `keywords`.

## Principle Contract

- `SKILL.md` has 10 `## Part` headings and principles numbered 1..56, each ending in `` (`#anchor`) ``.
- Each anchor must equal the canonical [cli.style](https://cli.style/) anchor listed in `.github/scripts/canonical_anchors.txt`, so audit citations resolve.
- Exactly principles 32, 33, 39, and 40 are marked `⚡ Divergent`.

## Run Checks Locally

```bash
python3 -m pip install --user jsonschema

# 1. Validate manifests against published SchemaStore schemas
python3 .github/scripts/validate_manifests.py

# 2. Check cross-file invariants
python3 .github/scripts/check_invariants.py

# 3. Test the invariant checker
python3 -m unittest discover -s .github/scripts

# 4. Validate with sage (if installed)
sage validate .
```
