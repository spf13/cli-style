# CLI Style (`spf13/cli-style`) — Agent Instructions

Canonical repository for the **CLI Style** (`https://cli.style/`) 56-principle dual-audience command-line design system and Agent Skill (`cli-style/SKILL.md`) by Steve Francia (`spf13`).

## Repository Layout

- `cli-style/SKILL.md`: The canonical `cli-style` skill definition enforcing all 56 principles across 10 parts.
- `.claude-plugin/marketplace.json`: Claude Code plugin marketplace manifest.

---

## Agent & Skill Ecosystem Integration (`dotagents` + `sage`)

### Architecture Map

- **`~/code/steve-skills`, `~/code/go-skills`, `~/code/cli-style`**: Canonical source repositories for Steve's authored skills (`D:\MyFiles\code\<repo>` on `galactus`, `/share/steve/code/<repo>` on `factory`, `~/code/<repo>` on `wandamax`).
- **`~/.agents` (`github.com/spf13/dotagents`, and `/share/steve/code/dotagents` in Orca on `factory`)**: Canonical multi-harness configuration repository (`sage.yaml`, `AGENTS.md`, `agents/`, `omp/`, `claude/`, `mcp/`).
- **`~/code/sage` (`github.com/spf13/sage`)**: CLI sync engine (`sage sync`) that links `~/code/<repo>/<skill>` into `~/.agents/skills/`, `~/.gemini/config/skills/`, and `~/.omp/agent/skills/`, and propagates `AGENTS.md` (`RULES.md`, `GEMINI.md`, `CLAUDE.md`), `agents/`, `omp/`, `claude/`, and `mcp/` across all harnesses.

### Mandatory Sync & Reload Protocol on Every Update

1. **Editing an existing skill (`cli-style/SKILL.md`)**:
   - Skills are symlinked (`~/.agents/skills/cli-style -> ~/code/cli-style/cli-style`), so edits are live immediately on the current machine.
   - Commit & push to `origin/main`, then pull on remote hosts:
     ```bash
     ssh factory "git -C /share/steve/code/cli-style pull --ff-only"
     ssh wandamax "git -C ~/code/cli-style pull --ff-only"
     ```
2. **Adding, renaming, or removing a skill**:
   - Run `sage sync` locally (auto-discovers new skills in `~/code/cli-style` and records portable `local_path: ~/code/cli-style` in `~/.agents/sage.yaml`).
   - Commit & push both `cli-style` (`origin/main`) AND `~/.agents` (`spf13/dotagents` `origin/master`).
   - Sync remote hosts so new symlinks and manifests materialize everywhere:
     ```bash
     ssh factory "git -C /share/steve/code/cli-style pull --ff-only && git -C /root/.agents pull --ff-only && git -C /share/steve/code/dotagents pull --ff-only && sage sync"
     ssh wandamax "git -C ~/code/cli-style pull --ff-only && git -C ~/.agents pull --ff-only && ~/go/bin/sage sync"
     ```
3. **Updating `sage` itself (`~/code/sage`)**:
   - Run `go test ./... && go install .`, commit & push `origin/master`, then install on `factory` and `wandamax`:
     ```bash
     ssh factory "cd /share/steve/code/sage && git pull --ff-only && go install . && cp /root/go/bin/sage /usr/local/bin/sage"
     ssh wandamax "cd ~/code/sage && git pull --ff-only && go install ."
     ```
