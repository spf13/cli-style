# Changelog

All notable changes to `spf13/cli-style` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-14

### Added

- Initial public release of the `cli-style` Agent Skill covering all 10 Parts and 56 Principles of [CLI Style](https://cli.style/).
- Operational workflows for designing new CLIs and running structured CLI Style audits with `#anchor` citations.
- Quick-reference implementation contracts: per-stream TTY & environment matrix (`#32`, `#33`, `#39`, `#40`), reserved flag vocabulary, semantic exit code table (`0`–`5`, `130`, `143`), and structured `stderr` JSON error envelope.
- Packaging manifests for `sage` (`.agents` protocol), `npx skills` (AgentSkills spec), and the Claude Code Plugin Marketplace (`.claude-plugin/`).
