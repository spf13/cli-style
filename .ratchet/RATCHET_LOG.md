# Ratchet Log

Process note: the orchestrator (holding full inventory context) implements; every judge is a fresh subagent that reads only BRIEF/BASELINE/diff/touched files + canonical source.

## Sweep 1 — rock 1: canonical fidelity

### S1 · fidelity — KEPT — 55→95 — b9d32c0
- Critique: 12/56 anchors absent from cli.style; 27/56 titles diverged; Part VIII subtitle differed from llms.txt (SKILL.md:63-229, :200).
- Change: all 56 headers regenerated from cli-website frontmatter (weight/title/anchor/divergent); bodies for 4, 10, 14, 30, 31, 37, 41, 45, 47, 51, 53 rewritten from canonical text; Workflow A + quick-ref header cross-refs updated.
- Verified: `python3 .github/scripts/check_invariants.py` → pass; scratch `compare.py` → anchor 56/56, title 56/56, divergent 56/56 (was 44/29/56); `validate_manifests.py` → pass.
- Judge: KEEP — all 56 match canonical; bodies faithful; sacred tables byte-identical. Minor non-contradictory drift noted (#14 path, #45 `--debug`, #53 dirs, #10 POSIX sentence retained).

### S1 · docs/voice — KEPT — 55→80 — a518e76 (+ phrasing fix 596d0c2)
- Critique: README Part summaries (README.md:58-67) advertised principles SKILL.md no longer teaches (plural nouns, `-` for stdio, pagination, retryable, `app upgrade`).
- Change: rewrote the 8 affected summary clauses to match SKILL.md; follow-up fixed two phrasings the judge flagged.
- Verified: `check_invariants.py` pass.
- Judge: KEEP — removes 5 stale claims; flagged Part VI grammar and "our bug" quote (fixed). Pre-existing omissions (#03, #12, #27) left — summaries are not exhaustive.

### S1 · correctness — KEPT — 55→88 — 9be74c5
- Critique: anchors changed (consumer-visible) but version stayed 1.0.0 with no migration path (plugin.json:6, SKILL.md:15, CHANGELOG.md).
- Change: plugin.json + SKILL.md metadata → 1.1.0; CHANGELOG [1.1.0] with old→new anchor table.
- Verified: removing the CHANGELOG entry makes `check_invariants.py` fail ("no '## [1.1.0]' entry", rc=1); restored → pass; `validate_manifests.py` pass.
- Judge: KEEP — all 12 migration rows exact; no tags. Noted: changelog doesn't enumerate ~20 title-only changes (line 9 covers them generically).

### S1 · reality — KEPT (gate) — 596d0c2..9be74c5
- Verified: `check_invariants.py` pass (v1.1.0); `validate_manifests.py` pass (2 manifests); canonical compare anchor/title/divergent 56/56; `git tag` empty. lychee not runnable locally [UNVERIFIED links].

### Sweep 1 scorecard
| Lens | Score | Result |
| --- | --- | --- |
| fidelity | 55→95 | KEPT |
| docs/voice | 55→80 | KEPT |
| correctness | 55→88 | KEPT |
| reality | pass | KEPT |

| Metric | Baseline | S1 |
| --- | --- | --- |
| Anchor match | 44/56 | 56/56 |
| Title match | 29/56 | 56/56 |
| ⚡ match | 56/56 | 56/56 |
| Tests | 0 | 0 |
| Checks | 2/2 pass | 2/2 pass |
| SKILL.md bytes | 20,726 | 21908 |
| Script LOC | 279 | 279 |

## Sweep 2 — rock 2: invariant checker catches drift

### S2 · completeness — KEPT — 35→78 — 6cd7f65
- Critique: checker only counted 1..56 (check_invariants.py:81-84); anchor typos, ⚡ drift, metadata drift all passed.
- Change: `canonical_anchors.txt` (from cli-website frontmatter); anchor-by-number check; ⚡ set check; metadata.version/category/tags vs manifests; description ≤1024; CONTRIBUTING "Principle Contract". Fixed real drift found: `metadata.category: coding` → `development`.
- Verified: category check failed before fix (rc=1); 4 manual mutations each fail with a clear message; clean → pass.
- Judge: KEEP — canonical list exact; 10 mutations caught; no false positives. Gaps: list length unchecked (extra line passes; deleted line → 46 cascading errors), titles unchecked, no unit tests.

### S2 · tests — KEPT — 0→62 — 3e4cd41
- Critique: zero tests for the checker; a broken rule would silently admit drift.
- Change: 11 subprocess tests on temp repo copies (one realistic mutation each); CI step in invariants job; CONTRIBUTING command.
- Verified: 11/11 pass (0.7s); disabling the ⚡ rule → 1 failure.
- Judge: KEEP — 23 rule mutations: main drift rules caught; NOT caught: SKILL metadata.tags, Part count, name equality, manifest key set/source/taxonomy, tag-at-HEAD.

### S2 · correctness — KEPT — 70→78 — 96f1d05
- Critique: extra canonical line passed silently; deleted line → 46 "#None" errors; titles (part of every citation) unchecked (check_invariants.py:96-101).
- Change: fixture renamed `canonical_principles.txt` with `anchor title`; length must equal SKILL.md count; titles compared (backticks/⚡ stripped). +5 tests (2 new rules; Part count, skill name, metadata.tags previously untested).
- Verified: 2 new tests failed on previous checker, pass now; 16/16 pass.
- Judge: KEEP — fixture identical to canonical. Minor: anchor-only fixture line → ValueError; backtick-stripping is lenient.

### S2 · reality — KEPT (gate)
- Verified: `python3 -m unittest discover -s .github/scripts` 16/16 OK; `check_invariants.py` pass; `validate_manifests.py` pass.

### Sweep 2 scorecard
| Lens | Score | Result |
| --- | --- | --- |
| completeness | 35→78 | KEPT |
| tests | 0→62 | KEPT |
| correctness | 70→78 | KEPT |
| reality | pass | KEPT |

| Metric | Baseline | S2 |
| --- | --- | --- |
| Tests | 0 | 16 (0.9s) |
| Rules mutation-caught | n/a | main drift rules + Part count, name, tags |
| Anchor / title match (enforced) | 44 / 29 (unenforced) | 56 / 56 (enforced) |
| Checks | 2/2 | 3/3 |
| Script LOC (check_invariants) | 210 | 253 |

### S2 note
- Lint: test file introduced 1 FURB167 (5→6, user-default ruff, no project config); cleared in S3 (→0).

## Sweep 3 — rock 3: simplify the toolchain

### S3 · simplify — KEPT — 70→80 — b90bf97
- Critique: many-skill scaffolding in a one-skill repo (directory scan with templates/.codegraph exclusions, TAXONOMY, catalog-wide versions; validate_manifests EXCLUDED scan).
- Change: both scripts address `cli-style` directly; one `version_tags` helper; non-semver version now fails; ruff clean (re.MULTILINE, executable shebangs). check_invariants 253→180, validate_manifests 69→60.
- Verified: 16/16 tests; both checks pass; `ruff check` clean.
- Judge: KEEP — tag behavior identical old vs new across 7 scenarios. Lost (acceptable for one skill): stray second plugin dir, extra README rows.

### S3 · architecture — CONVERGED — 88
- Two flat scripts (180 + 60 LOC), one fixture, one test file; no indirection left worth removing. Further change would be churn.

### S3 · docs/voice — KEPT — 70→82 — 822bd44
- Critique: tag errors printed raw tuples (`[(1, 2, 0)]`) and omitted the newer tag; CONTRIBUTING claimed a 1:1 directory scan the checker no longer does.
- Change: messages print `vX.Y.Z`; CONTRIBUTING states the enforced rule.
- Verified: scratch copy tagged v9.9.9 → both errors name v9.9.9; tests 16/16.
- Judge: KEEP — pass/fail unchanged; every CONTRIBUTING claim (lines 18–40) enforced.

### S3 · reality — KEPT (gate)
- Verified: tests 16/16 OK; check_invariants pass; validate_manifests pass.

### Sweep 3 scorecard
| Lens | Score | Result |
| --- | --- | --- |
| simplify | 70→80 | KEPT |
| architecture | 88 | CONVERGED |
| docs/voice | 70→82 | KEPT |
| reality | pass | KEPT |

| Metric | Baseline | S3 |
| --- | --- | --- |
| Tests | 0 | 16 |
| ruff findings | 5 | 0 |
| check_invariants LOC | 210 | 180 (while enforcing ~9 more rules) |
| validate_manifests LOC | 69 | 60 |
| Anchor / title match | 44 / 29 | 56 / 56 enforced |

### Convergence check (after S3)
All three ranked rocks are done; done signal met pending final gate and draft PR. Remaining backlog is low-impact or outside this repo → stop the loop and run the final bookend sweep.

## Final bookend sweep (lenses 5, 6, 10, 12, 13, 15)

### F · docs (link check) — KEPT — d2ac455
- Change: lychee now checks `cli-style/SKILL.md` (BRIEF-allowed CI edit).
- Judge: KEEP — CI-only, allowed, low risk. Bookend scores: architecture 88, simplify 85, ux 84, design/craft 90, docs/voice 80.

### F · docs/voice — KEPT — 78→87 — 2ad9286
- Critique: CHANGELOG omitted #4 (new rule) and restated 10/30/41/51; README Part VI clause garbled; validate_manifests docstring said "catalog".
- Change: three one-line fixes.
- Judge: KEEP — CHANGELOG matches SKILL.md diff; #30 "restated" slightly understates new requirements.

### F · architecture / simplify / ux / design — CONVERGED
- architecture 88 (remaining: fixture is a pinned copy; nothing re-derives it from cli-website), simplify 85 (checker 182 LOC vs ~120 target; remainder is release-tag logic kept on purpose), ux 84 (retryable column/key in sacred tables now has no backing principle), design/craft 90.
