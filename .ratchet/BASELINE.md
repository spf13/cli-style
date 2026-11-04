# Baseline — 2026-11-04 @ 27186f4

Archetype: **mixed** (agent-skill prose + small Python validation toolchain). No build step, no compiled artifact.

| Check | Command | Result |
| --- | --- | --- |
| Invariants | `python3 .github/scripts/check_invariants.py` | PASS — "invariants hold for 1 skill(s); version 1.0.0" (0.2s) |
| Manifest schemas | `python3 .github/scripts/validate_manifests.py` | PASS — 2 manifests vs schemastore (2.4s, needs network + jsonschema 4.26) |
| Link check | lychee (CI only) | NOT RUN — lychee not installed locally |
| `sage validate .` | — | NOT RUN — sage not installed |
| `npx skills` | — | NOT RUN — package not installed (registry reachable, v1.7.6) |
| Lint | `ruff check .github/scripts` (user default config, no project config) | 5 findings (2× EXE001 non-exec shebang, 3× FURB167 `re.M`) |
| Format | `ruff format --check .github/scripts` | 2 files would be reformatted |
| Tests | — | **0 tests**; checker scripts are untested |
| Coverage | — | n/a |

## Product metrics
- `cli-style/SKILL.md`: 278 lines, 20,726 bytes, 2,809 words. Frontmatter description: 521 chars (spec max 1024).
- Principles: 56 numbered, 10 Parts, 4 ⚡ Divergent (#32, #33, #39, #40).
- **Anchor fidelity vs canonical site: 44/56 (78.6%)**. Source: GitHub code-search index of private `spf13/CLI-website` (`content/**` filenames, `index.html`, `static/llms.txt`). `https://cli.style/` itself is blocked by the sandbox proxy (403), so the live site is [UNVERIFIED].
  - Mismatched (skill → site): 4 nouns-are-plural→name-for-typing, 10 posix-mechanics→long-flags-first, 14 dash-for-stdio→run-without-config, 19 be-idempotent→idempotent-or-refuse, 30 structured-output→machine-output-first-class, 31 tables-for-eyes→say-nothing-on-success, 37 bound-the-output→stream-dont-buffer, 41 clean-terminal-exit→handle-interrupts, 45 no-stack-traces→one-error-then-detail, 47 retry-safety→crashes-ask-to-be-reported, 51 json-contract→machine-format-is-strictest, 53 update-yourself→easy-to-remove.
  - None of the 12 skill-only slugs occur anywhere in `CLI-website` (code search: 0 hits each).
- Python tooling: 279 LOC (check_invariants 210, validate_manifests 69).

## Smoke (golden path, as inferred)
Agent loads `cli-style/SKILL.md` → frontmatter parses (name/description) → audit report cites `#NN` + `#anchor` that resolve at `https://cli.style/#anchor`. Today: parse OK; 12/56 citations would not resolve [per index].
