# BRIEF (locked 2026-11-04 — user answered "defaults")

## Intent
One Agent Skill (`cli-style/SKILL.md`) that teaches coding agents the 56 CLI Style principles so they design and audit CLIs and cite `#NN` + `#anchor` that resolve on https://cli.style/.

## Golden path + fixtures
Agent loads SKILL.md → Workflow B → audit report whose `#NN Title (`#anchor`)` citations match the canonical site.
- **Canonical source:** `spf13/cli-website` @ `15607c6` (cloned read-only at `/home/user/cli-website`): `content/*/*.md` frontmatter `weight`/`anchor`/`title`/`divergent`, and `static/llms.txt`. The live site is blocked by the sandbox (403) → [UNVERIFIED] live.
- **Fixture:** a committed list of the 56 canonical anchors (in number order) plus the ⚡ set {32,33,39,40}; `check_invariants.py` requires exact equality.
- **Smoke:** `python3 .github/scripts/check_invariants.py` + `python3 .github/scripts/validate_manifests.py` + `python3 -m unittest discover -s .github/scripts` all pass, and every SKILL.md principle anchor/title/number equals the canonical one.

## Truth on contradictions
- Site wins over SKILL.md for all 12 mismatched principles, and for titles/numbering generally.
- `metadata.category` → `development` (marketplace wins).
- SKILL.md:39 vs README.md:76 cobra-viper install lines: leave both.
- `sage validate .` in CONTRIBUTING: keep.

## Invariants (byte-stable / sacred)
- Skill name `cli-style`, directory layout, manifest key sets.
- Numbering 1–56, the 10 Parts, ⚡ set {32,33,39,40}.
- Exit-code table semantics (0–5, 130, 143) and JSON error envelope shape.
- SKILL.md prose is Steve's (CC BY-NC-ND): only fidelity fixes (to canonical text) and small factual clarifications. No restyling.
- Do not modify `spf13/cli-website` (read-only reference).

## Non-goals
- No new principles beyond the site's 56; no rewriting of matching principles' bodies for style.
- No tags/releases; no edits to branch protection or repo settings.

## Appetite & boundaries
- Conservative on prose; moderate on scripts.
- `.github/workflows/validate.yml` may be edited only to add a test job and to link-check SKILL.md.
- No new dependencies (stdlib `unittest` only). Network only for the existing schema fetch.
- Version: bump plugin.json + SKILL.md metadata to **1.1.0** with a CHANGELOG entry.

## Ranked rocks
1. Canonical fidelity of SKILL.md (anchors, titles, the 12 bodies; README summary that describes them).
2. Invariant checker catches real drift: canonical anchor list, ⚡ set, anchor uniqueness, SKILL.md metadata.version/tags/category vs plugin.json/marketplace, description ≤1024; stdlib unit tests that fail on drift.
3. Simplify checker for a single-skill repo (drop `templates`/`.codegraph`/taxonomy/catalog-wide version machinery), ~210 → ~120 LOC.

## Done signal
56/56 anchors (and titles/numbers) match canonical; the checker enforces it with tests that fail on drift; both checks pass; draft PR open from `claude/focused-pascal-26rrka`.
