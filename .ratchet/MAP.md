# Map

**Entry points (consumers)**
- `cli-style/SKILL.md` — the product. Loaded by sage (`~/.agents/skills`), `npx skills`, Claude Code plugin.
- `.claude-plugin/marketplace.json` — Claude Code marketplace (`/plugin marketplace add spf13/cli-style`).
- `cli-style/.claude-plugin/plugin.json` — plugin metadata (source of truth for version/keywords).

**SKILL.md layout**
- L1–17 frontmatter (name, description, license, metadata.version/tags/category)
- L29–56 Workflows A (design) / B (audit, report template)
- L60–229 Parts I–X, principles 1–56, each `N. **Title.** (`#anchor`)` + 1–2 line body
- L233–274 Quick-reference: TTY matrix, reserved flags, exit codes + JSON error envelope

**Tooling / tests**
- `.github/scripts/check_invariants.py` — cross-file invariants + 1..56 numbering regex. Carries multi-skill catalog machinery (EXCLUDED templates/.codegraph, TAXONOMY, catalog-wide versions).
- `.github/scripts/validate_manifests.py` — JSON schema validation (network).
- `.github/workflows/validate.yml` — manifests, invariants, lychee (README + CONTRIBUTING only).
- No unit tests. No fixtures.

**Docs**: README (install + Part summary), CONTRIBUTING (invariants), CHANGELOG (1.0.0), AGENTS.md (sync protocol), LICENSE (CC BY-NC-ND + grants + MIT).

**Churn**: 2 commits total; every file touched once (`.gitignore` twice). No hotspots.

**External canonical source**: `spf13/CLI-website` (private) — `content/NN-part/NN-slug.md`, `static/llms.txt`.
