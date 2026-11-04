# Plan (draft, pre-brief)

## Inferred brief
- **Intent:** a single Agent Skill that teaches coding agents the 56 CLI Style principles so they design/audit CLIs and cite `#NN` + `#anchor` back to https://cli.style/ (SKILL.md:21-25, :48-56; README.md:5-7).
- **Primary user:** coding agents (Claude Code, Cursor, Copilot, Gemini…) acting for Go/CLI developers; secondary: Steve maintaining it across galactus/factory/wandamax (AGENTS.md).
- **Golden path:** agent loads SKILL.md → runs Workflow B → emits audit report whose citations resolve on cli.style (SKILL.md:41-56).
- **Invariants (inferred):**
  - Skill name `cli-style` and directory layout fixed (CONTRIBUTING.md:7-23; check_invariants.py:150-153).
  - 10 Parts / 56 principles numbered 1..56 with `(`#anchor`)` (check_invariants.py:73-83).
  - ⚡ Divergent set = {32, 33, 39, 40} (SKILL.md:25; README.md:7).
  - Exit codes 0–5/130/143 and the JSON error envelope shape (SKILL.md:258-274).
  - Versions agree: plugin.json 1.0.0 = SKILL.md metadata 1.0.0 = CHANGELOG [1.0.0] (only the first and last are enforced).
  - Prose is CC BY-NC-ND and authored by Steve (LICENSE §1) — edits are author-sensitive.

## Top 3 rocks
1. **Canonical fidelity of SKILL.md vs cli.style** — 12/56 anchors absent from site; ~6 of those look like *different principles*, not renames (BASELINE.md). Lenses: fidelity → correctness → docs/voice → reality.
2. **Invariant checker catches real drift** — no check for anchor set vs canonical list, Divergent set, anchor uniqueness, SKILL.md metadata.version/tags vs plugin.json, description ≤1024; zero tests for the checker. Lenses: completeness → tests → correctness → reality.
3. **Simplify the toolchain to a single-skill repo** — check_invariants.py carries catalog-of-many machinery (EXCLUDED `templates`/`.codegraph`, TAXONOMY, catalog version uniformity, README multi-row parsing). Lenses: simplify → architecture → docs/voice → reality.

## Findings backlog (ranked)
1. [fidelity] 12 anchors mismatch canonical slugs (SKILL.md:69,87,95,111,145,147,159,174,188,192,206,216).
2. [fidelity] Possibly missing site principles: run-without-config, say-nothing-on-success, stream-dont-buffer, one-error-then-detail, crashes-ask-to-be-reported, easy-to-remove; and skill-only content (dash-for-stdio, tables-for-eyes, bound-the-output, no-stack-traces, retry-safety, update-yourself) — need canonical text.
3. [completeness] checker doesn't pin the anchor list / Divergent set / uniqueness (check_invariants.py:73-83).
4. [correctness] SKILL.md `metadata.version` "1.0.0" (SKILL.md:15) and `metadata.tags` (:13) are not checked against plugin.json; `metadata.category: coding` (:12) disagrees with marketplace `development` (marketplace.json:14).
5. [completeness] no max-length check on description (spec 1024) or name.
6. [tests] no tests for check_invariants.py (frontmatter parser handles `>`/`|` folding — untested).
7. [simplify] dead multi-skill code: EXCLUDED `templates`, `.codegraph` (check_invariants.py:16; validate_manifests.py:17), TAXONOMY with 3 categories, catalog-wide version set (:179-183).
8. [docs/voice] Reserved-flag row `--help / --version | -h` implies `-h` for version (SKILL.md:249).
9. [docs/voice] #32 only names `stdout` for disabling color; per-stream rule (#39) implies stderr color keys off stderr TTY (SKILL.md:150 vs :241).
10. [docs] cobra-viper install: SKILL.md:39 `sage add spf13/go-skills/cobra-viper` vs README.md:76 `sage add spf13/go-skills` [UNVERIFIED which is right].
11. [docs] CONTRIBUTING.md:47 `sage validate .` [UNVERIFIED command exists].
12. [reality] lychee skips SKILL.md links (validate.yml:43).
13. [lint] ruff (user default config) 5 findings; no project lint config.
