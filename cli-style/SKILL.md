---
name: cli-style
description: >
  CLI and Agent-Experience (AX) design system by Steve Francia (spf13), creator of
  Cobra, Viper, and Hugo. Enforces the 56 principles of CLI Style across 10 parts—unifying
  human ergonomics and agent safety via per-stream TTY detection, typed streams, and
  semantic exit codes. Activate when designing, building, auditing, or refactoring CLIs,
  subcommands, flags (--preview, --json, --no-color, --yes), config precedence, stdout/stderr,
  or CLI frameworks (Cobra, Viper, pflag, clap, click, typer, argparse, commander, oclif).
license: CC-BY-NC-ND-4.0
metadata:
  category: coding
  tags: "cli, design-system, agent-experience, developer-tools, terminal, ux"
  author: Steve Francia (steve.francia@gmail.com)
  version: "1.1.0"
  canonical: https://cli.style/
---

# CLI Style — The 56 Principles of Dual-Audience CLI Design

Canonical reference: **https://cli.style/** · Author: **Steve Francia (`spf13`)** (creator of Cobra, Viper, and Hugo)

Every CLI now has two readers: a **Human** at an interactive terminal and an **Agent** (or CI/script) invoking it programmatically.
- **52 principles** are identical for both readers.
- **4 principles (`#32`, `#33`, `#39`, `#40`)** are **⚡ Divergent** and must branch per-stream via TTY detection.

---

## Operational Workflows

### Workflow A · Designing or Building a CLI

- [ ] **1. Grammar & Tree (`#01`–`#07`):** Map capabilities to `app <noun> <verb> <target> [--modifiers]` with a short typeable name and a few shared verbs across many nouns (`create`, `get`, `list`, `describe`, `update`, `delete`, `run`, `preview`). Use subcommands, never mode flags.
- [ ] **2. Flags & Config (`#08`–`#15`):** Require zero flags and zero config files on the common path. Reserve standard flags (`--json`, `--plain`, `--preview`, `--yes`, `-q/--quiet`, `-v/--verbose`, `--no-color`, `--no-input`). Enforce precedence: `flags > env (APP_*) > project > user (XDG) > system > defaults`.
- [ ] **3. Blast Radius (`#16`–`#21`):** Classify mutations by recovery cost (`#20`: Undoable, Recoverable, Unrecoverable, Catastrophic) and wire `--preview` (concrete diff), `--yes`, or `--confirm <name>`.
- [ ] **4. Streams & TTY (`#28`–`#41`):** Send data strictly to `stdout` and diagnostics/progress/prompts/errors strictly to `stderr`. Check `isatty` independently on `stdin`, `stdout`, and `stderr`. Provide flag equivalents for every prompt.
- [ ] **5. Errors & Help (`#22`–`#27`, `#42`–`#48`):** Return semantic exit codes (`0`–`5`, `130`, `143`), include the fix command in every error, emit JSON errors on `stderr` under `--json`, and include 2–3 examples in every `--help`.

