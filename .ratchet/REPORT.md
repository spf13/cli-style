# Ratchet report: SKILL.md now cites cli.style correctly, and CI enforces it

**Done signal: met.** All 56 principle anchors and titles (and the numbering) match canonical cli.style. The checker enforces this, with tests that fail on drift. Every check passes on a fresh clone. This draft PR is open from `claude/focused-pascal-26rrka`.

Canonical source: `spf13/cli-website` @ `15607c6`, read-only. The live `https://cli.style/` was blocked by the sandbox proxy, so the live site itself was not checked [UNVERIFIED].

## Baseline vs final

| Metric | Baseline (27186f4) | Final |
| --- | --- | --- |
| Anchors matching cli.style | 44/56 | **56/56 (enforced)** |
| Titles matching cli.style | 29/56 | **56/56 (enforced)** |
| ⚡ Divergent set {32,33,39,40} | correct, not enforced | correct, enforced |
| Tests | 0 | 16 (≈1s, stdlib `unittest`) |
| CI checks | manifests, invariants, links (README + CONTRIBUTING) | + checker tests, + `SKILL.md` link check |
| `check_invariants.py` LOC | 210 | 182 (enforces ~9 more rules) |
| `validate_manifests.py` LOC | 69 | 60 |
| ruff findings (default rules, no project config) | 5 | 0 |
| `SKILL.md` size | 20,726 B | 21,913 B |
| Version | 1.0.0 | 1.1.0 (no tags created) |

Final gate, run on a fresh clone of the pushed branch: `python3 -m unittest discover -s .github/scripts` passed 16/16; `check_invariants.py` passed ("version 1.1.0", with the existing remote tag `v1.0.0` present); `validate_manifests.py` validated both manifests; `ruff check` was clean. Comparing against canonical gave anchors 56/56, titles 56/56 and ⚡ flags 56/56.

## Kept changes

| SHA | Lens | Change |
| --- | --- | --- |
| b9d32c0 | fidelity | All 56 principle headers regenerated from canonical frontmatter. 12 anchors that didn't exist on cli.style replaced. Bodies of #4, 10, 14, 30, 31, 37, 41, 45, 47, 51 and 53 rewritten from canonical text. Part VIII subtitle aligned with `llms.txt`. |
| a518e76, 596d0c2 | docs | README Part summaries no longer advertise principles the skill doesn't teach (plural nouns, `-` for stdio, pagination, retryable, `app upgrade`). |
| 9be74c5 | correctness | Version 1.1.0 in `plugin.json` and the `SKILL.md` metadata; CHANGELOG has an old→new anchor migration table. |
| 6cd7f65 | completeness | Checker pins anchors to a canonical fixture; checks the ⚡ set, the `SKILL.md` metadata (version, category, tags) against the manifests, and description length ≤ 1024. Fixed real drift it found: `category: coding` became `development`. |
| 3e4cd41 | tests | 11 tests, each mutating a temp copy of the repo and asserting a specific failure; added to the CI invariants job. |
| 96f1d05 | correctness | Fixture `canonical_principles.txt` now carries titles; checks list length and titles. 5 more tests, including three sacred rules that had no test: Part count, skill name, and `metadata.tags`. |
| b90bf97 | simplify | Removed the many-skill catalog scaffolding (directory scan, `templates`/`.codegraph` exclusions, category taxonomy, catalog-wide version logic). A version that isn't `MAJOR.MINOR.PATCH` now fails. Ruff is clean. |
| 822bd44 | docs | Tag errors print `vX.Y.Z` instead of raw tuples; CONTRIBUTING describes the rule the checker actually enforces. |
| d2ac455 | docs | lychee link check now covers `cli-style/SKILL.md`. |
| 2ad9286 | docs | CHANGELOG scope corrected (#4 and the restated principles), README Part VI line fixed, and the validator docstring updated. |

## Reverted attempts

None. Every pass got a KEEP from an independent judge (a fresh subagent that read only BRIEF, BASELINE, the diff and the canonical source). Architecture, simplify, ux and design/craft were marked CONVERGED in the bookend sweep.

## Remaining backlog (ranked)

1. **The `retryable` column and key now have no backing principle** (small). The old #47 `retry-safety` was replaced by the canonical `crashes-ask-to-be-reported`. The sacred exit-code table and JSON envelope still carry `Retryable?` and `retryable` (`SKILL.md:260-273`), but no principle tells an agent when to set them. Decide whether the site should gain this guidance or the tables should drop it.
2. **Short flag for `--preview`** (small, site side). The canonical #10 example uses `-p` for `--preview`, while `SKILL.md` reserves `-n/--preview` (#9 and the flag table). I kept `-n` and avoided the conflict in #10's body.
3. **`llms.txt` links to `https://cli.style/SKILL.md`, but `cli-website` has no `SKILL.md`** (small, site side). That link probably 404s [UNVERIFIED live].
4. **The fixture is a pinned copy** (small). Nothing re-derives `canonical_principles.txt` from `cli-website`, so when the site changes, regenerate it by hand. The generation one-liner is in RATCHET_LOG S2.
5. **#46 example differs from the envelope** (trivial, predates this branch). The #46 body shows `AUTH_REQUIRED` with no `exit_code`/`retryable`, while the reference envelope uses `AUTH_EXPIRED` with both.
6. **Other gaps** (trivial):
   - The checker no longer catches a stray second plugin directory or extra README table rows. That doesn't matter with one skill.
   - `ruff format` (default 88 columns) would rewrap the scripts; there's no project formatter configuration.

## Risks to review by hand

- **Prose.** The 11 rewritten bodies are your text, paraphrased from cli-website; their CC BY-NC-ND voice matters. Each judge confirmed they're faithful, but read them yourself: `git show b9d32c0 -- cli-style/SKILL.md`.
- **Anchor renames break saved citations.** That's why this is 1.1.0 with a migration table. Since anchors are a contract, you could argue for 2.0.0.
- **Guidance dropped with the old principles.** These aren't on the site, so the skill no longer teaches them:
  - `--limit`/`next_cursor` pagination
  - `-` for stdin/stdout
  - TTY table column limits
  - `retry_after_seconds`
  - `app upgrade` / no auto-update mid-command
- **CI.** The lychee job now fetches cli.style, GitHub, Cobra, Viper and pflag URLs from `SKILL.md`. It isn't runnable locally, so I haven't seen this job run [UNVERIFIED].
- **AGENTS.md sync protocol.** After merge, pull on `factory` and `wandamax` as documented. No skill was added or renamed, so `sage sync` isn't needed.
