# CLI Style — Agent Skill

**An elegant interface for a more automated age.**

The official [Agent Skill](https://cli.style/) for **[CLI Style](https://cli.style/)** — the 56-principle command-line design guide by **[Steve Francia (`spf13`)](https://github.com/spf13)**, creator of [Cobra](https://github.com/spf13/cobra), [Viper](https://github.com/spf13/viper), and [Hugo](https://github.com/gohugoio/hugo).

Every command-line application now has two readers: a **Human** at an interactive terminal and an **Agent** (or CI pipeline/script) running commands on a person's behalf. This skill equips coding agents to design, build, audit, and refactor command-line tools in any language against all 56 principles—including the 4 **⚡ Divergent** principles (`#32`, `#33`, `#39`, `#40`) where most otherwise-good applications break today.

- **Read the full guide:** [https://cli.style/](https://cli.style/)
- **Skill definition:** [`cli-style/SKILL.md`](./cli-style/SKILL.md)

## Skill Catalog

| Skill | What it covers | Install |
| --- | --- | --- |
| [`cli-style`](./cli-style/SKILL.md) | The 56 principles of dual-audience CLI design across 10 parts (Grammar, Convention, Outcome, Legibility, Output, Interaction, Failure, Time, Distribution, Trust), plus operational design/audit workflows, TTY detection matrix, standard flag vocabulary, and semantic exit codes. | `sage add spf13/cli-style` |

## Install

### Sage (`.agents` protocol — Claude, Gemini, Cursor, Copilot, Windsurf)

```bash
sage add spf13/cli-style
```

Don't have `sage` yet? Install it with `go install github.com/spf13/sage@latest`.

### Vercel / AgentSkills CLI (`npx skills`)

```bash
npx skills add spf13/cli-style
```

### Claude Code Plugin Marketplace

```text
/plugin marketplace add spf13/cli-style
/plugin install cli-style@cli-style
```

### Manual / Symlink (`.agents/skills`)

Clone this repository and link `cli-style` into your agent's skills directory.

On macOS and Linux:

```bash
ln -s "$PWD/cli-style" "$HOME/.agents/skills/cli-style"
```

On Windows (PowerShell):

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.agents\skills\cli-style" -Target "$PWD\cli-style"
```

## What This Skill Teaches Your Agent

1. **Part I · Grammar (`01`–`07`):** Sentence structure (`app <noun> <verb> <target> [--modifiers]`), subcommands over mode flags, plural nouns, shared verbs, single positional target, and `--` handling.
2. **Part II · Convention (`08`–`15`):** Zero-flag default path, universal flag meanings, POSIX/GNU short & long flag mechanics, the 6-level configuration precedence contract, XDG paths, `-` for stdio, and filter composition.
3. **Part III · Outcome (`16`–`21`):** Outcome-oriented flag names (`--preview` over `--dry-run`, `--overwrite` over `--force`), single-word names, concrete state diffs, idempotency, 4-tier destructive confirmation (`--yes` vs `--confirm <id>`), and read-only safety.
4. **Part IV · Legibility (`22`–`27`):** Dynamic shell completions, self-documenting command trees, real examples in every `--help`, exit `0` on help vs `2` on misuse, and `--json` support on `version` and `help`.
5. **Part V · Output (`28`–`37`):** Strict `stdout`/`stderr` separation, token-conscious output budgets, `--json` and `--plain` contracts, **⚡ `#32` Color is an enhancement**, **⚡ `#33` Progress on stderr only for a TTY**, responsive status on slow operations, zero-match empty states, line-oriented records, and pagination bounds.
6. **Part VI · Interaction (`38`–`41`):** Flag equivalents for every prompt, **⚡ `#39` Independent per-stream TTY detection**, **⚡ `#40` Prompt at a TTY / fail fast in automation**, and signal trapping (`130`/`143`) for clean terminal exit.
7. **Part VII · Failure (`42`–`48`):** Precondition checks and typo suggestions, actionable recovery commands in every error, semantic exit codes (`0`–`5`), no raw stack traces, structured JSON errors on `stderr`, explicit `retryable` metadata, and atomic writes.
8. **Part VIII · Time (`49`–`51`):** Additive evolution, dated deprecations on `stderr`, and immutable JSON schemas within a major version.
9. **Part IX · Distribution (`52`–`53`):** Single static binaries and explicit `app upgrade` (never mid-command auto-update).
10. **Part X · Trust (`54`–`56`):** Zero secrets in argv/flags (`--token-stdin`, `--token-file`, env), network transparency (`--offline`, `DO_NOT_TRACK=1`), and strict filesystem boundaries.

## Companion Go Skills

Building your CLI in Go with **Cobra** and **Viper**? Install [`spf13/go-skills`](https://github.com/spf13/go-skills) alongside `cli-style` for idiomatic Go and factory-built Cobra command architecture:

```bash
sage add spf13/go-skills
```

## License

© 2026 Steve Francia (`spf13`), spf13 labs LLC, and contributors.

- **Guide & Skill Text (`cli-style/SKILL.md`):** [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) with an explicit **AI Agent Installation & Execution Grant** permitting use in commercial and enterprise software development.
- **Packaging, Scripts & Generated Code:** [MIT](./LICENSE).

See [LICENSE](./LICENSE) for full details.