> **Go / Cobra & Viper:** Use **[Cobra](https://github.com/spf13/cobra)**, **[Viper](https://github.com/spf13/viper)**, and **[pflag](https://github.com/spf13/pflag)**. Pair with the optional `cobra-viper` skill (`sage add spf13/go-skills/cobra-viper` or `/plugin install cobra-viper@go-skills`).

### Workflow B · Auditing an Existing CLI

1. **Check the 4 ⚡ Divergent traps first (`#32`, `#33`, `#39`, `#40`)** — hanging `stdin` prompts in non-TTY, spinners on piped streams, or unguarded ANSI color.
2. **Verify Stream & Exit Code contracts (`#28`, `#30`, `#44`, `#46`)** — confirm `app ... --json | jq .` works on success, empty results, and errors.
3. **Check Grammar, Flags & Trust (`#01`–`#21`, `#54`–`#56`)** — noun-verb order, outcome flags (`--preview` vs `--dry-run`), secret flags, and XDG paths.
4. **Output a structured Audit Report:**

```markdown
## CLI Style Audit: `<app>`
- **Critical (Breaks Agents / Pipes):** <N> | **Major (Safety / Ergonomics):** <N> | **Minor (Polish):** <N>

1. **[CRITICAL] #40 When interactive, prompt rather than fail (`#prompts-are-courtesy`)**
   - **Location:** `cmd/delete.go` (`app clusters delete`)
   - **Problem:** Prompts on `stdin` without checking `isatty(stdin)`, hanging non-interactive callers.
   - **Fix:** Check `isatty(stdin) && isatty(stderr)`. When non-interactive without `--confirm <id>`, exit `2` and print the required flag on `stderr`.
```

---

## Part I · Grammar (01–07)
*How a command is shaped before it is run.*

1. **Speak in sentences.** (`#speak-in-sentences`)
   `app <noun> <verb> <target> [--modifiers]`. E.g., `app clusters restart prod-2 --preview`. Keep order consistent across the application.
2. **Use subcommands, not mode flags.** (`#structure-over-state`)
   Use the subcommand tree for actions and sub-domains instead of mode flags (`app auth login`, never `app --login`).
3. **Make invalid combinations impossible.** (`#unrepresentable`)
   Scope flags to the subtree that owns them. Split conflicting actions into separate subcommands (`app backups restore` vs `app backups schedule`), collapse mutually exclusive formats into one valued flag (`--output json`), and define deterministic precedence where shorthand flags like `-q` and `-v` coexist.
4. **Name the application for typing.** (`#name-for-typing`)
   Short, lowercase, no punctuation, easy to say (`app`, never `AppCloud_CLI-v2`). It will be typed thousands of times. Check that it doesn't shadow a command already on a normal system (`test`, `open`).
5. **Few verbs, many nouns.** (`#verbs-are-verbs`)
   Keep a small shared verb vocabulary (`create`, `get`, `list`, `describe`, `update`, `delete`, `run`, `preview`) across every resource.
6. **The target is positional; everything else is a flag.** (`#positional-arguments`)
   The named resource (`prod-2`) is positional. Options, filters, and settings are flags (`--region us-east-1 --nodes 3`). Never require multiple positional arguments whose order must be memorized.
7. **Honor `--`, the end of flags.** (`#end-of-flags`)
   Everything after `--` is passed verbatim as positional arguments (`pflag` handles this automatically).

---

## Part II · Convention (08–15)
*What a caller is entitled to expect without asking.*

8. **Convention over configuration.** (`#convention-over-configuration`)
   The common path takes zero flags. Every required flag on the default path is a decision you failed to make.
9. **One flag, one meaning, everywhere.** (`#one-flag-one-meaning`)
   Standard flags keep their universal meaning across every subcommand: `-h/--help`, `-v/--verbose`, `-q/--quiet`, `-n/--preview`, `-y/--yes`, `-o/--output`, `-f/--file`, `--json`, `--no-color`.
10. **Long flags are for scripts; short flags are for hands.** (`#long-flags-first`)
    Long flags (`--verbose`) go in scripts, runbooks, and issue comments because they explain themselves. Short flags (`-v`) are for the handful of options typed daily and spend a tiny, permanent namespace, so allocate them carefully. Support `--flag=value`, `--flag value`, and combined short booleans (`-abc`).
11. **Precedence is a contract.** (`#precedence-is-a-contract`)
    `flags > environment > project config > user config > system config > defaults`. Provide provenance inspection (`app config get region --origin`).
12. **Match configuration to lifespan.** (`#configuration-by-lifespan`)
    One-off overrides belong in flags; session/CI context in `APP_*` environment variables; durable team/personal settings in config files.
13. **Put configuration where the platform says.** (`#config-file-location`)
    Respect `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, and `XDG_STATE_HOME` when set, and platform defaults (`~/.config/app/`, `~/Library/Application Support/app/`, `%APPDATA%\app\`). Never drop new dotfiles in `$HOME`.
14. **Run with no configuration at all.** (`#run-without-config`)
    A fresh install on an empty machine must do something useful (`app status` works on sensible defaults). Config files are an optimization for repeat users, never a prerequisite: `Error: config.toml not found; run app init first` is a failure.
15. **Read stdin, write stdout; compose.** (`#be-a-filter`)
    Read newline-delimited targets or records from `stdin` and write clean records to `stdout` so commands compose with `jq`, `xargs`, and pipes.

---

## Part III · Outcome (16–21)
*What a command does to the world, and how it says so.*

16. **Name the outcome, not the mechanism.** (`#name-the-outcome`)
    `--preview` over `--dry-run`; `--overwrite` over `--force`. Name flags after what happens to the user's state.
17. **Use one word whenever possible.** (`#one-word-names`)
    Single-word commands and flags (`--preview`, `--fresh`, `--unchecked`, `--overwrite`) are easier to type and eliminate hyphenation ambiguity (`--no-cache` vs `--nocache`).
18. **Show the change, not the summary.** (`#preview-is-a-diff`)
    `--preview` must show the concrete delta (`~ cluster prod-2: nodes 3 -> 5`), not a vague count (`Would update 1 cluster`).
19. **Be idempotent, or refuse.** (`#idempotent-or-refuse`)
    Re-running a command should converge to the target state or fail cleanly before mutating. Support `--idempotency-key` or `--if-match` where applicable.
20. **Match confirmation to consequences.** (`#destruction-is-deliberate`)
    Scale friction to recovery cost: **Undoable** (run immediately, zero prompts), **Recoverable** (run by default, support `--preview`), **Unrecoverable** (confirm `y/N` at TTY or `--yes` in automation), **Catastrophic** (print blast radius and require naming the target via `--confirm prod-2`, never a blanket `--yes`).
21. **Do only what the name promises.** (`#least-surprise`)
    Read-only verbs (`get`, `list`, `describe`, `status`, `diff`, `help`, `version`) must never mutate state, write config, or phone home.

---

## Part IV · Legibility (22–27)
*How an application teaches itself to whoever is holding it.*

22. **Recognition over recall.** (`#recognition-over-recall`)
    Provide dynamic shell completions (`app completion bash|zsh|fish|powershell`) for subcommands, flags, and live resource names.
23. **Make the application self-documenting.** (`#self-documenting`)
    Generate help text, examples, completions, and man pages from the single command definition so documentation never drifts from the binary.
24. **Put real examples in every command's help.** (`#lead-with-examples`)
    Every command's `--help` must include 2–3 copy-pasteable invocations covering the common case, a preview/flag case, and a piped/advanced case.
25. **Help everywhere.** (`#help-everywhere`)
    Bare `app` prints concise help and exits `0`. Support `app help <cmd>`, `-h` (terse), and `--help` (complete) at every depth. Requested help exits `0`; usage error exits `2`.
26. **Version and capability are queryable.** (`#version-and-schema`)
    Provide `app version` and `app help` subcommands, and support `--json` on both (`app version --json`, `app help clusters --json`) so agents can inspect capabilities without scraping prose.
27. **End help with where to go next.** (`#point-to-the-fuller-docs`)
    End `--help` with a stable, versioned URL to the web documentation for that command.

---

## Part V · Output (28–37)
*What goes on which stream, and in what shape.*

28. **Streams are typed.** (`#streams-are-typed`)
    `stdout` is strictly for requested data, records, and `--json` payloads. `stderr` carries all diagnostics, progress, warnings, prompts, and errors.
29. **Print less than you think you should.** (`#output-is-a-budget`)
    Default output is concise (human attention and agent context tokens are both scarce). Use `--verbose` for detail and `--quiet` for silence.
30. **Machine output is a mode, not a fallback.** (`#machine-output-first-class`)
    Support `--json` on every command that returns data, including errors. Generate it from the same values as the human rendering, not a separate code path, and keep `stdout` parseable by `jq` with zero banners or trailing commentary.
31. **Say little on success.** (`#say-nothing-on-success`)
    Print what was produced, or print nothing (`deleted key deploy-ci`, not `Successfully deleted key "deploy-ci"! Operation completed without errors.`). The exit code already says it worked.
32. **Color is an enhancement, never information. ⚡ Divergent** (`#color-is-enhancement`)
    Every status conveyed by color must also be carried by a word or symbol (`✓ healthy`, `✗ degraded`). Disable ANSI color when `stdout` is not a TTY, `NO_COLOR` is set, `TERM=dumb`, or `--no-color` is passed.
33. **Progress goes on stderr, and only for a terminal. ⚡ Divergent** (`#progress-on-stderr`)
    Render spinners/progress bars on `stderr` only when `stderr` is an interactive TTY. When non-interactive, suppress redraws and emit at most discrete phase transitions on `stderr`.
34. **Communicate responsively.** (`#respond-quickly`)
    Silence on a slow operation looks identical to a hung process or blocked `stdin`. Emit status updates on `stderr` when waiting on network/locks, and support `--timeout`.
35. **Design the empty result.** (`#empty-states`)
    Zero matches exits `0`. Print `"No clusters in eu-west-1."` at a TTY, `[]` under `--json`, and 0 bytes when piped as plain text (`wc -l` == `0`).
36. **Keep plain output line-oriented.** (`#line-oriented`)
    In non-JSON text mode, emit one item per line without ASCII box-drawing borders so `grep`, `awk`, `sort`, and `wc -l` work directly.
37. **Stream results as you get them.** (`#stream-dont-buffer`)
    Emit records as they arrive instead of buffering everything to print a perfectly aligned table at the end. Incremental output can be watched, piped into a running pipeline (`app logs tail prod-2 | grep --line-buffered ERROR`), and interrupted usefully.

---

## Part VI · Interaction (38–41)
*When to converse, when to execute, and how to tell the difference.*

38. **Every prompt has a flag equivalent.** (`#nothing-interactive-only`)
    Every prompt, wizard step, confirmation, or `$EDITOR` message must have a flag equivalent (`--name`, `--region`, `--message`, `--yes`) so CI and agents can run any workflow in one non-interactive command.
39. **Detect the terminal; never assume one. ⚡ Divergent** (`#detect-the-tty`)
    Check `isatty` independently on `stdin`, `stdout`, and `stderr`. Provide `--interactive` and `--no-input` (plus `CI=true` detection) as explicit overrides.
40. **When interactive, prompt rather than fail. ⚡ Divergent** (`#prompts-are-courtesy`)
    - **Human (TTY)**: When required arguments are missing at an interactive terminal, prompt for them and print the reusable command (`Hint: next time run ...`).
    - **Agent (No TTY)**: Never block on `stdin`. Fail immediately with exit code `2` and name the missing flag.
41. **Exit promptly when interrupted.** (`#handle-interrupts`)
    Ctrl-C means now. On `SIGINT`/`SIGTERM`, clean up temp files and partial writes, restore cursor visibility, echo, and raw mode, then exit (`130` on `SIGINT`, `143` on `SIGTERM`). Ignoring the first interrupt teaches users to reach for a signal that skips cleanup.

---

## Part VII · Failure (42–48)
*How to break cleanly, legibly, and recoverably.*

42. **Fail forgivingly.** (`#fail-forgivingly`)
    Check preconditions before mutating state. On typos in commands or flags, suggest the closest valid match (`Did you mean "restart"?`) on `stderr` and exit `2`.
43. **Errors say what to do next.** (`#errors-say-what-next`)
    State what failed, why, and the exact command or flag that fixes it (`Run: app auth login --cluster prod-2`).
44. **Exit codes are part of your API.** (`#exit-codes-are-api`)
    Use distinct, documented codes: `0` success, `1` runtime failure, `2` invalid usage/flags, `3` auth/permission failure, `4` resource not found, `5` conflict/precondition failure.
45. **One sentence first, detail underneath.** (`#one-error-then-detail`)
    The first line names what failed in the user's terms (`Error: could not reach cluster "prod-2" (connection timed out after 5s)`). Stack traces, request IDs, and internal context go underneath or behind `--verbose`/`--debug`.
46. **Errors have a machine form too.** (`#errors-in-machine-form`)
    When `--json` is passed, emit structured JSON errors on `stderr` (`{"error":{"code":"AUTH_REQUIRED","message":"...","run":"..."}}`).
47. **An unexpected crash asks to be reported.** (`#crashes-ask-to-be-reported`)
    When the failure is your bug, not the user's mistake, say so plainly and print the version, platform, triggering command, and an issue URL (`Crash: internal panic in app v2.4.1 (linux/amd64, commit a8f3c1)`). Keep "you did something wrong" distinct from "we did something wrong."
48. **Make state changes atomic.** (`#never-half-write`)
    Write files via temp-file + atomic rename in the same directory. Multi-step mutations should roll back cleanly or record a resumable checkpoint.

---

## Part VIII · Time (49–51)
*How an application ages without breaking callers.*

49. **Add, don't subtract.** (`#only-add`)
    Keep old subcommands and flags working as aliases. Scripts and LLM training weights remember old syntax for years.
50. **Deprecate with a date and a migration plan.** (`#deprecate-with-a-date`)
    Warn on `stderr` with what is deprecated, the removal date, and the exact replacement (`Warning: --region-id will be removed on 2027-06-01; use --region instead.`).
51. **The machine format is the strictest promise you make.** (`#machine-format-is-strictest`)
    Human output can be redesigned; structured output cannot. Adding a key is safe. Removing, renaming, retyping, or reordering an array that carries meaning breaks callers silently. Version the format if you must change it, and serve both.

---

## Part IX · Distribution (52–53)
*How the application arrives and stays current.*

52. **Ship one file that runs anywhere.** (`#single-binary`)
    Zero runtime interpreter or shared-library dependencies. Publish checksums and archives for Linux, macOS, and Windows (`amd64` + `arm64`) and native package managers.
53. **As easy to remove as to install.** (`#easy-to-remove`)
    Document what you write and where. Keep everything in predictable places so deleting the binary and its config/cache directories removes the application completely (`rm /usr/local/bin/app && rm -rf ~/.config/app ~/.cache/app`).

---

## Part X · Trust (54–56)
*What an application owes the machine it runs on.*

54. **Secrets never come from arguments.** (`#secrets-never-in-arguments`)
    Flags appear in `ps`, shell history, and agent transcripts. Accept secrets via `--token-stdin`, `--token-file`, credential helpers, or environment variables.
55. **Be honest about what leaves the machine.** (`#be-honest-about-the-network`)
    Document network calls, support `--offline` where local execution is possible, and honor `DO_NOT_TRACK=1` and `--no-telemetry`.
56. **Write only where you were asked to write.** (`#write-only-where-asked`)
    Never create unrequested files outside your designated config/cache/state directories or explicit output paths, and clean up temporary files on exit.

---

## Quick-Reference Implementation Contracts

### 1. Per-Stream TTY & Environment Matrix (`#32`, `#33`, `#39`, `#40`)

| Signal / Condition | `stdout` | `stderr` | `stdin` / Prompts |
| --- | --- | --- | --- |
| All 3 streams are TTY | Aligned table, ANSI color | Spinners, progress bars, hints | Prompt for missing args (`#40`) & confirmations |
| `stdout` piped (`app list \| jq`), `stderr` TTY | Line records (or JSON if `--json`), **no ANSI** | Spinners/warnings allowed on `stderr` | Prompt only if `stdin` & `stderr` are TTY |
| `NO_COLOR != ""` or `TERM=dumb` or `--no-color` | Strip ANSI escapes; keep symbols (`✓`/`✗`) | Strip ANSI escapes | Unchanged |
| `CI=true` or `--no-input` or `!isatty(stdin)` | Unchanged | No spinners; discrete phase lines only | **Never read `stdin`**; exit `2` naming missing flag |
| `--json` passed | Valid JSON (`{}` or `[]`), zero prose | JSON error object on failure (`#46`); no spinners | Non-interactive unless `--interactive` is set |

### 2. Reserved Flag Vocabulary (`#09`, `#10`, `#16`, `#17`)

| Flag | Short | Purpose |
| --- | --- | --- |
| `--help` / `--version` | `-h` | Show help (`-h` terse, `--help` full with examples) or version and exit `0` |
| `--json` / `--plain` | | Machine JSON on `stdout` (JSON errors on `stderr`) / headerless tab-separated records |
| `--output <fmt>` | `-o` | Output format (`table`, `json`, `yaml`, `plain`) |
| `--file <path>` | `-f` | Input/manifest file path (`-` = `stdin`/`stdout`) |
| `--preview` | `-n` | Show concrete state diff without mutating (prefer over `--dry-run`) |
| `--yes` / `--confirm <id>` | `-y` | Confirm Tier 3 unrecoverable (`--yes`) or Tier 4 catastrophic (`--confirm <id>`) actions |
| `--quiet` / `--verbose` / `--debug` | `-q` / `-v` | Silence non-essential output (`-v` wins if combined with `-q`) / expand detail / emit traces |
| `--no-color` / `--no-input` / `--timeout <d>` | | Disable ANSI color / disable prompts (exit `2` if missing) / bound execution time |

### 3. Semantic Exit Codes & JSON Error Envelope (`#41`, `#43`, `#44`, `#46`)

| Code | Meaning | Retryable? |
| --- | --- | --- |
| `0` | Success (`--help`, `--version`, `--preview`, and empty results exit `0`) | N/A |
| `1` | General runtime or upstream failure | See `retryable` |
| `2` | Invalid usage, unknown flag, or missing required input in non-TTY | `false` |
| `3` | Authentication or permission failure | `false` |
| `4` | Target resource not found | `false` |
| `5` | Conflict, precondition failure, or idempotency violation | `false` |
| `130` / `143` | Interrupted by `SIGINT` (`130`) or `SIGTERM` (`143`) — terminal restored | `true` |

When `--json` fails, `stdout` stays empty and `stderr` receives:

```json
{"error":{"code":"AUTH_EXPIRED","exit_code":3,"message":"Credentials expired for \"prod-2\".","run":"app auth login --cluster prod-2","retryable":false}}
```

---

*© 2026 Steve Francia (spf13), spf13 labs LLC, and contributors · CC BY-NC-ND 4.0 (with Agent Execution & MIT Code Grant) · https://cli.style/*
