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
