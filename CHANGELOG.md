# Changelog

All notable changes to `spf13/cli-style` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-04

### Changed

- Aligned every principle's number, title, and `#anchor` in `cli-style/SKILL.md` with the canonical guide at [cli.style](https://cli.style/). Twelve anchors that did not exist on the site were replaced; update any saved citations:

  | # | Old anchor | New anchor |
  | --- | --- | --- |
  | 4 | `#nouns-are-plural` | `#name-for-typing` |
  | 10 | `#posix-mechanics` | `#long-flags-first` |
  | 14 | `#dash-for-stdio` | `#run-without-config` |
  | 19 | `#be-idempotent` | `#idempotent-or-refuse` |
  | 30 | `#structured-output` | `#machine-output-first-class` |
  | 31 | `#tables-for-eyes` | `#say-nothing-on-success` |
  | 37 | `#bound-the-output` | `#stream-dont-buffer` |
  | 41 | `#clean-terminal-exit` | `#handle-interrupts` |
  | 45 | `#no-stack-traces` | `#one-error-then-detail` |
  | 47 | `#retry-safety` | `#crashes-ask-to-be-reported` |
  | 51 | `#json-contract` | `#machine-format-is-strictest` |
  | 53 | `#update-yourself` | `#easy-to-remove` |

- Principles 4, 14, 31, 37, 45, 47, and 53 now teach the canonical rules (name the application for typing, run with no configuration, say little on success, stream instead of buffer, one sentence first, report crashes, easy to remove). Principles 10, 30, 41, and 51 are restated to match the canonical text.

## [1.0.0] - 2026-10-14

### Added

- Initial public release of the `cli-style` Agent Skill covering all 10 Parts and 56 Principles of [CLI Style](https://cli.style/).
- Operational workflows for designing new CLIs and running structured CLI Style audits with `#anchor` citations.
- Quick-reference implementation contracts: per-stream TTY & environment matrix (`#32`, `#33`, `#39`, `#40`), reserved flag vocabulary, semantic exit code table (`0`–`5`, `130`, `143`), and structured `stderr` JSON error envelope.
- Packaging manifests for `sage` (`.agents` protocol), `npx skills` (AgentSkills spec), and the Claude Code Plugin Marketplace (`.claude-plugin/`).
